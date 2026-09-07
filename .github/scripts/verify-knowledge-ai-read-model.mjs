import fs from 'node:fs';

export function validateReadModel(readModel, sourceContract) {
  const errors = [];
  const fail = (message) => errors.push(message);
  if (readModel?.schema_version !== '1.0') fail('read model schema_version must be 1.0');
  if (readModel?.component !== 'DSG.KnowledgeConsumerReadModel') fail('read model component mismatch');
  if (readModel?.authority !== 'projection') fail('read model authority must remain projection');
  if (readModel?.source_contract !== 'docs/data/knowledge-ai-evidence-contract.json') fail('source_contract mismatch');
  if (!Array.isArray(readModel?.items)) fail('items must be an array');

  const sourceItems = new Map((sourceContract?.items ?? []).map(x => [x.id, x]));
  const citations = new Map((sourceContract?.citations ?? []).map(x => [`${x.id}@${x.version}`, x]));
  const provenance = new Map((sourceContract?.provenance_records ?? []).map(x => [`${x.id}@${x.version}`, x]));
  const confidence = new Set((sourceContract?.confidence_contracts ?? []).map(x => `${x.id}@${x.version}`));

  for (const item of readModel?.items ?? []) {
    const src = sourceItems.get(item.source_item_ref);
    if (!src) { fail(`${item.id}: unresolved source_item_ref ${item.source_item_ref}`); continue; }
    for (const key of ['semantic_type', 'lifecycle_state', 'source_authority', 'ai_derived', 'producer']) {
      if (item[key] !== src[key]) fail(`${item.id}: ${key} must exactly preserve source item`);
    }
    if ((src.producer_version ?? null) !== (item.producer_version ?? null)) fail(`${item.id}: producer_version must exactly preserve source item`);

    const expectedCitationRefs = src.citation_refs ?? [];
    const actualCitationRefs = (item.citations ?? []).map(x => x.ref);
    if (JSON.stringify(actualCitationRefs) !== JSON.stringify(expectedCitationRefs)) fail(`${item.id}: Citation identities must be preserved exactly`);
    for (const projected of item.citations ?? []) {
      const governed = citations.get(projected.ref);
      if (!governed) { fail(`${item.id}: unresolved Citation ${projected.ref}`); continue; }
      if (projected.source_authority !== governed.source_authority) fail(`${item.id}: Citation authority mismatch ${projected.ref}`);
      if (projected.locator?.kind !== governed.locator?.kind || projected.locator?.value !== governed.locator?.value || (projected.locator?.anchor ?? null) !== (governed.locator?.anchor ?? null)) fail(`${item.id}: Citation locator mismatch ${projected.ref}`);
    }

    const expectedProvRefs = src.provenance_refs ?? [];
    const actualProvRefs = (item.provenance ?? []).map(x => x.ref);
    if (JSON.stringify(actualProvRefs) !== JSON.stringify(expectedProvRefs)) fail(`${item.id}: Provenance identities must be preserved exactly`);
    for (const projected of item.provenance ?? []) {
      const governed = provenance.get(projected.ref);
      if (!governed) { fail(`${item.id}: unresolved Provenance ${projected.ref}`); continue; }
      for (const key of ['method_id', 'output_ref']) if (projected[key] !== governed[key]) fail(`${item.id}: Provenance ${key} mismatch ${projected.ref}`);
      for (const key of ['input_refs', 'citation_refs']) if (JSON.stringify(projected[key] ?? []) !== JSON.stringify(governed[key] ?? [])) fail(`${item.id}: Provenance ${key} mismatch ${projected.ref}`);
    }

    if (src.confidence) {
      if (!item.confidence) fail(`${item.id}: Confidence must not be dropped`);
      else {
        if (item.confidence.contract_ref !== src.confidence.contract_ref || item.confidence.value !== src.confidence.value) fail(`${item.id}: Confidence contract/value must be preserved exactly`);
        if (!confidence.has(item.confidence.contract_ref)) fail(`${item.id}: unresolved Confidence contract ${item.confidence.contract_ref}`);
      }
    } else if (item.confidence) fail(`${item.id}: consumer cannot invent Confidence`);

    if (src.ai_derived && !item.ai_derived) fail(`${item.id}: AI-derived marker cannot be removed`);
    if (src.lifecycle_state !== 'validated' && item.lifecycle_state === 'validated') fail(`${item.id}: consumer cannot promote lifecycle to validated`);
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
