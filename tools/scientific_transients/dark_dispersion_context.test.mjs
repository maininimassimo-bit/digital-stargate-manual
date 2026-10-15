import test from 'node:test';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
const source=readFileSync('docs/javascripts/scientific-dark-dispersion.js','utf8');
const result=spawnSync('python',['-c',[
  'import json','from tools.scientific_transients.test_dark_dispersion_context import DarkContextTests',
  'f=DarkContextTests();f.setUp()','try: print(json.dumps(f.export()))','finally: f.doCleanups()'
].join('\n')],{encoding:'utf8',env:{...process.env,PYTHONDONTWRITEBYTECODE:'1'}});
assert.equal(result.status,0,result.stderr);const fixture=JSON.parse(result.stdout);
const scope=vm.createContext({});vm.runInContext(source,scope);const inspect=scope.DSGDarkDispersion.inspect;
test('actual Python minimised producer output accepted without scientific authority',()=>{
  const s=inspect(fixture);assert.equal(s.sources,50);assert.equal(s.maps,3);assert.equal(s.qualified,0);
});
test('private fields, fake uncertainty, independent/stable/master/LIGHT/execution promotions reject',()=>{
  for(const mutate of [v=>v.path='PRIVATE',v=>v.iidAttested=true,v=>v.lightAssociationAttested=true,
    v=>v.actualRejectedMasterVariance=0,v=>v.completeUncertainty=0,v=>v.significance=5,
    v=>v.qualifiedControls=59,v=>v.executionAuthorized=true,v=>v.scienceValidation='VALIDATED',
    v=>v.temporal2024to2026Stability='VALIDATED',v=>v.sources=true,v=>v.geometry=[2752,2160],
    v=>v.maps[0].privatePath='PRIVATE']){
    const v=structuredClone(fixture);mutate(v);assert.throws(()=>inspect(v));
  }
});
test('missing duplicated reordered wrong-unit and inconsistent maps reject',()=>{
  for(const mutate of [v=>v.maps.pop(),v=>v.maps.reverse(),v=>v.maps[1]=v.maps[0],
    v=>v.maps[1].sha256=v.maps[0].sha256,v=>v.maps[0].unit='ELECTRONS',v=>v.maps[1].unit='NATIVE_NORMALIZED_SAMPLE',
    v=>v.maps[2].mean*=2,v=>v.maps[1].minimum=-1,v=>v.maps[1].mean=NaN,v=>v.maps[1].maximum=Infinity,
    v=>v.maps[1].pixels=true,v=>v.maps[1].nativeReopenError=false,v=>v.maps[1].independentPixelError=1e-3,
    v=>v.maps[0].sha256='not-a-hash']){
    const v=structuredClone(fixture);mutate(v);assert.throws(()=>inspect(v));
  }
});
class Element{
  constructor(tag='div'){this.tag=tag;this.textContent='';this.children=[];this.value='';this.files=[];this.listeners=0;this.dataset={};this.isConnected=true;}
  append(node){this.children.push(node);}replaceChildren(){this.children=[];}
  addEventListener(type,handler){this[type]=handler;this.listeners++;}
}
function ui(){
  let current,subscribe,pagehide;const prohibited=()=>{throw Error('NETWORK_OR_STORAGE_FORBIDDEN');};
  const document={readyState:'complete',querySelector:()=>current?.root,createElement:tag=>new Element(tag)};
  const context=vm.createContext({document,TextEncoder,document$:{subscribe:f=>subscribe=f},window:{addEventListener:(n,f)=>pagehide=f},fetch:prohibited,localStorage:{setItem:prohibited},sessionStorage:{setItem:prohibited}});
  function mount(){const input=new Element('input'),status=new Element('p'),output=new Element();const root=new Element('section');
    root.querySelector=s=>s==='input[type="file"]'?input:s==='[role="status"]'?status:output;
    current={root,input,status,output};const text=JSON.stringify(fixture);input.files=[{size:Buffer.byteLength(text),text:async()=>text}];
    current.load=()=>input.change();return current;
  }
  mount();vm.runInContext(source,context);
  return {get current(){return current;},mount:()=>{const u=mount();subscribe();return u;},subscribe:()=>subscribe(),pagehide:()=>pagehide()};
}
test('renders three labelled local declarations and explicit missing uncertainty with no commands',async()=>{
  const h=ui(),u=h.current;await u.load();const text=JSON.stringify(u.output.children);
  assert.match(text,/50 dark del 2024/);assert.match(text,/master effettivo con rigetto sigma resta sconosciuta/);
  assert.match(text,/non rilegge originali o pixel/);assert.match(text,/Campione|campione normalizzato/);
  assert.equal(u.output.children.filter(x=>x.tag==='article').length,3);
  assert.equal(u.output.children.some(x=>['form','button','a'].includes(x.tag)),false);
});
test('missing invalid and changed files clear previously rendered evidence',async()=>{
  const u=ui().current;await u.load();assert.ok(u.output.children.length);u.input.files=[];await u.load();assert.equal(u.output.children.length,0);
  u.input.files=[{size:1,text:async()=>'{'}];await u.load();assert.match(u.status.textContent,/non valida/);assert.equal(u.output.children.length,0);
});
test('declared and actual UTF8 limits reject without stale success',async()=>{
  const u=ui().current;let reads=0;u.input.files=[{size:1048577,text:async()=>{reads++;return '{}';}}];await u.load();assert.equal(reads,0);
  u.input.files=[{size:1,text:async()=>'é'.repeat(524289)}];await u.load();assert.equal(u.output.children.length,0);assert.match(u.status.textContent,/non valida/);
});
test('late reads do not restore evidence after a later invalid selection',async()=>{
  const u=ui().current;let finish;u.input.files=[{size:100,text:()=>new Promise(r=>finish=r)}];const old=u.load();
  u.input.files=[{size:1,text:async()=>'{'}];await u.load();finish(JSON.stringify(fixture));await old;assert.equal(u.output.children.length,0);
});
test('navigation root replacement and pagehide clear declarations and do not duplicate listeners',async()=>{
  const h=ui(),old=h.current;let finish;old.input.files=[{size:100,text:()=>new Promise(r=>finish=r)}];const delayed=old.load();
  const current=h.mount();h.subscribe();assert.equal(current.input.listeners,1);finish(JSON.stringify(fixture));await delayed;assert.equal(old.output.children.length,0);
  await current.load();assert.equal(current.output.children.filter(x=>x.tag==='article').length,3);
  h.pagehide();assert.equal(current.output.children.length,0);assert.equal(current.input.value,'');
});
