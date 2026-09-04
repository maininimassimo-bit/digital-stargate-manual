import { access, readFile } from 'node:fs/promises';
import path from 'node:path';

const GRAPH_PATH = 'docs/data/knowledge-graph.json';
const ALLOWED_ENTITY_TYPES = new Set([
  'architecture_package', 'adr', 'component', 'evidence', 'backlog_item', 'technical_debt', 'capability'
]);
const ALLOWED_RELATION_TYPES = new Set([
  'depends_on', 'implements', 'governs', 'addresses', 'evidenced_by', 'documents', 'supersedes', 'relates_to'
]);
const ALLOWED_AUTHORITIES = new Set(['repository_authority', 'evidence_authority', 'projection']);

const fail = (message) => { throw new Error(message); };
const assert = (condition, message) => { if (!condition) fail(message); };
const readJson = async (file) => JSON.parse(await readFile(file, 'utf8'));

const validateLocator = async (locator, owner) => {
  assert(locator && typeof locator.path === 'string' && locator.path.length > 0, `${owner}: source_locator.path is required`);
  const value = locator.path.replaceAll('\\', '/');
  assert(!path.isAbsolute(value), `${owner}: source locator must be repository-relative: ${value}`);
  assert(!/^[A-Za-z]:/.test(value), `${owner}: Windows absolute source locator is forbidden: ${value}`);
  assert(!value.split('/').includes('..'), `${owner}: parent traversal is forbidden: ${value}`);
  try {
    await access(value);
  } catch {
    fail(`${owner}: source locator does not resolve to a tracked working-tree path: ${value}`);
  }
};

const main = async () => {
  const graph = await readJson(GRAPH_PATH);
  assert(graph.schema_version === '1.0', 'schema_version must be 1.0');
  assert(graph.component === 'DSG.RepositoryKnowledgeGraph', 'unexpected component');
  assert(graph.authority === 'projection', 'knowledge graph must remain a non-authoritative projection');
  assert(Array.isArray(graph.entities), 'entities must be an array');
  assert(Array.isArray(graph.relations), 'relations must be an array');

  const entityIds = new Set();
  for (const entity of graph.entities) {
    assert(typeof entity.id === 'string' && entity.id.length > 1, 'entity id is required');
    assert(!entityIds.has(entity.id), `duplicate entity id: ${entity.id}`);
    entityIds.add(entity.id);
    assert(ALLOWED_ENTITY_TYPES.has(entity.type), `${entity.id}: unsupported entity type ${entity.type}`);
    assert(ALLOWED_AUTHORITIES.has(entity.authority), `${entity.id}: unsupported authority ${entity.authority}`);
    assert(typeof entity.title === 'string' && entity.title.length > 0, `${entity.id}: title is required`);
    assert(typeof entity.status === 'string' && entity.status.length > 0, `${entity.id}: status is required`);
    await validateLocator(entity.source_locator, entity.id);
  }

  const relationIds = new Set();
  for (const relation of graph.relations) {
    assert(typeof relation.id === 'string' && relation.id.length > 1, 'relation id is required');
    assert(!relationIds.has(relation.id), `duplicate relation id: ${relation.id}`);
    relationIds.add(relation.id);
    assert(ALLOWED_RELATION_TYPES.has(relation.type), `${relation.id}: unsupported relation type ${relation.type}`);
    assert(relation.version === '1.0', `${relation.id}: relation version must be 1.0`);
    assert(entityIds.has(relation.from), `${relation.id}: dangling from endpoint ${relation.from}`);
    assert(entityIds.has(relation.to), `${relation.id}: dangling to endpoint ${relation.to}`);
    await validateLocator(relation.source_locator, relation.id);
  }

  console.log(`Knowledge Graph validation PASS: entities=${entityIds.size}; relations=${relationIds.size}; authority=${graph.authority}`);
};

main().catch((error) => {
  console.error(`Knowledge Graph validation FAILED: ${error.message}`);
  process.exitCode = 1;
});
