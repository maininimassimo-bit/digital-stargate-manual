"""F5 allowlisted projection builder; no publication, network or catalog writes.

The caller supplies independently trusted, current delivery/selection anchors.
Hashes bind bytes, not permission: an approval record must come from the Owner's
governed field review. Never manufacture it from a candidate in production.
"""
import json
from pathlib import Path
import re

from .archive import digest, encode
from .binding import closed, require, trusted_record
from .delivery import verify_delivery
from .provenance import bounded_text, utc_stamp, validate_emitted_profile

SCHEMA = Path(__file__).resolve().parents[3] / 'schemas/bkl049-public-workflow.schema.json'
MAX_PUBLIC_BYTES = 256 * 1024
MAX_VALUE_CHARACTERS = 4096
GAPS = ['PARTIAL_HISTORY', 'EXECUTION_NOT_OBSERVED', 'UPSTREAM_RELATIONS_UNRESOLVED',
        'PROCESS_VERSIONS_UNAVAILABLE', 'PUBLIC_FIELDS_OMITTED']
CITATION = 'architecture/assessments/BKL-049-F1-Workflow-Archive-Architecture/'


def public_id(value, prefix):
    require(isinstance(value, str) and re.fullmatch(prefix + r'-[A-Za-z0-9_-]{1,64}', value),
            'PUBLIC_ID_INVALID')
    return value


def build_public_projection(delivery_bytes, delivery_digest, current_snapshot_digest,
                            selection_bytes, selection_digest, current_selection_digest):
    """Return detached public fields only, or a fixed diagnostic.

    A new delivery revision or withdrawn/replaced selection invalidates approval.
    No routes, arbitrary notes, actor identities, source hashes or private IDs are
    copied. Parameter names AND exact lexical values require individual approval.
    Returned fields are text data, never HTML, JavaScript or replay instructions.
    """
    require(selection_digest == current_selection_digest, 'PUBLIC_SELECTION_STALE')
    bundle = verify_delivery(delivery_bytes, delivery_digest, current_snapshot_digest)
    selection = trusted_record(selection_bytes, selection_digest)
    closed(selection, {'kind', 'scope', 'deliverySha256', 'approvedBy', 'approvedAt',
                       'imageId', 'imageVersionId', 'workflowId', 'steps'})
    require(selection['kind'] == 'BKL049_PRIVATE_PUBLIC_SELECTION_V1'
            and selection['scope'] == 'EXACT_WORKFLOW_FIELDS_ONLY', 'PUBLIC_SELECTION_SCOPE')
    require(selection['deliverySha256'] == delivery_digest, 'PUBLIC_SELECTION_SOURCE')
    bounded_text(selection['approvedBy'], 256)
    utc_stamp(selection['approvedAt'])
    require(selection['approvedAt'] >= bundle['exportedAt'], 'PUBLIC_SELECTION_TIME')
    image_id = public_id(selection['imageId'], 'IMG')
    version_id = public_id(selection['imageVersionId'], 'VER')
    workflow_id = public_id(selection['workflowId'], 'WF')
    source = bundle['result']['sidecar']['workflow']['steps']
    steps = select_steps(source, selection['steps'])
    output = {
        'schemaVersion': '1.0', 'kind': 'BKL049_PUBLIC_WORKFLOW',
        'authority': 'processing_evidence', 'actionAuthority': 'NONE',
        'imageId': image_id, 'imageVersionId': version_id, 'workflowId': workflow_id,
        'bindingEvidenceClass': 'DECLARED', 'captureCompleteness': 'PARTIAL' if steps else 'UNAVAILABLE',
        'executionEvidence': 'NOT_ESTABLISHED', 'orderSemantics': 'EXPORTED_CONFIGURATION_ORDER',
        'methodCitation': CITATION, 'steps': steps,
        'omittedStepCount': len(source) - len(steps), 'gaps': list(GAPS),
    }
    # This schema is additive; existing PXP/catalog/gallery contracts stay closed.
    validate_emitted_profile(output, json.loads(SCHEMA.read_text(encoding='utf-8')))
    require(len(encode(output)) <= MAX_PUBLIC_BYTES, 'PUBLIC_OUTPUT_LIMIT')
    return output


def select_steps(source, selected):
    """Shared exact allowlist projection after a profile-specific authority check."""
    require(type(selected) is list and len(selected) <= 512, 'PUBLIC_STEP_LIMIT')
    by_id = {step['stepId']: step for step in source}
    steps, seen = [], set()
    for entry in selected:
        closed(entry, {'stepId', 'processId', 'parameters'})
        step_id = entry['stepId']
        require(isinstance(step_id, str) and step_id in by_id, 'PUBLIC_STEP_UNKNOWN')
        require(step_id not in seen, 'PUBLIC_STEP_DUPLICATE')
        seen.add(step_id)
        original = by_id[step_id]
        require(entry['processId'] == original['processId'], 'PUBLIC_PROCESS_MISMATCH')
        require(re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]{0,127}', original['processId']),
                'PUBLIC_PROCESS_INVALID')
        selected_params = entry['parameters']
        require(type(selected_params) is list and len(selected_params) <= 128, 'PUBLIC_PARAMETER_LIMIT')
        original_params = original['parameters']['bkl049LexicalV1']['exportParameters']
        params, names = [], set()
        for param in selected_params:
            closed(param, {'name', 'valueSha256'})
            name = param['name']
            require(isinstance(name, str) and name in original_params, 'PUBLIC_PARAMETER_UNKNOWN')
            require(name not in names, 'PUBLIC_PARAMETER_DUPLICATE')
            names.add(name)
            require(re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]{0,127}', name), 'PUBLIC_PARAMETER_NAME')
            value_bytes = encode(original_params[name])
            require(param['valueSha256'] == digest(value_bytes), 'PUBLIC_PARAMETER_CHANGED')
            # Preserve the tagged lexical representation; do not evaluate or coerce.
            value = value_bytes.decode('ascii')
            require(len(value) <= MAX_VALUE_CHARACTERS, 'PUBLIC_VALUE_LIMIT')
            params.append({'name': name, 'lexicalJson': value})
        steps.append({'sourceOrdinal': original['ordinal'], 'processId': original['processId'],
                      'evidenceClass': 'DECLARED', 'parameters': params,
                      'omittedParameterCount': len(original_params) - len(params)})
    steps.sort(key=lambda step: step['sourceOrdinal'])
    return steps
