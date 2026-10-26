#!/usr/bin/env bash
# Keep both Modal endpoints warm during experiments (tiny request every 20 s). Stop with: pkill -f keepwarm.sh
R="$(cd "$(dirname "$0")/../.." && pwd)"; set -a; . "$R/.env"; set +a
while true; do
  for pair in "gemma4-31b $MODAL_URL_GEMMA" "gptoss-120b $MODAL_URL_GPTOSS"; do
    set -- $pair
    code=$(curl -s -m 30 -o /dev/null -w "%{http_code}" "$2/chat/completions" -H "Authorization: Bearer $MODAL_PROXY_TOKEN" \
      -H "Content-Type: application/json" -d "{\"model\":\"$1\",\"max_tokens\":1,\"messages\":[{\"role\":\"user\",\"content\":\"hi\"}]}")
    echo "$(date -u +%T) $1 $code"
  done
  sleep 20
done
