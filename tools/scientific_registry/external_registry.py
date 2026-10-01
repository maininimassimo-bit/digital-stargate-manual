"""Owner-approved retrospective external profile and private authority journal.

No image reads, inferred timestamps, public writes or automatic decisions.
Callers authenticate explicit decisions and refresh the independent journal head.
The local journal requires a trusted private directory; hashes are not signatures.
"""
from copy import deepcopy
import re

from tools.pixinsight.workflow_archive.archive import (
    checked_path, digest, encode, read_regular, write_immutable)
from tools.pixinsight.workflow_archive.binding import closed, identity, require
from .configuration_preflight import utc
from .catalog_context import local_date
from .draft_journal import parse_selected_source, sha

PROFILE = 'DSG_EXTERNAL_RETROSPECTIVE_V1'
MAX_EVENTS = 128
MAX_EVENT_BYTES = 1024 * 1024
FACTS = ('author', 'subject', 'acquisitionDate', 'site', 'telescope', 'camera',
         'nominalFocalLengthMm', 'headerFocalLengthMm', 'timezoneId',
         'validFromUtc', 'validToUtc', 'processingDate')
REQUIRED_FACTS = FACTS[:6]
CLASSES = ('OBSERVED', 'DECLARED', 'SUGGESTED', 'PARTIAL', 'UNAVAILABLE')
OPERATIONS = {'REGISTER': ('AP-013', 'REGISTER_EXACT_EXTERNAL_ASSETS'),
              'ADMIT': ('AP-014', 'ADMIT_EXTERNAL_RECORD_AND_EXACT_WORKFLOW_ASSOCIATION'),
              'WITHDRAW': ('AP-014', 'WITHDRAW_EXTERNAL_RECORD'),
              'QUARANTINE': ('AP-013', 'QUARANTINE_EXTERNAL_ASSETS')}
LIMITATIONS = ['EXTERNAL_ACQUISITION', 'PARTIAL_SCIENTIFIC_METADATA',
               'SUBJECT_IDENTIFICATION_NOT_INDEPENDENTLY_VERIFIED',
               'SCIENTIFIC_QUALITY_NOT_ASSESSED', 'WORKFLOW_ASSOCIATION_DECLARED']


def text(value, limit=512):
    require(type(value) is str and 0 < len(value) <= limit and bool(value.strip())
            and not any(ord(c) < 32 for c in value), 'EXTERNAL_TEXT')


def stamp(value):
    result = utc(value)
    require(result is not None, 'EXTERNAL_TIME')
    return result


def external_id(value):
    require(type(value) is str and re.fullmatch(r'EXT-[A-Z0-9-]{1,64}', value), 'EXTERNAL_ID')


def candidate(source, expected_digest):
    """Validate closed external metadata, keeping unknowns and field provenance.

    A valid candidate is not registered or admitted. Sources are references to
    independently retained private evidence; syntax proves no authenticity.
    """
    row = parse_selected_source(source, expected_digest)
    closed(row, {'kind', 'profile', 'acquisitionId', 'revision', 'facts', 'evidence',
                 'original', 'preview', 'workflow', 'metadataState', 'qualityState'})
    require(row['kind'] == 'DSG_EXTERNAL_CANDIDATE_V1' and row['profile'] == PROFILE,
            'EXTERNAL_PROFILE')
    external_id(row['acquisitionId'])
    require(type(row['revision']) is int and 1 <= row['revision'] <= MAX_EVENTS, 'EXTERNAL_REVISION')
    require(row['metadataState'] == 'PARTIAL' and row['qualityState'] == 'UNKNOWN', 'EXTERNAL_STATE')
    evidence = row['evidence']
    require(type(evidence) is list and 1 <= len(evidence) <= 64, 'EXTERNAL_EVIDENCE')
    evidence_ids = set()
    for item in evidence:
        closed(item, {'evidenceId', 'sha256', 'scope'})
        text(item['evidenceId'], 128); sha(item['sha256'])
        require(item['evidenceId'] not in evidence_ids, 'EXTERNAL_EVIDENCE_DUPLICATE')
        require(item['scope'] in ('OWNER_DECLARATION', 'HEADER_ONLY', 'DOCUMENT'), 'EXTERNAL_EVIDENCE_SCOPE')
        evidence_ids.add(item['evidenceId'])
    closed(row['facts'], FACTS)
    for name, fact in row['facts'].items():
        closed(fact, {'value', 'evidenceClass', 'evidenceRefs', 'reason'})
        require(fact['evidenceClass'] in CLASSES, 'EXTERNAL_EVIDENCE_CLASS')
        refs = fact['evidenceRefs']
        require(type(refs) is list and len(refs) <= 8
                and all(type(ref) is str and ref in evidence_ids for ref in refs)
                and len(set(refs)) == len(refs), 'EXTERNAL_EVIDENCE_REFERENCE')
        value = fact['value']
        if value is None:
            require(name not in REQUIRED_FACTS and fact['evidenceClass'] in ('UNAVAILABLE', 'PARTIAL'),
                    'EXTERNAL_REQUIRED_FACT')
            text(fact['reason'])
            continue
        require(fact['evidenceClass'] != 'UNAVAILABLE' and len(refs) > 0, 'EXTERNAL_FACT_SOURCE')
        if name in REQUIRED_FACTS:
            require(fact['evidenceClass'] in ('OBSERVED', 'DECLARED'), 'EXTERNAL_REQUIRED_FACT')
        if name in ('acquisitionDate', 'processingDate'):
            require(local_date(value) is not None, 'EXTERNAL_DATE')
        elif name in ('validFromUtc', 'validToUtc'):
            stamp(value)
            require(fact['evidenceClass'] in ('OBSERVED', 'DECLARED'), 'EXTERNAL_VALIDITY_EVIDENCE')
        elif name in ('nominalFocalLengthMm', 'headerFocalLengthMm'):
            require(type(value) in (int, float) and 0 < value <= 100000, 'EXTERNAL_FOCAL_LENGTH')
        else:
            text(value)
        require(fact['reason'] is None or type(fact['reason']) is str, 'EXTERNAL_FACT_REASON')
        if fact['reason'] is not None:
            text(fact['reason'])
    start, end = (row['facts'][field]['value'] for field in ('validFromUtc', 'validToUtc'))
    require(end is None or start is not None and stamp(end) > stamp(start), 'EXTERNAL_VALIDITY_ORDER')
    identity(row['original']); identity(row['preview'])
    require(row['original']['imageId'] != row['preview']['imageId']
            and row['original']['objectRef'] != row['preview']['objectRef'], 'EXTERNAL_DISTINCT_ASSETS')
    closed(row['workflow'], {'packetSha256', 'sourceSha256', 'workflowId'})
    sha(row['workflow']['packetSha256']); sha(row['workflow']['sourceSha256'])
    text(row['workflow']['workflowId'], 128)
    require(row['workflow']['workflowId'].startswith('archive:'), 'EXTERNAL_WORKFLOW')
    return row


def measurements(source, expected_digest, selected):
    """Require separately selected FULL_FILE_BYTES evidence for both exact assets."""
    row = parse_selected_source(source, expected_digest)
    closed(row, {'kind', 'measuredAtUtc', 'scope', 'items'})
    require(row['kind'] == 'DSG_EXTERNAL_MEASUREMENTS_V1' and row['scope'] == 'FULL_FILE_BYTES',
            'EXTERNAL_MEASUREMENT_SCOPE')
    stamp(row['measuredAtUtc'])
    require(type(row['items']) is list and len(row['items']) == 2, 'EXTERNAL_MEASUREMENT_COUNT')
    for item in row['items']:
        identity(item)
    require(row['items'] == [selected['original'], selected['preview']], 'EXTERNAL_MEASUREMENT_MISMATCH')
    return row


def decision(source, expected_digest):
    """Consume an explicit authenticated-by-caller act, never manufacture consent."""
    row = parse_selected_source(source, expected_digest)
    closed(row, {'kind', 'decisionId', 'operation', 'authority', 'scope', 'actor',
                 'decidedAtUtc', 'acquisitionId', 'candidateSha256', 'previousRecordSha256',
                 'measurementSha256', 'rationale'})
    require(row['kind'] == 'DSG_EXTERNAL_OWNER_DECISION_V1', 'EXTERNAL_DECISION_KIND')
    op = row['operation']
    require(type(op) is str and op in OPERATIONS, 'EXTERNAL_OPERATION')
    require((row['authority'], row['scope']) == OPERATIONS[op], 'EXTERNAL_DECISION_SCOPE')
    text(row['decisionId'], 128); text(row['actor'], 128); text(row['rationale'], 2048)
    external_id(row['acquisitionId']); stamp(row['decidedAtUtc']); sha(row['candidateSha256'])
    if row['previousRecordSha256'] is not None:
        sha(row['previousRecordSha256'])
    if op == 'REGISTER':
        sha(row['measurementSha256'])
    else:
        require(row['measurementSha256'] is None, 'EXTERNAL_DECISION_MEASUREMENT')
    return row


def build_event(decision_bytes, decision_digest, *, sequence, previous_digest,
                candidate_bytes=None, candidate_digest=None,
                measurement_bytes=None, measurement_digest=None):
    act = decision(decision_bytes, decision_digest)
    require(type(sequence) is int and 1 <= sequence <= MAX_EVENTS, 'EXTERNAL_SEQUENCE')
    if sequence == 1:
        require(previous_digest is None, 'EXTERNAL_PREVIOUS')
    else:
        sha(previous_digest)
    selected = measured = None
    if act['operation'] == 'REGISTER':
        require(candidate_digest == act['candidateSha256']
                and measurement_digest == act['measurementSha256'], 'EXTERNAL_DECISION_SOURCE')
        selected = candidate(candidate_bytes, candidate_digest)
        measured = measurements(measurement_bytes, measurement_digest, selected)
        require(selected['acquisitionId'] == act['acquisitionId'], 'EXTERNAL_DECISION_CONTEXT')
        require(stamp(measured['measuredAtUtc']) <= stamp(act['decidedAtUtc']), 'EXTERNAL_MEASUREMENT_TIME')
    else:
        require(all(value is None for value in (candidate_bytes, candidate_digest,
                measurement_bytes, measurement_digest)), 'EXTERNAL_UNEXPECTED_INPUT')
    # Retain selected source bytes exactly, not a normalized replacement.
    return dict(kind='DSG_EXTERNAL_EVENT_V1', sequence=sequence, previousSha256=previous_digest,
                decisionSource=decision_bytes.decode('utf-8'), decisionSha256=decision_digest,
                candidateSource=candidate_bytes.decode('utf-8') if selected else None,
                measurementSource=measurement_bytes.decode('utf-8') if measured else None,
                publicationState='PRIVATE_NOT_APPROVED')


def verify_event(raw):
    require(type(raw) is bytes and len(raw) <= MAX_EVENT_BYTES, 'EXTERNAL_EVENT_SIZE')
    # Event can contain up to three individually bounded original sources.
    import json
    from tools.pixinsight.workflow_archive.archive import ArchiveError
    try:
        row = json.loads(raw)
        closed(row, {'kind', 'sequence', 'previousSha256', 'decisionSource', 'decisionSha256',
                     'candidateSource', 'measurementSource', 'publicationState'})
        act = decision(row['decisionSource'].encode('utf-8'), row['decisionSha256'])
        args = {}
        if row['candidateSource'] is not None:
            args.update(candidate_bytes=row['candidateSource'].encode('utf-8'),
                        candidate_digest=act['candidateSha256'])
        if row['measurementSource'] is not None:
            args.update(measurement_bytes=row['measurementSource'].encode('utf-8'),
                        measurement_digest=act['measurementSha256'])
        rebuilt = build_event(row['decisionSource'].encode('utf-8'), row['decisionSha256'],
                              sequence=row['sequence'], previous_digest=row['previousSha256'], **args)
        require(encode(rebuilt) == raw, 'EXTERNAL_EVENT_CONTENT')
        return rebuilt, act
    except ArchiveError:
        raise
    except (KeyError, ValueError, TypeError, AttributeError, UnicodeError, RecursionError):
        raise ArchiveError('EXTERNAL_EVENT_CONTENT') from None


def replay(events, expected_head):
    """Replay a bounded global journal: stale records, identity reuse and revoke fail closed."""
    require(type(events) is list and len(events) <= MAX_EVENTS, 'EXTERNAL_EVENT_COUNT')
    if expected_head is not None:
        sha(expected_head)
    previous, last_time = None, None
    records, allocated, decisions = {}, {}, set()
    for index, raw in enumerate(events, 1):
        row, act = verify_event(raw)
        require(row['sequence'] == index and row['previousSha256'] == previous, 'EXTERNAL_CHAIN')
        now = stamp(act['decidedAtUtc'])
        require(last_time is None or now >= last_time, 'EXTERNAL_TIME_ORDER')
        require(act['decisionId'] not in decisions, 'EXTERNAL_DECISION_REUSED')
        decisions.add(act['decisionId'])
        key, op = act['acquisitionId'], act['operation']
        old = records.get(key)
        require(act['previousRecordSha256'] == (old['eventSha256'] if old else None), 'EXTERNAL_STALE_RECORD')
        event_digest = digest(raw)
        if op == 'REGISTER':
            selected = candidate(row['candidateSource'].encode('utf-8'), act['candidateSha256'])
            require(old is None and selected['revision'] == 1 or old is not None
                    and old['state'] in ('REGISTERED', 'ADMITTED')
                    and selected['revision'] == old['candidate']['revision'] + 1, 'EXTERNAL_REVISION_TRANSITION')
            for asset in (selected['original'], selected['preview']):
                # Permanent version allocation: same object/image ID cannot change its bytes.
                for field in ('imageId', 'objectRef'):
                    token = (field, asset[field])
                    claim = (key, encode(asset))
                    require(token not in allocated or allocated[token] == claim, 'EXTERNAL_ID_COLLISION')
                    allocated[token] = claim
            records[key] = dict(candidate=selected, candidateSha256=act['candidateSha256'],
                                candidateSource=row['candidateSource'], measurementSource=row['measurementSource'],
                                measurementSha256=act['measurementSha256'], state='REGISTERED',
                                registeredAtUtc=act['decidedAtUtc'], admittedAtUtc=None,
                                eventSha256=event_digest)
        else:
            require(old is not None and act['candidateSha256'] == old['candidateSha256'], 'EXTERNAL_DECISION_SOURCE')
            if op == 'ADMIT':
                require(old['state'] == 'REGISTERED', 'EXTERNAL_ADMISSION_TRANSITION')
                old['state'], old['admittedAtUtc'] = 'ADMITTED', act['decidedAtUtc']
            else:
                require(old['state'] in ('REGISTERED', 'ADMITTED'), 'EXTERNAL_REVOKE_TRANSITION')
                old['state'] = 'WITHDRAWN' if op == 'WITHDRAW' else 'QUARANTINED'
            old['eventSha256'] = event_digest
        previous, last_time = event_digest, now
    require(previous == expected_head, 'EXTERNAL_STALE_HEAD')
    return records


def load_events(directory, expected_head):
    root = checked_path(directory)
    require(root.is_dir(), 'EXTERNAL_DIRECTORY')
    paths = []
    for index, path in enumerate(root.iterdir()):
        require(index < 1024, 'EXTERNAL_DIRECTORY_LIMIT')
        if path.name.startswith('.bkl049-'):
            continue  # Private staging residue is never an accepted event.
        require(re.fullmatch(r'[0-9]{4}\.external\.json', path.name), 'EXTERNAL_DIRECTORY_CONTENT')
        paths.append(path)
    require(len(paths) <= MAX_EVENTS, 'EXTERNAL_EVENT_COUNT')
    paths.sort(key=lambda item: item.name)
    events = []
    for number, path in enumerate(paths, 1):
        require(path.name == f'{number:04d}.external.json', 'EXTERNAL_CHAIN_GAP')
        events.append(read_regular(path, MAX_EVENT_BYTES))
    replay(events, expected_head)
    return events


def retain_event(event, directory, *, expected_head):
    """One global sequence serializes allocation and decisions without overwriting.

    An exact retry uses the new independently retained head. Crashes after commit
    but before anchor update require operator reconciliation, never auto-adoption.
    """
    raw = encode(event)
    row, _ = verify_event(raw)
    events = load_events(directory, expected_head)
    if row['sequence'] == len(events):
        require(events[-1] == raw, 'EXTERNAL_EVENT_CONFLICT')
        outcome = 'DUPLICATE_NOOP'
    else:
        replay(events + [raw], digest(raw))
        outcome = write_immutable(raw, checked_path(directory) / f"{row['sequence']:04d}.external.json")
    return dict(outcome=outcome, sha256=digest(raw), sequence=row['sequence'],
                publicationState='PRIVATE_NOT_APPROVED')


def export_snapshot(events, current_head, acquisition_id, *, exported_at):
    """Export only a current admitted revision; never map PARTIAL/UNKNOWN to V1."""
    records = replay(events, current_head)
    external_id(acquisition_id)
    selected = records.get(acquisition_id)
    require(selected is not None and selected['state'] == 'ADMITTED', 'EXTERNAL_NOT_ADMITTED')
    export_time = stamp(exported_at)
    require(export_time >= stamp(selected['admittedAtUtc']), 'EXTERNAL_EXPORT_TIME')
    if events:
        _, latest = verify_event(events[-1])
        require(export_time >= stamp(latest['decidedAtUtc']), 'EXTERNAL_EXPORT_TIME')
    return deepcopy(dict(kind='BKL049_EXTERNAL_SNAPSHOT_V2', profile=PROFILE,
                         assetAuthority='AP-013', catalogAuthority='AP-014',
                         journalHeadSha256=current_head, acquisitionId=acquisition_id,
                         candidateSha256=selected['candidateSha256'], candidate=selected['candidate'],
                         recordEventSha256=selected['eventSha256'], admissionState='ADMITTED',
                         metadataState='PARTIAL', qualityState='UNKNOWN', exportedAtUtc=exported_at,
                         limitations=LIMITATIONS, publicationState='PRIVATE_NOT_APPROVED'))
