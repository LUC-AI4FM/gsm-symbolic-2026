# Rebuttal: GSM-Symbolic on 2026 models

A response to Mirzadeh et al., *GSM-Symbolic* (ICLR 2025, [arXiv 2410.05229](https://arxiv.org/abs/2410.05229)),
written after re-running its protocol. Each point cites our data (`results/TABLES.md`, rebuilt from
`runs/` by `python -m gsmsym.score`) or a source we opened ([RELATED_WORK.md](RELATED_WORK.md)). Numbers
below were current at the commit that last touched this file; `results/TABLES.md` is authoritative.

**Scope.** Pilot scale: most models ran 1 to 10 instance sets per variant (Gemma 4 31B ran all 50 sets on
Symbolic, P1 and P2). Claude Haiku 5.5 ran through Claude Code subagents, a different deployment mode.
The paid frontier APIs we could not reach (Claude 4.7+, GPT-5.4+, Grok, GLM-5.3) are not covered.

## Summary

| Claim in the paper | On 2026 models | Basis |
|---|---|---|
| The harness reproduces the paper | **Yes** | Llama-3-8B-Instruct within 2 paper SDs on Symbolic, P1, P2 |
| Changing names and numbers lowers accuracy (Symbolic) | **Small**: drops of −2.0 to +5.1 points, CI excluding zero for 2 of 7 models | 7 models |
| Variance across instance sets shows fragility | **No**: every observed SD, ours and the paper's, is at or below binomial sampling noise | H2 table; Tab. 1 |
| Added clauses (P1, P2) cause large drops | **Not for 2026 models** (P1 -2.0 to +3.3, P2 0 to +8.8), still yes for Llama-3-8B (+21, +43) | 7 models |
| One inconsequential clause (NoOp) collapses accuracy | **Depends on the clause.** Calibrated distractors still cost 2026 models 20 to 31 points; distractors an auditor judges truly irrelevant cost them 0 to 5 | two NoOp constructions |
| LLMs pattern-match rather than reason | Not tested directly; the evidence above does not require it | |

**Eric Spencer's hypothesis (pre-registered H1): "2026 models will do much better on GSM-Symbolic, P1,
P2 and NoOp than the paper's models."** By the pre-registered rule the verdict is **partly supported**:
on Symbolic, P1 and P2 the 2026 models we ran are far better than the paper's (for example, P2 accuracy 85
to 96% against GPT-4o's 88% and Llama-3-8B's 28%), and on our pre-registered NoOp their median drop is
about 3 points. But only about half meet all four thresholds (several miss the 2-point Symbolic threshold by
under a point, inside their CIs), and on a NoOp set calibrated to the paper (see 5) the four 2026 models we ran on it drop 20 to 31 points,
no better than o1-preview's 18.6 on Apple's set. **2026 models still drop on NoOp.**

## 1. The reproduction holds

Llama-3-8B-Instruct, raw completion on Bedrock, 5 instance sets:

| | GSM8K-100 | Symbolic | P1 | P2 | NoOp |
|---|---|---|---|---|---|
| Paper (Tab. 1) | 74.0 | 74.6 ± 2.94 | 53.8 ± 4.54 | 28.3 ± 4.37 | 18.6 ± 3.86 |
| Ours | 77.0 | 73.6 ± 1.8 | 55.8 ± 3.3 | 32.8 ± 3.0 | 24.7 ± 3.0 (NoOp-S), 61.6 ± 1.3 (our NoOp) |

Symbolic, P1 and P2 fall within 2 paper SDs, the pre-registered criterion. The paper's large P1 and P2
drops for this model are real. So are its NoOp failures, with the right distractors (section 5).

## 2. On 2026 models the Symbolic drop is small and mostly within noise

Symbolic drops from GSM8K-100: Gemma 4 31B +1.8 [−0.3, +4.4] over 50 sets, DeepSeek V3.2 +2.7
[+0.7, +4.7], Nemotron 3 Super +0.0, Nemotron 3 Ultra +5.1 [+1.7, +9.0], GPT-OSS-120B +2.2 [−4.2, +8.7],
Kimi K3.1 −2.0 (one set), Claude Haiku 5.5 (subagent) +2.5 [−1.0, +6.0]. Only DeepSeek's and Nemotron 3
Ultra's CIs exclude zero, and both are smaller than the paper's drops for most 2024 models (Tab. 1).

Two limits of the measure itself:

- **The baseline is 100 questions.** At 96% accuracy one GSM8K-100 run has a binomial SD of about 2
  points, so a single baseline cannot resolve drops this small. Długosz et al. (EMNLP 2026,
  [arXiv 2605.28700](https://arxiv.org/abs/2605.28700)) reach the same conclusion with mixed-effects models
  on 20 open models: only 8 show a significant change.
- **The instances are not the same difficulty.** Długosz et al. find GSM-Symbolic's numbers are shifted
  larger than GSM8K's, and controlling for this removes significance in half the remaining cases. A
  drop from larger numbers is arithmetic load, not evidence against reasoning.

## 3. The variance claim does not survive a sampling-noise check

The paper reads the spread across its 50 instance sets as fragility. If each set is 100 independent
items with accuracy *p*, sampling noise alone gives an SD of sqrt(p(1−p)/100). **Every SD in the paper's
Tab. 1 that we checked is below that**: Llama-3-8B-Instruct reports 2.94 against a binomial 4.35, GPT-4o
1.87 against 2.20, o1-preview 1.82 against 2.60 (13 models, ratios 0.62 to 0.88). Ours behave the same:
every cell in our H2 table is consistent with binomial noise (Gemma 4 31B, 50 sets: SD 1.12 against 1.92
on Symbolic). An SD below the binomial value is what fixed per-template difficulty produces, not added
fragility. Ivanova et al. ([2024](https://probapproxincorrect.substack.com/p/towards-more-rigorous-evaluations))
made this point first; the paper's v2 Appendix B answers that an ideal reasoner would be always right or
always wrong per question, which is a normative claim and does not address set-level sampling noise.

## 4. P1 and P2 add work, so a drop is expected; 2026 models mostly absorb it

P1 and P2 add one and two clauses, and with them reasoning steps. If each step can fail, accuracy falls
with the number of steps for any solver, human or model, so a drop alone does not separate "reasoning"
from "pattern matching". The paper's own Llama-3-8B pattern (74 → 54 → 28) matches a roughly constant
per-clause loss. 2026 models lose little: P2 drops of 0 (GPT-OSS, Kimi), 2.0 (Haiku), 3.3 (Gemma, 50 sets),
4.0 (DeepSeek), 8.8 (Nemotron 3 Super; CI [−2.0, +19.2]). The paper's P1/P2 claim holds for 2024 small
models and is mostly gone at 2026.

## 5. NoOp: the effect is real, and its size depends on how ambiguous the clause is

Apple did not release GSM-NoOp, so we used two constructions:

- **Our NoOp** (pre-registered): Gemma 4 31B wrote one number-bearing sentence per item; two other models
  judged whether the answer stays unchanged. Both judges said UNCHANGED for 89% of sentences.
- **NoOp-S** (exploratory): the 945 clauses of Sturgeon (2026,
  [LessWrong](https://www.lesswrong.com/posts/Ze4C99Dasj74YKCFh/revisiting-gsm-symbolic-do-2026-frontier-models-still-fail);
  data on Hugging Face, `Experimental-Orange/gsm-noop-audited`), written by Claude Opus 4.6 and audited by
  GPT-5.5, which judged only 117 (12%) truly irrelevant and 821 ambiguous.

**Calibration on the anchor.** Llama-3-8B-Instruct scores 18.6% on Apple's NoOp in the paper, 24.7% on
NoOp-S and 61.6% on our NoOp. Sturgeon reports GPT-4o at 66.1% on NoOp-S against the paper's 63.1%. So
NoOp-S is close to Apple's distractors and **our NoOp is much milder**; our pre-registered NoOp verdict
must be read with that in mind.

| Model | NoOp drop (ours) | NoOp-S drop | NoOp-S, truly irrelevant only |
|---|---|---|---|
| Llama-3-8B-Instruct | +15.2 | +53.1 | +53.3 |
| Gemma 4 31B (10 sets) | +3.4 | +21.0 [+16.0, +26.1] | +2.5 |
| GPT-OSS-120B (10 sets) | +8.2 | +26.3 [+18.8, +33.8] | +5.2 [−2.1, +12.6] |
| DeepSeek V3.2 (2 sets) | +5.0 | +30.6 [+23.0, +38.8] | +0.0 (small n) |
| Claude Haiku 5.5, subagent (2 sets) | +3.1 | +19.7 [+12.6, +26.8] | +0.0 (small n) |

What this shows:

1. **2026 models still drop on NoOp.** On distractors calibrated to the paper, the 2026 models lose 20 to
   31 points, close to o1-preview's 18.6 on Apple's set; GPT-4o, in Sturgeon's data, falls 25.5 points from Symbolic to NoOp-S.
2. **The drop is concentrated in ambiguous clauses.** On the clauses GPT-5.5 judged truly irrelevant,
   the 2026 models lose 0 to 5 points (117 clauses over 10 sets, fewer for 2-set models), consistent with
   Sturgeon's 0 to 2 for Opus 4.6 and Haiku 4.5.
   Llama-3-8B still loses 53 points there, so the old model fails on irrelevant information that the new
   ones ignore.
3. Many NoOp clauses are ones a careful human might also act on ("roughly 8% didn't fully expand"). A
   model that uses such a clause is answering a different reading of the question, not failing to reason.
   The paper's NoOp mixes this with genuine distraction and reports the sum.

H3 (pre-registered, on our NoOp): the unanimous-judge subset lowers the drop by less than the 30%
threshold for most models, so **H3 is not supported on our NoOp**, whose judges filtered little. On NoOp-S
the GPT-5.5 audit removes most of the 2026 drop (exploratory).

Qu & Gomes ([arXiv 2609.17804](https://arxiv.org/abs/2609.17804)) give independent support for a real
effect on open models: Llama-3.3-70B falls from 0.950 to 0.780 on their NoOp but only to 0.898 on
length-matched filler.

## 6. Methodological weaknesses in the original

1. **Variance read as fragility** (section 3).
2. **Difficulty shifts**: larger numbers in Symbolic (Długosz et al.) and more steps in P1/P2 (section 4).
3. **NoOp construction unreleased and not audited for ambiguity** (section 5); its effect size cannot be
   re-measured exactly, and our two constructions give 3 and 21 points for the same model.
4. **The answer parser scores format.** The last-number rule fails when a model restates the question after
   answering ("…for the 42-mile-wide city"). GPT-OSS-120B gains 7 to 9 points on every variant under a
   format-aware parser (results, "Parser sensitivity"); for the other models the two parsers differ by at most 1.4 points.
5. **Table 1 has identical cells across different models.** Several base and instruct pairs share every
   digit in some columns, including the SD: Llama3-8b and Llama3-8b-instruct (Symbolic-M1 79.5 ± 3.62,
   Symbolic 74.6 ± 2.94, P1 53.8 ± 4.54, NoOp 18.6 ± 3.86, while their GSM8K columns differ: 55.8 vs
   76.0), Gemma-7b and Gemma-7b-it (Symbolic, P2, NoOp), Gemma2-9b and Gemma2-9b-it (Symbolic, P2, NoOp),
   Gemma2-2b and Gemma2-2b-it (M1, Symbolic, P1). Two models with GSM8K accuracies 20 points apart are
   unlikely to match to the decimal on four variants. We could not find this discussed elsewhere and
   cannot tell which column is wrong; it means per-model values in Tab. 1 need checking before reuse,
   including the Llama-3-8B-Instruct row we compare against.
6. **One deployment mode, unstated.** The paper decodes greedily from a bare prompt. That is an
   assumption about how models are used, and its conclusions about "reasoning limits" are conditional on it.
   We found no public source giving the split between raw API use and app or agent-harness use (Anthropic's
   Economic Index, [arXiv 2511.15080](https://arxiv.org/abs/2511.15080), shows both are large but gives no
   shares). Our only harness-mode model, Claude Haiku 5.5 in Claude Code, behaves like the API-decoded 2026
   models on every variant (Symbolic +2.5, P1 +1.5, P2 +2.0, NoOp-S +19.7). We do not have the same model in
   both modes, so we cannot isolate the mode effect.

## 7. Is GSM-Symbolic a bad test? (a thesis, tested)

Eric Spencer's view is that GSM-Symbolic is a bad test and that nobody evaluates models this way. What
the evidence supports:

- **Mostly saturated for 2026 models on Symbolic, P1, P2.** Accuracies of 85 to 98% with drops mostly
  inside the noise of a 100-question baseline (sections 2 and 4). It barely separates 2026 models there.
  (GPT-OSS-120B is the exception at 77 to 80%, much of it parser loss, 6.4.)
- **Weak construct validity for "reasoning".** Its drops mix sampling noise (3), harder arithmetic and
  more steps (2, 4), ambiguous distractors (5) and output format (6.4).
- **But not useless.** It still separates a 2024 8B model from 2026 models by 20 to 50 points on P1, P2
  and NoOp, and calibrated NoOp distractors still cost 2026 models 20 to 31 points. As a robustness probe
  it finds something real; as a measure of whether models "reason", it does not isolate that.
- **Deployment mode** is untested as a variable in the original (6.6), so "nobody uses it this way" is an
  argument about external validity that neither we nor the paper can settle with data.

## 8. Cross-domain: renaming in math vs renaming in TLA+ (ALIAS)

[ALIAS](https://github.com/LUC-AI4FM/ALIAS) (commit `8cd0580`) runs the same idea on 111 TLA+
specifications. With a grader that needs the original names, Claude Opus 4.8 drops 10.1 points [5.0, 15.7]
when identifiers are renamed; with a behavior-based grader the drop is 2.6 points (32.1% → 29.5%). GPT-5
drops 2.2 [−0.4, 4.7] name-based and 0 behavior-based. GSM-Symbolic's answer is a number, so names cannot
leak into the grade, and the 2026 models here lose −2.0 to +2.7 points under renaming plus renumbering.

Read together: once grading does not depend on names, renaming costs 2025-26 models about 0 to 3 points
in both domains. Different models were tested in the two studies (Opus 4.8 and GPT-5 there; open models
and Haiku 5.5 here), so this is a consistent pattern, not a paired comparison.
