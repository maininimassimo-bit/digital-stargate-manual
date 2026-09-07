import fs from 'node:fs';

const ref = (id, version = '1.0') => `${id}@${version}`;

export function validateTargetKnowledgeBase(kb, catalog) {
  const errors = []; const fail = m => errors.push(m);
  if (!kb || typeof kb !== 'object' || Array.isArray(kb)) return ['target knowledge base must be an object'];
  if (kb.schema_version !== '1.0') fail('schema_version must be 1.0');
  if (kb.component !== 'DSG.TargetKnowledgeBaseProjection') fail('component mismatch');
  if (kb.authority !== 'projection') fail('authority must remain projection');
  if (!/^[0-9a-f]{40}$/.test(kb.baseline_commit ?? '')) fail('baseline_commit must be a full commit SHA');
  if (kb.bounds?.max_identities !== 5 || kb.bounds?.max_relations !== 10) fail('F2 bounds must remain 5 identities / 10 relations');
  if (!Array.isArray(kb.identities) || kb.identities.length > 5) fail('identity bound exceeded or identities missing');
  if (!Array.isArray(kb.relations) || kb.relations.length > 10) fail('relation bound exceeded or relations missing');

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
    if (!Array.isArray(identity.source_refs) || identity.source_refs.length === 0) fail(`${identity.target_key}: source_refs required`);
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
  console.log(`Target Knowledge Base F2 OK: ${kb.identities.length} identities / ${kb.relations.length} relations`);
}
