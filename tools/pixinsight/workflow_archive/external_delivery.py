"""Versioned external F4/PXP private delivery; legacy scientific guard unchanged.

The source journal is replayed, not replaced by a self-asserted eligible snapshot.
Current journal and measurement anchors must be selected independently by caller.
"""
import json

from tools.scientific_registry.external_registry import (
    export_snapshot, measurements, stamp, LIMITATIONS)
from .archive import (ArchiveError, MAX_PACKET_BYTES, checked_path, digest, encode,
                      read_regular, verify_packet, write_immutable)
from .binding import closed, require
from .provenance import build_sidecar

KIND = 'BKL049_EXTERNAL_DELIVERY_V2'


def build_external_delivery(packet_bytes, packet_digest, declaration, *, events,
                            current_head, acquisition_id, measurement_bytes,
                            measurement_digest, exported_at):
    """Create a detached PRIVATE bundle after replaying exact admission and identity.

    Owner admission scope includes the exact candidate's workflow association;
    the processing declaration only describes exported configuration evidence.
    No admission is inferred from the latter, filenames or matching subject names.
    """
    snapshot = export_snapshot(events, current_head, acquisition_id, exported_at=exported_at)
    selected = snapshot['candidate']
    measured = measurements(measurement_bytes, measurement_digest, selected)
    require(stamp(measured['measuredAtUtc']) <= stamp(exported_at), 'EXTERNAL_DELIVERY_TIME')
    packet = verify_packet(packet_bytes, packet_digest)
    require(selected['workflow'] == {'packetSha256': packet_digest,
            'sourceSha256': packet['source']['sha256'], 'workflowId': 'archive:' + packet['receiptId']},
            'EXTERNAL_WORKFLOW_IDENTITY')
    require(type(declaration) is dict and 'sessionId' not in declaration and 'target' not in declaration,
            'EXTERNAL_NO_SESSION_ALIAS')
    sidecar = build_sidecar(packet_bytes, packet_digest, declaration, exported_at=exported_at)
    # New envelope is intentionally not a legacy AP14-W06/PXP V1 input.
    sidecar['schemaVersion'] = '2.0'
    sidecar['kind'] = 'BKL049_EXTERNAL_PXP_V2'
    sidecar['observationContext'] = dict(externalAcquisitionId=acquisition_id,
                                       metadataState='PARTIAL', qualityState='UNKNOWN')
    sidecar['workflow']['outputs'] = [dict(reference=selected['original']['objectRef'],
                                         resolutionState='RESOLVED', assetId=selected['original']['imageId'])]
    # Remove exactly the two statements superseded by this separate guard.
    replaced = {
        'Inputs, outputs and mask associations are unresolved. Ordered mask commands remain in the private source packet.':
            'The exact original output is bound to the admitted external record. Upstream inputs, step-level outputs and masks remain unresolved.',
        'No authoritative image/version binding, public classification or gallery acceptance is established.':
            'Original, preview and workflow identities match the admitted external record. Scientific metadata remains partial and quality unknown; publication is not authorized.',
    }
    require(set(replaced).issubset(sidecar['capture']['limitations']), 'EXTERNAL_F3_PROFILE_DRIFT')
    sidecar['capture']['limitations'] = [replaced.get(item, item) for item in sidecar['capture']['limitations']]
    sidecar['capture']['limitations'].extend(LIMITATIONS)
    bundle = dict(kind=KIND, profile=snapshot['profile'], publicationState='PRIVATE_NOT_APPROVED',
                  journal=[json.loads(raw) for raw in events], journalHeadSha256=current_head,
                  packet=packet, packetSha256=packet_digest, declaration=declaration,
                  measurementSource=measurement_bytes.decode('utf-8'), measurementSha256=measurement_digest,
                  acquisitionId=acquisition_id, exportedAtUtc=exported_at,
                  result=dict(snapshot=snapshot, sidecar=sidecar,
                              original=selected['original'], preview=selected['preview'],
                              associationEvidenceClass='DECLARED', actionAuthority='NONE'))
    raw = encode(bundle)
    require(len(raw) <= MAX_PACKET_BYTES, 'EXTERNAL_DELIVERY_SIZE')
    return json.loads(raw)


def verify_external_delivery(raw, expected_digest, current_head):
    """Regenerate the whole bundle against a fresh independent journal head."""
    require(type(raw) is bytes and len(raw) <= MAX_PACKET_BYTES and digest(raw) == expected_digest,
            'EXTERNAL_DELIVERY_INTEGRITY')
    try:
        row = json.loads(raw)
        closed(row, {'kind', 'profile', 'publicationState', 'journal', 'journalHeadSha256',
                     'packet', 'packetSha256', 'declaration', 'measurementSource', 'measurementSha256',
                     'acquisitionId', 'exportedAtUtc', 'result'})
        require(row['journalHeadSha256'] == current_head, 'EXTERNAL_DELIVERY_STALE')
        require(type(row['journal']) is list and len(row['journal']) <= 128, 'EXTERNAL_EVENT_COUNT')
        rebuilt = build_external_delivery(encode(row['packet']), row['packetSha256'], row['declaration'],
                    events=[encode(event) for event in row['journal']], current_head=current_head,
                    acquisition_id=row['acquisitionId'], measurement_bytes=row['measurementSource'].encode('utf-8'),
                    measurement_digest=row['measurementSha256'], exported_at=row['exportedAtUtc'])
        require(encode(rebuilt) == raw, 'EXTERNAL_DELIVERY_CONTENT')
        return rebuilt
    except ArchiveError:
        raise
    except (KeyError, ValueError, TypeError, AttributeError, UnicodeError, RecursionError):
        raise ArchiveError('EXTERNAL_DELIVERY_CONTENT') from None


def retain_external_delivery(bundle, directory, current_head):
    raw = encode(bundle)
    verify_external_delivery(raw, digest(raw), current_head)
    root = checked_path(directory)
    require(root.is_dir(), 'EXTERNAL_DELIVERY_DIRECTORY')
    filename = digest(raw) + '.external-pxp.json'
    return dict(outcome=write_immutable(raw, root / filename), filename=filename,
                sha256=digest(raw), publicationState='PRIVATE_NOT_APPROVED')


def load_external_delivery(path, expected_digest, current_head):
    return verify_external_delivery(read_regular(path, MAX_PACKET_BYTES), expected_digest, current_head)['result']
