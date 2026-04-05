#!/usr/bin/env bash
# Find the most recent Claude Code session and its subagent transcripts.
# Usage: ./scripts/debug/find-session.sh [project-path]

set -euo pipefail

PROJECT_DIR="${1:-$(pwd)}"
CLAUDE_DIR="$HOME/.claude/projects"

# Encode the project path the way Claude Code does (/ → -, leading / becomes -)
ENCODED=$(echo "$PROJECT_DIR" | tr '/' '-')

SESSION_DIR="$CLAUDE_DIR/$ENCODED"

if [ ! -d "$SESSION_DIR" ]; then
  echo "No session directory found at: $SESSION_DIR"
  echo "Try listing: ls $CLAUDE_DIR/"
  exit 1
fi

echo "=== Session directory ==="
echo "$SESSION_DIR"
echo ""

echo "=== Most recent session directories (last 5) ==="
ls -lt "$SESSION_DIR" | grep '^d' | head -5 || echo "  (none)"
echo ""

echo "=== Subagent transcripts (last 10) ==="
find "$SESSION_DIR" -path "*/subagents/agent-*.jsonl" 2>/dev/null \
  | xargs ls -lt 2>/dev/null | head -10 || echo "  (none)"
echo ""

echo "=== Agent log (if exists) ==="
if [ -f /tmp/rts-agent-log.txt ]; then
  tail -20 /tmp/rts-agent-log.txt
else
  echo "  No agent log at /tmp/rts-agent-log.txt"
  echo "  (Will be created after SubagentStart/Stop hooks fire)"
fi
