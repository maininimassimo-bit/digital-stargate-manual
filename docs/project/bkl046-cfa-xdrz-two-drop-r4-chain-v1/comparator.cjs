'use strict';
const assert = require('node:assert/strict');
const {execFile} = require('node:child_process');
const {createHash} = require('node:crypto');
const fs = require('node:fs/promises');
const path = require('node:path');
const {promisify} = require('node:util');
const exec = promisify(execFile);

const plan = '841fea0e7bc282073fe21dd1fae08c183347084376e3bbdf3632bb062853d01b';
const subject = 'a2f32c59f7185f1ba18e7e4d3379663a232d2ab9c98db54466eed62003492568';
const operation = 'BKL046_CFA_XDRZ_TWO_DROP_CONTROL_DSG_SHARED_001';
const schema = 'BKL046_CFA_XDRZ_TWO_DROP_NUMERICAL_OUTPUT_VERIFICATION_V1';
const base = 'O:/BKL046-CFA-XDRZ-verifica-due-depositi-v1';
const verifyPin = '85727edc11cd83e2f7dff7b52ac6bde8d06601ff8a4367e1f375187995a580aa';
const caps = name => name === "console.log" ? 4194304 : 262144;
const sha = raw => createHash('sha256').update(raw).digest('hex');
const hex = /^[0-9a-f]{64}$/;
const labels = ['070','100'].flatMap(width =>
  ['unmasked','mask-green','mask-wrong-channel','zero-detector','zero-reference','fractional'].map(id => width+'-'+id));
const names = ['batch.done.json','events.txt','console.log',
  ...labels.flatMap(id=>['rgb','weight'].map(kind=>id+'-'+kind+'.fits'))].sort();

async function read(file, cap = 262144) {
  const st = await fs.lstat(file);
  assert(st.isFile() && !st.isSymbolicLink() && st.size > 0 && st.size <= cap, 'Invalid product member');
  const raw = await fs.readFile(file);
  assert.equal(raw.length, st.size, 'Product changed size');
  return raw;
}

function verifierFor(python, packages, run) {
  const outputs = path.join(run,'products');
  const control = path.join(run,'control');
  const receipt = path.join(control,'comparison.json');
  const numeric = path.join(control,'numeric.json');

  function bound(context) {
    assert.equal(context.operation, operation);
    assert.equal(context.plan, plan);
    assert.equal(context.subject, subject);
    assert.equal(path.basename(run), context.reservation);
    assert.match(context.reservation, /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/);
    assert.match(context.batchMarkerSha256, hex);
  }

  async function revalidate(context, expected) {
    bound(context);
    const raw = await read(receipt);
    assert.equal(sha(raw),expected,'Comparison receipt changed');
    const data = JSON.parse(raw);
    assert.equal(data.reservation,context.reservation);
    assert.equal(data.operation,operation);
    assert.equal(data.plan,plan);
    assert.equal(data.subject,subject);
    assert.equal(data.resolved,true);
    assert.equal(data.numerical.status,'CONSISTENT_NUMERICAL_CONVENTION');
    assert.equal(data.numerical.nativeProvenanceVerified,false);
    assert.equal(data.numerical.admissionRequested,false);
    assert.equal(data.numerical.scientificClosures,0);
    assert.deepEqual(data.outputHashes,data.numerical.outputSha256);
    assert.equal(data.outputHashes['batch.done.json'],context.batchMarkerSha256);
    assert.deepEqual(Object.keys(data.outputHashes).sort(),names);
    assert.deepEqual((await fs.readdir(outputs)).sort(),names);
    for (const name of names) {
      assert.equal(sha(await read(path.join(outputs,name),caps(name))),data.outputHashes[name],'Product changed: '+name);
    }
    assert.equal(sha(await read(receipt)),expected,'Comparison receipt changed during readback');
  }

  async function compare(context) {
    bound(context);
    const raw = await read(path.join(base,'verifica.py'));
    assert.equal(sha(raw),verifyPin,'Changed verification program');
    await exec(python,['-I','-B','-S','-c',raw.toString('utf8'),path.join(base,'protocollo.json'),
      'O:/BKL046-CFA-XDRZ-batch-due-depositi-v1',
      'O:/BKL046-CFA-XDRZ-controllo-due-depositi-v1/oracoli.zip',
      'O:/BKL046-CFA-XDRZ-testimone-larghezza-v1/testimone.zip',
      'O:/BKL046-CFA-XDRZ-scala-pesi-v1/classifica.py',
      packages,numeric,'--outputs',outputs,'--reservation',context.reservation,
      '--marker-sha256',context.batchMarkerSha256],{windowsHide:true,timeout:60000});
    const numericalRaw = await read(numeric);
    const numerical = JSON.parse(numericalRaw);
    assert.equal(numerical.schema,schema);
    assert.equal(numerical.planSha256,plan);
    assert.equal(numerical.evidence,'UNATTESTED_NUMERICAL_COMPARISON');
    assert.equal(numerical.status,'CONSISTENT_NUMERICAL_CONVENTION','Unresolved CFA comparison retained');
    const result = Buffer.from(JSON.stringify({reservation:context.reservation,operation,plan,subject,
        resolved:true,numericalSha256:sha(numericalRaw),outputHashes:numerical.outputSha256,numerical})+'\n');
    await fs.writeFile(receipt,result,{flag:'wx'});
    const receiptSha256=sha(result);
    await revalidate(context,receiptSha256);
    return {verified:true,reservation:context.reservation,batchMarkerSha256:context.batchMarkerSha256,receiptSha256};
  }
  return {compare,revalidate};
}
module.exports={verifierFor};
