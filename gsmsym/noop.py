"""Build our GSM-NoOp clauses (Apple did not release GSM-NoOp).

For each official GSM-Symbolic instance, a generator model writes ONE sentence that sounds relevant,
contains a number, and does not change the answer (the paper's Fig. 7 recipe). Two other models then
judge independently whether the sentence leaves the answer unchanged. We publish only the sentences
(our text) and the judgements; the harness inserts each sentence before the final question sentence
of the official item at run time, so no modified copy of the CC BY-NC-ND data is redistributed.

Usage: python -m gsmsym.noop generate --instances 0-9
       python -m gsmsym.noop judge --instances 0-9
"""
import argparse
import json
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from . import routes
from .data import NOOP, _rows, gold, insert_clause
from .models import MODELS
from .run import parse_instances

GENERATOR = "mistral-large-4"
JUDGES = ("gpt-oss-120b", "nemotron-3-ultra")

GEN_PROMPT = """You are helping build a robustness test for math word problems.

Problem:
{q}

Correct answer: {a}

Write ONE extra sentence to insert into this problem just before its final question. The sentence must:
- mention a specific number and sound relevant to the story (for example, a detail about some of the items, people or events),
- leave the correct answer exactly unchanged: it must not add, remove or alter any quantity the solution uses, and a careful solver must be able to ignore it,
- not contradict the problem, not ask a question, and not mention that it is irrelevant.

Example of the style: "...but five of them were a bit smaller than average."

Reply with only the sentence."""

JUDGE_PROMPT = """A sentence was inserted into a math word problem.

Original problem:
{q}

Inserted sentence:
{c}

Original correct answer: {a}

Question: read literally and in its most natural interpretation, does the inserted sentence leave the correct answer unchanged at {a}? Reply with exactly one word: UNCHANGED if a careful solver should still answer {a}, or CHANGED if the sentence alters or makes ambiguous the quantities the answer depends on."""


def _call(model, prompt, max_tokens):
    m = MODELS[model]
    return routes.alcf(m["id"], prompt, cluster=m["cluster"], max_tokens=max_tokens, stop=None)[0]


def _clean(s):
    s = s.strip().strip('"').strip()
    s = re.sub(r"^(sentence|inserted sentence)\s*:\s*", "", s, flags=re.I).strip().strip('"')
    return s.splitlines()[0].strip() if s else s


def load():
    return {(r["id"], r["instance"]): r for r in map(json.loads, open(NOOP))} if NOOP.exists() else {}


def save(rows):
    NOOP.parent.mkdir(parents=True, exist_ok=True)
    with open(NOOP, "w") as f:
        for k in sorted(rows):
            f.write(json.dumps(rows[k]) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["generate", "judge"])
    ap.add_argument("--instances", default="0-4")
    ap.add_argument("--workers", type=int, default=16)
    a = ap.parse_args()
    inst = parse_instances(a.instances)
    rows = load()
    lock = threading.Lock()
    src = [r for r in _rows("symbolic") if r["instance"] in inst]

    def gen(r):
        k = (r["id"], r["instance"])
        if k in rows:
            return
        g = gold(r["answer"])
        ans = int(g) if g == int(g) else g
        try:
            c = _clean(_call(GENERATOR, GEN_PROMPT.format(q=r["question"], a=ans), 400))
        except routes.RouteError as e:
            print("gen error", k, e, file=sys.stderr)
            return
        if not c or not re.search(r"\d|\b(one|two|three|four|five|six|seven|eight|nine|ten|dozen|half)\b", c, re.I):
            c_ok = False
        else:
            c_ok = True
        with lock:
            rows[k] = {"id": r["id"], "instance": r["instance"], "clause": c, "has_number": c_ok,
                       "generator": MODELS[GENERATOR]["id"], "judges": {}, "keep": True}

    def judge(r):
        k = (r["id"], r["instance"])
        row = rows.get(k)
        if not row:
            return
        g = gold(r["answer"])
        ans = int(g) if g == int(g) else g
        for j in JUDGES:
            if MODELS[j]["id"] in row["judges"]:
                continue
            try:
                out = _call(j, JUDGE_PROMPT.format(q=r["question"], c=row["clause"], a=ans), 2048)
            except routes.RouteError as e:
                print("judge error", k, j, e, file=sys.stderr)
                continue
            words = re.findall(r"\b(UNCHANGED|CHANGED)\b", out.upper())
            with lock:
                row["judges"][MODELS[j]["id"]] = words[-1] if words else "UNPARSED"

    fn = gen if a.cmd == "generate" else judge
    with ThreadPoolExecutor(a.workers) as ex:
        for i, _ in enumerate(ex.map(fn, src)):
            if i % 200 == 199:
                with lock:
                    save(rows)
                print(f"  {i + 1}/{len(src)}", file=sys.stderr)
    save(rows)
    print(f"{len(rows)} clauses stored", file=sys.stderr)


if __name__ == "__main__":
    main()
