# Cost

Bedrock cash spent so far (logged usage x list price): **$9.15**.

Full protocol per model: 17,300 items (GSM8K-100, Symbolic 50 sets, P1 50 sets, P2 50 sets, NoOp ~47 x 100).
Token use per item is measured from our runs, per variant.

| Model | Route | items run | spent USD | full: M input tok | full: M output tok | full-run USD |
|---|---|---|---|---|---|---|
| llama3-8b-instruct | bedrock_completion | 2299 | 1.23 | 14.1 | 8.2 | 9.17 |
| deepseek-v3.2 | bedrock | 1319 | 1.56 | 14.2 | 6.0 | 20.01 |
| nemotron-super-3-120b | bedrock | 2122 | 0.85 | 15.2 | 6.7 | 6.64 |
| kimi-k3.1 | bedrock | 447 | 5.52 | 15.3 | 10.8 | 227.91 |
| gemma-4-31b-it | alcf | 14480 | 0.00 | 15.3 | 3.4 | 0.00 |
| gpt-oss-120b | alcf | 4580 | 0.00 | 15.0 | 10.7 | 0.00 |
| nemotron-3-ultra | alcf | 1481 | 0.00 | 15.2 | 21.0 | 0.00 |
| mistral-large-3-alcf | alcf | 28 | 0.00 | 24.0 | 4.1 | 0.00 |
| mistral-large-4-nvfp4 | alcf | 95 | 0.00 | 14.2 | 15.3 | 0.00 |
| nemotron-35-super-vl | alcf | 199 | 0.00 | 14.9 | 11.0 | 0.00 |

Moved to ALCF (same weights served there, no cash): nemotron-super-3-120b -> nemotron-3-super-120b-alcf.
Not on ALCF, so Bedrock-only: llama3-8b-instruct, deepseek-v3.2, kimi-k3.1 (ALCF serves Llama-3.1-8B-Instruct, a close relative of the Llama-3-8B anchor, which we run there too).

Full-run quote for the Bedrock-only models: **$257.08**, of which $248.78 is beyond what is already spent; without Kimi K3.1: $29.17.
ALCF and Claude Code subagent routes cost no cash.
