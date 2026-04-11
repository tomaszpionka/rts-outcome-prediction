# Steps

**Terminology source:** [`docs/TAXONOMY.md`](../TAXONOMY.md) — Step definition at §Step (~line 81).
**Schema source:** [`docs/templates/step_template.yaml`](../templates/step_template.yaml).

---

## What a Step is

A Step is the atomic leaf unit of work in the project hierarchy, nested below
a Pipeline Section, which is nested below a Phase:

```
Phase             NN
  Pipeline Section  NN_NN
    Step              NN_NN_NN
```

A Step that produces no artifact is not a Step — it is a Chore or a Refactor.

---

## Numbering convention

Steps are numbered `NN_NN_NN` — three zero-padded two-digit components:

```
NN_NN_NN
│  │  └─ Step index within the Pipeline Section
│  └──── Pipeline Section index within the Phase
└─────── Phase index
```

The numeric prefix is the canonical identifier used in cross-links and tooling.
The slug appended to file names (e.g., `NN_NN_NN_<slug>.py`) is for
human browse-ability only and does not change once chosen. Cross-section
dependencies must be declared explicitly via the `predecessors` field.

---

## Step contract

Every Step must produce all three outputs before it is considered complete:

1. **One sandbox notebook pair** — both the jupytext `.py` source and the
   paired `.ipynb` with committed outputs, at the canonical path under
   `sandbox/<game>/<dataset>/`.

2. **One or more artifacts** — files under
   `src/rts_predict/<game>/reports/<dataset>/artifacts/`, mirroring the Phase
   and Pipeline Section directory structure of the notebook.

3. **One research log entry** — in `reports/research_log.md`, summarising the
   Step's findings and linking back to the Step ID.

A Step is incomplete if any of these three outputs is missing.

---

## Step schema

Each Step is defined as a fenced YAML block inside a dataset ROADMAP file.
The full schema is in [`docs/templates/step_template.yaml`](../templates/step_template.yaml).

Required field groups:

| Group | Fields |
|---|---|
| Identity | `step_number`, `name`, `description` |
| Hierarchy context | `phase`, `pipeline_section`, `manual_reference`, `dataset` |
| Scientific purpose | `question`, `method`, `stratification` |
| Inputs / outputs | `notebook_path`, `inputs.duckdb_tables`, `outputs.data_artifacts`, `outputs.report` |
| Reproducibility | `reproducibility`, `scientific_invariants_applied` |
| Gate | `gate.artifact_check`, `gate.continue_predicate`, `gate.halt_predicate` |
| Traceability | `thesis_mapping`, `research_log_entry` |

Optional fields are omitted entirely rather than left as empty strings.
Do not add new fields without updating `docs/templates/step_template.yaml` first.

---

## Directory layout

Two mirrored trees reflect the hierarchy. Directories use `NN_<slug>` names.

**Sandbox notebooks:**
```
sandbox/<game>/<dataset>/NN_<phase-slug>/NN_<section-slug>/
  NN_NN_NN_<step-slug>.py      jupytext source
  NN_NN_NN_<step-slug>.ipynb   paired notebook (carries outputs)
```

**Report artifacts:**
```
src/rts_predict/<game>/reports/<dataset>/artifacts/NN_<phase-slug>/NN_<section-slug>/
  NN_NN_NN_<descriptive-name>.csv
  NN_NN_NN_<descriptive-name>.md
```

The mirroring rule: when a notebook runs, its artifacts land in the
corresponding `artifacts/` subdirectory. This is enforced by notebook helpers
in `rts_predict.common`, not by convention alone.

---

## Ownership

Steps live inside dataset ROADMAPs at
`src/rts_predict/<game>/reports/<dataset>/ROADMAP.md`.

A ROADMAP implements the Pipeline Sections from [`docs/PHASES.md`](../PHASES.md)
by decomposing each into executable Steps. It does not invent, rename, or omit
Pipeline Sections. Step definitions across datasets are independent even when
they share the same Step number — each is scoped to its own dataset.
