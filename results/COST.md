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
| gpt-oss-120b | alcf | 4480 | 0.00 | 15.0 | 10.6 | 0.00 |
| nemotron-3-ultra | alcf | 1481 | 0.00 | 15.2 | 21.0 | 0.00 |

Full run on all 4 Bedrock models: **$263.72** (remaining after spend so far: $254.57).
ALCF and Claude Code subagent routes cost no cash.
