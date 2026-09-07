import fs from 'node:fs';

export function validateReadModel(readModel, sourceContract) {
  const errors = []; const fail = m => errors.push(m);
  if (!readModel || typeof readModel !== 'object' || Array.isArray(readModel)) return ['read model must be an object'];
  const rootAllowed = new Set(['schema_version','component','authority','source_contract','items']);
  for (const k of Object.keys(readModel)) if (!rootAllowed.has(k)) fail(`unexpected root property ${k}`);
  if (readModel.schema_version !== '1.0') fail('read model schema_version must be 1.0');
  if (readModel.component !== 'DSG.KnowledgeConsumerReadModel') fail('read model component mismatch');
  if (readModel.authority !== 'projection') fail('read model authority must remain projection');
  if (readModel.source_contract !== 'docs/data/knowledge-ai-evidence-contract.json') fail('source_contract mismatch');
  if (!Array.isArray(readModel.items)) { fail('items must be an array'); return errors; }

  const sourceItems = new Map((sourceContract?.items ?? []).map(x => [x.id, x]));
  const citations = new Map((sourceContract?.citations ?? []).map(x => [`${x.id}@${x.version}`, x]));
  const provenance = new Map((sourceContract?.provenance_records ?? []).map(x => [`${x.id}@${x.version}`, x]));
  const confidence = new Set((sourceContract?.confidence_contracts ?? []).map(x => `${x.id}@${x.version}`));
  const itemAllowed = new Set(['id','source_item_ref','semantic_type','lifecycle_state','source_authority','ai_derived','producer','producer_version','produced_at_utc','observed_at_utc','method_id','evidence_refs','conflict_refs','citations','provenance','confidence']);
  const seenIds = new Set(), seenSources = new Set();

  for (const item of readModel.items) {
    if (!item || typeof item !== 'object' || Array.isArray(item)) { fail('consumer item must be an object'); continue; }
    for (const k of Object.keys(item)) if (!itemAllowed.has(k)) fail(`${item.id ?? '<unknown>'}: unexpected property ${k}`);
    for (const k of ['id','source_item_ref','semantic_type','lifecycle_state','source_authority','ai_derived','producer','produced_at_utc','citations','provenance']) if (!(k in item)) fail(`${item.id ?? '<unknown>'}: required property ${k} missing`);
    if (seenIds.has(item.id)) fail(`${item.id}: duplicate consumer id`); else seenIds.add(item.id);
    if (seenSources.has(item.source_item_ref)) fail(`${item.id}: duplicate source_item_ref ${item.source_item_ref}`); else seenSources.add(item.source_item_ref);
    const src = sourceItems.get(item.source_item_ref);
    if (!src) { fail(`${item.id}: unresolved source_item_ref ${item.source_item_ref}`); continue; }
    for (const key of ['semantic_type','lifecycle_state','source_authority','ai_derived','producer','produced_at_utc','producer_version','observed_at_utc','method_id']) if ((item[key] ?? null) !== (src[key] ?? null)) fail(`${item.id}: ${key} must exactly preserve source item`);
    for (const key of ['evidence_refs','conflict_refs']) if (JSON.stringify(item[key] ?? []) !== JSON.stringify(src[key] ?? [])) fail(`${item.id}: ${key} must exactly preserve source item`);
    if (src.semantic_type === 'observation' && !item.observed_at_utc) fail(`${item.id}: Observation must preserve observed_at_utc`);
    if (['claim','inference','recommendation'].includes(src.semantic_type) && !item.method_id) fail(`${item.id}: ${src.semantic_type} must preserve method_id`);
    if (src.semantic_type === 'conflict' && !Array.isArray(item.conflict_refs)) fail(`${item.id}: Conflict must preserve conflict_refs`);

    const expectedCitationRefs = src.citation_refs ?? [], actualCitationRefs = (item.citations ?? []).map(x => x.ref);
    if (JSON.stringify(actualCitationRefs) !== JSON.stringify(expectedCitationRefs)) fail(`${item.id}: Citation identities must be preserved exactly`);
    for (const projected of item.citations ?? []) { const governed = citations.get(projected.ref); if (!governed) { fail(`${item.id}: unresolved Citation ${projected.ref}`); continue; } if (projected.source_authority !== governed.source_authority) fail(`${item.id}: Citation authority mismatch ${projected.ref}`); if (projected.locator?.kind !== governed.locator?.kind || projected.locator?.value !== governed.locator?.value || (projected.locator?.anchor ?? null) !== (governed.locator?.anchor ?? null)) fail(`${item.id}: Citation locator mismatch ${projected.ref}`); }
    const expectedProvRefs = src.provenance_refs ?? [], actualProvRefs = (item.provenance ?? []).map(x => x.ref);
    if (JSON.stringify(actualProvRefs) !== JSON.stringify(expectedProvRefs)) fail(`${item.id}: Provenance identities must be preserved exactly`);
    for (const projected of item.provenance ?? []) { const governed = provenance.get(projected.ref); if (!governed) { fail(`${item.id}: unresolved Provenance ${projected.ref}`); continue; } for (const key of ['method_id','output_ref']) if (projected[key] !== governed[key]) fail(`${item.id}: Provenance ${key} mismatch ${projected.ref}`); for (const key of ['input_refs','citation_refs']) if (JSON.stringify(projected[key] ?? []) !== JSON.stringify(governed[key] ?? [])) fail(`${item.id}: Provenance ${key} mismatch ${projected.ref}`); }
    if (src.confidence) { if (!item.confidence) fail(`${item.id}: Confidence must not be dropped`); else { if (item.confidence.contract_ref !== src.confidence.contract_ref || item.confidence.value !== src.confidence.value) fail(`${item.id}: Confidence contract/value must be preserved exactly`); if (!confidence.has(item.confidence.contract_ref)) fail(`${item.id}: unresolved Confidence contract ${item.confidence.contract_ref}`); } } else if (item.confidence) fail(`${item.id}: consumer cannot invent Confidence`);
  }
  return errors;
}

if (process.argv[1]?.endsWith('verify-knowledge-ai-read-model.mjs')) {
  const readModel = JSON.parse(fs.readFileSync('docs/data/knowledge-ai-read-model.json', 'utf8'));
  const source = JSON.parse(fs.readFileSync('docs/data/knowledge-ai-evidence-contract.json', 'utf8'));
  const errors = validateReadModel(readModel, source);
  if (errors.length) { console.error(errors.join('\n')); process.exit(1); }
  console.log(`Knowledge / AI consumer read model OK: ${readModel.items.length} items`);
}
