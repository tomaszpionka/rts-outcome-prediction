---
plan_ref: planning/current_plan.md
spec_ref: reports/specs/01_05_preregistration.md @ master 63257289
reviewer: reviewer-adversarial
date: 2026-04-19
round: 1
---

# Critique: Chapter 4 DEFEND-IN-THESIS residuals — corpus framing (PR-1)

## Summary

Two **BLOCKERs** that require plan revision before execution. Two
**MAJORs** that change the prose output if writer-thesis proceeds as
written. Four **MINORs** worth tightening. Verdict: **REVISE**.

## Blockers

### B1 — `[POP:]` tag is absent from aoestats Phase 06 CSV (claim is partially false)

**Diagnosis.** T03 instructs writer-thesis to tell the examiner that
`[POP:]` appears in the `notes` column of every Phase 06 row across all
three datasets. Independent verification by `grep [POP:]` yields
**0 matches** in `phase06_interface_aoestats.csv` (137 rows), while the
same grep returns **35/35 rows in sc2egset** and **74/74 rows in
aoe2companion**. The aoestats CSV's notes column contains only technical
descriptors (e.g. `"continuous decile PSI n_bins=10 aoestats analyzes 15
columns..."` — see lines 2–5 of the file) and never a `[POP:]` scope.

The DEFEND-doc framing sketch for Residual #2 (line 68 of
`CHAPTER_4_DEFEND_IN_THESIS.md`) makes the same overreach — "the `[POP:]`
tag in the `notes` column of every Phase 06 row scopes every finding" —
but the artifact does not implement it for aoestats. The plan inherits
this overreach without auditing the CSVs. If writer-thesis drafts a
paragraph stating "`[POP:]` w kolumnie `notes` każdego wiersza Phase 06
CSV (pliki artifact `*/05_temporal_panel_eda/phase06_interface_*.csv`,
~35 / 74 / 136 wierszy dla sc2egset / aoe2companion / aoestats)"
(T03 step 3(b) verbatim), the thesis will make a claim that an
examiner can falsify in one `grep` command. This is a scientific-integrity
defect, not a writing-style defect.

**Fix.** Revise T03 to state the **actual** scoping mechanism. Two
options, both legitimate, but the plan must pick one and document it:

(a) Narrow the claim to what exists: sc2egset and aoe2companion carry
`[POP:tournament]` / `[POP:ranked_ladder]` in every row; aoestats is
**implicitly** `[POP:ranked_ladder]` from its spec §0 scope
(`leaderboard = 'random_map'` → `is_1v1_ranked`), and the thesis
states this explicitly rather than cite a CSV tag that does not appear.

(b) Add a preparatory chore (sibling PR or extend T02 scope) that
backfills `[POP:ranked_ladder]` into the aoestats `notes` column — then
T03's claim becomes true. This is a Category-D fix to a spec §12 Phase
06 interface artifact, not a thesis-writing task.

Recommendation: (a), because aoestats notes already carry other
technical tags (`B-02:`, `M-04:`) — adding a third tag post-hoc to
match a thesis claim is the wrong order of precedence. The thesis
must describe the world, not vice versa.

**Secondary finding (coupled):** Spec §1 (line 71) says aoestats
`[PRE-canonical_slot]` is applied to "any feature or statistic
conditioned on `team`" — grep also returns 0 hits for that tag.
This is out of PR-1 scope (it is Residual #5 for PR-3) but signals that
the Phase 06 aoestats CSV does **not** use the two scoping tags the
thesis plans to cite. PR-3 will hit the same BLOCKER unless resolved
now. Flag for planner-science.

### B2 — T03 header-level decision is internally contradictory

**Diagnosis.** T03 step 2 contains both statements on the same
bullet:

> "Draft a new subsection under the `### 4.1.3 Asymetria korpusów —
> ramy porównawcze` header (as a sibling `#### 4.1.4` — NOTE: the
> current chapter uses `###` for 4.1.X and `####` for 4.1.X.Y;
> since §4.1.4 is at the same level as §4.1.3, it must use `###`)."

The parenthetical says "must use `###`" but the main clause says
"sibling `#### 4.1.4`". Writer-thesis asked to execute this will need
to guess. Verification via grep of the current chapter: **`### 4.1.1`,
`### 4.1.2`, `### 4.1.3`, `### 4.2.1`** — all `4.X.Y` siblings are
`###`. `####` is reserved for `4.1.X.Y` (e.g. `#### 4.1.1.3`,
`#### 4.1.2.0`). So `### 4.1.4` is correct; the `####` in the main
clause is a typo that will produce a malformed header if copy-pasted.

**Also flagged:** the chapter already has one existing heading bug —
line 157 reads `#### 4.1.2 Podsumowanie i forward-reference do §4.1.3`
which mis-uses `####` for a §4.1.2.3-level element labeled §4.1.2.
The plan must NOT extend this bug by inserting a new `####` header
labeled `4.1.4`. If T03 lands as-written, the thesis will have two
malformed headings in the same section.

**Fix.** Strike the `####` language from T03 step 2; keep only "`###
4.1.4`". Optionally flag the pre-existing line 157 bug as MINOR fix
within the PR, or defer to a separate chore. Open question Q1 (plan
line 503) **claims resolution in the plan** but the T03 text was not
updated to match — Q1 resolution and T03 instructions diverge.

## Majors

### M1 — §4.1.2.1 paragraph risks examiner attack "744 is small and unjustified"

**Diagnosis.** The R4 split (construction-rationale in §4.1.2.1 now,
identification-defense in §4.4.5 in PR-2) is defensible in principle,
but T02 step 2(c) only gives writer-thesis a **parenthetical
forward-ref**: `(szczegóły identyfikacji ICC przy n=744 omawiane
w §4.4.5)`. An examiner reading §4.1.2.1 in isolation — which is
precisely how a committee member reads the data section — sees
"przy progu kohorty N=10 … kwalifikowalnych jest **744 graczy** …
N=20 daje 3 graczy" and forms the impression "this is a
ridiculously small cohort" before the forward-ref rescues the
argument. A parenthetical reference to a section that PR-1 **does not
create** cannot mitigate this.

The DEFEND doc (line 129) already has the right rhetorical move:
"At 744 clusters the ANOVA ICC point estimate is well-identified per
Gelman & Hill 2007 §11-12 … the cohort-size ceiling does not bias the
ICC, it widens the CI." That is the line that turns 744 from a
weakness into a defended design choice. Splitting it off leaves §4.1.2.1
doing half the rhetorical work and PR-2 doing the other half — but
§4.1.2.1 is where the number first appears in prose, so it must carry
enough defense to survive isolated reading.

**Fix.** Either:

(a) Allow T02's paragraph to add one defensive sentence: "Przy tej
wielkości kohorty estymata punktowa ICC typu ANOVA pozostaje
identyfikowalna (szerzej omawiane w §4.4.5); ograniczenie 744
graczy rozszerza przedział ufności, nie obciąża punktu estymaty."
Do NOT cite [Gelman2007] here (reserved for §4.4.5); hedge with the
forward-ref. This keeps the construction/identification split but
closes the §4.1.2.1 vulnerability.

(b) Move the 744 number out of §4.1.2.1 entirely and only introduce
it in §4.4.5 (PR-2). Then §4.1.2.1 would note only "the single-patch
constraint imposes a cohort ceiling documented in §4.4.5". This is
cleaner but delays the CONSORT-flow pedagogy (T02 step 1 argues the
number should appear before Tabela 4.2 so readers have it in hand).

Recommendation: (a). The plan's T02 §4.1.2.1 placement is a
deliberate pedagogical choice; respect it but arm it properly.

### M2 — Forward-refs to §4.4.4 / §4.4.5 / §4.4.6 will render as dead cross-references in PR-1 interim state

**Diagnosis.** T02 forward-refs §4.4.5; T03 forward-refs §4.4.4 and
§4.4.6. None of these sections exist on master; §4.4.4 is
`DRAFTABLE` in WRITING_STATUS; §4.4.5 and §4.4.6 are not even rows in
WRITING_STATUS. After PR-1 merges and **before** PR-2/PR-3 merge
(plan Q4 implies this gap is ≥ 1 session), the master HEAD thesis
has three forward-references pointing at section numbers that have no
headers. If an external reader (user, advisor, committee preview)
opens `04_data_and_methodology.md` during that interval, they see
broken xrefs.

The plan addresses this partially: T03 step 5 plants
`[REVIEW: forward-ref — §4.4.4/§4.4.6 nie istnieją jeszcze na master;
dodawane w PR-2 i PR-3]`. T02 step 3 merely suggests a `[REVIEW:
forward-ref — §4.4.5 added in PR-2]` flag "if writer-thesis prefers
explicit flagging" — which is optional. The inconsistency is itself
a defect: if forward-ref flagging is necessary for T03, it is
necessary for T02.

**Fix.**
1. Make the forward-ref `[REVIEW]` flag **mandatory** in T02 (not
   optional). Rewrite T02 step 3 accordingly.
2. Require the forward-ref text to use hedged Polish — e.g.
   `(omawiane w §4.4.5 w następnej aktualizacji rozdziału)` rather
   than bare `(patrz §4.4.5)`. This signals to the interim-state
   reader that the section is planned, not missing.
3. Consider adding skeleton `### 4.4.4`, `### 4.4.5`, `### 4.4.6`
   headers (status `SKELETON`) as a sibling chore inside PR-1 so
   the xrefs resolve to at least a stub. This is a 3-line change
   with large interim-coherence benefit. Out of scope for plan as
   written; raise to user for decision.

## Minors

### m1 — T04 CHANGELOG TBD backfill muddies the diff

The cosmetic backfill of PR #172 and PR #174 TBDs is unrelated to
Chapter 4 residuals. "Atomic commit" convention per
`.claude/rules/git-workflow.md` favors one logical unit per commit.
Recommendation: split T04 into two commits: `chore(changelog):
backfill PR#172 and PR#174 TBDs` first, then `chore(release): bump
to 3.24.0`. Two commits, one PR is fine per the rule.

### m2 — T02 `01_05_05_icc_results.json:35` line anchor is correct for N=10 but fragile

Line 35 in the JSON file is `"n_players": 744` (verified). Good. But
linking to a JSON line number is fragile — any future edit shifts the
anchor. Prefer keying to the `n_min10.n_players` JSONPath, cited as
`01_05_05_icc_results.json → icc_by_cohort_threshold.n_min10.n_players`.
Minor stylistic preference; does not affect scientific claim.

### m3 — Gate Condition flag budget (3–5) is achievable but tight

T01 = 1 flag, T02 = 1 flag (or 2 if B2/M2 fix forces a mandatory
forward-ref flag), T03 = 2 flags. Total = 4–5. Fine under current
T-task text. If the fixes above add one more forward-ref flag to T02,
total = 5–6, exceeding the stated ceiling. Raise the budget ceiling
to 6 in the Gate Condition to avoid a trivial gate fail.

### m4 — Sensitivity-axis source attribution: "PR #171 cohort-axis sensitivity (post-v1.0.4 spec amendment)"

The JSON artifact itself (line 74) confirms: *"v1.0.4 (PR fix/01-05-aoestats-icc-cohort-axis): sensitivity axis changed from requested-sample-size {20k,50k,100k} (which degenerated to the 744-player population) to spec §6.2 cohort match-count thresholds N ∈ {5,10,20}"*. T02 step 2(b) cites this correctly. No defect; this is a verified PASS and I record it here so the user sees the verification was done.

## Verdict

**REVISE.** B1 blocks execution because writer-thesis would draft a
factually wrong `[POP:]` claim citing an artifact that does not
contain the tag. B2 blocks because the plan's own Q1 resolution
disagrees with T03's instruction text. Fix B1 + B2 + M1 + M2 before
dispatching writer-thesis; the rest are tighten-on-execution.

## Resolutions applied at review time (verified PASSes)

- **Sensitivity-table numbers** (plan lines 86–90): 4 325 / 744 / 3
  players and 0.0251 / 0.0268 / 0.0176 ICC **exactly match**
  `01_05_05_icc_results.json` lines 16–57. PASS.
- **WRITING_STATUS row insertability**: the §4.1 table has one row
  per subsection (§4.1.1, §4.1.2, §4.1.3) — a new §4.1.4 row between
  §4.1.3 and §4.2.1 fits the schema. PASS.
- **§4.1.3 insertion point** (plan T01): the existing §4.1.3 ends at
  line 203 and §4.2 header is at line 205. Inserting a new trailing
  paragraph before line 205 preserves the Tabela 4.4a/4.4b
  structure. PASS.
- **Spec §7 / §11 W3 binding anchor** (plan line 91): spec §1 line
  67–71 confirms W3 ARTEFACT_EDGE binding is canonical and
  `[PRE-canonical_slot]` is the assigned flag name. PASS on the
  citation target; see B1 secondary finding for its artifact-level
  absence.
- **3-round adversarial cap interpretation** (plan Q4): two passes
  per PR (plan-side + execution-side) matches memory
  `feedback_adversarial_cap_execution.md`. PASS on workflow.


---

## Round 2 — execution-side

**Reviewer:** reviewer-adversarial
**Date:** 2026-04-19
**Base ref:** master 63257289
**Branch:** docs/thesis-ch4-corpus-framing-residuals

### Summary

Independent verification of the executed diff against the revised plan:
**0 BLOCKERs**, **1 MAJOR** (char-budget overrun ~59% over stated Gate
ceiling; writer-thesis understated this as 44%), **3 MINORs**. Verdict:
**PASS** — with one MAJOR the user should knowingly accept or send
back for trimming. The MINORs are tighten-on-merge or defer-to-Pass-2.
Execution-side round 1 of 3 consumed.

### Blockers

None. Plan-side B1 and B2 fixes were implemented correctly
(artifact-vs-spec honest-match language in §4.1.4; `###` header at
§4.1.4; pre-existing line-159 `#### 4.1.2 Podsumowanie` bug correctly
left untouched per Out-of-scope). M1 defensive sentence present. Both
M2 mandatory forward-ref flags planted with hedged Polish wording.

### Majors

#### M1-exec — Char overage is 59%, not 44% as self-reported

Empirical `wc -m` on the three inserted paragraphs:

| Task | Plan budget | Delivered | Over by |
|------|-------------|-----------|---------|
| T01 | 300–500 | 794 | +59% |
| T02 | 500–700 | 1 121 | +60% |
| T03 | 1 000–1 500 | 2 546 | +70% |
| **Total** | **~2 100–2 800** | **~4 461** | **+59%** |

Writer-thesis reported "~4 030 chars, 44% over." True figure is
~4 461 chars / 2 800 = **+59%** — self-report understates by ~430
chars and ~15 percentage points. Critical Review Checklist
numerical-consistency item should have caught this.

Load-bearing audit: most content is examiner-friendly scaffolding,
not boilerplate. But tightening opportunities exist:
- T03 inline CSV-artifact inventory (35/35, 74/74, 137, column
  clauses) → could move to REVIEW_QUEUE Key artifacts cell; ~450 chars.
- T02 sensitivity table inline → JSONPath citation suffices; ~200 chars.

**Severity rationale.** MAJOR not BLOCKER because content is load-
bearing; no scientific-integrity defect. The plan's Gate Condition
ceiling is a writer-thesis self-discipline rule. User should either
(a) accept overage on this PR with true figure recorded, or (b)
trigger a targeted tighten pass (1 round) of writer-thesis.

### Minors

#### m1-exec — aoestats row count off-by-one (cosmetic)

T03 says `phase06_interface_aoestats.csv (137 wierszy)`. Data-row
count (excluding header) is **136**. sc2egset "35/35" and aoe2companion
"74/74" use data-row convention; aoestats "137" uses total-line
convention. Inconsistent.

**Fix.** Change `137 wierszy` → `136 wierszy` in T03 (1 token edit).

#### m2-exec — "§0 w koniunkcji z filtrem R02" attribution slightly over-generous to §0

Writer-thesis reframed to "implicit z spec §0 w koniunkcji z filtrem
cleaning R02 (`leaderboard = 'random_map'`)". Independent check:
spec §0 names datasets + Phase 01 step 01_05 scope, but does NOT
state `leaderboard = 'random_map'` or reference R02. Operative
scoping for aoestats ranked_ladder comes from **R02 alone**; §0 binds
aoestats to the 01_05 protocol. Prose is defensible under charitable
reading but tightening would say "implicit via cleaning rule R02,
with spec §0 binding aoestats to 01_05 protocol". Defer to Pass-2.

#### m3-exec — Plan text says "F4", writer used "F6"

Writer-thesis correctly detected F4 was taken and used F6. The plan
T03 step 8 text still says "a new `F4` entry (or next free `F`-number)".
Cosmetic plan/actual divergence; fix plan text to `F6` when committed.

### Passes (verified)

- **Numerical accuracy (T02 sensitivity table).** All six numbers verified
  against `01_05_05_icc_results.json`:
  - n_min5.n_players = 4325, n_obs = 30975 (JSON lines 16–17)
  - n_min10.n_players = 744, n_obs = 7909 (JSON lines 35–36)
  - n_min20.n_players = 3, n_obs = 77 (JSON lines 54–55)
  - Polish typography: space thousands, comma decimals. PASS.
- **Reference-window dates (T01).** 2022-08-29 → 2022-10-27, patch 66692.
  Match. PASS.
- **B1 `[POP:]` artifact state (T03).** `grep '\[POP:'` returns
  0/137 for aoestats, 35/35 for sc2egset, 74/74 for aoe2companion.
  Prose says `nie niesie jawnego tagu [POP:]` for aoestats. Honest-
  matched. PASS.
- **B2 header level.** `### 4.1.4` at line 209 (3 hashes, sibling to
  §4.1.3). Pre-existing line-159 `#### 4.1.2` bug untouched per Out-
  of-scope deferral. PASS.
- **M1 defensive sentence.** Present at line 101: "Estymata punktowa
  ICC typu ANOVA pozostaje identyfikowalna … rozszerza przedział
  ufności, nie obciąża punktu estymaty." Wording matches. PASS.
- **M2 forward-ref flags.** Both present with hedged Polish phrase
  "w kolejnej aktualizacji rozdziału". PASS.
- **Flag inventory.** Exactly 5 new flags (T01=1, T02=2, T03=2).
  Gate budget 3–7 satisfied. PASS.
- **Tracker updates.** REVIEW_QUEUE §4.1.3 / §4.1.2 / §4.1.4 rows
  updated; WRITING_STATUS §4.1.2 / §4.1.3 notes + §4.1.4 new row
  inserted correctly; "Last updated: 2026-04-19" bumped. PASS.
- **BACKLOG F6 entry.** Matches F1/F2/F3 format; enumerates both
  `[POP:ranked_ladder]` and `[PRE-canonical_slot]` tag backfill;
  category D; Acceptance with grep row-count assertion. PASS.
- **Cross-chapter consistency.** T03 N=2 Friedman inapplicability
  claim matches existing §2.6 language. PASS.
- **Pre-commit hook risk.** `.md`-only diff; ruff/mypy skip; planning
  validation hook will check `current_plan.md` frontmatter (all
  required fields present). PASS (best-effort audit).
- **Polish-idiom flagging.** All five idiom uncertainties explicitly
  flagged via `[REVIEW: … verify Polish idiom for …]`. PASS.

### Verdict

**PASS** — cleared for PR wrap-up conditional on user's decision about
the char overage. No scientific-integrity defect remains. Three MINORs
fixable in 2 minutes; MAJOR is a budget-vs-content tradeoff the user
owns.
