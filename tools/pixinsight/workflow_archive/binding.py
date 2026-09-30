"""Private single-output binding guard. Consumes authority; never grants it.

Trusted digests must be independently governed, not recomputed from candidates.
No image reads, catalog writes, network, publication or native execution.
"""
from copy import deepcopy
import json
import re

from .archive import ArchiveError, digest, encode, verify_packet
from .provenance import build_sidecar, bounded_text, utc_stamp, validate_emitted_profile

MAX_RECORD_BYTES = 256 * 1024
ID = r'[A-Za-z0-9._:-]{1,128}'
SHA = r'[a-f0-9]{64}'
IDENTITY = {'imageId', 'objectRef', 'sha256', 'byteSize'}


def require(condition, code):
    if not condition:
        raise ArchiveError(code)


def closed(value, keys):
    require(type(value) is dict and set(value) == set(keys), 'BINDING_FIELDS')


def identifier(value):
    require(isinstance(value, str) and re.fullmatch(ID, value) is not None
            and value.lower() not in {'unknown', 'unavailable', 'null'}, 'BINDING_ID')
    return value


def identity(value):
    closed(value, IDENTITY)
    identifier(value['imageId'])
    identifier(value['objectRef'])
    require(value['objectRef'].startswith('obj:'), 'BINDING_OBJECT_REF')
    require(isinstance(value['sha256'], str) and re.fullmatch(SHA, value['sha256']) is not None,
            'BINDING_DIGEST')
    require(type(value['byteSize']) is int and 1 <= value['byteSize'] <= 1099511627776,
            'BINDING_BYTE_SIZE')
    return value


def trusted_record(raw, expected):
    require(isinstance(expected, str) and re.fullmatch(SHA, expected) is not None,
            'BINDING_TRUST_ANCHOR_REQUIRED')
    require(isinstance(raw, bytes) and len(raw) <= MAX_RECORD_BYTES and digest(raw) == expected,
            'BINDING_RECORD_INTEGRITY')
    try:
        value = json.loads(raw)
        # Canonical input also rejects duplicate keys, NaN and trailing material.
        require(encode(value) == raw, 'BINDING_NONCANONICAL')
    except (ValueError, TypeError, UnicodeError, RecursionError):
        raise ArchiveError('BINDING_RECORD_INVALID') from None
    return value


def unique(rows, key):
    require(type(rows) is list and 1 <= len(rows) <= 8, 'BINDING_RECORD_COUNT')
    values = []
    for row in rows:
        require(type(row) is dict and key in row, 'BINDING_FIELDS')
        values.append(identifier(row[key]))
    require(len(set(values)) == len(values), 'BINDING_DUPLICATE_ID')


def asset_identity(asset):
    return {key: asset[key] for key in IDENTITY}


def build_binding(packet_bytes, packet_digest, declaration, *, exported_at,
                  snapshot_bytes, snapshot_digest, current_snapshot_digest,
                  measurement_bytes, measurement_digest,
                  association_bytes, association_digest):
    """Return a private receipt plus reconstructed sidecar, or a fixed error code.

    Narrow first profile: one mandatory original output, one preview, no inferred
    upstream assets. All snapshots/measurements/attestations are selected by an
    authorized caller; a hash authenticates none of them. Current snapshot anchor
    must be refreshed by that caller before every regeneration.
    """
    require(current_snapshot_digest == snapshot_digest, 'BINDING_STALE_SNAPSHOT')
    packet = verify_packet(packet_bytes, packet_digest)
    sidecar = build_sidecar(packet_bytes, packet_digest, declaration, exported_at=exported_at)
    snapshot = trusted_record(snapshot_bytes, snapshot_digest)
    measurements = trusted_record(measurement_bytes, measurement_digest)
    association = trusted_record(association_bytes, association_digest)

    closed(snapshot, {'kind', 'revision', 'catalogAuthority', 'assetAuthority', 'catalogItems', 'assets'})
    require(snapshot['kind'] == 'BKL049_PRIVATE_BINDING_SNAPSHOT_V1'
            and snapshot['catalogAuthority'] == 'AP-014' and snapshot['assetAuthority'] == 'AP-013',
            'BINDING_AUTHORITY')
    identifier(snapshot['revision'])
    unique(snapshot['catalogItems'], 'entityId')
    unique(snapshot['catalogItems'], 'catalogItemId')
    unique(snapshot['assets'], 'imageId')
    unique(snapshot['assets'], 'objectRef')
    for item in snapshot['catalogItems']:
        closed(item, {'entityId', 'catalogItemId', 'qualityState', 'targetRef'})
        identifier(item['targetRef'])
        require(item['targetRef'].startswith('target:'), 'BINDING_TARGET')
        require(isinstance(item['qualityState'], str)
                and item['qualityState'] in {'ACCEPTED', 'WITHDRAWN', 'UNAVAILABLE'}, 'BINDING_CATALOG_STATE')
    for asset in snapshot['assets']:
        closed(asset, IDENTITY | {'archiveState', 'metadataState', 'sessionRef', 'targetRef', 'derivativeRefs'})
        identity(asset_identity(asset))
        identifier(asset['sessionRef']); identifier(asset['targetRef'])
        require(asset['sessionRef'].startswith('session:') and asset['targetRef'].startswith('target:'),
                'BINDING_CONTEXT_REF')
        require(isinstance(asset['archiveState'], str) and isinstance(asset['metadataState'], str)
                and asset['archiveState'] in {'CATALOGED', 'QUARANTINED', 'UNAVAILABLE'}
                and asset['metadataState'] in {'COMPLETE', 'PARTIAL', 'UNAVAILABLE'}, 'BINDING_ASSET_STATE')
        refs = asset['derivativeRefs']
        require(type(refs) is list and len(refs) <= 8, 'BINDING_DERIVATIVE_REFS')
        for ref in refs:
            identifier(ref)
        require(len(set(refs)) == len(refs), 'BINDING_DUPLICATE_ID')

    closed(measurements, {'kind', 'measuredAt', 'items'})
    require(measurements['kind'] == 'BKL049_PRIVATE_MEASUREMENTS_V1', 'BINDING_MEASUREMENT_KIND')
    utc_stamp(measurements['measuredAt'])
    require(measurements['measuredAt'] <= exported_at, 'BINDING_TIME_ORDER')
    unique(measurements['items'], 'imageId')
    unique(measurements['items'], 'objectRef')
    for item in measurements['items']:
        identity(item)

    closed(association, {'kind', 'bindingId', 'declaredBy', 'declaredAt', 'evidenceClass',
                         'scope', 'packetSha256', 'sourceSha256', 'workflowId', 'snapshotSha256',
                         'original', 'preview'})
    require(association['kind'] == 'BKL049_PRIVATE_ASSOCIATION_V1'
            and association['evidenceClass'] == 'DECLARED'
            and association['scope'] == 'WORKFLOW_TO_ORIGINAL_AND_PREVIEW', 'BINDING_DECLARATION_SCOPE')
    identifier(association['bindingId'])
    bounded_text(association['declaredBy'], 256)
    utc_stamp(association['declaredAt'])
    require(association['declaredAt'] <= exported_at, 'BINDING_TIME_ORDER')
    require(association['packetSha256'] == packet_digest
            and association['sourceSha256'] == packet['source']['sha256']
            and association['workflowId'] == sidecar['workflow']['workflowId']
            and association['snapshotSha256'] == snapshot_digest, 'BINDING_UNRELATED_SOURCE')
    original = identity(association['original'])
    preview = identity(association['preview'])
    require(original['imageId'] != preview['imageId'] and original['objectRef'] != preview['objectRef'],
            'BINDING_DERIVATIVE_IDENTITY')

    # Only build maps after validating uniqueness throughout the supplied snapshot.
    assets = {a['imageId']: a for a in snapshot['assets']}
    measured = {a['imageId']: a for a in measurements['items']}
    selected = []
    for expected in (original, preview):
        candidate = assets.get(expected['imageId'])
        require(candidate is not None, 'BINDING_ASSET_MISSING')
        require(asset_identity(candidate) == expected and measured.get(expected['imageId']) == expected,
                'BINDING_IDENTITY_MISMATCH')
        require(candidate['archiveState'] == 'CATALOGED' and candidate['metadataState'] == 'COMPLETE',
                'BINDING_ASSET_INELIGIBLE')
        selected.append(candidate)
    main, derivative = selected
    require(preview['objectRef'] in main['derivativeRefs'], 'BINDING_DERIVATIVE_MISSING')
    require(main['sessionRef'] == derivative['sessionRef'] and main['targetRef'] == derivative['targetRef'],
            'BINDING_DERIVATIVE_CONTEXT')
    session_id = main['sessionRef'][len('session:'):]
    target_id = main['targetRef'][len('target:'):]
    identifier(session_id); identifier(target_id)
    catalog = next((c for c in snapshot['catalogItems'] if c['entityId'] == session_id), None)
    require(catalog is not None and catalog['qualityState'] == 'ACCEPTED'
            and catalog['targetRef'] == main['targetRef'], 'BINDING_CATALOG_INELIGIBLE')
    require(sidecar['observationContext'] == {'sessionId': session_id, 'target': target_id},
            'BINDING_SIDECAR_CONTEXT')

    # Relation is DECLARED separately; process evidence and upstream gaps unchanged.
    sidecar = deepcopy(sidecar)
    sidecar['workflow']['outputs'] = [{'reference': main['objectRef'], 'resolutionState': 'RESOLVED',
                                      'assetId': main['imageId']}]
    limitation_updates = {
        'Inputs, outputs and mask associations are unresolved. Ordered mask commands remain in the private source packet.':
            'The mandatory original output is verified against the selected snapshot. Upstream inputs, step-level outputs and masks remain unresolved; ordered mask commands remain in the private source packet.',
        'No authoritative image/version binding, public classification or gallery acceptance is established.':
            'Original/preview identity is verified against the selected governed snapshot with an Owner-declared workflow association. Current eligibility must be rechecked; public classification and gallery acceptance are not established.',
    }
    require(set(limitation_updates).issubset(sidecar['capture']['limitations']), 'BINDING_F3_PROFILE_DRIFT')
    sidecar['capture']['limitations'] = [limitation_updates.get(item, item)
                                         for item in sidecar['capture']['limitations']]
    validate_emitted_profile(sidecar)
    receipt = {
        'kind': 'BKL049_PRIVATE_BINDING_V1', 'bindingId': association['bindingId'],
        'state': 'VERIFIED_AGAINST_SELECTED_SNAPSHOT', 'evidenceClass': 'DECLARED',
        'publicationState': 'PRIVATE_NOT_APPROVED', 'authority': 'processing_evidence',
        'actionAuthority': 'NONE', 'snapshotRevision': snapshot['revision'],
        'snapshotSha256': snapshot_digest, 'packetSha256': packet_digest,
        'measurementSha256': measurement_digest, 'associationSha256': association_digest,
        'sidecarSha256': digest(encode(sidecar)), 'original': original, 'preview': preview,
        'catalogItemId': catalog['catalogItemId'], 'exportedAt': exported_at,
        'captureCompleteness': sidecar['capture']['completeness'],
        'limitations': ['UPSTREAM_ASSETS_UNRESOLVED', 'ASSOCIATION_OWNER_DECLARED',
                        'REVALIDATE_CURRENT_SNAPSHOT_BEFORE_USE', 'PUBLICATION_NOT_AUTHORIZED'],
    }
    return {'receipt': receipt, 'sidecar': sidecar,
            'reconciliationInput': {'catalogItems': [deepcopy(catalog)],
                'assets': [{'assetId': main['imageId'], 'integrityState': 'VERIFIED'}]}}


def compare_retained(candidate, retained_bytes, retained_digest):
    """Classify retry only. Caller retains receipts immutably; no write is performed."""
    retained = trusted_record(retained_bytes, retained_digest)
    require(type(retained) is dict, 'BINDING_RECEIPT_KIND')
    require(type(candidate) is dict and candidate.get('kind') == 'BKL049_PRIVATE_BINDING_V1',
            'BINDING_RECEIPT_KIND')
    require(retained.get('kind') == candidate['kind'] and retained.get('bindingId') == candidate.get('bindingId'),
            'BINDING_RETAINED_ID')
    require(encode(candidate) == retained_bytes, 'BINDING_RECEIPT_CONFLICT')
    return 'DUPLICATE_NOOP'
