import { readFile } from 'node:fs/promises';

const DOMAINS = new Set(['weather', 'dome', 'mount', 'camera', 'power', 'network', 'eagle_health']);
const BAD = new Set(['MISSING', 'STALE', 'UNAVAILABLE', 'PARTIAL', 'CONFLICTING']);
const TOP = new Set(['schema_version','contract_id','batch_id','fixture_kind','source_plane','acquisition_mode','source_manifest','archived_at_utc','safety_boundary','domains']);
const fail = message => { throw new Error(message); };
const assert = (condition, message) => { if (!condition) fail(message); };
const readJson = async path => JSON.parse(await readFile(path, 'utf8'));

export const validateArchivedTelemetry = batch => {
  assert(batch.schema_version === '1.0', 'schema_version must be 1.0');
  assert(batch.contract_id === 'DSG.BKL036.F4.ArchivedTelemetry', 'contract_id mismatch');
  assert(['synthetic_offline','repository_archived_snapshot'].includes(batch.fixture_kind), 'invalid fixture_kind');
  assert(batch.source_plane === 'repository_evidence', 'source plane must be repository_evidence');
  assert(batch.acquisition_mode === 'read_only_snapshot_import', 'unsupported acquisition mode');
  for (const key of Object.keys(batch)) assert(TOP.has(key), `unexpected top-level key: ${key}`);
  const boundary = batch.safety_boundary;
  assert(boundary && boundary.live_transport_used === false && boundary.commands_issued === false, 'live transport or commands are not allowed');
  assert(boundary.scheduling_enabled === false && boundary.remediation_enabled === false, 'scheduling/remediation are not allowed');
  assert(boundary.safety_authority === 'LOCAL_PHYSICAL_INTERLOCKS', 'local interlocks must remain Safety Authority');
  assert(Array.isArray(batch.domains) && batch.domains.length === DOMAINS.size, 'exactly seven domains are required');
  const seen = new Set();
  for (const item of batch.domains) {
    assert(DOMAINS.has(item.domain), `unsupported domain: ${item.domain}`);
    assert(!seen.has(item.domain), `duplicate domain: ${item.domain}`);
    seen.add(item.domain);
    assert(typeof item.source === 'string' && item.source, `source missing: ${item.domain}`);
    assert(typeof item.authority === 'string' && item.authority, `authority missing: ${item.domain}`);
    assert(['PRESENT','MISSING','STALE','UNAVAILABLE','PARTIAL','CONFLICTING'].includes(item.evidence_status), `invalid evidence status: ${item.domain}`);
    assert(['COMPARABLE','CONTEXT_ONLY','INCOMPATIBLE','UNKNOWN'].includes(item.compatibility), `invalid compatibility: ${item.domain}`);
    assert(['CURRENT','STALE','UNKNOWN','CONFLICTING'].includes(item.quality), `invalid quality: ${item.domain}`);
    if (BAD.has(item.evidence_status)) assert(item.compatibility !== 'COMPARABLE', `incomplete evidence cannot be comparable: ${item.domain}`);
    if (item.evidence_status === 'PRESENT') assert(item.observed_at_utc && item.fresh_until_utc, `present evidence requires timestamps: ${item.domain}`);
  }
  assert(seen.size === DOMAINS.size, 'all seven mandatory domains must be represented');
  return true;
};

const main = async () => {
  const input = process.argv[2] || 'docs/data/bkl-036-f4-telemetry-ingest-fixture.json';
  await validateArchivedTelemetry(await readJson(input));
  console.log(`BKL-036-F4 archived telemetry PASS: ${input}`);
};
if (import.meta.url === `file://${process.argv[1]}`) main().catch(error => { console.error(error.message); process.exitCode = 1; });
