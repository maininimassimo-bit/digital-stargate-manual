'use strict';
const assert = require('node:assert/strict');
const {createHash, generateKeyPairSync, sign} = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const {spawnSync} = require('node:child_process');
const {authorize} = require('./entry.cjs');
const digest = (bytes) => createHash('sha256').update(bytes).digest('hex');
const root = __dirname;
const subjectFile = path.join(root, 'launcher-subject.json');
const subject = JSON.parse(fs.readFileSync(subjectFile));
const subjectSha = digest(fs.readFileSync(subjectFile));
const [python, output] = process.argv.slice(2);
const temp = fs.mkdtempSync(path.join(root, 'test-'));
function write(name, value) {
  const location = path.join(temp, name + '.json');
  const bytes = Buffer.from(JSON.stringify(value) + '\n');
  fs.writeFileSync(location, bytes, {flag: 'wx'});
  return {path: location, sha256: digest(bytes)};
}
function keys() {
  return generateKeyPairSync('ed25519');
}
function review(role, body, key, name = role) {
  const packet = {body, signature: sign(null, Buffer.from(JSON.stringify(body)), key.privateKey).toString('base64')};
  return {...write(name, packet), publicKey: key.publicKey.export({type: 'spki', format: 'der'}).toString('base64')};
}
const cases = [];
try {
  const seed = {scope: subject.scope, subjectSha256: subjectSha, decision: 'APPROVED', blockers: []};
  const arbKey = keys();
  const rqKey = keys();
  const ARB = review('ARB', {...seed, role: 'ARB', reviewer: 'synthetic-arb'}, arbKey);
  const rq = {...seed, role: 'RQ', reviewer: 'synthetic-rq', arbSha256: ARB.sha256};
  const RQ = review('RQ', rq, rqKey);
  const good = {scope: subject.scope, host: 'DSG-SHARED', subjectSha256: subjectSha,
    python, expires: Date.now() + 60000, ARB, RQ};
  const roles = {
    ARB: {reviewer: 'synthetic-arb', publicKey: ARB.publicKey},
    RQ: {reviewer: 'synthetic-rq', publicKey: RQ.publicKey},
  };
  function check(name, data, reason, overrides = {}) {
    const doc = write(name, data);
    const trust = {scope: subject.scope, host: 'DSG-SHARED', subjectSha256: subjectSha,
      approvalFile: doc.path, approvalPin: doc.sha256, reviewers: roles, ...overrides};
    const invoke = () => authorize({folder: root, trust});
    if (reason) assert.throws(invoke, reason);
    else assert.equal(typeof invoke().load('launcher.cjs').launch, 'function');
    cases.push({name, accepted: !reason});
  }
  check('signed-fixture-only', good);
  check('expired', {...good, expires: 0}, /expired/);
  check('wrong-subject', {...good, subjectSha256: 'a'.repeat(64)}, /subject not enrolled/);
  check('missing-rq', {...good, RQ: {...RQ, path: path.join(temp, 'absent.json')}}, {code: 'ENOENT'});
  check('wrong-role-key', {...good, RQ: {...RQ, publicKey: keys().publicKey.export({type: 'spki', format: 'der'}).toString('base64')}}, /role key not enrolled/);
  const blocker = review('RQ', {...rq, blockers: ['fixture blocker']}, rqKey, 'blocker');
  check('rq-blocker', {...good, RQ: blocker}, /scope or decision/);
  const otherArb = review('RQ', {...rq, arbSha256: 'f'.repeat(64)}, rqKey, 'swapped');
  check('wrong-arb-binding', {...good, RQ: otherArb}, /Expected values/);
  const shared = review('RQ', rq, arbKey, 'shared');
  check('same-role-key', {...good, RQ: shared}, /same signing identity/,
    {reviewers: {...roles, RQ: {...roles.RQ, publicKey: ARB.publicKey}}});
  check('caller-digest-not-enrolled', good, /reviewed bytes changed/, {approvalPin: 'a'.repeat(64)});
  const outsider = review('ARB', {...seed, role: 'ARB', reviewer: 'synthetic-arb'}, keys(), 'outsider');
  check('valid-signature-unenrolled-key', {...good, ARB: outsider}, /role key not enrolled/);
  const sibling = review('ARB', {...seed, role: 'ARB', reviewer: 'alternate-arb'}, arbKey, 'sibling');
  check('valid-signature-unenrolled-identity', {...good, ARB: sibling}, /identity not enrolled/);
  for (const [name, args, expected] of [
    ['cli-rejects-caller-approval', ['caller.json', 'f'.repeat(64)], /no caller arguments/],
    ['cli-rejects-without-enrollment', [], /managed activation not enrolled/],
  ]) {
    const result = spawnSync(process.execPath, [path.join(root, 'entry.cjs'), ...args],
      {windowsHide: true, encoding: 'utf8', timeout: 10000});
    assert.equal(result.status, 1, result.error?.message);
    assert.match(result.stderr, expected);
    cases.push({name, accepted: false});
  }
  const bootstrap=fs.readFileSync(path.join(root,'bootstrap.py'),'utf8');
  const result=spawnSync(python,['-I','-B','-S','-c',bootstrap,root,JSON.stringify(subject),'check-import'],
    {windowsHide:true,encoding:'utf8',timeout:10000});
  assert.equal(result.status,0,result.stderr || String(result.error));
  const imports=JSON.parse(result.stdout);
  assert.equal(imports.parentLoaded,true);
  assert.equal(imports.launched,false);
  const report={schema:'BKL046_CFA_ORIGIN_LAUNCHER_REVIEW_CANDIDATE_V1',subjectSha,cases,imports,
    testSigningKeysAreFixtures:true,admissionRequested:false,nativeExecutions:0,scientificClosures:0};
  fs.writeFileSync(output, JSON.stringify(report, null, 2) + '\n', {flag: 'wx'});
  console.log(JSON.stringify(report));
} finally {
  fs.rmSync(temp, {recursive: true});
}