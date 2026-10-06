"""Explicit private historical provenance; never fabricates catalog/session records."""
import re
from datetime import date

from .broker import require
from tools.pixinsight.workflow_archive.archive import build_packet


def historical(selection):
    return 'historicalSource' in selection


def validate_historical(selection):
    value = selection.get('historicalSource')
    require(isinstance(value, dict) and set(value) == {'target', 'provenance', 'attested'}, 'HISTORICAL_SOURCE_FIELDS')
    for key, maximum in [('target', 160), ('provenance', 2000)]:
        text = value[key]
        require(isinstance(text, str) and bool(text.strip()) and len(text) <= maximum and
                not any(ord(c) < 32 and (key == 'target' or c not in '\n\r\t') for c in text), 'HISTORICAL_SOURCE_TEXT')
    require(value['target'].strip().upper() not in {'UNKNOWN', 'UNSPECIFIED', 'N/A'}, 'HISTORICAL_TARGET_REQUIRED')
    require(value['attested'] is True, 'HISTORICAL_ATTESTATION_REQUIRED')
    require(selection.get('sessionIds') == [] and selection.get('catalogSha256') is None and
            selection.get('parent') is None and selection.get('associationConfirmed') is False,
            'HISTORICAL_NO_CATALOG_ASSOCIATION')
    title = selection.get('title')
    require(isinstance(title, str) and bool(title.strip()) and len(title) <= 160 and
            not any(ord(c) < 32 for c in title), 'HISTORICAL_TITLE')
    value_date = selection.get('processingDate')
    require(isinstance(value_date, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', value_date), 'PROCESSING_DATE_INVALID')
    try:
        date.fromisoformat(value_date)
    except ValueError:
        require(False, 'PROCESSING_DATE_INVALID')
    return value


def historical_review(selection, workflow_raw=b'', receipt_id='BKL049-historical', imported_at=''):
    source = validate_historical(selection)
    return {'target': source['target'].strip(),
            'sessionContext': {'source': 'HISTORICAL_OWNER_DECLARATION', 'catalogSha256': None,
                               'sessions': [], 'association': 'NOT_ESTABLISHED',
                               'registryAdmission': 'NOT_ESTABLISHED',
                               'historicalSource': source.copy()},
            'workflow': build_packet(workflow_raw, receipt_id, imported_at) if workflow_raw else None}
