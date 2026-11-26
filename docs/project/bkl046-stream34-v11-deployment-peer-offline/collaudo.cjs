'use strict';
const assert = require('node:assert/strict');
const {createHash, generateKeyPairSync, sign} = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const {createRequire} = require('node:module');
const {compileFunction} = require('node:vm');

const subjectSha256 = '0b029846da0412875e26595e2ead8361bc35fcef2c882ec2be95303b9582bdd1';
const sha = data => createHash('sha256').update(data).digest('hex');
const encode = value => Buffer.from(JSON.stringify(value));

async function main([root, scratch, output]) {
  assert.equal(process.env.COMPUTERNAME?.toUpperCase(), 'DSG-SHARED');
  for (const folder of [root,scratch,output]) assert(path.isAbsolute(folder));
  const subjectBytes = fs.readFileSync(path.join(root,'launcher-subject.json'));
  assert.equal(sha(subjectBytes),subjectSha256);
  const subject = JSON.parse(subjectBytes);
  assert.equal(subject.scope,'BKL046_STREAM34_COMPLETE_VM_LAUNCHER');
  for (const [name,pin] of Object.entries(subject.memberSha256))
    assert.equal(sha(fs.readFileSync(path.join(root,name))),pin,name);
  const source = path.join(root,'stream34_deployment_entry.cjs');
  const entryRaw = fs.readFileSync(source);
  assert.equal(sha(entryRaw), subject.memberSha256[path.basename(source)]);
  const module = {exports:{}};
  compileFunction(entryRaw.toString('utf8'),['require','module'],{filename:source})(createRequire(source),module);
  const {loadDeployment} = module.exports;

  fs.mkdirSync(scratch);
  const fixture = name => path.join(scratch,name);
  const peerDirectory = fixture('mailbox');
  fs.mkdirSync(peerDirectory);
  const write = (name,obj) => {
    const raw=encode(obj);
    fs.writeFileSync(fixture(name),raw,{flag:'wx'});
    return sha(raw);
  };
  const [arb,rq,enrollment,owner,peer] = Array.from({length:5},() => generateKeyPairSync('ed25519'));
  const pub = pair => pair.publicKey.export({format:'der',type:'spki'}).toString('base64');
  const packet = (body,pair) => ({body,signature:sign(null,encode(body),pair.privateKey).toString('base64')});
  const scope=subject.scope;
  const trustSha256=write('trust.json',{schema:'BKL046_STREAM34_ROLE_TRUST_V1',
    arbPublic:pub(arb),rqPublic:pub(rq),enrollmentPublic:pub(enrollment)});
  const receipt=(role,reviewer)=>({role,reviewer,decision:'APPROVED',scope,subjectSha256,blockers:[]});
  const arbSha256=write('ARB.json',receipt('ARB','fixture-arb'));
  const rqSha256=write('RQ.json',{...receipt('RQ','fixture-rq'),arbSha256});
  for (const [role,receiptSha256,key] of [['ARB',arbSha256,arb],['RQ',rqSha256,rq]])
    write(role+'.origin.json',packet({protocol:'BKL046_STREAM34_REVIEW_ORIGIN_V1',role,
      scope,subjectSha256,receiptSha256,reviewOrigin:'test-only'},key));
  const sessionNonce='5'.repeat(32);
  const valid={protocol:'BKL046_STREAM34_LAUNCH_ENROLLMENT_V1',scope,subjectSha256,
    arbSha256,rqSha256,providerSha256:subject.memberSha256['stream34_native_ui.cjs'],peerDirectory,
    sessionNonce,expires:Date.now()+15000,ownerPublic:pub(owner),peerPublic:pub(peer)};
  const enrollmentSha256=write('enrollment.json',packet(valid,enrollment));
  const expiredSha256=write('expired.json',packet({...valid,expires:0},enrollment));
  const python=fixture('python-placeholder.bin');
  fs.writeFileSync(python,'Offline fixture only. Not executable.',{flag:'wx'});
  const approval={schema:'BKL046_STREAM34_OPERATOR_DEPLOYMENT_V1',host:'DSG-SHARED',folder:root,
    reviews:scratch,python,trustFile:fixture('trust.json'),peerDirectory,subjectSha256,arbSha256,rqSha256,trustSha256};
  const pin=write('deployment.json',approval);
  const rejected=[];
  function reject(name,action,error) {
    assert.throws(action,error);
    rejected.push(name);
  }
  const transfer = (name,fields) => {
    const file=name+'.json';
    return [fixture(file),write(file,{...approval,...fields})];
  };
  reject('wrong_approval_pin',()=>loadDeployment(fixture('deployment.json'),'0'.repeat(64)),/DEPLOYMENT_APPROVAL_PIN_MISMATCH/);
  reject('other_host',()=>loadDeployment(...transfer('other-host',{host:'OTHER'})),/DEPLOYMENT_HOST_SCOPE/);
  reject('relative_peer_path',()=>loadDeployment(...transfer('relative-peer',{peerDirectory:'relative'})),/DEPLOYMENT_PATH:peerDirectory/);
  reject('wrong_subject',()=>loadDeployment(...transfer('other-subject',{subjectSha256:'0'.repeat(64)})),/DEPLOYMENT_SUBJECT_CHANGED/);
  const deployed=loadDeployment(fixture('deployment.json'),pin);
  let listed=0;
  const sky={async list_windows() {listed++; return [{id:17}];}};
  const opts={enrollmentFile:fixture('enrollment.json'),enrollmentSha256,sky,
    reviewActualFrame(){throw Error('UNEXPECTED_WINDOW_CAPTURE');}};
  async function rejectAsync(name, action,error) {
    await assert.rejects(action,error);
    rejected.push(name);
  }
  await rejectAsync('wrong_peer_key',()=>deployed.runSky({...opts,peerPrivateKey:owner.privateKey}),/AUTHORITY_ORIGINAL_SKY_KEY/);
  await rejectAsync('expired_session',()=>deployed.runSky({...opts,enrollmentFile:fixture('expired.json'),
    enrollmentSha256:expiredSha256,peerPrivateKey:peer.privateKey}),/AUTHORITY_ENROLLMENT_SCOPE_OR_EXPIRY/);
  await rejectAsync('nonmatching_python',()=>deployed.runOperator({...opts,ownerPrivateKey:owner.privateKey,
    onDiagnostic(){throw Error('UNEXPECTED_OPERATOR_START');}}),/LAUNCHER_PYTHON_PIN/);
  assert.equal(listed,0);

  const box=createRequire(source)('./stream34_mailbox.cjs');
  const {createPeerLease}=createRequire(source)('./stream34_peer.cjs');
  const listener=deployed.runSky({...opts,peerPrivateKey:peer.privateKey});
  listener.catch(()=>{});
  const lease=createPeerLease({scope:{subjectSha256,sessionNonce},ownerPrivateKey:owner.privateKey,
    peerPublicKey:peer.publicKey,exchange:box.createExchange(peerDirectory,'heartbeat')});
  assert.equal((await lease.check()).windowCount,1);
  assert.equal(listed,1);
  await box.publish(peerDirectory,'operator-finished',packet({
    protocol:'BKL046_STREAM34_OPERATOR_FINISHED_V1',subjectSha256,sessionNonce,
    status:'LEASE_RELEASED',reservation:'2ef31af6-ff22-48cf-bfb5-2e9c3bc772be'
  },owner));
  await rejectAsync('signed_completion_without_observed_close',()=>listener,/SKY_HOST_FINAL_BINDING/);

  const evidence={schema:'BKL046_STREAM34_V11_DEPLOYMENT_PEER_OFFLINE_V1',subjectSha256,
    entrySha256:sha(entryRaw),verifiedSubjectMembers:Object.keys(subject.memberSha256).length,
    simulatedHeartbeatThroughDeployment:true,fixtureWindowEnumerations:listed,rejections:rejected,
    independentApprovalsReceived:false,productionEnrollment:false,nativeAdmissionRequested:false,
    nativeExecutions:0,scientificClosures:0};
  fs.writeFileSync(output,JSON.stringify(evidence,null,2)+'\n',{flag:'wx'});
}
main(process.argv.slice(2)).catch(error=>{console.error(error);process.exitCode=1;});