# Results

Rebuilt by `python -m gsmsym.score` from `runs/*/raw.jsonl`. Accuracy in %, mean (± SD across instance sets) [number of complete sets]. Drop = GSM8K-100 minus variant, with a 95% paired bootstrap CI over templates. Answers parsed with the paper's last-number rule.

## API-decoded models (greedy where the API allows)

| Model | Route | GSM8K-100 | Symbolic | P1 | P2 | NoOp | NoOp (unanimous) | NoOp-S | NoOp-S (irrelevant) |
|---|---|---|---|---|---|---|---|---|---|
| beam-1.0 | alcf | 97.0 | 95.4 (±1.3) [50] | 95.2 (±1.5) [50] | 94.8 (±2.1) [50] | 92.5 (±1.9) [50] | 96.8 (±1.8) [50] | 74.6 (±3.8) [10] | 94.9 (±5.0) [10] |
| deepseek-v3.2 | bedrock | 96.0 | 93.3 (±0.6) [3] | 92.7 (±1.2) [3] | 90.0 (±2.0) [3] | 90.9 (±1.7) [3] | 94.1 (±1.3) [3] | 66.5 (±1.8) [2] | 94.4 (±6.4) [2] |
| gemma-4-31b-it | alcf | 98.0 | 96.2 (±1.1) [50] | 95.4 (±1.4) [50] | 94.7 (±1.5) [50] | 94.4 (±1.6) [50] | 98.3 (±1.3) [50] | 77.3 (±3.3) [10] | 94.9 (±4.7) [10] |
| gpt-oss-120b | alcf | 80.0 | 77.5 (±3.1) [50] | 77.5 (±3.0) [50] | 77.0 (±4.5) [50] | 69.0 (±3.3) [50] | 72.1 (±3.3) [50] | 54.1 (±3.0) [10] | 81.2 (±8.3) [10] |
| gpt-oss-20b | alcf | 77.0 | 77.8 (±3.2) [50] | 77.0 (±2.5) [50] | 75.6 (±4.0) [50] | 63.8 (±4.3) [50] | 66.4 (±4.3) [50] | 51.8 (±3.5) [10] | 70.1 (±13.9) [10] |
| inkling | alcf | 97.0 | 95.9 (±1.2) [50] | 95.0 (±2.0) [50] | 94.1 (±2.2) [50] | 92.8 (±1.7) [50] | 97.5 (±1.3) [50] | – | – |
| kimi-k3.1 | bedrock | 96.0 | 98.0 [1] | 98.0 [1] | 96.0 [1] | 95.9 [1] | 96.6 [1] | – | – |
| llama-3.1-70b-instruct | alcf | 93.0 | – | – | – | – | – | – | – |
| llama-3.1-8b-instruct-completion | alcf_completion | 81.0 | 74.3 (±3.1) [50] | 62.1 (±4.0) [50] | 36.4 (±5.5) [50] | 65.3 (±3.8) [50] | 69.0 (±3.6) [50] | 29.6 (±4.1) [10] | 58.1 (±14.6) [10] |
| llama-4-scout | alcf | 88.0 | 84.4 (±2.3) [50] | 79.4 (±2.7) [50] | 67.5 (±5.2) [50] | 77.9 (±3.0) [50] | 82.5 (±3.0) [50] | 48.9 (±2.7) [10] | 76.9 (±15.2) [10] |
| llama3-8b-instruct | bedrock_completion | 77.0 | 73.6 (±1.8) [5] | 55.8 (±3.3) [5] | 32.8 (±3.0) [5] | 61.6 (±1.3) [5] | 63.6 (±2.9) [5] | 24.7 (±3.0) [5] | 44.8 (±21.3) [5] |
| mistral-large-2407 | alcf | 95.0 | 90.4 (±2.0) [50] | – | – | – | – | – | – |
| mistral-large-3-alcf | alcf | 92.0 | 87.0 (±2.8) [50] | 80.6 (±2.5) [50] | – | – | – | – | – |
| mistral-large-4-nvfp4 | alcf | 97.0 | 96.4 (±1.4) [50] | 95.7 (±1.7) [50] | 93.1 (±2.5) [50] | 92.7 (±1.8) [50] | 97.2 (±1.5) [50] | 71.8 (±3.3) [10] | 96.6 (±6.5) [10] |
| nemotron-3-ultra | alcf | 98.0 | 92.9 (±1.1) [10] | – | – | – | – | – | – |
| nemotron-35-super-vl | alcf | 98.0 | 95.9 (±1.0) [50] | 94.8 (±1.4) [50] | 90.8 (±2.6) [50] | 91.6 (±1.8) [50] | 96.7 (±1.4) [50] | 64.8 (±4.9) [10] | 94.9 (±4.1) [10] |
| nemotron-super-3-120b | bedrock | 95.0 | 95.0 (±0.7) [5] | 92.8 (±1.3) [5] | 85.2 (±3.6) [5] | 92.8 (±2.0) [5] | 96.9 (±1.3) [5] | – | – |

Drops (points) with 95% CI:

| Model | Symbolic | P1 | P2 | NoOp | NoOp (unanimous) | NoOp-S | NoOp-S (irrelevant) |
|---|---|---|---|---|---|---|---|
| beam-1.0 | +1.6 [-1.0, +4.3] | +1.8 [-2.0, +5.3] | +3.2 [-3.0, +9.2] | +4.1 [+0.5, +8.0] | +1.2 [-1.6, +3.6] | +22.4 [+17.3, +27.5] | +2.2 [-5.3, +10.0] |
| deepseek-v3.2 | +2.7 [+0.7, +4.7] | +3.3 [-0.7, +8.0] | +4.0 [-4.7, +13.3] | +5.0 [+1.4, +9.1] | +4.0 [+0.9, +7.6] | +30.6 [+23.0, +38.8] | +0.0 [+0.0, +0.0] |
| gemma-4-31b-it | +1.8 [-0.4, +4.5] | +2.6 [-1.0, +6.3] | +3.3 [-3.3, +10.0] | +3.2 [+0.6, +6.4] | +1.3 [-0.5, +3.4] | +21.0 [+16.1, +25.9] | +2.5 [+0.0, +7.0] |
| gpt-oss-120b | +2.5 [-3.8, +8.7] | +2.5 [-4.9, +9.5] | +1.0 [-9.5, +10.8] | +9.4 [+2.8, +15.9] | +7.3 [+0.8, +13.5] | +26.3 [+18.7, +33.8] | +5.2 [-2.0, +12.8] |
| gpt-oss-20b | -0.8 [-8.9, +6.9] | +0.0 [-8.2, +8.0] | -5.6 [-19.3, +7.3] | +11.9 [+4.1, +19.8] | +9.7 [+1.8, +17.3] | +25.8 [+17.6, +33.8] | +13.4 [+0.9, +26.2] |
| inkling | +1.1 [-1.6, +3.9] | +2.0 [-1.6, +5.4] | +3.9 [-2.0, +10.2] | +3.8 [+0.0, +7.9] | +1.4 [-1.7, +4.3] | – | – |
| kimi-k3.1 | -2.0 [-6.0, +2.0] | -2.0 [-6.0, +2.0] | +0.0 [-8.0, +8.0] | +0.0 [-6.2, +6.2] | +0.0 [-5.7, +5.7] | – | – |
| llama-3.1-70b-instruct | – | – | – | – | – | – | – |
| llama-3.1-8b-instruct-completion | +6.7 [+0.5, +13.0] | +18.9 [+11.8, +26.2] | +43.6 [+31.4, +55.7] | +15.1 [+7.7, +22.4] | +13.8 [+6.5, +20.9] | +52.0 [+43.6, +60.1] | +37.1 [+23.7, +50.7] |
| llama-4-scout | +3.6 [-2.3, +9.3] | +8.6 [+1.7, +15.4] | +18.5 [+7.0, +29.6] | +9.1 [+2.4, +15.6] | +6.9 [+0.5, +13.0] | +39.7 [+32.3, +47.1] | +15.5 [+3.2, +28.2] |
| llama3-8b-instruct | +3.4 [-4.2, +10.6] | +21.2 [+13.4, +29.0] | +43.2 [+29.6, +56.4] | +15.2 [+6.9, +23.5] | +13.8 [+5.1, +22.5] | +53.1 [+44.1, +61.7] | +53.3 [+32.9, +71.4] |
| mistral-large-2407 | +4.6 [+0.5, +8.8] | – | – | – | – | – | – |
| mistral-large-3-alcf | +5.0 [+0.8, +9.2] | +11.4 [+5.4, +17.5] | – | – | – | – | – |
| mistral-large-4-nvfp4 | +0.6 [-1.7, +3.0] | +1.3 [-2.9, +5.2] | +4.9 [-1.8, +11.7] | +3.9 [+0.5, +7.9] | +0.6 [-2.3, +3.5] | +25.7 [+20.4, +31.3] | +5.0 [+0.0, +11.0] |
| nemotron-3-ultra | +5.1 [+1.7, +9.0] | – | – | – | – | – | – |
| nemotron-35-super-vl | +2.1 [+0.4, +4.4] | +3.2 [-0.2, +6.8] | +7.2 [+0.0, +14.7] | +5.9 [+2.9, +9.6] | +2.8 [+1.2, +4.7] | +33.5 [+27.9, +39.2] | +4.5 [+0.5, +10.2] |
| nemotron-super-3-120b | +0.0 [-3.4, +3.6] | +2.2 [-2.4, +7.0] | +8.8 [-1.6, +19.2] | +1.9 [-2.2, +6.1] | +0.7 [-3.4, +4.8] | – | – |

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
| beam-1.0 | symbolic | 50 | 1.34 | 2.10 | 2.54 | yes |
| beam-1.0 | p1 | 50 | 1.48 | 2.14 | 2.57 | yes |
| beam-1.0 | p2 | 50 | 2.14 | 3.14 | 3.81 | yes |
| beam-1.0 | noop | 50 | 1.94 | 2.73 | 3.29 | yes |
| gemma-4-31b-it | symbolic | 50 | 1.12 | 1.92 | 2.30 | yes |
| gemma-4-31b-it | p1 | 50 | 1.37 | 2.09 | 2.53 | yes |
| gemma-4-31b-it | p2 | 50 | 1.54 | 3.17 | 3.86 | yes |
| gemma-4-31b-it | noop | 50 | 1.57 | 2.38 | 2.86 | yes |
| gpt-oss-120b | symbolic | 50 | 3.11 | 4.18 | 4.96 | yes |
| gpt-oss-120b | p1 | 50 | 2.96 | 4.18 | 4.96 | yes |
| gpt-oss-120b | p2 | 50 | 4.50 | 5.95 | 7.15 | yes |
| gpt-oss-120b | noop | 50 | 3.27 | 4.79 | 5.73 | yes |
| gpt-oss-20b | symbolic | 50 | 3.25 | 4.15 | 5.01 | yes |
| gpt-oss-20b | p1 | 50 | 2.48 | 4.21 | 5.04 | yes |
| gpt-oss-20b | p2 | 50 | 4.01 | 6.07 | 7.23 | yes |
| gpt-oss-20b | noop | 50 | 4.26 | 4.98 | 5.94 | yes |
| inkling | symbolic | 50 | 1.18 | 1.98 | 2.39 | yes |
| inkling | p1 | 50 | 1.98 | 2.18 | 2.65 | yes |
| inkling | p2 | 50 | 2.25 | 3.34 | 4.01 | yes |
| inkling | noop | 50 | 1.75 | 2.68 | 3.20 | yes |
| llama-3.1-8b-instruct-completion | symbolic | 50 | 3.11 | 4.37 | 5.24 | yes |
| llama-3.1-8b-instruct-completion | p1 | 50 | 3.97 | 4.85 | 5.83 | yes |
| llama-3.1-8b-instruct-completion | p2 | 50 | 5.51 | 6.80 | 8.16 | yes |
| llama-3.1-8b-instruct-completion | noop | 50 | 3.76 | 4.93 | 5.93 | yes |
| llama-4-scout | symbolic | 50 | 2.28 | 3.63 | 4.37 | yes |
| llama-4-scout | p1 | 50 | 2.68 | 4.05 | 4.91 | yes |
| llama-4-scout | p2 | 50 | 5.17 | 6.62 | 7.87 | yes |
| llama-4-scout | noop | 50 | 3.04 | 4.30 | 5.10 | yes |
| llama3-8b-instruct | symbolic | 5 | 1.82 | 4.41 | 7.44 | yes |
| llama3-8b-instruct | p1 | 5 | 3.27 | 4.97 | 8.20 | yes |
| llama3-8b-instruct | p2 | 5 | 3.03 | 6.64 | 11.26 | yes |
| llama3-8b-instruct | noop | 5 | 1.30 | 5.01 | 8.56 | yes |
| mistral-large-2407 | symbolic | 50 | 2.04 | 2.95 | 3.55 | yes |
| mistral-large-3-alcf | symbolic | 50 | 2.77 | 3.36 | 4.05 | yes |
| mistral-large-3-alcf | p1 | 50 | 2.50 | 3.95 | 4.71 | yes |
| mistral-large-4-nvfp4 | symbolic | 50 | 1.37 | 1.85 | 2.24 | yes |
| mistral-large-4-nvfp4 | p1 | 50 | 1.69 | 2.02 | 2.45 | yes |
| mistral-large-4-nvfp4 | p2 | 50 | 2.46 | 3.58 | 4.30 | yes |
| mistral-large-4-nvfp4 | noop | 50 | 1.78 | 2.70 | 3.23 | yes |
| nemotron-3-ultra | symbolic | 10 | 1.10 | 2.57 | 3.79 | yes |
| nemotron-35-super-vl | symbolic | 50 | 1.01 | 1.98 | 2.41 | yes |
| nemotron-35-super-vl | p1 | 50 | 1.36 | 2.21 | 2.63 | yes |
| nemotron-35-super-vl | p2 | 50 | 2.65 | 4.09 | 4.92 | yes |
| nemotron-35-super-vl | noop | 50 | 1.76 | 2.87 | 3.46 | yes |
| nemotron-super-3-120b | symbolic | 5 | 0.71 | 2.18 | 3.83 | yes |
| nemotron-super-3-120b | p1 | 5 | 1.30 | 2.58 | 4.30 | yes |
| nemotron-super-3-120b | p2 | 5 | 3.63 | 5.02 | 8.29 | yes |
| nemotron-super-3-120b | noop | 5 | 1.98 | 2.66 | 4.42 | yes |

## Parser sensitivity: paper rule vs format-aware rule (accuracy %)

The format-aware rule reads 'final answer is', \boxed{}, or 'Answer:' before falling back to the paper's last-number rule. Large gaps mean the paper rule scores formatting, not arithmetic.

| Model | GSM8K-100 | Symbolic | P1 | P2 | NoOp |
|---|---|---|---|---|---|
| beam-1.0 | 97.0 / 92.0 | 95.4 / 93.1 | 95.2 / 94.5 | 94.8 / 94.5 | 92.5 / 91.5 |
| claude-haiku-5-5-subagent | 96.0 / 96.0 | 93.5 / 93.5 | 94.5 / 94.5 | 94.0 / 94.0 | 92.7 / 92.7 |
| deepseek-v3.2 | 96.0 / 96.0 | 93.3 / 94.0 | 92.7 / 93.3 | 90.0 / 91.3 | 90.9 / 92.3 |
| gemma-4-31b-it | 98.0 / 98.0 | 96.2 / 96.2 | 95.4 / 95.4 | 94.7 / 94.7 | 94.4 / 94.4 |
| gpt-oss-120b | 80.0 / 89.0 | 77.5 / 85.2 | 77.5 / 84.5 | 77.0 / 85.1 | 69.0 / 78.9 |
| gpt-oss-20b | 77.0 / 87.0 | 77.8 / 86.4 | 77.0 / 85.9 | 75.6 / 82.7 | 63.8 / 79.0 |
| inkling | 97.0 / 97.0 | 95.9 / 95.9 | 95.0 / 95.1 | 94.1 / 94.1 | 92.8 / 92.8 |
| kimi-k3.1 | 96.0 / 96.0 | 98.0 / 98.0 | 98.0 / 98.0 | 96.0 / 96.0 | 95.9 / 97.9 |
| llama-3.1-70b-instruct | 93.0 / 93.0 | – | – | – | – |
| llama-3.1-8b-instruct-completion | 81.0 / 80.0 | 74.3 / 73.9 | 62.1 / 60.6 | 36.4 / 35.5 | 65.3 / 65.0 |
| llama-4-scout | 88.0 / 88.0 | 84.4 / 84.4 | 79.4 / 79.2 | 67.5 / 67.3 | 77.9 / 77.9 |
| llama3-8b-instruct | 77.0 / 77.0 | 73.6 / 72.2 | 55.8 / 54.4 | 32.8 / 32.0 | 61.6 / 61.1 |
| mistral-large-2407 | 95.0 / 96.0 | 90.4 / 92.6 | – | – | – |
| mistral-large-3-alcf | 92.0 / 91.0 | 87.0 / 89.3 | 80.6 / 87.4 | – | – |
| mistral-large-4-nvfp4 | 97.0 / 97.0 | 96.4 / 96.5 | 95.7 / 95.7 | 93.1 / 93.2 | 92.7 / 92.7 |
| nemotron-3-ultra | 98.0 / 98.0 | 92.9 / 92.9 | – | – | – |
| nemotron-35-super-vl | 98.0 / 98.0 | 95.9 / 95.9 | 94.8 / 94.9 | 90.8 / 90.8 | 91.6 / 91.6 |
| nemotron-super-3-120b | 95.0 / 95.0 | 95.0 / 95.0 | 92.8 / 93.0 | 85.2 / 86.0 | 92.8 / 93.0 |

## H1 check (pre-registered thresholds: Symbolic <= 2, P1 <= 5, P2 <= 10, NoOp <= 9.3 points)

| Model | Symbolic | P1 | P2 | NoOp | meets H1 | sets (min) |
|---|---|---|---|---|---|---|
| beam-1.0 | +1.6 ok | +1.8 ok | +3.2 ok | +4.1 ok | yes | 50 |
| claude-haiku-5-5-subagent | +2.5 no | +1.5 ok | +2.0 ok | +3.1 ok | no | 2 |
| deepseek-v3.2 | +2.7 no | +3.3 ok | +4.0 ok | +5.0 ok | no | 3 |
| gemma-4-31b-it | +1.8 ok | +2.6 ok | +3.3 ok | +3.2 ok | yes | 50 |
| gpt-oss-120b | +2.5 no | +2.5 ok | +1.0 ok | +9.4 no | no | 50 |
| gpt-oss-20b | -0.8 ok | +0.0 ok | -5.6 ok | +11.9 no | no | 50 |
| inkling | +1.1 ok | +2.0 ok | +3.9 ok | +3.8 ok | yes | 50 |
| kimi-k3.1 | -2.0 ok | -2.0 ok | +0.0 ok | +0.0 ok | yes | 1 |
| llama-3.1-8b-instruct-completion | +6.7 no | +18.9 no | +43.6 no | +15.1 no | no | 50 |
| llama-4-scout | +3.6 no | +8.6 no | +18.5 no | +9.1 ok | no | 50 |
| mistral-large-4-nvfp4 | +0.6 ok | +1.3 ok | +4.9 ok | +3.9 ok | yes | 50 |
| nemotron-35-super-vl | +2.1 no | +3.2 ok | +7.2 ok | +5.9 ok | no | 50 |
| nemotron-super-3-120b | +0.0 ok | +2.2 ok | +8.8 ok | +1.9 ok | yes | 5 |

## Cash spend on Bedrock (from logged token usage x list price)

| Model | USD |
|---|---|
| beam-1.0 | 0.00 |
| deepseek-v3.2 | 1.56 |
| gemma-4-31b-it | 0.00 |
| gpt-oss-120b | 0.00 |
| gpt-oss-20b | 0.00 |
| inkling | 0.00 |
| kimi-k3.1 | 5.52 |
| llama-3.1-70b-instruct | 0.00 |
| llama-3.1-8b-instruct-completion | 0.00 |
| llama-4-scout | 0.00 |
| llama3-8b-instruct | 1.23 |
| mistral-large-2407 | 0.00 |
| mistral-large-3-alcf | 0.00 |
| mistral-large-4-nvfp4 | 0.00 |
| nemotron-3-ultra | 0.00 |
| nemotron-35-super-vl | 0.00 |
| nemotron-super-3-120b | 0.85 |
| total | 9.15 |
