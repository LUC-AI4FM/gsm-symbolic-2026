"""Run one model on one variant and log every request and raw response.

Layout (mirrors LUC-AI4FM/ALIAS run folders):
  runs/<model>/requests.jsonl   custom_id, model id, route, decoding params, prompt (or its sha256 for noop)
  runs/<model>/raw.jsonl        custom_id, type, text, stop_reason, usage, model_version, date_utc, latency_s
  runs/<model>/provenance.json  code and input hashes, git head, model, route, created_utc

Usage: python -m gsmsym.run MODEL VARIANT [--instances 0-4] [--budget-usd 2.0] [--workers 12]
"""
import argparse
import datetime as dt
import hashlib
import json
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from . import routes
from .data import ROOT, build_prompt, items
from .models import MODELS, cost


def sha(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()


def parse_instances(s):
    if not s:
        return None
    out = set()
    for part in s.split(","):
        a, _, b = part.partition("-")
        out.update(range(int(a), int(b or a) + 1))
    return out


def spent(model):
    p = ROOT / "runs" / model / "raw.jsonl"
    if not p.exists():
        return 0.0
    return sum(cost(model, json.loads(l).get("usage") or {}) for l in open(p))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("model")
    ap.add_argument("variant")
    ap.add_argument("--instances")
    ap.add_argument("--templates", help="e.g. 0-49")
    ap.add_argument("--budget-usd", type=float, default=1.0, help="cap on this model's cumulative logged spend")
    ap.add_argument("--workers", type=int, default=12)
    a = ap.parse_args(argv)
    m = MODELS[a.model]
    out = ROOT / "runs" / a.model
    out.mkdir(parents=True, exist_ok=True)
    done = set()
    if (out / "raw.jsonl").exists():
        done = {json.loads(l)["custom_id"] for l in open(out / "raw.jsonl")
                if json.loads(l)["type"] == "succeeded"}
    tmpl = parse_instances(a.templates)
    todo = [it for it in items(a.variant, parse_instances(a.instances))
            if it["custom_id"] not in done and (tmpl is None or it["id"] in tmpl)]
    base = spent(a.model)
    print(f"{a.model} {a.variant}: {len(todo)} to run, {len(done)} done, ${base:.3f} spent so far", file=sys.stderr)

    prov = {
        "run_id": a.model, "created_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "argv": ["gsmsym.run"] + (argv or sys.argv[1:]),
        "code": {str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in sorted((ROOT / "gsmsym").glob("*.py"))},
        "inputs": {str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in
                   sorted((ROOT / "data" / "ml-gsm-symbolic" / "generated_data").glob("*.jsonl"))
                   + ([ROOT / "noop" / "clauses.jsonl"] if (ROOT / "noop" / "clauses.jsonl").exists() else [])},
        "git_head": subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True,
                                   text=True).stdout.strip(),
        "model": m["id"], "route": m["route"], "decoding": {"temperature": m.get("temperature", 0.0),
                                                          "max_tokens": m["max_tokens"], "stop": m.get("stop")},
    }
    with open(out / "provenance.jsonl", "a") as f:
        f.write(json.dumps(prov) + "\n")

    lock = threading.Lock()
    state = {"spend": base, "stop": False, "n": 0}

    def call(it):
        if state["stop"]:
            return None
        prompt = build_prompt(it["question"])
        t0 = time.time()
        kw = dict(max_tokens=m["max_tokens"], temperature=m.get("temperature", 0.0))
        try:
            if m["route"] == "bedrock":
                text, stop, usage, ver = routes.bedrock(m["id"], prompt, stop=m.get("stop"), **kw)
            elif m["route"] == "bedrock_completion":
                text, stop, usage, ver = routes.bedrock_completion(m["id"], prompt, **kw)
            else:
                text, stop, usage, ver = routes.alcf(m["id"], prompt, cluster=m["cluster"], stop=m.get("stop"), **kw)
            rec = {"custom_id": it["custom_id"], "type": "succeeded", "text": text, "stop_reason": stop,
                   "usage": usage, "model": m["id"], "model_version": ver}
        except routes.RouteError as e:
            rec = {"custom_id": it["custom_id"], "type": "errored", "error": str(e), "model": m["id"]}
        rec["date_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
        rec["latency_s"] = round(time.time() - t0, 2)
        req = {"custom_id": it["custom_id"], "model": m["id"], "route": m["route"], **kw, "stop": m.get("stop"),
               "prompt_sha256": sha(prompt)}
        if a.variant != "noop":  # noop questions are adaptations of CC BY-NC-ND items; rebuild with gsmsym.data
            req["prompt"] = prompt
        with lock:
            with open(out / "requests.jsonl", "a") as f:
                f.write(json.dumps(req) + "\n")
            with open(out / "raw.jsonl", "a") as f:
                f.write(json.dumps(rec) + "\n")
            state["spend"] += cost(a.model, rec.get("usage") or {})
            state["n"] += 1
            if state["spend"] > a.budget_usd:
                state["stop"] = True
            if state["n"] % 50 == 0:
                print(f"  {state['n']}/{len(todo)} ${state['spend']:.3f}", file=sys.stderr)
        return rec

    with ThreadPoolExecutor(a.workers) as ex:
        futs = [ex.submit(call, it) for it in todo]
        errs = 0
        for f in as_completed(futs):
            r = f.result()
            if r and r["type"] != "succeeded":
                errs += 1
                if errs <= 3:
                    print("  error:", r["error"][:200], file=sys.stderr)
    print(f"done {state['n']} calls, {errs} errors, cumulative ${state['spend']:.3f}"
          + (" (BUDGET STOP)" if state["stop"] else ""), file=sys.stderr)


if __name__ == "__main__":
    main()
