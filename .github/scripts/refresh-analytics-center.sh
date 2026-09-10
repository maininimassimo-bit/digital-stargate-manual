#!/usr/bin/env bash
set -euo pipefail

python dsg-analytics/configuration/build_configuration_summary.py --repo-root .
python dsg-analytics/dashboard/build_dashboard_v31.py --repo-root .
python .github/scripts/verify-analytics-center-consistency.py
