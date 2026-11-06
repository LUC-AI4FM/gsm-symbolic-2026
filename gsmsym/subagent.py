"""Claude models through Claude Code subagents (not the API).

Each batch holds one variant and one instance set for up to 50 different templates, so a batch never
shows two instances of the same template. The batch prompt carries the paper's header and 8 shots once,
then each problem in the paper's `Q: ... A: Let's think step by step.` format under a `### <custom_id>`
marker. The subagent must answer by reasoning only (no tools); batches whose transcript shows any tool
use other than the final hand-off are discarded.

  python -m gsmsym.subagent make  --variant symbolic --instances 0-1     -> batches/<batch_id>.txt
  python -m gsmsym.subagent ingest --model claude-haiku-subagent          -> runs/<model>/raw.jsonl
"""
import argparse
import json
import re
from pathlib import Path

from .data import HEADER, ROOT, SHOTS, items
from .run import parse_instances

BATCHES = ROOT / "batches"
SIZE = 50

RULES = """Rules for this task:
- Answer by reasoning only. Do not run code and do not use Bash, file, web or any other tool. The only
  tool call allowed is the final hand-off that returns your answer.
- Solve every problem independently, in order.
- For each problem, write its marker line exactly as given (for example `### 0012-symbolic-03`), then on the next
  line continue the answer in the style of the examples: `A: Let's think step by step. <reasoning>. The final answer is <number>.`
- Write nothing else: no introduction, no summary, no tables.
"""


def few_shot():
    lines = [HEADER, ""]
    for q, a, final in SHOTS:
        lines.append(f"Q: {q}\nA: Let's think step by step. {a}. The final answer is {final}.\n")
    return "\n".join(lines)


def make(variant, instances):
    BATCHES.mkdir(exist_ok=True)
    by_inst = {}
    for it in items(variant, instances):
        by_inst.setdefault(it["instance"], []).append(it)
    made = []
    for inst, its in sorted(by_inst.items()):
        its.sort(key=lambda x: x["id"])
        for k in range(0, len(its), SIZE):
            chunk = its[k:k + SIZE]
            bid = f"{variant}-{inst:02d}-{k // SIZE}"
            body = [RULES, "Examples:\n", few_shot(), "Problems:\n"]
            for it in chunk:
                body.append(f"### {it['custom_id']}\nQ: {it['question']}\nA: Let's think step by step.\n")
            (BATCHES / f"{bid}.txt").write_text("\n".join(body))
            (BATCHES / f"{bid}.ids.json").write_text(json.dumps([it["custom_id"] for it in chunk]))
            made.append(bid)
    print("\n".join(made))


def ingest(model):
    out = ROOT / "runs" / model
    recs = []
    for meta_p in sorted((out / "batches").glob("*.json")):
        meta = json.loads(meta_p.read_text())
        text = (out / "batches" / (meta_p.stem + ".txt")).read_text()
        ids = json.loads((BATCHES / f"{meta['batch_id']}.ids.json").read_text())
        parts = re.split(r"^###\s*(\S+)\s*$", text, flags=re.M)
        found = {parts[i]: parts[i + 1] for i in range(1, len(parts) - 1, 2)}
        for cid in ids:
            ok = meta["valid"] and cid in found
            recs.append({"custom_id": cid, "type": "succeeded" if ok else "errored",
                         "text": found.get(cid, ""), "stop_reason": None, "usage": {},
                         "model": meta["model"], "route": "claude-code-subagent", "batch_id": meta["batch_id"],
                         "batch_tool_uses": meta["tool_uses"], "batch_total_tokens": meta.get("total_tokens"),
                         "date_utc": meta["date_utc"],
                         **({} if ok else {"error": "batch discarded (tool use)" if not meta["valid"] else "missing"})})
    with open(out / "raw.jsonl", "w") as f:
        for r in recs:
            f.write(json.dumps(r) + "\n")
    print(f"{len(recs)} records, {sum(r['type'] == 'succeeded' for r in recs)} usable")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["make", "ingest"])
    ap.add_argument("--variant")
    ap.add_argument("--instances")
    ap.add_argument("--model")
    a = ap.parse_args()
    if a.cmd == "make":
        make(a.variant, parse_instances(a.instances))
    else:
        ingest(a.model)


if __name__ == "__main__":
    main()
