#!/usr/bin/env bash
# Cost of one worker run, read from the LiteLLM spend log (WSL).
# The window runs from task.md to final.txt of ~/.codex-runs/<task>, so
# parallel runs overlap; no key is needed, the database is local.
set -euo pipefail

task="${1:?usage: run-cost.sh <task>}"
run_dir="$HOME/.codex-runs/$task"
from=$(date -u -d "@$(( $(stat -c %Y "$run_dir/task.md") - 60 ))" '+%Y-%m-%d %H:%M:%S')
to=$(date -u -d "@$(( $(stat -c %Y "$run_dir/final.txt") + 60 ))" '+%Y-%m-%d %H:%M:%S')

cd "$HOME/services/litellm"
docker compose exec -T db psql -U litellm -d litellm -P pager=off -c "
SELECT model_group AS alias, count(*) AS calls,
       sum(prompt_tokens) AS input_tokens, sum(completion_tokens) AS output_tokens,
       round(sum(spend)::numeric, 4) AS usd
FROM \"LiteLLM_SpendLogs\"
WHERE \"startTime\" BETWEEN '$from' AND '$to' AND model_group LIKE 'worker-%'
GROUP BY 1;"
