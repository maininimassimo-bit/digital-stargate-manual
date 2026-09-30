"""F0 fixed synthetic bridge only. No arbitrary input or real-source conversion."""
import json
from pathlib import Path
from read_export_subset import parse_export
STAMP = '2026-09-30T00:00:00Z'

def build():
    text = Path(__file__).with_name('synthetic-export.fixture.txt').read_text(encoding='utf-8')
    parsed = parse_export(text)
    artifact = 'synthetic:sha256:' + parsed['sourceSha256']
    steps = []
    def visit(name, path, parent=None, local_index=None):
        obj = parsed['instances'][name]
        if obj['process'] == 'ProcessContainer':
            for index, child in enumerate(obj['children']):
                visit(child, path + [name], name, index)
            return
        commands = [] if parent is None else [c for c in parsed['instances'][parent]['maskCommands'] if c['index'] == local_index]
        refs = list(dict.fromkeys(c['reference'] for c in commands if c['operation'] == 'setMask'))
        ordinal = len(steps) + 1
        steps.append({'stepId': 'SYNTHETIC-STEP-' + str(ordinal), 'ordinal': ordinal,
                      'processId': obj['process'], 'processVersion': None,
                      'evidenceClass': 'DECLARED', 'capturedAt': None,
                      'parameters': {'syntheticExportParameters': obj['parameters']},
                      'sourceLocators': [artifact, 'synthetic:container-path:' + '/'.join(path + [name])],
                      'notes': json.dumps({'researchOnly': True, 'localMaskCommands': commands}),
                      'declaredBy': 'SYNTHETIC-TEST-ACTOR', 'declaredAt': STAMP,
                      'inputRefs': [], 'outputRefs': [], 'maskRefs': refs})
    visit(parsed['root'], [])
    return {'schemaVersion': '1.0', 'sidecarId': 'PXP-SYNTHETIC-BRIDGE-001', 'exportedAt': STAMP,
            'authority': 'processing_evidence', 'actionAuthority': 'NONE',
            'source': {'product': 'PixInsight', 'productVersion': 'SYNTHETIC-NOT-RUNTIME',
                       'hostId': 'SYNTHETIC-HOST', 'workspaceId': 'SYNTHETIC-WORKSPACE',
                       'captureMethod': 'PROCESS_HISTORY_EXPORT', 'sourceLocators': [artifact]},
            'observationContext': {'sessionId': 'SYNTHETIC-SESSION', 'target': 'SYNTHETIC-TARGET',
                                   'projectId': 'SYNTHETIC-PROJECT', 'campaignId': None},
            'workflow': {'workflowId': 'SYNTHETIC-WORKFLOW', 'runId': 'SYNTHETIC-RUN',
                         'startedAt': None, 'completedAt': None, 'steps': steps,
                         # Invented test-only bindings; not inferred from expressions or view names.
                         'inputs': [{'reference': 'SYNTHETIC-INPUT', 'assetId': 'SYNTHETIC-INPUT', 'resolutionState': 'RESOLVED'}],
                         'outputs': [{'reference': 'SYNTHETIC-OUTPUT', 'assetId': 'SYNTHETIC-OUTPUT', 'resolutionState': 'RESOLVED'}]},
            'capture': {'completeness': 'PARTIAL', 'observedStepCount': 0, 'declaredStepCount': len(steps),
                        'limitations': ['SYNTHETIC ONLY; no executed workflow evidence',
                                        'Depth-first fixture order is not a proven global execution order',
                                        'Identity bindings are invented test inputs',
                                        'Parameter wrapper and note encoding are experiment-only, not accepted semantics',
                                        'Container-level inherited masks and full project graph not mapped']}}

if __name__ == '__main__':
    print(json.dumps(build(), indent=2))
