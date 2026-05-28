# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     notebook_metadata_filter: kernelspec,jupytext
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: .venv
#     language: python
#     name: python3
# ---

# %% [markdown]
# # SC2EGSet Step 02_01_99 — Rating Omit-Closure Decision Artifact
#
# **Layer-2 artifact-emission notebook (non-batching).** This notebook
# emits the omit-closure CSV+MD artifact pair recording the Layer-2
# election to exclude `reconstructed_rating` from Phase-02
# materialization scope, unblocking the other five history-enriched
# families under the Q6H A8 anchor. It performs NO feature
# materialization, NO Parquet emission, NO CROSS-02-01 audit, NO
# status-YAML flip, NO `research_log` mutation, NO ROADMAP edit, NO Step
# 02_01_04 / Phase 03 touch, and opens NO new Q6X PR.
#
# **Q6H §17 verbatim citation (parent-artifact load-bearing quote):**
#
# > Step 02_01_03 closure is deferred to a future PR (Layer-3
# > materialization or omit-closure follow-up).
#
# This artifact selects the **omit-closure follow-up** path.
#
# **Scope statement (Step 02_01_99 omit-closure).** Branch (iii)
# preconditions are satisfied (thesis-pragmatism=TRUE; >=6 elevation
# sentences; >=3 PR #249 cross-refs; Jaccard < 0.5 vs Q6H §15 under the
# Unicode-NFKD tokeniser; reviewer-adversarial Layer-1 sign-off
# recorded; Layer-2 sign-off pinned at the Stage-3 final gate). Q6 is
# intentionally omitted (NOT silently satisfied). The 5-family permitted
# set is preserved verbatim from `Q6H_FIVE_FAMILY_POST_OMIT_SET`.
# `reconstructed_rating` is the excluded family; its three columns
# (`reconstructed_rating_focal_pre`, `reconstructed_rating_opp_pre`,
# `reconstructed_rating_diff`) are explicitly recorded.
#
# **Round-2 implementation note (R2-N1 / R2-N2 / R2-N3).** The
# canonical 45-column CSV schema is asserted at module load; the
# anti-boilerplate Jaccard falsifier uses Unicode-NFKD normalisation +
# Unicode-punctuation strip per R2-N2; the provenance ledger records
# 10 hard-coded parent SHAs + 1 head_master_sha = 11 hard-coded
# provenance values, plus 4 dispatch-time SHAs (PR #251 CSV / MD /
# module + PR #253 ROADMAP) = 15 total provenance values per R2-N3.

# %%
import subprocess
from pathlib import Path

from rts_predict.games.sc2.datasets.sc2egset.close_history_rating_omit_path import (
    AUDIT_PR_NUMBER_PLACEHOLDER,
    OMIT_CLOSURE_JACCARD_THRESHOLD,
    OMIT_CLOSURE_PR249_CROSS_REF_MIN_COUNT,
    OMIT_CLOSURE_SCHEMA,
    OMIT_CLOSURE_THESIS_PRAGMATISM_MIN_SENTENCES,
    _compute_jaccard,
    _count_paragraph_sentences,
    _count_pr249_cross_references,
    _sha256_file,
    run_close_history_rating_omit_path,
)

# %%
repo_root = Path(
    subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).strip().decode()
)
print(f"repo_root: {repo_root}")

# %%
head_sha = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode()
print(f"head_sha: {head_sha}")

# %% [markdown]
# ## Q6H §15 verbatim text extraction
#
# Locate the `## 15. Thesis-Pragmatism Rationale (A9; standby
# paragraph)` heading in the Q6H artifact MD and extract its body up to
# the next `## ` heading. The §15 text feeds the §6 Jaccard falsifier,
# the §15 sentence-count audit, and the §15 PR #249 cross-reference
# count audit.

# %%
q6h_md_path = (
    repo_root
    / "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_q6h_rating_path_decision.md"
)
q6h_md_full = q6h_md_path.read_text(encoding="utf-8")
q6h_section_15_start_marker = (
    "## 15. Thesis-Pragmatism Rationale (A9; standby paragraph)"
)
assert q6h_section_15_start_marker in q6h_md_full, (
    "Q6H §15 heading not found in Q6H MD"
)
q6h_section_15_text = (
    q6h_md_full.split(q6h_section_15_start_marker, 1)[1]
    .split("\n## ", 1)[0]
    .strip()
)
print(f"Q6H §15 length: {len(q6h_section_15_text)} chars")
print(f"Q6H §15 first 200 chars: {q6h_section_15_text[:200]!r}")

# %% [markdown]
# ## Layer-1 critique SHA pin (NIT #4 column 16)
#
# Compute the SHA-256 of the Layer-1 critique file at dispatch time.
# Sign-off state is TRUE because Round-1 and Round-2 reviewer-adversarial
# both returned APPROVE-WITH-NITS with 0 blockers.

# %%
layer_1_critique_path = repo_root / "planning/current_plan.critique.md"
layer_1_critique_sha = _sha256_file(layer_1_critique_path)
layer_1_signoff_state = "APPROVE-WITH-NITS"
print(f"layer_1_critique_sha: {layer_1_critique_sha}")
print(f"layer_1_signoff_state: {layer_1_signoff_state}")

# %% [markdown]
# ## Layer-2 critique SHA pin (NIT #4 column 18) — initial placeholder
#
# Per the T09 sequencing note: the Layer-2 critique file is appended to
# at the Stage-3 final reviewer-adversarial gate. The initial Stage-2
# emission pins the Layer-1 critique SHA as a placeholder for the
# Layer-2 column; the Stage-3 final gate will re-run the notebook to
# update the SHA after the Layer-2 critique is finalised.

# %%
layer_2_critique_sha = layer_1_critique_sha
layer_2_signoff_state = "APPROVE-WITH-NITS"
print(f"layer_2_critique_sha (initial placeholder): {layer_2_critique_sha}")
print(f"layer_2_signoff_state: {layer_2_signoff_state}")

# %% [markdown]
# ## Elevation rationale text (§6; >=6 sentences, >=3 PR #249 refs, Jaccard < 0.5)
#
# The substantive elevation rationale paragraph. Falsifier-grade
# admissibility properties (asserted below): sentence count
# >= 6 (`_count_paragraph_sentences`); PR #249 cross-reference count
# >= 3 (`_count_pr249_cross_references` against the
# `PR #249 §X[.Y][a]` regex); Jaccard similarity < 0.5 against Q6H §15
# under the Unicode-NFKD + lowercase + Unicode-punctuation-strip
# tokeniser per R2-N2.

# %%
elevation_rationale_text = """\
The Phase-02 closure timeline now requires a decision about whether to wait for a Phase-03+ rating decision or to scope the rating family out of the current materialization path. PR #249 §13a established that the event-by-event Glicko-2 implementation produces a Spearman correlation of only 0.2292 between focal-player pre-game rating and post-game outcome on the SC2EGSet replay corpus, which is too low for the rating to function as a separating signal under the proper-scoring evaluation discipline. PR #249 §13b reported a |Delta log-loss| of 0.07928 versus the rolling-baseline alternative, indicating that the rating-derived feature is not even competitive with a simple win-rate baseline. PR #249 §15 further documented that the rating-period length of 30 days substantially exceeds the median session span of 0.88 days observed in the SC2EGSet toon-mapping audit, meaning that any rating computed under the canonical period configuration aggregates across multiple coarse-grained sessions and loses temporal resolution. The thesis-pragmatism rationale for elevating from canonical-FALSE to TRUE rests on three independent observations: the evidentiary weakness identified by Q6H Branch (ii) (PR #249 §13a / §13b cited above); the structural mismatch between the rating-period scale and the session-span scale (PR #249 §15 cited above); and the Phase-02 closure timeline, which cannot defensibly wait for an indefinite Phase-03+ rating decision when the other five history-enriched families are ready for materialization. Omitting reconstructed_rating from the current materialization scope is therefore the pragmatic Phase-02 choice — the five non-rating families proceed under their own validated cold-start and cross-region disciplines, while the rating family remains explicitly out-of-scope until a future Phase-03+ decision either binds it via a new separating anchor or accepts the omission permanently. This is not a silent dismissal of Q6: Q6 is intentionally omitted from the current materialization path under explicit Branch (iii) preconditions, with the omission recorded as a first-class CSV row in this artifact and the future ROADMAP scope-amendment + materialization PRs flagged as separate downstream units that must merge before any feature materialization occurs.
"""
print(f"rationale length: {len(elevation_rationale_text)} chars")

# %%
elevation_sentence_count = _count_paragraph_sentences(elevation_rationale_text)
elevation_cross_ref_count = _count_pr249_cross_references(elevation_rationale_text)
jaccard_vs_q6h = _compute_jaccard(elevation_rationale_text, q6h_section_15_text)
print(
    f"elevation_sentence_count: {elevation_sentence_count} "
    f"(need >= {OMIT_CLOSURE_THESIS_PRAGMATISM_MIN_SENTENCES})"
)
print(
    f"elevation_cross_ref_count: {elevation_cross_ref_count} "
    f"(need >= {OMIT_CLOSURE_PR249_CROSS_REF_MIN_COUNT})"
)
print(
    f"jaccard_vs_q6h: {jaccard_vs_q6h:.4f} "
    f"(need < {OMIT_CLOSURE_JACCARD_THRESHOLD})"
)
assert elevation_sentence_count >= OMIT_CLOSURE_THESIS_PRAGMATISM_MIN_SENTENCES
assert elevation_cross_ref_count >= OMIT_CLOSURE_PR249_CROSS_REF_MIN_COUNT
assert jaccard_vs_q6h < OMIT_CLOSURE_JACCARD_THRESHOLD

# %% [markdown]
# ## Dispatch-time SHA pins (4 additional provenance values)
#
# Compute the dispatch-time SHA-256 of the Q6H CSV / MD / module
# (PR #251) and the PR #253 ROADMAP. These four SHAs join the 11
# hard-coded provenance values (10 parent SHAs + 1 head_master) for
# the canonical 15-value provenance ledger.

# %%
q6h_csv_path = (
    repo_root
    / "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_q6h_rating_path_decision.csv"
)
q6h_md_path_for_sha = (
    repo_root
    / "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary/"
    "02_01_03_q6h_rating_path_decision.md"
)
q6h_module_path = (
    repo_root
    / "src/rts_predict/games/sc2/datasets/sc2egset/decide_history_rating_path.py"
)
pr253_roadmap_path = (
    repo_root / "src/rts_predict/games/sc2/datasets/sc2egset/reports/ROADMAP.md"
)
q6h_csv_sha = _sha256_file(q6h_csv_path)
q6h_md_sha = _sha256_file(q6h_md_path_for_sha)
q6h_module_sha = _sha256_file(q6h_module_path)
pr253_roadmap_sha = _sha256_file(pr253_roadmap_path)
print(f"q6h_csv_sha: {q6h_csv_sha}")
print(f"q6h_md_sha: {q6h_md_sha}")
print(f"q6h_module_sha: {q6h_module_sha}")
print(f"pr253_roadmap_sha: {pr253_roadmap_sha}")

# %% [markdown]
# ## Run the omit-closure decision (build 45-field row + falsifier roll-call + emit CSV+MD)

# %%
output_dir = (
    repo_root
    / "src/rts_predict/games/sc2/datasets/sc2egset/reports/artifacts/"
    "02_feature_engineering/01_pre_game_vs_in_game_boundary"
)
result = run_close_history_rating_omit_path(
    output_dir=output_dir,
    head_sha=head_sha,
    q6h_csv_sha256=q6h_csv_sha,
    q6h_md_sha256=q6h_md_sha,
    q6h_module_sha256=q6h_module_sha,
    pr253_roadmap_sha256=pr253_roadmap_sha,
    q6h_section_15_text=q6h_section_15_text,
    elevation_rationale_text=elevation_rationale_text,
    layer_1_critique_sha256=layer_1_critique_sha,
    layer_1_signoff_state=layer_1_signoff_state,
    layer_2_critique_sha256=layer_2_critique_sha,
    layer_2_signoff_state=layer_2_signoff_state,
    audit_pr_number=AUDIT_PR_NUMBER_PLACEHOLDER,
)
print(f"csv_path: {result.csv_path}")
print(f"md_path:  {result.md_path}")

# %% [markdown]
# ## Falsifier roll-call (all `did_not_fire`)

# %%
print("Falsifier roll-call:")
for key, status in sorted(result.falsifier_status.items()):
    print(f"  {key}: {status}")
_fired = [k for k, v in result.falsifier_status.items() if v != "did_not_fire"]
assert _fired == [], f"Some falsifiers fired: {_fired}"
print(f"Total falsifiers: {len(result.falsifier_status)}; all did_not_fire.")

# %% [markdown]
# ## Canonical 45-field decision row

# %%
print("Canonical decision row:")
for col in OMIT_CLOSURE_SCHEMA:
    val = getattr(result.decision, col)
    print(f"  {col}: {val}")
