'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {createHash, createPublicKey, verify} = require('node:crypto');
const {compileFunction} = require('node:vm');
const {isBuiltin} = require('node:module');

const scope = 'BKL046_CFA_XDRZ_ORIGIN_DSG_SHARED_V1';
const hex = /^[0-9a-f]{64}$/;
const digest = (bytes) => createHash('sha256').update(bytes).digest('hex');

function readPinned(file, pin) {
  assert(path.isAbsolute(file) && hex.test(pin), 'invalid reviewed input pin');
  const info = fs.lstatSync(file);
  assert(info.isFile() && !info.isSymbolicLink(), 'reviewed input is redirected');
  const bytes = fs.readFileSync(file);
  assert.equal(digest(bytes), pin, 'reviewed bytes changed: ' + path.basename(file));
  return bytes;
}

function authorize({folder, trust}) {
  assert(trust?.scope === scope && trust.host === 'DSG-SHARED', 'managed activation not enrolled');
  const {approvalFile, approvalPin} = trust;
  assert(path.isAbsolute(folder), 'absolute candidate directory required');
  const approval = JSON.parse(readPinned(approvalFile, approvalPin));
  assert.equal(approval.scope, scope);
  assert.equal(approval.subjectSha256, trust.subjectSha256, 'subject not enrolled');
  assert.equal(approval.host, 'DSG-SHARED');
  assert.equal(process.env.COMPUTERNAME?.toUpperCase(), approval.host);
  assert(Number.isSafeInteger(approval.expires) && Date.now() < approval.expires, 'expired launch approval');
  const raw = readPinned(path.join(folder, 'launcher-subject.json'), approval.subjectSha256);
  const subject = JSON.parse(raw);
  assert.equal(subject.scope, scope);
  const publicKeys = new Set();
  const reviewers = new Set();
  for (const role of ['ARB', 'RQ']) {
    const review = approval[role];
    const enrolled = trust.reviewers?.[role];
    assert(enrolled && review.publicKey === enrolled.publicKey, 'review role key not enrolled: ' + role);
    const packet = JSON.parse(readPinned(review.path, review.sha256));
    const publicKey = createPublicKey({key: Buffer.from(review.publicKey, 'base64'), format: 'der', type: 'spki'});
    assert.equal(publicKey.asymmetricKeyType, 'ed25519');
    assert.equal(publicKey.export({format: 'der', type: 'spki'}).toString('base64'), review.publicKey);
    assert(!publicKeys.has(review.publicKey), 'review roles use the same signing identity');
    publicKeys.add(review.publicKey);
    const body = packet.body;
    assert.equal(body.reviewer, enrolled.reviewer, 'review identity not enrolled: ' + role);
    assert(verify(null, Buffer.from(JSON.stringify(body)), publicKey, Buffer.from(packet.signature, 'base64')),
      'invalid review signature: ' + role);
    assert(body.role === role && body.scope === scope && body.subjectSha256 === approval.subjectSha256 &&
      body.decision === 'APPROVED' && Array.isArray(body.blockers) && body.blockers.length === 0,
      'review scope or decision differs: ' + role);
    assert(typeof body.reviewer === 'string' && body.reviewer && !reviewers.has(body.reviewer),
      'reviewer identities are not independent');
    reviewers.add(body.reviewer);
    if (role === 'RQ') assert.equal(body.arbSha256, approval.ARB.sha256);
  }
  for (const member of [process.execPath, approval.python]) {
    readPinned(member, member === process.execPath ? subject.nodeSha256 : subject.pythonSha256);
  }
  const members = new Map();
  for (const [name, pin] of Object.entries(subject.memberSha256)) {
    assert(/^[A-Za-z0-9_.-]+\.(?:cjs|py)$/.test(name));
    members.set(name, readPinned(path.join(folder, name), pin));
  }
  for (const [relative, pin] of Object.entries(subject.authoritySha256)) {
    assert(/^[A-Za-z0-9_.-]+(?:\/[A-Za-z0-9_.-]+)*$/.test(relative)
      && !relative.split('/').some(part => part === '.' || part === '..'), 'invalid reviewed data name');
    readPinned(path.join(folder, relative), pin);
  }
  assert.equal(digest(members.get('entry.cjs')), digest(fs.readFileSync(__filename)), 'running entry differs');
  const cache = new Map();
  function load(name) {
    if (cache.has(name)) return cache.get(name).exports;
    assert(members.has(name) && name.endsWith('.cjs'), 'module outside reviewed package');
    const module = {exports: {}};
    const filename = path.join(folder, name);
    cache.set(name, module);
    const compile = compileFunction(members.get(name).toString('utf8'),
      ['require', 'module', '__filename', '__dirname'], {filename});
    compile((specifier) => {
      if (specifier.startsWith('node:') && isBuiltin(specifier)) return require(specifier);
      assert(/^\.\/[A-Za-z0-9_.-]+\.cjs$/.test(specifier), 'module outside reviewed namespace');
      return load(specifier.slice(2));
    }, module, filename, folder);
    return module.exports;
  }
  return {approval, subject, load};
}

async function main() {
  assert(process.argv.length === 2, 'activation accepts no caller arguments');
  const trust = require('./managed-activation.cjs');
  const {approval, subject, load} = authorize({folder: __dirname, trust});
  const result = await load('launcher.cjs').launch(subject, approval.python);
  console.log(JSON.stringify(result));
}

if (require.main === module) {
  main().catch((error) => { console.error(error.message); process.exitCode = 1; });
}

module.exports = {authorize};