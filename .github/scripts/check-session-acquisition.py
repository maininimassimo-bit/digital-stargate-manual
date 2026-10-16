"""Read-only guard: use the canonical analyzer before scientific publication."""
import argparse
import importlib.util
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def has_acquisition(session: Path) -> bool:
    spec = importlib.util.spec_from_file_location("session_acquisition_analyzer", ROOT / "dsg-analytics/analyzer/analyze_session.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    metrics = module.parse_nina(session / "raw/nina")
    return metrics["light_started"] > 0 or metrics["light_completed"] > 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session", required=True, type=Path)
    args = parser.parse_args()
    if not (args.session / "raw/nina").is_dir():
        raise SystemExit("Missing NINA evidence directory")
    skip = not has_acquisition(args.session)
    print("No scientific acquisition; safe no-op." if skip else "Scientific acquisition found.")
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output:
            output.write(f"skip={str(skip).lower()}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
