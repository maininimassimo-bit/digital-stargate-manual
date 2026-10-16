import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import test from 'node:test';
import assert from 'node:assert/strict';
const source=readFileSync(new URL('./native_linear_uncertainty.jsh',import.meta.url),'utf8');
const context=vm.createContext({});vm.runInContext(source,context);
const kernel=context.DSGNativeLinearUncertainty;
const H='a'.repeat(64), G='b'.repeat(64);
const components=['PHOTON_READ_DIGITIZATION','DARK_MASTER_AND_TEMPORAL','FLAT_GAIN_NORMALIZATION','CALIBRATION',
 'SKY_BACKGROUND_ESTIMATOR','RESAMPLING_REGISTRATION','QUANTIZATION','REFERENCE_PSF_APERTURE_SELECTION'];
// Every array below is invented numeric data, never astronomical pixels or a mask.
function fixture(A=[[2,0],[0,2]],x=[10,3],a=[1,0],b=[0,1]) {
 const refs=Array.from({length:A[0].length},(_,i)=>'synthetic-latent-'+i);
 return {protocol:'DSG_NATIVE_LINEAR_UNCERTAINTY_V1',identity:{imageSha256:H,gridSha256:H,maskSha256:H,
  normalizationSha256:H,weightSha256:H,modelSha256:H,factorSourceSha256:H,epochRef:'synthetic-epoch',
  unit:'NORMALIZED_SAMPLE',coordinateConvention:'PI_NATIVE_GEOMETRIC_ROW_MAJOR'},
 grid:{width:x.length,height:1,channels:1,channel:0},pixelIndices:x.map((_,i)=>i),samples:x,aperture:a,background:b,
 basis:{sha256:H,whiteningEvidenceSha256:H,latentRefs:refs},
 factors:refs.map((latentRef,j)=>{const rows=A.flatMap((r,i)=>r[j]===0?[]:[i]);
  return {latentRef,rows,responses:rows.map(i=>A[i][j]),structuralZeroEvidenceSha256:rows.length?null:H};}),
 budget:components.map(component=>({component,state:'MISSING',evidenceSha256:null,domainSha256:null}))};
}
function result(m){return kernel.inspect(m);}
function close(a,b,tol=1e-13){assert(Math.abs(a-b)<=tol*Math.max(1,Math.abs(b)),`${a} != ${b}`);}
test('exact independently rational-derived dense covariance answers',()=>{
 const cases=[
  [fixture(),7,8,[2,-2]],
  [fixture([[2],[2]]),7,0,[0]],
  [fixture([[2],[-2]]),7,16,[4]],
  [fixture([[2,1,0],[3,0,1],[1,-1,2],[2,1,-1]],[12,8,2,4],[.5,1,0,0],[0,0,.25,.75]),35/4,123/32,[11/8,-1/4,11/8]]];
 for(const [m,F,V,u] of cases){const r=result(m);close(r.observedFiniteApertureFlux,F);close(r.varianceUnderSuppliedJointModel,V);
  assert.deepEqual([...r.latentResponses],u);assert.equal(r.fullPhysicalVariance,null);assert.equal(r.significance,null);
  assert.equal(r.qualifiedControls,0);assert.equal(r.scientificValidation,'NOT_VALIDATED');}
});
test('dense oracle agrees for deterministic signed synthetic sparse factors',()=>{
 for(let k=1;k<=20;k++){
  const A=Array.from({length:4},(_,i)=>Array.from({length:3},(_,j)=>((k*(i+1)+(j+1)*3)%11-5)/4));
  const m=fixture(A,[12,8,2,4],[.5,1,0,0],[0,0,.25,.75]),w=[.5,1,-.375,-1.125];
  const C=A.map(r=>A.map(s=>r.reduce((v,p,j)=>v+p*s[j],0)));
  const V=w.reduce((s,p,i)=>s+w.reduce((t,q,j)=>t+p*C[i][j]*q,0),0);
  close(result(m).varianceUnderSuppliedJointModel,V);
 }
});
test('signed scaling obeys flux and variance transformations',()=>{
 for(const scale of [-8,.125,2.5]){
  const m=fixture();m.samples=m.samples.map(v=>v*scale);m.factors.forEach(f=>{f.responses=f.responses.map(v=>v*scale);});
  const r=result(m);close(r.observedFiniteApertureFlux,7*scale);close(r.varianceUnderSuppliedJointModel,8*scale*scale);
 }
});
test('constant offset cancels and compensated flux preserves a small residual',()=>{
 const c=fixture([[1],[1],[1],[1]],[1e16,1,-1e16,0],[1,1,1,0],[0,0,0,1]);
 assert.equal(result(c).observedFiniteApertureFlux,1);
 const d=fixture();d.samples=d.samples.map(v=>v+128);assert.equal(result(d).observedFiniteApertureFlux,7);
});
test('ARB exact dyadic counterexample retains product-roundoff residual',()=>{
 const samples=[2**53,1,3002399751580331.5];
 const m=fixture(samples.map(v=>[v]),samples,[.5,1,0],[0,0,1]);
 const r=result(m);assert.equal(r.observedFiniteApertureFlux,-.25);
 assert.equal(r.latentResponses[0],-.25);assert.equal(r.varianceUnderSuppliedJointModel,.0625);
 assert.equal(r.significance,null);
});
test('several levels of cancellation retain a unit residual',()=>{
 const samples=[1e100,1e50,1,-1e100,-1e50,0];
 const m=fixture(samples.map(()=>[1]),samples,[1,1,1,1,1,0],[0,0,0,0,0,1]);
 assert.equal(result(m).observedFiniteApertureFlux,1);
});
test('ARB subnormal low-product counterexample is rejected, never converted to zero',()=>{
 const v=[2*2**-1022,2**-1022,6004799503160661*2**-1074];
 const m=fixture(v.map(x=>[x]),[10,3,1],[.5,1,0],[0,0,1]);
 // Exact response 2^-1075 and variance 2^-2150 are not representable in Float64.
 assert.throws(()=>result(m),/UNDERFLOW|SUBNORMAL/);
});
test('cross-epoch signed covariance and shared-mode difference',()=>{
 const l=fixture([[2,-1],[0,0]]),r=fixture([[-3,4],[0,0]]);
 const c=kernel.compare(l,r);assert.equal(c.covarianceUnderSuppliedJointModel,-10);
 close(c.differenceVarianceUnderSuppliedJointModel,50);
 assert.equal(kernel.compare(l,l).differenceVarianceUnderSuppliedJointModel,0);
 assert.equal(c.significance,null);
});
test('global ordered basis, normalization and units are mandatory across epochs',()=>{
 for(const change of [m=>m.basis.sha256=G,m=>m.basis.whiteningEvidenceSha256=G,
  m=>m.identity.normalizationSha256=G,m=>m.identity.unit='ADU',m=>{m.basis.latentRefs.reverse();m.factors.reverse();}]){
  const r=fixture();change(r);assert.throws(()=>kernel.compare(fixture(),r),/CROSS_/);
 }
});
test('unknown physical terms and claimed represented terms never gain physical acceptance',()=>{
 const m=fixture();m.budget.forEach(b=>{b.state='REPRESENTED_JOINTLY';b.evidenceSha256=H;b.domainSha256=H;});
 const r=result(m);assert.equal(r.fullPhysicalVariance,null);assert.equal(r.provenanceVerified,false);
 assert.equal(r.physicalApplicabilityVerified,false);assert.equal(r.qualifiedControls,0);
});
test('strict structure, finite values, geometry, masks and exact support fail closed',()=>{
 for(const change of [m=>m.extra=true,m=>m.identity.extra=true,m=>m.identity.maskSha256=null,
  m=>m.identity.unit='UNKNOWN',m=>m.grid.channel=1,m=>m.grid.width=100000001,m=>m.samples[0]=NaN,
  m=>m.samples[0]=Infinity,m=>m.aperture[0]=-.1,m=>m.aperture[0]=2,m=>m.background[0]=.1,
  m=>m.background[1]=.5,m=>m.aperture=[0,0],m=>m.pixelIndices=[1,0],m=>m.pixelIndices=[0,0],
  m=>m.pixelIndices=[0,2],m=>m.samples.pop(),m=>m.aperture=[0,0],m=>m.background=[0,0]]){
  const m=fixture();change(m);assert.throws(()=>result(m),/LINEAR_/);
 }
 const z=fixture([[1],[1],[1]],[1,2,3],[1,0,0],[0,1,0]);assert.throws(()=>result(z),/WEIGHTS/);
});
test('all factor axes, sparse rows and structural-zero evidence are compulsory',()=>{
 for(const change of [m=>m.factors.pop(),m=>m.factors.reverse(),m=>m.basis.latentRefs[1]=m.basis.latentRefs[0],
  m=>m.factors[0].rows=[1,0],m=>m.factors[0].rows=[0,0],m=>m.factors[0].rows=[2],
  m=>m.factors[0].responses=[0],m=>m.factors[0].responses=[NaN],m=>m.factors[0].responses=[],
  m=>m.factors[0].structuralZeroEvidenceSha256=H,
  m=>{m.factors[0].rows=[];m.factors[0].responses=[];m.factors[0].structuralZeroEvidenceSha256=null;}]){
  const m=fixture();change(m);assert.throws(()=>result(m),/LINEAR_/);
 }
 const z=fixture([[0],[0]]);assert.equal(result(z).varianceUnderSuppliedJointModel,0);
});
test('physical inventory cannot omit, duplicate or silently exclude a contribution',()=>{
 for(const change of [m=>m.budget.pop(),m=>m.budget.reverse(),m=>m.budget[0].state='NEGLIGIBLE',
  m=>m.budget[0].evidenceSha256=H,m=>m.budget[0].state='EXCLUDED_WITH_DOMAIN_EVIDENCE']){
  const m=fixture();change(m);assert.throws(()=>result(m),/BUDGET/);
 }
});
test('overflow and nonzero products lost to underflow raise explicit errors',()=>{
 for(const value of [Number.MAX_VALUE,Number.MIN_VALUE]){
  const m=fixture([[value],[0]]);assert.throws(()=>result(m),/OVERFLOW|UNDERFLOW|SUBNORMAL/);
 }
 const m=fixture([[1],[1]],[1,1],[Number.MIN_VALUE,0],[0,1]);
 m.factors[0].responses=[.5,.5];assert.throws(()=>result(m),/UNDERFLOW/);
 const c=fixture([[1e200,1e-200],[0,0]]);assert.throws(()=>result(c),/UNDERFLOW|OVERFLOW/);
});
test('bounds reject instead of truncating',()=>{
 const m=fixture();m.pixelIndices=Array(16385).fill(0);assert.throws(()=>result(m),/SUPPORT/);
 const l=fixture();l.basis.latentRefs=Array(16385).fill('x');assert.throws(()=>result(l),/BASIS/);
 // 65*16384 responses exceed the aggregate bound while each sparse factor is legal.
 const n=16384,Arow=Array.from({length:n},(_,i)=>i),b=Array(n).fill(0);b[n-1]=1;
 const a=Array(n).fill(1);a[n-1]=0;
 const v=fixture([[1],[1]]);v.grid.width=n;v.pixelIndices=Arow;v.samples=Array(n).fill(1);v.aperture=a;v.background=b;
 v.basis.latentRefs=Array.from({length:65},(_,i)=>'axis-'+i);
 v.factors=v.basis.latentRefs.map(latentRef=>({latentRef,rows:Arow,responses:Array(n).fill(1),structuralZeroEvidenceSha256:null}));
 assert.throws(()=>result(v),/RESPONSE_BOUND/);
});
test('inputs are preserved and result vectors cannot alter later computations',()=>{
 const m=fixture(),before=JSON.stringify(m),r=result(m);r.latentRefs[0]='changed';r.latentResponses[0]=900;
 assert.equal(JSON.stringify(m),before);assert.equal(result(m).latentRefs[0],'synthetic-latent-0');
 assert.equal(kernel.compare(m,m).differenceVarianceUnderSuppliedJointModel,0);
});
function freezeData(v) {
 if(v&&typeof v==='object'){
  for(const key of Object.keys(v)){const d=Object.getOwnPropertyDescriptor(v,key);if('value' in d)freezeData(d.value);}
  Object.freeze(v);
 }
 return v;
}
function engineData(v) {
 context.dsgSyntheticJSON=JSON.stringify(v);
 const parsed=vm.runInContext('JSON.parse(dsgSyntheticJSON)',context);
 delete context.dsgSyntheticJSON;return parsed;
}
function frozenFixture(v){return freezeData(engineData(v));}
test('trusted budget protocol preserves every computational output',()=>{
 assert.equal(kernel.budgetMonitorProtocol,'DSG_NATIVE_LINEAR_TRUSTED_BUDGET_V1');
 for(const original of [fixture(),fixture([[2],[2]]),fixture([[2],[-2]])]){
  const m=engineData(original);
  const before=JSON.stringify(result(m));freezeData(m);let calls=0;
  assert.equal(JSON.stringify(kernel.inspect(m,()=>{calls++;})),before);assert(calls>=3);
  const expected=JSON.stringify(kernel.compare(m,m));
  assert.equal(JSON.stringify(kernel.compare(m,m,()=>{calls++;})),expected);
 }
});
test('monitored computation requires complete frozen passive input and rejects accessors',()=>{
 let calls=0;assert.throws(()=>kernel.inspect(fixture(),()=>{calls++;}),/IMMUTABLE_REQUIRED/);assert.equal(calls,0);
 const partial=engineData(fixture());Object.freeze(partial);assert.throws(()=>kernel.inspect(partial,()=>{}),/IMMUTABLE_REQUIRED/);
 const active=engineData(fixture());Object.defineProperty(active,'samples',{enumerable:true,get(){throw Error('EXECUTED');}});freezeData(active);
 assert.throws(()=>kernel.inspect(active,()=>{}),/IMMUTABLE_ACCESSOR_OR_INDEX/);
 for(const monitor of [{},'cancel',true,0])assert.throws(()=>kernel.inspect(fixture(),monitor),/BUDGET_MONITOR/);
 assert.throws(()=>kernel.compare(frozenFixture(fixture()),fixture(),()=>{}),/IMMUTABLE_REQUIRED/);
});
test('monitor cancellation never returns a partial measurement',()=>{
 const m=frozenFixture(fixture());assert.throws(()=>kernel.inspect(m,()=>{throw Error('CANCELLED');}),/CANCELLED/);
 assert.throws(()=>kernel.compare(m,m,()=>{throw Error('DEADLINE');}),/DEADLINE/);
 close(result(m).varianceUnderSuppliedJointModel,8);
});
test('long source support and factor loops keep checking the monitor',()=>{
 const n=8192,a=Array(n).fill(1),b=Array(n).fill(0);a[n-1]=0;b[n-1]=1;
 const m=frozenFixture(fixture(Array.from({length:n},()=>[1]),Array(n).fill(2),a,b));
 let calls=0;const r=kernel.inspect(m,()=>{calls++;});assert(calls>20);assert.equal(r.observedFiniteApertureFlux,0);
 let reached=0;assert.throws(()=>kernel.inspect(m,()=>{if(++reached===20)throw Error('STOP_LONG_LOOP');}),/STOP_LONG_LOOP/);
 assert.equal(reached,20);
});
test('reentrant monitoring has no shared budget state or mutable model window',()=>{
 const m=frozenFixture(fixture());let first=true,inner;
 const r=kernel.inspect(m,()=>{
  assert.throws(()=>{m.samples[0]=999;},TypeError);
  if(first){first=false;inner=result(fixture([[2],[-2]]));}
 });
 assert.equal(r.observedFiniteApertureFlux,7);assert.equal(inner.varianceUnderSuppliedJointModel,16);
 assert.equal(m.samples[0],10);
});
test('ARB inherited sample getter and a hole disguised by an extra property are rejected',()=>{
 const m=engineData(fixture());let captured=10,getterCalls=0,monitorCalls=0;
 const sparse=engineData([null,3]);delete sparse[0];sparse.extra=0;
 const custom=Object.create(Object.getPrototypeOf(sparse));
 Object.defineProperty(custom,'0',{get(){getterCalls++;return captured;}});
 Object.setPrototypeOf(sparse,custom);m.samples=sparse;freezeData(m);
 assert.throws(()=>kernel.inspect(m,()=>{monitorCalls++;captured=999;}),/IMMUTABLE_PROTOTYPE/);
 assert.equal(getterCalls,0);assert.equal(monitorCalls,0);
 const plain=engineData(fixture());delete plain.samples[0];plain.samples.extra=0;freezeData(plain);
 assert.throws(()=>kernel.inspect(plain,()=>{}),/IMMUTABLE_ACCESSOR_OR_INDEX/);
});
test('hidden additions, symbols and foreign prototypes are rejected by monitored mode',()=>{
 const hidden=engineData(fixture());Object.defineProperty(hidden.samples,'hidden',{value:1});freezeData(hidden);
 assert.throws(()=>kernel.inspect(hidden,()=>{}),/IMMUTABLE_FIELDS/);
 const symbol=engineData(fixture());symbol.samples[Symbol('hidden')]=1;freezeData(symbol);
 assert.throws(()=>kernel.inspect(symbol,()=>{}),/IMMUTABLE_SYMBOL/);
 assert.throws(()=>kernel.inspect(freezeData(fixture()),()=>{}),/IMMUTABLE_PROTOTYPE/);
});
