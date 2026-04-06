# Plan: PJAIT References and Nemenyi Cleanup (Category E — Docs only)

**Branch:** `docs/pjait-references`
**Branch base:** `master` (after `docs/thesis-formatting-rules` is merged)
**Version bump:** minor
**Files touched:** 8 files modified, 1 file tracked

## Dependency

`docs/thesis-formatting-rules` branch must be merged to master first (Steps 4b and 5 reference `.claude/thesis-formatting-rules.yaml`). If blocked, those two sub-steps can be deferred.

---

## Critical Finding: 7 Stale Nemenyi References

| # | File | Context |
|---|------|---------|
| 1 | `.claude/scientific-invariants.md` line 106 | Invariant #10 — **most critical** (read every session) |
| 2 | `thesis/THESIS_STRUCTURE.md` line 114 | §2.6 description |
| 3 | `thesis/THESIS_STRUCTURE.md` line 313 | §5.3.1 description |
| 4 | `thesis/chapters/02_theoretical_background.md` line 50 | Skeleton comment |
| 5 | `thesis/chapters/04_data_and_methodology.md` line 108 | Skeleton comment |
| 6 | `thesis/chapters/05_experiments_and_results.md` line 58 | Skeleton comment |
| 7 | `docs/THESIS_WRITING_MANUAL.md` | Already correct — describes deprecation |

Authoritative replacement (from `docs/THESIS_WRITING_MANUAL.md` §3.2, PR #38):
**Friedman omnibus + pairwise Wilcoxon/Holm + Bayesian signed-rank with ROPE (baycomp)**

`SC2_THESIS_ROADMAP.md` — zero Nemenyi references (clean).

---

## Step 1 — `.claude/scientific-invariants.md` — fix invariant #10

**old_string:**
```
(Friedman test with Nemenyi post-hoc, per Demšar 2006)
```

**new_string:**
```
(Friedman omnibus test, then pairwise Wilcoxon signed-rank with Holm
    correction, complemented by Bayesian signed-rank with ROPE via baycomp;
    per Benavoli et al. 2017, Garcia & Herrera 2008)
```

Verify: `grep -c "Nemenyi" .claude/scientific-invariants.md` → 0

---

## Step 2 — `thesis/THESIS_STRUCTURE.md` — 3 edits

**2a.** §2.6 (line 113–116):

old:
```
- Friedman test with Nemenyi post-hoc for comparing classifiers across
  multiple datasets [cite: Demšar 2006, JMLR]
- Critical difference diagrams
```

new:
```
- Friedman omnibus test for comparing classifiers across multiple datasets
  [cite: Demšar 2006, JMLR]
- Pairwise Wilcoxon signed-rank with Holm correction [cite: Garcia & Herrera
  2008; Garcia et al. 2010]
- Bayesian signed-rank test with ROPE [cite: Benavoli et al. 2017]
- Critical difference diagrams (Wilcoxon-based, not Nemenyi-based)
```

**2b.** §5.3.1 (line 313):

old: `- Friedman test with Nemenyi post-hoc on matched method × game matrix`
new: `- Friedman omnibus + Wilcoxon/Holm pairwise tests + Bayesian signed-rank on matched method × game matrix`

**2c.** Add institution line below the Degree line (line 5):

```
**Institution:** Polish-Japanese Academy of Information Technology (PJAIT), Warsaw
```

Verify: `grep -c "Nemenyi" thesis/THESIS_STRUCTURE.md` → 0; `grep "PJAIT" thesis/THESIS_STRUCTURE.md` → match

---

## Step 3 — Thesis chapter skeletons — 3 files

**3a.** `thesis/chapters/02_theoretical_background.md` line 50:

old: `Friedman test + Nemenyi post-hoc (Demšar 2006), critical difference diagrams.`
new:
```
Friedman omnibus + Wilcoxon/Holm pairwise + Bayesian signed-rank (ROPE).
Nemenyi deprecated due to pool-dependence (Benavoli et al. 2016).
Critical difference diagrams (Wilcoxon-based). See THESIS_WRITING_MANUAL.md §3.2.
```

**3b.** `thesis/chapters/04_data_and_methodology.md` line 108:

old: `Friedman + Nemenyi for cross-game comparison.`
new:
```
Friedman omnibus + Wilcoxon/Holm pairwise + Bayesian signed-rank for cross-game comparison.
See THESIS_WRITING_MANUAL.md §3.2.
```

**3c.** `thesis/chapters/05_experiments_and_results.md` line 58:

old: `Friedman test + Nemenyi, critical difference diagram.`
new:
```
Friedman omnibus + Wilcoxon/Holm pairwise + Bayesian signed-rank, critical difference diagram.
See THESIS_WRITING_MANUAL.md §3.2.
```

Verify: `grep -rc "Nemenyi" thesis/chapters/` → all 0

---

## Step 4 — `README.md` — PJAIT context + Key Documents

**4a.** Add after thesis title line:

```markdown
**Institution:** Polish-Japanese Academy of Information Technology (PJAIT), Warsaw
**Degree:** Master of Science in Computer Science, Data Science specialisation
```

**4b.** Add to Key Documents table (after `.claude/` row):

```markdown
| `docs/PJAIT_THESIS_REQUIREMENTS.md` | Institutional requirements — formatting, defense, grading |
| `.claude/thesis-formatting-rules.yaml` | Machine-readable PJAIT formatting thresholds |
```

Verify: `grep "PJAIT" README.md` → match; `grep "thesis-formatting-rules" README.md` → match

---

## Step 5 — `thesis/WRITING_STATUS.md` — add formatting targets box

Insert after the Status key table (before first chapter section):

```markdown
---

## Formatting targets

Minimum length: **72,000 characters with spaces** (~40 normalized pages, typical 60–80).
Abstract: 400–1500 characters. Keywords: 3–5.
Full validation rules: `.claude/thesis-formatting-rules.yaml` → `content_thresholds`.
Source: `docs/PJAIT_THESIS_REQUIREMENTS.md`.

---
```

Verify: `grep "thesis-formatting-rules" thesis/WRITING_STATUS.md` → match

---

## Step 6 — Track `docs/PJAIT_THESIS_REQUIREMENTS.md` in git

File exists but is untracked (`??`). Stage with `git add docs/PJAIT_THESIS_REQUIREMENTS.md`.

---

## Step 7 — CHANGELOG + version bump

Bump minor in `pyproject.toml`. Add to `CHANGELOG.md` under `[Unreleased]`:

```
### Added
- `docs/PJAIT_THESIS_REQUIREMENTS.md` tracked in git; authoritative source for formatting and defense requirements
- `README.md` PJAIT institution name, degree, and key document references
- `thesis/WRITING_STATUS.md` formatting targets reference box
- `thesis/THESIS_STRUCTURE.md` PJAIT institution line

### Changed
- `.claude/scientific-invariants.md` invariant #10: Nemenyi → Wilcoxon/Holm + Bayesian signed-rank
- `thesis/THESIS_STRUCTURE.md` §2.6 and §5.3.1: same Nemenyi → Wilcoxon/Holm + Bayesian update
- `thesis/chapters/02_theoretical_background.md`, `04_data_and_methodology.md`, `05_experiments_and_results.md`: skeleton comments updated
```

---

## Commits

1. `docs(thesis): replace stale Nemenyi references with Wilcoxon/Holm + Bayesian signed-rank`
   Files: `.claude/scientific-invariants.md`, `thesis/THESIS_STRUCTURE.md`, all 3 chapter skeletons

2. `docs(thesis): add PJAIT institutional context and formatting references`
   Files: `README.md`, `thesis/THESIS_STRUCTURE.md` (institution line), `thesis/WRITING_STATUS.md`, `docs/PJAIT_THESIS_REQUIREMENTS.md`, `CHANGELOG.md`, `pyproject.toml`

---

## Gate Condition

- `grep -rc "Nemenyi" .claude/scientific-invariants.md thesis/THESIS_STRUCTURE.md thesis/chapters/` → all 0
- `grep -c "PJAIT" README.md thesis/THESIS_STRUCTURE.md` → non-zero for both
- `grep -c "thesis-formatting-rules" README.md thesis/WRITING_STATUS.md` → non-zero for both
- `git status docs/PJAIT_THESIS_REQUIREMENTS.md` → tracked
