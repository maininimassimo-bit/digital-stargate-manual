#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read_rows(path: Path):
    with path.open('r', encoding='utf-8-sig', newline='') as handle:
        return list(csv.DictReader(handle))


history = {row['session_id']: row for row in read_rows(ROOT / 'data/analytics/history/sessions.csv')}
metadata = {row['session_id']: row for row in read_rows(ROOT / 'data/analytics/metadata/session-scientific-metadata.csv')}
mapping = {row['session_id']: row for row in read_rows(ROOT / 'data/analytics/configurations/session-configuration-map.csv')}

failures = []
for session_id, row in history.items():
    actual = str(row.get('configuration_id') or '').strip()
    meta = metadata.get(session_id, {})
    mapped = mapping.get(session_id, {})

    expected = ''
    source = ''
    if str(meta.get('metadata_state') or '').strip() == 'REGISTERED' and str(meta.get('configuration_id') or '').strip():
        expected = str(meta['configuration_id']).strip()
        source = 'REGISTERED scientific metadata'
    elif str(mapped.get('configuration_id') or '').strip():
        expected = str(mapped['configuration_id']).strip()
        source = 'session configuration map'

    if expected and actual != expected:
        failures.append(f'{session_id}: expected {expected} from {source}, found {actual or "<empty>"}')

if failures:
    raise SystemExit('Governed configuration propagation FAILED:\n- ' + '\n- '.join(failures))

resolved = sum(1 for row in history.values() if str(row.get('configuration_id') or '').strip())
unresolved = len(history) - resolved
print(f'Governed configuration propagation PASS: sessions={len(history)}; resolved={resolved}; unresolved={unresolved}')
