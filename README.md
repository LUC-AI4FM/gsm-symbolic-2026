# GSM-Symbolic on 2026 models

A re-run of **GSM-Symbolic** (Mirzadeh et al., *Understanding the Limitations of Mathematical Reasoning in
Large Language Models*, ICLR 2025, [arXiv 2410.05229](https://arxiv.org/abs/2410.05229)) on models released
in 2025 and 2026, with the paper's prompt, shots, decoding and answer parser, a reproduction check on a
model the paper tested, a pre-registered hypothesis, and a rebuttal.

| Document | Contents |
|---|---|
| [PREREGISTRATION.md](PREREGISTRATION.md) | Hypotheses H1 to H3 and their thresholds, committed before scoring |
| [results/TABLES.md](results/TABLES.md) | Every table, rebuilt from the raw logs by `python -m gsmsym.score` |
| [REBUTTAL.md](REBUTTAL.md) | Which claims hold on 2026 models, which do not, and where the method is weak |
| [RELATED_WORK.md](RELATED_WORK.md) | Replications, critiques and follow-ups, each opened and checked |

<!--RESULTS-->

## Method

| Setting | Value |
|---|---|
| Data | Official release, [apple/ml-gsm-symbolic](https://github.com/apple/ml-gsm-symbolic) at `3b645c25`: Symbolic and P1 (100 templates × 50 instances), P2 (50 × 50) |
| Baseline | GSM8K-100: the 100 original GSM8K test questions behind the templates (paper Tab. 1, "GSM8K (100)") |
| NoOp | Not released by Apple. We rebuilt it (below) |
| Prompt | The README template: header, the 8 common GSM8K CoT exemplars (lm-evaluation-harness `c0745fec`), `Q: … A: Let's think step by step.` |
| Decoding | temperature 0 where the API allows; Kimi K3/K3.1 reject the field and use defaults; reasoning models keep default reasoning |
| Parser | The paper's rule: cut at `\nQ:`, drop commas, take the last number, compare as float. A "final answer is" parser is reported as a check |
| Metrics | Mean accuracy over instance sets, SD across sets, drop from GSM8K-100 with a 95% paired bootstrap CI over templates |
| Instance sets | A set is instance *k* of every template. Sets per model and variant are listed in each table cell |

**NoOp reconstruction.** For every Symbolic instance, Gemma 4 31B writes one sentence that contains a
number, sounds relevant and leaves the answer unchanged (the recipe of the paper's Fig. 7). GPT-OSS-120B and
Nemotron 3 Ultra then judge independently whether the answer stays the same. The sentence is inserted before
the item's final question sentence at run time. We report NoOp on all items and on items both judges call
UNCHANGED. Only our sentences are published (`noop/clauses.jsonl`); NoOp prompts are logged as hashes.

**Reproduction anchor.** Llama-3-8B-Instruct, which the paper tested, runs through raw text completion on
Bedrock (no chat template), the closest match to the paper's open-model setup. A first attempt through the
chat API with a `Q:` stop sequence cut every answer short (31/100); it is kept in `runs/_discarded/`.

## Routes and deployment mode

Deployment mode is a variable here, not a detail.

| Mode | Route | Models |
|---|---|---|
| Raw API decoding, as in the paper | Amazon Bedrock (Converse or raw completion) | Llama-3-8B-Instruct, DeepSeek V3.2, Nemotron 3 Super 120B, Kimi K3.1 |
| Raw API decoding, as in the paper | ALCF inference service (OpenAI-compatible) | Gemma 4 31B, GPT-OSS-120B, Nemotron 3 Ultra |
| Agent harness | Claude Code subagents | Claude Haiku 5.5 |

Claude models were run only as Claude Code subagents, never through a paid API. Each subagent gets 50
problems in one prompt (the 8 shots once, then each problem in the paper's format), answers by reasoning
only, and returns its text; batches where the subagent used any tool other than the final hand-off are
discarded (none were). Answers are then scored with the same parser. This is **not** comparable one-to-one
with API decoding: default sampling instead of greedy, the Claude Code system prompt, and 50 problems
sharing one context. These results are kept in a separate table.

The original paper decodes greedily from a bare prompt. That is one assumption about how models are used.
We found no public source giving the split between raw API use and app or agent-harness use; Anthropic's
Economic Index ([arXiv 2511.15080](https://arxiv.org/abs/2511.15080)) shows both channels are large but does
not give shares. So we report the modes side by side and do not claim either is "real" use.

**Not reached.** On Bedrock, Claude 4.7 to 5.5, GPT-5.4 to 6.1, Grok 4.6/4.7 and GLM-5.3 return
`AccessDeniedException` ("not available for this account"): access was never enabled for the account we
used, and enabling it means accepting new provider terms, which we did not do. Mistral Large 4 on ALCF
answered only in its reasoning channel and took about 80 s per item, so it was dropped.

<!--COST-->

## Reproducing

```bash
./scripts/fetch_data.sh                          # official data at the pinned commit
export GSMSYM_AWS_CMD="aws"                      # or your audited wrapper; needs bedrock-runtime access
export GSMSYM_ALCF_TOKEN_CMD="python inference_auth_token.py get_access_token"
python -m gsmsym.run deepseek-v3.2 symbolic --instances 0-4 --budget-usd 1
python -m gsmsym.noop generate --instances 0-9 && python -m gsmsym.noop judge --instances 0-9
python -m gsmsym.score                           # rebuilds results/ and figures/ from runs/
```

Claude Code subagent batches: `python -m gsmsym.subagent make --variant p1 --instances 0-1`, give each
`batches/*.txt` verbatim to a subagent, then `python3 scripts/collect_subagents.py <transcript dir>` and
`python -m gsmsym.subagent ingest --model claude-haiku-5-5-subagent`.

### Run folders

Same layout as [LUC-AI4FM/ALIAS](https://github.com/LUC-AI4FM/ALIAS). `custom_id` is
`<template>-<condition>-<instance>`, the ALIAS `<spec_id>-<condition>-<sample>` convention.

| File | Contents |
|---|---|
| `runs/<model>/requests.jsonl` | model id, route, decoding settings, prompt (NoOp: SHA-256 only) |
| `runs/<model>/raw.jsonl` | unedited response text, stop reason, token usage, UTC date, latency, errors |
| `runs/<model>/graded.json` | per item: `id`, `condition`, `instance`/`sample`, `pred`, `gold`, `pass`, `pass_final_rule` |
| `runs/<model>/provenance.jsonl` | code and input hashes, git head, model, route, decoding, per invocation |
| `runs/claude-*-subagent/batches/` | each subagent's full returned text and its tool and token counts |

<!--ALIAS-->

## Model output terms

We publish model outputs for research. Checked: Google's Gemma terms (§3.3, Google claims no rights in
outputs), the Meta Llama 3 license (outputs may not be used to improve other LLMs, §1.b.v; we publish
them for evaluation only; Built with Meta Llama 3), and Anthropic's Commercial Terms (customer owns outputs,
§B; no training of competing models, §D.4). Not reviewed clause by clause: DeepSeek (MIT model license),
Kimi (modified MIT), NVIDIA Nemotron (NVIDIA Open Model License), GPT-OSS (Apache 2.0); we found nothing in
these model cards restricting publication of outputs. **Do not use `runs/` to train models.**

## License

Code and our text: MIT ([LICENSE](LICENSE)). GSM-Symbolic data: CC BY-NC-ND 4.0, © Apple, not vendored;
request logs quote unmodified items with attribution. GSM8K: MIT.

## Citation

```bibtex
@misc{gsm-symbolic,
  title  = {GSM-Symbolic: Understanding the Limitations of Mathematical Reasoning in Large Language Models},
  author = {Iman Mirzadeh and Keivan Alizadeh and Hooman Shahrokhi and Oncel Tuzel and Samy Bengio and Mehrdad Farajtabar},
  year   = {2024}, url = {https://arxiv.org/abs/2410.05229}
}
```
