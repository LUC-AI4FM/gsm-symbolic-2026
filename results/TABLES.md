# Results

Rebuilt by `python -m gsmsym.score` from `runs/*/raw.jsonl`. Accuracy in %, mean (± SD across instance sets) [number of complete sets]. Drop = GSM8K-100 minus variant, with a 95% paired bootstrap CI over templates. Answers parsed with the paper's last-number rule.

## API-decoded models (greedy where the API allows)

| Model | Route | GSM8K-100 | Symbolic | P1 | P2 | NoOp | NoOp (unanimous) |
|---|---|---|---|---|---|---|---|
| deepseek-v3.2 | bedrock | 96.4 | – | – | – | – | – |
| gemma-4-31b-it | alcf | 98.0 | 95.4 (±1.1) [10] | 95.5 (±1.3) [10] | 95.2 (±1.4) [10] | – | – |
| kimi-k3.1 | bedrock | 97.2 | – | – | – | – | – |
| llama3-8b-instruct | bedrock_completion | 77.0 | 73.6 (±1.8) [5] | 55.8 (±3.3) [5] | – | – | – |
| nemotron-super-3-120b | bedrock | 85.7 | – | – | – | – | – |

Drops (points) with 95% CI:

| Model | Symbolic | P1 | P2 | NoOp | NoOp (unanimous) |
|---|---|---|---|---|---|
| deepseek-v3.2 | – | – | – | – | – |
| gemma-4-31b-it | +2.6 [+0.1, +5.8] | +2.5 [-1.3, +6.3] | +2.8 [-3.8, +9.6] | – | – |
| kimi-k3.1 | – | – | – | – | – |
| llama3-8b-instruct | +3.4 [-4.0, +10.6] | +21.2 [+13.2, +29.2] | – | – | – |
| nemotron-super-3-120b | – | – | – | – | – |

## Claude models via Claude Code subagent (not API; default sampling, Claude Code system prompt, 50 problems per context)

| Model | Route | GSM8K-100 | Symbolic | P1 | P2 | NoOp | NoOp (unanimous) |
|---|---|---|---|---|---|---|---|
| claude-haiku-5-5-subagent | claude-code-subagent | 96.0 | 93.5 (±0.7) [2] | 94.5 (±0.7) [2] | 94.0 (±2.8) [2] | 92.7 (±0.1) [2] | 94.7 (±0.4) [2] |

Drops (points) with 95% CI:

| Model | Symbolic | P1 | P2 | NoOp | NoOp (unanimous) |
|---|---|---|---|---|---|
| claude-haiku-5-5-subagent | +2.5 [-1.0, +6.0] | +1.5 [-2.5, +6.0] | +2.0 [-6.0, +10.0] | +3.1 [-1.0, +7.7] | +0.0 [+0.0, +0.0] |

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
| gemma-4-31b-it | symbolic | 10 | 1.07 | 2.09 | 3.13 | yes |
| gemma-4-31b-it | p1 | 10 | 1.27 | 2.07 | 2.99 | yes |
| gemma-4-31b-it | p2 | 10 | 1.40 | 3.02 | 4.52 | yes |
| llama3-8b-instruct | symbolic | 5 | 1.82 | 4.41 | 7.33 | yes |
| llama3-8b-instruct | p1 | 5 | 3.27 | 4.97 | 8.17 | yes |

## Cash spend on Bedrock (from logged token usage x list price)

| Model | USD |
|---|---|
| deepseek-v3.2 | 0.22 |
| gemma-4-31b-it | 0.00 |
| kimi-k3.1 | 0.42 |
| llama3-8b-instruct | 0.66 |
| nemotron-super-3-120b | 0.05 |
| total | 1.35 |
