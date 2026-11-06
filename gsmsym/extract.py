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
    """Sensitivity check: the number after the last 'final answer is', else the paper rule."""
    t = truncate(resp).replace(",", "")
    m = re.findall(r"final answer is[^0-9\-]*(-?\d+\.?\d*)", t, flags=re.I)
    return float(m[-1]) if m else paper_extract(resp)


def correct(pred, gold) -> bool:
    return pred is not None and abs(pred - gold) < 1e-6
