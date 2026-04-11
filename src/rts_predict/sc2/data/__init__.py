"""SC2 data pipeline — Phase 01 minimal subset.

Submodules:
    processing  — raw_enriched view creation (filesystem-derived columns only).

Legacy modules (ingestion, exploration, audit, schemas) were deleted in v2.1.0.
They assumed raw file schema knowledge not validated under the Phase 01 system.
Phase 01 Step 01_01_02 (schema discovery) will produce validated replacements.
"""
