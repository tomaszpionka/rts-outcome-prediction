# Thesis Writing Status

Last updated: 2026-04-17

---

## Status key

| Status | Meaning |
|--------|---------|
| `SKELETON` | Header and brief note exist. No prose. |
| `BLOCKED` | Feeding phase incomplete — cannot write yet. |
| `DRAFTABLE` | Feeding phase complete — ready to draft. |
| `DRAFTED` | First draft exists. May need revision later. |
| `REVISED` | Updated after later phase provided new context. |
| `FINAL` | Content-complete, ready for typesetting. |

---

## Formatting targets

Minimum length: **72,000 characters with spaces** (~40 normalized pages, typical 60–80).
Abstract: 400–1500 characters. Keywords: 3–5.
Full validation rules: `.claude/thesis-formatting-rules.yaml` → `content_thresholds`.
Source: `docs/thesis/PJAIT_THESIS_REQUIREMENTS.md`.

---

## Chapter 1 — Introduction

| Section | Status | Feeds from | Notes |
|---------|--------|------------|-------|
| §1.1 Background and motivation | `DRAFTED` | — | Literature + framing. Gate 0 voice calibration draft. |
| §1.2 Problem statement | `DRAFTABLE` | — | Literature + framing |
| §1.3 Research questions | `DRAFTED` | — | Literature + framing. Drafted 2026-04-17. 4 RQs operationalized; 9 inline citations; 2 [REVIEW] flags. ~5.0k chars Polish. Finalize after Phase 03–04. |
| §1.4 Scope and limitations | `DRAFTED` | — | Literature + framing. Drafted 2026-04-17. 7 inline citations; 1 [REVIEW] flag (AoE2 roadmap). ~4.6k chars Polish. Revise after AoE2 lit review. |
| §1.5 Thesis outline | `BLOCKED` | All chapters | Write last |

## Chapter 2 — Theoretical Background

| Section | Status | Feeds from | Notes |
|---------|--------|------------|-------|
| §2.1 RTS game characteristics | `DRAFTABLE` | — | Literature |
| §2.2 StarCraft II | `DRAFTABLE` | Phase 01 (Data Exploration — timing, mechanics) | Literature part draftable; data-derived details added after Phase 01 |
| §2.3 Age of Empires II | `BLOCKED` | AoE2 roadmap | Future |
| §2.4 ML methods for classification | `DRAFTABLE` | — | Literature |
| §2.5 Player skill rating systems | `DRAFTED` | — | Literature; Gate 0.5 calibration draft (2026-04-17). 14 distinct keys / 24 inline citations, 4 [REVIEW] flags. ~20.9k chars Polish. **Gate 0.5: PASS_FOR_PRODUCTION_SCALING.** |
| §2.6 Evaluation metrics | `DRAFTABLE` | — | Literature |

## Chapter 3 — Related Work

| Section | Status | Feeds from | Notes |
|---------|--------|------------|-------|
| §3.1 Traditional sports prediction | `DRAFTABLE` | — | Literature |
| §3.2 StarCraft prediction literature | `DRAFTED` | — | Literature; Pass 1 calibration draft (2026-04-17). 28 distinct keys / ~46 inline citations, 6 [REVIEW] flags. ~14.8k chars Polish. 15 new bibtex entries appended. Tarassoli2024 flagged as SC-Phi2 misattribution; deferred to user morning review. |
| §3.3 MOBA and other esports | `DRAFTABLE` | — | Literature |
| §3.4 AoE2 prediction | `BLOCKED` | AoE2 lit review | Future |
| §3.5 Research gap | `BLOCKED` | §3.1-§3.4 | Skeleton draftable from §3.1-§3.3; full draft blocked on §3.4 (AoE2 lit review) |

## Chapter 4 — Data and Methodology

| Section | Status | Feeds from | Notes |
|---------|--------|------------|-------|
| §4.1.1 SC2EGSet description | `BLOCKED` | Phase 01 (Data Exploration) | Steps 01_01–01_07 done; awaiting Step 01_08 (game settings + field completeness audit) |
| §4.4.4 Evaluation metrics | `DRAFTABLE` | — | Literature |

Remaining 11 sections all `BLOCKED` — waiting on Phase 01–04 (SC2) and AoE2 roadmap phases.

## Chapter 5 — Experiments and Results

All 6 sections `BLOCKED` — waiting on Phases 03-05 (SC2) and AoE2 phases.

## Chapter 6 — Discussion

| Section | Status | Feeds from | Notes |
|---------|--------|------------|-------|
| §6.5 Threats to validity | `DRAFTABLE` | — | Start listing known threats; expand after experiments |

Remaining 4 sections all `BLOCKED` — waiting on Chapter 5.

## Chapter 7 — Conclusions

| Section | Status | Feeds from | Notes |
|---------|--------|------------|-------|
| §7.3 Future work | `DRAFTABLE` | — | Accumulate ideas; finalize last |

Remaining 2 sections all `BLOCKED` — waiting on Chapters 5–6.

## Appendices

| Section | Status | Feeds from | Notes |
|---------|--------|------------|-------|
| Appendix E — Code repository | `SKELETON` | — | Repo structure description |

Remaining 4 appendices all `BLOCKED` — waiting on Phase 01–05 artifacts.
