#!/usr/bin/env bash
# Run the full protocol for several ALCF models in order. A model that does not answer a probe
# (cold or unavailable) is deferred to the end of the lane and probed once more.
# Usage: PUSH=1 scripts/alcf_lane.sh WORKERS MODEL...
set -u
cd "$(dirname "$0")/.."
W=$1; shift
probe() { python3 - "$1" <<'PY'
import sys
from gsmsym import routes
from gsmsym.models import MODELS
m = MODELS[sys.argv[1]]
try:
    routes.alcf(m["id"], "What is 2+3? Reply with the number.", cluster=m["cluster"], max_tokens=1024, stop=None,
                completion=m["route"] == "alcf_completion")
except Exception as e:
    print("probe failed:", e); sys.exit(1)
PY
}
deferred=()
for M in "$@"; do
  if probe "$M"; then ./scripts/alcf_full.sh "$M" "$W"; else echo "DEFERRED $M"; deferred+=("$M"); fi
done
for M in "${deferred[@]:-}"; do
  [ -n "$M" ] || continue
  if probe "$M"; then ./scripts/alcf_full.sh "$M" "$W"; else echo "UNAVAILABLE $M"; fi
done
echo LANE_DONE
