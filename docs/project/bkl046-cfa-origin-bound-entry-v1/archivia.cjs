'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs/promises');
const path=require('node:path');
const {createHash}=require('node:crypto');

const sha=bytes=>createHash('sha256').update(bytes).digest('hex');
const uuid=/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;
const labels=['zero-origin0','zero-origin05','half-origin0','half-origin05'];
const fits=labels.flatMap(c=>['rgb','weight'].map(k=>c+'-'+k+'.fits')).sort();

async function create(file,bytes){
  const handle=await fs.open(file,'wx');
  try{
    await handle.writeFile(bytes);
    await handle.sync();
  }finally{
    await handle.close();
  }
}
async function plain(pathname){
  const info=await fs.lstat(pathname);
  assert(info.isFile()&&!info.isSymbolicLink(),'nonregular evidence file');
  return fs.readFile(pathname);
}
async function publish({root,run,acquired,original,receipt,receiptSha256,reservation,capturePin,closePin,entryFile,entryPin}){
  assert.match(reservation,uuid);
  const stats=await fs.lstat(root);
  assert(stats.isDirectory()&&!stats.isSymbolicLink());
  const acquiredRecord=JSON.parse(acquired);
  assert.equal(acquiredRecord.reservation,reservation);
  const receiptBytes=await plain(receipt);
  assert.equal(sha(receiptBytes),receiptSha256,'receipt changed');
  const result=JSON.parse(receiptBytes);
  assert.equal(result.reservation,reservation);
  assert.equal(result.operation,acquiredRecord.operation);
  assert.equal(result.classification.status,'MATCHED_TESTED_HYPOTHESIS');
  assert.equal(result.classification.hypotheses.length,1);
  assert.deepEqual(Object.keys(result.classification.outputSha256).sort(),fits);
  const files=[
    ['receipt.json',receiptBytes,receiptSha256],
    ['r4-acquired.json',acquired,sha(acquired)],
    ['r4-original.json',original,sha(original)],
  ];
  for(const [name,pin] of [['events.txt',result.eventsSha256],['batch.done.json',result.markerSha256]]){
    files.push([name,await plain(path.join(run,name)),pin]);
  }
  for(const name of fits){
    files.push([name,await plain(path.join(run,'outputs',name)),result.classification.outputSha256[name]]);
  }
  files.push(['window.bmp',await plain(path.join(run,'window.bmp')),capturePin]);
  files.push(['normal-close.json',await plain(path.join(run,'normal-close.json')),closePin]);
  files.push(['batch-entry.js',await plain(entryFile),entryPin]);
  assert.equal(files.length,16);
  for(const [name,bytes,pin] of files){
    assert.equal(sha(bytes),pin,'evidence changed: '+name);
  }
  const directory=path.join(root,reservation);
  await fs.mkdir(directory);
  const records=[];
  for(const [name,bytes,pin] of files){
    await create(path.join(directory,name),bytes);
    records.push({name,length:bytes.length,sha256:pin});
  }
  const marker=Buffer.from(JSON.stringify({schema:'BKL046_CFA_ORIGIN_ARCHIVE_V1',
    scope:'ARCHIVED_EVIDENCE_NOT_RELEASE',reservation,operation:result.operation,members:records})+'\n');
  const markerRecord={name:'ARCHIVED.json',length:marker.length,sha256:sha(marker)};
  const holdEntries=[...records,markerRecord];
  async function verify(includeMarker=true){
    const expected=includeMarker?holdEntries:records;
    const stat=await fs.lstat(directory);
    assert(stat.isDirectory()&&!stat.isSymbolicLink(),'archive directory differs');
    assert.deepEqual((await fs.readdir(directory)).sort(),expected.map(x=>x.name).sort(),'archive namespace differs');
    for(const {name,length,sha256} of expected){
      const bytes=await plain(path.join(directory,name));
      assert(bytes.length===length && sha(bytes)===sha256,'archive readback differs: '+name);
    }
  }
  await verify(false);
  await create(path.join(directory,markerRecord.name),marker);
  await verify();
  return {directory,holdEntries,verify};
}
module.exports={publish};
