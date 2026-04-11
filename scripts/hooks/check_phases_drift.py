#!/usr/bin/env python3
"""Pre-commit hook: verify docs/ml_experiment_phases/PHASES.md has not drifted
from the canonical phase table in docs/PHASES.md.

Compares phase number + name pairs only (ignores source links and summaries,
which use different relative paths in each file).
"""
import re
import sys
from pathlib import Path

PHASE_ROW = re.compile(r'^\| \*\*(\d{2})\*\* \| ([^|]+) \|')


def extract_phases(path: Path) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in path.read_text().splitlines():
        m = PHASE_ROW.match(line)
        if m:
            rows[m.group(1)] = m.group(2).strip()
    return rows


repo_root = Path(__file__).resolve().parents[2]
canonical = extract_phases(repo_root / "docs/PHASES.md")
derivative = extract_phases(repo_root / "docs/ml_experiment_phases/PHASES.md")

if canonical != derivative:
    print("DRIFT: docs/ml_experiment_phases/PHASES.md has drifted from docs/PHASES.md")
    for num in sorted(set(canonical) | set(derivative)):
        c = canonical.get(num, "<missing>")
        d = derivative.get(num, "<missing>")
        if c != d:
            print(f"  Phase {num}: canonical='{c}'  derivative='{d}'")
    sys.exit(1)
