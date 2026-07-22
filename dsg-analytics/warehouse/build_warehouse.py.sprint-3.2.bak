#!/usr/bin/env python3
"""Build the Digital StarGate Observatory Data Warehouse."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(
        0,
        str(
            Path(__file__).resolve().parent.parent
        ),
    )

from warehouse.builder import (
    WarehouseBuildError,
    build_warehouse,
)
from warehouse.datasets import (
    SessionsDatasetBuildError,
)
from warehouse.validators import (
    WarehouseValidationError,
)


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description=(
            "Build the Digital StarGate Observatory "
            "Data Warehouse."
        )
    )

    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path("."),
        help="Repository root directory.",
    )

    return parser.parse_args()


def main() -> int:
    """Run the warehouse build."""

    args = parse_arguments()
    repository_root = args.repo_root.resolve()

    try:
        (
            schema_path,
            metadata_path,
            sessions_path,
        ) = build_warehouse(repository_root)
    except (
        WarehouseBuildError,
        WarehouseValidationError,
        SessionsDatasetBuildError,
        FileNotFoundError,
        ImportError,
        OSError,
        ValueError,
    ) as exc:
        print("WAREHOUSE BUILD ERROR")
        print(str(exc))
        return 1

    print(
        "Observatory Data Warehouse build completed."
    )
    print(f"- Schema: {schema_path}")
    print(f"- Metadata: {metadata_path}")
    print(f"- Sessions: {sessions_path}")
    print("- Sessions status: populated")
    print(
        "- Remaining datasets: "
        "targets, equipment, weather, quality"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())