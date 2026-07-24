#!/usr/bin/env python3
"""Digital StarGate Analytics v3.1 - native MkDocs Material dashboard."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import build_dashboard as legacy

SCRIPT_DIR = Path(__file__).