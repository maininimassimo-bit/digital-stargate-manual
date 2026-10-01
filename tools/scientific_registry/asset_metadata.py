"""Private selected DSDM-002 asset validation; no file access or authority."""
import re

from .catalog_context import valid as context_valid
from .configuration_preflight import utc
from .draft_journal import parse_selected_source


KIND = 'DSG_PRIVATE_ASSET_SELECTION_V1'
MEASUREMENTS = 'DSG_PRIVATE_ASSET_MEASUREMENTS_V1'
COMMON = dict(createdAtUtc='utc', createdBy='text', updatedAtUtc='utc', updatedBy='text',
              recordVersion='version', lifecycleStatus='unresolved', sourceSystem='text')
REQUIRED = {
    'assets': dict(assetId='id', assetClass='assetClass', originalFileName='text1024', format='text',
                   sizeBytes='uint', immutabilityStatus='immutabilityStatus',
                   integrityStatus='integrityStatus', registrationStatus='registrationStatus'),
    'volumes': dict(storageVolumeId='id', logicalName='text', storageType='storageType', role='role',
                    healthStatus='healthStatus', availabilityStatus='volumeAvailability',
                    encryptionStatus='encryptionStatus', backupStatus='backupStatus'),
    'locators': dict(locatorId='id', assetId='id', storageVolumeId='id', relativePath='relativePath',
                     locatorType='locatorType', availabilityStatus='unresolved', firstSeenAtUtc='utc',
                     sanitizedForPublication='boolean'),
    'integrityRecords': dict(integrityRecordId='id', assetId='id', algorithm='shaAlgorithm',
                             hashValue='sha', computedAtUtc='utc', computedBy='text',
                             verificationType='verificationType', result='result'),
    'relations': dict(assetRelationId='id', sourceAssetId='id', targetAssetId='id',
                      relationType='relationType', confidence='unresolved'),
}
OPTIONAL = {
    'assets': dict(mediaType='text', createdAtObserved='utc', modifiedAtObserved='utc',
                   metadataCompleteness='percentage', canonicalContentHash='sha',
                   canonicalHashAlgorithm='shaAlgorithm'),
    'volumes': dict(volumeLabelObserved='text', deviceSerialReference='text', filesystem='text',
                    capacityBytes='uint'),
    'locators': dict(lastVerifiedAtUtc='utc', supersededAtUtc='utc'),
    'integrityRecords': dict(locatorId='id', previousIntegrityRecordId='id', errorDetail='text'),
    'relations': dict(processingRunId='unsupportedReference', notes='text4000'),
}
KEYS = dict(assets='assetId', volumes='storageVolumeId', locators='locatorId',
            integrityRecords='integrityRecordId', relations='assetRelationId')
ENUMS = {
    'assetClass': ('RAW_ORIGINAL', 'CALIBRATION_ORIGINAL', 'CALIBRATION_MASTER', 'CALIBRATED',
                   'REGISTERED', 'INTEGRATED', 'PROCESSING_INTERMEDIATE', 'FINAL_SCIENTIFIC',
                   'FINAL_PUBLICATION', 'DOCUMENTATION', 'UNCLASSIFIED'),
    'immutabilityStatus': ('NOT_ASSESSED', 'LOGICALLY_IMMUTABLE', 'WRITE_PROTECTED', 'MUTABLE',
                           'VIOLATION_DETECTED', 'UNKNOWN'),
    'integrityStatus': ('NOT_VERIFIED', 'VERIFIED_ONCE', 'VERIFIED_PERIODICALLY', 'MISMATCH',
                        'UNREADABLE', 'UNKNOWN'),
    'registrationStatus': ('DISCOVERED', 'REGISTERED', 'VERIFIED', 'QUARANTINED', 'WITHDRAWN'),
    'storageType': ('LOCAL_DISK', 'USB_DISK', 'NETWORK_SHARE', 'OBJECT_STORAGE', 'OTHER'),
    'role': ('ACQUISITION_SOURCE', 'ACTIVE_ARCHIVE', 'HISTORICAL_ARCHIVE', 'CALIBRATION_LIBRARY',
             'STAGING', 'BACKUP', 'OTHER'),
    'healthStatus': ('HEALTHY', 'DEGRADED', 'FAILED', 'UNKNOWN'),
    'volumeAvailability': ('ONLINE', 'OFFLINE', 'NOT_CONNECTED', 'UNKNOWN'),
    'encryptionStatus': ('ENCRYPTED', 'NOT_ENCRYPTED', 'UNKNOWN'),
    'backupStatus': ('PROTECTED', 'PARTIALLY_PROTECTED', 'NOT_PROTECTED', 'UNKNOWN'),
    'locatorType': ('PRIMARY', 'SECONDARY', 'STAGING', 'SOURCE', 'BACKUP'),
    'verificationType': ('INITIAL', 'REPEAT', 'TRANSFER_SOURCE', 'TRANSFER_DESTINATION', 'PERIODIC', 'MIGRATION'),
    'result': ('MATCH', 'MISMATCH', 'COMPUTED', 'FAILED', 'PARTIAL'),
    'relationType': ('DERIVED_FROM', 'CALIBRATED_FROM', 'REGISTERED_FROM', 'INTEGRATED_FROM',
                     'PUBLICATION_VARIANT_OF', 'DUPLICATE_OF', 'POSSIBLE_DUPLICATE_OF', 'SUPERSEDES', 'RELATED_TO'),
    'shaAlgorithm': ('SHA-256',),
}
MEASUREMENT_FIELDS = dict(assetId='id', sha256='sha', sizeBytes='uint', scope='text',
                          measuredAtUtc='utc', evidenceRef='text')


def valid(value, rule):
    if rule in ENUMS:
        return type(value) is str and value in ENUMS[rule]
    if rule == 'uint':
        return type(value) is int and 0 <= value <= 9223372036854775807
    if rule == 'percentage':
        return type(value) in (int, float) and 0 <= value <= 100
    if rule == 'boolean':
        return type(value) is bool
    if rule == 'sha':
        return type(value) is str and re.fullmatch(r'[a-f0-9]{64}', value) is not None
    if rule == 'relativePath':
        if type(value) is not str or not 0 < len(value) <= 2048 or ':' in value or '\x00' in value:
            return False
        return all(part not in ('', '.', '..') for part in value.replace('\\', '/').split('/'))
    if rule == 'unsupportedReference':
        return False
    return context_valid(value, rule)


def check_asset_metadata(source, expected_digest, *, measurement_source=None, measurement_digest=None):
    """Check candidates against separately selected full-file measurements if supplied.

    Digests are integrity anchors, not authentication or proof of independent
    measurement. A caller must establish origin/scope/currentness separately.
    No scientific file/path is opened and no acceptance/export is possible.
    """
    data = parse_selected_source(source, expected_digest)
    findings, gaps, eligibility, indexes, rows = [], [], [], {}, {}

    def finding(collection, index, field, code):
        findings.append(dict(collection=collection, index=index, field=field, code=code))

    if set(data) - {'kind', 'originalAssetId', 'previewAssetId', *REQUIRED}:
        finding('selection', None, None, 'UNSUPPORTED_FIELDS')
    if data.get('kind') != KIND:
        finding('selection', None, 'kind', 'UNSUPPORTED_KIND')
    for field in ('originalAssetId', 'previewAssetId'):
        if not valid(data.get(field), 'id'):
            finding('selection', None, field, 'REQUIRED_ID')
    if valid(data.get('originalAssetId'), 'id') and data['originalAssetId'] == data.get('previewAssetId'):
        finding('selection', None, 'previewAssetId', 'SAME_SELECTED_ID')

    for collection, fields in REQUIRED.items():
        selected = data.get(collection)
        indexes[collection] = {}
        if type(selected) is not list or not 1 <= len(selected) <= 8:
            finding(collection, None, None, 'RECORD_COUNT')
            rows[collection] = []
            continue
        rows[collection] = selected
        identities = {}
        rules = {**COMMON, **fields, **OPTIONAL[collection], 'correlationId': 'text'}
        for index, row in enumerate(selected):
            if type(row) is not dict:
                finding(collection, index, None, 'INVALID_RECORD')
                continue
            if set(row) - set(rules):
                finding(collection, index, None, 'UNSUPPORTED_FIELDS')
            for field, rule in rules.items():
                value = row.get(field)
                if value is None:
                    if field in COMMON or field in fields:
                        finding(collection, index, field, 'REQUIRED')
                elif not valid(value, rule):
                    finding(collection, index, field, 'UNSUPPORTED_REFERENCE' if rule == 'unsupportedReference'
                            else 'INVALID_VALUE')
                elif rule == 'unresolved':
                    gaps.append(dict(collection=collection, index=index, field=field,
                                     code='VOCABULARY_UNRESOLVED'))
            key = KEYS[collection]
            if valid(row.get(key), 'id'):
                identities.setdefault(row[key], []).append(index)
            for earlier, later in (('createdAtUtc', 'updatedAtUtc'), ('firstSeenAtUtc', 'lastVerifiedAtUtc'),
                                   ('firstSeenAtUtc', 'supersededAtUtc')):
                start, end = utc(row.get(earlier)), utc(row.get(later))
                if start and end and end < start:
                    finding(collection, index, later, 'TIME_ORDER')
            if collection == 'assets':
                if (row.get('canonicalContentHash') is None) != (row.get('canonicalHashAlgorithm') is None):
                    finding(collection, index, 'canonicalContentHash', 'INCOMPLETE_HASH_PAIR')
        for identity, positions in identities.items():
            if len(positions) > 1:
                for index in positions:
                    finding(collection, index, KEYS[collection], 'DUPLICATE_ID')
            else:
                indexes[collection][identity] = selected[positions[0]]

    references = (('locators', 'assetId', 'assets'), ('locators', 'storageVolumeId', 'volumes'),
                  ('integrityRecords', 'assetId', 'assets'), ('integrityRecords', 'locatorId', 'locators'),
                  ('integrityRecords', 'previousIntegrityRecordId', 'integrityRecords'),
                  ('relations', 'sourceAssetId', 'assets'), ('relations', 'targetAssetId', 'assets'))
    for collection, field, destination in references:
        for index, row in enumerate(rows[collection]):
            if type(row) is dict and valid(row.get(field), 'id') and row[field] not in indexes[destination]:
                finding(collection, index, field, 'UNRESOLVED_REFERENCE')

    volume_names = set()
    for index, volume in enumerate(rows['volumes']):
        if type(volume) is dict and valid(volume.get('logicalName'), 'text'):
            if volume['logicalName'] in volume_names:
                finding('volumes', index, 'logicalName', 'DUPLICATE_LOGICAL_NAME')
            volume_names.add(volume['logicalName'])
    active_locations = set()
    for index, locator in enumerate(rows['locators']):
        if type(locator) is not dict:
            continue
        if valid(locator.get('storageVolumeId'), 'id') and valid(locator.get('relativePath'), 'relativePath'):
            key = (locator['storageVolumeId'], locator['relativePath'].replace('\\', '/'))
            if locator.get('supersededAtUtc') is None:
                if key in active_locations:
                    finding('locators', index, 'relativePath', 'DUPLICATE_ACTIVE_LOCATION')
                active_locations.add(key)

    for index, integrity in enumerate(rows['integrityRecords']):
        if type(integrity) is not dict:
            continue
        locator = indexes['locators'].get(integrity.get('locatorId')) if valid(integrity.get('locatorId'), 'id') else None
        if locator and locator.get('assetId') != integrity.get('assetId'):
            finding('integrityRecords', index, 'locatorId', 'LOCATOR_ASSET_MISMATCH')
        asset = indexes['assets'].get(integrity.get('assetId')) if valid(integrity.get('assetId'), 'id') else None
        if asset and integrity.get('result') in ('MATCH', 'COMPUTED'):
            if (asset.get('canonicalContentHash') is not None
                    and (asset['canonicalContentHash'] != integrity.get('hashValue')
                         or asset.get('canonicalHashAlgorithm') != integrity.get('algorithm'))):
                finding('integrityRecords', index, 'hashValue', 'INTEGRITY_IDENTITY_MISMATCH')
        if asset and integrity.get('result') in ('MISMATCH', 'FAILED', 'PARTIAL'):
            eligibility.append(dict(collection='integrityRecords', index=index,
                                    code='NEGATIVE_OR_PARTIAL_INTEGRITY'))
        previous = indexes['integrityRecords'].get(integrity.get('previousIntegrityRecordId')) if valid(integrity.get('previousIntegrityRecordId'), 'id') else None
        if previous:
            if previous.get('assetId') != integrity.get('assetId') or previous is integrity:
                finding('integrityRecords', index, 'previousIntegrityRecordId', 'PREDECESSOR_MISMATCH')
            earlier, later = utc(previous.get('computedAtUtc')), utc(integrity.get('computedAtUtc'))
            if earlier and later and later < earlier:
                finding('integrityRecords', index, 'computedAtUtc', 'TIME_ORDER')
    # Bound predecessor traversal to the selected collection; equal-time cycles
    # cannot bypass the chronological check above.
    for index, integrity in enumerate(rows['integrityRecords']):
        if type(integrity) is not dict:
            continue
        seen, current = set(), integrity
        for _ in range(9):
            key = current.get('integrityRecordId')
            if not valid(key, 'id'):
                break
            if key in seen:
                finding('integrityRecords', index, 'previousIntegrityRecordId', 'PREDECESSOR_CYCLE')
                break
            seen.add(key)
            previous = current.get('previousIntegrityRecordId')
            if not valid(previous, 'id') or previous not in indexes['integrityRecords']:
                break
            current = indexes['integrityRecords'][previous]

    for index, relation in enumerate(rows['relations']):
        if type(relation) is dict and valid(relation.get('sourceAssetId'), 'id'):
            if relation['sourceAssetId'] == relation.get('targetAssetId'):
                finding('relations', index, 'targetAssetId', 'SELF_RELATION')
    original, preview = data.get('originalAssetId'), data.get('previewAssetId')
    selected_assets = []
    for field, identity in (('originalAssetId', original), ('previewAssetId', preview)):
        if valid(identity, 'id'):
            asset = indexes['assets'].get(identity)
            if asset is None:
                finding('selection', None, field, 'UNRESOLVED_REFERENCE')
            else:
                selected_assets.append(asset)
                if (asset.get('registrationStatus') in ('QUARANTINED', 'WITHDRAWN')
                        or asset.get('integrityStatus') in ('MISMATCH', 'UNREADABLE')
                        or asset.get('immutabilityStatus') == 'VIOLATION_DETECTED'):
                    eligibility.append(dict(collection='selection', field=field,
                                            code='ASSET_INELIGIBLE'))
                if not any(row.get('assetId') == identity for row in indexes['locators'].values()):
                    finding('selection', None, field, 'MISSING_LOCATOR')
                if not any(row.get('assetId') == identity for row in indexes['integrityRecords'].values()):
                    finding('selection', None, field, 'MISSING_INTEGRITY_RECORD')
    if not any(row.get('sourceAssetId') == preview and row.get('targetAssetId') == original
               and row.get('relationType') in ('DERIVED_FROM', 'PUBLICATION_VARIANT_OF')
               for row in indexes['relations'].values()) or not valid(original, 'id') or not valid(preview, 'id'):
        finding('selection', None, 'previewAssetId', 'MISSING_SELECTED_DERIVATIVE_RELATION')

    measurements = {}
    if measurement_source is None and measurement_digest is None:
        finding('measurements', None, None, 'MEASUREMENTS_UNAVAILABLE')
    else:
        measured = parse_selected_source(measurement_source, measurement_digest)
        if set(measured) != {'kind', 'items'} or measured.get('kind') != MEASUREMENTS:
            finding('measurements', None, None, 'UNSUPPORTED_FIELDS_OR_KIND')
        items = measured.get('items')
        if type(items) is not list or not 1 <= len(items) <= 8:
            finding('measurements', None, None, 'RECORD_COUNT')
            items = []
        groups = {}
        for index, item in enumerate(items):
            if type(item) is not dict or set(item) != set(MEASUREMENT_FIELDS):
                finding('measurements', index, None, 'INVALID_RECORD')
                continue
            valid_item = True
            for field, rule in MEASUREMENT_FIELDS.items():
                if not valid(item[field], rule):
                    finding('measurements', index, field, 'INVALID_VALUE')
                    valid_item = False
            if item['scope'] != 'FULL_FILE_BYTES':
                finding('measurements', index, 'scope', 'FULL_FILE_SCOPE_REQUIRED')
                valid_item = False
            if valid(item['assetId'], 'id'):
                groups.setdefault(item['assetId'], []).append((index, item, valid_item))
                if item['assetId'] not in indexes['assets']:
                    finding('measurements', index, 'assetId', 'UNRESOLVED_REFERENCE')
        for identity, group in groups.items():
            if len(group) != 1:
                for index, _, _ in group:
                    finding('measurements', index, 'assetId', 'DUPLICATE_ID')
            elif group[0][2]:
                measurements[identity] = group[0][1]

    for index, asset in enumerate(selected_assets):
        measurement = measurements.get(asset['assetId'])
        if measurement is None:
            finding('selectedAssets', index, None, 'FULL_FILE_MEASUREMENT_MISSING')
        elif (asset.get('canonicalHashAlgorithm') != 'SHA-256'
              or asset.get('canonicalContentHash') != measurement['sha256']
              or asset.get('sizeBytes') != measurement['sizeBytes']):
            finding('selectedAssets', index, None, 'MEASURED_IDENTITY_MISMATCH')
    return dict(kind='DSG_PRIVATE_ASSET_VALIDATION_REPORT_V1', sourceSha256=expected_digest,
                measurementSha256=measurement_digest, findings=findings, vocabularyGaps=gaps,
                eligibilityFindings=eligibility,
                structuralState='FINDINGS' if findings else 'NO_STRUCTURAL_FINDINGS',
                state='DRAFT_NOT_ACCEPTED', publicationState='PRIVATE_NOT_APPROVED',
                scientificAuthority='NONE', catalogWritePerformed=False, acceptanceEligible=False,
                unverified=['GLOBAL_IDENTITY_AND_STORAGE_GOVERNANCE', 'PROVENANCE_AND_RELATION_EVIDENCE',
                            'MEASUREMENT_AUTHENTICITY_SCOPE_AND_FRESHNESS', 'VOCABULARY_GOVERNANCE',
                            'FILESYSTEM_ALIAS_AND_AVAILABILITY_POLICY', 'EXPLICIT_REGISTRATION_AND_ACCEPTANCE',
                            'CURRENT_REVISION_WITHDRAWAL_AND_QUARANTINE', 'OPERATIONAL_RETENTION',
                            'CATALOG_CONTEXT_AND_EXACT_F4_BINDING', 'PUBLICATION_APPROVAL'])
