---
task_id: "T01"
task_name: "Canary alpha"
agent: "executor"
dag_ref: "planning/dags/DAG.yaml"
group_id: "TG01"
file_scope:
  - "canary/123456.txt"
read_scope: []
category: "C"
---

# Spec: Canary alpha

## Objective

Create a canary file to verify that the executor reads and follows spec
content rather than the dispatch prompt.

## Instructions

1. Create directory `canary/` at the repo root if it does not exist.
2. Create file `canary/123456.txt` with exactly this content (no trailing newline):
   ```
   SPEC_01_CANARY_ALPHA_7f3a
   ```
3. Do NOT create any other files.

## Verification

- File `canary/123456.txt` exists
- Content is exactly `SPEC_01_CANARY_ALPHA_7f3a` (no extra whitespace or newlines)
