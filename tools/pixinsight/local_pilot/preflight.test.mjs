import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import test from 'node:test';

const source = readFileSync(new URL('./preflight.jsh', import.meta.url), 'utf8');
const digest = 'a'.repeat(64);
function fixture() {
  const manifest = {schemaVersion:'1.0',jobId:'synthetic-p1',mode:'PREFLIGHT_ONLY',
    inputs:['R','G','B','L'].map(role=>({role,path:`/${role}.xisf`,sha256:digest,imageIndex:0,width:10,height:12}))};
  let fileMissing=false, changed=false, reads=0, opened=0;
  const image={width:10,height:12,numberOfNominalChannels:1,isColor:false,bitsPerSample:32,
    median:()=>0.01,MAD:()=>0.001};
  const context={CoreApplication:{versionMajor:1,versionMinor:9,versionRelease:5,versionBuild:1706},
    ImageWindow:{windows:[],open:()=>{opened++;return [{mainView:{image,historyIndex:0},isModified:false},
      {mainView:{image:{...image,width:30,height:40}},isModified:false}];}},
    File:{exists:()=>!fileMissing,readFile:()=>++reads},
    CryptographicHash:class {hash(){return {toHex:()=>changed&&reads>1?'b'.repeat(64):digest};}}};
  const names=['AutomaticBackgroundExtractor','ChannelCombination','BackgroundNeutralization','ColorCalibration',
    'BlurXTerminator','NoiseXTerminator','StarXTerminator','MaskedStretch','LocalHistogramEqualization',
    'LRGBCombination','CurvesTransformation','PixelMath'];
  for (const name of names) context[name]=function(){};
  vm.createContext(context);vm.runInContext(source,context);
  return {manifest,context,image,run:()=>context.DSGPilotPreflight(manifest),opened:()=>opened,
    missing:()=>{fileMissing=true;},change:()=>{changed=true;}};
}
test('explicit first image of a multi-image container is inspected without processing',()=>{
  const f=fixture(),r=f.run();assert.equal(r.status,'PREFLIGHT_PASSED');
  assert.equal(r.inputs.length,4);assert.equal(r.inputs[0].containerImageCount,2);
  assert.equal(r.processingExecuted,false);assert.equal(r.providerRequests,0);
  assert.ok(r.inputs.every(i=>i.modified===false));
});
for (const [name,mutate,expected] of [
  ['processing mode',f=>f.manifest.mode='PROCESS','Processing is not enabled'],
  ['schema',f=>f.manifest.schemaVersion='2','Unsupported manifest'],
  ['job identity',f=>f.manifest.jobId='../job','Invalid job identity'],
  ['missing master',f=>f.missing(),'Missing selected master'],
  ['changed source digest',f=>f.manifest.inputs[0].sha256='b'.repeat(64),'Source digest mismatch'],
  ['missing image selection',f=>delete f.manifest.inputs[0].imageIndex,'Explicit XISF image index required'],
  ['wrong selected image',f=>f.manifest.inputs[0].imageIndex=1,'Selected image dimensions mismatch'],
  ['different dimensions',f=>f.manifest.inputs[1].width=11,'Selected image dimensions mismatch'],
  ['wrong channel role',f=>f.manifest.inputs[0].role='B','Role order must be R,G,B,L'],
  ['colour master',f=>f.image.isColor=true,'Monochrome master required'],
  ['module unavailable',f=>delete f.context.BlurXTerminator,'Required module missing'],
  ['source changes during read',f=>f.change(),'Source changed during inspection']
]) test(`rejects ${name}`,()=>{const f=fixture();mutate(f);assert.throws(f.run,new RegExp(expected));});
