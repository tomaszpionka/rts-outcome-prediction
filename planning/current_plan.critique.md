# Adversarial Review — Plan 01_02_02 DuckDB Ingestion

**Date:** 2026-04-13
**Reviewer:** reviewer-adversarial (claude-opus-4-6)
**Verdict:** REDESIGN (2 blockers, 5 warnings, 2 notes)

---

## Blockers

### B1. Old DAG/specs target 01_02_01, not 01_02_02

The plan correctly targets step 01_02_02, but the materialized `DAG.yaml`
and `specs/` still reference the old 01_02_01 step. These must be
regenerated before execution. (Expected — materialization hasn't happened yet.)

### B2. T03 and T04 describe work already done

- **T03** says "add binary_as_string=true to aoe2companion pre_ingestion.py"
  — but it's already there on lines 31, 66, 75, 174.
- **T04** says "add load_raw_overview to aoestats pre_ingestion.py" — but
  `ingest_overviews_raw()` already exists at line 204.

These tasks are no-ops. Remove them or rewrite to describe actual deltas.

---

## Warnings

### W1. replay_id hash function unspecified

Plan says "hash of filename" but doesn't specify which hash (MD5? SHA256?
Python hash()?). `replay_id` is the join key between `replays_meta` and
`replay_players` — must be deterministic and documented. Python's `hash()`
varies across processes (PYTHONHASHSEED). Recommend: SHA-256 truncated
to 16 hex chars, matching the existing filename hash pattern.

### W2. ToonPlayerDescMap field list is approximate

Plan says "~23 per-player fields" but the exact list depends on era.
The 01_02_01 section 8c reads fields from a single sample file. If
field sets vary across 2016-2024 replays, the normalisation function
must handle varying schemas. This risk is unquantified.

### W3. Event Parquet extraction feasibility unconfirmed

Storage estimate depends on 01_02_01 re-execution (which hasn't happened).
Plan should specify fallback: if SSD space insufficient, extract only
trackerEvents (smallest, most prediction-relevant) or defer entirely.

### W4. Existing ingestion.py modules (legacy) not addressed

Both AoE2 datasets have `ingestion.py` AND `pre_ingestion.py` with
different table naming conventions (`raw_matches` vs `matches_raw`).
Plan must either deprecate legacy ingestion.py or reconcile naming.

### W5. SC2 ToonPlayerDescMap normalisation lacks era-stability check

Different replay eras (2016 vs 2024) may have different player fields
in ToonPlayerDescMap. The plan does not verify this or specify how
union_by_name normalisation handles missing fields.

---

## Notes

### N1. Gate conditions don't verify event Parquet output

Gate condition 4 checks ingestion.py exists but not that
extract_events_to_parquet produces valid output. Add: "Parquet event
files exist in output directory with non-zero size."

### N2. Cross-game module structure asymmetry

After this plan, SC2 has pre_ingestion.py + ingestion.py (new).
AoE2 has pre_ingestion.py (dual-purpose) + ingestion.py (legacy).
Not a problem, but should be documented as a design decision.

---

## Recommended Fixes Before Materialization

1. **Remove T03 and T04** — work is already done. If any actual delta
   remains (e.g., updating tests), rewrite to describe only the delta.
2. **Specify replay_id** as SHA-256 of filename stem, truncated to 16 hex.
3. **Add SSD fallback** for event extraction: if median estimate > available
   space, extract trackerEvents only.
4. **Add event Parquet to gate conditions.**
5. **Document the ingestion.py vs pre_ingestion.py situation** — either
   deprecate legacy ingestion.py or reconcile. This can be a separate
   chore, not part of this plan.
6. **Regenerate DAG + specs** targeting 01_02_02 (standard materialization).
