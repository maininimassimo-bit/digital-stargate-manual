import test from 'node:test';
import assert from 'node:assert/strict';
import {OwnerSession, validateDescriptor} from '../../docs/javascripts/s4-lab-owner.mjs';

const descriptor = () => ({baseUrl: 'https://dsg-s4-lab-dddddddddddd-183451329061.europe-west1.run.app/',
  deadline: 1100, sessionRef: 'd'.repeat(32), sourceRevision: 'e'.repeat(40),
  jobs: [1, 2].map(i => ({requestId: String(i).repeat(32), bindingRef: String(i + 2).repeat(32)}))});
const health = d => ({protocol: 'DSG_S4_LAB_V1', sessionRef: d.sessionRef,
  sourceRevision: d.sourceRevision, storageMode: 'GCS_ADC'});
const audit = (d, complete = false) => ({...health(d), phase: complete ? null : 'CREATE',
  finishedPhases: complete ? ['REGISTER', 'CREATE'] : ['REGISTER'], bindings: d.jobs,
  jobs: complete ? d.jobs.map((request, i) => ({jobId: String(i), request, state: 'QUEUED'})) : [],
  generation: 4, sha256: 'f'.repeat(64), observedUpload412: 2,
  attempts: Array.from({length: 6}, (_, i) => ({committed: i < 4})),
  reads: ['REGISTER', 'CREATE'].flatMap(phase => ['A', 'B'].map(executor => ({phase, executor, generation: 1}))),
  copies: Array.from({length: 6}, () => ({verified: true}))});

test('default browser transport preserves the global fetch receiver', async () => {
  const saved = globalThis.fetch, d = descriptor(); let calls = 0;
  globalThis.fetch = function () {
    assert.equal(this, globalThis);calls++;
    return Promise.resolve({status: 200, json: async () => health(d)});
  };
  try {
    const session = new OwnerSession(d, 'FIXTURE', undefined, () => 1000);
    assert.deepEqual(await session.request('/health', undefined, false), health(d));
    assert.equal(calls, 1);session.forget();
  } finally {globalThis.fetch = saved;}
});

test('successful browser sequence preserves token privacy and confirms before repeat', async () => {
  const d = descriptor(), calls = []; let auditCount = 0;
  const transport = async (url, options) => {
    calls.push({path: url.pathname, options});
    const value = url.pathname === '/health' ? health(d) : url.pathname === '/lab/audit'
      ? audit(d, auditCount++ > 0) : url.pathname === '/lab/finish' ? {} : {jobId: url.pathname[3]};
    return {status: 200, json: async () => value};
  };
  const session = new OwnerSession(d, 'SECRET_TOKEN', transport, () => 1000);
  const receipt = await session.createPair();
  assert.equal(session.token, ''); assert.equal(session.uncertain, false);
  assert.equal(JSON.stringify(receipt).includes('SECRET_TOKEN'), false);
  assert.equal(calls[0].options.headers.Authorization, undefined);
  assert.deepEqual(calls.map(row => row.path), ['/health', '/lab/audit',
    '/e/A/v1/transient-analysis/jobs', '/e/B/v1/transient-analysis/jobs',
    '/lab/finish', '/lab/audit', '/e/A/v1/transient-analysis/jobs', '/e/B/v1/transient-analysis/jobs', '/lab/audit']);
  await assert.rejects(session.createPair(), /già utilizzata/);
});

test('one lost response sends no repeat and erases token', async () => {
  const d = descriptor(), calls = [];
  const transport = async url => {
    calls.push(url.pathname);
    if (url.pathname.includes('/e/B/')) throw Error('Lost acknowledgement');
    return {status: 200, json: async () => url.pathname === '/health' ? health(d) :
      url.pathname === '/lab/audit' ? audit(d) : {jobId: 'A'}};
  };
  const session = new OwnerSession(d, 'SECRET_TOKEN', transport, () => 1000);
  await assert.rejects(session.createPair(), /Coppia incerta/);
  assert.equal(session.token, '');assert.equal(session.uncertain, true);
  assert.equal(calls.filter(path => path.includes('/jobs')).length, 2);
  assert.equal(calls.includes('/lab/finish'), false);
  await assert.rejects(session.createPair(), /già utilizzata/);
});

test('wrong source or synthetic storage blocks token-bearing mutation', async () => {
  for (const changed of [{sourceRevision: 'f'.repeat(40)}, {storageMode: 'SYNTHETIC'}]) {
    const d = descriptor(), calls = [];
    const session = new OwnerSession(d, 'SECRET_TOKEN', async (url, options) => {
      calls.push(options); return {status: 200, json: async () => ({...health(d), ...changed})};
    }, () => 1000);
    await assert.rejects(session.createPair(), /non corrispondenti/);
    assert.equal(calls.length, 1);assert.equal(calls[0].headers.Authorization, undefined);
    assert.equal(session.token, '');
  }
});

test('descriptor rejects old services, expiry, duplicate jobs and extra settings', () => {
  for (const changed of [{baseUrl: 'https://dsg-pixinsight-pilot-183451329061.europe-west1.run.app/'},
    {deadline: 1000}, {deadline: 2801}, {extra: 'allowNative'}]) {
    assert.throws(() => validateDescriptor({...descriptor(), ...changed}, 1000));
  }
  const d = descriptor();d.jobs[1] = d.jobs[0];assert.throws(() => validateDescriptor(d, 1000));
});
