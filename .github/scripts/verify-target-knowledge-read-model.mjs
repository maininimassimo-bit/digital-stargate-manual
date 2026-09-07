import fs from 'node:fs';
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const exact=(o,ks)=>o&&typeof o==='object'&&!Array.isArray(o)&&Object.keys(o).length===ks.length&&ks.every(k=>Object.hasOwn(o,k));
const ref=x=>`${x.id}@${x.version}`;
export function validateTargetKnowledgeReadModel(rm,tkb,rec){
 const e=[],root=['schema_version','component','authority','source_contracts','bounds','targets'];
 if(!exact(rm,root))e.push('root structure must match F4 contract');
 if(rm.schema_version!=='1.0'||rm.component!=='DSG.TargetKnowledgeConsumerReadModel'||rm.authority!=='projection')e.push('F4 identity/authority invalid');
 if(!same(rm.source_contracts,['docs/data/target-knowledge-base.json','docs/data/target-identity-reconciliation.json']))e.push('source contracts must remain exact F2/F3 projections');
 if(!exact(rm.bounds??{},['max_targets'])||rm.bounds?.max_targets!==5||!Array.isArray(rm.targets)||rm.targets.length>5)e.push('target bound invalid');
 const ids=new Map((tkb.identities??[]).map(x=>[x.target_key,x])), matches=new Map((rec.matches??[]).map(x=>[x.target_key,x]));
 const tkbCit=new Map((tkb.citations??[]).map(x=>[ref(x),x])),recCit=new Map((rec.citations??[]).map(x=>[ref(x),x]));
 const tkbProv=new Map((tkb.provenance_records??[]).map(x=>[ref(x),x])),recProv=new Map((rec.provenance_records??[]).map(x=>[ref(x),x]));
 const conflictsByTarget=new Map();for(const c of rec.conflicts??[]){if(!conflictsByTarget.has(c.target_key))conflictsByTarget.set(c.target_key,[]);conflictsByTarget.get(c.target_key).push(c.conflict_id);}
 const seen=new Set();
 for(const t of rm.targets??[]){const ks=['target_key','canonical_name','aliases','identity_state','target_id','target_id_state','scientific_sessions','reconciliation_evidence_sessions','source_authorities','citation_refs','provenance_refs','conflict_refs'];if(!exact(t,ks)){e.push(`${t.target_key??'?'} structure invalid`);continue;}if(seen.has(t.target_key))e.push(`duplicate target ${t.target_key}`);seen.add(t.target_key);const id=ids.get(t.target_key),m=matches.get(t.target_key);if(!id){e.push(`${t.target_key} missing F2 identity`);continue;}if(!m){e.push(`${t.target_key} missing F3 reconciliation`);continue;}
  for(const k of ['canonical_name','identity_state'])if(t[k]!==id[k])e.push(`${t.target_key} ${k} must preserve F2`);if(!same(t.aliases,id.aliases))e.push(`${t.target_key} aliases must preserve F2`);if(t.target_id!==m.target_id||t.target_id_state!==m.identity_state)e.push(`${t.target_key} target identifier must preserve F3`);
  const sci=(tkb.relations??[]).filter(r=>r.target_key===t.target_key&&r.relation_type==='TARGET_HAS_SESSION').map(r=>r.session_id).sort();if(!same([...t.scientific_sessions].sort(),sci))e.push(`${t.target_key} scientific sessions must preserve F2 relations`);if(!same(t.reconciliation_evidence_sessions,m.session_ids))e.push(`${t.target_key} reconciliation evidence sessions must preserve F3 evidence and remain distinct from scientific relations`);
  if(!same(t.source_authorities,['governed_scientific_projection','analytics_projection']))e.push(`${t.target_key} source authorities must remain explicit`);
  const expectedCit=[...id.citation_refs,...m.citation_refs],expectedProv=[...id.provenance_refs,...m.provenance_refs];if(!same(t.citation_refs,expectedCit))e.push(`${t.target_key} Citations must preserve F2/F3 identity lineage`);if(!same(t.provenance_refs,expectedProv))e.push(`${t.target_key} Provenance must preserve F2/F3 identity lineage`);for(const x of id.citation_refs)if(!tkbCit.has(x))e.push(`${t.target_key} unresolved F2 Citation ${x}`);for(const x of m.citation_refs)if(!recCit.has(x))e.push(`${t.target_key} unresolved F3 Citation ${x}`);for(const x of id.provenance_refs)if(!tkbProv.has(x))e.push(`${t.target_key} unresolved F2 Provenance ${x}`);for(const x of m.provenance_refs)if(!recProv.has(x))e.push(`${t.target_key} unresolved F3 Provenance ${x}`);
  const expectedConflicts=(conflictsByTarget.get(t.target_key)??[]).sort();if(!same([...t.conflict_refs].sort(),expectedConflicts))e.push(`${t.target_key} conflicts must remain explicit and complete`);if(expectedConflicts.length&&t.target_id_state!=='conflicted')e.push(`${t.target_key} conflict cannot be flattened to validated identifier`);
 }
 for(const key of ids.keys())if(matches.has(key)&&!seen.has(key))e.push(`eligible reconciled target ${key} omitted from consumer projection`);
 return e;
}
if(import.meta.url===`file://${process.argv[1]}`){const errors=validateTargetKnowledgeReadModel(read('docs/data/target-knowledge-read-model.json'),read('docs/data/target-knowledge-base.json'),read('docs/data/target-identity-reconciliation.json'));if(errors.length){console.error(errors.join('\n'));process.exit(1);}console.log('Target Knowledge F4 read model OK');}
