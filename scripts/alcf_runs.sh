#!/usr/bin/env bash
# ALCF runs (no cash cost). Usage: scripts/alcf_runs.sh MODEL INSTANCES [WORKERS]
set -u
cd "$(dirname "$0")/.."
M=$1; I=$2; W=${3:-16}
python3 -m gsmsym.run "$M" gsm8k --workers "$W" 2>&1 | tail -1
for v in symbolic p1 p2; do python3 -m gsmsym.run "$M" $v --instances "$I" --workers "$W" 2>&1 | tail -1; done
