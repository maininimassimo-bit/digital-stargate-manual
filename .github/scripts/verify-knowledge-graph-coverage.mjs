import { readFile, readdir } from 'node:fs/promises';
import path from 'node:path';

const root = process.cwd();
const graphPath = path.join(root, 'docs', 'data', 'knowledge-graph.json');
const roadmapPath = path.join(root, '.github', 'roadmap', 'roadmap-source.json');
const architectureRoot = path.join(root, 'docs', 'architecture');

const graph = JSON.parse(await readFile(graphPath, 'utf8'));
const roadmap = JSON.parse(await readFile(roadmapPath, 'utf8'));
const entities = new Map(graph.entities.map((entity) => [entity.id, entity]));
const failures = [];

function collectRoadmapItems(value, output = []) {
  if (Array.isArray(value)) {
    for (const item of value) collectRoadmapItems(item, output);
    return output;
  }
  if (!value || typeof value !== 'object') return output;
  if (typeof value.id === 'string' && /^AP-\d{3}$/.test(value.id)) output.push(value.id);
  for (const child of Object.values(value)) collectRoadmapItems(child, output);
  return output;
}

async function walk(dir) {
  const entries = await readdir(dir, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) files.push(...await walk(full));
    else files.push(full);
  }
  return files;
}

function reconcile(ids, expectedType, family) {
  const unique = [...new Set(ids)].sort();
  const missing = [];
  const wrongType = [];
  for (const id of unique) {
    const entity = entities.get(id);
    if (!entity) missing.push(id);
    else if (entity.type !== expectedType) wrongType.push(`${id}:${entity.type}`);
  }
  const covered = unique.length - missing.length - wrongType.length;
  const pct = unique.length === 0 ? 0 : (covered / unique.length) * 100;
  console.log(`${family}: expected=${unique.length} covered=${covered} coverage=${pct.toFixed(1)}%`);
  if (missing.length) failures.push(`${family} missing: ${missing.join(', ')}`);
  if (wrongType.length) failures.push(`${family} wrong type: ${wrongType.join(', ')}`);
  if (pct !== 100) failures.push(`${family} coverage threshold not met: ${pct.toFixed(1)}% < 100%`);
  return { expected: unique.length, covered, pct };
}

const apIds = collectRoadmapItems(roadmap);
const files = await walk(architectureRoot);
const adrIds = files
  .map((file) => path.basename(file).match(/^(ADR-\d{3})-.*\.md$/)?.[1])
  .filter(Boolean);

if (apIds.length === 0) failures.push('No canonical AP identifiers discovered from roadmap source.');
if (adrIds.length === 0) failures.push('No canonical ADR identifiers discovered from repository files.');

const ap = reconcile(apIds, 'architecture_package', 'Architecture Package');
const adr = reconcile(adrIds, 'adr', 'ADR');

const counts = {};
for (const entity of graph.entities) counts[entity.type] = (counts[entity.type] ?? 0) + 1;
console.log(`Graph entities by type: ${JSON.stringify(counts)}`);
console.log(`Graph relations: ${graph.relations.length}`);

if (failures.length) {
  console.error('Knowledge graph coverage verification FAILED:');
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

console.log(`Knowledge graph coverage verification PASS: AP=${ap.pct.toFixed(1)}% ADR=${adr.pct.toFixed(1)}%`);
