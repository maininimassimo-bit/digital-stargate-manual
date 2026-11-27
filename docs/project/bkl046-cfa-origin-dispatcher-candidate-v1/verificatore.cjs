'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs/promises');
const path=require('node:path');
const {createHash}=require('node:crypto');
const {execFile}=require('node:child_process');
const {promisify}=require('node:util');
const exec=promisify(execFile);
const sha=raw=>createHash('sha256').update(raw).digest('hex');
const verifierPin='1a2036157bb31e4bf7a09408e7bef25051d19ff0e8fe891ab513690f7483aa06';
const cases=['zero-origin0','zero-origin05','half-origin0','half-origin05'];
const names=cases.flatMap(c=>['rgb','weight'].map(k=>c+'-'+k+'.fits')).sort();
const hypotheses=new Set(['use-declared','fixed-zero','fixed-half']);

function verifierFor(python, run, authority){
  const receipt=path.join(run,'control','comparison.json');
  async function check(pin){
    assert.equal(sha(await fs.readFile(authority.verifier)),verifierPin,'origin verifier bytes changed');
    const bytes=await fs.readFile(receipt);
    if(pin!==undefined)assert.equal(sha(bytes),pin,'origin receipt changed');
    return bytes;
  }
  async function revalidate(context,pin){
    const receiptBytes=await check(pin);
    const r=JSON.parse(receiptBytes);
    assert.equal(r.schema,'BKL046_CFA_ORIGIN_BOUND_BATCH_EVIDENCE_V1');
    assert.equal(r.reservation,context.reservation);
    assert.equal(r.operation,context.operation);
    assert.equal(r.batchSha256,context.subject);
    assert.equal(r.markerSha256,context.batchMarkerSha256);
    assert.equal(r.classification.planSha256,context.plan);
    assert.equal(r.classification.status,'MATCHED_TESTED_HYPOTHESIS');
    assert(r.classification.hypotheses.length===1 && hypotheses.has(r.classification.hypotheses[0]));
    assert.equal(sha(await fs.readFile(path.join(run,'batch.done.json'))),r.markerSha256,'marker changed');
    assert.equal(sha(await fs.readFile(path.join(run,'events.txt'))),r.eventsSha256,'origin transcript changed');
    assert.deepEqual(Object.keys(r.classification.outputSha256).sort(),names);
    assert.deepEqual((await fs.readdir(path.join(run,'outputs'))).sort(),names);
    for(const n of names){
      assert.equal(sha(await fs.readFile(path.join(run,'outputs',n))),r.classification.outputSha256[n],'FITS changed: '+n);
    }
    assert.deepEqual(await check(pin),receiptBytes);
  }
  async function compare(context){
    assert.equal(sha(await fs.readFile(authority.verifier)),verifierPin,'origin verifier bytes changed');
    await exec(python,['-I','-B','-S',authority.verifier,context.reservation,authority.plan,
                       authority.oracle,authority.comparator,authority.dependencies,run,receipt],
      {windowsHide:true,timeout:120000,maxBuffer:65536});
    const receiptSha256=sha(await check());
    await revalidate(context,receiptSha256);
    return {verified:true,reservation:context.reservation,batchMarkerSha256:context.batchMarkerSha256,receiptSha256};
  }
  return {receipt,compare,revalidate};
}
module.exports={verifierFor};
