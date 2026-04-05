# Plan: Fix agent invocation, observability, and permission infrastructure

**Branch:** `chore/agent-observability`
**Category:** B (Infrastructure chore)
**Estimated steps:** 7

---

## Problem statement

Custom subagents (planner-science, executor, etc.) are NOT being invoked as
actual subagents. Evidence: "Allow this bash command?" prompts appear for
planner tasks, the UI shows Sonnet (main session model), and the planner
executes Python analysis scripts instead of producing read-only plans.

Root causes (from Claude Code docs + GitHub issues research):
1. No `permissionMode` set on agents → they inherit "Ask before edits"
2. No `color` field → no visual feedback when agent IS running
3. No SubagentStart/Stop hooks → no logging to confirm invocation
4. No debugging tooling → can't find current session transcripts
5. Missing Bash allow patterns → even if agent runs, Bash calls get blocked
6. The `@planner-science` text might be typed as plain text rather than
   picked from the typeahead → Claude treats it as natural language hint

---

## Step 1 — Add colors and permissionMode to all agent frontmatter

**Files:** All 5 files in `.claude/agents/`

### `.claude/agents/planner-science.md`

Replace the YAML frontmatter with:

```yaml
---
name: planner-science
description: >
  Thesis methodology planner with deep scientific reasoning. Use for: Phase
  work architecture (Phases 0-10), scientific invariant evaluation, data
  exploration strategy, statistical methodology, feature engineering design,
  evaluation framework, cross-game comparability, ML pipeline architecture.
  Triggers: "plan phase", "thesis strategy", "methodology", "scientific
  review", or any planning task involving thesis science. MUST be used
  proactively for any data science planning.
model: opus
effort: max
color: purple
permissionMode: plan
tools:
  - Read
  - Grep
  - Glob
  - Bash
---
```

Changes: added `color: purple`, added `permissionMode: plan`, added
"MUST be used proactively" to description (improves auto-delegation per docs).
The markdown body (system prompt) stays unchanged.

### `.claude/agents/planner.md`

Add to frontmatter:

```yaml
color: blue
permissionMode: plan
```

### `.claude/agents/executor.md`

Add to frontmatter:

```yaml
color: green
```

Do NOT add permissionMode — executor needs write access.

### `.claude/agents/reviewer.md`

Add to frontmatter:

```yaml
color: orange
```

Do NOT add permissionMode — reviewer needs read + bash for tests/lint.

### `.claude/agents/lookup.md`

Add to frontmatter:

```yaml
color: cyan
```

### Gate: Run `claude agents` from terminal. All 5 agents should appear with their colors listed.

---

## Step 2 — Add SubagentStart/Stop logging hooks

**File:** `.claude/settings.json`

Add these hook entries alongside the existing PostToolUse and PreToolUse hooks:

```json
{
  "hooks": {
    "SubagentStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo \"[$(date '+%H:%M:%S')] SUBAGENT START: type=$(echo $AGENT_INPUT | jq -r '.agent_type // \"unknown\"')\" >> /tmp/rts-agent-log.txt"
          }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo \"[$(date '+%H:%M:%S')] SUBAGENT STOP: type=$(echo $AGENT_INPUT | jq -r '.agent_type // \"unknown\"') transcript=$(echo $AGENT_INPUT | jq -r '.agent_transcript_path // \"none\"')\" >> /tmp/rts-agent-log.txt"
          }
        ]
      }
    ]
  }
}
```

Keep all existing hooks (PostToolUse for lint-on-edit, PreToolUse for
guard-write-path). Just add the two new event types.

### Gate: After saving, start a new session, invoke any agent. Check `cat /tmp/rts-agent-log.txt` for entries.

---

## Step 3 — Add a session-finder debug script

**File:** `scripts/debug/find-session.sh`

```bash
#!/usr/bin/env bash
# Find the most recent Claude Code session and its subagent transcripts.
# Usage: ./scripts/debug/find-session.sh [project-path]

set -euo pipefail

PROJECT_DIR="${1:-$(pwd)}"
CLAUDE_DIR="$HOME/.claude/projects"

# Encode the project path the way Claude Code does (/ → -)
ENCODED=$(echo "$PROJECT_DIR" | sed 's|^/||' | tr '/' '-')

SESSION_DIR="$CLAUDE_DIR/$ENCODED"

if [ ! -d "$SESSION_DIR" ]; then
  echo "No session directory found at: $SESSION_DIR"
  echo "Try listing: ls $CLAUDE_DIR/"
  exit 1
fi

echo "=== Session directory ==="
echo "$SESSION_DIR"
echo ""

echo "=== Most recent session files (last 5) ==="
ls -lt "$SESSION_DIR"/*.jsonl 2>/dev/null | head -5 || echo "  (none)"
echo ""

echo "=== Subagent transcripts (last 10) ==="
ls -lt "$SESSION_DIR"/agent-*.jsonl 2>/dev/null | head -10 || echo "  (none)"
echo ""

echo "=== Agent log (if exists) ==="
if [ -f /tmp/rts-agent-log.txt ]; then
  tail -20 /tmp/rts-agent-log.txt
else
  echo "  No agent log at /tmp/rts-agent-log.txt"
  echo "  (Will be created after SubagentStart/Stop hooks fire)"
fi
```

Then: `chmod +x scripts/debug/find-session.sh`

Also create the parent directory: `mkdir -p scripts/debug`

### Gate: Script runs without errors and shows session directory.

---

## Step 4 — Add missing Bash allow patterns to settings.json

**File:** `.claude/settings.json`

The current allow list is missing patterns that agents need. Add these to
the `permissions.allow` array:

```json
"Bash(python3 -c *)",
"Bash(python3 -m pytest*)",
"Bash(echo *)",
"Bash(wc -l *)",
"Bash(sort *)",
"Bash(date *)",
"Bash(jq *)",
"Bash(du *)"
```

This prevents "Allow this bash command?" prompts for common read-only
operations that planners and executors run constantly.

**Important:** Do NOT add `Bash(python3 *)` as a broad pattern — that would
allow arbitrary script execution. The `-c` flag pattern covers inline
analysis snippets; `pytest` covers test runs.

### Gate: Run a session, try `python3 -c "print('hello')"` — should execute without permission prompt.

---

## Step 5 — Add TodoWrite to planner agents' tools

**Files:** `.claude/agents/planner-science.md`, `.claude/agents/planner.md`

Both planners currently have `tools: Read, Grep, Glob, Bash`. They also
need `TodoWrite` so they can create structured task lists (the TodoWrite
tool is how agents output structured plans without needing file Write
access).

Update both agents' tools lists:

```yaml
tools:
  - Read
  - Grep
  - Glob
  - Bash
  - TodoWrite
```

### Gate: The planner can create todo items without needing Write permission.

---

## Step 6 — Update AGENT_MANUAL.md with debugging section

**File:** `docs/AGENT_MANUAL.md`

Replace the existing `## Troubleshooting` section with an expanded version:

```markdown
## Troubleshooting

**Agent not being invoked:** Claude sometimes handles tasks in the main
session instead of delegating. Three fixes, in order of reliability:

1. Use the `@` typeahead picker (type `@`, select from dropdown) — this
   *guarantees* invocation, unlike typing `@agent-name` as plain text.
2. Use explicit phrasing: "Use the planner-science agent to plan..."
3. Nuclear option: `claude --agent planner-science` from the integrated
   terminal to run the entire session as that agent.

**How to verify an agent actually ran:**

1. Check `/tmp/rts-agent-log.txt` — our SubagentStart/Stop hooks log
   every invocation with timestamps and transcript paths.
2. Run `./scripts/debug/find-session.sh` to find subagent transcripts.
3. Look for the agent's color badge in the UI (purple = planner-science,
   blue = planner, green = executor, orange = reviewer, cyan = lookup).
4. Press Ctrl+O to toggle verbose mode — subagent spawning shows in the
   tool call stream.

**Permission prompt appearing for read-only agents:** If planner-science
shows "Allow this bash command?", the agent wasn't invoked as a subagent
(planners use `permissionMode: plan` which is read-only). You're seeing
the main session's permission mode. Fix: use `@` typeahead or `--agent`.

**Agent loaded but using wrong model:** Run `claude agents` from the
terminal. The model should show next to each agent name. If it shows
`inherit`, the frontmatter `model:` field isn't being picked up —
check YAML syntax. For definitive testing, set
`export CLAUDE_CODE_SUBAGENT_MODEL=opus` before launching.

**VSCode extension vs integrated terminal:** The extension panel and the
integrated terminal (`Ctrl+\``) share the same engine but the extension
has limited TTY support. For agent-heavy work, prefer the integrated
terminal. Run `claude` directly to get full subagent support.

**Agent colors:**
| Agent | Color | Model |
|-------|-------|-------|
| planner-science | purple | Opus |
| planner | blue | Sonnet |
| executor | green | Sonnet |
| reviewer | orange | Sonnet |
| lookup | cyan | Haiku |
```

### Gate: The new troubleshooting section is accurate and references all new debugging tools.

---

## Step 7 — Verification checklist

Run these checks after all changes are saved:

1. `claude agents` — all 5 agents listed with correct models and colors
2. Start new session in integrated terminal (not extension panel)
3. Type `@` and verify `planner-science` appears in typeahead
4. Select it, paste a short test prompt: "Read PHASE_STATUS.yaml and
   summarize current phase"
5. Verify: purple color badge visible, no permission prompts, output is
   read-only (no file writes attempted)
6. After completion: `cat /tmp/rts-agent-log.txt` shows START and STOP
   entries with agent type = "planner-science"
7. `./scripts/debug/find-session.sh` shows a new `agent-*.jsonl` file

If step 5 still shows permission prompts or no color badge:
- The subagent may not have loaded. Restart the session.
- Try `claude --agent planner-science` as a fallback.
- Check `claude agents` output for YAML parse errors.

### Gate: All 7 checks pass. Agent invocation is observable and verifiable.

---

## Files changed summary (steps 1–6)

| File | Action |
|------|--------|
| `.claude/agents/planner-science.md` | Edit frontmatter (color, permissionMode, description) |
| `.claude/agents/planner.md` | Edit frontmatter (color, permissionMode, tools) |
| `.claude/agents/executor.md` | Edit frontmatter (color) |
| `.claude/agents/reviewer.md` | Edit frontmatter (color) |
| `.claude/agents/lookup.md` | Edit frontmatter (color) |
| `.claude/settings.json` | Add SubagentStart/Stop hooks, add Bash allow patterns |
| `scripts/debug/find-session.sh` | New file |
| `scripts/hooks/log-subagent.sh` | New file (hook script for SubagentStart/Stop) |
| `docs/AGENT_MANUAL.md` | Replace Troubleshooting section |

---

## Safety and Performance Analysis (pre-steps 7–13)

| Hook | Latency | Failure mode | Verdict |
|------|---------|--------------|---------|
| `lint-on-edit.sh` (PostToolUse) | ~300–800 ms per .py edit (Poetry venv startup) | Non-blocking (`\|\| true`) | Acceptable |
| `guard-write-path.sh` (PreToolUse) | Sub-ms | Blocking (exit 2 blocks write) — relative path resolution assumes CWD = repo root | Acceptable; caveat documented in Step 9 |
| `log-subagent.sh` (SubagentStart/Stop) | <100 ms (4 jq calls + /tmp append) | **Medium risk**: `set -euo pipefail` exits non-zero on missing field — could block subagent spawn | Fixed in Step 8 |

---

## Step 8 — Harden `scripts/hooks/log-subagent.sh`

**File:** `scripts/hooks/log-subagent.sh`

Replace the four separate `echo "$INPUT" | jq -r '.<field>'` calls with a single
`jq` invocation using TSV output, and add `// "unknown"` fallbacks to every field.

New content:

```bash
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
```

Verification:
```bash
echo '{"hook_event_name":"SubagentStart","session_id":"s1","agent_id":"a1","agent_type":"task"}' | ./scripts/hooks/log-subagent.sh && tail -1 /tmp/rts-agent-log.txt
echo '{"hook_event_name":"SubagentStart"}' | ./scripts/hooks/log-subagent.sh && tail -1 /tmp/rts-agent-log.txt
```

Both must exit 0. Second invocation must log "unknown" values, not crash.

### Gate: Both test invocations exit 0; log shows "unknown" for missing fields.

---

## Step 9 — Add CWD caveat comment to `scripts/hooks/guard-write-path.sh`

**File:** `scripts/hooks/guard-write-path.sh`

Find the block that resolves relative paths (the line using `$(pwd)/$FILE_PATH`)
and add a comment immediately above it:

```bash
# Relative paths are resolved from CWD, which Claude Code sets to the repo root.
# Agents always use absolute paths, so this is safe in practice.
```

No logic change — comment only.

Verification: `bash -n scripts/hooks/guard-write-path.sh` exits 0.

### Gate: `bash -n` exits 0.

---

## Step 10 — Fix `scripts/debug/find-session.sh` subagent transcript lookup

**File:** `scripts/debug/find-session.sh`

Subagent transcripts live at `<session_dir>/<session_id>/subagents/agent-<agent_id>.jsonl`,
not at `<session_dir>/agent-*.jsonl`. Update accordingly:

```bash
echo "=== Most recent session directories (last 5) ==="
ls -lt "$SESSION_DIR" | grep '^d' | head -5 || echo "  (none)"
echo ""

echo "=== Subagent transcripts (last 10) ==="
find "$SESSION_DIR" -path "*/subagents/agent-*.jsonl" 2>/dev/null \
  | xargs ls -lt 2>/dev/null | head -10 || echo "  (none)"
echo ""
```

Also remove the old glob: `ls -lt "$SESSION_DIR"/*.jsonl`.

Verification: `./scripts/debug/find-session.sh` — output shows `subagents/` paths; no "none" when agents have run.

### Gate: Script exits 0 and shows correct subagent paths.

---

## Step 11 — Check for debug artifact references

Grep for `rts-agent-input-debug` across the repo:

```bash
grep -r "rts-agent-input-debug" .
```

If any references found in repo files (AGENT_MANUAL.md, find-session.sh, hooks): remove them.
If zero matches: no action needed. The `/tmp` file is an orphan that will disappear on next reboot.

### Gate: `grep -r "rts-agent-input-debug" .` returns zero matches.

---

## Step 12 — Update `docs/AGENT_MANUAL.md`

**File:** `docs/AGENT_MANUAL.md`

In the Troubleshooting section, update item 2 of "How to verify an agent actually ran":

> "Run `./scripts/debug/find-session.sh` to find subagent transcripts (stored under
> `<session_id>/subagents/agent-<agent_id>.jsonl`). The `transcript=` value in
> `/tmp/rts-agent-log.txt` gives the exact path."

Add a **Performance notes** subsection at the end of Troubleshooting:

```markdown
**PostToolUse lint latency:** `lint-on-edit.sh` adds ~300–800 ms per `.py` write
due to Poetry venv startup. During executor sessions writing many files, this is
expected — not a hang.

**Write guard and relative paths:** `guard-write-path.sh` resolves relative paths
from CWD. All agents use absolute paths by default, so this is transparent.
```

### Gate: Section accurately describes `subagents/` structure and latency expectations.

---

## Step 13 — CHANGELOG, version bump, and PR wrap-up

**Files:** `CHANGELOG.md`, `pyproject.toml`

Current version: `0.16.3`. Branch: `chore/` → patch bump. New version: `0.16.4`.

Move `[Unreleased]` → `[0.16.4] — 2026-04-05 (PR #35: chore/agent-observability)`.

CHANGELOG entries:

```
### Added
- SubagentStart/Stop hooks (`scripts/hooks/log-subagent.sh`) logging agent events
  to `/tmp/rts-agent-log.txt` with session ID, agent ID, type, and transcript path
- `scripts/debug/find-session.sh` — finds session directories and correlates
  subagent transcript paths
- `color` and `permissionMode` fields in all 5 agent frontmatter files
- New Bash allow patterns in `settings.json`: `python3 -c *`, `echo *`, `date *`,
  `jq *`, `du *`, `sort *`, `python3 -m pytest*`

### Changed
- `scripts/debug/find-session.sh` updated to search `<session_id>/subagents/`
  for agent transcripts (correct Claude Code layout)
- `scripts/hooks/log-subagent.sh` hardened: single jq call, `// "unknown"`
  fallbacks on all fields
- `docs/AGENT_MANUAL.md` Troubleshooting section expanded with transcript paths,
  lint latency note, and write-guard CWD caveat
```

Run final checks (no .py touched, so no pytest/mypy needed):

```bash
bash -n scripts/hooks/log-subagent.sh
bash -n scripts/hooks/lint-on-edit.sh
bash -n scripts/hooks/guard-write-path.sh
bash -n scripts/debug/find-session.sh
grep '^version' pyproject.toml   # must show 0.16.4
```

Then commit and propose PR (user executes git push and gh pr create):

```bash
git add .claude/agents/ .claude/settings.json \
        scripts/hooks/log-subagent.sh \
        scripts/debug/find-session.sh \
        scripts/hooks/guard-write-path.sh \
        docs/AGENT_MANUAL.md \
        CHANGELOG.md pyproject.toml
git commit -m "chore(agent-observability): add subagent observability hooks and debug tooling"
git commit -m "chore(release): bump version to 0.16.4"
```

### Gate: All `bash -n` checks pass; version = 0.16.4; user has push + PR commands ready.
