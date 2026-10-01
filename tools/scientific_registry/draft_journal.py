"""Immutable private registration drafts; no acceptance or catalog export API.

Filesystem primitives are reused from the private archive utility only. No
PixInsight parsing, scientific normalization, image access or network occurs.
"""
import base64
import json
import re
from datetime import datetime

from tools.pixinsight.workflow_archive.archive import (
    ArchiveError, checked_path, digest, encode, read_regular, write_immutable)

MAX_SOURCE_BYTES = 256 * 1024
MAX_REVISION_BYTES = 512 * 1024
MAX_REVISIONS = 128
KIND = 'DSG_PRIVATE_REGISTRATION_DRAFT_V1'


def require(condition, code):
    if not condition:
        raise ArchiveError(code)


def sha(value):
    require(type(value) is str and re.fullmatch(r'[a-f0-9]{64}', value), 'REGISTRY_ANCHOR')


def build_draft(source, source_digest, *, submission_id, revision, previous_digest, recorded_at):
    """Preserve selected UTF-8 JSON bytes exactly, including unresolved fields.

    source_digest must be independently selected by the caller. No claim about
    source authenticity or scientific validity follows from hashing/parsing.
    """
    require(type(source) is bytes and 0 < len(source) <= MAX_SOURCE_BYTES, 'REGISTRY_SOURCE_SIZE')
    sha(source_digest)
    require(digest(source) == source_digest, 'REGISTRY_SOURCE_INTEGRITY')
    require(type(submission_id) is str and re.fullmatch(r'REG-[A-Z0-9-]{1,64}', submission_id),
            'REGISTRY_SUBMISSION_ID')
    require(type(revision) is int and 1 <= revision <= MAX_REVISIONS, 'REGISTRY_REVISION')
    if revision == 1:
        require(previous_digest is None, 'REGISTRY_PREVIOUS')
    else:
        sha(previous_digest)
    require(type(recorded_at) is str and re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', recorded_at),
            'REGISTRY_TIME')
    try:
        datetime.strptime(recorded_at, '%Y-%m-%dT%H:%M:%SZ')
        def pairs(items):
            out = {}
            for key, value in items:
                require(key not in out, 'REGISTRY_DUPLICATE_KEY')
                out[key] = value
            return out
        def reject_constant(value):
            raise ArchiveError('REGISTRY_SOURCE_JSON')
        parsed = json.loads(source.decode('utf-8'), object_pairs_hook=pairs,
                            parse_constant=reject_constant)
        require(type(parsed) is dict, 'REGISTRY_SOURCE_JSON')
        pending, count = [(parsed, 0)], 0
        while pending:
            value, depth = pending.pop()
            count += 1
            require(depth <= 32 and count <= 32768, 'REGISTRY_JSON_LIMIT')
            if type(value) is dict:
                pending.extend((child, depth + 1) for child in value.values())
            elif type(value) is list:
                pending.extend((child, depth + 1) for child in value)
        # Reject numeric overflow and bound canonical expansion, without using it
        # as a replacement for the retained original bytes.
        encode(parsed)
    except ArchiveError:
        raise
    except (ValueError, UnicodeError, TypeError, RecursionError):
        raise ArchiveError('REGISTRY_SOURCE_JSON') from None
    return {
        'kind': KIND, 'submissionId': submission_id, 'revision': revision,
        'previousSha256': previous_digest, 'recordedAt': recorded_at,
        'state': 'DRAFT_NOT_ACCEPTED', 'publicationState': 'PRIVATE_NOT_APPROVED',
        'scientificAuthority': 'NONE', 'catalogWritePerformed': False,
        'source': {'sha256': source_digest, 'byteSize': len(source),
                   'originalBase64': base64.b64encode(source).decode('ascii')},
    }


def verify_draft(raw, expected_digest):
    sha(expected_digest)
    require(type(raw) is bytes and len(raw) <= MAX_REVISION_BYTES
            and digest(raw) == expected_digest, 'REGISTRY_INTEGRITY')
    try:
        row = json.loads(raw)
        source = base64.b64decode(row['source']['originalBase64'], validate=True)
        rebuilt = build_draft(source, row['source']['sha256'], submission_id=row['submissionId'],
                              revision=row['revision'], previous_digest=row['previousSha256'],
                              recorded_at=row['recordedAt'])
        require(encode(rebuilt) == raw, 'REGISTRY_CONTENT')
        return rebuilt
    except ArchiveError:
        raise
    except (KeyError, ValueError, TypeError, UnicodeError, RecursionError):
        raise ArchiveError('REGISTRY_CONTENT') from None


def filename(submission_id, revision):
    return digest(submission_id.encode('ascii')) + f'.{revision:03d}.draft.json'


def load_chain(directory, submission_id, *, expected_head):
    """Check the entire bounded retained chain against a fresh external anchor.

    Caller owns authenticity, freshness and independent anchor retention. An
    obsolete anchor plus a rolled-back directory cannot prove currentness.
    """
    root = checked_path(directory)
    require(root.is_dir(), 'REGISTRY_DIRECTORY')
    require(type(submission_id) is str and re.fullmatch(r'REG-[A-Z0-9-]{1,64}', submission_id),
            'REGISTRY_SUBMISSION_ID')
    prefix = digest(submission_id.encode('ascii')) + '.'
    # Bound traversal as well as selected revisions. Use a dedicated directory.
    paths = []
    for index, path in enumerate(root.iterdir()):
        require(index < 1024, 'REGISTRY_DIRECTORY_LIMIT')
        if path.name.startswith(prefix):
            paths.append(path)
    require(len(paths) <= MAX_REVISIONS, 'REGISTRY_REVISION_LIMIT')
    paths.sort(key=lambda path: path.name)
    previous, last_time, result = None, None, []
    for number, path in enumerate(paths, 1):
        require(path.name == filename(submission_id, number), 'REGISTRY_CHAIN_GAP')
        raw = read_regular(path, MAX_REVISION_BYTES)
        row = verify_draft(raw, digest(raw))
        require(row['submissionId'] == submission_id and row['revision'] == number
                and row['previousSha256'] == previous, 'REGISTRY_CHAIN')
        require(last_time is None or last_time <= row['recordedAt'], 'REGISTRY_TIME_ORDER')
        previous, last_time = digest(raw), row['recordedAt']
        result.append(row)
    require(expected_head is None or type(expected_head) is str, 'REGISTRY_ANCHOR')
    if expected_head is not None:
        sha(expected_head)
    require(previous == expected_head, 'REGISTRY_STALE_HEAD')
    return result


def retain_draft(draft, directory, *, expected_head):
    """Create one revision, never overwrite; concurrent competing append conflicts.

    This is a draft-only journal. It has no scientific acceptance operation and
    cannot create the AP-013/AP-014 snapshot consumed by F4.
    """
    raw = encode(draft)
    row = verify_draft(raw, digest(raw))
    root = checked_path(directory)
    # Exact retry may use the already independently retained new head.
    chain = load_chain(root, row['submissionId'], expected_head=expected_head)
    if chain and row['revision'] == len(chain):
        require(encode(chain[-1]) == raw, 'REGISTRY_REVISION_CONFLICT')
        outcome = 'DUPLICATE_NOOP'
    else:
        require(row['revision'] == len(chain) + 1 and row['previousSha256'] == expected_head,
                'REGISTRY_STALE_HEAD')
        require(not chain or chain[-1]['recordedAt'] <= row['recordedAt'], 'REGISTRY_TIME_ORDER')
        outcome = write_immutable(raw, root / filename(row['submissionId'], row['revision']))
    return {'outcome': outcome, 'sha256': digest(raw), 'revision': row['revision'],
            'filename': filename(row['submissionId'], row['revision']),
            'state': 'DRAFT_NOT_ACCEPTED', 'publicationState': 'PRIVATE_NOT_APPROVED'}
