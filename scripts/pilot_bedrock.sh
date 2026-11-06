#!/usr/bin/env bash
# Pilot on Bedrock: instance sets per variant, with per-model spend caps (USD, cumulative per model).
set -u
cd "$(dirname "$0")/.."
run(){ python3 -m gsmsym.run "$@" 2>&1 | tail -2; }
for v in symbolic p1 p2; do run llama3-8b-instruct $v --instances 0-4 --budget-usd 1.0; done &
( run nemotron-super-3-120b gsm8k --budget-usd 0.6; for v in symbolic p1 p2; do run nemotron-super-3-120b $v --instances 0-4 --budget-usd 0.6; done ) &
( run deepseek-v3.2 gsm8k --budget-usd 1.5; for v in symbolic p1 p2; do run deepseek-v3.2 $v --instances 0-2 --budget-usd 1.5; done ) &
( run kimi-k3.1 gsm8k --budget-usd 5.0 --workers 8; for v in symbolic p1 p2; do run kimi-k3.1 $v --instances 0 --budget-usd 5.0 --workers 8; done ) &
wait
