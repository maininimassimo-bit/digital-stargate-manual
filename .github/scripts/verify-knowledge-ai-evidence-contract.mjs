import { readFile } from 'node:fs/promises';

const DEFAULT_PATH = 'docs/data/knowledge-ai-evidence-contract.json';
const path = process.argv[2] ?? DEFAULT_PATH;
const fail = (message) => { throw new Error(message); };
const assert = (condition, message) => { if (!condition) fail(message); };
const readJson = async (file) => JSON.parse(await readFile(file, 'utf8'));
const derivedTypes = new Set(['claim', 'inference', 'recommendation']);
const allowedTypes = new Set(['observation', 'evidence', 'claim', 'inference', 'recommendation', 'conflict', 'unknown']);
const allowedLifecycle = new Set(['incomplete', 'unknown', 'draft', 'validated', 'superseded', 'rejected']);
const allowedSourceAuthorities = new Set(['repository_authority', 'scientific_catalog', 'analytics_product', 'telemetry_projection', 'session_projection', 'external_scientific_storage', 'projection', 'unknown']);
const requireArray = (value, message) => assert(Array.isArray(value) && value.length > 0, message);

const main = async () => {
  const document = await readJson(path);
  assert(document.schema_version === '1.0', 'schema_version must be 1.0');
  assert(document.component === 'DSG.KnowledgeAIEvidenceContract', 'unexpected component');
  assert(document.authority === 'projection', 'contract dataset must remain a projection');
  assert(Array.isArray(document.items), 'items must be an array');
  assert(Array.isArray(document.citations), 'citations must be an array');
  assert(Array.isArray(document.provenance_records), 'provenance_records must be an array');
  assert(Array.isArray(document.confidence_contracts), 'confidence_contracts must be an array');

  const citationKeys = new Set();
  for (const citation of document.citations) {
    assert(typeof citation.id === 'string' && citation.id.length > 1, 'citation id is required');
    assert(typeof citation.version === 'string' && citation.version.length > 0, `${citation.id}: citation version is required`);
    const key = `${citation.id}@${citation.version}`;
    assert(!citationKeys.has(key), `duplicate citation: ${key}`); citationKeys.add(key);
    assert(allowedSourceAuthorities.has(citation.source_authority), `${key}: unsupported source_authority ${citation.source_authority}`);
    assert(citation.locator && typeof citation.locator.kind === 'string' && typeof citation.locator.value === 'string' && citation.locator.value.length > 0, `${key}: governed locator is required`);
    assert(typeof citation.producer === 'string' && citation.producer.length > 0, `${key}: producer is required`);
    assert(typeof citation.produced_at_utc === 'string' && citation.produced_at_utc.length > 0, `${key}: produced_at_utc is required`);
  }

  const provenanceKeys = new Set();
  for (const provenance of document.provenance_records) {
    assert(typeof provenance.id === 'string' && provenance.id.length > 1, 'provenance id is required');
    assert(typeof provenance.version === 'string' && provenance.version.length > 0, `${provenance.id}: provenance version is required`);
    const key = `${provenance.id}@${provenance.version}`;
    assert(!provenanceKeys.has(key), `duplicate provenance record: ${key}`); provenanceKeys.add(key);
    assert(typeof provenance.producer === 'string' && provenance.producer.length > 0, `${key}: producer is required`);
    assert(typeof provenance.produced_at_utc === 'string' && provenance.produced_at_utc.length > 0, `${key}: produced_at_utc is required`);
    assert(typeof provenance.method_id === 'string' && provenance.method_id.length > 0, `${key}: method_id is required`);
    requireArray(provenance.input_refs, `${key}: input_refs are required`);
    assert(typeof provenance.output_ref === 'string' && provenance.output_ref.length > 1, `${key}: output_ref is required`);
    requireArray(provenance.citation_refs, `${key}: citation_refs are required`);
    for (const ref of provenance.citation_refs) assert(citationKeys.has(ref), `${key}: unresolved citation ${ref}`);
  }

  const confidenceContracts = new Set();
  for (const contract of document.confidence_contracts) {
    assert(typeof contract.id === 'string' && contract.id.length > 1, 'confidence contract id is required');
    assert(typeof contract.version === 'string' && contract.version.length > 0, `${contract.id}: confidence contract version is required`);
    const key = `${contract.id}@${contract.version}`;
    assert(!confidenceContracts.has(key), `duplicate confidence contract: ${key}`); confidenceContracts.add(key);
    assert(typeof contract.scale === 'string' && contract.scale.length > 0, `${key}: scale is required`);
    assert(typeof contract.method === 'string' && contract.method.length > 0, `${key}: method is required`);
    assert(typeof contract.producer === 'string' && contract.producer.length > 0, `${key}: producer is required`);
  }

  const ids = new Set(document.items.map((item) => item.id));
  assert(ids.size === document.items.length, 'duplicate item id');
  for (const item of document.items) {
    assert(typeof item.id === 'string' && item.id.length > 1, 'item id is required');
    assert(allowedTypes.has(item.semantic_type), `${item.id}: unsupported semantic_type ${item.semantic_type}`);
    assert(allowedLifecycle.has(item.lifecycle_state), `${item.id}: unsupported lifecycle_state ${item.lifecycle_state}`);
    assert(typeof item.producer === 'string' && item.producer.length > 0, `${item.id}: producer is required`);
    assert(typeof item.produced_at_utc === 'string' && item.produced_at_utc.length > 0, `${item.id}: produced_at_utc is required`);
    assert(allowedSourceAuthorities.has(item.source_authority), `${item.id}: unsupported source_authority ${item.source_authority}`);
    assert(typeof item.ai_derived === 'boolean', `${item.id}: ai_derived is required`);
    if (item.semantic_type === 'observation') assert(typeof item.observed_at_utc === 'string' && item.observed_at_utc.length > 0, `${item.id}: observation time is required`);
    if (derivedTypes.has(item.semantic_type)) assert(typeof item.method_id === 'string' && item.method_id.length > 0, `${item.id}: derivation method is required`);

    const validated = item.lifecycle_state === 'validated';
    if (validated && derivedTypes.has(item.semantic_type)) {
      requireArray(item.evidence_refs, `${item.id}: validated derived item requires evidence_refs`);
      requireArray(item.citation_refs, `${item.id}: validated derived item requires citation_refs`);
      requireArray(item.provenance_refs, `${item.id}: validated derived item requires provenance_refs`);
    }
    if (validated && item.semantic_type === 'evidence') requireArray(item.citation_refs, `${item.id}: validated evidence requires citation_refs`);
    if (validated && item.ai_derived) {
      requireArray(item.evidence_refs, `${item.id}: validated AI item requires evidence_refs`);
      requireArray(item.citation_refs, `${item.id}: validated AI item requires citation_refs`);
      requireArray(item.provenance_refs, `${item.id}: validated AI item requires provenance_refs`);
      assert(typeof item.producer_version === 'string' && item.producer_version.length > 0, `${item.id}: validated AI item requires producer_version`);
    }
    for (const ref of item.evidence_refs ?? []) assert(ids.has(ref), `${item.id}: unresolved evidence ${ref}`);
    for (const ref of item.citation_refs ?? []) assert(citationKeys.has(ref), `${item.id}: unresolved citation ${ref}`);
    for (const ref of item.provenance_refs ?? []) assert(provenanceKeys.has(ref), `${item.id}: unresolved provenance ${ref}`);
    if (item.confidence !== undefined) {
      assert(typeof item.confidence.contract_ref === 'string' && item.confidence.contract_ref.length > 0, `${item.id}: confidence.contract_ref is required`);
      assert(confidenceContracts.has(item.confidence.contract_ref), `${item.id}: unresolved confidence contract ${item.confidence.contract_ref}`);
      assert(item.confidence.value !== undefined, `${item.id}: confidence.value is required`);
    }
    if (item.semantic_type === 'conflict') requireArray(item.conflict_refs, `${item.id}: conflict_refs are required`);
  }

  for (const provenance of document.provenance_records) {
    const key = `${provenance.id}@${provenance.version}`;
    assert(ids.has(provenance.output_ref), `${key}: unresolved output_ref ${provenance.output_ref}`);
    for (const ref of provenance.input_refs) assert(ids.has(ref), `${key}: unresolved input_ref ${ref}`);
  }
  console.log(`Knowledge/AI evidence validation PASS: items=${ids.size}; citations=${citationKeys.size}; provenance=${provenanceKeys.size}; confidence_contracts=${confidenceContracts.size}`);
};

main().catch((error) => { console.error(`Knowledge/AI evidence validation FAILED: ${error.message}`); process.exitCode = 1; });
