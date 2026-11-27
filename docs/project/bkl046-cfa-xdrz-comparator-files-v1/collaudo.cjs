'use strict';
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs/promises');
const path = require('node:path');

const [candidate, controls, python, run, report] = process.argv.slice(2);
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
async function pinned(file, expected) {
  const raw = await fs.readFile(file);
  assert.equal(hash(raw), expected);
  return raw;
}
function json(bytes) {
  return JSON.parse(bytes.toString('utf8'));
}
const subjectSHA = '3ad86ab652dbe80b08fc6b939dd2b10fb3038563784598f08c10ada3a545b072';
const planSHA = '377aea9a4decbf470a95c92f7f85852bc59f5e056b76a8c7ae110e842fcfd6e7';
const manifestSHA = '6fd2da645650a19f4654276607612c0af5ba193734a0087fc221058aab4fe16b';
const verifierSHA = 'c04623fb80badca0db83917c237a9d7fef5041d0fd9b6a6a371f86cf8397c54f';
const reservation = 'e8e2314a-b079-4d9c-af5e-1516b6207595';
const names = ['integer-unmasked', 'integer-green-mask', 'integer-wrong-channel', 'shear-center0', 'shear-edge05'];
const options = {enableCFA:true,scale:1,dropShrink:.70,useLUT:false,enableImageWeighting:false,
  enableSurfaceSplines:false,enableLocalNormalization:false,enableAdaptiveNormalization:false,
  truncateOnOutOfRange:false,closePreviousImages:false,showImages:false,onError:0,cfaPattern:0,kernelFunction:1};
const createOnly = {flag:'wx'};

async function main() {
  const subject = json(await pinned(path.join(candidate,'launcher-subject.json'), subjectSHA));
  const comparatorPath=path.join(candidate,'comparator.cjs');
  await pinned(comparatorPath,subject.memberSha256['comparator.cjs']);
  await pinned(process.execPath,subject.nodeSha256);
  await pinned(python,subject.pythonSha256);
  const {verifierFor}=require(comparatorPath);
  const plan=json(await pinned(path.join(controls,'piano-controllo.json'),planSHA));
  const fixtures=path.resolve(controls,'fixture');
  const manifest=json(await pinned(path.join(fixtures,'manifest.json'),manifestSHA));
  const expected=new Map();
  for (const scene of ['unmasked','detector','reference','wrong-channel','shear']) {
    expected.set(scene,{});
    for (const type of ['rgb','weight']) {
      const filename=scene+'-expected-'+type+'.fits';
      expected.get(scene)[type]=await pinned(path.join(fixtures,filename),manifest.files[filename]);
    }
  }
  await fs.mkdir(run);
  const cases=[];
  async function prepare(id,mask='detector',shear='shear-edge05') {
    const state=path.join(run,id);
    const out=path.join(state,'outputs');
    await fs.mkdir(out,{recursive:true});
    const params=[], exports=[];
    for (const c of plan.cases) {
      const {id: label, files, enableRejection}=c;
      const scene=label==='integer-green-mask' ? mask :
        label.startsWith('shear-') ? label===shear ? 'shear' : 'unmasked' : c.expected[0];
      for (const kind of ['rgb','weight']) {
        await fs.writeFile(path.join(out,label+'-'+kind+'.fits'),expected.get(scene)[kind],createOnly);
      }
      params.push('DSG_CFA_PARAMETERS '+JSON.stringify({caseId:label,source:'synthetic fixture',
        settings:{...options,enableRejection,inputData:files.map(f=>[true,'O:/BKL046-CFA-XDRZ-tre-ingressi-v1/fixture/'+f,''])}}));
      exports.push('DSG_CFA_EXPORT '+JSON.stringify({caseId:label,intensity:label+'-rgb.fits',weights:label+'-weight.fits'}));
    }
    const marker=Buffer.from(JSON.stringify({schema:'BKL046_CFA_XDRZ_BATCH_OUTPUT_MARKER_V1',
      scope:'OUTPUT_MARKER_NOT_ADMISSION',operation:subject.operation,planSha256:planSHA,
      subjectSha256:subject.syntheticSubjectSha256,reservation,cases:names}));
    const context={reservation,operation:subject.operation,plan:planSHA,
      subject:subject.syntheticSubjectSha256,batchMarkerSha256:hash(marker)};
    const markerPath=path.join(out,'batch.done.json');
    const eventPath=path.join(out,'events.txt');
    await fs.writeFile(eventPath,[...params,...exports].join('\n')+'\n',createOnly);
    await fs.writeFile(markerPath,marker,createOnly);
    return {state,out,eventPath,markerPath,context,params,exports,api:verifierFor(python,state,out)};
  }
  for (const [mask,shear] of [['detector','shear-edge05'],['reference','shear-center0']]) {
    const t=await prepare(mask,mask,shear);
    const result=await t.api.compare(t.context);
    assert.equal(result.verified,true);
    await t.api.revalidate(t.context,result.receiptSha256);
    const r=json(await fs.readFile(path.join(t.state,'comparison.json')));
    assert.equal(r.evidence.maskCoordinates,mask);
    assert.equal(r.evidence.shearAgreement,shear);
    cases.push({name:mask,accepted:true});
  }
  for (const [name,change,expectedFailure] of [
    ['missing-fits', t=>fs.unlink(path.join(t.out,'integer-unmasked-weight.fits')), /unexpected or missing FITS exports/],
    ['extra-fits', t=>fs.copyFile(path.join(t.out,'integer-unmasked-rgb.fits'),path.join(t.out,'extra.fits')), /unexpected or missing FITS exports/],
    ['duplicate-event', t=>fs.appendFile(t.eventPath,t.params[0]+'\n'), /repeated or unknown console event/],
    ['missing-event', t=>fs.writeFile(t.eventPath,[...t.params,...t.exports.slice(0,-1)].join('\n')+'\n'), /missing or unexpected control cases/],
    ['incorrect-fits-values', t=>fs.writeFile(path.join(t.out,'integer-green-mask-weight.fits'),expected.get('unmasked').weight), /unexpected native comparison/],
  ]) {
    const t=await prepare(name);
    await change(t);
    await assert.rejects(t.api.compare(t.context),
      e => e.message==='CFA comparator failed' && expectedFailure.test(e.cause?.stderr ?? ''));
    cases.push({name,accepted:false,phase:'initialComparison'});
  }
  for (const [name,change,expectedFailure] of [
    ['fits-changed', t=>fs.appendFile(path.join(t.out,'integer-unmasked-rgb.fits'),' '), /FITS output changed/],
    ['log-changed', t=>fs.appendFile(t.eventPath,'\n'), /event log changed/],
    ['marker-changed', t=>fs.appendFile(t.markerPath,' '), /batch marker changed/],
    ['receipt-changed', t=>fs.appendFile(path.join(t.state,'comparison.json'),' '), /comparison receipt changed/],
  ]) {
    const t=await prepare(name);
    const result=await t.api.compare(t.context);
    await change(t);
    await assert.rejects(t.api.revalidate(t.context,result.receiptSha256), expectedFailure);
    cases.push({name,accepted:false,phase:'readback'});
  }
  const result={schema:'BKL046_CFA_XDRZ_COMPARATOR_FILE_TEST_V1',subjectSHA,planSHA,manifestSHA,verifierSHA,
    comparatorSHA:subject.memberSha256['comparator.cjs'],cases,fixtureProvenance:'SYNTHETIC_STANDINS',
    scientificClosures:0,nativeExecutions:0,admissionRequested:false};
  await fs.writeFile(report,JSON.stringify(result,null,2)+'\n',createOnly);
  console.log(JSON.stringify(result));
}
main().catch(error=>{console.error(error);process.exitCode=1});
