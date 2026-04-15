# Adversarial Critique — plan_aoestats_01_02_05.md

**Verdict: REVISE BEFORE EXECUTION**

Plan reviewed against: OLD plan from 19:46 (before planner comprehensive revision).
Note: planner revision (from completion at 20:30) addresses BLOCKER #1, #2 and WARNING #3, #4, #5, #6.
Remaining open issues noted below.

---

## BLOCKER — Already addressed by planner revision

### B1: T06 duration SQL unit mismatch
Plan had `FLOOR(duration / 1e9 / 60) * 60` producing bins in SECONDS while comment said "minutes."
**Planner fix:** `FLOOR(duration / 1e9 / 60) AS minute_bin` with dual-panel design.

### B2: T07 ELO sentinel annotation formula nonsensical
Plan derived sentinel count as `n_null - sentinel_count = 0 - 34 = -34`.
**Planner fix:** Read directly from `census["elo_sentinel_counts"]["team_0_elo_negative"]` (=34).

---

## WARNING — Already addressed by planner revision

### W3: "range 0-3500" magic number (Invariant #7 violation)
Actual max across all ELO/old_rating columns is 3045, not 3500.
**Planner fix:** Updated to 3045, with 3045/25 = ~122 bins derivation.

### W4: T08 age uptime bin widths uniform at 20s
Feudal p95=963s, castle p95=1752s, imperial p95=2933s — 20s uniform is wrong for all.
**Planner fix:** Variable bin widths: feudal=10s, castle=20s, imperial=30s (~42-43 bins each).

### W5: Predecessor 01_02_04 not in STEP_STATUS.yaml
**Planner fix:** T01 now adds 01_02_04 (complete) and 01_02_05 (not_started) to STEP_STATUS.

### W6: Duration log y-axis alone insufficient for skewness=1032
Single log-y histogram with median/max 2000x ratio produces unreadable body.
**Planner fix:** Dual-panel: left=linear body clipped at 120min, right=full range log-y.

---

## REMAINING OPEN ISSUES (not addressed by planner revision)

### W7 (was NOTE #9): Verification cell should assert, not just print monthly count
`assert len(monthly_df) == census["temporal_range"]["distinct_months"]` is more rigorous than just printing.

### N1 (NOTE #10): Missing explicit figsize on several plots
T03 (winner), T05 (leaderboard), T09 (opening), T10 (outlier), T11 (NULL rate) lack figsize specs.

### N2 (NOTE #11): `plt.close()` not specified after each figure
With 13 figures, memory accumulation is a risk on the 45GB database session.

---

## Key statistics verified from JSON artifact

- duration: skewness=1032.64, kurtosis=2,808,034, max=5,574,815s (64 days), median=2619.7s
- ELO: range 0-3045, sentinels: team_0_elo=-1.0 (N=34), team_1_elo=-1.0 (N=39)
- opening: 86.05% NULL, 15,011,294 non-NULL rows
- num_players: 60.6% 2p, 16.5% 4p, 8.9% 6p, 14.0% 8p
- match_rating_diff: skew=0.0, kurtosis=65.68, range [-2185, +2185]
