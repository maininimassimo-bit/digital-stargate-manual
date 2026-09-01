#!/usr/bin/env bash
set -euo pipefail

SESSION_ID="2026-08-31_2026-09-01"
SESSION_DIR="data/sessions/2026/08/${SESSION_ID}"
METRICS="${SESSION_DIR}/normalized/session-metrics.json"
HISTORY="data/analytics/history/sessions.csv"
LATEST="docs/data/realtime/latest-observation.json"

python dsg-analytics/analyzer/analyze_session.py --session "${SESSION_DIR}" >/tmp/dsg-e2e-metrics.json
python dsg-analytics/history/update_history.py --metrics "${METRICS}" --history "${HISTORY}"
python dsg-analytics/history/consolidate_history.py --mode update
python dsg-analytics/history/enrich_scientific_history.py
node .github/scripts/generate-scientific-session-catalog.mjs --write
node .github/scripts/generate-scientific-catalog.mjs --write
python dsg-analytics/reporter/update_latest_observation.py --session "${SESSION_DIR}" --output "${LATEST}"

python - <<'PY'
import csv, json, math
from pathlib import Path
sid='2026-08-31_2026-09-01'
metrics=json.loads(Path(f'data/sessions/2026/08/{sid}/normalized/session-metrics.json').read_text(encoding='utf-8'))
science=metrics['scientific']; sqm=metrics['sqm']
assert metrics['schema_version']=='0.2.0'
assert science['target_name']=='M 27'
assert math.isclose(float(science['ra_deg']),299.9,abs_tol=1e-6)
assert math.isclose(float(science['dec_deg']),22+43/60+16/3600,abs_tol=1e-6)
assert science['camera']=='QHY695A'
assert science['telescope']=='Celestron C8 XLT'
assert int(science['binning'])==1
assert science['configuration_id']=='C8_QHY695A_BIN1'
assert sqm['state']=='AVAILABLE'
assert math.isclose(float(sqm['median_mag_arcsec2']),18.66,abs_tol=1e-6)

with Path('data/analytics/history/sessions.csv').open(encoding='utf-8-sig',newline='') as handle:
    row=next(r for r in csv.DictReader(handle) if r['session_id']==sid)
assert row['target_name']=='M 27'
assert row['camera']=='QHY695A'
assert row['configuration_id']=='C8_QHY695A_BIN1'
assert math.isclose(float(row['sqm_median_mag_arcsec2']),18.66,abs_tol=1e-6)

catalog=json.loads(Path('docs/data/scientific-session-catalog.json').read_text(encoding='utf-8'))
session=next(s for s in catalog['sessions'] if s['sessionId']==sid)
assert session['target']=='M 27'
assert session['coordinateSource']=='canonical-session-metrics'
assert math.isclose(float(session['raDeg']),299.9,abs_tol=1e-6)
assert session['camera']=='QHY695A'
assert session['configurationId']=='C8_QHY695A_BIN1'
assert math.isclose(float(session['sqm']['medianMagArcsec2']),18.66,abs_tol=1e-6)

index=json.loads(Path('docs/data/scientific-observation-index.json').read_text(encoding='utf-8'))
doc=next(d for d in index['searchDocuments'] if sid in d['searchDocumentId'])
assert doc['facetValues']['camera']==['QHY695A']
assert doc['facetValues']['sqmState']==['AVAILABLE']
assert math.isclose(float(doc['rankingSignals']['sqmMedianMagArcsec2']),18.66,abs_tol=1e-6)

latest=json.loads(Path('docs/data/realtime/latest-observation.json').read_text(encoding='utf-8'))
assert latest['session_id']==sid
assert latest['target']['name']=='M 27'
assert math.isclose(float(latest['target']['ra_deg']),299.9,abs_tol=1e-6)
assert latest['equipment']['camera']=='QHY695A'
assert latest['equipment']['configuration_id']=='C8_QHY695A_BIN1'
assert math.isclose(float(latest['metrics']['sqm_median_mag_arcsec2']),18.66,abs_tol=1e-6)
print('Scientific session E2E gate passed.')
PY
