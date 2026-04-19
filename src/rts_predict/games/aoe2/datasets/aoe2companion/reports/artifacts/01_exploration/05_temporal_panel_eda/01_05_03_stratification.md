# 01_05_03 Stratification — aoe2companion

spec: reports/specs/01_05_preregistration.md@7e259dd8

## regime_id ≡ calendar quarter

Per spec §3, the cross-dataset `regime_id ≡ calendar quarter` identity is preserved.
The secondary-regime analysis below is `[WITHIN-AOEC-SECONDARY; NOT CROSS-DATASET]`.

## M-02 Deviation Note (pre-authorized)

Spec §5 names `rm_1v1 / rm_team` as the secondary leaderboard regime for aoec.
`rm_team` is out-of-analytical-scope per 01_04_01 R01 (non-1v1 matches excluded from primary substrate).
Secondary regime is implemented as `rm_1v1 (lb=6) vs qp_rm_1v1 (lb=18)`.
Research log records: "secondary regime analysis rm_1v1/qp_rm_1v1 is scope-stratification, not ladder-segmentation."

## Results

Max |PSI(lb=6) - PSI(lb=18)| for faction: **0.1345**

Verdict: **confirmed**

## SQL

```sql

SELECT m.internalLeaderboardId AS lb, mhm.faction, COUNT(*) AS cnt
FROM matches_history_minimal mhm
JOIN matches_1v1_clean m
  ON m.matchId = CAST(REPLACE(mhm.match_id, 'aoe2companion::', '') AS INTEGER)
 AND CAST(m.profileId AS VARCHAR) = mhm.player_id
WHERE mhm.started_at >= TIMESTAMP '2022-08-29'
  AND mhm.started_at <  TIMESTAMP '2023-01-01'
  AND m.is_null_cluster = FALSE
  AND m.internalLeaderboardId IN (6, 18)
GROUP BY lb, faction

```

_conditional on >=10 matches in reference period; see §6 for sensitivity_
_[WITHIN-AOEC-SECONDARY; NOT CROSS-DATASET]_
