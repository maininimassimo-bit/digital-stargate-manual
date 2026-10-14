import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import vm from 'node:vm';
const scripts=['scientific-covariance','scientific-test-plan-review','scientific-astrometry-context','scientific-multi-epoch','scientific-case-dossier','scientific-controlled-recovery','scientific-case-workspace'];
function load(ctx){for(const s of scripts)vm.runInContext(readFileSync('docs/javascripts/'+s+'.js','utf8'),ctx);return ctx.DSGCaseWorkspace.inspect;}
const inspect=load(vm.createContext({}));
const r=spawnSync('python',['-c',[
 'import json','from tools.scientific_transients.test_case_workspace import WorkspaceTests',
 'f=WorkspaceTests();f.setUp()','try: print(json.dumps(f.export()))','finally: f.doCleanups()'
].join('\n')],{encoding:'utf8',env:{...process.env,PYTHONDONTWRITEBYTECODE:'1'}});
assert.equal(r.status,0,r.stderr);const original=JSON.parse(r.stdout);
test('actual Python assembly accepted without scientific promotion',()=>{const s=inspect(original);assert.equal(s.attempts,3);assert.equal(s.qualified,0);assert.equal(s.technicalComplete,true);});
for(const [name,change] of [
 ['case mismatch',v=>v.caseRef='f'.repeat(32)],['plan head mismatch',v=>v.dossier.planHeadSha256='a'.repeat(64)],
 ['comparison case mismatch',v=>v.comparison.caseRef='f'.repeat(32)],['comparison removed',v=>v.comparison=null],
 ['historical dossier',v=>v.dossier.planStatus='HISTORICAL_PLAN_REVISION'],['changed package',v=>v.dossier.packageStatus='RETAINED_PACKAGE_UNAVAILABLE_OR_CHANGED'],
 ['invented scientific acceptance',v=>v.scientificAcceptance=true],['invented qualification',v=>v.qualifiedControls=59],
 ['private field',v=>v.privatePath='secret'],['unlabelled context',v=>v.contextualRecovery={}]
])test(name+' rejected',()=>{const v=structuredClone(original);change(v);assert.throws(()=>inspect(v));});
test('actual contextual V2 workspace integration when explicitly supplied', {skip:!process.env.DSG_CASE_WORKSPACE},()=>{
 const v=JSON.parse(readFileSync(process.env.DSG_CASE_WORKSPACE,'utf8')),s=inspect(v);assert.equal(s.context.injections,16);assert.equal(s.context.recovered,1);assert.equal(s.qualified,0);
});
test('actual real-input unexecuted workspace stays incomplete', {skip:!process.env.DSG_UNEXECUTED_WORKSPACE},()=>{
 const v=JSON.parse(readFileSync(process.env.DSG_UNEXECUTED_WORKSPACE,'utf8')),s=inspect(v);
 assert.equal(s.attempts,0);assert.equal(s.technicalComplete,false);assert.equal(s.context,null);assert.equal(s.qualified,0);
 assert.equal(v.plan.cases.length,1);assert.equal(v.dossier.decisions.length,0);
});
function ui(){
 const node=()=>({textContent:'',children:[],append(...items){this.children.push(...items);},replaceChildren(){this.children=[];}});
 let listener;const input={files:[],value:'',addEventListener(type,fn){listener=fn;}},status=node(),out=node();
 const root={dataset:{},isConnected:true,querySelector(selector){return selector==='input'?input:selector==='[role="status"]'?status:out;}};
 // Other panel initialisers see no root in this isolated UI fixture.
 const ctx=vm.createContext({});load(ctx);
 ctx.document={readyState:'complete',querySelector:()=>root,createElement:node};
 vm.runInContext(readFileSync('docs/javascripts/scientific-case-workspace.js','utf8'),ctx);
 return {out,status,root,change(file){input.files=file?[file]:[];return listener();}};
}
const file=()=>({size:100,text:async()=>JSON.stringify(original)});
test('bad replacement clears previous workspace',async()=>{const u=ui();await u.change(file());assert.equal(u.out.children.length,3);await u.change({size:1,text:async()=>'{'});assert.equal(u.out.children.length,0);});
test('oversize import is not read',async()=>{const u=ui();await u.change({size:1048577,text(){assert.fail('read');}});assert.equal(u.out.children.length,0);});
test('late older import cannot replace current workspace',async()=>{const u=ui();let release;const pending=u.change({size:1,text:()=>new Promise(r=>release=r)});await u.change(file());release('{');await pending;assert.equal(u.out.children.length,3);});
test('disconnected panel cannot render pending workspace',async()=>{const u=ui();let release;const pending=u.change({size:1,text:()=>new Promise(r=>release=r)});u.root.isConnected=false;release(JSON.stringify(original));await pending;assert.equal(u.out.children.length,0);});
