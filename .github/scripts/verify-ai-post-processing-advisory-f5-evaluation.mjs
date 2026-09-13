import { readFile } from 'node:fs/promises';
import { pathToFileURL } from 'node:url';
import process from 'node:process';
import { F2_CONTRACT_LIMITS } from './ai-post-processing-advisory-contract.mjs';
import {
  buildRealEvidenceEvaluation,
  canonicalJson,
  CATALOG_PATH,
  discoverExecutionEvidenceSources,
  discoverHumanDecisionSources,
  F4_PROJECTION_PATH,
  F5_EVALUATION_STATE,
  F5_METHOD_REGISTRY,
  F5_SCHEMA_VERSION,
  validateRealEvidenceEvaluation
} from './ai-post-processing-advisory-real-evidence-evaluation.mjs';
import { OUTPUT_PATH } from './generate-ai-post-processing-advisory-f5-evaluation.mjs';

const SCHEMA_PATH = 'docs/contracts/ai-post-processing-assistant-f5-evaluation.schema.json';
const F2_SCHEMA_PATH = 'docs/contracts/ai-post-processing-assistant-f2.schema.json';
const AUTOMATIC_WORKFLOW_PATH = '.github/workflows/analyze-session-automatic.yml';
const assert = (condition, message) => { if (!condition) throw new Error(message); };

export function verifyAtomicWorkflowIntegration(workflow) {
  const f4Write = 'node .github/scripts/generate-ai-post-processing-advisory-projection.mjs --write';
  const f5Write = 'node .github/scripts/generate-ai-post-processing-advisory-f5-evaluation.mjs --write';
  const f5Check = 'node .github/scripts/generate-ai-post-processing-advisory-f5-evaluation.mjs --check';
  const f5Verify = 'node .github/scripts/verify-ai-post-processing-advisory-f5-evaluation.mjs';
  const occurrences = (value) => (workflow.match(new RegExp(value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g')) || []).length;
  assert(occurrences(f4Write) >= 2, 'F4 generation must run in initial and retry paths.');
  assert(occurrences(f5Write) >= 2, 'F5 evaluation generation must run in initial and retry paths.');
  assert(occurrences(f5Check) >= 2, 'F5 evaluation drift check must run in initial and retry paths.');
  assert(occurrences(f5Verify) >= 2, 'F5 evaluation verifier must run in initial and retry paths.');
  assert(workflow.includes('docs/data/ai-post-processing-advisory-f5-evaluation.json'), 'F5 evaluation is missing from the atomic governed path set.');
  const f4Indexes = [...workflow.matchAll(new RegExp(f4Write.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'))].map(match => match.index);
  const f5Indexes = [...workflow.matchAll(new RegExp(f5Write.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'))].map(match => match.index);
  assert(f5Indexes.every((index, position) => index > f4Indexes[position]), 'F5 evaluation must be generated after its F4 projection in every path.');
  assert(workflow.includes('git reset --hard origin/main') && workflow.includes('regenerate; git add -- "${governed_paths[@]}"'), 'Retry path must regenerate the complete governed set from origin/main.');
  return true;
}

function verifySchemaRegistry(schema) {
  assert(schema?.properties?.schemaVersion?.const === F5_SCHEMA_VERSION, 'F5 schemaVersion registry mismatch.');
  assert(schema.properties.evaluationType.const === 'BKL046_F5_REAL_EVIDENCE_EVALUATION', 'F5 evaluationType registry mismatch.');
  assert(schema.properties.evaluationState.const === F5_EVALUATION_STATE, 'F5 evaluationState registry mismatch.');
  const registryDefinitions = {
    cohortIds: 'cohortId',
    selectionRuleIds: 'selectionRuleId',
    technicalGateIds: 'technicalGateId',
    technicalStates: 'technicalState',
    scientificStates: 'scientificState',
    humanDecisionStates: 'humanDecisionState',
    productionStates: 'productionState',
    capabilityOutcomes: 'capabilityOutcome',
    closureRecommendations: 'closureRecommendation',
    gateStates: 'gateState',
    evidenceStates: 'evidenceState',
    reasonCodes: 'reasonCode'
  };
  for (const [registryKey, definitionKey] of Object.entries(registryDefinitions)) {
    assert(
      canonicalJson(schema.$defs?.[definitionKey]?.enum) === canonicalJson(F5_METHOD_REGISTRY[registryKey]),
      `F5 schema ${registryKey} registry drift.`
    );
  }
  return true;
}

function verifyF2ReceiptSchemaBinding(schema, f2Schema) {
  const stableId = f2Schema?.$defs?.stableId;
  const receipt = f2Schema?.$defs?.humanDecisionReceipt;
  const edit = f2Schema?.$defs?.decisionEdit;
  assert(schema?.$defs?.rawHumanDecisionSource?.properties?.receipt?.$ref === 'ai-post-processing-assistant-f2.schema.json#/$defs/humanDecisionReceipt', 'F5 raw Human Decision schema must reuse the F2 receipt definition.');
  assert(stableId?.minLength === F2_CONTRACT_LIMITS.stableIdMinLength, 'F2 stableId minimum drift.');
  assert(stableId?.maxLength === F2_CONTRACT_LIMITS.stableIdMaxLength, 'F2 stableId maximum drift.');
  assert(stableId?.pattern === F2_CONTRACT_LIMITS.stableIdPattern, 'F2 stableId pattern drift.');
  assert(receipt?.properties?.decisionEdits?.maxItems === F2_CONTRACT_LIMITS.decisionEditsMaxItems, 'F2 decisionEdits bound drift.');
  assert(receipt?.properties?.decisionRationale?.maxLength === F2_CONTRACT_LIMITS.decisionRationaleMaxLength, 'F2 decisionRationale bound drift.');
  assert(edit?.properties?.parameterId?.maxLength === F2_CONTRACT_LIMITS.decisionEditParameterIdMaxLength, 'F2 decisionEdit parameter bound drift.');
  assert(edit?.properties?.unit?.maxLength === F2_CONTRACT_LIMITS.decisionEditUnitMaxLength, 'F2 decisionEdit unit bound drift.');
  assert(edit?.properties?.reason?.maxLength === F2_CONTRACT_LIMITS.decisionEditReasonMaxLength, 'F2 decisionEdit reason bound drift.');
  return true;
}

async function main() {
  const [catalog, f4Projection, report, schema, f2Schema, workflow, humanDecisionSources, executionEvidenceSources] = await Promise.all([
    readFile(CATALOG_PATH, 'utf8').then(JSON.parse),
    readFile(F4_PROJECTION_PATH, 'utf8').then(JSON.parse),
    readFile(OUTPUT_PATH, 'utf8').then(JSON.parse),
    readFile(SCHEMA_PATH, 'utf8').then(JSON.parse),
    readFile(F2_SCHEMA_PATH, 'utf8').then(JSON.parse),
    readFile(AUTOMATIC_WORKFLOW_PATH, 'utf8'),
    discoverHumanDecisionSources('.'),
    discoverExecutionEvidenceSources('.')
  ]);

  validateRealEvidenceEvaluation(report);
  verifySchemaRegistry(schema);
  verifyF2ReceiptSchemaBinding(schema, f2Schema);
  verifyAtomicWorkflowIntegration(workflow);
  const expected = buildRealEvidenceEvaluation({
    catalog,
    f4Projection,
    humanDecisionSources,
    executionEvidenceSources,
    generatedAt: report.generatedAt
  });
  assert(canonicalJson(report) === canonicalJson(expected), 'Persisted F5 evaluation does not match governed inputs.');
  assert(report.outcomes.closureRecommendation === 'CLOSE_DETERMINISTIC_CAPABILITY', 'F5-C must close only the deterministic capability.');
  assert(report.outcomes.aiModelImplemented === false, 'F5-C cannot claim an implemented AI model.');
  assert(report.outcomes.production.state === 'NOT_READY_FOR_PRODUCTION', 'F5-C cannot claim production readiness.');
  process.stdout.write('BKL-046 F5-C report, closed registry, source contracts and bounded closure evaluation verified.\n');
}

export { verifyF2ReceiptSchemaBinding, verifySchemaRegistry };

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch((error) => { console.error(error.message); process.exitCode = 1; });
}
