"""F3 private DECLARED/PARTIAL adapter. No binding or publication authority."""
from copy import deepcopy
from datetime import datetime
import json
from pathlib import Path
import re

from .archive import ArchiveError, encode, verify_packet

SCHEMA = Path(__file__).resolve().parents[3] / 'docs/contracts/pixinsight-workflow-provenance.schema.json'
ANNOTATIONS = {'$schema', '$id', 'title', '$defs', 'description'}
KEYWORDS = {'$ref', 'type', 'const', 'enum', 'required', 'properties', 'additionalProperties',
            'items', 'maxItems', 'minItems', 'maxProperties', 'maxLength', 'minLength', 'pattern',
            'minimum', 'format'}


def utc_stamp(value):
    if not isinstance(value, str) or not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z', value):
        raise ArchiveError('DECLARATION_TIME_INVALID')
    try:
        datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        raise ArchiveError('DECLARATION_TIME_INVALID') from None
    return value


def bounded_text(value, limit):
    if not isinstance(value, str) or not value.strip():
        raise ArchiveError('CONTEXT_TEXT_INVALID')
    try:
        if len(value.encode('utf-16-le')) // 2 > limit:
            raise ArchiveError('CONTEXT_TEXT_LIMIT')
    except UnicodeError:
        raise ArchiveError('CONTEXT_TEXT_INVALID') from None
    return value


def validate_emitted_profile(value, schema=None):
    """Evaluate every constraint used by the pinned PXP schema, fail on new keywords.

    Not a generic JSON Schema engine. Input is the bounded constructed F3 profile;
    unconstrained parameter values are secured by verified source reconstruction.
    """
    if schema is None:
        schema = json.loads(SCHEMA.read_text(encoding='utf-8'))
    root = schema

    def check(item, rule, depth=0):
        if depth > 40 or not isinstance(rule, dict) or set(rule) - KEYWORDS - ANNOTATIONS:
            raise ArchiveError('PROFILE_SCHEMA_UNSUPPORTED')
        if '$ref' in rule:
            reference = rule['$ref']
            if not reference.startswith('#/$defs/') or reference.count('/') != 2:
                raise ArchiveError('PROFILE_SCHEMA_UNSUPPORTED')
            try:
                check(item, root['$defs'][reference.split('/')[-1]], depth + 1)
            except KeyError:
                raise ArchiveError('PROFILE_SCHEMA_UNSUPPORTED') from None
        if 'type' in rule:
            allowed = rule['type'] if isinstance(rule['type'], list) else [rule['type']]
            types = {'object': dict, 'array': list, 'string': str, 'integer': int, 'null': type(None), 'boolean': bool}
            if any(x not in types for x in allowed):
                raise ArchiveError('PROFILE_SCHEMA_UNSUPPORTED')
            if type(item) not in [types[x] for x in allowed]:
                raise ArchiveError('PROFILE_TYPE')
        if 'const' in rule and item != rule['const']:
            raise ArchiveError('PROFILE_CONST')
        if 'enum' in rule and item not in rule['enum']:
            raise ArchiveError('PROFILE_ENUM')
        if isinstance(item, dict):
            if not set(rule.get('required', [])).issubset(item):
                raise ArchiveError('PROFILE_REQUIRED')
            if len(item) > rule.get('maxProperties', len(item)):
                raise ArchiveError('PROFILE_PROPERTY_LIMIT')
            properties = rule.get('properties', {})
            if rule.get('additionalProperties') is False and set(item) - set(properties):
                raise ArchiveError('PROFILE_EXTRA_PROPERTY')
            for key, child in item.items():
                if key in properties:
                    check(child, properties[key], depth + 1)
        if isinstance(item, list):
            if len(item) > rule.get('maxItems', len(item)) or len(item) < rule.get('minItems', 0):
                raise ArchiveError('PROFILE_ARRAY_LIMIT')
            if 'items' in rule:
                for child in item:
                    check(child, rule['items'], depth + 1)
        if isinstance(item, str):
            if len(item) > rule.get('maxLength', len(item)) or len(item) < rule.get('minLength', 0):
                raise ArchiveError('PROFILE_STRING_LIMIT')
            if 'pattern' in rule and re.search(rule['pattern'], item) is None:
                raise ArchiveError('PROFILE_PATTERN')
            if 'format' in rule:
                if rule['format'] != 'date-time':
                    raise ArchiveError('PROFILE_SCHEMA_UNSUPPORTED')
                utc_stamp(item)
        if type(item) is int and 'minimum' in rule and item < rule['minimum']:
            raise ArchiveError('PROFILE_MINIMUM')
    check(value, schema)
    return True


def build_sidecar(packet_bytes, expected_packet_digest, declaration, *, exported_at):
    packet = verify_packet(packet_bytes, expected_packet_digest)
    archive = packet['archive']
    if archive is None:
        raise ArchiveError('SOURCE_UNSUPPORTED')
    required = {'declaredBy', 'declaredAt', 'sourceSha256', 'scope'}
    optional = {'sessionId', 'target', 'productVersion'}
    if not isinstance(declaration, dict) or not required.issubset(declaration) or set(declaration) - required - optional:
        raise ArchiveError('DECLARATION_INVALID')
    if declaration['scope'] != 'EXPORTED_CONFIGURATIONS_ONLY' or declaration['sourceSha256'] != packet['source']['sha256']:
        raise ArchiveError('DECLARATION_SOURCE_MISMATCH')
    actor = bounded_text(declaration['declaredBy'], 256)
    declared_at = utc_stamp(declaration['declaredAt'])
    exported_at = utc_stamp(exported_at)
    if exported_at < packet['importedAt'] or exported_at < declared_at:
        raise ArchiveError('EXPORT_TIME_CONFLICT')
    # The supplied attestation clock is distinct from the receipt/import clock.
    receipt = packet['receiptId']
    source_ref = 'receipt:' + receipt
    steps = []
    stack = [(archive['root'], [])]
    while stack:
        name, parents = stack.pop()
        instance = archive['instances'][name]
        if instance['process'] == 'ProcessContainer':
            stack.extend((child, parents + [name]) for child in reversed(instance['children']))
            continue
        steps.append({
            'stepId': f'step-{len(steps) + 1:04d}', 'ordinal': len(steps) + 1,
            'processId': instance['process'], 'processVersion': None,
            'evidenceClass': 'DECLARED', 'capturedAt': None,
            'parameters': {'bkl049LexicalV1': {
                'exportParameters': deepcopy(instance['parameters']),
                'sourceInstance': name, 'containerPath': parents,
            }},
            'sourceLocators': [source_ref + '#instance=' + name],
            'declaredBy': actor, 'declaredAt': declared_at,
            'inputRefs': [], 'outputRefs': [], 'maskRefs': [],
        })
    sidecar = {
        'schemaVersion': '1.0', 'sidecarId': 'PXP-' + receipt,
        'exportedAt': exported_at, 'authority': 'processing_evidence', 'actionAuthority': 'NONE',
        'source': {'product': 'PixInsight', 'productVersion': bounded_text(declaration.get('productVersion', 'unknown'), 64),
                   'hostId': 'unknown', 'workspaceId': 'unknown', 'captureMethod': 'PROCESS_HISTORY_EXPORT',
                   'sourceLocators': [source_ref]},
        'observationContext': {'sessionId': bounded_text(declaration.get('sessionId', 'unknown'), 128),
                               'target': bounded_text(declaration.get('target', 'unknown'), 256)},
        'workflow': {'workflowId': 'archive:' + receipt, 'runId': 'import:' + receipt,
                     'startedAt': None, 'completedAt': None, 'steps': steps, 'inputs': [], 'outputs': []},
        'capture': {'completeness': 'PARTIAL' if steps else 'UNAVAILABLE',
                    'observedStepCount': 0, 'declaredStepCount': len(steps),
                    'limitations': [
                        'Configuration/export order is declared, not observed execution or complete chronology.',
                        'Archive/import identifiers are not original PixInsight run identifiers; historical times/versions remain unknown.',
                        'Lexical encoding bkl049LexicalV1 preserves source values without native semantic conversion.',
                        'Inputs, outputs and mask associations are unresolved. Ordered mask commands remain in the private source packet.',
                        'No authoritative image/version binding, public classification or gallery acceptance is established.',
                        'The coarse manifest is lossy; retain this sidecar and its original private packet together.',
                    ]},
    }
    validate_emitted_profile(sidecar)
    encode(sidecar)  # F2 packet-size ceiling also bounds the constructed sidecar.
    return sidecar
