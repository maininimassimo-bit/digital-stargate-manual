import { readFile } from 'node:fs/promises';
import { pathToFileURL } from 'node:url';
import process from 'node:process';
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

async function main() {
  const [catalog, f4Projection, report, schema, humanDecisionSources, executionEvidenceSources] = await Promise.all([
    readFile(CATALOG_PATH, 'utf8').then(JSON.parse),
    readFile(F4_PROJECTION_PATH, 'utf8').then(JSON.parse),
    readFile(OUTPUT_PATH, 'utf8').then(JSON.parse),
    readFile(SCHEMA_PATH, 'utf8').then(JSON.parse),
    discoverHumanDecisionSources('.'),
    discoverExecutionEvidenceSources('.')
  ]);

  validateRealEvidenceEvaluation(report);
  verifySchemaRegistry(schema);
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

export { verifySchemaRegistry };

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch((error) => { console.error(error.message); process.exitCode = 1; });
}
