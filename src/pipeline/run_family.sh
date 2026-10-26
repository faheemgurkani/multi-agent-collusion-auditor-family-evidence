#!/usr/bin/env bash
# Run Colosseum for one family over the given configs, sequentially. Usage: run_family.sh <phase> <family> <cond...>
set -u
R="$(cd "$(dirname "$0")/../.." && pwd)"
PHASE=$1; FAM=$2; shift 2
cd "$R/starter/collusion_hackathon/colosseum"
if [ "$FAM" = "nemotron" ]; then unset LLM_BASE_URL LLM_API_KEY; export OR_PROVIDER_JSON='{"order":["DekaLLM"],"allow_fallbacks":false}';
else
  set -a; . "$R/.env"; set +a
  case $FAM in gemma) export LLM_BASE_URL="$MODAL_URL_GEMMA";; gptoss) export LLM_BASE_URL="$MODAL_URL_GPTOSS";; esac
  export LLM_API_KEY="$MODAL_PROXY_TOKEN"; unset OR_PROVIDER_JSON
fi
export TOGETHER_MAX_RETRIES=15 TOGETHER_RETRY_MAX_SLEEP_S=60  # ride out Modal cold starts / 503s
mkdir -p "$R/src/data/logs"
for C in "$@"; do
  echo "=== $(date -u +%FT%TZ) START $PHASE $FAM $C"
  COLOSSEUM_YES=1 uv run --python 3.11 python -m experiments.collusion.run --config "$R/src/configs/$PHASE/${FAM}_${C}.yaml" -y
  echo "=== $(date -u +%FT%TZ) END $PHASE $FAM $C rc=$?"
done
