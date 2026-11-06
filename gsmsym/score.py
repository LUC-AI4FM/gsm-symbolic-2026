"""Rebuild every table and figure from the raw logs.

  python -m gsmsym.score            -> runs/<model>/graded.json, results/summary.json, results/TABLES.md, figures/*.png
"""
import json
import math
import random
from collections import defaultdict
from pathlib import Path

from .data import NOOP, ROOT, items
from .extract import correct, final_answer_extract, paper_extract
from .models import MODELS, cost

VARS = ("symbolic", "p1", "p2", "noop")
# Paper Tab. 1 (arXiv 2410.05229v2): GSM8K(100), Symbolic, P1, P2, NoOp (mean, sd across sets)
PAPER = {
    "Llama3-8b-instruct": (74.0, (74.6, 2.94), (53.8, 4.54), (28.3, 4.37), (18.6, 3.86)),
    "Gemma2-27b-it": (92.0, (88.3, 2.56), (80.7, 4.07), (63.4, 4.14), (30.0, 3.39)),
    "Phi-3.5-mini-instruct": (88.0, (82.1, 3.38), (64.8, 5.43), (44.8, 6.32), (22.4, 4.03)),
    "GPT-4o-mini": (95.0, (91.7, 2.02), (81.1, 3.05), (72.4, 4.57), (54.1, 3.85)),
    "GPT-4o": (95.0, (94.9, 1.87), (93.9, 2.59), (88.0, 3.43), (63.1, 4.53)),
    "o1-mini": (93.0, (94.5, 1.58), (94.3, 2.57), (89.1, 3.56), (66.0, 4.60)),
    "o1-preview": (96.0, (92.7, 1.82), (95.4, 1.72), (94.0, 2.38), (77.4, 3.84)),
}
SUBAGENT_NOTE = "via Claude Code subagent (not API; default sampling, Claude Code system prompt, 50 problems per context)"
RNG = random.Random(20261106)


def gold_map():
    g = {}
    for v in ("gsm8k", "symbolic", "p1", "p2", "noop"):
        for it in items(v):
            g[it["custom_id"]] = it["gold"]
    return g


def noop_unanimous():
    if not NOOP.exists():
        return set()
    out = set()
    for r in map(json.loads, open(NOOP)):
        j = list(r.get("judges", {}).values())
        if len(j) >= 2 and all(x == "UNCHANGED" for x in j) and r.get("has_number"):
            out.add(f"{r['id']:04d}-noop-{r['instance']:02d}")
    return out


def grade_run(run, gold):
    recs = {}
    p = ROOT / "runs" / run / "raw.jsonl"
    for l in open(p):
        r = json.loads(l)
        if r["type"] == "succeeded" or r["custom_id"] not in recs:
            recs[r["custom_id"]] = r
    graded = []
    for cid, r in sorted(recs.items()):
        if cid not in gold:
            continue
        t, cond, inst = cid.split("-")
        ok = r["type"] == "succeeded"
        pred = paper_extract(r["text"]) if ok else None
        pred2 = final_answer_extract(r["text"]) if ok else None
        graded.append({"id": int(t), "condition": cond, "instance": int(inst), "custom_id": cid,
                       "status": r["type"], "pred": pred, "gold": gold[cid],
                       "pass": ok and correct(pred, gold[cid]), "pass_final_rule": ok and correct(pred2, gold[cid])})
    (ROOT / "runs" / run / "graded.json").write_text(json.dumps(graded, indent=0))
    return graded, list(recs.values())


def table(graded, unanimous):
    by = defaultdict(lambda: defaultdict(dict))  # cond -> instance -> id -> pass
    for g in graded:
        if g["status"] != "succeeded":
            continue
        by[g["condition"]][g["instance"]][g["id"]] = (g["pass"], g["pass_final_rule"])
    ntempl = {"gsm8k": 100, "symbolic": 100, "p1": 100, "p2": 50, "noop": 100}
    out = {}
    base = by.get("gsm8k", {}).get(0, {})
    out["gsm8k"] = {"acc": 100 * sum(v[0] for v in base.values()) / len(base), "n": len(base)} if base else None
    for cond in VARS + ("noop_unanimous",):
        src = by.get("noop" if cond == "noop_unanimous" else cond, {})
        sets = {}
        for inst, d in src.items():
            if cond == "noop_unanimous":
                d = {t: v for t, v in d.items() if f"{t:04d}-noop-{inst:02d}" in unanimous}
                if len(d) >= 10:
                    sets[inst] = d
            elif len(d) >= 0.95 * ntempl[cond]:  # complete sets only
                sets[inst] = d
        if not sets:
            continue
        accs = [100 * sum(v[0] for v in d.values()) / len(d) for d in sets.values()]
        accs2 = [100 * sum(v[1] for v in d.values()) / len(d) for d in sets.values()]
        mean = sum(accs) / len(accs)
        sd = statistics_sd(accs)
        n_items = sum(len(d) for d in sets.values()) / len(sets)
        p = mean / 100
        exp_sd = 100 * math.sqrt(p * (1 - p) / n_items)
        cell = {"acc": mean, "sd": sd, "sets": len(sets), "templates_per_set": n_items,
                "acc_final_rule": sum(accs2) / len(accs2), "binomial_sd": exp_sd}
        if len(sets) >= 5:
            sims = []
            for _ in range(2000):
                sims.append(statistics_sd([100 * sum(RNG.random() < p for _ in range(round(n_items))) / round(n_items)
                                           for _ in range(len(sets))]))
            sims.sort()
            cell["binomial_sd_p975"] = sims[int(0.975 * len(sims))]
            cell["h2_consistent_with_binomial"] = sd <= cell["binomial_sd_p975"]
        if base:
            # paired bootstrap over templates: per-template accuracy across sets vs original question
            tids = sorted({t for d in sets.values() for t in d} & set(base))
            per = {t: [d[t][0] for d in sets.values() if t in d] for t in tids}
            pv = {t: sum(x) / len(x) for t, x in per.items()}
            point = 100 * (sum(base[t][0] for t in tids) - sum(pv[t] for t in tids)) / len(tids)
            boots = []
            for _ in range(10000):
                s = [RNG.choice(tids) for _ in tids]
                boots.append(100 * (sum(base[t][0] for t in s) - sum(pv[t] for t in s)) / len(s))
            boots.sort()
            cell["drop_paired"] = point
            cell["drop_ci95"] = (boots[250], boots[9750])
            cell["drop"] = out["gsm8k"]["acc"] - mean
        out[cond] = cell
    return out


def statistics_sd(xs):
    if len(xs) < 2:
        return float("nan")
    m = sum(xs) / len(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def fmt(c, key="acc"):
    if not c:
        return "–"
    s = f"{c[key]:.1f}"
    if c.get("sd") == c.get("sd") and c.get("sets", 1) > 1:
        s += f" (±{c['sd']:.1f})"
    return s + (f" [{c['sets']}]" if "sets" in c else "")


def main():
    gold = gold_map()
    unanimous = noop_unanimous()
    summary, spend = {}, {}
    for d in sorted((ROOT / "runs").iterdir()):
        if not d.is_dir() or d.name.startswith("_") or not (d / "raw.jsonl").exists():
            continue
        graded, recs = grade_run(d.name, gold)
        summary[d.name] = table(graded, unanimous)
        if d.name in MODELS:
            spend[d.name] = sum(cost(d.name, r.get("usage") or {}) for r in recs)
            summary[d.name]["_meta"] = {k: MODELS[d.name][k] for k in ("id", "route", "released")}
        else:
            summary[d.name]["_meta"] = {"route": "claude-code-subagent", "note": SUBAGENT_NOTE}
    res = ROOT / "results"
    res.mkdir(exist_ok=True)
    (res / "summary.json").write_text(json.dumps({"models": summary, "bedrock_spend_usd": spend}, indent=1))

    L = ["# Results", "", "Rebuilt by `python -m gsmsym.score` from `runs/*/raw.jsonl`. Accuracy in %, mean (± SD across "
         "instance sets) [number of complete sets]. Drop = GSM8K-100 minus variant, with a 95% paired bootstrap CI "
         "over templates. Answers parsed with the paper's last-number rule.", ""]

    def section(title, names):
        L.extend([f"## {title}", "", "| Model | Route | GSM8K-100 | Symbolic | P1 | P2 | NoOp | NoOp (unanimous) |",
                  "|---|---|---|---|---|---|---|---|"])
        for n in names:
            s = summary[n]
            g = s.get("gsm8k")
            L.append(f"| {n} | {s['_meta'].get('route')} | {g['acc']:.1f} |" if g else f"| {n} | {s['_meta'].get('route')} | – |")
            L[-1] += "".join(f" {fmt(s.get(v))} |" for v in VARS + ("noop_unanimous",))
        L.extend(["", "Drops (points) with 95% CI:", "", "| Model | Symbolic | P1 | P2 | NoOp | NoOp (unanimous) |",
                  "|---|---|---|---|---|---|"])
        for n in names:
            s = summary[n]
            row = f"| {n} |"
            for v in VARS + ("noop_unanimous",):
                c = s.get(v)
                row += (f" {c['drop_paired']:+.1f} [{c['drop_ci95'][0]:+.1f}, {c['drop_ci95'][1]:+.1f}] |"
                        if c and "drop_paired" in c else " – |")
            L.append(row)
        L.append("")

    api = [n for n in summary if summary[n]["_meta"]["route"] != "claude-code-subagent"]
    sub = [n for n in summary if n not in api]
    section("API-decoded models (greedy where the API allows)", api)
    if sub:
        section("Claude models " + SUBAGENT_NOTE, sub)
    L.extend(["## Paper (Tab. 1, arXiv 2410.05229v2), for reference", "",
              "| Model | GSM8K-100 | Symbolic | P1 | P2 | NoOp |", "|---|---|---|---|---|---|"])
    for n, (g, *vs) in PAPER.items():
        L.append(f"| {n} | {g} |" + "".join(f" {m} (±{s}) |" for m, s in vs))
    L.extend(["", "## Variance across instance sets vs binomial expectation (H2)", "",
              "| Model | Variant | sets | observed SD | binomial SD | 97.5th pct of binomial SD | consistent |",
              "|---|---|---|---|---|---|---|"])
    for n, s in summary.items():
        for v in VARS:
            c = s.get(v)
            if c and "binomial_sd_p975" in c:
                L.append(f"| {n} | {v} | {c['sets']} | {c['sd']:.2f} | {c['binomial_sd']:.2f} | "
                         f"{c['binomial_sd_p975']:.2f} | {'yes' if c['h2_consistent_with_binomial'] else 'no'} |")
    L.extend(["", "## Cash spend on Bedrock (from logged token usage x list price)", "",
              "| Model | USD |", "|---|---|"] + [f"| {k} | {v:.2f} |" for k, v in spend.items()]
             + [f"| total | {sum(spend.values()):.2f} |", ""])
    (res / "TABLES.md").write_text("\n".join(L))
    figures(summary)
    print("\n".join(L))


def figures(summary):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    fig_dir = ROOT / "figures"
    fig_dir.mkdir(exist_ok=True)
    names = [n for n in summary if summary[n].get("gsm8k")]
    xs = ["gsm8k"] + list(VARS)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for n in names:
        s = summary[n]
        ys = [s["gsm8k"]["acc"]] + [s[v]["acc"] if v in s else float("nan") for v in VARS]
        es = [0] + [s[v]["sd"] if v in s and s[v]["sd"] == s[v]["sd"] else 0 for v in VARS]
        ax.errorbar(range(len(xs)), ys, yerr=es, marker="o", capsize=3, label=n)
    for n in ("GPT-4o", "o1-preview", "Llama3-8b-instruct"):
        g, *vs = PAPER[n]
        ax.plot(range(len(xs)), [g] + [m for m, _ in vs], ls="--", color="grey", alpha=0.6)
        ax.annotate(f"paper {n}", (4, vs[-1][0]), fontsize=7, color="grey")
    ax.set_xticks(range(len(xs)), ["GSM8K-100", "Symbolic", "P1", "P2", "NoOp"])
    ax.set_ylabel("8-shot CoT accuracy (%)")
    ax.set_ylim(0, 100)
    ax.legend(fontsize=7, loc="lower left")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(fig_dir / "accuracy_by_variant.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
