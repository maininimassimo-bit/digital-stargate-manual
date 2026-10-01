"""Private AP14-W02 candidate checks. Findings never create catalog authority."""
import re
from datetime import date

from tools.pixinsight.workflow_archive.archive import digest, encode
from .configuration_preflight import check_configuration, utc
from .draft_journal import parse_selected_source


KIND = 'DSG_PRIVATE_CATALOG_CONTEXT_CANDIDATE_V1'
MAX_ROWS = 8
COMMON = dict(schemaVersion='text', recordVersion='version', createdAtUtc='utc',
              updatedAtUtc='utc', sourceSystem='text', sourceVersion='text', sourceDigest='digest')
REQUIRED = {
    'projects': dict(projectId='projectId', projectName='text200', projectType='unresolved',
                     priority='priority', status='projectStatus'),
    'campaigns': dict(campaignId='campaignId', projectId='projectId', campaignName='text200',
                      status='unresolved'),
    'targets': dict(targetId='targetId', canonicalName='text200', targetType='targetType'),
    'observations': dict(observationId='observationId', campaignId='campaignId', targetId='targetId',
                         observationTitle='text250', observationMode='observationMode',
                         priority='priority', status='unresolved', completionState='unresolved'),
    'sessions': dict(sessionId='id', observationId='observationId', localObservingDate='date',
                     observatoryId='id', instrumentConfigurationId='id', sessionStatus='sessionStatus',
                     qualityState='qualityState'),
    'catalogItems': dict(catalogItemId='catalogItemId', entityType='sessionEntity', entityId='id',
                         catalogState='catalogState', qualityState='qualityState',
                         reconciliationState='reconciliationState'),
}
OPTIONAL = {
    'projects': dict(objective='text4000', ownerId='id', startedAt='date',
                     targetCompletionDate='date', completedAt='date'),
    'campaigns': dict(objective='text4000', validFrom='date', validTo='date',
                      completionCriteria='unsupportedDetail'),
    'targets': dict(alternativeNames='uniqueTexts', rightAscensionDeg='ra', declinationDeg='dec',
                    constellation='text', catalogReferences='unsupportedDetail'),
    'observations': dict(scientificObjective='text4000', requiredIntegrationByFilter='integration',
                         achievedIntegrationByFilter='integration'),
    'sessions': dict(startedAtUtc='utc', completedAtUtc='utc', operatorId='id',
                     sourceReference='text', transferState='unresolved'),
    'catalogItems': dict(indexedAtUtc='utc', lastReconciledAtUtc='utc',
                         supersedesCatalogItemId='catalogItemId'),
}
KEYS = dict(projects='projectId', campaigns='campaignId', targets='targetId',
            observations='observationId', sessions='sessionId', catalogItems='catalogItemId')
PATTERNS = {
    'projectId': r'PRJ-[0-9]{4}-[0-9]{3}', 'campaignId': r'CAM-[0-9]{4}-[0-9]{3}',
    'targetId': r'TGT-[A-Z0-9]+-[A-Z0-9-]+', 'observationId': r'OBS-[0-9]{8}-[0-9]{3}',
    'catalogItemId': r'CAT-[A-Z]+-[A-Z0-9-]+', 'id': r'[A-Za-z0-9._:-]{1,128}',
    'digest': r'sha256:[a-f0-9]{64}',
}
# AP14-W01 6.1, 6.13 and 9; target taxonomy: DSDM-002 4.1.
ENUMS = {
    'projectStatus': ('PLANNED', 'ACTIVE', 'ON_HOLD', 'READY_FOR_PROCESSING', 'PROCESSING',
                      'REVIEW', 'COMPLETED', 'ARCHIVED'),
    'targetType': ('GALAXY', 'NEBULA', 'PLANETARY_NEBULA', 'STAR_CLUSTER', 'GLOBULAR_CLUSTER',
                   'OPEN_CLUSTER', 'SUPERNOVA_REMNANT', 'COMET', 'PLANET', 'MOON', 'STAR',
                   'DARK_NEBULA', 'WIDE_FIELD', 'OTHER', 'UNKNOWN'),
    'observationMode': ('BROADBAND', 'NARROWBAND', 'LUMINANCE', 'RGB', 'SHO', 'HOO', 'LRGB',
                        'SURVEY', 'CALIBRATION', 'ENGINEERING', 'OTHER'),
    'sessionStatus': ('PLANNED', 'READY', 'RUNNING', 'COMPLETED', 'PARTIAL', 'FAILED', 'CANCELLED',
                      'ACCEPTED', 'ARCHIVED'),
    'qualityState': ('UNKNOWN', 'PENDING', 'ACCEPTABLE', 'ACCEPTED', 'REJECTED', 'DEGRADED', 'SUPERSEDED'),
    'catalogState': ('DISCOVERED', 'NORMALIZED', 'INDEXABLE', 'INDEXED', 'SUPERSEDED', 'WITHDRAWN'),
    'reconciliationState': ('MATCHED', 'MISSING_SOURCE', 'MISSING_PROJECTION', 'STALE_PROJECTION',
                            'CONFLICT', 'RESOLVED'),
    'sessionEntity': ('OBSERVATION_SESSION',),
}


def local_date(value):
    if type(value) is not str or not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', value):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def valid(value, rule):
    if rule in PATTERNS:
        return (type(value) is str and len(value) <= 128 and re.fullmatch(PATTERNS[rule], value)
                is not None and value.upper() not in ('UNKNOWN', 'UNAVAILABLE', 'NULL'))
    if rule in ENUMS:
        return type(value) is str and value in ENUMS[rule]
    if rule == 'utc':
        return utc(value) is not None
    if rule == 'date':
        return local_date(value) is not None
    if rule in ('version', 'priority'):
        return type(value) is int and 1 <= value <= (5 if rule == 'priority' else 2147483647)
    if rule in ('ra', 'dec'):
        return type(value) in (float, int) and (0 <= value < 360 if rule == 'ra' else -90 <= value <= 90)
    if rule == 'uniqueTexts':
        return (type(value) is list and len(value) <= 32
                and all(valid(item, 'text200') for item in value) and len(set(value)) == len(value))
    if rule == 'integration':
        return (type(value) is dict and len(value) <= 32 and all(valid(key, 'id')
                and type(amount) in (int, float) and amount >= 0 for key, amount in value.items()))
    if rule == 'unsupportedDetail':
        return False
    limit = int(rule[4:]) if rule.startswith('text') and rule[4:] else 2048
    return type(value) is str and 0 < len(value) <= limit and bool(value.strip())


def check_catalog_context(source, expected_digest):
    """Check selected candidate records and references without defaults or writes.

    Bounded profile: 1..8 records per collection, session-only catalog items, one
    selected configuration. Source/provenance and vocabulary authority are not
    established by a matching digest or by successful structural checks.
    """
    data = parse_selected_source(source, expected_digest)
    findings, vocabulary_gaps = [], []

    def finding(collection, index, field, code):
        findings.append(dict(collection=collection, index=index, field=field, code=code))

    if set(data) - {'kind', 'configurationSelection', *REQUIRED}:
        finding('selection', None, None, 'UNSUPPORTED_FIELDS')
    if data.get('kind') != KIND:
        finding('selection', None, 'kind', 'UNSUPPORTED_KIND')
    configuration = data.get('configurationSelection')
    if type(configuration) is not dict:
        finding('configurationSelection', None, None, 'REQUIRED_RECORD')
        configuration = {}
    config_raw = encode(configuration)
    config_report = check_configuration(config_raw, digest(config_raw))
    rows, indexes = {}, {}
    for collection, fields in REQUIRED.items():
        selected = data.get(collection)
        indexes[collection] = {}
        if type(selected) is not list or not 1 <= len(selected) <= MAX_ROWS:
            finding(collection, None, None, 'RECORD_COUNT')
            rows[collection] = []
            continue
        rows[collection] = selected
        rules = {**COMMON, **fields, **OPTIONAL[collection]}
        identities = {}
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
                    continue
                if not valid(value, rule):
                    finding(collection, index, field,
                            'UNSUPPORTED_DETAIL' if rule == 'unsupportedDetail' else 'INVALID_VALUE')
                elif rule == 'unresolved':
                    vocabulary_gaps.append(dict(collection=collection, index=index, field=field,
                                                code='VOCABULARY_UNRESOLVED'))
            key = KEYS[collection]
            identity = row.get(key)
            if valid(identity, fields[key]):
                identities.setdefault(identity, []).append(index)
            for earlier, later, parser in (
                    ('createdAtUtc', 'updatedAtUtc', utc), ('startedAtUtc', 'completedAtUtc', utc),
                    ('startedAt', 'completedAt', local_date),
                    ('startedAt', 'targetCompletionDate', local_date), ('validFrom', 'validTo', local_date)):
                start, end = parser(row.get(earlier)), parser(row.get(later))
                if start and end and end < start:
                    finding(collection, index, later, 'TIME_ORDER')
            if collection == 'catalogItems':
                if row.get('catalogState') == 'INDEXED' and row.get('reconciliationState') == 'CONFLICT':
                    finding(collection, index, 'catalogState', 'CONFLICT_INDEXED')
                if identity is not None and row.get('supersedesCatalogItemId') == identity:
                    finding(collection, index, 'supersedesCatalogItemId', 'SELF_REFERENCE')
        for identity, positions in identities.items():
            if len(positions) > 1:
                for index in positions:
                    finding(collection, index, KEYS[collection], 'DUPLICATE_ID')
            else:
                indexes[collection][identity] = selected[positions[0]]

    def resolve(collection, index, row, field, destination):
        value = row.get(field)
        if not valid(value, 'id'):
            return None
        target = indexes[destination].get(value)
        if target is None:
            finding(collection, index, field, 'UNRESOLVED_REFERENCE')
        return target

    relations = (('campaigns', 'projectId', 'projects'), ('observations', 'campaignId', 'campaigns'),
                 ('observations', 'targetId', 'targets'), ('sessions', 'observationId', 'observations'),
                 ('catalogItems', 'entityId', 'sessions'),
                 ('catalogItems', 'supersedesCatalogItemId', 'catalogItems'))
    for collection, field, destination in relations:
        for index, row in enumerate(rows[collection]):
            if type(row) is dict and row.get(field) is not None:
                resolve(collection, index, row, field, destination)

    names, entities = set(), set()
    for index, target in enumerate(rows['targets']):
        if type(target) is dict and valid(target.get('canonicalName'), 'text200'):
            name = target['canonicalName'].casefold()
            if name in names:
                finding('targets', index, 'canonicalName', 'DUPLICATE_NAME')
            names.add(name)
    for index, item in enumerate(rows['catalogItems']):
        if type(item) is not dict:
            continue
        if valid(item.get('entityId'), 'id') and valid(item.get('recordVersion'), 'version'):
            identity = (item.get('entityType') if type(item.get('entityType')) is str else None,
                        item['entityId'], item['recordVersion'])
            if identity in entities:
                finding('catalogItems', index, 'entityId', 'DUPLICATE_ENTITY_VERSION')
            entities.add(identity)

    config = configuration.get('configuration')
    config = config if type(config) is dict else {}
    site = configuration.get('observatory')
    site = site if type(site) is dict else {}
    for index, session in enumerate(rows['sessions']):
        if type(session) is not dict:
            continue
        for field, expected in (('instrumentConfigurationId', config.get('instrumentConfigurationId')),
                                ('observatoryId', site.get('observatoryId'))):
            if session.get(field) is not None and (not valid(expected, 'id') or session[field] != expected):
                finding('sessions', index, field, 'CONFIGURATION_REFERENCE_MISMATCH')
        lower, upper = utc(config.get('validFromUtc')), utc(config.get('validToUtc'))
        for field in ('startedAtUtc', 'completedAtUtc'):
            instant = utc(session.get(field))
            if instant and ((lower and instant < lower) or (upper and instant > upper)):
                finding('sessions', index, field, 'OUTSIDE_CONFIGURATION_INTERVAL')

    return dict(kind='DSG_PRIVATE_CATALOG_CONTEXT_REPORT_V1', sourceSha256=expected_digest,
                profile='AP14-W02-2.3-3-4.1-4.5-4.12-SELECTED-CONTEXT',
                structuralState='FINDINGS' if findings or config_report['findings'] else 'NO_STRUCTURAL_FINDINGS',
                findings=findings, vocabularyGaps=vocabulary_gaps, configurationReport=config_report,
                state='DRAFT_NOT_ACCEPTED', publicationState='PRIVATE_NOT_APPROVED', scientificAuthority='NONE',
                acceptanceEligible=False, catalogWritePerformed=False,
                unverified=['VOCABULARY_GOVERNANCE', 'GLOBAL_IDENTITY_ALLOCATION_AND_COLLISIONS',
                            'SOURCE_PROVENANCE_AND_DIGEST_MEANING', 'HISTORICAL_CONFIGURATION_VALIDITY',
                            'LOCAL_OBSERVING_DATE_AND_TIMEZONE', 'ASSET_REGISTRATION_DECISION',
                            'CATALOG_ACCEPTANCE_DECISION', 'OPERATIONAL_RETENTION_AND_CURRENT_SNAPSHOT',
                            'EXACT_F4_BINDING', 'PUBLICATION_APPROVAL'])
