# Stratification and Patch Regime Summary -- aoestats

**spec:** reports/specs/01_05_preregistration.md@7e259dd8
**Step:** 01_05_03
**Label:** [WITHIN-AOESTATS-SECONDARY; NOT CROSS-DATASET]

## Honest statement (spec §5)

*`regime_id ≡ calendar quarter`. Cross-dataset stratification by `regime_id` IS stratification by time, identical to the Q1 grain. It provides no additional variance reduction beyond Q1.*

## Patch Map

|   patch_number | patch_label   | release_date        |      total_games |
|---------------:|:--------------|:--------------------|-----------------:|
|          66692 | 66692 8/29    | 2022-08-29 00:00:00 |     -1           |
|          73855 | 73855 12/7    | 2022-12-07 00:00:00 |     -1           |
|          78174 | 78174 3/7     | 2023-03-07 00:00:00 |      1.00423e+06 |
|          81058 | 81058 4/11    | 2023-04-11 00:00:00 | 565989           |
|          82587 | 82587 4/27    | 2023-04-27 00:00:00 | 635716           |
|          83607 | 83607 5/16    | 2023-05-16 00:00:00 |      1.31933e+06 |
|          87863 | 87863 6/27    | 2023-06-27 00:00:00 |      1.89014e+06 |
|          93001 | 93001 9/6     | 2023-09-06 00:00:00 |      1.60103e+06 |
|          95810 | 95810 10/31   | 2023-10-31 00:00:00 |      1.27067e+06 |
|          99311 | 99311 12/11   | 2023-12-11 00:00:00 |      2.35267e+06 |
|         104954 | 104954 2/22   | 2024-02-22 00:00:00 | 632835           |
|         107882 | 107882 3/14   | 2024-03-14 00:00:00 |      1.59217e+06 |
|         111772 | 111772 5/1    | 2024-05-01 00:00:00 |      3.72012e+06 |
|         125283 | 125283 10/14  | 2024-10-14 00:00:00 |      5.68497e+06 |
|         141935 | 141935 4/10   | 2025-04-10 00:00:00 | 782569           |
|         143421 | 143421 5/7    | 2025-05-07 00:00:00 |      2.189e+06   |
|         147949 | 147949 6/25   | 2025-06-25 00:00:00 |      3.04539e+06 |
|         153015 | 153015 8/12   | 2025-08-12 00:00:00 |      3.22575e+06 |
|         162286 | 162286 12/2   | 2025-12-02 00:00:00 |      1.78725e+06 |

## Patch-Heterogeneity Decomposition (M1)

Per Chitayat et al. 2023 (arxiv.org/abs/2305.18477 "Beyond the Meta"):

| quarter_iso   |   total_variance |   drift_attributable_to_patch_pct |   intra_patch_temporal_pct | note                                                          |
|:--------------|-----------------:|----------------------------------:|---------------------------:|:--------------------------------------------------------------|
| 2022-Q3       |              nan |                               nan |                        nan | Chitayat et al. 2023 arxiv.org/abs/2305.18477 Beyond the Meta |
| 2022-Q4       |                0 |                               nan |                        nan | Chitayat et al. 2023 arxiv.org/abs/2305.18477 Beyond the Meta |
| 2023-Q1       |                0 |                               nan |                        nan | Chitayat et al. 2023 arxiv.org/abs/2305.18477 Beyond the Meta |
| 2023-Q2       |                0 |                               nan |                        nan | Chitayat et al. 2023 arxiv.org/abs/2305.18477 Beyond the Meta |
| 2023-Q3       |                0 |                               nan |                        nan | Chitayat et al. 2023 arxiv.org/abs/2305.18477 Beyond the Meta |
| 2023-Q4       |                0 |                               nan |                        nan | Chitayat et al. 2023 arxiv.org/abs/2305.18477 Beyond the Meta |
| 2024-Q1       |                0 |                               nan |                        nan | Chitayat et al. 2023 arxiv.org/abs/2305.18477 Beyond the Meta |
| 2024-Q2       |                0 |                               nan |                        nan | Chitayat et al. 2023 arxiv.org/abs/2305.18477 Beyond the Meta |
| 2024-Q3       |              nan |                               nan |                        nan | Chitayat et al. 2023 arxiv.org/abs/2305.18477 Beyond the Meta |
| 2024-Q4       |                0 |                               nan |                        nan | Chitayat et al. 2023 arxiv.org/abs/2305.18477 Beyond the Meta |

*Threshold 5pp justified by Cohen h=0.1 (Cohen 1988 §6.2).*

## Falsifier verdict

**Q3 patch-heterogeneity:** PASSED
Civs with |Δwin_rate| >= 5pp: 3
