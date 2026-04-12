#!/usr/bin/env python3
"""Pre-commit hook: validate that .claude/rules/ trigger globs match real files.

A rule whose `paths:` glob matches nothing is silently dead — it never fires.
This hook catches that class of breakage (e.g. path restructures that shift
files out from under a rule's glob) before it reaches the main branch.

Fires only when a file under .claude/rules/ is staged.

Exit codes:
    0 — all globs match at least one file (warnings printed for empty matches)
    1 — one or more globs match nothing (hard block)
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml  # PyYAML — project dependency

ROOT = Path(__file__).resolve().parents[2]
RULES_DIR = ROOT / ".claude" / "rules"

# Globs that are intentionally empty right now (e.g. code that will be written
# in future phases). These suppress the hard error and emit a warning instead.
# Remove an entry once files matching the glob actually exist.
EXPECTED_EMPTY: set[str] = {
    # Data pipeline Python files — layout is correct but code doesn't exist
    # yet (Phase 01 is still in progress). Re-evaluate once Phase 02 begins.
    "src/rts_predict/games/*/datasets/*/data/**/*.py",
}


# ---------------------------------------------------------------------------
# Frontmatter parser (minimal — only needs the paths: list)
# ---------------------------------------------------------------------------


def _extract_paths_from_frontmatter(text: str) -> list[str]:
    """Extract the `paths:` list from YAML frontmatter (---...--- block)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return []

    # Find closing ---
    close = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            close = i
            break

    if close is None:
        return []

    frontmatter_text = "\n".join(lines[1:close])
    try:
        data = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return []

    if not isinstance(data, dict):
        return []

    paths = data.get("paths", [])
    if isinstance(paths, str):
        paths = [paths]
    return [p for p in paths if isinstance(p, str)]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    rule_files = sorted(RULES_DIR.glob("*.md"))
    if not rule_files:
        print(f"check_rule_triggers: no rule files found in {RULES_DIR}", file=sys.stderr)
        return 0

    for rule_file in rule_files:
        text = rule_file.read_text(encoding="utf-8")
        globs = _extract_paths_from_frontmatter(text)

        if not globs:
            # Rule file has no paths: frontmatter — always-on rule, skip
            continue

        rule_name = rule_file.name
        for pattern in globs:
            matches = list(ROOT.glob(pattern))
            # Filter out directories — rules apply to files
            matches = [m for m in matches if m.is_file()]

            if not matches:
                if pattern in EXPECTED_EMPTY:
                    warnings.append(
                        f"{rule_name}: glob {pattern!r} matches nothing "
                        f"(listed in EXPECTED_EMPTY — suppressed)"
                    )
                else:
                    errors.append(
                        f"{rule_name}: glob {pattern!r} matches NO files "
                        f"in the repo — rule will never fire"
                    )

    if warnings:
        for w in warnings:
            print(f"  ⚠ {w}", file=sys.stderr)

    if errors:
        print("DEAD RULE TRIGGERS DETECTED", file=sys.stderr)
        print(
            "The following .claude/rules/ path globs match no files:\n",
            file=sys.stderr,
        )
        for err in errors:
            print(f"  ✗ {err}", file=sys.stderr)
        print(
            "\nFix: update the glob in the rule's frontmatter to match the",
            file=sys.stderr,
        )
        print(
            "     current file layout, or add to EXPECTED_EMPTY if intentional.",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
