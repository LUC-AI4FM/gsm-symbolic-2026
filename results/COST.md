# Cost

Bedrock cash spent so far (logged usage x list price): **$6.37**.

Full protocol per model: 17,300 items (GSM8K-100, Symbolic 50 sets, P1 50 sets, P2 50 sets, NoOp ~47 x 100).
Token use per item is measured from our runs, per variant.

| Model | Route | items run | spent USD | full: M input tok | full: M output tok | full-run USD |
|---|---|---|---|---|---|---|
| llama3-8b-instruct | bedrock_completion | 1350 | 0.71 | 14.1 | 8.1 | 9.11 |
| deepseek-v3.2 | bedrock | 175 | 0.22 | 14.3 | 6.2 | 20.35 |
| nemotron-super-3-120b | bedrock | 892 | 0.31 | 15.3 | 6.8 | 6.71 |
| kimi-k3.1 | bedrock | 423 | 5.13 | 15.3 | 10.5 | 224.06 |
| gemma-4-31b-it | alcf | 8030 | 0.00 | 15.4 | 3.6 | 0.00 |

Full run on all 4 Bedrock models: **$260.23** (remaining after spend so far: $253.86).
ALCF and Claude Code subagent routes cost no cash.
