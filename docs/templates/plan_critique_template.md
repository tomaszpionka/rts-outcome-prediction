---
plan_ref:           # planning/current_plan.md
created:            # ISO-8601
reviewer_model:     # e.g. claude-opus-4-6 (adversarial reviewer role)
category:           # mirrors plan category (A / B / C / D / E / F)
---

# Critique: <short title matching plan>

> Produced by reviewer-adversarial. Audience: Tomasz + viva preparation.
> Not consumed by executors or materialization.

## Invariants check

All 8 scientific invariants (`.claude/scientific-invariants.md`) assessed
below. Format: yes / no / n-a + evidence pointer.

- **#1 (per-player split)** — yes / no / n-a — <plan section or reason for n-a>
- **#2 (canonical player identifier)** — yes / no / n-a — <plan section or reason for n-a>
- **#3 (strict temporal discipline — match_time < T)** — yes / no / n-a — <plan section or reason for n-a>
- **#4 (prediction target is next game given prior history)** — yes / no / n-a — <plan section or reason for n-a>
- **#5 (symmetric player treatment)** — yes / no / n-a — <plan section or reason for n-a>
- **#6 (SQL / code shipped with findings)** — yes / no / n-a — <plan section or reason for n-a>
- **#7 (no magic numbers)** — yes / no / n-a — <plan section or reason for n-a>
- **#8 (cross-game protocol)** — yes / no / n-a — <plan section or reason for n-a>

## Temporal discipline assessment

> Required for category A and F plans. Omit (or mark n-a) for category C and E.

<For each feature computation or rolling aggregate in the plan, assess whether
`match_time < T` is strictly enforced. Identify any of these three leakage
failure modes:
  (a) rolling aggregates that include the target game's own value
  (b) head-to-head win rates that include the target game
  (c) within-tournament features that include the target game's position
Note any missing temporal leakage tests.>

## Defensibility check

<For each major choice in the plan, strongest objection + what would rebut it.>

- **Choice:** <what the plan decided>
  - **Strongest objection:** <the honest attack>
  - **Rebuttal evidence needed:** <what would close the gap>

## Likely supervisor / committee questions

<Grouped by plan section they target. Concrete questions, not vague worries.>

- On methodology:
- On data:
- On evaluation:

## Known weaknesses

<The reviewer's honest-uncertainty register. Things the plan is NOT confident
about or has left unresolved.>

## Alternatives considered and rejected

<Future-thesis gold. Each entry: alternative, reason rejected, conditions under
which it would be reconsidered.>

- **Alternative:**
  - **Rejected because:**
  - **Reconsider if:**

## Citations

<Every scientific claim in the critique must cite its source. Uncited claims
must be labeled `[OPINION]`. Use author-year format, e.g. (de Prado 2018,
Ch. 7) or (Benavoli et al. 2017).>
