"""Compose private candidate checks without accepting or exporting records."""
from tools.pixinsight.workflow_archive.archive import digest, encode
from .asset_metadata import check_asset_metadata
from .catalog_context import check_catalog_context, valid
from .draft_journal import parse_selected_source


KIND = 'DSG_PRIVATE_REGISTRATION_SELECTION_V1'


def check_registration_metadata(source, expected_digest, *, measurement_source=None, measurement_digest=None):
    """Check an explicit selected pair/context, never infer or publish a binding.

    Nested digests derive from the parent selection, not independent trust.
    Measurement bytes/digest must be separately selected by the caller.
    """
    data = parse_selected_source(source, expected_digest)
    findings = []
    if set(data) != {'kind', 'catalogContext', 'assetSelection', 'sessionId', 'targetId'} or data.get('kind') != KIND:
        findings.append('SELECTION_FIELDS_OR_KIND')
    reports = {}
    for field, checker in (('catalogContext', check_catalog_context), ('assetSelection', check_asset_metadata)):
        value = data.get(field)
        if type(value) is not dict:
            findings.append('MISSING_' + field.upper())
            value = {}
        raw = encode(value)
        kwargs = dict(measurement_source=measurement_source, measurement_digest=measurement_digest) if field == 'assetSelection' else {}
        reports[field] = checker(raw, digest(raw), **kwargs)
    for field in ('sessionId', 'targetId'):
        if not valid(data.get(field), 'id'):
            findings.append('INVALID_' + field.upper())

    catalog = data.get('catalogContext')
    catalog = catalog if type(catalog) is dict else {}

    def exactly_one(collection, key, expected):
        rows = catalog.get(collection)
        if type(rows) is not list or len(rows) > 8 or not valid(expected, 'id'):
            return None
        matches = [row for row in rows if type(row) is dict and row.get(key) == expected]
        return matches[0] if len(matches) == 1 else None

    session = exactly_one('sessions', 'sessionId', data.get('sessionId'))
    target = exactly_one('targets', 'targetId', data.get('targetId'))
    observation = exactly_one('observations', 'observationId', session.get('observationId')) if session else None
    if session is None or target is None or observation is None:
        findings.append('SELECTED_CONTEXT_UNRESOLVED')
    elif observation.get('targetId') != data['targetId']:
        findings.append('SELECTED_TARGET_MISMATCH')
    if exactly_one('catalogItems', 'entityId', data.get('sessionId')) is None:
        findings.append('SELECTED_CATALOG_ITEM_UNRESOLVED')
    return dict(kind='DSG_PRIVATE_REGISTRATION_VALIDATION_REPORT_V1', sourceSha256=expected_digest,
                findings=findings, reports=reports, state='DRAFT_NOT_ACCEPTED',
                publicationState='PRIVATE_NOT_APPROVED', scientificAuthority='NONE',
                acceptanceEligible=False, catalogWritePerformed=False,
                validationScope='SELECTED_METADATA_AND_REFERENCE_CONSISTENCY_ONLY',
                unverified=['COMPLETE_SCIENTIFIC_RUBRIC_AND_VOCABULARIES', 'IDENTITY_AND_SOURCE_GOVERNANCE',
                            'HISTORICAL_CONFIGURATION_VALIDITY', 'SEPARATE_REAL_RECORD_DECISIONS',
                            'OPERATIONAL_RETENTION_AND_CURRENT_AUTHORITY_SNAPSHOT',
                            'EXACT_F4_WORKFLOW_BINDING', 'PUBLICATION_APPROVAL'])
