# Plan Critique — reviewer-adversarial Mode A

**Target:** `planning/current_plan.md`
**Date:** 2026-04-20
**Reviewer:** reviewer-adversarial Mode A (pre-execution methodology audit)

## Verdict: REQUIRE_MINOR_REVISION

Plan correctly identifies the three-way drift and proposes a defensible target end-state. Three MAJOR methodology-grade issues and three MINOR issues to resolve before dispatch. None is a BLOCKER.

## Findings

### MAJOR A1: §4.1.4 line 213 bare "Friedman oraz Wilcoxon-Holm" mention breaks within-game/cross-game partition
`04_data_and_methodology.md:213` reads *"dla N = 2 gier Friedman oraz Wilcoxon-Holm są inaplikowalne per [Demsar2006]"* — correct for cross-game scope, but the reader has no within-game/cross-game qualifier cue. After T03's softened candidate framing in §4.4.4, §4.1.4 reads as firmer methodology than §4.4.4 does — inversion.

**Fix:** Extend T03 step 5.5 (or add a new T02 step) requiring either (i) a within-game qualifier on line 213 ("w ramach cross-game przy N = 2…"), or (ii) explicit scoping declaration that §4.1.4 line 213 is cross-game-only.

### MAJOR A2: Candidate #3 is not methodologically distinct from Candidate #1's post-hoc block
T03 step 6's three candidates reduce to two framework families:
- Candidate #1 = Friedman omnibus + post-hoc Wilcoxon-Holm + Bayesian signed-rank
- Candidate #3 = Sequential pairwise Wilcoxon with Holm (i.e., #1's post-hoc phase minus omnibus minus Bayesian component)
- Candidate #2 = pure Bayesian

This is two families (frequentist + Bayesian) plus one gating variant of the frequentist track — not three inference frameworks. Exposes the plan to the "single-protocol verb-swap" charge line 192 warns against.

**Fix:** Either replace Candidate #3 with genuinely distinct framework (e.g., Iman-Davenport F-statistic — distinct omnibus test endorsed by Demsar), or re-label the enumeration as "two candidate families with gating variants".

### MAJOR A3: ROPE-removal doesn't address the implicit α = 0,05 Holm schedule in §2.6.3 line 215
§2.6.3 line 215 contains "*progami α/(k−i+1) dla i-tego najmniejszego*" — the Holm sequential α-schedule presupposes a fixed α (implicitly 0,05) never cited in §2.6 prose. Plan removes the visible ROPE magic number but leaves an invisible load-bearing α threshold unaddressed — invariant #7 half-compliance.

**Fix:** T02 step 5 should explicitly instruct either (a) α is kept with an in-prose citation, or (b) α is deferred alongside ROPE to methodology finalization.

### MINOR A4: Open Q 5 (§4.2 grep sweep) is actually resolved by this Mode A review
Independent grep of `Dimitriadis|tryptyk|Nemenyi|Wilcoxon|Friedman|signed-rank|Bayesian|ROPE` on `04_data_and_methodology.md` returns exactly 2 hits: line 213 (§4.1.4) and line 371 (§4.4.4). §4.2 confirmed untouched. Plan's Open Q 5 can be marked RESOLVED.

### MINOR A5: Malformed REVIEW_QUEUE row at line 43-44 may break executor grep scripting
`REVIEW_QUEUE.md:43-44` has table-pipe anomaly. T03 step 10's "flag count 3" arithmetic is correct but executor should be warned about the malformed row.

### MINOR A6: "Sanity-check, not blocking" character budgets are permissive enough to allow net-additive substance
±1500 char budget on §2.6 = ~10% drift; non-blocking means overshoots can substantively expand the section beyond "prose swap" intent.

**Fix:** Either make character budgets blocking, or add explicit "no net-additive content" gate bullet.

## Probes answered

- **Probe 1 (un-commitment vs lower-abstraction commitment):** Option B shifts commitment from triptych to ECE-stack — net commitment is not reduced, it is relocated. User's resolution is defensible but aware.
- **Probe 2 (cross-ref graph):** Acyclic. §1.2 → §4.4.4, §2.6.x → §4.4.4, §4.4.4 → §2.6 + §4.4.2. No cycles.
- **Probe 3 (invariant #8 timing):** Advisory framing is load-bearing, not window-dressing. Sound.
- **Probe 4 (ROPE invariant #7):** Partially addressed — ROPE removed but α=0,05 uncovered. See A3.
- **Probe 5 (Demsar §3.1.3):** WebFetch could not read the PDF binary. Plan's T02 deferral with [REVIEW:] fallback is correct. Cannot close here.
- **Probe 6 (voice consistency):** Adequate register shift from §2.6.1 decisive to §2.6.2-5 hedged; writer-thesis can handle.
- **Probe 7 (scope creep):** File Manifest clean; 5 files only. See A6 for char-budget permissiveness.
- **Probe 8 (Ambiguity B):** Resolved. See A4.
- **Probe 9 (Option b re-verification):** Option (a) more un-commitment-pure; Option (b) more examiner-defensible. User's choice stands.
- **Probe 10 (Pass-2 flag count):** Arithmetic correct. See A5 for row format anomaly.

### Additional methodology probes

- **Candidate-space enumeration soundness:** Three candidates reduce to two framework choices — see A2.
- **Deferral language credibility:** "Deferred to §4.4.2 (BLOCKED)" is honest but weak; risk surfacing only when §4.4.2 is drafted.
- **Within-game/cross-game partition:** Methodologically sound for N=2, but §4.1.4 line 213 implicitly breaks it — see A1.

## Recommendation

**REQUIRE_MINOR_REVISION before dispatch.** Apply A1, A2, A3 (MAJORs) before writer-thesis execution. A5, A6 (MINORs) are optional polish. A4 resolves Open Q 5 in-place.

After these revisions, plan is PROCEED material.

## Sources

- Demšar 2006, JMLR: https://jmlr.org/papers/v7/demsar06a.html — §3.1.3 / §3.2 section anchor not verifiable via web tools, correctly deferred to T02.
- García & Herrera 2008, JMLR extension: https://www.jmlr.org/papers/volume9/garcia08a/garcia08a.pdf
