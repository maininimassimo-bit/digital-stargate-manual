// Synthetic only. The binding guard runs before existing reconciliation.
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { validatePixInsightWorkflowProvenance } from './pixinsight-workflow-provenance.mjs';
import { provenanceSidecarToManifest } from './pixinsight-provenance-to-manifest.mjs';
import { validateManifest } from './pixinsight-manifest.mjs';
import { PixInsightReconciliationService } from './pixinsight-reconciliation.mjs';

const child = spawnSync('python', ['-c',
  'import json; from tools.pixinsight.workflow_archive.test_delivery import retained_handoff; print(json.dumps(retained_handoff()))'],
{ cwd: fileURLToPath(new URL('../../', import.meta.url)), shell: false, encoding: 'utf8', timeout: 10000, maxBuffer: 1024 * 1024 });
assert.equal(child.status, 0, 'Synthetic F4 guard failed');
const { receipt, sidecar, reconciliationInput } = JSON.parse(child.stdout);
assert.equal(validatePixInsightWorkflowProvenance(sidecar).valid, true);
const manifest = provenanceSidecarToManifest(sidecar);
assert.equal(validateManifest(manifest).valid, true);
assert.deepEqual(manifest.processingRun.outputs, [receipt.original.imageId]);
assert.equal(sidecar.workflow.outputs[0].reference, receipt.original.objectRef);
const result = new PixInsightReconciliationService(reconciliationInput).reconcile(manifest, { reconciledAt: sidecar.exportedAt });
assert.equal(result.state, 'matched');
assert.equal(result.session.matched, true);
assert.equal(result.outputs.requested, 1);
assert.equal(result.outputs.matched, 1);
assert.deepEqual(result.outputs.missing, []);
assert.deepEqual(manifest.processingRun.processes, []);
assert.equal(manifest.processingRun.parameters.captureCompleteness, 'PARTIAL');
assert.ok(manifest.processingRun.parameters.limitations.some(text => text.includes('mandatory original output is verified against the selected snapshot')));
assert.ok(!manifest.processingRun.parameters.limitations.some(text => text.startsWith('No authoritative image/version binding')));
assert.equal(receipt.evidenceClass, 'DECLARED');
assert.equal(receipt.publicationState, 'PRIVATE_NOT_APPROVED');
// A bare reconciliation can match a wrong object; it must never bypass this guard.
assert.equal(Object.hasOwn(reconciliationInput.assets[0], 'sha256'), false);
console.log('BKL-049 F4 guard bridge PASS: exact mandatory original handed to AP14-W06; DECLARED/PARTIAL and private publication state retained.');
