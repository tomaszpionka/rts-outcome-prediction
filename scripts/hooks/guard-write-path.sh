#!/usr/bin/env bash
set -euo pipefail

FILE_PATH=$(jq -r '.tool_input.file_path // .tool_input.path // empty' 2>/dev/null || echo "")
[ -z "$FILE_PATH" ] && exit 0

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo "")"

# Resolve to absolute
if [[ "$FILE_PATH" == /* ]]; then
  ABS_PATH="$FILE_PATH"
elif [[ "$FILE_PATH" == ~* ]]; then
  ABS_PATH="${FILE_PATH/#\~/$HOME}"
else
  # Relative paths are resolved from CWD, which Claude Code sets to the repo root.
  # Agents always use absolute paths, so this is safe in practice.
  ABS_PATH="$(pwd)/$FILE_PATH"
fi

# Inside repo — allow silently
if [ -n "$REPO_ROOT" ] && [[ "$ABS_PATH" == "$REPO_ROOT"* ]]; then
  exit 0
fi

# Inside home but outside repo — ask user
if [[ "$ABS_PATH" == "$HOME"* ]]; then
  echo '{"permissionDecision": "ask"}'
  exit 0
fi

# Outside home — block
echo "BLOCKED: Write to '$FILE_PATH' is outside your home directory." >&2
exit 2
