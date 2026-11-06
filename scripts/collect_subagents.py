"""Collect Claude Code subagent batch outputs from local transcripts, verbatim.

Finds subagent transcripts whose first user message starts with the exact text of a batch file
(batches/<id>.txt) and writes
  runs/<run>/batches/<id>.txt   the subagent's final report, unedited
  runs/<run>/batches/<id>.json  model id, tool calls, token usage, date, validity
A batch is valid only if the only tool the subagent called was the final hand-off.
Usage: python3 scripts/collect_subagents.py TRANSCRIPT_DIR
"""
import glob
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
batches = {p.stem: p.read_text().rstrip() for p in (ROOT / "batches").glob("*.txt")}
HANDOFF = {"SubagentHandback"}


def first_prompt(L):
    for l in L:
        if l.get("type") == "user":
            c = l["message"]["content"]
            return c if isinstance(c, str) else "".join(x.get("text", "") for x in c if isinstance(x, dict))
    return ""


n = 0
for path in sorted(glob.glob(str(Path(sys.argv[1]) / "**" / "agent-*.jsonl"), recursive=True)):
    L = [json.loads(x) for x in open(path)]
    prompt = first_prompt(L).strip()
    bid = next((b for b, t in batches.items() if prompt.startswith(t)), None)
    if bid is None:
        continue
    model, tools, report, last_ts = None, [], None, None
    usage = {"input": 0, "cache_creation": 0, "cache_read": 0, "output": 0}
    for l in L:
        if l.get("type") != "assistant":
            continue
        m = l["message"]
        model = m.get("model") or model
        u = m.get("usage") or {}
        usage["input"] += u.get("input_tokens", 0)
        usage["cache_creation"] += u.get("cache_creation_input_tokens", 0)
        usage["cache_read"] += u.get("cache_read_input_tokens", 0)
        usage["output"] += u.get("output_tokens", 0)
        last_ts = l.get("timestamp", last_ts)
        for c in m["content"]:
            if c.get("type") == "tool_use":
                tools.append(c["name"])
                if c["name"] in HANDOFF:
                    report = c["input"].get("message")
    if report is None:
        for l in reversed(L):
            if l.get("type") == "assistant":
                report = "".join(c.get("text", "") for c in l["message"]["content"] if c.get("type") == "text")
                break
    other = [t for t in tools if t not in HANDOFF]
    run = f"claude-{(model or 'unknown').replace('claude-', '')}-subagent"
    out = ROOT / "runs" / run / "batches"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{bid}.txt").write_text(report or "")
    (out / f"{bid}.json").write_text(json.dumps({
        "batch_id": bid, "model": model, "route": "claude-code-subagent", "tool_uses": len(tools),
        "non_handoff_tools": other, "valid": not other and bool(report), "usage": usage,
        "total_tokens": sum(usage.values()), "date_utc": last_ts}, indent=1))
    n += 1
    print(bid, model, "tools:", tools, "tokens:", usage)
print(f"collected {n} batches")
