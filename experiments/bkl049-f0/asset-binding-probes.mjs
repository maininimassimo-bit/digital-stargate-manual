// F0-only experiment against existing reconciliation. Synthetic IDs; no images or PixInsight.
import assert from 'node:assert/strict';
import { PixInsightReconciliationService } from '../../.github/scripts/pixinsight-reconciliation.mjs';
const stamp='2026-09-30T00:00:00Z';
const manifest=()=>({observationContext:{sessionId:'SYNTHETIC-SESSION'},processingRun:{inputs:['SYNTHETIC-MAIN','SYNTHETIC-STARS'],outputs:['SYNTHETIC-FINAL']}});
const assets=()=>['MAIN','STARS','FINAL'].map((name)=>({assetId:`SYNTHETIC-${name}`,sha256:'a'.repeat(64),integrityState:'VERIFIED'}));
const catalogItems=[{entityId:'SYNTHETIC-SESSION',catalogItemId:'SYNTHETIC-CATALOG'}];
const reconcile=(items=assets(),m=manifest(),catalog=catalogItems)=>new PixInsightReconciliationService({assets:items,catalogItems:catalog}).reconcile(m,{reconciledAt:stamp});
const results=[];
function probe(id,finding,fn){fn();results.push({id,outcome:'REPRODUCED',finding});}
probe('A01','Exact asset and session IDs yield matched with read-only authority.',()=>{const r=reconcile();assert.equal(r.state,'matched');assert.equal(r.authority.mode,'read-only');});
probe('A02','Same display name with a different asset ID does not resolve the expected output.',()=>{const a=assets();a[2]={...a[2],assetId:'SYNTHETIC-OTHER',displayName:'SYNTHETIC-FINAL'};const r=reconcile(a);assert.equal(r.state,'partially-matched');assert.deepEqual(r.outputs.missing,['SYNTHETIC-FINAL']);});
probe('A03','Known asset integrity conflict yields conflict.',()=>{const a=assets();a[2].integrityState='CONFLICT';assert.equal(reconcile(a).state,'conflict');});
probe('A04','Missing session remains partially matched despite exact assets.',()=>assert.equal(reconcile(assets(),manifest(),[]).state,'partially-matched'));
probe('A05','Different catalog digests under the same IDs both yield matched: this layer does not prove expected byte identity.',()=>{const a=assets();a[2].sha256='b'.repeat(64);assert.equal(reconcile().state,'matched');assert.equal(reconcile(a).state,'matched');});
probe('A06','Duplicate asset IDs select the last record; conflicting duplicates require an upstream uniqueness invariant.',()=>{const a=assets();const conflict={...a[2],integrityState:'CONFLICT'};assert.equal(reconcile([...a,conflict]).state,'conflict');assert.equal(reconcile([conflict,...a]).state,'matched');});
console.log(JSON.stringify({experiment:'BKL049-F0-ASSET-BINDING',dataClass:'SYNTHETIC_ONLY',scope:'Direct calls to existing reconciliation; minimal internal input, not a validated full manifest or a live gallery integration',results},null,2));
