# Spec Mechanics Audit: Do Specs Actually Work?

**Date:** 2026-04-11
**Triggered by:** CLI transcript analysis showing executor T05 received a
60-line prompt that duplicated the spec content, making it impossible to
distinguish "executor followed the spec" from "executor followed the prompt."

---

## 1. What Context Does a Subagent Actually Receive?

### Evidence from transcript inspection

Examined subagent JSONL transcripts in
`~/.claude/projects/.../subagents/agent-*.jsonl`:

| Record | role | Content |
|--------|------|---------|
| 0 | user | The dispatch prompt (the `prompt` parameter from `Agent()`) |
| 1 | assistant | "Let me read the spec..." |
| 2+ | assistant | Tool calls (Read, Bash, etc.) and their results |

**No system role messages appear in transcripts.** The conversation contains
only `user` and `assistant` turns. However, this is inconclusive — system
prompts are typically sent as a separate API parameter and are NOT stored
in the conversation transcript format.

### What we know for certain

1. **The dispatch `prompt` is the first user message.** Confirmed by inspecting
   `agent-a00bb03d006d5fc14.jsonl` (executor T01):
   ```
   message.content: "Execute task T01 per spec planning/specs/spec_01_log_subagent.md..."
   ```

2. **The agent definition YAML frontmatter controls model + tools.** The
   `executor.md` frontmatter sets `model: sonnet`, `tools: [Read, Write, ...]`.
   These are consumed by Claude Code to configure the API call, not as
   conversation content.

3. **The agent definition body text** (the markdown after `---`) — its
   injection mechanism is **undocumented**. It may be injected as a system
   prompt (invisible in transcripts), or it may be reference documentation
   only. We cannot determine this from the transcript format.

4. **CLAUDE.md and .claude/rules/*.md** — same uncertainty. The main session
   sees these as `<system-reminder>` tags, but whether subagents inherit
   them is not determinable from transcripts.

### What the Claude Code Agent tool documentation says

From the system prompt:
> "A new Agent call starts a fresh agent with **no memory of prior runs**,
> so the prompt must be self-contained."

> "Brief the agent like a smart colleague who just walked into the room —
> it hasn't seen this conversation, doesn't know what you've tried"

This strongly implies the prompt is the primary (possibly sole) input for
task-specific context. The agent definition body and CLAUDE.md may provide
general project rules, but the task itself must come from the prompt.

---

## 2. The Duplication Problem (Claude Chat's Analysis)

### What happened with T05 (session_audit.py)

The orchestrator dispatched T05 with this structure:

```
Agent({
  subagent_type: "executor",
  prompt: "Execute task T05... Read the spec at planning/specs/spec_05_dashboard.md first.
  
  ## Context
  [60 lines of normative content duplicating the spec:
   - JSONL parsing details
   - Agent log format
   - CLI interface
   - 7 sections to generate
   - Error handling rules
   - Dependencies constraint]"
})
```

The executor then:
1. Read the spec (1 tool call)
2. Proceeded with empirical discovery (10+ tool calls against the environment)
3. Wrote the script

### The problem

The spec was read once but the prompt already contained everything. There is
no way to determine from the transcript whether the executor:
- (a) Followed the spec content it read, or
- (b) Followed the prompt content it was given, or
- (c) Merged both (prompt wins on conflicts since it's the first user message)

### Contrast with T01 (log-subagent.sh)

The T01 dispatch was a pointer-style prompt:
```
"Execute task T01 per spec planning/specs/spec_01_log_subagent.md.
 Read the spec first, then read scripts/hooks/log-subagent.sh and
 make the changes.
 
 Key changes:
 1. Replace line 4...
 2. Replace the 3 scattered state file paths...
 3. Add PROJECT=...
 4. Append project=$PROJECT..."
```

This is better than T05 — it references the spec AND provides key changes,
but the key changes are a summary, not a duplication. The spec remains the
detailed source. However, even here the prompt carries enough to execute
without the spec.

---

## 3. Are Specs Load-Bearing or Ceremonial?

### Load-bearing (specs serve a real purpose)

1. **Persistence across sessions.** If a session crashes mid-execution,
   the next session can pick up from the spec. The dispatch prompt is
   ephemeral — it lives only in the orchestrator's conversation context.

2. **Review gate evidence.** When a reviewer checks "did the executor do
   what it was supposed to?" it reads the spec, not the prompt. The spec
   is the reviewable contract.

3. **Audit trail.** The spec is committed to git. The dispatch prompt is
   not. Post-hoc, you can determine what the executor was told to do by
   reading the spec, even months later.

4. **Multi-executor consistency.** When 7 executors run in parallel (like
   PR #108's Wave 2), each reads its own spec. Without specs, you'd need
   7 separate prompts with no shared format, no reviewable contract.

5. **Scope control.** The spec's `file_scope` and `read_scope` define
   boundaries. An executor that goes outside its scope can be flagged.

### Ceremonial (specs don't add marginal value during execution)

1. **Same-session execution.** When the orchestrator dispatches and the
   executor completes within one session, the prompt carries everything.
   The spec read is confirmation, not discovery.

2. **Prompt duplication makes the spec redundant for that run.** If the
   prompt contains the spec's content verbatim, the spec read is a no-op
   from the executor's perspective.

3. **No enforcement mechanism.** Nothing prevents the executor from ignoring
   the spec and following only the prompt. No post-execution check compares
   "what the spec said" vs "what the executor actually did."

### Verdict: specs are load-bearing for the SYSTEM, not for any single RUN

A spec's value is upstream (planning) and downstream (review, audit, re-execution),
not at the moment of execution. During execution, the prompt dominates. This is
not a bug — it's how agent dispatch works. The fix is to change the prompt
pattern, not to remove specs.

---

## 4. The Real Fix: Pointer Prompts, Not Restatement Prompts

### Current anti-pattern (T05 style)

```python
Agent({
  prompt: """Execute task T05.
  Read the spec at planning/specs/spec_05.md.
  
  [60 lines duplicating the spec content]"""
})
```

**Problem:** The spec is redundant for this run. The executor can't tell
which source to trust. If spec and prompt disagree, the prompt wins silently.

### Recommended pattern

```python
Agent({
  prompt: """You are executing task T05.
  
  Your spec is at: planning/specs/spec_05_dashboard.md
  
  Read the spec FIRST. It is your contract. Execute exactly what it says.
  Do not infer requirements from this message — the spec is the sole
  source of truth for this task.
  
  After reading the spec, confirm: spec path, task_id, file_scope, and
  the number of verification checks you will run."""
})
```

**Why this works:**
- The prompt is a pointer, not a restatement
- The executor must read the spec to know what to do
- The "confirm" step creates a checkable trace: did the executor report
  the correct spec fields?
- If the spec is missing or corrupt, the executor will report it instead
  of proceeding from a stale prompt

### Even better: echo-then-execute

Add to the executor agent definition (`.claude/agents/executor.md`):

```markdown
## Spec-first protocol
When dispatched with a spec_file reference:
1. Read the spec file
2. Report: task_id, file_scope, verification count
3. Only then begin execution
If the spec file does not exist or is empty, STOP and report the error.
```

This makes spec usage auditable from the transcript.

---

## 5. What Cannot Be Determined (Honest Unknowns)

| Question | Answer |
|----------|--------|
| Does the executor see CLAUDE.md? | **Unknown.** Transcripts don't capture system prompts. |
| Does the executor see .claude/agents/executor.md body text? | **Unknown.** Same limitation. |
| Does the executor see .claude/rules/*.md? | **Unknown.** Same limitation. |
| Which wins if spec and prompt disagree? | **The prompt, probably.** It's the first user message. The spec is a Read result in a later turn — earlier context has priority in attention. |
| Can we verify spec adherence post-hoc? | **Partially.** Compare spec's verification section against the executor's reported results. But this is manual. |

### How to resolve these unknowns

1. **Test with a canary.** Dispatch an executor with a prompt that says
   "do X" and a spec that says "do Y" (where X and Y are observably
   different). See which one the executor does. This is the only way to
   empirically determine priority.

2. **Add a system prompt probe.** Dispatch an executor with: "Before doing
   anything, report: (a) do you see any system-level rules? (b) what is
   the first line of your system prompt? (c) do you have CLAUDE.md content
   in your context?" This would reveal what the executor actually sees.

---

## 6. Recommendations

### Immediate (this PR or next)

1. **Update `.claude/agents/executor.md`** — add a "Spec-first protocol"
   section requiring the executor to echo spec metadata before executing.

2. **Update `/materialize_plan` or the orchestrator dispatch pattern** —
   dispatch prompts should be pointers with at most a 1-2 line summary,
   not full spec restatements. The CLAUDE.md or orchestrator instructions
   should say: "When dispatching an executor to a spec, the prompt MUST
   reference the spec_file path and MUST NOT duplicate spec content."

3. **Update `planning/specs/README.md`** — document that specs are the
   contract for review and audit, not just an input to the executor.

### Future (enforcement)

4. **Post-execution spec-vs-output check.** The reviewer agent should
   compare the spec's verification section against the executor's actual
   results. This is already partially happening (reviewers check gate
   conditions) but should be made explicit.

5. **Canary test.** Run the conflict test described in section 5 to
   empirically determine spec vs prompt priority.

---

## 7. Answer to the Core Questions

**"Is the executor's context derived from the spec?"**

Partially. The executor reads the spec as a tool call, but the dispatch
prompt is the dominant context. When the prompt duplicates the spec, the
spec read is confirmation, not the source of truth.

**"Are specs redundant?"**

No — they are load-bearing for review, audit, persistence, and
re-execution. They are partially redundant at the moment of execution
when the prompt duplicates their content. The fix is to stop duplicating.

**"Where does the subagent get its context from?"**

From (in likely priority order):
1. The dispatch prompt (first user message — certain)
2. Possibly CLAUDE.md / agent definition / rules (as system prompt — unknown)
3. Tool call results, including the spec Read (later turns — certain but lower priority)

**"Claude Chat's concerns are valid?"**

Yes. The transcript evidence supports their analysis. The prompt-spec
duplication pattern makes spec adherence unfalsifiable. The recommended
fix (pointer prompts + echo protocol) addresses this directly.

---

*Audited from subagent transcripts in ~/.claude/projects/.../*.jsonl,
executor agent definition, and CLI output analysis.*

---

## 8. Follow-Up: Resolving the Unknowns (2026-04-12)

**Source:** Claude Code official documentation (code.claude.com), specifically:
- [Subagents in the SDK](https://code.claude.com/docs/en/agent-sdk/subagents.md) — "What subagents inherit" table
- [How the agent loop works](https://code.claude.com/docs/en/agent-sdk/agent-loop.md) — context window section
- [Use Claude Code features in the SDK](https://code.claude.com/docs/en/agent-sdk/claude-code-features.md) — settingSources behavior

### The "Unknown" answers from Section 5 are now resolved

| Question | Section 5 said | Docs say |
|----------|---------------|----------|
| Does executor see CLAUDE.md? | Unknown | **Yes** — inherited via `settingSources: ["project"]` |
| Does executor see `.claude/agents/executor.md` body? | Unknown | **Yes** — injected as the subagent's **system prompt** |
| Does executor see `.claude/rules/*.md`? | Unknown | **Yes** — inherited alongside CLAUDE.md |

In Claude Code CLI, subagents defined in `.claude/agents/` automatically inherit
project context because the session is already configured with setting sources.

### What subagents inherit (from official docs)

| The subagent receives | The subagent does NOT receive |
|----------------------|------------------------------|
| Its own system prompt (`executor.md` body) | Parent's conversation history or tool results |
| The Agent tool's `prompt` string (as first user message) | The parent's system prompt |
| Project CLAUDE.md (loaded via `settingSources`) | Skills (unless listed in agent definition) |
| `.claude/rules/*.md` files | |
| Tool definitions (inherited from parent, or filtered by `tools` field) | |

### The three layers of executor context

1. **System prompt** = `executor.md` body + CLAUDE.md + rules (always present, invisible in transcripts)
2. **First user message** = the dispatch prompt from `Agent({ prompt: "..." })`
3. **Tool results** = whatever the executor reads (the spec file, source files, etc.)

This means specs compete with whatever the orchestrator puts in the dispatch
prompt — not with a vacuum. If the prompt is a pointer, the spec wins for
task-specific content. If the prompt duplicates the spec, the prompt wins
(earlier in the conversation = higher attention priority).

### "No memory" means no conversation history, not no CLAUDE.md

The Agent tool docs say: "A new Agent call starts a fresh agent with no memory
of prior runs, so the prompt must be self-contained."

**"No memory" refers only to conversation history.** CLAUDE.md is not "memory"
in the conversation sense — it's persistent project context that loads fresh
in every agent/subagent at startup.

---

## 9. The Key Insight: "Execute the Plan" vs "Execute the DAG"

### The framing matters enormously

**"Execute the plan"** → the orchestrator reads `current_plan.md`, which has
all the details (objectives, instructions, verification steps). It naturally
wants to restate that content in the dispatch prompt. This is how T05 ended
up with 60 lines of duplicated spec content.

**"Execute the DAG"** → the orchestrator reads `DAG.yaml`, which contains only:
- `task_id`, `spec_file` path, `agent`, `depends_on`, `file_scope`
- No objectives, no instructions, no verification steps

The DAG is structurally incapable of carrying spec content. If the orchestrator
only reads the DAG, it **can only** dispatch pointers — there's nothing to
duplicate.

### Conclusion: "execute the plan" should become "execute the DAG"

The DAG is the execution contract. The plan is the human-readable intent that
was already consumed during materialization. The DAG's structure enforces
pointer-style dispatch naturally — no rule needed to prevent duplication,
because there's nothing to duplicate.

---

## 10. Canary Test Design

### Purpose

Empirically verify that executors follow spec content (not the dispatch prompt)
when dispatched with pointer-style prompts via the DAG.

### Setup (done before the test session)

1. Pick 2-3 existing specs (e.g., spec_01, spec_02)
2. Replace their content with trivially verifiable canary instructions:
   - spec_01: "Create file `canary/01.txt` containing exactly: `SPEC_01_CANARY_ALPHA`"
   - spec_02: "Create file `canary/02.txt` containing exactly: `SPEC_02_CANARY_BETA`"
3. Don't touch `DAG.yaml` — it already points to those spec files
4. Commit so the fresh session sees it

### Test (new session)

Tell the session: "Execute the DAG at `planning/dags/DAG.yaml`."

Optionally add: "Read the DAG, dispatch executors per task groups. Do NOT read
the specs yourself — pass only the spec_file path to each executor."

Or even simpler: just "Execute the DAG" and see if CLAUDE.md's rules are
sufficient without the extra instruction.

### What to check

1. **Did the orchestrator read the specs before dispatching?** If yes, the
   pointer rule isn't working — the orchestrator is pulling content into its
   context and may restate it.
2. **Did the executor create the canary files?** If yes, specs are load-bearing
   at execution time.
3. **Does the canary file content match the spec?** If yes, the executor
   followed the spec, not the prompt.

### Stronger variant (conflict test)

Have the dispatch prompt say "write PROMPT_WINS" and the spec say "write
SPEC_WINS." This requires manually crafting the dispatch prompt, which is
hard in Claude Code — but possible if the user writes a custom Agent() call
in the instructions.

---

## 11. Recommended Changes

### 1. CLAUDE.md — Execution section (governs the orchestrator)

Add after "agents read their assigned spec file, not the full plan":

```
When dispatching an executor, the prompt MUST be a pointer: spec_file path
+ at most a 1-2 line context summary. MUST NOT restate spec content.
The orchestrator reads DAG.yaml for task structure — not specs, not the plan.
```

### 2. `.claude/agents/executor.md` (governs the executor)

Add a spec-first protocol section:

```markdown
## Spec-first protocol
When dispatched with a spec_file reference:
1. Read the spec file FIRST
2. Echo: task_id, file_scope, verification count
3. Only then begin execution
If the spec file does not exist or is empty, STOP and report the error.
```

### 3. Delete `spec_mechanics_audit.md` after changes are applied

This document served its purpose as an investigation artifact. Once the rules
are encoded in CLAUDE.md and executor.md, the audit is superseded. The three
"Unknown" answers in Section 5 are now known to be wrong and could mislead
future sessions if left in place — but Sections 8-11 correct them.

---

## 12. Priority Order

1. **Add both rules now** — they're tiny and directly relevant to any plan
   execution work
2. **Run the canary test** after the rules are in place — replace 2 specs,
   fresh session, "execute the DAG"
3. **Archive or delete this file** after canary test confirms the fix works

---

*Follow-up research conducted 2026-04-12 using Claude Code official documentation
and project codebase analysis.*

---

## 13. Canary Test Results (2026-04-12)

### Baseline runs (before fixes)

Two baseline tests were run before adding the dispatch rules. Both failed
identically:

**Run 1:** User said "execute the @planning/dags/DAG.yaml" (fresh session).
- Orchestrator read DAG.yaml ✓
- Orchestrator immediately read `current_plan.md` ✗ (violates pointer rule)
- Orchestrator noticed DAG was "stale" (branch mismatch) and invoked
  `/materialize_plan` autonomously
- Orchestrator deleted all existing specs (`rm -f planning/specs/spec_*.md`)
- User stopped the session before any executors were dispatched

**Run 2:** Same prompt, new session (after adding the NEVER rule to Critical
Rules, but before fixing the stale DAG).
- Same behavior: orchestrator read DAG, then `current_plan.md`
- Orchestrator concluded DAG was stale and began re-materialization
- The NEVER rule did not hold because the DAG's `branch:` field didn't match
  the current branch — the orchestrator treated the inconsistency as
  justification to override the rule

**Root cause:** The DAG was genuinely stale (from a previous merged PR). The
orchestrator reasonably concluded it needed the plan to understand the current
state. The NEVER rule was insufficient when the DAG appeared broken.

### Fix: proper canary setup

Created a consistent canary DAG + 2 spec files:

- `DAG.yaml`: `dag_id: dag_canary_test`, `branch: chore/plan-template-rewrite`
  (matches current branch), 1 task group with 2 parallel tasks
- `spec_01_canary_alpha.md`: "Create `canary/01.txt` with `SPEC_01_CANARY_ALPHA_7f3a`"
- `spec_02_canary_beta.md`: "Create `canary/02.txt` with `SPEC_02_CANARY_BETA_9d1e`"

The canary strings contain random suffixes to ensure the executor can only
produce them by reading the spec.

The user additionally modified spec_01's `file_scope` to `canary/123456.txt`
(deliberately mismatching the DAG's `canary/01.txt`) to test spec-vs-DAG
priority.

### Canary test (with fixes in place)

User said: "execute the @planning/dags/DAG.yaml" (fresh session).

**Orchestrator behavior:**
- Read DAG.yaml ✓
- Did NOT read `current_plan.md` ✓ (NEVER rule held)
- Did NOT read any spec files ✓ (pointer dispatch worked)
- Dispatched T01 and T02 in parallel with pointer prompts ✓

**Executor behavior:**
- T01: 5 tool calls, 12.5k tokens — created `canary/123456.txt` (the spec's
  filename, not the DAG's `canary/01.txt`) ✓
- T02: 4 tool calls, 12.3k tokens — created `canary/02.txt` ✓
- Both executors followed their specs as the sole source of truth ✓

**Reviewer behavior:**
- Caught the DAG/spec drift on T01 (DAG says `canary/01.txt`, spec says
  `canary/123456.txt`, executor created `canary/123456.txt`) ✓
- Caught spec internal inconsistency (Instructions say 123456, Verification
  still says 01.txt) ✓
- Flagged both as blockers ✓
- T02 passed clean ✓

### Conclusions from canary test

1. **Specs are load-bearing at execution time.** The executor created files
   with content that could only come from reading the spec (random suffixes).

2. **Pointer dispatch works.** The orchestrator read only DAG.yaml and passed
   spec_file paths — no content duplication.

3. **Spec beats DAG on conflict.** When spec and DAG disagreed on the filename,
   the executor followed the spec. This is correct: the spec is the contract,
   the DAG is the routing structure.

4. **Review gates catch drift.** The reviewer detected the DAG/spec
   inconsistency and flagged it as a blocker.

5. **The echo protocol worked.** Executors reported what they did, making
   the decision auditable.

6. **The NEVER rule requires a consistent DAG.** When the DAG appears broken
   (branch mismatch, missing specs), the orchestrator will override the rule.
   The fix was not a stronger rule — it was a consistent test setup.

### Priority of context during execution (empirically confirmed)

1. **Spec content** (read via tool call) — the executor's contract
2. **DAG metadata** (file_scope, depends_on) — routing, not content
3. **Dispatch prompt** — pointer only, no task-specific content

---

## 14. Review Agent Access During DAG Execution

### The scoping problem

The Critical Rules NEVER line says the orchestrator must not read specs or
the plan. But the final reviewer-deep NEEDS to read both for plan-vs-reality
alignment and spec compliance checking. Since reviewer-deep inherits CLAUDE.md,
the NEVER rule could conflict with its review mandate.

### Resolution: scope the rule to executor dispatch

The NEVER rule was refined to: "NEVER read `current_plan.md` or spec files
**when dispatching executors**" — not "during DAG execution" broadly.

Three distinct dispatch patterns now exist:

| Agent type | What the orchestrator passes | What the agent reads |
|-----------|------------------------------|---------------------|
| **Executor** | `spec_file` path only (pointer) | The spec file (via tool call) |
| **Reviewer** (per-TG gate) | Diff scope | The diff only |
| **Reviewer-deep** (final) | `plan_ref` path + all `spec_file` paths + `base_ref` | Plan, all specs, full diff |

The orchestrator constructs all three dispatch prompts from DAG metadata alone —
it never reads the plan or specs itself. The reviewer-deep reads them as part
of its review.

---

*Canary test conducted 2026-04-12. Rules updated in CLAUDE.md and executor.md.*
