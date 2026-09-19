import { readFile } from 'node:fs/promises';

const SCHEMA_PATH = 'contracts/telemetry/bkl-036-f2-evidence-envelope-v1.schema.json';
const FIXTURE_PATH = process.argv[2] || 'docs/data/bkl-036-f2-descriptive-health-fixture.json';
const DOMAINS = new Set(['weather', 'dome', 'mount', 'camera', 'power', 'network', 'eagle_health']);
const EVIDENCE_STATUS = new Set(['PRESENT', 'MISSING', 'STALE', 'UNAVAILABLE', 'PARTIAL', 'CONFLICTING']);
const COMPATIBILITY = new Set(['COMPARABLE', 'CONTEXT_ONLY', 'INCOMPATIBLE', 'UNKNOWN']);
const FORBIDDEN_KEYS = new Set(['score', 'threshold', 'ranking', 'recommendation', 'command', 'remediation', 'readiness', 'safety_authority']);

const fail = (message) => { throw new Error(message); };
const assert = (condition, message) => { if (!condition) fail(message); };
const readJson = async (path) => JSON.parse(await readFile(path, 'utf8'));

export const validateEnvelope = (envelope, schema) => {
  assert(envelope.schema_version === schema.properties.schema_version.const, 'schema_version mismatch');
  assert(envelope.contract_id === schema.properties.contract_id.const, 'contract_id mismatch');
  assert(envelope.fixture_kind === 'synthetic_offline', 'fixture must be synthetic_offline');
  assert(envelope.authority === 'projection', 'authority must be projection');
  assert(envelope.action_authority === 'NONE', 'action authority must be NONE');
  for (const key of Object.keys(envelope)) assert(!FORBIDDEN_KEYS.has(key), `forbidden top-level key: ${key}`);
  assert(envelope.descriptive_projection && envelope.descriptive_projection.score_available === false, 'descriptive projection cannot expose a score');
  assert(['AVAILABLE', 'DEGRADED', 'UNKNOWN', 'UNAVAILABLE', 'CONFLICTING'].includes(envelope.descriptive_projection.status), 'invalid descriptive status');
  assert(Array.isArray(envelope.descriptive_projection.reasons) && envelope.descriptive_projection.reasons.length > 0, 'descriptive reasons required');
  assert(Array.isArray(envelope.evidence) && envelope.evidence.length === DOMAINS.size, 'evidence must contain exactly seven domains');
  const seen = new Set();
  for (const item of envelope.evidence) {
    assert(DOMAINS.has(item.domain), `unsupported domain: ${item.domain}`);
    assert(!seen.has(item.domain), `duplicate domain: ${item.domain}`);
    seen.add(item.domain);
    assert(EVIDENCE_STATUS.has(item.evidence_status), `invalid evidence status: ${item.domain}`);
    assert(COMPATIBILITY.has(item.compatibility), `invalid compatibility: ${item.domain}`);
    assert(item.runtime_disposition !== 'LIVE_RUNTIME_ACCEPTED', `runtime acceptance is not authorized: ${item.domain}`);
    if (['MISSING', 'STALE', 'UNAVAILABLE', 'PARTIAL', 'CONFLICTING'].includes(item.evidence_status)) {
      assert(item.compatibility !== 'COMPARABLE', `fail-closed compatibility violation: ${item.domain}`);
    }
    assert(item.privacy_classification, `privacy classification missing: ${item.domain}`);
  }
  assert(seen.size === DOMAINS.size, 'not all mandatory domains are represented');
  return true;
};

const main = async () => {
  const schema = await readJson(SCHEMA_PATH);
  const envelope = await readJson(FIXTURE_PATH);
  validateEnvelope(envelope, schema);
  console.log(`BKL-036-F2 evidence envelope PASS: ${FIXTURE_PATH}`);
};

if (import.meta.url === `file://${process.argv[1]}`) main().catch((error) => { console.error(error.message); process.exitCode = 1; });
