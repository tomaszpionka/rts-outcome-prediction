Cell 1 — Front-matter (markdown)
# {Phase X / Step X.Y} — {Descriptive Title}

| Field | Value |
|-------|-------|
| Phase | {phase_id, e.g. 1} |
| Step | {step_id, e.g. 1.8} |
| Dataset | {sc2egset / aoe2companion / aoestats} |
| Game | {sc2 / aoe2} |
| Date | {YYYY-MM-DD} |
| Report artifacts | `{path/to/artifact1.csv}`, `{path/to/artifact2.md}` |
| Scientific question | {One sentence: what are we trying to learn?} |
| ROADMAP reference | `{path/to/ROADMAP.md}` Step X.Y |

Cell 2 — Imports (code)
# %% [markdown]
# ## Setup

# %%
from rts_predict.common.notebook_utils import get_notebook_db
# ... other imports from src/rts_predict/ ...

con = get_notebook_db("sc2", "sc2egset")

Cells 3–N — Query/computation pairs
Each step = code cell (con.fetch_df(query)) + markdown cell (interpretation). Every query code cell must be followed by a markdown cell within 2 cells.

Cell N+1 — Conclusion (markdown)
## Conclusion

### Artifacts produced
- `{path/to/artifact_1.csv}` — {one-line description}

### Follow-ups
- {Follow-up 1: what and where it feeds}

### Thesis mapping
- {Target section in `thesis/THESIS_STRUCTURE.md`}

Cell N+2 — Cleanup (code)
# %%
con.close()

Cell complexity rules (sandbox/notebook_config.toml):
  - [cells] max_lines = 50
  - No inline definitions (FunctionDef, AsyncFunctionDef, ClassDef) except for very simple lambdas
  - use src/rts_predict/ modules 
  - Single config location — no magic numbers in reviewer code
