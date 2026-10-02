"""Approved-field external projection and bounded local collection publisher.

No cloud calls, credentials, uploads or automatic Git publication. Production
caller authenticates exact publication approvals and refreshes all current heads.
"""
import json
import os
from pathlib import Path
import re
import tempfile

from .archive import ArchiveError, checked_path, digest, encode, read_regular
from .binding import closed, require, trusted_record
from .external_delivery import verify_external_delivery
from .provenance import bounded_text, utc_stamp, validate_emitted_profile
from .public_projection import GAPS, MAX_PUBLIC_BYTES, public_id, select_steps
from tools.scientific_registry.configuration_preflight import utc

SCHEMA = Path(__file__).resolve().parents[3] / 'schemas/bkl049-public-workflow-external.schema.json'
CONTEXT = dict(origin='EXTERNAL', metadataState='PARTIAL', qualityState='UNKNOWN',
               subjectIdentification='DECLARED_NOT_INDEPENDENTLY_VERIFIED')
CITATION = 'architecture/ADR-019-External-Retrospective-Scientific-Records/'
MAX_COLLECTION_BYTES = 2 * 1024 * 1024
PREVIEW_PATTERN = r'https://storage\.googleapis\.com/[a-z0-9][a-z0-9.-]{1,220}/[A-Za-z0-9_-][A-Za-z0-9_/-]*\.(?:jpg|jpeg|png|webp)'


def public_text(value, limit):
    bounded_text(value, limit)
    require(not any(ord(char) < 32 for char in value), 'EXTERNAL_PUBLIC_TEXT')
    return value


def build_external_projection(*, delivery_bytes, delivery_digest, current_head,
                              selection_bytes, selection_digest, current_selection_digest,
                              now):
    require(selection_digest == current_selection_digest, 'PUBLIC_SELECTION_STALE')
    utc_stamp(now)
    bundle = verify_external_delivery(delivery_bytes, delivery_digest, current_head)
    selected = trusted_record(selection_bytes, selection_digest)
    closed(selected, {'kind', 'scope', 'deliverySha256', 'approvedBy', 'approvedAt', 'validUntil',
                      'rightsConfirmed', 'imageId', 'imageVersionId', 'workflowId', 'title',
                      'attribution', 'preview', 'steps'})
    persistent = selected['kind'] == 'BKL049_EXTERNAL_PUBLIC_SELECTION_V3'
    require((persistent or selected['kind'] == 'BKL049_EXTERNAL_PUBLIC_SELECTION_V2')
            and selected['scope'] == 'EXACT_EXTERNAL_PREVIEW_AND_WORKFLOW'
            and selected['rightsConfirmed'] is True, 'EXTERNAL_PUBLIC_APPROVAL')
    require(selected['deliverySha256'] == delivery_digest, 'PUBLIC_SELECTION_SOURCE')
    bounded_text(selected['approvedBy'], 256)
    utc_stamp(selected['approvedAt'])
    require(bundle['exportedAtUtc'] <= selected['approvedAt'] <= now,
            'EXTERNAL_PUBLIC_APPROVAL_TIME')
    if persistent:
        require(selected['validUntil'] is None, 'EXTERNAL_PUBLIC_APPROVAL_WINDOW')
    else:
        utc_stamp(selected['validUntil'])
        require(now < selected['validUntil'], 'EXTERNAL_PUBLIC_APPROVAL_TIME')
        require((utc(selected['validUntil']) - utc(selected['approvedAt'])).total_seconds() <= 86400,
                'EXTERNAL_PUBLIC_APPROVAL_WINDOW')
    closed(selected['preview'], {'url', 'alt', 'sha256'})
    preview = selected['preview']
    require(type(preview['url']) is str and len(preview['url']) <= 1024
            and re.fullmatch(PREVIEW_PATTERN, preview['url']), 'EXTERNAL_PUBLIC_URL')
    require(preview['sha256'] == bundle['result']['preview']['sha256'], 'EXTERNAL_PUBLIC_PREVIEW_IDENTITY')
    source = bundle['result']['sidecar']['workflow']['steps']
    steps = select_steps(source, selected['steps'])
    result = dict(schemaVersion='2.0', kind='BKL049_PUBLIC_EXTERNAL_WORKFLOW',
                  authority='processing_evidence', actionAuthority='NONE',
                  imageId=public_id(selected['imageId'], 'IMG'),
                  imageVersionId=public_id(selected['imageVersionId'], 'VER'),
                  workflowId=public_id(selected['workflowId'], 'WF'),
                  bindingEvidenceClass='DECLARED', captureCompleteness='PARTIAL' if steps else 'UNAVAILABLE',
                  executionEvidence='NOT_ESTABLISHED', orderSemantics='EXPORTED_CONFIGURATION_ORDER',
                  methodCitation=CITATION, steps=steps, omittedStepCount=len(source) - len(steps), gaps=list(GAPS),
                  scientificContext=dict(CONTEXT), title=public_text(selected['title'], 200),
                  attribution=public_text(selected['attribution'], 256),
                  preview=dict(url=preview['url'], alt=public_text(preview['alt'], 300)))
    validate_emitted_profile(result, json.loads(SCHEMA.read_text(encoding='utf-8')))
    require(len(encode(result)) <= MAX_PUBLIC_BYTES, 'PUBLIC_OUTPUT_LIMIT')
    return result


def build_external_collection(entries, *, published_at, valid_until, now):
    """Whole selected external collection, never merge with stale cached projections.

    Empty selection withdraws every workflow; the legacy empty V1 collection is
    preserved. A future mixed publisher is not inferred by merging existing rows.
    """
    utc_stamp(now)
    require(type(entries) is list and len(entries) <= 8, 'EXTERNAL_PUBLIC_COUNT')
    records, images, workflows = [], set(), set()
    persistent = bool(entries) and valid_until is None
    if entries:
        utc_stamp(published_at)
        require(published_at <= now, 'EXTERNAL_PUBLIC_WINDOW')
        if not persistent:
            utc_stamp(valid_until)
            require(now < valid_until
                    and 0 < (utc(valid_until) - utc(published_at)).total_seconds() <= 86400,
                    'EXTERNAL_PUBLIC_WINDOW')
    else:
        require(published_at is None and valid_until is None, 'EXTERNAL_PUBLIC_EMPTY')
    for entry in entries:
        closed(entry, {'delivery_bytes', 'delivery_digest', 'current_head', 'selection_bytes',
                      'selection_digest', 'current_selection_digest'})
        result = build_external_projection(**entry, now=now)
        approval = trusted_record(entry['selection_bytes'], entry['selection_digest'])
        require(approval['approvedAt'] <= published_at, 'EXTERNAL_PUBLIC_RELEASE_WINDOW')
        if persistent:
            require(approval['kind'] == 'BKL049_EXTERNAL_PUBLIC_SELECTION_V3'
                    and approval['validUntil'] is None, 'EXTERNAL_PUBLIC_RELEASE_WINDOW')
        else:
            require(approval['kind'] == 'BKL049_EXTERNAL_PUBLIC_SELECTION_V2'
                    and valid_until <= approval['validUntil'], 'EXTERNAL_PUBLIC_RELEASE_WINDOW')
        key = (result['imageId'], result['imageVersionId'])
        require(key not in images and result['workflowId'] not in workflows, 'EXTERNAL_PUBLIC_DUPLICATE')
        images.add(key); workflows.add(result['workflowId']); records.append(result)
    collection = dict(schemaVersion='2.0' if persistent else '1.0', kind='BKL049_PUBLIC_COLLECTION', authority='processing_evidence',
                      actionAuthority='NONE', publishedAt=published_at, validUntil=valid_until, records=records)
    require(len(encode(collection)) <= MAX_COLLECTION_BYTES, 'EXTERNAL_PUBLIC_COLLECTION_SIZE')
    return collection


def publish_external_collection(entries, output, *, expected_previous_digest,
                                published_at, valid_until, now):
    """Replace one explicitly selected local collection after fresh reconstruction.

    Requires trusted local parent, cooperating writers and an independent prior
    file digest. Lock excludes concurrent publishers; stale disk content rejects.
    No network publication, preview upload or URL-content verification is implied.
    """
    target = checked_path(output)
    require(target.name == 'bkl049-public-workflows.json', 'EXTERNAL_PUBLIC_TARGET')
    lock = target.with_name('.bkl049-publication.lock')
    temporary = None
    cleanup_pending = False
    receipt = None
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except OSError:
        raise ArchiveError('EXTERNAL_PUBLICATION_LOCKED') from None
    try:
        os.close(descriptor)
        previous = read_regular(target, MAX_COLLECTION_BYTES)
        require(digest(previous) == expected_previous_digest, 'EXTERNAL_PUBLICATION_CONFLICT')
        collection = build_external_collection(entries, published_at=published_at, valid_until=valid_until, now=now)
        raw = encode(collection) + b'\n'
        if raw == previous:
            receipt = dict(outcome='DUPLICATE_NOOP', sha256=digest(raw), records=len(collection['records']))
        else:
            with tempfile.NamedTemporaryFile(dir=target.parent, prefix='.bkl049-release-', delete=False) as stream:
                temporary = Path(stream.name)
                stream.write(raw); stream.flush(); os.fsync(stream.fileno())
            # Recheck immediately before atomic replacement; hostile parent/admin is out of scope.
            require(read_regular(target, MAX_COLLECTION_BYTES) == previous, 'EXTERNAL_PUBLICATION_CONFLICT')
            os.replace(temporary, target)
            temporary = None
            receipt = dict(outcome='LOCAL_COLLECTION_REPLACED', sha256=digest(raw), records=len(collection['records']))
    except OSError:
        raise ArchiveError('EXTERNAL_PUBLICATION_IO') from None
    finally:
        for residue in (temporary, lock):
            if residue is not None:
                try:
                    residue.unlink(missing_ok=True)
                except OSError:
                    cleanup_pending = True
    receipt['cleanupPending'] = cleanup_pending
    return receipt
