# Agent Audit: planner-science and executor

Date: 2026-04-10

---

## Scope: planner-science

### 1. Invariant count mismatch [BLOCKER]

**File:** `.claude/agents/planner-science.md`, line 31
**Text:** "Evaluate scientific methodology against the 10 invariants"
**Fact:** `.claude/scientific-invariants.md` defines exactly **8 invariants**, numbered 1 through 8, grouped under 5 headings: Identity and splitting (#1, #2), Temporal discipline (#3, #4), Symmetric player treatment (#5), Reproducibility and rigour (#6, #7), Cross-game comparability (#8).

This is not a cosmetic error. The planner-science agent is told there are 10 invariants, so it may hallucinate 2 additional invariants to "evaluate against," or it may stop at 8 and conclude it has missed 2 it cannot find, wasting reasoning budget searching for phantom constraints. Either way, the canonical reference and the agent prompt disagree on the fundamental count of the governing rules the agent exists to enforce.

**Severity: BLOCKER.** An agent whose mission is invariant enforcement must have the correct invariant count.

---

### 2. Data layout section is SC2-only [WARNING]

**File:** `.claude/agents/planner-science.md`, lines 58–63
**Text:** "All data lives under `src/rts_predict/sc2/data/sc2egset/`"

The thesis covers both SC2 and AoE2. Three datasets are active (sc2egset, aoe2companion, aoestats) and all three PHASE_STATUS files show Phase 01 `in_progress`. The planner-science agent — whose explicit role includes "Maintain cross-game comparability (SC2 ↔ AoE2)" — has a data layout section that mentions only SC2. An AoE2 planning session will find no data layout guidance in its own prompt.

AoE2 data exists at `src/rts_predict/aoe2/data/aoe2companion/` and `src/rts_predict/aoe2/data/aoestats/`, with a fully populated `config.py` defining all paths. The layout differs materially from SC2 (daily parquets vs. tournament-organized replay JSONs; paired directories for matches+players; CSV ratings files alongside parquet).

**Risk:** Planner-science may propose SC2-shaped ingestion plans for AoE2 data (e.g., assuming tournament directories or `.SC2Replay.json` structure).

---

### 3. Missing `ml-protocol.md` from read-first list [WARNING]

**File:** `.claude/agents/planner-science.md`, lines 49–56 (Read first section)

The read-first list includes scientific-invariants.md, INDEX.md, PHASE_STATUS, ROADMAP, INVARIANTS.md, and research_log.md. It does not include `.claude/ml-protocol.md`, which CLAUDE.md lists as a key file and which contains critical Phase 04+ rules including: the three leakage failure modes to test explicitly, the per-player leave-last-tournament-out split strategy, fixed seed convention, and the "veterans only" reporting requirement.

The reviewer-adversarial agent does list ml-protocol.md in its required reading, but the adversarial reviewer challenges plans after they are made — the planner should have the constraints before it.

**Risk:** Currently Phase 01 is active, so not immediately dangerous. When Phase 04 planning begins, planner-science will design ML experiments without the experiment protocol in its mandatory reading, and reviewer-adversarial will catch deviations after the fact — an avoidable waste of two Opus invocations.

---

### 4. No guidance on multi-dataset planning coordination [WARNING]

**File:** `.claude/agents/planner-science.md`, full prompt

The prompt says "Plan Phase work using the methodology defined in docs/INDEX.md, scoped to the active dataset indicated by PHASE_STATUS.yaml." But there are three active datasets, all at Phase 01 `in_progress`. The prompt does not address:

- How the agent determines which dataset it is planning for when invoked
- Whether it should check all three PHASE_STATUS files or just one
- How to handle cross-dataset coordination (e.g., ensuring parallel Phase 01 steps produce comparable outputs)

The PHASES.md file states "Two datasets under the same game are treated as independent entities" and that cross-dataset coordination "is tracked in reports/research_log.md and the thesis chapters, not in any ROADMAP." But planner-science has no instruction to verify that a plan for one dataset does not silently diverge from the methodology used on another dataset at the same phase.

---

### 5. `permissionMode: plan` correctly reinforced [NOTE]

The prompt says "READ-ONLY. Do NOT use Write or Edit" (line 38) and "Do NOT write _current_plan.md" (line 39). The frontmatter sets `permissionMode: plan`. The tool list includes Read, Grep, Glob, Bash, TodoWrite — no Write or Edit. This is consistent. The `Bash` tool is not explicitly restricted to read-only in the prompt, though `permissionMode: plan` enforces this at the infrastructure level.

No flaw identified.

---

### 6. Category A plan requirements are adequate but missing invariant documentation requirement [NOTE]

The required elements for Category A plans (phase/step ref, branch, files, function signatures, SQL queries, test cases, gate condition, sandbox notebook path, artifact target) are comprehensive. One gap: the plan requirements do not explicitly require specifying **which scientific invariants are applied and how**, though the ROADMAP step template includes a `scientific_invariants_applied` section. The planner-science prompt says "Always check scientific-invariants.md before proposing design decisions" but does not mandate that the plan output documents which invariants are relevant to each step.

---

### 7. No instruction to verify prior Phase gates before planning new Phases [NOTE]

The prompt says "Always reference the specific Phase/Step from the active dataset's ROADMAP.md" but does not instruct the agent to verify that prerequisite Phase gates have been met before planning a new Phase. CLAUDE.md says "NEVER begin a new phase until all prior phase artifacts exist on disk" — this rule is in CLAUDE.md but not in the planner-science prompt itself.

---

## Scope: executor

### 1. Model tier mismatch for scientific work [WARNING]

**File:** `.claude/agents/executor.md`, frontmatter: `model: sonnet`

The executor runs on Sonnet by default and is responsible for Category A Phase work including temporal leakage prevention and Category F thesis chapters. The reviewer agent explicitly acknowledges that "Sonnet may miss edge cases" for temporal reasoning, flagging for Pass 2 Opus review. But the executor's own prompt has no equivalent self-awareness instruction — it simply says "Ensure temporal discipline" as if that is a trivial mechanical check for Sonnet.

**Risk:** The executor should at minimum instruct itself to flag temporally complex steps (window functions, rolling aggregates, rating systems) to the user as candidates for `/model opus` switch.

---

### 2. Category A temporal discipline instruction is superficial [WARNING]

**File:** `.claude/agents/executor.md`, lines 65–66
**Text:** "Ensure temporal discipline (features at T use only data < T)"

This is the entirety of temporal discipline guidance for the agent that writes all the code. The ml-protocol.md enumerates three specific leakage failure modes:
1. Rolling aggregates computed using the target game's own value
2. Head-to-head win rates that include the target game
3. Within-tournament features that include the target game's position

The executor prompt distills all of this into a single parenthetical. It does not:
- Enumerate the specific leakage failure modes
- Instruct the agent to write temporal leakage tests
- Reference ml-protocol.md at all (grep confirms zero matches)
- Specify strict less-than (`match_time < T`), not less-than-or-equal (`match_time <= T`) — scientific-invariants.md is explicit on this

**Risk:** When Phase 02 begins, the executor may implement `<=` instead of `<`, or forget to exclude the current row from rolling aggregates. The reviewer running on Sonnet has the same limitation.

---

### 3. Notebook workflow step 1 references nonexistent template location [WARNING]

**File:** `.claude/agents/executor.md`, line 74
**Text:** "Use the template from `_current_plan.md` B.3."

This reference assumes `_current_plan.md` always contains a notebook template at section B.3, but `_current_plan.md` is overwritten for each new plan. The current `_current_plan.md` is a Category C chore with no B.3 section. If the executor is invoked for notebook work when a non-Category-A plan is active, this instruction points to nothing.

**Fix:** The notebook template should live in a stable location (e.g., `sandbox/README.md` or `docs/templates/`) rather than being referenced from a volatile file.

---

### 4. Category F boundary with writer-thesis is contradictory [WARNING]

**File:** `.claude/agents/executor.md`, lines 68–69

The executor has full Category F instructions (Critical Review Checklist, WRITING_STATUS.md updates). But the decision flowchart in AGENT_MANUAL routes thesis writing to `@writer-thesis`, while Workflow B routes it to `@executor`. Both agents have the capability; neither prompt clearly cedes ownership to the other.

**Critical gap:** The `writer-thesis` agent has a "HALT if evidence is insufficient" guardrail — it refuses to write prose that the artifacts don't support. The executor's Category F instructions lack this safeguard. An executor running on Sonnet with no HALT-on-unsupported-claims constraint may generate thesis prose with under-evidenced claims.

---

### 5. diff-cover command missing `--fail-under` flag [NOTE]

**File:** `.claude/agents/executor.md`, lines 56–57
**Text:** `poetry run diff-cover coverage.xml` (without `--fail-under=90`)

The reviewer agent uses `--fail-under=90` to get an unambiguous exit code. The executor relies on parsing the percentage from prose output, which is more error-prone for a Sonnet model.

---

### 6. Parallel execution rules do not prohibit writes to shared state [NOTE]

**File:** `.claude/agents/executor.md`, lines 39–48

The parallel execution rules prohibit git operations but do not prohibit concurrent writes to shared files:
- `reports/research_log.md` (which the executor updates after each step)
- `_current_plan.md` (no explicit write prohibition in parallel rules)
- Report artifacts in `reports/<dataset>/artifacts/`

The "conflict risk" reporting instruction (line 45) is reactive, not preventive. The parent's discipline (CLAUDE.md "Parallel Executor Orchestration") is the only guard. Defense-in-depth would have the executor's prompt explicitly prohibit writing to shared state files when in parallel mode.

---

### 7. No instruction to read per-dataset INVARIANTS.md [NOTE]

**File:** `.claude/agents/executor.md`, lines 98–100

The executor's read-first list is only `_current_plan.md` and PHASE_STATUS.yaml. Planner-science's read-first list includes the active dataset's INVARIANTS.md. Per-dataset invariants contain empirical findings from Phase 01 (field availability, derived constants, observed distributions) that the executor needs when implementing Phase 02+ code. If the plan is vague on a dataset-specific constraint, the executor has no prompt-level instruction to consult INVARIANTS.md.

---

### 8. Data layout section is SC2-only [WARNING]

**File:** `.claude/agents/executor.md`, lines 102–106
**Text:** "All data under `src/rts_predict/sc2/data/sc2egset/`"

Same issue as planner-science finding #2. Additionally, the executor's data layout section omits `staging/` and `tmp/` directories that the planner-science version includes — the executor implements code against these paths but its prompt doesn't mention them. The executor also references `config.py via DATASET_DIR`, which is the SC2 variable name; the AoE2 config uses different variable names (`AOE2COMPANION_DIR`, `AOESTATS_DIR`).

---

### 9. 90% diff-coverage threshold undocumented against 95% overall gate [NOTE]

**File:** `.claude/agents/executor.md`, line 57

The executor uses a 90% diff-coverage threshold. The pyproject.toml sets `fail_under = 95` for overall coverage. These thresholds measure different things and are not in conflict, but the relationship is undocumented, which could confuse the agent when both checks fail for different reasons.

---

## Cross-cutting

### 1. Handoff protocol has a write-gap [WARNING]

**File:** planner-science.md line 39; executor.md line 25

Planner-science produces the plan in chat but cannot write `_current_plan.md`. The executor reads `_current_plan.md`. The user bridges the gap by manually writing the plan to disk. This three-party handoff (planner-science → user → executor) is documented only in the AGENT_MANUAL, not in either agent's prompt. If the user writes a modified version, the executor will execute a different plan than was approved, and neither agent detects the divergence.

---

### 2. Data layout sections are divergent and incomplete [WARNING]

- Both agents reference only `src/rts_predict/sc2/data/sc2egset/`
- Planner-science lists `staging/` and `tmp/`; executor does not
- Neither mentions AoE2 data paths
- The executor references `DATASET_DIR` which is the SC2 variable; AoE2 uses different names

Both prompts should either unify to point at `config.py` as the canonical path registry, or document all games.

---

### 3. Research log staleness risk in re-planning [NOTE]

Planner-science reads `reports/research_log.md` at planning time. Executor writes to it after each step. If planner-science is re-invoked after partial execution (to re-plan a failed step), it reads a log containing interim findings from partial execution. The research log format (structured fields including "Issues encountered" and "Resolution/Outcome") provides enough structure for the planner to identify incomplete entries. Risk is real but inherent to the plan/execute cycle.

---

### 4. Neither agent references the Cross-Domain Transfer manual proactively [NOTE]

Planner-science says "Maintain cross-game comparability (SC2 ↔ AoE2)" but does not reference `docs/ml_experiment_lifecycle/06_CROSS_DOMAIN_TRANSFER_MANUAL.md` in its read-first list. If planner-science designs a Phase 02 SC2 feature with no AoE2 analog, cross-game comparability is silently undermined. The INDEX.md lookup (in the read-first list) would surface the manual at Phase 06, but not during Phase 02 feature engineering planning.

---

## Verdict

### planner-science

**Requires revision.** The invariant count mismatch (line 31: "10 invariants" vs. the actual 8) is a BLOCKER — the agent may hallucinate phantom invariants or search for missing ones. The SC2-only data layout section actively misleads during AoE2 planning sessions that are already in progress. The missing ml-protocol.md from the read-first list is a time bomb for Phase 04 planning.

The prompt is otherwise well-structured. The constraint language is clear, the read-first protocol is comprehensive for current Phase 01 work, and Category A plan requirements are sound. All findings are fixable without redesigning the agent.

### executor

**Requires revision, less urgently.** The most consequential finding is the Category F boundary ambiguity: the executor can write thesis chapters but lacks the writer-thesis agent's HALT-on-unsupported-claims safeguard. The superficial temporal discipline instruction (one parenthetical for the thesis's most critical methodological constraint) will compound when Phase 02+ feature engineering begins. The SC2-only data layout and the fragile B.3 template reference are maintainability hazards.

The executor prompt is otherwise well-specified: notebook workflow steps are detailed and correctly ordered, parallel execution rules are appropriate, test placement rules are clear. The model tier mismatch is a documented design choice, but the executor should echo the reviewer's honesty about Sonnet's temporal reasoning limitations and self-flag complex temporal steps for Opus.


### Summary
---
  Audit Summary                                                                                                                                                        
               
  planner-science — Requires revision                                                                                                                                  
                                                                                                                                                                       
  ┌─────┬──────────┬──────────────────────────────────────────────────────────────────────────────────────────────────┐
  │  #  │ Severity │                                             Finding                                              │                                                
  ├─────┼──────────┼──────────────────────────────────────────────────────────────────────────────────────────────────┤                                              
  │ 1   │ BLOCKER  │ Prompt says "10 invariants" — the actual count is 8. Agent may hallucinate 2 phantom invariants. │
  ├─────┼──────────┼──────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ 2   │ WARNING  │ Data layout section is SC2-only despite AoE2 datasets being actively in Phase 01.                │                                                
  ├─────┼──────────┼──────────────────────────────────────────────────────────────────────────────────────────────────┤                                                
  │ 3   │ WARNING  │ ml-protocol.md missing from read-first list — a time bomb when Phase 04 planning begins.         │                                                
  ├─────┼──────────┼──────────────────────────────────────────────────────────────────────────────────────────────────┤                                                
  │ 4   │ WARNING  │ No guidance on which dataset to plan for when multiple are active simultaneously.                │                                              
  ├─────┼──────────┼──────────────────────────────────────────────────────────────────────────────────────────────────┤                                                
  │ 5   │ NOTE     │ Category A plan requirements don't mandate documenting which invariants apply per step.          │                                              
  ├─────┼──────────┼──────────────────────────────────────────────────────────────────────────────────────────────────┤                                                
  │ 6   │ NOTE     │ No instruction to verify prior Phase gates before planning a new one.                            │                                              
  └─────┴──────────┴──────────────────────────────────────────────────────────────────────────────────────────────────┘                                                
                                                                                                                                                                     
  executor — Requires revision (less urgently)                                                                                                                         
                                                                                                                                                                     
  ┌─────┬──────────┬────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐                                  
  │  #  │ Severity │                                                    Finding                                                     │                                
  ├─────┼──────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ 1   │ WARNING  │ Sonnet-by-default with no self-awareness instruction about temporal reasoning limitations.                     │
  ├─────┼──────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ 2   │ WARNING  │ Temporal discipline guidance is a single parenthetical — no leakage failure modes, no strict < T vs <= T spec. │                                  
  ├─────┼──────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤                                  
  │ 3   │ WARNING  │ Notebook workflow step 1 references _current_plan.md B.3, which only exists in Category A plans.               │                                  
  ├─────┼──────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤                                  
  │ 4   │ WARNING  │ Category F (thesis) instructions lack the writer-thesis agent's HALT-on-unsupported-claims guardrail.          │                                
  ├─────┼──────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤                                  
  │ 5   │ WARNING  │ Data layout section is SC2-only, and diverges from planner-science's version (missing staging/, tmp/).         │                                
  ├─────┼──────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤                                  
  │ 6   │ NOTE     │ diff-cover command missing --fail-under=90 flag (reviewer has it; executor does not).                          │                                
  ├─────┼──────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤                                  
  │ 7   │ NOTE     │ Parallel execution rules don't prohibit writes to research_log.md or shared artifacts.                         │                                
  ├─────┼──────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤                                  
  │ 8   │ NOTE     │ Read-first list omits per-dataset INVARIANTS.md.                                                               │                                
  └─────┴──────────┴────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘                                  
                                                                                                                                                                     
  Cross-cutting                                                                                                                                                        
                                                                                                                                                                     
  - WARNING: No agent writes _current_plan.md — the user bridges a three-party handoff with no validation.                                                             
  - WARNING: Both agents have divergent, SC2-only data layout sections.
  - NOTE: Neither agent proactively consults the Cross-Domain Transfer manual during pre-Phase-06 feature planning.   
