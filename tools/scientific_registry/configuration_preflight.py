"""Read-only DSDM-002 configuration checks, never scientific acceptance.

The caller selects private JSON bytes and their independently retained digest.
No input path, identifier, value or source text is reflected in findings.
"""
import re
from datetime import datetime

from .draft_journal import parse_selected_source


KIND = 'DSG_PRIVATE_CONFIGURATION_PREFLIGHT_V1'
SECTIONS = {
    'observatory': ('observatoryId', 'name', 'timezoneId', 'status'),
    'telescope': ('telescopeId', 'model', 'status'),
    'camera': ('cameraId', 'model', 'isColor', 'status'),
    'configuration': ('instrumentConfigurationId', 'observatoryId', 'telescopeId',
                      'cameraId', 'configurationName', 'configurationVersion',
                      'validFromUtc', 'status'),
}
AUDIT = ('createdAtUtc', 'createdBy', 'updatedAtUtc', 'updatedBy',
         'recordVersion', 'lifecycleStatus', 'sourceSystem')
OPTIONAL = {
    'observatory': ('siteCode', 'latitude', 'longitude', 'elevationMeters'),
    'telescope': ('manufacturer', 'apertureMm', 'nativeFocalLengthMm',
                  'nativeFocalRatio', 'opticalDesign', 'assetReference'),
    'camera': ('manufacturer', 'serialReference', 'sensorName', 'sensorType',
               'pixelSizeMicron', 'widthPixels', 'heightPixels', 'coolingSupported'),
    'configuration': ('mountId', 'focuserId', 'filterWheelId', 'reducerOrCorrector',
                      'effectiveFocalLengthMm', 'effectiveFocalRatio',
                      'pixelScaleArcsecPerPixel', 'validToUtc'),
}
TIMES = ('validFromUtc', 'validToUtc', 'createdAtUtc', 'updatedAtUtc')
INTEGERS = ('configurationVersion', 'recordVersion', 'widthPixels', 'heightPixels')
POSITIVE = ('apertureMm', 'nativeFocalLengthMm', 'nativeFocalRatio',
            'pixelSizeMicron', 'effectiveFocalLengthMm', 'effectiveFocalRatio',
            'pixelScaleArcsecPerPixel')


def utc(value):
    """Validate explicit UTC syntax and calendar; never attach a timezone."""
    if type(value) is not str or not re.fullmatch(
            r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?Z', value):
        return None
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        return None


def check_configuration(source, expected_digest):
    """Return bounded structural findings; even zero findings never means accepted.

    Input is an internal selection with observatory/telescope/camera/configuration
    objects, not a replacement public schema or a whole-registry validator. DSDM
    identifiers are checked as stable nonempty references here; their governed
    allocation, namespace mapping and uniqueness are separate review obligations.
    """
    data = parse_selected_source(source, expected_digest)
    findings = []

    def finding(section, field, code):
        findings.append({'section': section, 'field': field, 'code': code})

    if set(data) - set(SECTIONS):
        finding('selection', None, 'UNSUPPORTED_FIELDS')
    rows = {}
    for section, required in SECTIONS.items():
        row = data.get(section)
        if type(row) is not dict:
            finding(section, None, 'MISSING_RECORD' if row is None else 'INVALID_RECORD')
            continue
        rows[section] = row
        allowed = (*required, *AUDIT, *OPTIONAL[section], 'correlationId')
        if set(row) - set(allowed):
            finding(section, None, 'UNSUPPORTED_FIELDS')
        for field in allowed:
            value = row.get(field)
            if value is None:
                if field in (*required, *AUDIT):
                    finding(section, field, 'REQUIRED')
                continue
            valid = True
            if field in TIMES:
                valid = utc(value) is not None
            elif field in INTEGERS:
                valid = type(value) is int and value >= 1
            elif field in ('isColor', 'coolingSupported'):
                valid = type(value) is bool
            elif field in POSITIVE:
                valid = type(value) in (int, float) and value > 0
            elif field in ('latitude', 'longitude', 'elevationMeters'):
                valid = type(value) in (int, float)
                if valid and field != 'elevationMeters':
                    bound = 90 if field == 'latitude' else 180
                    valid = -bound <= value <= bound
            else:
                valid = type(value) is str and 0 < len(value) <= 2048 and bool(value.strip())
            if not valid:
                finding(section, field, 'INVALID_VALUE')
        if section == 'configuration' and row.get('status') is not None:
            if row['status'] not in ('DRAFT', 'ACTIVE', 'RETIRED'):
                finding(section, 'status', 'INVALID_ENUM')
        created, updated = utc(row.get('createdAtUtc')), utc(row.get('updatedAtUtc'))
        if created and updated and updated < created:
            finding(section, 'updatedAtUtc', 'TIME_ORDER')
        start, end = utc(row.get('validFromUtc')), utc(row.get('validToUtc'))
        if start and end and end <= start:
            finding(section, 'validToUtc', 'TIME_ORDER')

    configuration = rows.get('configuration', {})
    for section, field in (('observatory', 'observatoryId'), ('telescope', 'telescopeId'),
                           ('camera', 'cameraId')):
        reference = configuration.get(field)
        identity = rows.get(section, {}).get(field)
        if type(reference) is str and reference.strip() and type(identity) is str and identity.strip():
            if reference != identity:
                finding('configuration', field, 'REFERENCE_MISMATCH')

    return {
        'kind': KIND,
        'sourceSha256': expected_digest,
        'profile': 'DSDM-002-SECTIONS-2.2-5.1-5.2-5.3-5.5-STRUCTURAL-SUBSET',
        'structuralState': 'FINDINGS' if findings else 'NO_STRUCTURAL_FINDINGS',
        'findings': findings,
        'state': 'DRAFT_NOT_ACCEPTED', 'publicationState': 'PRIVATE_NOT_APPROVED',
        'scientificAuthority': 'NONE', 'catalogWritePerformed': False,
        'acceptanceEligible': False,
        'unverified': ['GOVERNED_IDENTITIES_AND_VOCABULARIES', 'SOURCE_PROVENANCE',
                       'TIMEZONE_SEMANTICS', 'HISTORICAL_CONFIGURATION_VALIDITY',
                       'OBSERVATION_SESSION_CONTEXT', 'ASSET_REGISTRATION',
                       'CATALOG_ACCEPTANCE', 'OPERATIONAL_RETENTION', 'EXACT_F4_BINDING'],
    }
