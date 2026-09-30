"""Atomic PRIVATE handoff bundle. No catalog writes or public delivery.

Persist original export and all binding inputs/results in one create-only file.
External trusted bundle/current-snapshot anchors are mandatory on every load.
"""
import json

from .archive import (ArchiveError, MAX_PACKET_BYTES, checked_path, digest, encode,
                      read_regular, verify_packet, write_immutable)
from .binding import build_binding, closed, require, trusted_record


KIND = 'BKL049_PRIVATE_DELIVERY_V1'


def build_delivery(packet_bytes, packet_digest, declaration, **binding_args):
    """Build from independently anchored inputs, using the unchanged F4 guard."""
    result = build_binding(packet_bytes, packet_digest, declaration, **binding_args)
    bundle = {
        'kind': KIND, 'publicationState': 'PRIVATE_NOT_APPROVED',
        'packet': verify_packet(packet_bytes, packet_digest),
        'packetSha256': packet_digest, 'declaration': declaration,
        'exportedAt': binding_args['exported_at'],
        'snapshot': trusted_record(binding_args['snapshot_bytes'], binding_args['snapshot_digest']),
        'snapshotSha256': binding_args['snapshot_digest'],
        'measurements': trusted_record(binding_args['measurement_bytes'], binding_args['measurement_digest']),
        'measurementSha256': binding_args['measurement_digest'],
        'association': trusted_record(binding_args['association_bytes'], binding_args['association_digest']),
        'associationSha256': binding_args['association_digest'], 'result': result,
    }
    # Return a detached canonical object, not aliases of caller-owned dictionaries.
    return json.loads(encode(bundle))


def verify_delivery(raw, expected_digest, current_snapshot_digest):
    """Reconstruct retained evidence before handoff; never trust stored results.

    The externally trusted bundle digest binds all embedded source anchors. It
    authenticates nothing by itself. The caller must refresh the authority's
    current snapshot digest; an old snapshot cannot authorize current delivery.
    """
    require(isinstance(raw, bytes) and len(raw) <= MAX_PACKET_BYTES, 'DELIVERY_SIZE_LIMIT')
    require(isinstance(expected_digest, str) and len(expected_digest) == 64
            and all(c in '0123456789abcdef' for c in expected_digest), 'DELIVERY_TRUST_REQUIRED')
    require(digest(raw) == expected_digest, 'DELIVERY_INTEGRITY')
    try:
        bundle = json.loads(raw)
        closed(bundle, {'kind', 'publicationState', 'packet', 'packetSha256', 'declaration',
                        'exportedAt', 'snapshot', 'snapshotSha256', 'measurements',
                        'measurementSha256', 'association', 'associationSha256', 'result'})
        require(bundle['kind'] == KIND and bundle['publicationState'] == 'PRIVATE_NOT_APPROVED',
                'DELIVERY_KIND')
        rebuilt = build_delivery(
            encode(bundle['packet']), bundle['packetSha256'], bundle['declaration'],
            exported_at=bundle['exportedAt'],
            snapshot_bytes=encode(bundle['snapshot']), snapshot_digest=bundle['snapshotSha256'],
            current_snapshot_digest=current_snapshot_digest,
            measurement_bytes=encode(bundle['measurements']), measurement_digest=bundle['measurementSha256'],
            association_bytes=encode(bundle['association']), association_digest=bundle['associationSha256'])
        require(encode(rebuilt) == raw, 'DELIVERY_CONTENT_MISMATCH')
        return rebuilt
    except ArchiveError:
        raise
    except (ValueError, KeyError, TypeError, UnicodeError, RecursionError):
        raise ArchiveError('DELIVERY_INVALID') from None


def retain_delivery(bundle, directory, current_snapshot_digest):
    """Commit one binding ID at one deterministic path. Returns a private receipt.

    Changed content under the same binding ID conflicts, including declaration,
    export time or context changes. A deliberate new binding ID is a revision,
    not a replacement. Caller must retain the returned digest independently.
    """
    raw = encode(bundle)
    verified = verify_delivery(raw, digest(raw), current_snapshot_digest)
    root = checked_path(directory)
    require(root.is_dir(), 'DELIVERY_DIRECTORY_REQUIRED')
    binding_id = verified['result']['receipt']['bindingId']
    filename = digest(binding_id.encode('utf-8')) + '.bkl049.json'
    outcome = write_immutable(raw, root / filename)
    return {'outcome': outcome, 'filename': filename, 'sha256': digest(raw),
            'bindingId': binding_id, 'publicationState': 'PRIVATE_NOT_APPROVED'}


def load_delivery(path, expected_digest, current_snapshot_digest):
    """Return only regenerated guard output to the private AP14-W06 caller."""
    raw = read_regular(path, MAX_PACKET_BYTES)
    return verify_delivery(raw, expected_digest, current_snapshot_digest)['result']
