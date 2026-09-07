import fs from 'node:fs';

const readJson = p => JSON.parse(fs.readFileSync(p, 'utf8'));
const parseCsv = text => {
  const rows=[]; let row=[], cell='', quoted=false;
  for (let i=0;i<text.length;i++) { const c=text[i], n=text[i+1]; if (c==='"') { if (quoted && n==='"') { cell+='"'; i++; } else quoted=!quoted; } else if (c===',' && !quoted) { row.push(cell); cell=''; } else if ((c==='\n'||c==='\r') && !quoted) { if (c==='\r'&&n==='\n') i++; row.push(cell); if (row.some(x=>x!=='')) rows.push(row); row=[]; cell=''; } else cell+=c; }
  if (cell || row.length) { row.push(cell); rows.push(row); }
  const [head,...data]=rows; return data.map(r=>Object.fromEntries(head.map((h,i)=>[h,r[i]??''])));
};
const uniq = xs => new Set(xs).size===xs.length;
const exactKeys=(o,keys)=>Object.keys(o).length===keys.length&&keys.every(k=>Object.hasOwn(o,k));

export function validateTargetIdentityReconciliation(doc, tkb, metadataRows) {
  const e=[];
  const root=['schema_version','component','authority','baseline_commit','source_contract','bounds','matches','conflicts'];
  if (!exactKeys(doc,root)) e.push('root structure must match F3 contract');
  if (doc.schema_version!=='1.0'||doc.component!=='DSG.TargetIdentityReconciliation') e.push('invalid F3 contract identity');
  if (doc.authority!=='projection') e.push('authority must remain projection');
  if (!/^[0-9a-f]{40}$/.test(doc.baseline_commit??'')) e.push('baseline_commit must be full SHA');
  const sc=doc.source_contract??{};
  if (sc.path!=='data/analytics/metadata/session-scientific-metadata.csv'||sc.authority!=='analytics_projection'||sc.key!=='session_id'||JSON.stringify(sc.accepted_states)!=='["REGISTERED"]') e.push('source contract must remain bounded analytics projection / REGISTERED only');
  if (doc.bounds?.max_matches!==5||doc.bounds?.max_conflicts!==5) e.push('F3 bounds must remain 5/5');
  if (!Array.isArray(doc.matches)||doc.matches.length>5) e.push('match bound exceeded');
  if (!Array.isArray(doc.conflicts)||doc.conflicts.length>5) e.push('conflict bound exceeded');
  const identities=new Map((tkb.identities??[]).map(x=>[x.target_key,x]));
  const registered=metadataRows.filter(r=>r.metadata_state==='REGISTERED');
  const bySession=new Map(registered.map(r=>[r.session_id,r]));
  const seenIds=new Map();
  for (const m of doc.matches??[]) {
    const keys=['target_key','target_id','canonical_name','aliases','session_ids','identity_state','source_authority','source_refs','method_id'];
    if (!exactKeys(m,keys)) { e.push(`match ${m.target_key??'?'} structure invalid`); continue; }
    const identity=identities.get(m.target_key);
    if (!identity) { e.push(`match ${m.target_key} has no F2 identity`); continue; }
    if (m.canonical_name!==identity.canonical_name) e.push(`match ${m.target_key} canonical name must preserve F2 identity`);
    if (m.identity_state!=='validated'||m.source_authority!=='analytics_projection'||m.method_id!=='BKL035-F3-EXACT-ID-RECONCILIATION-1') e.push(`match ${m.target_key} governance fields invalid`);
    if (!Array.isArray(m.aliases)||m.aliases.length!==0) e.push(`match ${m.target_key} aliases require explicit governed alias evidence`);
    if (!Array.isArray(m.session_ids)||!m.session_ids.length||!uniq(m.session_ids)) e.push(`match ${m.target_key} session_ids invalid`);
    const expectedRefs=(m.session_ids??[]).map(s=>`analytics-metadata:${s}`);
    if (JSON.stringify(m.source_refs)!==JSON.stringify(expectedRefs)) e.push(`match ${m.target_key} source_refs must bind exactly to metadata sessions`);
    const rows=(m.session_ids??[]).map(s=>bySession.get(s));
    if (rows.some(x=>!x)) e.push(`match ${m.target_key} references missing/non-REGISTERED metadata session`);
    else {
      if (rows.some(r=>r.target_name!==m.canonical_name)) e.push(`match ${m.target_key} target_name disagreement must fail closed`);
      if (rows.some(r=>r.target_id!==m.target_id)) e.push(`match ${m.target_key} target_id disagreement must fail closed`);
      if (!/^TGT-[A-Z0-9-]+$/.test(m.target_id)) e.push(`match ${m.target_key} target_id format invalid`);
    }
    if (seenIds.has(m.target_id)&&seenIds.get(m.target_id)!==m.target_key) e.push(`target_id ${m.target_id} maps to multiple target keys`); else seenIds.set(m.target_id,m.target_key);
  }
  for (const c of doc.conflicts??[]) {
    if (c.identity_state!=='conflicted'||c.method_id!=='BKL035-F3-EXACT-ID-RECONCILIATION-1') e.push(`conflict ${c.conflict_id??'?'} governance invalid`);
    if (!['TARGET_ID_DISAGREEMENT','CANONICAL_NAME_DISAGREEMENT','ALIAS_COLLISION'].includes(c.reason)) e.push(`conflict ${c.conflict_id??'?'} reason invalid`);
  }
  return e;
}

if (import.meta.url===`file://${process.argv[1]}`) {
  const doc=readJson('docs/data/target-identity-reconciliation.json');
  const tkb=readJson('docs/data/target-knowledge-base.json');
  const rows=parseCsv(fs.readFileSync('data/analytics/metadata/session-scientific-metadata.csv','utf8'));
  const errors=validateTargetIdentityReconciliation(doc,tkb,rows);
  if (errors.length) { console.error(errors.join('\n')); process.exit(1); }
  console.log(`Target Identity Reconciliation F3 OK: ${doc.matches.length} matches / ${doc.conflicts.length} conflicts`);
}

export { parseCsv };
