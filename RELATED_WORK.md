# Related work

Scope: work from 2024 to 2026 that replicates, extends, critiques or rebuts GSM-Symbolic
(Mirzadeh et al., arXiv 2410.05229, ICLR 2025), plus foundational GSM8K robustness work it builds on.
Every entry below was opened on 2026-11-06. Findings are taken from the abstract unless marked
"(paper text)". Percentages are as stated by each source; "drop of X%" can be absolute or relative
depending on the source.

Reference paper:
- **GSM-Symbolic: Understanding the Limitations of Mathematical Reasoning in Large Language Models** (Mirzadeh et al., 2024; v2 2025-08-27 is the ICLR camera-ready with added appendix discussion). https://arxiv.org/abs/2410.05229 . ICLR 2025 proceedings PDF: https://proceedings.iclr.cc/paper_files/paper/2025/file/ec2e7a896f8250986b3907f57621ce94-Paper-Conference.pdf . Claims: (C1) noticeable variance across instantiations of the same question; (C2) accuracy falls when only numbers change; (C3) accuracy falls as clauses are added (P1, P2); (C4) one seemingly relevant but inconsequential clause (NoOp) causes drops up to 65%; (C5) hypothesis that LLMs replicate reasoning steps rather than reason.

## 1. Direct replications and re-evaluations

- **The Importance of Being Statistically Earnest: A Critical Re-evaluation of GSM-Symbolic** (Długosz et al., 2026, EMNLP 2026 main, per arXiv comment). https://arxiv.org/abs/2605.28700 . Re-evaluates 20 open-weight models with bootstrapped binomial GLMMs with per-question random effects; only 8 show a statistically significant GSM8K vs GSM-Symbolic change under the original prompt format. Finds GSM-Symbolic integers are shifted towards larger values than GSM8K (K-S 0.12, p < 0.001), and controlling for this accounts for significance in half the remaining cases. (Paper text) Appendix D.1 attributes differences from the original numbers partly to unreported model checkpoints and prompt formatting; the paper does not re-test P1, P2 or NoOp. Relevance: challenges C1 and C2 (and the "numbers range does not increase" design claim).

- **Revisiting GSM-Symbolic: models seem to reason okay, actually** (posted as "Sturb" on LessWrong, 2026-06-05; the linked code repository is BenSturgeon/gsm-symbolic-revisited). https://www.lesswrong.com/posts/Ze4C99Dasj74YKCFh/revisiting-gsm-symbolic-do-2026-frontier-models-still-fail . Regenerates NoOp clauses with Claude Opus 4.6 for 1,000 GSM-Symbolic items (100 templates x 10), then has GPT-5.5 and Opus label each clause as truly irrelevant, ambiguous or relevant. Unaudited distractors reproduce drops of roughly the original size for GPT-4o; on the 117 clauses GPT-5.5 judged truly irrelevant, drops for GPT-4o, Opus 4.6 and Haiku 4.5 are 0 to 2 points and not distinguishable from zero (template-clustered bootstrap). Auditor agreement was low (kappa 0.32). Blog, not peer reviewed; small filtered set. Relevance: challenges C4 (argues the NoOp effect is driven by ambiguous distractors).

- **A Four-Stage Decomposition of Word-Problem Solving and Mechanistic Fragility in LLM Math Reasoning** (Qu et al., 2026, arXiv preprint). https://arxiv.org/abs/2609.17804 . Mechanistic account in which a single irrelevant clause corrupts an "Operation Planning" stage implemented by identifiable attention heads. (Paper text) Rebuilds GSM-NoOp (Claude Opus 4.7 proposes clauses, authors select manually) plus a length-matched GSM-Filler control; for Llama-3.3-70B with CoT, accuracy is 0.950 Symbolic, 0.780 NoOp, 0.898 Filler, 0.941 digit-free Filler, with the same ordering on Qwen-2.5-14B and Gemma-2-9B. Relevance: supports C4 for open models while showing part of the drop comes from added numbers and length rather than meaning; extends C5 with a mechanism.

- **GSM-SEM: Benchmark and Framework for Generating Semantically Variant Augmentations** (Singh et al., 2026, arXiv preprint). https://arxiv.org/abs/2605.07053 . Applies semantic perturbations (entities, attributes, relationships) on top of GSM8K, GSM-Symbolic and GSM-Plus; across 14 SOTA LLMs reports consistent drops, largest when semantic perturbation is combined with symbolic/plus variants (average 28% at maximum strictness). Releases human-validated GSM-Symbolic-SEM. Relevance: extends C2 and C3.

- **The Reasoning-Memorization Interplay in Language Models Is Mediated by a Single Direction** (Hong et al., 2025, arXiv preprint). https://arxiv.org/abs/2503.23084 . Identifies residual-stream features that shift models between reasoning and memory recall and can causally change reasoning-task performance. The abstract does not name GSM-Symbolic, and we did not confirm in the paper text that it is used. Relevance: extends C5 (mechanistic memorization vs reasoning).

## 2. Critiques of the statistics and design

- **Towards more rigorous evaluations of language models** (Ivanova, with Ilievski and Konstantinov, 2024-11-28, Substack blog). https://probapproxincorrect.substack.com/p/towards-more-rigorous-evaluations . Models per-set accuracy as Binomial(100, p): the spread across 50 sets for Llama3-8B and GPT-4o falls within Wilson intervals around GSM8K, so the variance is expected sampling noise. Per-model Fisher tests find only 3 of 25 models significantly worse on GSM-Symbolic than GSM8K (one significantly better); argues rising variance on P1/P2 follows mechanically from p(1-p) as accuracy falls, and added clauses add arithmetic steps; notes some Figure 1 sampling ranges exclude the original GSM8K values. Finds the NoOp drop significant for all models and calls it the most robust result. Relevance: challenges C1, C2, C3; supports C4.

- **Original authors' response** (Mirzadeh et al., Appendix B of the ICLR camera-ready, arXiv v2). https://arxiv.org/abs/2410.05229 (full text at https://arxiv.org/html/2410.05229v2). (Paper text) Appendix B answers Ivanova et al. directly. It rejects modelling each question as a Bernoulli trial and argues an ideal reasoner should be degenerate per question (always right or always wrong), so its accuracy on renamed variants should match the original with no added variance. Relevance: defends C1. Caveat for our analysis: this is a normative claim about an ideal reasoner. It does not rebut the point that set-level accuracy over 100 sampled templates carries binomial sampling noise when per-question success rates are not 0 or 1.

- **Długosz et al. 2026** (entry in section 1) is the peer-reviewed form of the statistical critique: random effects per question, multiple-comparison correction and a number-magnitude confound.

- Not found: a stable published source on "Table 1 oddities" in the original paper. Neither the Ivanova post nor Długosz et al. discuss the original Table 1 by name (Ivanova discusses the "more than one standard deviation" criterion used in the main comparison).

## 3. Contamination and memorization of GSM8K

- **A Careful Examination of Large Language Model Performance on Grade School Arithmetic** (Zhang et al., 2024, NeurIPS 2024 Datasets and Benchmarks). https://arxiv.org/abs/2405.00332 . GSM1k mirrors GSM8K; accuracy drops of up to 8%, with some model families showing systematic overfitting and a positive correlation between likelihood of generating GSM8K text and the GSM8K-GSM1k gap. Frontier models show minimal overfitting and all models generalise to new problems. Relevance: supports a memorization component (C5) but suggests it is modest for frontier models.

- **Benchmarking Benchmark Leakage in Large Language Models** (Xu et al., 2024, arXiv preprint). https://arxiv.org/abs/2404.18824 . Perplexity and n-gram detectors across 31 LLMs find substantial instances of training on benchmark training and even test sets in math reasoning. Relevance: supports the contamination premise behind GSM-Symbolic.

- **Investigating Data Contamination in Modern Benchmarks for Large Language Models** (Deng et al., 2023, NAACL 2024). https://arxiv.org/abs/2311.09783 . Retrieval and test-slot-guessing probes show commercial LLMs can recover masked test content (MMLU, TruthfulQA). Not GSM8K-specific. Relevance: background for the contamination premise.

- **VarBench: Robust Language Model Benchmarking Through Dynamic Variable Perturbation** (Qian et al., 2024, arXiv preprint). https://arxiv.org/abs/2406.17681 . Extracts variables from GSM8K (and ARC, CSQA, TruthfulQA) test items and resamples their values each evaluation; abstract says this gives a more accurate assessment and mitigates contamination. Same idea as GSM-Symbolic, released earlier. Relevance: supports C2 (independent precursor).

- **Do Large Language Model Benchmarks Test Reliability?** (Vendrow et al., 2025, arXiv preprint). https://arxiv.org/abs/2502.03461 . Finds pervasive label errors in popular benchmarks and releases cleaned "platinum" versions (including GSM8K); frontier models still fail some elementary math word problems. Relevance: methodological; GSM8K label noise affects the GSM8K baseline that GSM-Symbolic compares against.

- **Physics of Language Models: Part 2.1, Grade-School Math and the Hidden Reasoning Process** (Ye et al., 2024, arXiv; ICML 2024 tutorial). https://arxiv.org/abs/2407.20311 . Controlled synthetic GSM-style experiments (iGSM) asking whether models learn reasoning skills or memorise templates; the abstract reports "hidden mechanisms" without a headline number. Relevance: challenges C5 in a controlled-training setting (the paper text argues models trained on such data do learn reasoning skills; not checked here beyond the abstract).

## 4. Perturbation and robustness benchmarks

- **Large Language Models Can Be Easily Distracted by Irrelevant Context** (Shi et al., 2023, ICML 2023). https://arxiv.org/abs/2302.00093 . GSM-IC adds irrelevant information to GSM8K problems; performance drops dramatically, and self-consistency or an instruction to ignore irrelevant information mitigates it. Relevance: precursor to C4; suggests a prompt-level mitigation GSM-NoOp re-runs should test.

- **PAL: Program-aided Language Models** (Gao et al., 2022, arXiv). https://arxiv.org/abs/2211.10435 . Offloads computation to a Python interpreter; the paper introduces GSM-Hard (GSM8K with larger numbers; paper text, not in abstract). Relevance: extends C2; large-number difficulty is the same confound Długosz et al. measure.

- **GSM-Plus: A Comprehensive Benchmark for Evaluating the Robustness of LLMs as Mathematical Problem Solvers** (Li et al., 2024, ACL 2024). https://arxiv.org/abs/2402.19255 . Eight-type perturbation extension of GSM8K; across 25 LLMs, models solving a GSM8K item can fail when statements are added or the question target changes. Relevance: supports C3 and C4.

- **Functional Benchmarks for Robust Evaluation of Reasoning Performance, and the Reasoning Gap** (Srivastava et al., 2024, arXiv preprint). https://arxiv.org/abs/2402.19450 . MATH() functional variants; "reasoning gap" between static and functional accuracy of 58% to 80% for SOTA models, with the caveat that better prompting likely shrinks it. Relevance: supports C2 on harder math.

- **Is Your Model Really A Good Math Reasoner? Evaluating Mathematical Reasoning with Checklist** (Zhou et al., 2024, arXiv preprint). https://arxiv.org/abs/2407.08733 . MathCheck-GSM tests task generalisation and robustness on 26 LLMs; GPT-4o-class models hold up while many other families decline. Relevance: supports C2 to C4 for weaker models, challenges their generality for frontier models.

- **Putnam-AXIOM: A Functional and Static Benchmark for Measuring Higher Level Mathematical Reasoning in LLMs** (Gulati et al., 2025; journal ref field lists ICML 2025). https://arxiv.org/abs/2508.08292 . 100 functional variants of Putnam problems; o1-preview drops from 41.9% by 19.6 points (46.8% relative), and ten of the other eighteen models show non-overlapping 95% CIs. Relevance: supports C2 at competition level, with CIs reported.

- **MATH-Perturb: Benchmarking LLMs' Math Reasoning Abilities against Hard Perturbations** (Huang et al., 2025, arXiv preprint). https://arxiv.org/abs/2502.06453 . 279 level-5 MATH items each with simple and hard perturbations; hard perturbations cut o1-mini by 16.49% and gemini-2.0-flash-thinking by 12.9%, and the authors describe models blindly applying learned methods. Relevance: supports C5 for reasoning models; separates difficulty-preserving from difficulty-changing edits, which is the axis the P1/P2 critique turns on.

- **GSM-Infinite: How Do Your LLMs Behave over Infinitely Increasing Context Length and Reasoning Complexity?** (Zhou et al., 2025, arXiv preprint). https://arxiv.org/abs/2502.05252 . Graph-based GSM generator with controllable noise nodes; sigmoid decline in accuracy as complexity rises, and exponentially more inference compute yields only linear gains. Relevance: extends C3 (difficulty scaling) and C4 (noise).

- **Mathematical Reasoning in Large Language Models: Assessing Logical and Arithmetic Errors across Wide Numerical Ranges** (Shrestha et al., 2025, arXiv preprint). https://arxiv.org/abs/2502.08680 . GSM-Ranges perturbs GSM8K numbers across scales; logical error rates rise up to 14 points as numbers grow, and arithmetic embedded in word problems degrades. Relevance: supports the number-magnitude confound raised against C2.

- **How Is LLM Reasoning Distracted by Irrelevant Context? An Analysis Using a Controlled Benchmark** (Yang et al., 2025, EMNLP 2025 main, pp. 13329-13347). https://arxiv.org/abs/2505.18761 ; https://aclanthology.org/2025.emnlp-main.674/ . GSM-DC injects controlled distractors into symbolic reasoning graphs; LLMs are sensitive to irrelevant context in path selection and arithmetic; training with strong distractors and PRM-guided tree search improve robustness. Relevance: supports C4 under controlled, unambiguous distractors.

- **Recitation over Reasoning: How Cutting-Edge Language Models Can Fail on Elementary School-Level Reasoning Problems?** (Yan et al., 2025, AACL-IJCNLP 2025). https://arxiv.org/abs/2504.00509 . RoR-Bench changes one phrase in a condition; top models such as o1 and DeepSeek-R1 lose up to 60% on elementary arithmetic and reasoning. Relevance: supports C5 on reasoning models.

- **Cats Confuse Reasoning LLM: Query Agnostic Adversarial Triggers for Reasoning Models** (Rajeev et al., 2025, CoLM 2025). https://arxiv.org/abs/2503.01781 . Short irrelevant suffixes found on DeepSeek V3 transfer to DeepSeek R1 and R1-distilled models, raising the chance of a wrong answer by over 300%. Triggers are adversarially optimised, unlike NoOp. Relevance: supports C4 for reasoning models.

- **Lost in the Noise: How Reasoning Models Fail with Contextual Distractors** (Lee et al., 2026, arXiv preprint). https://arxiv.org/abs/2601.07226 . NoisyBench across 11 datasets (RAG, reasoning, alignment, tool use): drops up to 80% with distractors, and more test-time compute can worsen performance under noise. Not GSM-specific. Relevance: supports C4 for 2025-2026 reasoning models.

- **Reasoning or Reciting? Exploring the Capabilities and Limitations of Language Models Through Counterfactual Tasks** (Wu et al., 2023, NAACL 2024). https://arxiv.org/abs/2307.02477 . Across 11 counterfactual task variants, performance is non-trivial but consistently degrades. Relevance: precursor to C5.

- **UGMathBench: A Diverse and Dynamic Benchmark for Undergraduate-Level Mathematical Reasoning with Large Language Models** (Xu et al., 2025, ICLR 2025). https://arxiv.org/abs/2501.13766 . Three randomised versions per problem; effective accuracy (all versions right) tops out at 56.3% (o1-mini), with large reasoning gaps. Relevance: supports C1 and C2 at undergraduate level.

- **Toward Automated Robustness Evaluation of Mathematical Reasoning** (Hou et al., 2025, Findings of ACL 2026 per arXiv comment). https://arxiv.org/abs/2506.05038 . MaSTer generates per-model adversarial rewrites of GSM8K and MATH-500 items with a rewrite-verify loop. Relevance: extends the template approach to adaptive perturbation.

- **BeyondBench: Contamination-Resistant Evaluation of Reasoning in Language Models** (Srivastava et al., 2025, ICLR 2026). https://arxiv.org/abs/2509.24210 . Algorithmic problem generation over 101 models; performance falls sharply with complexity and without tools. Relevance: extends the contamination-resistant generator idea beyond GSM.

## 5. GSM-NoOp data availability and licenses

- Apple's official release (GitHub moved from apple/ml-gsm-symbolic to https://github.com/apple-aiml-research/ml-gsm-symbolic ; HF https://huggingface.co/datasets/apple/GSM-Symbolic ) contains only `symbolic`, `p1` and `p2` templates and generated data. No NoOp set was released (checked the file listings and commit history on 2026-11-06; last data commit 2024-12-08). Data license: CC BY-NC-ND 4.0 (HF card and `generated_data/LICENSE-CC-BY-NC-ND-4.0.md`); the repo-level LICENSE is Apple's sample-code licence. The NoDerivatives term matters for any re-release of modified GSM-Symbolic items, NoOp variants included.
- **Experimental-Orange/gsm-noop-audited** (HF, updated 2026-05-26). https://huggingface.co/datasets/Experimental-Orange/gsm-noop-audited . Regenerated NoOp clauses for GSM-Symbolic, with GPT-5.5 and Opus audit labels and per-model results (Sturgeon, above). Card license `other` (`apple-sample-code`), and the LICENSE file is Apple's sample-code licence text. Code: https://github.com/BenSturgeon/gsm-symbolic-revisited (MIT).
- **deliaqu/llm-reasoning-decomposed** (GitHub, MIT, last push 2026-10-05). https://github.com/deliaqu/llm-reasoning-decomposed . Construction scripts for GSM-NoOp, GSM-Filler and GSM-Filler-DF (Qu et al., above). Its `data/README.md` states that the datasets are not yet included.
- Not a GSM-NoOp re-release: `LFrancis/GSM8k-NoOp-Plus` (HF, no license field) holds GSM8K test variants with typo, lexicon, syntax and similar perturbations. `charlotteyu18/GSM8K_Noop_Evaluation` (GitHub, MIT) contains only a LICENSE file.

## 6. Cross-domain control: renaming in TLA+ (ALIAS)

- **ALIAS: What Renaming Drops Measure in LLM-Written TLA+ Specifications** (LUC-AI4FM, replication package, under review). https://github.com/LUC-AI4FM/ALIAS at commit `8cd05808a952f3876a2e2705cb94e54b467789c2` (2026-10-12). The TLA+ analogue of GSM-Symbolic's name perturbation: 111 TLA+-Bench specifications renamed and re-verified with SANY and TLC. From the committed `runs/opus48_rerun/analysis.txt`, Claude Opus 4.8 falls from 28.3% to 18.2% under the name-based (role-based TLC) grader, a 10.1-point drop [5.0, 15.7]; from `runs/opus48_rerun/behavior_graded.json`, the behavior-based grader (refinement in both directions, no name matching) gives 32.1% clean vs 29.5% renamed (555 samples each), a 2.6-point drop. GPT-5 (`runs/v1_gpt5/`) drops 2.2 points [-0.4, 4.7] name-based and 9.0% vs 9.0% behavior-based. Relevance: in TLA+, most of the renaming drop for 2026-era models was produced by a grader that needs the original names, not by the model; in GSM-Symbolic the answer is a number, so that grader artefact cannot occur, which makes the two a useful pair (see REBUTTAL.md).

## 7. How models are deployed (raw API vs apps and agent harnesses)

- **Anthropic Economic Index report: Uneven geographic and enterprise AI adoption** (Appel et al., 2025, arXiv preprint). https://arxiv.org/abs/2511.15080 . Analyses one million Claude.ai conversations and one million first-party API transcripts and finds API customers automate more specialised tasks. It does not give each channel's share of total usage. Relevance: both raw-API and app use are large; we found no public source giving the split, so the share of "real" use that looks like GSM-Symbolic's bare greedy API call is unknown.

## Verification log

All fetched 2026-11-06. arXiv entries were verified through the arXiv API (export.arxiv.org, title, authors, comment fields and abstract) and abs pages where noted.

| URL | Method |
|---|---|
| https://arxiv.org/abs/2410.05229 | abs page + API |
| https://arxiv.org/html/2410.05229v2 | HTML full text (Appendix B) |
| https://proceedings.iclr.cc/paper_files/paper/2025/file/ec2e7a896f8250986b3907f57621ce94-Paper-Conference.pdf | HTTP 200 |
| https://arxiv.org/abs/2605.28700 | API + HTML full text |
| https://www.lesswrong.com/posts/Ze4C99Dasj74YKCFh/revisiting-gsm-symbolic-do-2026-frontier-models-still-fail | page fetch |
| https://arxiv.org/abs/2609.17804 | API + HTML full text |
| https://arxiv.org/abs/2605.07053 | API |
| https://arxiv.org/abs/2503.23084 | API |
| https://probapproxincorrect.substack.com/p/towards-more-rigorous-evaluations | page fetch |
| https://arxiv.org/abs/2405.00332 | API |
| https://arxiv.org/abs/2404.18824 | API |
| https://arxiv.org/abs/2311.09783 | API |
| https://arxiv.org/abs/2406.17681 | API |
| https://arxiv.org/abs/2502.03461 | API |
| https://arxiv.org/abs/2407.20311 | API |
| https://arxiv.org/abs/2302.00093 | API |
| https://arxiv.org/abs/2211.10435 | API |
| https://arxiv.org/abs/2402.19255 | API |
| https://arxiv.org/abs/2402.19450 | API |
| https://arxiv.org/abs/2407.08733 | API |
| https://arxiv.org/abs/2508.08292 | API |
| https://arxiv.org/abs/2502.06453 | API |
| https://arxiv.org/abs/2502.05252 | API |
| https://arxiv.org/abs/2502.08680 | API |
| https://arxiv.org/abs/2505.18761 | API |
| https://aclanthology.org/2025.emnlp-main.674/ | page fetch |
| https://arxiv.org/abs/2504.00509 | API |
| https://arxiv.org/abs/2503.01781 | API |
| https://arxiv.org/abs/2601.07226 | API |
| https://arxiv.org/abs/2307.02477 | API |
| https://arxiv.org/abs/2501.13766 | API |
| https://arxiv.org/abs/2506.05038 | API |
| https://arxiv.org/abs/2509.24210 | API |
| https://github.com/apple-aiml-research/ml-gsm-symbolic | GitHub API (metadata, contents, commits) |
| https://huggingface.co/datasets/apple/GSM-Symbolic | HF API |
| https://huggingface.co/datasets/Experimental-Orange/gsm-noop-audited | HF API + README + LICENSE |
| https://github.com/BenSturgeon/gsm-symbolic-revisited | GitHub API |
| https://github.com/deliaqu/llm-reasoning-decomposed | GitHub API + data/README.md |
| https://huggingface.co/datasets/LFrancis/GSM8k-NoOp-Plus | HF API + README |
| https://github.com/charlotteyu18/GSM8K_Noop_Evaluation | GitHub API |
| https://github.com/LUC-AI4FM/ALIAS (commit 8cd0580) | git clone, committed run files |
| https://arxiv.org/abs/2511.15080 | abs page |

Not verified, so not included: the OpenReview forum page (blocked by a browser check); a MathGPT.AI blog post reporting GSM-Symbolic P2 scores for R1-distilled and Qwen3 models (no primary source); a pith.science "simulated rebuttal" page (labelled simulated).
