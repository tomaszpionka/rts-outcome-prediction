# Audit: Insights Suggestions vs Current Setup

## 1. Report Confirmation

Successfully read the full HTML report at `~/.claude/usage-data/report.html`.
Last paragraph (fun ending): *"User asked for repo subdirectory sizes... and an
ASCII lego human. Claude delivered both without blinking."*

---

## 2. CLAUDE.md Suggested Additions — Validation

### Suggestion 1: "Always create a feature branch before making changes"
- **Already covered?** PARTIALLY. `settings.json` denies `git commit`/`git push`
  but Claude can still *write files* while on master.
- **Verdict: ADOPT.** Add explicit "never work on master" to Critical Rules.
  Enforce at runtime with a PreToolUse branch guard hook (see §3).

### Suggestion 2: "Read plan once, act immediately — don't over-explore"
- **Verdict: DROP.** User's actual workflow is deliberate multi-step: Opus reads
  plan → splits into `specs_N.md` files → executor subagents consume specs.
  This is intentionally multi-read, not "stalling." Rule would fight the workflow.

### Suggestion 3: "Always update CHANGELOG.md for PRs"
- **Already covered?** YES — `git-workflow.md` steps 3-5 and checklist #3.
- **Verdict: SKIP.** Friction was from Claude ignoring existing rules, not missing.

### Suggestion 4: "Absolute paths for PR body files"
- **Verdict: ADOPT (refined).** Consolidate all ephemeral artifacts to
  `.github/tmp/`: `pr.txt` (already there) and `commit.txt` (migrate from
  `temp/commit_msg.txt`). Update git-workflow.md and memory accordingly.

### Suggestion 5: "Read-only planning — don't write files"
- **Already covered?** YES — CLAUDE.md § Planning Protocol #1-3.
- **Verdict: SKIP.**

### Suggestion 6: "Respond in chat, don't write to files unless asked"
- **Verdict: DROP.** User prefers markdown file preview over terminal output.
  Adding this rule would fight the user's preference.

---

## 3. Feature Suggestions — Validation

### Feature 1: Custom Skills (/pr, /execute-plan)
- **Verdict: PLAN SEPARATELY.** Good idea, separate Category C chore after this.

### Feature 2: PreToolUse hook to block edits on master
- **Verdict: ADOPT.** Highest-ROI change — prevents the #1 friction source.

### Feature 3: Headless Mode
- **Verdict: DROP.** User's supervisory CLI workflow (running commands and
  subagents directly) is peak performance for them.

---

## 4. Memory Audit

### Index integrity
- `MEMORY.md` lists 10 entries
- Directory contains 12 .md files (including MEMORY.md)
- **1 orphan:** `feedback_poetry_venv.md` — NOT in MEMORY.md

### The venv activation question

Two contradictory memories exist:

| File | Says | Date |
|------|------|------|
| `feedback_poetry_venv.md` (orphan) | ALWAYS prefix with `source .venv/bin/activate &&` | Apr 4 |
| `feedback_no_source_activate.md` (indexed) | NEVER prefix — use bare `poetry run` | Apr 5 |

**Root cause of the contradiction:** `feedback_no_source_activate.md` was created
because the `source .venv/bin/activate &&` prefix broke `Bash(poetry *)` allow
rules in `settings.json`. But `settings.local.json` has since been updated with:
```
"Bash(source .venv/bin/activate && poetry:*)"
"Bash(source .venv/bin/activate && poetry run:*)"
```
So the permission issue is resolved — both patterns now match.

**User's decision:** Re-adopt venv activation for reproducibility and package
consistency ("works for you but doesn't work for me" problem). The reasoning:
- `poetry run` relies on Poetry's internal venv detection, which can break
  across machines if system Python differs
- `source .venv/bin/activate &&` explicitly sets `VIRTUAL_ENV` and puts
  `python3.12` first in PATH — deterministic regardless of system Python
- This also guards against any bare `python3` or `pip` invocation accidentally
  using system Python

**Resolution:** Delete `feedback_no_source_activate.md` (now stale). Update
`feedback_poetry_venv.md` with cleaner wording. Add it to the MEMORY.md index.
Update CLAUDE.md Critical Rules to match.

### Per-file assessment (post-resolution)

| File | Type | Action |
|------|------|--------|
| `user_senior_data_engineer.md` | user | Keep as-is |
| `feedback_version_tracking.md` | feedback | Keep as-is |
| `feedback_no_source_activate.md` | feedback | **DELETE** — superseded |
| `feedback_poetry_venv.md` | feedback | **UPDATE** and add to index |
| `feedback_context_manager_style.md` | feedback | Keep as-is |
| `feedback_plan_scope.md` | feedback | Keep as-is |
| `feedback_pr_body_file.md` | feedback | **UPDATE** — point to `.github/tmp/` |
| `feedback_pr_body_cleanup.md` | feedback | Keep as-is |
| `feedback_opusplan_setting.md` | feedback | Keep as-is |
| `feedback_git_commit_format.md` | feedback | **UPDATE** — `commit.txt` in `.github/tmp/` |
| `project_jupytext_location.md` | project | Keep as-is |

### Scientific/academic methodology risk
**NONE found.** All memories are engineering workflow. Scientific invariants,
thesis rules, and ML protocol live in `.claude/` proper — correct placement.

---

## 5. Proposed Changes (Execution Plan)

### Change A: CLAUDE.md — add "never work on master" to Critical Rules

Add after the existing NEVER rules:
```markdown
- **NEVER** make file changes while on master — always work on a feature branch
```

### Change B: CLAUDE.md — update poetry rule

Change:
```
- **ALWAYS** use `poetry run <command>` — NEVER bare `python3` or `pip install`
```
To:
```
- **ALWAYS** activate the venv first: `source .venv/bin/activate && poetry run <command>`
  — NEVER bare `python3` or `pip install`
```

### Change C: git-workflow.md — consolidate ephemeral files to .github/tmp/

Update the PR Body Format section to:
1. Use `.github/tmp/pr.txt` (already does — confirm)
2. Add note about always using absolute paths
3. Add `commit.txt` pattern alongside `pr.txt`

Updated bash example:
```bash
# Commit message — write via Write tool to .github/tmp/commit.txt
# Then user runs: git commit -F .github/tmp/commit.txt

# PR body — write via Write tool to .github/tmp/pr.txt
# Then: gh pr create --title "..." --body-file .github/tmp/pr.txt

# Clean up after PR is created
rm .github/tmp/pr.txt .github/tmp/commit.txt
```

### Change D: PreToolUse branch guard hook

New script `scripts/hooks/guard-master-branch.sh`:
```bash
#!/usr/bin/env bash
branch=$(git branch --show-current 2>/dev/null)
if [ "$branch" = "master" ] || [ "$branch" = "main" ]; then
  echo "BLOCKED: On $branch branch. Create a feature branch first." >&2
  exit 1
fi
```

Add to `settings.json` hooks → PreToolUse array (alongside existing guard-write-path):
```json
{
  "matcher": "Write|Edit",
  "hooks": [{
    "type": "command",
    "command": "./scripts/hooks/guard-master-branch.sh"
  }]
}
```

### Change E: Memory reconciliation

**E.1** — Delete `feedback_no_source_activate.md`

**E.2** — Rewrite `feedback_poetry_venv.md`:
```markdown
---
name: Activate venv before poetry commands
description: Always prefix poetry commands with 'source .venv/bin/activate &&' for reproducibility across machines
type: feedback
---

Always prefix poetry commands with `source .venv/bin/activate &&` in Bash:
```
source .venv/bin/activate && poetry run <command>
```

**Why:** Ensures deterministic Python resolution regardless of system Python
version. Bare `poetry run` can break on machines where system Python differs.
The `settings.local.json` already whitelists `Bash(source .venv/bin/activate && poetry:*)`.

**How to apply:** Every poetry command: `source .venv/bin/activate && poetry <cmd>`.
This is also reflected in CLAUDE.md Critical Rules.
```

**E.3** — Update `feedback_git_commit_format.md` — change path from
`temp/commit_msg.txt` to `.github/tmp/commit.txt`

**E.4** — Update `feedback_pr_body_file.md` — confirm `.github/tmp/pr.txt`
path (already correct), add note about absolute paths

**E.5** — Update MEMORY.md index:
- Change `feedback_no_source_activate` entry → `feedback_poetry_venv` with
  updated description

### Change F: settings.json — add venv-prefixed poetry commands to shared allow list

Add to `settings.json` permissions.allow:
```json
"Bash(source .venv/bin/activate && poetry *)"
```
This way the allow rule works without relying on settings.local.json.

---

## 6. Consistency Ripple from Change B (venv activation)

Validation found that switching from bare `poetry run` to
`source .venv/bin/activate && poetry run` requires updating 6 files for
consistency. **None of these are breaking** — bare `poetry run` still works —
but inconsistency between CLAUDE.md and agent/rule files would confuse agents.

| File | What to update |
|------|---------------|
| `CLAUDE.md` § Commands table | Prefix all 4 commands with `source .venv/bin/activate &&` |
| `.claude/rules/python-code.md` lines 9-11 | Prefix ruff/mypy/pytest commands |
| `.claude/rules/git-workflow.md` lines 17-19 | Prefix ruff/mypy/pytest commands |
| `.claude/agents/executor.md` lines 36,42,69,71 | Prefix all `poetry run` invocations |
| `.claude/agents/reviewer.md` lines 22-24,34,37 | Prefix all `poetry run` invocations |
| `scripts/hooks/lint-on-edit.sh` line 9 | Prefix `poetry run ruff check` |

**Risk assessment:** LOW. All changes are mechanical find-and-replace of
`poetry run` → `source .venv/bin/activate && poetry run`. No logic changes.
The `settings.local.json` already allows both patterns. Adding the shared
allow rule (Change F) ensures it works even without local overrides.

**Scientific invariants impact:** NONE. These are all tooling invocations,
not data/feature/model code.

---

## 7. What We're NOT Doing (and Why)

| Suggestion | Why skip |
|------------|----------|
| CHANGELOG duplication in CLAUDE.md | Already in git-workflow.md |
| Read-only planning duplication | Already strongest version in CLAUDE.md |
| "Read plan once, act immediately" | Fights user's Opus→specs→executor workflow |
| "Respond in chat not files" | User prefers markdown file preview |
| Custom /pr skill | Separate Category C chore — plan after this |
| Headless mode | User's CLI+subagent workflow is preferred |
| `git push origin <branch>:<branch>` | git push is denied — user runs manually |

---

## 8. Change G: README.md cleanup

The root `README.md` has two stale sections:

### G.1 — "Prior Drafts" section (lines 33-39)

Lists 3 specific files that **no longer exist** (deleted in v0.13.2 legacy cleanup):
- `src/rts_predict/sc2/reports/archive/ROADMAP_v1.md` — gone
- `src/rts_predict/sc2/reports/archive/methodology_v1.md` — gone
- `src/rts_predict/sc2/reports/archive/sanity_validation.md` — gone

The path `sc2/reports/archive/` itself doesn't exist — archives live at
`sc2/reports/sc2egset/archive/`. Replace the file-by-file table with directory
pointers to the actual archive locations:

```markdown
## Prior Work (reference only — not authoritative)

Superseded drafts and pre-restart artifacts are preserved in per-dataset
archive directories:

- `src/rts_predict/sc2/reports/sc2egset/archive/` — SC2EGSet prior exploration
- `src/rts_predict/aoe2/reports/aoe2companion/archive/` — AoE2 Companion prior work
- `src/rts_predict/aoe2/reports/aoestats/archive/` — AoE2 aoestats prior work

Each archive has a `_README.md` explaining what it contains and why it was
superseded.
```

### G.2 — "Project State" section (lines 41-47)

This is a point-in-time status snapshot that will immediately become stale.
The authoritative phase status trackers are:
- `docs/PHASES.md` (canonical phase list)
- `src/rts_predict/<game>/reports/<dataset>/PHASE_STATUS.yaml` (per-dataset status)

Replace with a pointer, not a snapshot:

```markdown
## Project Status

Phase progress is tracked per dataset in `PHASE_STATUS.yaml` files — see
`docs/PHASES.md` for the canonical phase list and `ARCHITECTURE.md` for
the full source-of-truth hierarchy.
```

### G.3 — "Quick Start" section (lines 14-18)

Update to match Change B (venv activation):

```markdown
## Quick Start
```bash
source .venv/bin/activate && poetry install
source .venv/bin/activate && poetry run sc2 --help
source .venv/bin/activate && poetry run pytest tests/ -v --cov=rts_predict
```
```

---

## 9. Verification

After execution:
1. `grep "NEVER.*master" CLAUDE.md` → should match the new rule
2. `grep "source .venv" CLAUDE.md` → should match updated poetry rule
3. `grep "absolute" .claude/rules/git-workflow.md` → should match
4. `grep "commit.txt" .claude/rules/git-workflow.md` → should match
5. `ls scripts/hooks/guard-master-branch.sh` → exists and executable
6. `jq '.hooks.PreToolUse | length' .claude/settings.json` → should be 2
7. `jq '.permissions.allow[] | select(contains("source .venv"))' .claude/settings.json` → should match
8. Memory dir: `feedback_no_source_activate.md` gone, `feedback_poetry_venv.md` updated, MEMORY.md index updated
9. Integration test: start new session on master → Write/Edit blocked by hook
10. `grep "PHASE_STATUS" README.md` → should match, no stale status snapshot
11. `grep "archive/" README.md` → should point to dirs, not specific files

---

## 10. Follow-up (separate session)

- Plan custom skills (`/pr`, `/execute-plan`) as Category C chore
- Consider whether `temp/` dir should be renamed to `specs/` for the
  Opus→specs→executor workflow (user mentioned this as a possibility)
