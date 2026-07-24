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
    EquipmentDatasetBuildError,
    QualityDatasetBuildError,
    SessionsDatasetBuildError,
    TargetsDatasetBuildError,
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
            targets_path,
            equipment_path,
            quality_path,
        ) = build_warehouse(repository_root)

    except (
        WarehouseBuildError,
        WarehouseValidationError,
        SessionsDatasetBuildError,
        TargetsDatasetBuildError,
        EquipmentDatasetBuildError,
        QualityDatasetBuildError,
        FileNotFoundError,
        ImportError,
        OSError,
        ValueError,
    ) as exc:
        print()
        print("WAREHOUSE BUILD ERROR")
        print()
        print(str(exc))
        return 1

    print()
    print("Observatory Data Warehouse build completed.")
    print()

    print(f"Schema:     {schema_path}")
    print(f"Metadata:   {metadata_path}")
    print(f"Sessions:   {sessions_path}")
    print(f"Targets:    {targets_path}")
    print(f"Equipment:  {equipment_path}")
    print(f"Quality:    {quality_path}")

    print()
    print("Datasets populated:")
    print("  ✓ sessions")
    print("  ✓ targets")
    print("  ✓ equipment")
    print("  ✓ quality")

    print()
    print("Pending datasets:")
    print("  • weather")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
