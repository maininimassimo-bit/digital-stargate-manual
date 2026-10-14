import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import '../../docs/javascripts/scientific-input-lineage.js';
const ref=n=>n.toString(16).padStart(32,'0');
const sample=()=>({schema:'BKL051_INPUT_LINEAGE_V1',scope:'RETAINED_METADATA_COPY_PILOT_ONLY',receiptSha256:'1'.repeat(64),manifestSha256:'2'.repeat(64),terminalSha256:'3'.repeat(64),candidateDraftSha256:'4'.repeat(64),candidatePlanRef:ref(1),
  inputs:[{inputRef:ref(2),filter:'Green',rawSha256:'5'.repeat(64),calibratedSha256:'6'.repeat(64),derivedSha256:'7'.repeat(64),byteIntegrity:'RECHECKED_LOCAL_FILES',metadataCopy:'NATIVE_RECEIPT_REPORTED',pixelEquality:'REPORTED_ZERO_DIFFERENCE_NOT_REMEASURED',sampleMembership:'OUTSIDE_CANDIDATE_MANIFEST'}],
  calibrationSemantics:'NOT_ATTESTED_BY_THIS_IMPORT',scienceValidation:'NOT_VALIDATED',completeUncertainty:null,significance:null,qualifiedControls:0,executionAuthorized:false});
test('lineage keeps distinct identities and excludes outside pilot from candidate count',()=>{const s=DSGInputLineage.inspect(sample());assert.equal(s.inputs,1);assert.equal(s.included,0);assert.equal(s.outside,1);assert.equal(s.qualified,0);});
test('cannot promote calibration, significance, uncertainty or execution authorization',()=>{for(const change of [v=>v.scienceValidation='VALIDATED',v=>v.calibrationSemantics='VALIDATED',v=>v.significance=5,v=>v.completeUncertainty=0,v=>v.qualifiedControls=1,v=>v.executionAuthorized=true]){const v=sample();change(v);assert.throws(()=>DSGInputLineage.inspect(v));}});
test('private fields, duplicate original and identical raw/derived identity rejected',()=>{for(const change of [v=>v.inputs[0].path='F:/private',v=>v.inputs.push({...v.inputs[0],inputRef:ref(3),derivedSha256:'8'.repeat(64)}),v=>v.inputs[0].derivedSha256=v.inputs[0].rawSha256]){const v=sample();change(v);assert.throws(()=>DSGInputLineage.inspect(v));}});
function ui(){
  class Element{constructor(tag){this.tag=tag;this.children=[];this.style={};this.textContent='';}append(...items){this.children.push(...items);}replaceChildren(){this.children=[];this.textContent='';}}
  const input={files:[],value:'file',addEventListener:(_,fn)=>input.change=fn},status=new Element('p'),output=new Element('div');
  const root={dataset:{},isConnected:true,querySelector:s=>s==='input'?input:s==='[role="status"]'?status:output};
  const document={readyState:'complete',querySelector:()=>root,createElement:t=>new Element(t)};
  vm.runInNewContext(readFileSync(new URL('../../docs/javascripts/scientific-input-lineage.js',import.meta.url),'utf8'),{document});return {input,status,output,root};
}
test('UI displays unknown significance and clears prior results on invalid input',async()=>{const u=ui();u.input.files=[{size:100,text:async()=>JSON.stringify(sample())}];await u.input.change();assert.equal(u.output.children.length,3);assert.match(u.output.children[0].textContent,/Fuori dal manifest: 1/);assert.match(u.status.textContent,/non rimisurata/);u.input.files=[{size:1,text:async()=>'{'}];await u.input.change();assert.equal(u.output.children.length,0);});
test('UI rejects over 1 MiB without reading',async()=>{const u=ui();let read=false;u.input.files=[{size:1048577,text:async()=>{read=true;return '{}';}}];await u.input.change();assert.equal(read,false);});
test('late lineage import cannot overwrite a later invalid import',async()=>{const u=ui();let resolve;u.input.files=[{size:100,text:()=>new Promise(r=>resolve=r)}];const old=u.input.change();u.input.files=[{size:1,text:async()=>'{'}];await u.input.change();resolve(JSON.stringify(sample()));await old;assert.equal(u.output.children.length,0);});
test('browser consumes receipt produced by byte-verifying Python adapter',()=>{const result=spawnSync('python',['-c',[
  'import json','from tools.scientific_transients.test_input_lineage import LineageTests','t=LineageTests();t.setUp()',
  'try: print(json.dumps(t.inspect()))','finally: t.doCleanups()',
].join('\n')],{encoding:'utf8',env:{...process.env,PYTHONDONTWRITEBYTECODE:'1'}});assert.equal(result.status,0,result.stderr);const v=JSON.parse(result.stdout);assert.equal(DSGInputLineage.inspect(v).included,1);assert.equal(v.executionAuthorized,false);});
