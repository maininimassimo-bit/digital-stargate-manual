#!/usr/bin/env python3
"""Enrich consolidated history from governed scientific evidence.

This migration adapter is intentionally downstream of consolidate_history.py:
legacy normalization remains compatible while schema 2.1 scientific/SQM fields
are copied from canonical normalized metrics. Missing configuration metadata is
then resolved fail-closed from governed repository metadata without guessing.
"""
from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

FIELDS = [
    'target_name', 'ra_deg', 'dec_deg', 'coordinate_epoch',
    'configuration_id', 'telescope', 'camera', 'binning',
    'sqm_state', 'sqm_start', 'sqm_end', 'sqm_min_mag_arcsec2',
    'sqm_max_mag_arcsec2', 'sqm_mean_mag_arcsec2',
    'sqm_median_mag_arcsec2', 'sqm_valid_samples',
    'sqm_temporal_coverage', 'sqm_source', 'sqm_quality'
]


def val(mapping, key):
    value = mapping.get(key)
    return '' if value is None else value


def projection(metrics):
    scientific = metrics.get('scientific', {})
    sqm = metrics.get('sqm', {})
    return {
        'target_name': val(scientific, 'target_name'),
        'ra_deg': val(scientific, 'ra_deg'),
        'dec_deg': val(scientific, 'dec_deg'),
        'coordinate_epoch': val(scientific, 'epoch'),
        'configuration_id': val(scientific, 'configuration_id'),
        'telescope': val(scientific, 'telescope'),
        'camera': val(scientific, 'camera'),
        'binning': val(scientific, 'binning'),
        'sqm_state': val(sqm, 'state'),
        'sqm_start': val(sqm, 'start'),
        'sqm_end': val(sqm, 'end'),
        'sqm_min_mag_arcsec2': val(sqm, 'min_mag_arcsec2'),
        'sqm_max_mag_arcsec2': val(sqm, 'max_mag_arcsec2'),
        'sqm_mean_mag_arcsec2': val(sqm, 'mean_mag_arcsec2'),
        'sqm_median_mag_arcsec2': val(sqm, 'median_mag_arcsec2'),
        'sqm_valid_samples': val(sqm, 'valid_samples'),
        'sqm_temporal_coverage': val(sqm, 'temporal_coverage'),
        'sqm_source': val(sqm, 'source'),
        'sqm_quality': val(sqm, 'quality'),
    }


def read_index(path: Path):
    if not path.exists():
        return {}
    with path.open('r', encoding='utf-8-sig', newline='') as handle:
        return {
            str(row.get('session_id') or '').strip(): row
            for row in csv.DictReader(handle)
            if str(row.get('session_id') or '').strip()
        }


def governed_configuration(root: Path, session_id: str):
    metadata = read_index(root / 'data/analytics/metadata/session-scientific-metadata.csv').get(session_id, {})
    mapping = read_index(root / 'data/analytics/configurations/session-configuration-map.csv').get(session_id, {})

    # REGISTERED scientific metadata is the strongest repository attestation.
    if str(metadata.get('metadata_state') or '').strip() == 'REGISTERED' and str(metadata.get('configuration_id') or '').strip():
        return metadata

    # The governed session map may attest a configuration independently.
    if str(mapping.get('configuration_id') or '').strip():
        return mapping

    return {}


def apply_governed_configuration(row, root: Path):
    # Never overwrite configuration evidence already projected from canonical metrics.
    if str(row.get('configuration_id') or '').strip():
        return

    governed = governed_configuration(root, str(row.get('session_id') or '').strip())
    configuration_id = str(governed.get('configuration_id') or '').strip()
    if not configuration_id:
        return

    row['configuration_id'] = configuration_id
    for field in ('telescope', 'camera', 'binning'):
        if not str(row.get(field) or '').strip() and str(governed.get(field) or '').strip():
            row[field] = governed[field]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--history', default='data/analytics/history/sessions.csv')
    parser.add_argument('--repo-root', default='.')
    args = parser.parse_args()
    root = Path(args.repo_root)
    history_path = root / args.history

    with history_path.open('r', encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        base = list(reader.fieldnames or [])

    fields = []
    for name in base + FIELDS:
        if name not in fields:
            fields.append(name)

    updated_at = datetime.now(timezone.utc).isoformat(timespec='seconds')
    for row in rows:
        source = str(row.get('source_metrics_path') or '').strip()
        if source:
            metrics_path = Path(source)
            metrics_path = metrics_path if metrics_path.is_absolute() else root / metrics_path
            if metrics_path.exists():
                metrics = json.loads(metrics_path.read_text(encoding='utf-8-sig'))
                row.update(projection(metrics))

        apply_governed_configuration(row, root)
        row['schema_version'] = '2.1.0'
        row['updated_at_utc'] = updated_at

    with history_path.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)


if __name__ == '__main__':
    main()
