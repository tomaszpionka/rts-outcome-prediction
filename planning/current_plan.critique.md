---
verdict: REVISE_BEFORE_EXECUTION
plan_reviewed: planning/current_plan.md
revision_reviewed: 1
reviewer_model: claude-opus-4-7[1m]
date: 2026-04-17
findings:
  - id: BLOCKER-1
    severity: BLOCKER
    title: "T04 'Fixed:' entry is fictitious — no observable bug exists in per_view_target_cols.player_history_all"
    description: |
      Aoestats line 1096 defines `_target_cols_ph: set = {"winner"}`; line 1568
      hardcodes `"player_history_all": ["winner"]`. `list(_target_cols_ph)` evaluates
      to `["winner"]` — IDENTICAL to the hardcoded literal. There is no surfaced bug.
      T04 step 5 introduces unnecessary churn and T06 step 4's CHANGELOG entry
      claims a "(pre-existing bug surfaced during refactor)" which is false. Same
      situation for matches_1v1_clean (line 1567 vs line 990).
      Required fix: EITHER drop T04 step 5 entirely (and remove the corresponding
      "Fixed:" CHANGELOG line in T06), OR keep the dynamicization but reclassify
      under "Changed:" with honest framing ("Defensive: derive
      per_view_target_cols.* from runtime _target_cols_* sets to prevent future
      drift"). Do NOT use "Fixed" or "bug" for a value identical to its hardcoded
      counterpart.
    investigated: "Concern 4 (pre-existing bug fix in T04)"

  - id: WARNING-1
    severity: WARNING
    title: "T05 step 3 instruction does not match aoec's actual call style"
    description: |
      sc2 and aoestats call `_detect_constants` with 3 positional args. aoec uses
      keyword `identity_cols=`: `_detect_constants(_VIEW_M1, list(_dtype_m1.keys()),
      identity_cols=_IDENTITY_COLS_M1)` (lines 1165, 1245). T05 step 3 instructs
      "con becomes 3rd positional, identity_cols 4th" — semantically still works
      via either positional or keyword form. Suggested: append note to T05 step 3
      explaining either form is acceptable; pick one consistently for aoec.
    investigated: "Concern 2 (API contract change)"

  - id: WARNING-2
    severity: WARNING
    title: "Aoec JSON shape change extends beyond W2: n_cols silently renamed to columns_audited"
    description: |
      aoec line 1763-1772 currently uses `"n_cols": len(df_ledger_m1)`. The new
      `build_audit_views_block` returns `{"columns_audited": int}`. Field rename is
      a side-effect of W2 canonicalization that any downstream consumer or thesis
      text referencing `n_cols` would silently break on. Plan gate condition #6
      enumerates removed top-level keys but does NOT call out the field rename.
      Required fix: add explicit CHANGELOG bullet "aoec inline missingness_audit
      .<view>.n_cols field renamed to views.<view>.columns_audited as part of W2
      canonicalization."
    investigated: "Concern 3 (W2 JSON shape gate)"

  - id: WARNING-3
    severity: WARNING
    title: "T02 coverage gap — zero-missingness no-spec branch + empty build_audit_views_block input not explicitly tested"
    description: |
      `_consolidate_ledger`'s `n_total_missing == 0` branch has 2 sub-cases:
      (a) `spec_entry is not None` — covered by T02 #8.
      (b) `spec_entry is None` — NOT explicitly tested. Branch coverage may not
      reach 100% without a fixture column with zero NULLs/sentinels and absent
      from spec dict.
      Also: `build_audit_views_block({})` empty input not tested.
      Required fix: add to T02 #8: "Zero-missingness for column NOT in spec →
      mechanism='N/A', recommendation='RETAIN_AS_IS', carries_sem=False,
      is_primary=False". Add to T02 #9: "Empty view_ledgers dict → {'views': {}}".
    investigated: "Concern 5 (test coverage completeness)"

  - id: NOTE-1
    severity: NOTE
    title: "T05 step 4 uses string literals while T03/T04 use variables — minor inconsistency"
    description: |
      T03/T04 use `_view_mfc`/`_view_hist`/`_view_m1`/`_view_ph`. T05 step 4 uses
      string literals "matches_1v1_clean" / "player_history_all" despite `_VIEW_M1`
      and `_VIEW_PH` existing in the aoec notebook. Cosmetic inconsistency. Suggest
      unifying to `{_VIEW_M1: ..., _VIEW_PH: ...}` for aoec.
    investigated: "Concern 2 (API contract change)"

  - id: NOTE-2
    severity: NOTE
    title: "Plan claim 'sc2 body identical to aoestats' is approximately true but understates differences"
    description: |
      Bodies are SEMANTICALLY equivalent. Differences: aoestats `_consolidate_ledger`
      uses intermediate variable `col_field`; sc2 uses inline `nrow["column_name"]
      if "column_name" in nrow else nrow["column"]`. sc2 has try/except guard
      around `con.execute` in `_sentinel_census`; aoestats does not. Plan correctly
      handles both (adopt aoestats body + add try/except) — wording could be
      tightened to "use aoestats body as base; merge in sc2's try/except guard"
      to avoid implying byte-equivalence where there is only semantic equivalence.
    investigated: "Concern 1 (backward compatibility)"

verified_correct:
  - "sc2egset already has canonical views.<view_name>: shape (lines 1976-1987) — T03 W2 work IS a no-op as planned"
  - "aoestats inline pattern is flat ledger_<view_name> keys (lines 1572-1573) — W2 fix is needed and correctly described"
  - "aoec inline pattern is direct top-level keys <view_name>: (lines 1763, 1768) — W2 fix is needed and correctly described"
  - "All 5 helper bodies in sc2/aoestats are semantically equivalent (text differs but logic identical); aoec _recommend IS demonstrably contracted (missing 'Listwise deletion' and 'Phase 02 conditional imputation' tail sentences) — Q2 acceptance is well-targeted"
  - "All variables referenced by T03/T04/T05 (_view_mfc, _total_mfc_rows, df_ledger_*, _view_m1/_VIEW_M1, etc.) exist in scope at the artifact-write cells of all three notebooks"
  - "_recommend has 8 reachable code paths; T02's 8 listed tests cover every path"
  - "True-constant + target conflict (test #9) is structurally trivial: B4 gate requires n_total_missing > 0 which a true constant cannot satisfy"
  - "CHANGELOG.md [3.10.3] block (line 22) exists, is populated with audit work, [Unreleased] (line 12) is empty — T06 'append to [3.10.3]' strategy is correct"
  - "df_null schema heterogeneity handled by aoestats's col_field lookup pattern that the plan adopts as canonical"
  - "_consolidate_ledger output schema = 17 columns confirmed; test 'exactly 17 columns' is implementable"
  - "All file paths in T03/T04/T05 file_scope sections exist on disk"

locked_decisions_check:
  user_Q1_stay_3_10_3: pass
  user_Q2_accept_aoec_text_delta: pass
  user_Q3_build_audit_views_returns_views_dict: pass
---

# Adversarial Review — NOTE-3+W2 Refactor Plan

## Verdict: REVISE_BEFORE_EXECUTION

Single blocker: BLOCKER-1 puts a fictitious "Fixed:" bug into the public CHANGELOG. Three warnings (WARNING-1/2/3) are non-blocking but should be tightened to minimize executor ambiguity and to honestly catalog the W2 canonicalization side-effects. Two NOTEs are cosmetic.

Once BLOCKER-1 is addressed, the refactor itself — extracting 5 functions, adding 1 public helper, normalizing W2 JSON shape, accepting the canonical `_recommend` text — is methodologically sound for a Category B refactor. The byte-identical-CSV claims for sc2egset and aoestats are sustained by direct inspection; aoec's `recommendation` column will indeed be byte-identical and `recommendation_justification` will differ exactly as Q2 anticipates.

## Path to APPROVE

1. **BLOCKER-1:** drop T04 step 5 + remove the corresponding T06 CHANGELOG "Fixed:" line. (Cleanest.) OR reclassify as "Changed: defensive dynamicization" — your call.
2. **WARNING-1:** append clarification to T05 step 3 about aoec's keyword-arg call style.
3. **WARNING-2:** add explicit CHANGELOG bullet documenting the `n_cols` → `columns_audited` rename.
4. **WARNING-3:** add 2 test cases to T02 (zero-missingness no-spec branch + empty build_audit_views_block input).
5. **NOTE-1:** unify T05 step 4 to use `_VIEW_M1`/`_VIEW_PH` variables for consistency with T03/T04.
6. **NOTE-2:** reword T01 step 2 intro to acknowledge sc2/aoestats bodies are semantically (not byte-) equivalent.

## Reproducibility note

This review verified ground truth by direct file reads against all 3 notebooks at the relevant line ranges. All claims about line numbers and variable scopes are inspectable.
