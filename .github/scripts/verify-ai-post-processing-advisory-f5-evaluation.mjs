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
  F5_METHOD_REGISTRY,
  validateRealEvidenceEvaluation
} from './ai-post-processing-advisory-real-evidence-evaluation.mjs';
import { OUTPUT_PATH } from './generate-ai-post-processing-advisory-f5-evaluation.mjs';

const SCHEMA_PATH = 'docs/contracts/ai-post-processing-assistant-f5-evaluation.schema.json';
const F2_SCHEMA_PATH = 'docs/contracts/ai-post-processing-assistant-f2.schema.json';
const assert = (condition, message) => { if (!condition) throw new Error(message); };

function verifySchemaRegistry(schema) {
  assert(schema?.properties?.schemaVersion?.const === '1.0', 'F5 schemaVersion registry mismatch.');
  assert(schema.properties.evaluationType.const === 'BKL046_F5_REAL_EVIDENCE_EVALUATION', 'F5 evaluationType registry mismatch.');
  assert(schema.properties.evaluationState.const === 'F5A_FOUNDATION_EVALUATED', 'F5 evaluationState registry mismatch.');
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
  const [catalog, f4Projection, report, schema, f2Schema, humanDecisionSources, executionEvidenceSources] = await Promise.all([
    readFile(CATALOG_PATH, 'utf8').then(JSON.parse),
    readFile(F4_PROJECTION_PATH, 'utf8').then(JSON.parse),
    readFile(OUTPUT_PATH, 'utf8').then(JSON.parse),
    readFile(SCHEMA_PATH, 'utf8').then(JSON.parse),
    readFile(F2_SCHEMA_PATH, 'utf8').then(JSON.parse),
    discoverHumanDecisionSources('.'),
    discoverExecutionEvidenceSources('.')
  ]);

  validateRealEvidenceEvaluation(report);
  verifySchemaRegistry(schema);
  verifyF2ReceiptSchemaBinding(schema, f2Schema);
  const expected = buildRealEvidenceEvaluation({
    catalog,
    f4Projection,
    humanDecisionSources,
    executionEvidenceSources,
    generatedAt: report.generatedAt
  });
  assert(canonicalJson(report) === canonicalJson(expected), 'Persisted F5 evaluation does not match governed inputs.');
  assert(report.outcomes.closureRecommendation === 'KEEP_OPEN', 'F5-A cannot close BKL-046.');
  assert(report.outcomes.aiModelImplemented === false, 'F5-A cannot claim an implemented AI model.');
  assert(report.outcomes.production.state === 'NOT_READY_FOR_PRODUCTION', 'F5-A cannot claim production readiness.');
  process.stdout.write('BKL-046 F5-A report, closed registry, source contracts and known-answer evaluation verified.\n');
}

export { verifyF2ReceiptSchemaBinding, verifySchemaRegistry };

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch((error) => { console.error(error.message); process.exitCode = 1; });
}
