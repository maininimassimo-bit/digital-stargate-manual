import { readFile } from 'node:fs/promises';
import path from 'node:path';

const root = process.cwd();
const graphPath = path.join(root, 'docs', 'data', 'knowledge-graph.json');
const registerPath = path.join(root, 'docs', 'architecture', 'traceability-register.md');

const graph = JSON.parse(await readFile(graphPath, 'utf8'));
const register = await readFile(registerPath, 'utf8');
const entities = new Map(graph.entities.map((entity) => [entity.id, entity]));
const relations = graph.relations;
const failures = [];

const sectionMatch = register.match(/## 4\. Architecture Artifact Register\s+([\s\S]*?)(?=\n## 5\.)/);
if (!sectionMatch) {
  console.error('Architecture Artifact Register section not found.');
  process.exit(1);
}

const rows = sectionMatch[1]
  .split(/\r?\n/)
  .filter((line) => /^\|[^-]/.test(line.trim()))
  .slice(2)
  .map((line) => line.split('|').slice(1, -1).map((cell) => cell.trim()))
  .filter((cells) => cells.length >= 5 && cells[0]);

if (rows.length === 0) failures.push('No governed artifact rows discovered.');

let identitiesCovered = 0;
let materialRelationsCovered = 0;

for (const [id, title, packageId] of rows) {
  const expectedType = id.startsWith('ARB-') ? 'evidence' : 'component';
  const entity = entities.get(id);
  if (!entity) {
    failures.push(`Missing ${expectedType} entity: ${id}`);
    continue;
  }
  if (entity.type !== expectedType) {
    failures.push(`Wrong entity type for ${id}: expected=${expectedType} actual=${entity.type}`);
    continue;
  }
  identitiesCovered += 1;

  if (!entities.has(packageId)) {
    failures.push(`Missing package entity required by register: ${packageId} for ${id}`);
    continue;
  }

  const relationFound = expectedType === 'evidence'
    ? relations.some((relation) => relation.type === 'evidenced_by' && relation.from === packageId && relation.to === id)
    : relations.some((relation) => relation.type === 'documents' && relation.from === id && relation.to === packageId);

  if (!relationFound) {
    failures.push(`Missing material relation for ${id} -> ${packageId}`);
    continue;
  }
  materialRelationsCovered += 1;
}

const identityPct = rows.length ? (identitiesCovered / rows.length) * 100 : 0;
const relationPct = rows.length ? (materialRelationsCovered / rows.length) * 100 : 0;

console.log(`Artifact register rows=${rows.length}`);
console.log(`Identity coverage=${identityPct.toFixed(1)}% (${identitiesCovered}/${rows.length})`);
console.log(`Material relation coverage=${relationPct.toFixed(1)}% (${materialRelationsCovered}/${rows.length})`);

if (identityPct !== 100) failures.push(`Artifact identity threshold not met: ${identityPct.toFixed(1)}% < 100%`);
if (relationPct !== 100) failures.push(`Material relation threshold not met: ${relationPct.toFixed(1)}% < 100%`);

if (failures.length) {
  console.error('Knowledge graph material relation verification FAILED:');
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

console.log('Knowledge graph material relation verification PASS.');
