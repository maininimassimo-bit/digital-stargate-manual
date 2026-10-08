import test from 'node:test';import assert from 'node:assert/strict';
import {inspectEpochPosition as inspect} from './epoch.mjs';
const fixture=()=>({raDeg:7.606083572,decDeg:11.79044105,parallaxMas:125,pmRaCosDecMasYr:300,pmDecMasYr:-428.8,radialVelocityKmS:52.51,fromJulianYear:2016,toJulianYear:1992.25,timeScale:'TCB'});
const close=(a,b)=>assert.ok(Math.abs(a-b)<1e-10,`${a} != ${b}`);
test('public IVOA six-dimensional known answer agrees without matching acceptance',()=>{
  const r=inspect(fixture());close(r.raDeg,7.6040614046279735);close(r.decDeg,11.793270382827929);
  assert.equal(r.covariance,null);assert.equal(r.matchClassification,'NOT_EVALUATED');assert.equal(r.scientificComparison,'NOT_VALIDATED');
});
test('same epoch is identity with large proper motion close to pole',()=>{
  const f={...fixture(),raDeg:359.999,decDeg:89.999,pmRaCosDecMasYr:10000,pmDecMasYr:-10000,toJulianYear:2016};
  const r=inspect(f);close(r.raDeg,f.raDeg);close(r.decDeg,f.decDeg);
});
test('longitude wrap and cos-declination convention at equator',()=>{
  const f={...fixture(),raDeg:359.999,decDeg:0,pmRaCosDecMasYr:3600000,pmDecMasYr:0,radialVelocityKmS:0,toJulianYear:2017};
  const r=inspect(f);close(r.raDeg,359.999+Math.atan(Math.PI/180)*180/Math.PI-360);close(r.decDeg,0);
});
test('no division by cos declination at north or south pole',()=>{
  for(const dec of [-90,90]) {const f={...fixture(),decDeg:dec,toJulianYear:2017};const r=inspect(f);assert.ok(Number.isFinite(r.raDeg)&&Number.isFinite(r.decDeg));assert.ok(Math.abs(r.decDeg)<=90);}
});
test('unknown motion, distance or epoch never becomes zero',()=>{
  for(const k of Object.keys(fixture()).filter(k=>k!=='timeScale')) {const f=fixture();f[k]=null;const r=inspect(f);assert.equal(r.status,'INCOMPLETE');assert.equal(r.raDeg,null);}
  for(const p of [0,-1])assert.equal(inspect({...fixture(),parallaxMas:p}).status,'INCOMPLETE');
});
test('TCB years cannot be relabeled UTC; closed schema and finite values enforced',()=>{
  for(const change of [{timeScale:'UTC'},{raDeg:360},{decDeg:91},{toJulianYear:Infinity},{ownerApproved:true},{radius:1}])assert.throws(()=>inspect({...fixture(),...change}),/INVALID_EPOCH_POSITION/);
});
test('motion perspective affects result; stationary direction retained under radial motion',()=>{
  const f={...fixture(),pmRaCosDecMasYr:0,pmDecMasYr:0};const r=inspect(f);close(r.raDeg,f.raDeg);close(r.decDeg,f.decDeg);
  assert.notEqual(inspect(fixture()).raDeg,inspect({...fixture(),radialVelocityKmS:0}).raDeg);
});
