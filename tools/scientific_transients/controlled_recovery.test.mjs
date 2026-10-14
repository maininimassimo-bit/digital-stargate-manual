import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
const ctx=vm.createContext({});
vm.runInContext(readFileSync('docs/javascripts/scientific-controlled-recovery.js','utf8'),ctx);
const inspect=ctx.DSGControlledRecovery.inspect;
// Self-contained synthetic contract fixture; integration is an explicit extra.
const path=process.env.DSG_RECOVERY_RECEIPT;
const digest='a'.repeat(64),ref=n=>n.toString(16).padStart(32,'0');
const original={schema:'BKL051_CONTROLLED_RECOVERY_RESULT_V1',origin:'SYNTHETIC_ADDITION_ON_REAL_M27_BACKGROUND',
 prelaunchSha256:digest,protocolSha256:digest,sourceSha256:digest,archiveSealSha256:digest,
 terminalSha256:{generator:digest,worker:digest},images:[1,2].map(n=>({imageRef:ref(n),imageSha256:digest,catalogSha256:digest,sources:20})),
 matchingRadiusPixels:3,gaussianSigmaPixels:2,sourceShotNoiseAdded:false,
 truthSeparation:'STRUCTURAL_WORKER_PAYLOAD_CHECK_ONLY_NOT_INDEPENDENT_BLIND_ATTESTATION',positionsPassedToDetector:false,
 scientificValidation:'NOT_VALIDATED',scientificAcceptance:false,archiveSealTiming:'POST_RUN_AFTER_INITIAL_SCORE_NOT_PRETRUTH_PROOF',
 badPixelQuality:'ALL_PIXELS_ADMITTED_NOT_SCIENTIFIC_BAD_PIXEL_VALIDATION',parameterPolicyAccepted:false,submissionAuthorized:false,completeDependencyArchive:false,
 rows:Array.from({length:16},(_,i)=>({targetRef:ref(i+10),groupRef:digest.slice(0,32),truthAddedFlux:.01,
 injectionStatus:'EVALUATED',recovered:i===11,baselineMatches:[],afterMatches:i===11?[7]:[],baselineProbeFlag:false,
 measuredAddedFlux:null,fullFluxVariance:null,significance:null})),
 injectionDenominator:16,recoveredInjections:1,evaluatedInjections:16,ambiguousInjections:0,missingInjections:0,
 baselineProbeDenominator:16,baselineProbesWithSources:0,independentTrialCount:null,qualifiedNullControls:0,falsePositiveConfidenceBound:null,
 measuredFluxBias:null,measuredFluxErrorRMS:null,status:'DIAGNOSTIC_POSITION_SCORING_ONLY'};
if(path)test('explicit retained native receipt integration',()=>{
 const actual=inspect(JSON.parse(readFileSync(path,'utf8')));assert.equal(actual.injections,16);assert.equal(actual.recovered,1);assert.equal(actual.qualified,0);
});
test('retained result keeps every insertion and no scientific promotion',()=>{
 const s=inspect(original);assert.equal(s.injections,16);assert.equal(s.recovered,1);assert.equal(s.qualified,0);assert.equal(s.independentTrials,null);
});
for(const [name,mutate] of [
 ['changed denominator',v=>v.injectionDenominator--],
 ['invented recovery',v=>v.recoveredInjections++],
 ['invented independence',v=>v.independentTrialCount=16],
 ['invented null qualification',v=>v.qualifiedNullControls=16],
 ['invented confidence bound',v=>v.falsePositiveConfidenceBound=.05],
 ['invented scientific acceptance',v=>v.scientificAcceptance=true],
 ['private coordinates',v=>v.rows[0].x=12],
 ['fabricated measured flux',v=>v.rows[0].measuredAddedFlux=.1],
 ['relabelled chronology',v=>v.archiveSealTiming='BEFORE_TRUTH'],
 ['duplicate identity',v=>v.rows[1].targetRef=v.rows[0].targetRef],
 ['inconsistent baseline ambiguity',v=>v.rows[0].baselineMatches=[1]],
 ['nonfinite radius',v=>v.matchingRadiusPixels=Infinity],
 ['unknown group',v=>v.rows[0].groupRef='f'.repeat(32)],
 ['invented Poisson model',v=>v.sourceShotNoiseAdded=true],
 ['incomplete provenance',v=>delete v.protocolSha256]
])test(name+' rejected',()=>{const v=structuredClone(original);mutate(v);assert.throws(()=>inspect(v));});
test('inspection does not mutate retained receipt',()=>{const before=JSON.stringify(original);inspect(original);assert.equal(JSON.stringify(original),before);});
function sharedReceipt(){
 const v=structuredClone(original),hit=v.rows.find(r=>r.recovered),other=v.rows.find(r=>!r.recovered);
 other.afterMatches=[...hit.afterMatches];other.recovered=true;v.recoveredInjections=2;return v;
}
test('one source claimed as two recoveries rejected',()=>assert.throws(()=>inspect(sharedReceipt())));
test('all shared-source associations explicitly ambiguous accepted',()=>{
 const v=sharedReceipt();for(const r of v.rows.filter(r=>r.recovered)){r.injectionStatus='AMBIGUOUS';r.recovered=null;}
 v.recoveredInjections=0;v.ambiguousInjections=2;v.evaluatedInjections=14;
 assert.equal(inspect(v).ambiguous,2);
});
test('partial shared-source ambiguity rejected',()=>{
 const v=sharedReceipt(),r=v.rows.find(r=>r.recovered);r.injectionStatus='AMBIGUOUS';r.recovered=null;
 v.recoveredInjections=1;v.ambiguousInjections=1;v.evaluatedInjections=15;assert.throws(()=>inspect(v));
});
function ui(){
 const node=()=>({textContent:'',children:[],append(...items){this.children.push(...items);},replaceChildren(){this.children=[];}});
 let listener;const input={files:[],value:'',addEventListener(type,fn){assert.equal(type,'change');listener=fn;}},status=node(),output=node();
 const root={dataset:{},isConnected:true,querySelector(selector){return selector==='input'?input:selector==='[role="status"]'?status:output;}};
 const document={readyState:'complete',querySelector(){return root;},createElement:node};
 vm.runInContext(readFileSync('docs/javascripts/scientific-controlled-recovery.js','utf8'),vm.createContext({document}));
 return {input,status,output,root,change(file){input.files=file?[file]:[];return listener();}};
}
const receipt=()=>({size:100,text:async()=>JSON.stringify(original)});
test('UI renders valid receipt and clears it on a malformed replacement',async()=>{
 const u=ui();await u.change(receipt());assert.equal(u.output.children.length,4);
 await u.change({size:10,text:async()=>'{'});assert.equal(u.output.children.length,0);assert.match(u.status.textContent,/non valida/);
});
test('UI refuses oversize file before reading its contents',async()=>{
 const u=ui();await u.change({size:1048577,text(){assert.fail('oversize read');}});assert.equal(u.output.children.length,0);
});
test('UI clears result when selection is cancelled',async()=>{
 const u=ui();await u.change(receipt());await u.change(null);assert.equal(u.output.children.length,0);
});
test('late earlier file cannot replace newer result',async()=>{
 const u=ui();let release;const first=u.change({size:10,text:()=>new Promise(resolve=>release=resolve)});
 await u.change(receipt());const rendered=u.output.children;release('{');await first;
 assert.equal(u.output.children,rendered);assert.equal(rendered.length,4);assert.match(u.status.textContent,/coerenti/);
});
test('disconnected panel cannot render a delayed import',async()=>{
 const u=ui();let release;const pending=u.change({size:10,text:()=>new Promise(resolve=>release=resolve)});
 u.root.isConnected=false;release(JSON.stringify(original));await pending;assert.equal(u.output.children.length,0);
});
