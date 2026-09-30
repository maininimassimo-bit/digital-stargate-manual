// Synthetic-only integration test. Executes repository Python, never exported JS.
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { validatePixInsightWorkflowProvenance } from './pixinsight-workflow-provenance.mjs';
import { provenanceSidecarToManifest } from './pixinsight-provenance-to-manifest.mjs';
import { validateManifest } from './pixinsight-manifest.mjs';
import { PixInsightSynchronizationLedger } from './pixinsight-ledger.mjs';
import { PixInsightReconciliationService } from './pixinsight-reconciliation.mjs';
import { PixInsightProcessingProjectionBuilder } from './pixinsight-processing-projection.mjs';
import { buildPixInsightProvenanceReadModel } from './pixinsight-provenance-read-model.mjs';

const child = spawnSync('python', ['-c',
  'import json; from tools.pixinsight.workflow_archive.test_provenance import sample, sidecar_for; p,d=sample(); print(json.dumps(sidecar_for(p,d)))'],
{ cwd: fileURLToPath(new URL('../../', import.meta.url)), shell: false, encoding: 'utf8', timeout: 10000, maxBuffer: 1024 * 1024 });
assert.equal(child.status, 0, 'Synthetic F3 fixture creation failed');
const sidecar = JSON.parse(child.stdout);
assert.equal(validatePixInsightWorkflowProvenance(sidecar).valid, true);
const manifest = provenanceSidecarToManifest(sidecar);
assert.equal(validateManifest(manifest).valid, true);
assert.deepEqual(manifest.processingRun.processes, []);
assert.equal(sidecar.capture.completeness, 'PARTIAL');
assert.equal(sidecar.capture.declaredStepCount, 2);
assert.equal(sidecar.capture.observedStepCount, 0);
const stamp = '2026-09-30T18:03:00Z';
const ledger = new PixInsightSynchronizationLedger();
const record = ledger.append(manifest, { receivedAt: stamp });
const reconciliation = new PixInsightReconciliationService().reconcile(manifest, { reconciledAt: stamp });
assert.equal(reconciliation.state, 'unresolved');
assert.equal(reconciliation.outputs.requested, 0);
assert.equal(ledger.append(manifest, { receivedAt: stamp }).outcome, 'duplicate-noop');
const { projection } = new PixInsightProcessingProjectionBuilder().build({ manifest, ledgerRecord: record, reconciliation, projectedAt: stamp });
const model = buildPixInsightProvenanceReadModel({ sidecar, processingProjection: projection });
assert.equal(model.reconciliation.state, 'unresolved');
assert.equal(model.authority.acceptanceAuthority, false);
assert.equal(model.provenanceState, 'PARTIAL');
assert.deepEqual(model.workflow.steps.map(step => step.evidenceClass), ['DECLARED', 'DECLARED']);
assert.equal(model.workflow.steps[0].parameters.bkl049LexicalV1.exportParameters.n.literal, '+0.1200E-03');
assert.deepEqual(model.workflow.steps[0].parameters.bkl049LexicalV1.containerPath, ['Root', 'Group']);
assert.equal(Object.hasOwn(manifest.processingRun.parameters, 'bkl049LexicalV1'), false);
assert.ok(!JSON.stringify(manifest).includes('+0.1200E-03'));
const invalid = structuredClone(sidecar);
delete invalid.workflow.steps[0].declaredBy;
assert.throws(() => validatePixInsightWorkflowProvenance(invalid));
console.log('BKL-049 F3 synthetic bridge PASS: PXP/manifest valid, DECLARED/PARTIAL preserved, unresolved association stays unresolved, lexical values retained in private read model.');
