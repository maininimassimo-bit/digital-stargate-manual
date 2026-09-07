import { readFile } from 'node:fs/promises';

const DEFAULT_PATH = 'docs/data/knowledge-ai-evidence-contract.json';
const path = process.argv[2] ?? DEFAULT_PATH;
const fail = (message) => { throw new Error(message); };
const assert = (condition, message) => { if (!condition) fail(message); };
const readJson = async (file) => JSON.parse(await readFile(file, 'utf8'));
const derivedTypes = new Set(['claim', 'inference', 'recommendation']);
const allowedTypes = new Set(['observation', 'evidence', 'claim', 'inference', 'recommendation', 'conflict', 'unknown']);
const allowedLifecycle = new Set(['incomplete', 'unknown', 'draft', 'validated', 'superseded', 'rejected']);

const main = async () => {
  const document = await readJson(path);
  assert(document.schema_version === '1.0', 'schema_version must be 1.0');
  assert(document.component === 'DSG.KnowledgeAIEvidenceContract', 'unexpected component');
  assert(document.authority === 'projection', 'contract dataset must remain a projection');
  assert(Array.isArray(document.items), 'items must be an array');
  assert(Array.isArray(document.confidence_contracts), 'confidence_contracts must be an array');

  const confidenceContracts = new Set();
  for (const contract of document.confidence_contracts) {
    assert(typeof contract.id === 'string' && contract.id.length > 1, 'confidence contract id is required');
    assert(typeof contract.version === 'string' && contract.version.length > 0, `${contract.id}: confidence contract version is required`);
    const key = `${contract.id}@${contract.version}`;
    assert(!confidenceContracts.has(key), `duplicate confidence contract: ${key}`);
    confidenceContracts.add(key);
    assert(typeof contract.scale === 'string' && contract.scale.length > 0, `${key}: scale is required`);
    assert(typeof contract.method === 'string' && contract.method.length > 0, `${key}: method is required`);
    assert(typeof contract.producer === 'string' && contract.producer.length > 0, `${key}: producer is required`);
  }

  const ids = new Set();
  for (const item of document.items) {
    assert(typeof item.id === 'string' && item.id.length > 1, 'item id is required');
    assert(!ids.has(item.id), `duplicate item id: ${item.id}`); ids.add(item.id);
    assert(allowedTypes.has(item.semantic_type), `${item.id}: unsupported semantic_type ${item.semantic_type}`);
    assert(allowedLifecycle.has(item.lifecycle_state), `${item.id}: unsupported lifecycle_state ${item.lifecycle_state}`);
    assert(typeof item.producer === 'string' && item.producer.length > 0, `${item.id}: producer is required`);
    assert(typeof item.produced_at_utc === 'string' && item.produced_at_utc.length > 0, `${item.id}: produced_at_utc is required`);
    assert(typeof item.source_authority === 'string' && item.source_authority.length > 0, `${item.id}: source_authority is required`);
    assert(typeof item.ai_derived === 'boolean', `${item.id}: ai_derived is required`);

    if (item.semantic_type === 'observation') assert(typeof item.observed_at_utc === 'string' && item.observed_at_utc.length > 0, `${item.id}: observation time is required`);
    if (derivedTypes.has(item.semantic_type)) assert(typeof item.method_id === 'string' && item.method_id.length > 0, `${item.id}: derivation method is required`);

    const complete = item.lifecycle_state === 'validated';
    if (complete && derivedTypes.has(item.semantic_type)) {
      assert(Array.isArray(item.evidence_refs) && item.evidence_refs.length > 0, `${item.id}: validated derived item requires evidence_refs`);
      assert(Array.isArray(item.citation_refs) && item.citation_refs.length > 0, `${item.id}: validated derived item requires citation_refs`);
    }
    if (complete && item.ai_derived) {
      assert(Array.isArray(item.evidence_refs) && item.evidence_refs.length > 0, `${item.id}: validated AI item requires evidence_refs`);
      assert(Array.isArray(item.citation_refs) && item.citation_refs.length > 0, `${item.id}: validated AI item requires citation_refs`);
      assert(typeof item.producer_version === 'string' && item.producer_version.length > 0, `${item.id}: validated AI item requires producer_version`);
    }
    if (item.confidence !== undefined) {
      assert(typeof item.confidence.contract_ref === 'string' && item.confidence.contract_ref.length > 0, `${item.id}: confidence.contract_ref is required`);
      assert(confidenceContracts.has(item.confidence.contract_ref), `${item.id}: unresolved confidence contract ${item.confidence.contract_ref}`);
      assert(item.confidence.value !== undefined, `${item.id}: confidence.value is required`);
    }
    if (item.semantic_type === 'conflict') assert(Array.isArray(item.conflict_refs) && item.conflict_refs.length > 0, `${item.id}: conflict_refs are required`);
  }
  console.log(`Knowledge/AI evidence validation PASS: items=${ids.size}; confidence_contracts=${confidenceContracts.size}`);
};

main().catch((error) => { console.error(`Knowledge/AI evidence validation FAILED: ${error.message}`); process.exitCode = 1; });
