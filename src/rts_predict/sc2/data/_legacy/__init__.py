"""Legacy SC2 data code — quarantined pending Phase 01 schema validation.

These modules assume raw file schema knowledge (column names, types, JSON
structure) that has NOT been validated under the Phase 01 system. Step 01_01_01
(file inventory) only counted files — it never opened them.

When Step 01_01_02 (schema discovery) validates the schemas, this code can be
restored to the parent directory with the validation provenance chain intact.
If schemas differ from assumptions, this code must be updated to match reality.

Do NOT import from this package in active code. Imports will work but the
results are unvalidated.
"""
