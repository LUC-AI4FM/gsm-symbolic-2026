# Results

Rebuilt by `python -m gsmsym.score` from `runs/*/raw.jsonl`. Accuracy in %, mean (± SD across instance sets) [number of complete sets]. Drop = GSM8K-100 minus variant, with a 95% paired bootstrap CI over templates. Answers parsed with the paper's last-number rule.

## API-decoded models (greedy where the API allows)

| Model | Route | GSM8K-100 | Symbolic | P1 | P2 | NoOp | NoOp (unanimous) | NoOp-S | NoOp-S (irrelevant) |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v3.2 | bedrock | 96.0 | 93.3 (±0.6) [3] | 92.7 (±1.2) [3] | 90.0 (±2.0) [3] | 90.9 (±1.7) [3] | 94.1 (±1.3) [3] | 66.5 (±1.8) [2] | 94.4 (±6.4) [2] |
| gemma-4-31b-it | alcf | 98.0 | 96.2 (±1.1) [50] | 95.4 (±1.4) [50] | 94.7 (±1.5) [50] | 94.4 (±1.6) [50] | 98.8 (±1.3) [50] | 77.3 (±3.3) [10] | 94.9 (±4.7) [10] |
| gpt-oss-120b | alcf | 80.0 | 77.5 (±3.1) [50] | 77.3 (±2.5) [10] | 78.0 (±4.3) [10] | 70.3 (±2.1) [10] | 73.3 (±2.4) [10] | 54.1 (±3.0) [10] | 81.2 (±8.3) [10] |
| kimi-k3.1 | bedrock | 96.0 | 98.0 [1] | 98.0 [1] | 96.0 [1] | 95.9 [1] | 96.6 [1] | – | – |
| llama-3.1-8b-instruct-completion | alcf_completion | 81.0 | – | – | – | – | – | – | – |
| llama3-8b-instruct | bedrock_completion | 77.0 | 73.6 (±1.8) [5] | 55.8 (±3.3) [5] | 32.8 (±3.0) [5] | 61.6 (±1.3) [5] | 63.6 (±2.9) [5] | 24.7 (±3.0) [5] | 44.8 (±21.3) [5] |
| mistral-large-3-alcf | alcf | 92.0 | – | – | – | – | – | – | – |
| mistral-large-4-nvfp4 | alcf | 97.0 | 96.4 (±1.4) [50] | – | – | – | – | – | – |
| nemotron-3-ultra | alcf | 98.0 | 92.9 (±1.1) [10] | – | – | – | – | – | – |
| nemotron-35-super-vl | alcf | 98.0 | 95.9 (±1.0) [50] | 94.8 (±1.4) [50] | – | – | – | – | – |
| nemotron-super-3-120b | bedrock | 95.0 | 95.0 (±0.7) [5] | 92.8 (±1.3) [5] | 85.2 (±3.6) [5] | 92.8 (±2.0) [5] | 96.9 (±1.3) [5] | – | – |

Drops (points) with 95% CI:

| Model | Symbolic | P1 | P2 | NoOp | NoOp (unanimous) | NoOp-S | NoOp-S (irrelevant) |
|---|---|---|---|---|---|---|---|
| deepseek-v3.2 | +2.7 [+0.7, +4.7] | +3.3 [-0.7, +8.0] | +4.0 [-4.7, +13.3] | +5.0 [+1.4, +9.1] | +4.0 [+0.9, +7.8] | +30.6 [+23.0, +38.8] | +0.0 [+0.0, +0.0] |
| gemma-4-31b-it | +1.8 [-0.3, +4.4] | +2.6 [-1.1, +6.2] | +3.3 [-3.2, +10.2] | +3.2 [+0.6, +6.3] | +2.2 [-0.4, +5.4] | +21.0 [+16.1, +26.1] | +2.5 [+0.0, +7.0] |
| gpt-oss-120b | +2.5 [-3.8, +8.9] | +2.7 [-4.6, +10.1] | +0.0 [-11.0, +10.2] | +8.2 [+1.4, +15.0] | +7.2 [+0.2, +14.2] | +26.3 [+18.9, +33.8] | +5.2 [-1.9, +12.7] |
| kimi-k3.1 | -2.0 [-6.0, +2.0] | -2.0 [-6.0, +2.0] | +0.0 [-8.0, +8.0] | +0.0 [-6.2, +6.2] | +0.0 [-5.7, +5.7] | – | – |
| llama-3.1-8b-instruct-completion | – | – | – | – | – | – | – |
| llama3-8b-instruct | +3.4 [-4.2, +10.8] | +21.2 [+13.4, +29.2] | +43.2 [+29.2, +56.4] | +15.2 [+7.1, +23.6] | +13.8 [+5.2, +22.5] | +53.1 [+44.2, +61.6] | +53.3 [+34.3, +71.4] |
| mistral-large-3-alcf | – | – | – | – | – | – | – |
| mistral-large-4-nvfp4 | +0.6 [-1.7, +3.0] | – | – | – | – | – | – |
| nemotron-3-ultra | +5.1 [+1.7, +9.0] | – | – | – | – | – | – |
| nemotron-35-super-vl | +2.1 [+0.4, +4.5] | +3.2 [-0.2, +6.8] | – | – | – | – | – |
| nemotron-super-3-120b | +0.0 [-3.4, +3.6] | +2.2 [-2.4, +7.0] | +8.8 [-2.0, +19.2] | +1.9 [-2.2, +6.0] | +0.7 [-3.4, +4.7] | – | – |

## Claude models via Claude Code subagent (not API; default sampling, Claude Code system prompt, 50 problems per context)

| Model | Route | GSM8K-100 | Symbolic | P1 | P2 | NoOp | NoOp (unanimous) | NoOp-S | NoOp-S (irrelevant) |
|---|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5-subagent | claude-code-subagent | 96.0 | 93.5 (±0.7) [2] | 94.5 (±0.7) [2] | 94.0 (±2.8) [2] | 92.7 (±0.1) [2] | 95.9 (±0.7) [2] | 78.1 (±1.2) [2] | 100.0 (±0.0) [2] |

Drops (points) with 95% CI:

| Model | Symbolic | P1 | P2 | NoOp | NoOp (unanimous) | NoOp-S | NoOp-S (irrelevant) |
|---|---|---|---|---|---|---|---|
| claude-haiku-5-5-subagent | +2.5 [-1.0, +6.0] | +1.5 [-2.5, +6.0] | +2.0 [-6.0, +10.0] | +3.1 [-1.0, +7.7] | +2.7 [-1.1, +7.1] | +19.7 [+12.6, +26.8] | +0.0 [+0.0, +0.0] |

## Paper (Tab. 1, arXiv 2410.05229v2), for reference

| Model | GSM8K-100 | Symbolic | P1 | P2 | NoOp |
|---|---|---|---|---|---|
| Llama3-8b-instruct | 74.0 | 74.6 (±2.94) | 53.8 (±4.54) | 28.3 (±4.37) | 18.6 (±3.86) |
| Gemma2-27b-it | 92.0 | 88.3 (±2.56) | 80.7 (±4.07) | 63.4 (±4.14) | 30.0 (±3.39) |
| Phi-3.5-mini-instruct | 88.0 | 82.1 (±3.38) | 64.8 (±5.43) | 44.8 (±6.32) | 22.4 (±4.03) |
| GPT-4o-mini | 95.0 | 91.7 (±2.02) | 81.1 (±3.05) | 72.4 (±4.57) | 54.1 (±3.85) |
| GPT-4o | 95.0 | 94.9 (±1.87) | 93.9 (±2.59) | 88.0 (±3.43) | 63.1 (±4.53) |
| o1-mini | 93.0 | 94.5 (±1.58) | 94.3 (±2.57) | 89.1 (±3.56) | 66.0 (±4.6) |
| o1-preview | 96.0 | 92.7 (±1.82) | 95.4 (±1.72) | 94.0 (±2.38) | 77.4 (±3.84) |

## Variance across instance sets vs binomial expectation (H2)

| Model | Variant | sets | observed SD | binomial SD | 97.5th pct of binomial SD | consistent |
|---|---|---|---|---|---|---|
| gemma-4-31b-it | symbolic | 50 | 1.12 | 1.92 | 2.31 | yes |
| gemma-4-31b-it | p1 | 50 | 1.37 | 2.09 | 2.50 | yes |
| gemma-4-31b-it | p2 | 50 | 1.54 | 3.17 | 3.90 | yes |
| gemma-4-31b-it | noop | 50 | 1.57 | 2.38 | 2.88 | yes |
| gpt-oss-120b | symbolic | 50 | 3.11 | 4.18 | 5.01 | yes |
| gpt-oss-120b | p1 | 10 | 2.50 | 4.19 | 6.14 | yes |
| gpt-oss-120b | p2 | 10 | 4.32 | 5.86 | 8.64 | yes |
| gpt-oss-120b | noop | 10 | 2.10 | 4.73 | 6.88 | yes |
| llama3-8b-instruct | symbolic | 5 | 1.82 | 4.41 | 7.40 | yes |
| llama3-8b-instruct | p1 | 5 | 3.27 | 4.97 | 8.26 | yes |
| llama3-8b-instruct | p2 | 5 | 3.03 | 6.64 | 11.37 | yes |
| llama3-8b-instruct | noop | 5 | 1.30 | 5.01 | 8.34 | yes |
| mistral-large-4-nvfp4 | symbolic | 50 | 1.37 | 1.85 | 2.23 | yes |
| nemotron-3-ultra | symbolic | 10 | 1.10 | 2.57 | 3.84 | yes |
| nemotron-35-super-vl | symbolic | 50 | 1.01 | 1.98 | 2.40 | yes |
| nemotron-35-super-vl | p1 | 50 | 1.36 | 2.21 | 2.66 | yes |
| nemotron-super-3-120b | symbolic | 5 | 0.71 | 2.18 | 3.65 | yes |
| nemotron-super-3-120b | p1 | 5 | 1.30 | 2.58 | 4.39 | yes |
| nemotron-super-3-120b | p2 | 5 | 3.63 | 5.02 | 8.53 | yes |
| nemotron-super-3-120b | noop | 5 | 1.98 | 2.66 | 4.49 | yes |

## Parser sensitivity: paper rule vs format-aware rule (accuracy %)

The format-aware rule reads 'final answer is', \boxed{}, or 'Answer:' before falling back to the paper's last-number rule. Large gaps mean the paper rule scores formatting, not arithmetic.

| Model | GSM8K-100 | Symbolic | P1 | P2 | NoOp |
|---|---|---|---|---|---|
| claude-haiku-5-5-subagent | 96.0 / 96.0 | 93.5 / 93.5 | 94.5 / 94.5 | 94.0 / 94.0 | 92.7 / 92.7 |
| deepseek-v3.2 | 96.0 / 96.0 | 93.3 / 94.0 | 92.7 / 93.3 | 90.0 / 91.3 | 90.9 / 92.3 |
| gemma-4-31b-it | 98.0 / 98.0 | 96.2 / 96.2 | 95.4 / 95.4 | 94.7 / 94.7 | 94.4 / 94.4 |
| gpt-oss-120b | 80.0 / 89.0 | 77.5 / 85.2 | 77.3 / 84.2 | 78.0 / 86.0 | 70.3 / 79.5 |
| kimi-k3.1 | 96.0 / 96.0 | 98.0 / 98.0 | 98.0 / 98.0 | 96.0 / 96.0 | 95.9 / 97.9 |
| llama-3.1-8b-instruct-completion | 81.0 / 80.0 | – | – | – | – |
| llama3-8b-instruct | 77.0 / 77.0 | 73.6 / 72.2 | 55.8 / 54.4 | 32.8 / 32.0 | 61.6 / 61.1 |
| mistral-large-3-alcf | 92.0 / 91.0 | – | – | – | – |
| mistral-large-4-nvfp4 | 97.0 / 97.0 | 96.4 / 96.5 | – | – | – |
| nemotron-3-ultra | 98.0 / 98.0 | 92.9 / 92.9 | – | – | – |
| nemotron-35-super-vl | 98.0 / 98.0 | 95.9 / 95.9 | 94.8 / 94.9 | – | – |
| nemotron-super-3-120b | 95.0 / 95.0 | 95.0 / 95.0 | 92.8 / 93.0 | 85.2 / 86.0 | 92.8 / 93.0 |

## H1 check (pre-registered thresholds: Symbolic <= 2, P1 <= 5, P2 <= 10, NoOp <= 9.3 points)

| Model | Symbolic | P1 | P2 | NoOp | meets H1 | sets (min) |
|---|---|---|---|---|---|---|
| claude-haiku-5-5-subagent | +2.5 no | +1.5 ok | +2.0 ok | +3.1 ok | no | 2 |
| deepseek-v3.2 | +2.7 no | +3.3 ok | +4.0 ok | +5.0 ok | no | 3 |
| gemma-4-31b-it | +1.8 ok | +2.6 ok | +3.3 ok | +3.2 ok | yes | 50 |
| gpt-oss-120b | +2.5 no | +2.7 ok | +0.0 ok | +8.2 ok | no | 10 |
| kimi-k3.1 | -2.0 ok | -2.0 ok | +0.0 ok | +0.0 ok | yes | 1 |
| nemotron-super-3-120b | +0.0 ok | +2.2 ok | +8.8 ok | +1.9 ok | yes | 5 |

## Cash spend on Bedrock (from logged token usage x list price)

| Model | USD |
|---|---|
| deepseek-v3.2 | 1.56 |
| gemma-4-31b-it | 0.00 |
| gpt-oss-120b | 0.00 |
| kimi-k3.1 | 5.52 |
| llama-3.1-8b-instruct-completion | 0.00 |
| llama3-8b-instruct | 1.23 |
| mistral-large-3-alcf | 0.00 |
| mistral-large-4-nvfp4 | 0.00 |
| nemotron-3-ultra | 0.00 |
| nemotron-35-super-vl | 0.00 |
| nemotron-super-3-120b | 0.85 |
| total | 9.15 |
