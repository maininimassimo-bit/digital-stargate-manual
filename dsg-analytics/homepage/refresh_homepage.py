#!/usr/bin/env python3
"""Validate the fail-closed homepage shell used by runtime projection consumers."""
from __future__ import annotations

import argparse
from pathlib import Path

START_MARKER = "<!-- DSG:AUTO-HOMEPAGE:START -->"
END_MARKER = "<!-- DSG:AUTO-HOMEPAGE:END -->"

REQUIRED_CONTRACT_TOKENS = (
    "data-dsg-home-snapshot",
    "data-home-freshness",
    "data-home-current-package",
    "data-home-current-detail",
    "data-home-latest-session",
    "data-home-latest-detail",
    "data-home-latest-link",
    "data-home-session-count",
    "data-home-session-totals",
)

FORBIDDEN_STALE_TOKENS = (
    "AP-013 in corso",
    "31,83 h",
    ">3 sessioni<",
)


def generated_block(text: str) -> str:
    """Return the single governed homepage block or fail on an ambiguous shell."""
    if text.count(START_MARKER) != 1 or text.count(END_MARKER) != 1:
        raise RuntimeError("Homepage automatic block markers missing or ambiguous")
    start = text.index(START_MARKER)
    end = text.index(END_MARKER, start) + len(END_MARKER)
    return text[start:end]


def validate_dynamic_shell(text: str) -> None:
    """Enforce runtime-binding hooks and reject known plausible stale fallback values."""
    block = generated_block(text)
    missing = [token for token in REQUIRED_CONTRACT_TOKENS if token not in block]
    if missing:
        raise RuntimeError(f"Homepage dynamic shell missing contract tokens: {', '.join(missing)}")
    stale = [token for token in FORBIDDEN_STALE_TOKENS if token.casefold() in block.casefold()]
    if stale:
        raise RuntimeError(f"Homepage dynamic shell contains stale fallback values: {', '.join(stale)}")
    if "cache: 'no-store'" in block or "fetch(" in block:
        raise RuntimeError("Homepage dynamic logic must remain in the external JavaScript consumer")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    homepage = args.repo_root.resolve() / "docs" / "index.md"
    validate_dynamic_shell(homepage.read_text(encoding="utf-8-sig"))
    print("Homepage dynamic projection shell validated: fail-closed runtime consumer contract PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
