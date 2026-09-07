import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const manifestPath = path.join(root, 'docs/data/knowledge-ai-seed-reconciliation.json');
const contractPath = path.join(root, 'docs/data/knowledge-ai-evidence-contract.json');

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exitCode = 1;
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

const manifest = readJson(manifestPath);
const contract = readJson(contractPath);
const allowedTypes = new Set(['observation','evidence','claim','inference','recommendation','conflict','unknown']);
const allowedLifecycle = new Set(['incomplete','unknown','draft','validated','superseded','rejected']);
const itemById = new Map((contract.items ?? []).map(item => [item.id, item]));
const sourceById = new Map();

if (manifest.schema_version !== '1.0') fail('manifest schema_version must be 1.0');
if (manifest.component !== 'DSG.KnowledgeSeedReconciliation') fail('unexpected manifest component');
if (manifest.authority !== 'projection') fail('manifest must remain a projection');
if (!/^[0-9a-f]{40}$/.test(manifest.baseline_commit ?? '')) fail('baseline_commit must be a full commit SHA');

const maxSources = manifest.bounds?.max_sources;
const maxSeeds = manifest.bounds?.max_seeds;
if (!Number.isInteger(maxSources) || maxSources < 1 || maxSources > 10) fail('max_sources must be an integer from 1 to 10');
if (!Number.isInteger(maxSeeds) || maxSeeds < 1 || maxSeeds > 10) fail('max_seeds must be an integer from 1 to 10');
if ((manifest.sources ?? []).length > maxSources) fail('source count exceeds governed bound');
if ((manifest.seeds ?? []).length > maxSeeds) fail('seed count exceeds governed bound');

for (const source of manifest.sources ?? []) {
  if (!source.id || sourceById.has(source.id)) fail(`duplicate or missing source id: ${source.id ?? '<missing>'}`);
  sourceById.set(source.id, source);
  if (source.source_authority !== 'repository_authority') fail(`${source.id}: F3 source must be repository_authority`);
  if (!source.path || path.isAbsolute(source.path) || source.path.includes('..')) fail(`${source.id}: source path must be repository-relative`);
  const resolved = path.join(root, source.path);
  if (!fs.existsSync(resolved) || !fs.statSync(resolved).isFile()) fail(`${source.id}: source file does not exist: ${source.path}`);
}

const seedIds = new Set();
for (const seed of manifest.seeds ?? []) {
  if (!seed.id || seedIds.has(seed.id)) fail(`duplicate or missing seed id: ${seed.id ?? '<missing>'}`);
  seedIds.add(seed.id);
  if (!allowedTypes.has(seed.semantic_type)) fail(`${seed.id}: unsupported semantic_type ${seed.semantic_type}`);
  if (!allowedLifecycle.has(seed.lifecycle_state)) fail(`${seed.id}: unsupported lifecycle_state ${seed.lifecycle_state}`);
  if (seed.source_authority !== 'repository_authority') fail(`${seed.id}: source_authority must be repository_authority`);
  const source = sourceById.get(seed.source_ref);
  if (!source) {
    fail(`${seed.id}: unresolved source_ref ${seed.source_ref}`);
    continue;
  }
  const item = itemById.get(seed.knowledge_item_ref);
  if (!item) {
    fail(`${seed.id}: unresolved knowledge_item_ref ${seed.knowledge_item_ref}`);
  } else {
    if (item.semantic_type !== seed.semantic_type) fail(`${seed.id}: semantic_type differs from knowledge item`);
    if (item.lifecycle_state !== seed.lifecycle_state) fail(`${seed.id}: lifecycle_state differs from knowledge item`);
    if (item.source_authority !== seed.source_authority) fail(`${seed.id}: source_authority differs from knowledge item`);
  }
  if (!Array.isArray(seed.required_fragments) || seed.required_fragments.length < 1 || seed.required_fragments.length > 3) {
    fail(`${seed.id}: required_fragments must contain 1..3 bounded assertions`);
    continue;
  }
  const sourceText = fs.readFileSync(path.join(root, source.path), 'utf8');
  for (const fragment of seed.required_fragments) {
    if (typeof fragment !== 'string' || fragment.length < 8 || fragment.length > 240) fail(`${seed.id}: invalid required fragment`);
    else if (!sourceText.includes(fragment)) fail(`${seed.id}: authoritative source drifted; fragment not found in ${source.path}: ${fragment}`);
  }
}

if ((manifest.sources ?? []).length === 0 || (manifest.seeds ?? []).length === 0) fail('F3 manifest must contain a bounded non-empty seed set');

if (!process.exitCode) {
  console.log(`PASS: reconciled ${manifest.seeds.length} governed seeds against ${manifest.sources.length} repository-authoritative sources; bounds sources<=${maxSources}, seeds<=${maxSeeds}.`);
}
