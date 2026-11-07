"""Answer extraction exactly as the GSM-Symbolic README describes, plus a stricter variant for sensitivity."""
import re

STOP = ("\nQ:", "\n\nQ:")


def truncate(resp: str) -> str:
    """The paper stops generation when the model starts a new question ("Q:")."""
    cut = len(resp)
    for s in STOP:
        i = resp.find(s)
        if i != -1:
            cut = min(cut, i)
    return resp[:cut]


def paper_extract(resp: str):
    """README rule: drop commas, take the last number, compare as float."""
    resp = truncate(resp).replace(",", "")
    nums = re.findall(r"-?\d+\.?\d*", resp)
    return float(nums[-1]) if nums else None


def final_answer_extract(resp: str):
    """Format-aware parser (sensitivity check; exploratory beyond the pre-registered 'final answer is' rule).

    In order: the number after the last 'final answer is'; the last \\boxed{...}; the first number after the
    last 'Answer:'; otherwise the paper rule. Catches chat models that restate the question after answering.
    """
    t = truncate(resp).replace(",", "")
    m = re.findall(r"final answer is[^0-9\-]*(-?\d+\.?\d*)", t, flags=re.I)
    if m:
        return float(m[-1])
    m = re.findall(r"\\boxed\{[^0-9\-}]*(-?\d+\.?\d*)", t)
    if m:
        return float(m[-1])
    i = max(t.rfind("Answer:"), t.rfind("answer:"), t.rfind("Answer**"))
    if i != -1:
        m = re.search(r"-?\d+\.?\d*", t[i:])
        if m:
            return float(m.group())
    return paper_extract(resp)


def correct(pred, gold) -> bool:
    return pred is not None and abs(pred - gold) < 1e-6
