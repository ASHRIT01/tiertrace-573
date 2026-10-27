#!/bin/bash
# Runs the remaining secondary-split jobs in order, ONE model process at a time. Resume-on-restart is the runner's own (records already in the file are skipped).
# If the runner exits without a DONE line it checks Ollama (starts it if needed), logs a RESTART note and relaunches; stops after 3 attempts without progress.
cd "$(dirname "$0")/.." || exit 1
for job in "$@"; do
  s=${job%:*}; k=${job#*:}; fails=0; out=runs/${s}_4b_v2_run$k.jsonl; log=runs/${s}_run_log.txt
  while true; do
    curl -s localhost:11434/api/version >/dev/null || { (nohup /opt/homebrew/bin/ollama serve >> runs/scratch/ollama_serve.log 2>&1 &); sleep 10; echo "$(date '+%F %T') | OLLAMA NOT RUNNING: started by supervisor | before $s run $k" >> $log; }
    before=$( [ -f $out ] && wc -l < $out || echo 0 )
    .venv/bin/python -u scripts/phase6_run.py $s $k >> runs/${s}_run$k.log 2>&1
    grep -q "| DONE | run $k |" $log && break
    after=$( [ -f $out ] && wc -l < $out || echo 0 )
    if [ "$after" -le "$before" ]; then fails=$((fails+1)); else fails=0; fi
    echo "$(date '+%F %T') | SUPERVISOR NOTE | run $k | runner exited without DONE; records in file: $after; consecutive attempts without progress: $fails" >> $log
    [ $fails -ge 3 ] && { echo "$(date '+%F %T') | SUPERVISOR STOP | $s run $k | no progress in 3 attempts" >> $log; exit 1; }
    sleep 20
  done
done
