import crypto from 'node:crypto';

const ALLOWED_ROOT = new Set(['schemaVersion','sidecarId','exportedAt','authority','actionAuthority','source','observationContext','workflow','capture']);
const EVIDENCE = new Set(['OBSERVED','DECLARED']);
const COMPLETENESS = new Set(['COMPLETE','PARTIAL','UNAVAILABLE']);
const CAPTURE_METHOD = new Set(['PROJECT_HISTORY_EXPORT','PROCESS_HISTORY_EXPORT','GOVERNED_PJSR_EXPORT','HYBRID']);

const fail = (message) => { throw new Error(`PixInsight provenance validation failed: ${message}`); };
const object = (v) => v && typeof v === 'object' && !Array.isArray(v);
const text = (v) => typeof v === 'string' && v.trim().length > 0;
const date = (v) => v === null || (text(v) && !Number.isNaN(Date.parse(v)));

export const canonicalize = (value) => {
  if (Array.isArray(value)) return value.map(canonicalize);
  if (!object(value)) return value;
  return Object.fromEntries(Object.keys(value).sort().map((key) => [key, canonicalize(value[key])]));
};

export const canonicalJson = (value) => JSON.stringify(canonicalize(value));
export const digest = (value) => crypto.createHash('sha256').update(canonicalJson(value)).digest('hex');

export function validatePixInsightWorkflowProvenance(sidecar) {
  if (!object(sidecar)) fail('root must be an object');
  for (const key of Object.keys(sidecar)) if (!ALLOWED_ROOT.has(key)) fail(`unexpected root property ${key}`);
  for (const key of ALLOWED_ROOT) if (!(key in sidecar)) fail(`missing root property ${key}`);
  if (sidecar.schemaVersion !== '1.0') fail('schemaVersion must be 1.0');
  if (!/^PXP-[A-Za-z0-9._:-]{8,}$/.test(sidecar.sidecarId || '')) fail('invalid sidecarId');
  if (!date(sidecar.exportedAt) || sidecar.exportedAt === null) fail('invalid exportedAt');
  if (sidecar.authority !== 'processing_evidence') fail('authority must be processing_evidence');
  if (sidecar.actionAuthority !== 'NONE') fail('actionAuthority must be NONE');

  const s = sidecar.source;
  if (!object(s) || s.product !== 'PixInsight' || !text(s.productVersion) || !text(s.hostId) || !text(s.workspaceId)) fail('invalid source identity');
  if (!CAPTURE_METHOD.has(s.captureMethod)) fail('unsupported captureMethod');
  if (s.sourceLocators !== undefined && (!Array.isArray(s.sourceLocators) || s.sourceLocators.some((x) => !text(x)))) fail('invalid sourceLocators');

  const c = sidecar.observationContext;
  if (!object(c) || !text(c.sessionId) || !text(c.target)) fail('invalid observationContext');

  const w = sidecar.workflow;
  if (!object(w) || !text(w.workflowId) || !text(w.runId) || !Array.isArray(w.steps) || !Array.isArray(w.inputs) || !Array.isArray(w.outputs)) fail('invalid workflow');
  const ordinals = new Set();
  for (const step of w.steps) {
    if (!object(step) || !text(step.stepId) || !Number.isInteger(step.ordinal) || step.ordinal < 1 || !text(step.processId)) fail('invalid workflow step');
    if (ordinals.has(step.ordinal)) fail(`duplicate step ordinal ${step.ordinal}`);
    ordinals.add(step.ordinal);
    if (!EVIDENCE.has(step.evidenceClass)) fail(`unsupported evidenceClass ${step.evidenceClass}`);
    if (!object(step.parameters)) fail(`step ${step.stepId} parameters must be an object`);
    if (!Array.isArray(step.sourceLocators)) fail(`step ${step.stepId} sourceLocators must be an array`);
    if (step.evidenceClass === 'OBSERVED' && step.sourceLocators.length === 0) fail(`OBSERVED step ${step.stepId} requires source evidence`);
    if (step.evidenceClass === 'DECLARED' && (!text(step.declaredBy) || !date(step.declaredAt) || step.declaredAt === null)) fail(`DECLARED step ${step.stepId} requires declaration provenance`);
  }
  const ordered = [...ordinals].sort((a,b) => a-b);
  ordered.forEach((ordinal, index) => { if (ordinal !== index + 1) fail('step ordinals must be contiguous and start at 1'); });

  const capture = sidecar.capture;
  if (!object(capture) || !COMPLETENESS.has(capture.completeness) || !Array.isArray(capture.limitations)) fail('invalid capture status');
  if (capture.completeness !== 'COMPLETE' && capture.limitations.length === 0) fail('incomplete capture requires explicit limitations');
  if (capture.completeness === 'UNAVAILABLE' && w.steps.some((step) => step.evidenceClass === 'OBSERVED')) fail('UNAVAILABLE capture cannot contain OBSERVED steps');
  if (capture.observedStepCount !== undefined && capture.observedStepCount !== w.steps.filter((x) => x.evidenceClass === 'OBSERVED').length) fail('observedStepCount mismatch');
  if (capture.declaredStepCount !== undefined && capture.declaredStepCount !== w.steps.filter((x) => x.evidenceClass === 'DECLARED').length) fail('declaredStepCount mismatch');

  return { valid: true, digest: digest(sidecar), canonical: canonicalize(sidecar) };
}
