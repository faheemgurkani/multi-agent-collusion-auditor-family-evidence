#!/usr/bin/env bash
# After all agent runs finish: build views, summarise, audit new transcripts with every auditor, probe, analyse.
# Modal auditors run behind keep-warm (stopped at the end); Nemotron's remaining audits run after audit_pipeline2.
set -u
R="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$R/src/pipeline"; PY="$R/.venv/bin/python"; L="$R/src/data/logs"
for p in main main_ext; do "$PY" -u build_views.py --phase $p; done
"$PY" -u summarize.py --phase main            # glob main_* covers main_ext
nohup ./keepwarm.sh > "$L/keepwarm.log" 2>&1 &
until [ "$(tail -2 "$L/keepwarm.log" | grep -c ' 200$')" -ge 2 ]; do sleep 15; done
echo "$(date -u +%T) endpoints warm"
"$PY" -u audit.py --phase main --k 3 --auditors gemma gptoss
"$PY" -u audit.py --phase main --probe --auditors gemma gptoss
pkill -f keepwarm.sh; echo "$(date -u +%T) keep-warm stopped"
until grep -q PIPELINE_DONE "$L/audit_pipeline2.log"; do sleep 30; done
"$PY" -u audit.py --phase main --k 3 --auditors nemotron
"$PY" -u audit.py --phase main --probe --auditors nemotron
"$PY" -u ../analysis/analyze.py --phase main --boot 10000 --perm 5000
echo FINALIZE_DONE
