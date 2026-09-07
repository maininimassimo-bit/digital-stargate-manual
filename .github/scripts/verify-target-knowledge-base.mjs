import fs from 'node:fs';

const ref = (id, version = '1.0') => `${id}@${version}`;
const isObject = x => x && typeof x === 'object' && !Array.isArray(x);
const unique = a => Array.isArray(a) && new Set(a).size === a.length;
const nonEmptyStrings = a => Array.isArray(a) && a.every(x => typeof x === 'string' && x.length >= 2) && unique(a);
const exactKeys = (obj, allowed, label, fail) => { if (!isObject(obj)) { fail(`${label}: must be an object`); return; } for (const k of Object.keys(obj)) if (!allowed.includes(k)) fail(`${label}: unexpected property ${k}`); };
const required = (obj, keys, label, fail) => { for (const k of keys) if (!(k in (obj ?? {}))) fail(`${label}: required property ${k} missing`); };

export function validateTargetKnowledgeBase(kb, catalog) {
  const errors = []; const fail = m => errors.push(m);
  if (!isObject(kb)) return ['target knowledge base must be an object'];

  // Normative executable structural validation for schemas/target-knowledge-base.schema.json.
  const rootKeys = ['schema_version','component','authority','baseline_commit','bounds','identities','relations','citations','provenance_records'];
  exactKeys(kb, rootKeys, 'root', fail); required(kb, rootKeys, 'root', fail);
  if (kb.schema_version !== '1.0') fail('schema_version must be 1.0');
  if (kb.component !== 'DSG.TargetKnowledgeBaseProjection') fail('component mismatch');
  if (kb.authority !== 'projection') fail('authority must remain projection');
  if (!/^[0-9a-f]{40}$/.test(kb.baseline_commit ?? '')) fail('baseline_commit must be a full commit SHA');
  exactKeys(kb.bounds, ['max_identities','max_relations'], 'bounds', fail); required(kb.bounds, ['max_identities','max_relations'], 'bounds', fail);
  if (kb.bounds?.max_identities !== 5 || kb.bounds?.max_relations !== 10) fail('F2 bounds must remain 5 identities / 10 relations');
  if (!Array.isArray(kb.identities) || kb.identities.length > 5) fail('identity bound exceeded or identities missing');
  if (!Array.isArray(kb.relations) || kb.relations.length > 10) fail('relation bound exceeded or relations missing');
  if (!Array.isArray(kb.citations)) fail('citations must be an array');
  if (!Array.isArray(kb.provenance_records)) fail('provenance_records must be an array');

  const identityKeys = ['target_key','canonical_name','aliases','identity_state','source_refs','citation_refs','provenance_refs'];
  for (const [i, x] of (kb.identities ?? []).entries()) {
    const label = `identity[${i}]`; exactKeys(x, identityKeys, label, fail); required(x, identityKeys, label, fail);
    if (typeof x.canonical_name !== 'string' || !x.canonical_name.length) fail(`${label}: canonical_name must be non-empty`);
    if (!Array.isArray(x.aliases) || !unique(x.aliases) || x.aliases.some(a => typeof a !== 'string' || !a.length)) fail(`${label}: aliases must be unique non-empty strings`);
    if (!nonEmptyStrings(x.source_refs) || !x.source_refs.length) fail(`${label}: source_refs must be unique non-empty refs`);
    if (!nonEmptyStrings(x.citation_refs)) fail(`${label}: citation_refs must be unique refs`);
    if (!nonEmptyStrings(x.provenance_refs)) fail(`${label}: provenance_refs must be unique refs`);
  }
  const relationKeys = ['id','relation_type','target_key','session_id','object_ref','source_refs','citation_refs','provenance_refs'];
  for (const [i, x] of (kb.relations ?? []).entries()) {
    const label = `relation[${i}]`; exactKeys(x, relationKeys, label, fail); required(x, relationKeys, label, fail);
    if (typeof x.id !== 'string' || x.id.length < 2 || typeof x.object_ref !== 'string' || x.object_ref.length < 2) fail(`${label}: id/object_ref must be refs`);
    if (!(typeof x.session_id === 'string' || x.session_id === null)) fail(`${label}: session_id must be string or null`);
    if (!nonEmptyStrings(x.source_refs) || !x.source_refs.length || !nonEmptyStrings(x.citation_refs) || !x.citation_refs.length || !nonEmptyStrings(x.provenance_refs)) fail(`${label}: source/Citation/Provenance refs violate schema`);
  }
  const citationKeys = ['id','version','source_authority','locator'];
  const locatorKeys = ['path','record_key','record_value'];
  for (const [i, x] of (kb.citations ?? []).entries()) {
    const label = `citation[${i}]`; exactKeys(x, citationKeys, label, fail); required(x, citationKeys, label, fail);
    exactKeys(x.locator, locatorKeys, `${label}.locator`, fail); required(x.locator, locatorKeys, `${label}.locator`, fail);
    for (const k of ['id','version']) if (typeof x[k] !== 'string' || !x[k].length) fail(`${label}: ${k} must be non-empty`);
    for (const k of locatorKeys) if (typeof x.locator?.[k] !== 'string' || !x.locator[k].length) fail(`${label}.locator: ${k} must be non-empty`);
  }
  const provenanceKeys = ['id','version','method_id','input_refs','output_ref','citation_refs'];
  for (const [i, x] of (kb.provenance_records ?? []).entries()) {
    const label = `provenance[${i}]`; exactKeys(x, provenanceKeys, label, fail); required(x, provenanceKeys, label, fail);
    if (typeof x.id !== 'string' || !x.id.length || typeof x.version !== 'string' || !x.version.length || typeof x.output_ref !== 'string' || x.output_ref.length < 2) fail(`${label}: id/version/output_ref violate schema`);
    if (!nonEmptyStrings(x.input_refs) || !x.input_refs.length || !nonEmptyStrings(x.citation_refs) || !x.citation_refs.length) fail(`${label}: input_refs/citation_refs violate schema`);
  }

  const sessions = new Map((catalog?.sessions ?? []).map(x => [x.sessionId, x]));
  const citations = new Map((kb.citations ?? []).map(x => [ref(x.id, x.version), x]));
  const provenance = new Map((kb.provenance_records ?? []).map(x => [ref(x.id, x.version), x]));
  const identities = new Map(); const relationIds = new Set();

  for (const citation of kb.citations ?? []) {
    if (citation.source_authority !== 'governed_scientific_projection') fail(`${citation.id}: fixture citation authority must remain governed_scientific_projection`);
    if (citation.locator?.path !== 'docs/data/scientific-session-catalog.json' || citation.locator?.record_key !== 'sessions[].sessionId') fail(`${citation.id}: citation must use canonical Session Catalog locator`);
    if (!sessions.has(citation.locator?.record_value)) fail(`${citation.id}: unresolved session locator ${citation.locator?.record_value}`);
  }

  for (const identity of kb.identities ?? []) {
    if (!/^dsg-target:[a-z0-9]+(?:-[a-z0-9]+)*$/.test(identity.target_key ?? '')) fail(`${identity.target_key ?? '<unknown>'}: invalid target_key`);
    if (identities.has(identity.target_key)) fail(`${identity.target_key}: duplicate target_key`); else identities.set(identity.target_key, identity);
    if (!['validated','conflicted','incomplete','unknown'].includes(identity.identity_state)) fail(`${identity.target_key}: invalid identity_state`);
    if (identity.identity_state === 'validated' && (!Array.isArray(identity.citation_refs) || identity.citation_refs.length === 0)) fail(`${identity.target_key}: validated identity requires Citation`);
    for (const c of identity.citation_refs ?? []) if (!citations.has(c)) fail(`${identity.target_key}: unresolved Citation ${c}`);
    for (const p of identity.provenance_refs ?? []) if (!provenance.has(p)) fail(`${identity.target_key}: unresolved Provenance ${p}`);

    const sourceSessions = (identity.source_refs ?? []).filter(x => x.startsWith('session:')).map(x => x.slice(8));
    const records = sourceSessions.map(x => sessions.get(x));
    if (records.some(x => !x)) { fail(`${identity.target_key}: unresolved source session`); continue; }
    if (records.length) {
      const names = new Set(records.map(x => x.target));
      if (names.size !== 1) fail(`${identity.target_key}: primary governed target names conflict`);
      if (identity.canonical_name !== records[0].target) fail(`${identity.target_key}: canonical_name must preserve primary governed target name`);
      const coordinatePairs = new Set(records.filter(x => Number.isFinite(x.raDeg) && Number.isFinite(x.decDeg)).map(x => `${x.raDeg}|${x.decDeg}`));
      if (coordinatePairs.size > 1) fail(`${identity.target_key}: governed coordinate evidence conflicts; automatic merge prohibited`);
    }
    const expectedSources = [...identity.source_refs].sort();
    const expectedCitations = [...identity.citation_refs].sort();
    for (const pRef of identity.provenance_refs ?? []) {
      const p = provenance.get(pRef); if (!p) continue;
      if (p.output_ref !== identity.target_key) fail(`${identity.target_key}: Provenance output_ref must bind to identity`);
      if (JSON.stringify([...p.input_refs].sort()) !== JSON.stringify(expectedSources)) fail(`${identity.target_key}: Provenance input_refs must bind exactly to identity source_refs`);
      if (JSON.stringify([...p.citation_refs].sort()) !== JSON.stringify(expectedCitations)) fail(`${identity.target_key}: Provenance Citation set must bind exactly to identity citations`);
    }
    for (const cRef of identity.citation_refs ?? []) {
      const c = citations.get(cRef); if (c && !identity.source_refs.includes(`session:${c.locator.record_value}`)) fail(`${identity.target_key}: Citation must bind to an identity source session`);
    }
  }

  for (const relation of kb.relations ?? []) {
    if (relationIds.has(relation.id)) fail(`${relation.id}: duplicate relation id`); else relationIds.add(relation.id);
    if (!identities.has(relation.target_key)) fail(`${relation.id}: unresolved target_key ${relation.target_key}`);
    for (const c of relation.citation_refs ?? []) if (!citations.has(c)) fail(`${relation.id}: unresolved Citation ${c}`);
    for (const p of relation.provenance_refs ?? []) if (!provenance.has(p)) fail(`${relation.id}: unresolved Provenance ${p}`);
    if (['TARGET_HAS_SESSION','TARGET_HAS_SQM_EVIDENCE','TARGET_USES_SETUP','TARGET_HAS_ASSET','TARGET_HAS_PROCESSING_PROVENANCE'].includes(relation.relation_type) && !relation.session_id) fail(`${relation.id}: ${relation.relation_type} must remain session-scoped`);
    if (relation.session_id) {
      const session = sessions.get(relation.session_id);
      if (!session) fail(`${relation.id}: unresolved session_id ${relation.session_id}`);
      else if (identities.get(relation.target_key)?.canonical_name !== session.target) fail(`${relation.id}: relation target conflicts with governed session target`);
    }
    if (relation.relation_type === 'TARGET_HAS_SESSION') {
      const expectedSource = `session:${relation.session_id}`;
      if (relation.object_ref !== expectedSource) fail(`${relation.id}: object_ref must equal session:<session_id>`);
      if (JSON.stringify(relation.source_refs) !== JSON.stringify([expectedSource])) fail(`${relation.id}: source_refs must bind exactly to relation session`);
      for (const cRef of relation.citation_refs ?? []) { const c = citations.get(cRef); if (c?.locator?.record_value !== relation.session_id) fail(`${relation.id}: Citation must bind to relation session_id`); }
      for (const pRef of relation.provenance_refs ?? []) { const p = provenance.get(pRef); if (!p) continue; if (p.output_ref !== relation.id) fail(`${relation.id}: Provenance output_ref must bind to relation id`); if (JSON.stringify(p.input_refs) !== JSON.stringify([expectedSource])) fail(`${relation.id}: Provenance input_refs must bind exactly to relation session`); if (JSON.stringify([...p.citation_refs].sort()) !== JSON.stringify([...relation.citation_refs].sort())) fail(`${relation.id}: Provenance Citation set must bind exactly to relation citations`); }
    }
    if (relation.relation_type !== 'TARGET_HAS_SESSION') fail(`${relation.id}: bounded F2 fixture may materialize TARGET_HAS_SESSION only; later relations require their governed source reconciliation`);
  }

  for (const p of kb.provenance_records ?? []) {
    if (!['BKL035-F2-TARGET-KEY-1','BKL035-F2-SOURCE-LINK-1'].includes(p.method_id)) fail(`${p.id}: ungoverned derivation method ${p.method_id}`);
    for (const c of p.citation_refs ?? []) if (!citations.has(c)) fail(`${p.id}: unresolved Citation ${c}`);
  }
  return errors;
}

if (process.argv[1]?.endsWith('verify-target-knowledge-base.mjs')) {
  const kb = JSON.parse(fs.readFileSync('docs/data/target-knowledge-base.json', 'utf8'));
  const catalog = JSON.parse(fs.readFileSync('docs/data/scientific-session-catalog.json', 'utf8'));
  const errors = validateTargetKnowledgeBase(kb, catalog);
  if (errors.length) { console.error(errors.join('\n')); process.exit(1); }
  console.log(`Target Knowledge Base F2 structural+semantic contract OK: ${kb.identities.length} identities / ${kb.relations.length} relations`);
}
