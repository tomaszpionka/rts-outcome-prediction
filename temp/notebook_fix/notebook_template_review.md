# Adversarial Review — Notebook Template + Existing Notebooks

```
Target: temp/notebook_template.md, sandbox/README.md, sandbox/notebook_config.toml,
        sandbox/sc2/sc2egset/01_exploration/01_acquisition/01_01_01_file_inventory.py,
        sandbox/aoe2/aoe2companion/01_exploration/01_acquisition/01_01_01_file_inventory.py,
        sandbox/aoe2/aoestats/01_exploration/01_acquisition/01_01_01_file_inventory.py
Phase: 01 (Data Exploration) — in_progress for sc2egset
Date: 2026-04-10
Review mode: B (Artifact Review)
```

---

## Executive Summary

The existing Phase 01 notebooks are methodologically sound for their scope. The template, however, **contradicts the notebooks it purportedly governs** and lacks structural enforcement of scientific invariants that become load-bearing in Phase 02+. Verdict: **REVISE** before generating Phase 02 notebooks.

---

## Invariant Compliance

| Invariant | Status | Notes |
|-----------|--------|-------|
| #1 (per-player split) | N/A | Phase 01 file inventory; no splitting |
| #2 (canonical nickname) | N/A | No player identity work |
| #3 (temporal < T) | **AT RISK** | Template has no leakage verification section |
| #4 (prediction target) | N/A | No prediction work |
| #5 (symmetric treatment) | N/A | No feature computation |
| #6 (reproducibility) | RESPECTED / **AT RISK** | Current notebooks ok; template doesn't enforce artifact-level code embedding |
| #7 (no magic numbers) | RESPECTED / **AT RISK** | No thresholds used yet; template has no threshold justification field |
| #8 (cross-game protocol) | RESPECTED | Template is game-agnostic in structure |

---

## Template Strengths

- Game-agnostic structure supports cross-game comparability
- Front-matter table captures essential metadata (phase, dataset, scientific question)
- Mandatory markdown interpretation cells after code cells enforce narrative discipline
- Conclusion section with thesis mapping creates traceability
- Cleanup cell prevents resource leaks

---

## Critical Gaps

### Finding #1 — Template vs. existing notebooks: front-matter divergence

The template prescribes a markdown table with fields: Phase, Step, Dataset, Game, Date, Report artifacts, Scientific question, ROADMAP reference.

Existing notebooks use an entirely different format — bold key-value pairs:

```
**Phase:** 01 — Data Exploration
**Pipeline Section:** 01_01 — ...
**Dataset:** sc2egset
**Question:** ...
```

Divergences:
- Template uses a markdown table; notebooks use bold key-value pairs
- Template requires `Date` field; no existing notebook has a date
- Template requires `Report artifacts` listed in front-matter; no existing notebook declares these upfront
- Template requires `ROADMAP reference`; no existing notebook includes this
- Template uses `Step` field with format `e.g. 1.8`; notebooks use `XX_YY_ZZ` format per project taxonomy
- Notebooks include a `Layout note` section not prescribed by the template

**Impact:** If the template is cited in the methodology chapter as the notebook standard, an examiner who checks any notebook will find it non-conformant.

### Finding #2 — No Conclusion section in any existing notebook

The template prescribes a Conclusion cell containing: Artifacts produced, Follow-ups, Thesis mapping. None of the three existing notebooks contain any of these. They end with a brief "Verification" markdown cell.

**Impact:** The notebook (the executable artifact an examiner would re-run) does not self-document where its findings feed into the thesis. Thesis mapping lives only in the ROADMAP YAML, creating a traceability gap.

### Finding #3 — No `con.close()` cleanup cell in any existing notebook

None of the existing notebooks call `con.close()` or `get_notebook_db()` — they are filesystem-only inventories. The template's mandatory setup/cleanup cells are DuckDB-centric and inapplicable to non-DuckDB notebooks.

**Impact:** Template does not accommodate non-DuckDB notebooks, which already exist.

### Finding #4 — Template does not enforce Invariant #6 (reproducibility alongside results)

Invariant #6 requires that report artifacts embed the exact SQL/Python code used to compute each number. The template's "Cells 3-N" guidance says only "code cell + markdown cell." It does not require artifact-level code embedding.

**Impact:** As notebooks grow complex (Phase 02+), report artifacts will contain derived statistics without derivation code. Compliance depends on executor discipline, not template structure.

### Finding #5 — No version/environment pinning in front-matter

The template does not require recording Python version, library versions, or `poetry.lock` hash. An examiner re-running months later may get different results due to dependency drift.

### Finding #6 — No temporal leakage verification section

Starting Phase 02 (Feature Engineering) and Phase 03 (Splitting & Baselines), every notebook touching DuckDB will compute features where Invariant #3 is load-bearing. The template has no required cell or front-matter field for temporal leakage verification.

**Impact:** Whether temporal discipline is enforced depends entirely on executor diligence, not template structure.

---

## Recommended Additions/Changes

### Template structure changes

1. **Reconcile front-matter format** — Either adopt the bold key-value style the notebooks actually use, or update all notebooks to match the table format. Do not leave both in contradiction.

2. **Fix step numbering** — Replace `{step_id, e.g. 1.8}` with `{step_id, e.g. 01_01_01}` to match project taxonomy.

3. **Add conditional DuckDB section** — The setup/cleanup cells should be conditional. Add a note: "If this notebook does not use DuckDB, omit the `get_notebook_db()` / `con.close()` cells."

4. **Parameterize game/dataset** — Replace hardcoded `con = get_notebook_db("sc2", "sc2egset")` with `con = get_notebook_db("{game}", "{dataset}")` to prevent copy-paste errors.

### New required sections

5. **Add "Invariants applied" front-matter field** — Mirror the `scientific_invariants_applied` field from the ROADMAP step template. Each notebook must declare which invariants are active and how they are verified in code.

6. **Add temporal leakage verification cell** (Phase 02+ only) — Before the Conclusion, require a cell that explicitly verifies no future data was used. Example: assert that all feature computation windows end before game T.

7. **Add environment snapshot field** — Front-matter should record: Python version, key library versions, or `poetry.lock` commit hash.

8. **Add phase-specific required sections** — The template should have conditional sections for:
   - Phase 02: Feature category (pre-game vs. in-game), symmetry verification, cold-start handling
   - Phase 03: Split strategy, leakage verification
   - Phase 05: Statistical test justification, assumptions checked, ROPE intervals

### Enforcement

9. **Implement the planned AST-based cell cap check** — The 50-line cell cap in `notebook_config.toml` is currently unenforced (the comment says "planned"). Add a pre-commit hook or CI check.

10. **Add notebook lint to CI** — Validate front-matter completeness, cell count limits, and required sections programmatically.

---

## Existing Notebook Conformance Audit

| Requirement | SC2 sc2egset | AoE2 companion | AoE2 stats |
|-------------|:---:|:---:|:---:|
| Front-matter present | Yes (different format) | Yes (different format) | Yes (different format) |
| Date field | Missing | Missing | Missing |
| ROADMAP reference | Missing | Missing | Missing |
| Report artifacts in front-matter | Missing | Missing | Missing |
| Scientific question | Present | Present | Present |
| Markdown after each code cell | Yes | Yes | Yes |
| Conclusion section | Missing | Missing | Missing |
| Thesis mapping | Missing | Missing | Missing |
| Follow-ups section | Missing | Missing | Missing |
| Cleanup cell | N/A (no DuckDB) | N/A (no DuckDB) | N/A (no DuckDB) |
| Cell cap (50 lines) | Compliant | Compliant | Compliant |
| No inline definitions | Compliant | Compliant | Compliant |

---

## Examiner's Questions (anticipate these)

1. **"Your template says front-matter should be a table with Date and ROADMAP reference fields. None of your notebooks have either. Which is the authoritative format?"**

2. **"How do you ensure that Phase 02+ notebooks don't leak future data? I see no structural check in your template."**

3. **"Your notebook_config.toml sets a 50-line cell cap, but I see no pre-commit hook or CI check that enforces it. What happens when an executor writes a 60-line cell?"**

4. **"Your template hardcodes `con = get_notebook_db('sc2', 'sc2egset')`. How do you prevent copy-paste errors when creating AoE2 notebooks?"**

5. **"Where in the notebook can I find the thesis section that these findings feed? I see a Verification cell but no Thesis mapping."**

---

## Risks

| Severity | Finding | Action |
|----------|---------|--------|
| WARNING | Template-notebook divergence undermines credibility | Reconcile before Phase 02 |
| WARNING | No temporal leakage verification section | Add required cell for Phase 02+ |
| WARNING | 50-line cell cap is unenforced | Implement AST-based check |
| NOTE | Template does not accommodate non-DuckDB notebooks | Add conditional path |
| NOTE | No environment version pinning | Add front-matter field |
| NOTE | Step numbering example inconsistent with taxonomy | Fix to `XX_YY_ZZ` |

---

## Final Verdict: REVISE

The existing Phase 01 notebooks are methodologically sound for their scope — simple file inventories with no temporal, statistical, or feature engineering concerns. No methodology flaws identified in the notebooks themselves.

The template is **not fit for purpose**. It contradicts the notebooks it governs (finding #1), omits sections the notebooks omit (finding #2), hardcodes assumptions that don't hold for all notebooks (finding #3), lacks enforcement of scientific invariants (finding #4), and uses numbering conventions inconsistent with the project taxonomy (finding #6).

**The template must be revised before Phase 02 notebooks are generated**, because Phase 02 is where temporal discipline, feature engineering documentation, and threshold justification become load-bearing — and the current template provides no structural guardrails for any of these.

Recommend a follow-up review once Phase 02+ notebooks exist to re-evaluate temporal leakage enforcement against actual feature computation code.
