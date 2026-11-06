#!/usr/bin/env bash
# Fetch the official GSM-Symbolic release (CC BY-NC-ND 4.0, Apple) at the commit we used.
set -euo pipefail
cd "$(dirname "$0")/.."
COMMIT=3b645c25d200bf950fb84e8cdcbfeccd91d6a8af
mkdir -p data
if [ ! -d data/ml-gsm-symbolic ]; then
  git clone https://github.com/apple/ml-gsm-symbolic data/ml-gsm-symbolic
fi
git -C data/ml-gsm-symbolic checkout -q "$COMMIT"
sha256sum data/ml-gsm-symbolic/generated_data/*.jsonl 2>/dev/null || shasum -a 256 data/ml-gsm-symbolic/generated_data/*.jsonl
