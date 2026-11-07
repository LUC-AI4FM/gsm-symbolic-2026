#!/usr/bin/env bash
# Full protocol for one ALCF model: GSM8K-100, 50 instance sets of Symbolic, P1, P2 and our NoOp,
# and the 10 sets of NoOp-S. Resumable (finished items are skipped). After each variant the tables are
# rebuilt and, with PUSH=1, committed and pushed. Usage: scripts/alcf_full.sh MODEL [WORKERS]
set -u
cd "$(dirname "$0")/.."
M=$1; W=${2:-12}
publish() {
  [ "${PUSH:-0}" = 1 ] || return 0
  until mkdir .publish.lock 2>/dev/null; do sleep 5; done
  python3 -m gsmsym.score >/dev/null 2>&1; python3 scripts/quote.py >/dev/null 2>&1
  git add runs results figures noop >/dev/null 2>&1
  git commit -qm "ALCF full protocol: $M $1

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" >/dev/null 2>&1 && \
    { git pull -q --rebase origin main >/dev/null 2>&1; git push -q origin HEAD:main >/dev/null 2>&1; }
  rmdir .publish.lock
}
python3 -m gsmsym.run "$M" gsm8k --workers "$W" 2>&1 | tail -1
for v in symbolic p1 p2 noop; do
  python3 -m gsmsym.run "$M" $v --instances 0-49 --workers "$W" 2>&1 | tail -1
  publish $v
done
python3 -m gsmsym.run "$M" noop2 --workers "$W" 2>&1 | tail -1
publish noop2
echo "FULL_DONE $M"
