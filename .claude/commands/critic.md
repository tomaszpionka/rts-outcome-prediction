# Continuous-Critic Workflow

Dispatch 4 parallel adversarial critics on a single file, merge findings,
apply a user-approved subset of revisions via a writer agent, and re-run
until no BLOCKERs remain or 3 iterations are exhausted.

## Arguments

Expected: a single file path.

`$ARGUMENTS` → treat as the **target file** to critique. If empty, STOP and
ask the user for a path.

## Pre-flight

1. Run `git branch --show-current`. If on `master` or `main`, STOP and tell
   the user to create a feature branch first (per Git & Branch Hygiene).
2. Verify `$ARGUMENTS` exists via `Read` (1 line). If missing, STOP with
   "Target file not found: $ARGUMENTS".
3. Ensure `.github/tmp/` exists — if not, run `mkdir -p .github/tmp`.
4. **Hash the target.** Run `shasum -a 256 "$ARGUMENTS" | awk '{print $1}' > .github/tmp/critic_hash.txt`.
   This pins the target state so later iterations can detect external swaps.
5. Announce: "Starting /critic on `$ARGUMENTS`. Max 3 iterations. You will
   be prompted before any writer dispatch."

## Loop (iterations 1–3)

Let `N` = current iteration (1, 2, or 3).

### Step A — Hash guard + dispatch 4 critics in parallel

**Before dispatching critics**, verify the target has not been swapped externally:

1. Read stored hash from `.github/tmp/critic_hash.txt`.
2. Compute current hash: `shasum -a 256 "$ARGUMENTS" | awk '{print $1}'`.
3. If hashes differ, **HALT the loop** with this message:
   > Target file `$ARGUMENTS` changed externally between iterations (hash
   > mismatch). Loop aborted. Applied revisions from prior iteration(s)
   > may still be valid — commit or revert them manually, then re-run
   > `/critic $ARGUMENTS` once the target is stable.

   Go directly to Cleanup. Do NOT dispatch critics.
4. If hashes match, proceed.

Then, in a **single message**, make 4 Agent tool calls:

1. `subagent_type: critic-empirical`
2. `subagent_type: critic-logical`
3. `subagent_type: critic-scope`
4. `subagent_type: critic-structural`

Each critic prompt must include:
- Target file path: `$ARGUMENTS`
- Output file path: `.github/tmp/critic_<critic>_<N>.md`
- Iteration number: `N`
- Context: "You are iteration N of max 3. Prior iterations' revisions
  are applied to the target. If N > 1, prior-iteration findings are in
  `.github/tmp/critic_merged_<N-1>.md` — read it to avoid re-flagging
  resolved items."

Critics emit their findings in chat (per their definitions) because their
`Write` tool is disabled. After all 4 return, **YOU** (the command
orchestrator) persist each critic's output to its designated
`.github/tmp/critic_<critic>_<N>.md` file via the `Write` tool.

### Step B — Dispatch merger

Single Agent call:
- `subagent_type: critic-merger`
- Prompt includes: target path, 4 critic output paths, output path
  `.github/tmp/critic_merged_<N>.md`, iteration `N`.

Merger's `Write` tool is authorized — it writes the merged file directly.

### Step C — Present merged plan to user

- Read `.github/tmp/critic_merged_<N>.md` (full contents).
- Echo the **Verdict**, **Revision list**, and **Subset selection prompt**
  to the user in chat.
- STOP. Wait for user reply. Do NOT dispatch the writer yet.

User reply options (per merger's subset-selection prompt):
- `apply recommended` — dispatch writer with RECOMMENDED items only.
- `apply all` — dispatch writer with RECOMMENDED + OPTIONAL items.
- `apply R1,R3,R5` — dispatch writer with the named revision IDs.
- `defer all` — skip this iteration. Go to cleanup.

### Step D — Dispatch writer on approved subset

Choose writer by target path:
- `thesis/...` → `subagent_type: writer-thesis`
- anything else → `subagent_type: executor`

Single Agent call. Prompt includes:
- Target file: `$ARGUMENTS`
- Merged revision file: `.github/tmp/critic_merged_<N>.md`
- Approved revision IDs (verbatim from user reply)
- Instruction: "Apply ONLY the approved revisions. Do not modify other
  parts of the file. Do not introduce new scope. Each revision's
  `Proposed fix` is advisory — use your judgment on the exact edit, but
  stay within the named target location."

Writer makes the edits directly. You do NOT re-verify them here — the
next iteration's critics will.

**Update the hash guard** — after the writer returns, re-hash the target
and overwrite the stored hash so iteration N+1's Step A compares against
the post-writer state:
`shasum -a 256 "$ARGUMENTS" | awk '{print $1}' > .github/tmp/critic_hash.txt`

### Step E — Loop decision

Read the merger's `Loop decision` field:
- `CONTINUE` AND `N < 3` → increment `N`, go back to Step A.
- `CLEAN` OR `N == 3` → exit loop, go to Cleanup.

Also exit immediately if user replied `defer all` in Step C.

## Cleanup

1. Report to user:
   - Final iteration count.
   - BLOCKERs remaining (if any) from the last merged file.
   - List of revision IDs applied across all iterations.
2. Delete temp files:
   ```
   rm -f .github/tmp/critic_empirical_*.md \
         .github/tmp/critic_logical_*.md \
         .github/tmp/critic_scope_*.md \
         .github/tmp/critic_structural_*.md \
         .github/tmp/critic_merged_*.md \
         .github/tmp/critic_hash.txt
   ```
3. If any BLOCKER remains after iteration 3, recommend the user either:
   - Open a follow-up PR for the remaining items.
   - Re-run `/critic $ARGUMENTS` after manual intervention.

## Rules

- NEVER dispatch the writer without explicit user approval of the subset.
- NEVER skip the merger step — the 4 raw critic outputs are NOT a
  patch-ready plan.
- NEVER run more than 3 iterations.
- If any critic returns empty or errors, retry once. Second failure →
  STOP and report which critic failed; do not proceed to merger with
  partial input.
- Per-iteration temp files are OK to accumulate; cleanup happens at the
  end of the full loop.
- If the target file is itself under `.github/tmp/` or
  `planning/current_plan.md` during an active `/loop`, confirm with the
  user first — these are ephemeral artifacts and may not benefit from
  continuous critique.
