#!/usr/bin/env bash
set -euo pipefail

INPUT=$(cat)
read -r EVENT SESSION AGENT TYPE TRANSCRIPT <<< "$(echo "$INPUT" | jq -r '[
  .hook_event_name // "unknown",
  .session_id // "unknown",
  .agent_id // "unknown",
  .agent_type // "unknown",
  (.agent_transcript_path // "none")
] | @tsv')"

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
echo "[$TIMESTAMP] $EVENT session=$SESSION agent=$AGENT type=$TYPE transcript=$TRANSCRIPT" >> /tmp/rts-agent-log.txt
