"""Compatibility entry point; original F0 implementation is retained in Git history.
The hardened parser is owned by tools.pixinsight.workflow_archive.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.pixinsight.workflow_archive.export_parser import (  # noqa: E402
    MAX_BYTES, Unsupported, parse_export, safe_summary, main,
)
if __name__ == '__main__':
    main()
