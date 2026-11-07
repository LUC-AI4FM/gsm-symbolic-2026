"""Cost quote for the full protocol on Bedrock, from measured tokens per item in runs/*/raw.jsonl.

Full protocol per model (paper counts): GSM8K-100 (100) + Symbolic (100 x 50) + P1 (100 x 50) + P2 (50 x 50)
+ NoOp (about 94 x 50 after dropping clauses without a number) = 17,300 items.
Usage: python3 scripts/quote.py  -> results/COST.md
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from gsmsym.models import MODELS, cost  # noqa: E402

FULL = {"gsm8k": 100, "symbolic": 5000, "p1": 5000, "p2": 2500, "noop": 4700}
# Bedrock models we could not run but might add once access is enabled (list prices, us-east-1, per 1M tokens),
# with token use assumed equal to the median measured non-reasoning model.
EXTRA = {"claude-opus-4-6 (Bedrock)": (5.5, 27.5), "claude-sonnet-4-6 (Bedrock)": (3.3, 16.5)}

# Bedrock models whose exact weights ALCF also serves: their full protocol runs on ALCF instead.
MOVED_TO_ALCF = {"nemotron-super-3-120b": "nemotron-3-super-120b-alcf"}

rows, spent = [], 0.0
med_in = med_out = None
for name, m in MODELS.items():
    p = ROOT / "runs" / name / "raw.jsonl"
    if not p.exists():
        continue
    recs = [json.loads(l) for l in open(p)]
    ok = [r for r in recs if r["type"] == "succeeded"]
    s = sum(cost(name, r.get("usage") or {}) for r in ok)
    if m["route"].startswith("bedrock"):
        spent += s
    by = {}
    for r in ok:
        v = r["custom_id"].split("-")[1]
        by.setdefault(v, []).append(r["usage"])
    est, tin, tout = 0.0, 0, 0
    for v, n in FULL.items():
        us = by.get(v) or [u for x in by.values() for u in x]
        if not us:
            continue
        ai = sum(u.get("input") or 0 for u in us) / len(us)
        ao = sum(u.get("output") or 0 for u in us) / len(us)
        tin += ai * n
        tout += ao * n
    est = cost(name, {"input": tin, "output": tout})
    rows.append((name, m["route"], len(ok), s, tin / 1e6, tout / 1e6, est))

L = ["# Cost", "", f"Bedrock cash spent so far (logged usage x list price): **${spent:.2f}**.", "",
     "Full protocol per model: 17,300 items (GSM8K-100, Symbolic 50 sets, P1 50 sets, P2 50 sets, NoOp ~47 x 100).",
     "Token use per item is measured from our runs, per variant.", "",
     "| Model | Route | items run | spent USD | full: M input tok | full: M output tok | full-run USD |",
     "|---|---|---|---|---|---|---|"]
for r in rows:
    L.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]:.2f} | {r[4]:.1f} | {r[5]:.1f} | {r[6]:.2f} |")
bed = [r for r in rows if r[1].startswith("bedrock") and r[0] not in MOVED_TO_ALCF]
rem = sum(r[6] - r[3] for r in bed)
L += ["", "Moved to ALCF (same weights served there, no cash): "
      + ", ".join(f"{k} -> {v}" for k, v in MOVED_TO_ALCF.items()) + ".",
      "Not on ALCF, so Bedrock-only: " + ", ".join(r[0] for r in bed)
      + " (ALCF serves Llama-3.1-8B-Instruct, a close relative of the Llama-3-8B anchor, which we run there too).",
      "", f"Full-run quote for the Bedrock-only models: **${sum(r[6] for r in bed):.2f}**, "
      f"of which ${rem:.2f} is beyond what is already spent; without Kimi K3.1: "
      f"${sum(r[6] for r in bed if r[0] != 'kimi-k3.1'):.2f}.",
      "ALCF and Claude Code subagent routes cost no cash."]
(ROOT / "results").mkdir(exist_ok=True)
(ROOT / "results" / "COST.md").write_text("\n".join(L) + "\n")
print("\n".join(L))
