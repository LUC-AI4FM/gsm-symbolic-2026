"""Load the official GSM-Symbolic release and build the 8-shot prompt the paper describes.

The data is not vendored (CC BY-NC-ND 4.0). `scripts/fetch_data.sh` clones it at a pinned commit.
"""
import json
import re
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "ml-gsm-symbolic" / "generated_data"
NOOP = ROOT / "noop" / "clauses.jsonl"

FILES = {"symbolic": "GSM_symbolic.jsonl", "p1": "GSM_p1.jsonl", "p2": "GSM_p2.jsonl"}
VARIANTS = ("gsm8k", "symbolic", "p1", "p2", "noop", "noop2")
STURGEON = ROOT / "data" / "sturgeon" / "distractors"

# The common GSM8K 8-shot chain-of-thought exemplars (Wei et al. 2022), verbatim from
# lm-evaluation-harness commit c0745fec, lm_eval/tasks/gsm8k/gsm8k-cot.yaml, which the
# GSM-Symbolic README names as the exemplar source.
SHOTS = [
    ("There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?",
     "There are 15 trees originally. Then there were 21 trees after some more were planted. So there must have been 21 - 15 = 6", "6"),
    ("If there are 3 cars in the parking lot and 2 more cars arrive, how many cars are in the parking lot?",
     "There are originally 3 cars. 2 more cars arrive. 3 + 2 = 5", "5"),
    ("Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?",
     "Originally, Leah had 32 chocolates. Her sister had 42. So in total they had 32 + 42 = 74. After eating 35, they had 74 - 35 = 39", "39"),
    ("Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?",
     "Jason started with 20 lollipops. Then he had 12 after giving some to Denny. So he gave Denny 20 - 12 = 8", "8"),
    ("Shawn has five toys. For Christmas, he got two toys each from his mom and dad. How many toys does he have now?",
     "Shawn started with 5 toys. If he got 2 toys each from his mom and dad, then that is 4 more toys. 5 + 4 = 9", "9"),
    ("There were nine computers in the server room. Five more computers were installed each day, from monday to thursday. How many computers are now in the server room?",
     "There were originally 9 computers. For each of 4 days, 5 more computers were added. So 5 * 4 = 20 computers were added. 9 + 20 is 29", "29"),
    ("Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?",
     "Michael started with 58 golf balls. After losing 23 on tuesday, he had 58 - 23 = 35. After losing 2 more, he had 35 - 2 = 33 golf balls", "33"),
    ("Olivia has $23. She bought five bagels for $3 each. How much money does she have left?",
     "Olivia had 23 dollars. 5 bagels for 3 dollars each will be 5 x 3 = 15 dollars. So she has 23 - 15 dollars left. 23 - 15 is 8", "8"),
]

HEADER = "As an expert problem solver, solve step by step the following mathematical questions."


def build_prompt(question: str) -> str:
    """The prompt template from the GSM-Symbolic README, with the 8 shots above."""
    parts = [HEADER, ""]
    for q, a, final in SHOTS:
        parts.append(f"Q: {q}\nA: Let's think step by step. {a}. The final answer is {final}.\n")
    parts.append(f"Q: {question}\nA: Let's think step by step.")
    return "\n".join(parts)


def gold(answer_field: str) -> float:
    return float(answer_field.split("####")[-1].strip().replace(",", ""))


@lru_cache(maxsize=None)
def _rows(name):
    return [json.loads(l) for l in open(DATA / FILES[name])]


@lru_cache(maxsize=None)
def _noop():
    if not NOOP.exists():
        return {}
    return {(r["id"], r["instance"]): r for r in map(json.loads, open(NOOP)) if r.get("keep", True) and r.get("has_number", True)}


def insert_clause(question: str, clause: str) -> str:
    """Insert the NoOp sentence just before the final (question) sentence."""
    sents = re.split(r"(?<=[.!?])\s+", question.strip())
    if len(sents) < 2:
        return clause + " " + question
    return " ".join(sents[:-1] + [clause, sents[-1]])


def items(variant: str, instances=None):
    """Yield dicts: custom_id, id, instance, question, gold.

    custom_id follows the ALIAS convention <task>-<condition>-<sample>.
    gsm8k is the 100 original GSM8K test questions behind the templates (paper Tab. 1, "GSM8K (100)").
    noop applies our own clauses (noop/clauses.jsonl) to the official symbolic instances at run time.
    """
    if variant == "gsm8k":
        for r in _rows("symbolic"):
            if r["instance"] == 0:
                yield dict(custom_id=f"{r['id']:04d}-gsm8k-00", id=r["id"], instance=0,
                           question=r["original_question"], gold=gold(r["original_answer"]))
        return
    if variant == "noop2":
        # Second NoOp construction: Sturgeon (2026) clauses by Claude Opus 4.6 on 100 templates x 10 instances.
        for r in map(json.loads, open(STURGEON / "GSM_noop_100.jsonl")):
            if instances is not None and r["instance"] not in instances:
                continue
            yield dict(custom_id=f"{r['id']:04d}-noop2-{r['instance']:02d}", id=r["id"], instance=r["instance"],
                       question=r["question"], gold=gold(r["answer"]) if "answer" in r else float(r["gold_answer"]))
        return
    if variant == "noop":
        clauses = _noop()
        for r in _rows("symbolic"):
            if instances is not None and r["instance"] not in instances:
                continue
            c = clauses.get((r["id"], r["instance"]))
            if c is None:
                continue
            yield dict(custom_id=f"{r['id']:04d}-noop-{r['instance']:02d}", id=r["id"], instance=r["instance"],
                       question=insert_clause(r["question"], c["clause"]), gold=gold(r["answer"]))
        return
    for r in _rows(variant):
        if instances is not None and r["instance"] not in instances:
            continue
        yield dict(custom_id=f"{r['id']:04d}-{variant}-{r['instance']:02d}", id=r["id"], instance=r["instance"],
                   question=r["question"], gold=gold(r["answer"]))
