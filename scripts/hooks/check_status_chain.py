#!/usr/bin/env python3
"""Pre-commit hook: validate Tier 7 status chain consistency.

When any STEP_STATUS.yaml, PIPELINE_SECTION_STATUS.yaml, or PHASE_STATUS.yaml
is staged, checks that the three files in each dataset's chain are mutually
consistent. Flags drift without attempting to auto-fix — the executor must
regenerate.

Derivation rules (from each file's header comments):
  Pipeline section status:
    complete    = ALL its steps are complete
    in_progress = ANY step is in_progress or complete
    not_started = NO step has started

  Phase status:
    complete    = ALL its pipeline sections are complete
    in_progress = ANY pipeline section is in_progress or complete
    not_started = NO pipeline section has started

Exit codes:
    0 — consistent (or no status files staged)
    1 — drift detected
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml  # PyYAML — project dependency

ROOT = Path(__file__).resolve().parents[2]

STATUS_GLOB = "src/rts_predict/games/*/datasets/*/reports"


# ---------------------------------------------------------------------------
# Per-dataset validation
# ---------------------------------------------------------------------------


def check_dataset(reports_dir: Path) -> list[str]:
    """Check one dataset's reports/ directory. Returns list of error messages.

    STEP_STATUS only contains *started* steps — future steps are added
    incrementally. This means we cannot derive a definitive "complete" status
    from STEP_STATUS alone (more steps may be pending). We only check for
    definitive contradictions:

      - section/phase says "not_started" but upstream has started entries
      - section/phase says "complete"    but upstream has incomplete entries

    "in_progress" in the lower tier is never a contradiction — it's consistent
    with having pending steps/sections not yet in the source file.
    """
    errors: list[str] = []

    step_f = reports_dir / "STEP_STATUS.yaml"
    section_f = reports_dir / "PIPELINE_SECTION_STATUS.yaml"
    phase_f = reports_dir / "PHASE_STATUS.yaml"

    if not (step_f.exists() and section_f.exists() and phase_f.exists()):
        return []  # incomplete chain — nothing to validate

    try:
        step_data = yaml.safe_load(step_f.read_text())
        section_data = yaml.safe_load(section_f.read_text())
        phase_data = yaml.safe_load(phase_f.read_text())
    except yaml.YAMLError as exc:
        return [f"{reports_dir}: YAML parse error — {exc}"]

    steps: dict = step_data.get("steps", {}) or {}
    sections: dict = section_data.get("pipeline_sections", {}) or {}
    phases: dict = phase_data.get("phases", {}) or {}

    label = reports_dir.relative_to(ROOT)

    # ── Steps → Section contradictions ───────────────────────────────────
    # Group step statuses by section
    section_step_statuses: dict[str, list[str]] = {}
    for _step_id, step_info in steps.items():
        sec_id = step_info.get("pipeline_section", "")
        status = step_info.get("status", "not_started")
        section_step_statuses.setdefault(sec_id, []).append(status)

    for sec_id, sec_info in sections.items():
        recorded = sec_info.get("status", "not_started")
        step_statuses = section_step_statuses.get(sec_id, [])

        if recorded == "not_started" and any(
            s in ("complete", "in_progress") for s in step_statuses
        ):
            errors.append(
                f"{label}/PIPELINE_SECTION_STATUS.yaml: "
                f"section {sec_id!r} is 'not_started' but STEP_STATUS "
                f"has started steps for it {step_statuses}"
            )
        elif recorded == "complete" and any(
            s != "complete" for s in step_statuses
        ):
            errors.append(
                f"{label}/PIPELINE_SECTION_STATUS.yaml: "
                f"section {sec_id!r} is 'complete' but STEP_STATUS "
                f"has incomplete steps {step_statuses}"
            )

    # ── Sections → Phase contradictions ──────────────────────────────────
    phase_section_statuses: dict[str, list[str]] = {}
    for sec_id, sec_info in sections.items():
        phase_id = sec_info.get("phase", "")
        status = sec_info.get("status", "not_started")
        phase_section_statuses.setdefault(phase_id, []).append(status)

    for phase_id, phase_info in phases.items():
        recorded = phase_info.get("status", "not_started")
        sec_statuses = phase_section_statuses.get(phase_id, [])

        if recorded == "not_started" and any(
            s in ("complete", "in_progress") for s in sec_statuses
        ):
            errors.append(
                f"{label}/PHASE_STATUS.yaml: "
                f"phase {phase_id!r} is 'not_started' but "
                f"PIPELINE_SECTION_STATUS has started sections {sec_statuses}"
            )
        elif recorded == "complete" and any(
            s != "complete" for s in sec_statuses
        ):
            errors.append(
                f"{label}/PHASE_STATUS.yaml: "
                f"phase {phase_id!r} is 'complete' but "
                f"PIPELINE_SECTION_STATUS has incomplete sections {sec_statuses}"
            )

    return errors


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    all_errors: list[str] = []

    for reports_dir in sorted(ROOT.glob(STATUS_GLOB)):
        if not reports_dir.is_dir():
            continue
        all_errors.extend(check_dataset(reports_dir))

    if all_errors:
        print("STATUS CHAIN DRIFT DETECTED", file=sys.stderr)
        print(
            "Tier 7 is non-authoritative — regenerate from the ROADMAP:\n",
            file=sys.stderr,
        )
        for err in all_errors:
            print(f"  ✗ {err}", file=sys.stderr)
        print(
            "\nFix: update the stale file to match its upstream source,",
            file=sys.stderr,
        )
        print(
            "     or regenerate the full chain from ROADMAP.md.",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
