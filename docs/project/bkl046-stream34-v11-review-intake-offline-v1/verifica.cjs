'use strict';
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');

const scope = 'BKL046_STREAM34_COMPLETE_VM_LAUNCHER';
const roles = ['arbPublic', 'rqPublic', 'enrollmentPublic'];
const hex = /^[a-f0-9]{64}$/;
const v11Subject = '0b029846da0412875e26595e2ead8361bc35fcef2c882ec2be95303b9582bdd1';
const digest = raw => crypto.createHash('sha256').update(raw).digest('hex');

function key(raw) {
  assert.equal(typeof raw,'string','TRUST_KEY_TYPE');
  const v = crypto.createPublicKey({key:Buffer.from(raw,'base64'),type:'spki',format:'der'});
  assert.equal(v.asymmetricKeyType,'ed25519','TRUST_KEY_TYPE');
  assert.equal(v.export({type:'spki',format:'der'}).toString('base64'),raw,'TRUST_KEY_ENCODING');
  return v;
}

function bounded(filename) {
  assert.ok(path.isAbsolute(filename),'ABSOLUTE_CONTROL_PATH');
  const metadata=fs.lstatSync(filename);
  assert.ok(metadata.isFile()&&!metadata.isSymbolicLink()&&metadata.nlink===1,'REGULAR_APPROVAL_FILE');
  const handle=fs.openSync(filename,'r');
  try {
    const bound=fs.fstatSync(handle);
    assert.ok(bound.dev===metadata.dev&&bound.ino===metadata.ino&&bound.nlink===1,'APPROVAL_FILE_IDENTITY');
    assert.ok(bound.size>0&&bound.size<=65536,'APPROVAL_FILE_SIZE');
    const buffer=Buffer.alloc(65537);
    const n=fs.readSync(handle,buffer,0,buffer.length,0);
    const after=fs.fstatSync(handle);
    assert.ok(n===bound.size&&after.size===bound.size&&after.mtimeMs===bound.mtimeMs,
              'APPROVAL_FILE_CHANGED_DURING_READ');
    return buffer.subarray(0,n);
  } finally {fs.closeSync(handle);}
}

function verify({subjectSha256, trustRaw, trustSha256, reviews}) {
  assert.ok(subjectSha256===v11Subject,'APPROVAL_SUBJECT_CHANGED');
  assert.match(trustSha256,hex,'AUTHENTICATED_TRUST_PIN_REQUIRED');
  assert.ok(digest(trustRaw)===trustSha256,'TRUST_DIGEST_CHANGED');
  const trust=JSON.parse(trustRaw);
  assert.equal(trust.schema,'BKL046_STREAM34_ROLE_TRUST_V1','TRUST_SCHEMA');
  assert.ok(new Set(roles.map(n=>trust[n])).size===3,'TRUST_ROLES_NOT_INDEPENDENT');
  const keys=Object.fromEntries(roles.map(n=>[n,key(trust[n])]));
  const accepted={};
  for(const role of ['ARB','RQ']){
    const packet=reviews[role];
    if(!packet&&role==='RQ')break;
    assert.ok(packet,'ARB_REQUIRED_FIRST');
    const raw=packet.receipt, origin=JSON.parse(packet.origin);
    const body=origin.body;
    assert.ok(crypto.verify(null,Buffer.from(JSON.stringify(body)),keys[role.toLowerCase()+'Public'],
                           Buffer.from(origin.signature,'base64')),'ORIGIN_SIGNATURE_INVALID');
    assert.ok(body.protocol==='BKL046_STREAM34_REVIEW_ORIGIN_V1'&&body.role===role&&body.scope===scope&&
              body.subjectSha256===subjectSha256&&body.receiptSha256===digest(raw)&&
              typeof body.reviewOrigin==='string'&&body.reviewOrigin.length>0,'ORIGIN_BINDING_MISMATCH');
    const review=JSON.parse(raw);
    assert.ok(review.role===role&&review.scope===scope&&review.subjectSha256===subjectSha256&&
              review.decision==='APPROVED'&&Array.isArray(review.blockers)&&review.blockers.length===0&&
              typeof review.reviewer==='string'&&review.reviewer.length>0,'REVIEW_NOT_APPROVED');
    if(role==='RQ')
      assert.ok(review.arbSha256===accepted.ARB.receiptSha256&&review.reviewer!==accepted.ARB.reviewer,'RQ_ARB_LINK');
    accepted[role]={receiptSha256:digest(raw),originSha256:digest(packet.origin),reviewer:review.reviewer};
  }
  return {status:accepted.RQ?'BOTH_RECEIPTS_VERIFIED':'ARB_VERIFIED_RQ_PENDING',
          subjectSha256,trustSha256,rolesVerified:Object.keys(accepted),
          receipts:Object.fromEntries(Object.entries(accepted).map(([role, item])=>
             [role,{receiptSha256:item.receiptSha256,originSha256:item.originSha256}])),
          enrollmentAttempted:false,deploymentAuthorized:false,admissionRequested:false,nativeExecutions:0};
}

function main(argv) {
  const [folder, subjectSha256, trustFile, trustSha256, report] = argv;
  assert.ok(path.isAbsolute(folder)&&path.isAbsolute(report),'ABSOLUTE_CONTROL_PATH');
  const reviews={};
  for(const role of ['ARB','RQ']){
    const receipt=path.join(folder,role+'.json'), origin=path.join(folder,role+'.origin.json');
    if(role==='RQ'&&!fs.existsSync(receipt)&&!fs.existsSync(origin))continue;
    reviews[role]={receipt:bounded(receipt),origin:bounded(origin)};
  }
  const result=verify({subjectSha256,trustRaw:bounded(trustFile),trustSha256,reviews});
  fs.writeFileSync(report,JSON.stringify(result,null,2)+'\n',{flag:'wx'});
}

module.exports={verify,digest};
if(require.main===module)main(process.argv.slice(2));
