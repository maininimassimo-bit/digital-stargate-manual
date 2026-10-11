import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import test from 'node:test';
import assert from 'node:assert/strict';
const code=readFileSync(new URL('./measurements.jsh',import.meta.url),'utf8');
function fixture({failNoise=false,empty=false}={}) {
  let selected={area:4096}, pushes=0,pops=0;
  const image={width:64,height:64,numberOfNominalChannels:1,
    pushSelections(){++pushes;},popSelections(){++pops;},resetSelections(){},
    set selectedRect(v){selected=v;},get selectedRect(){return selected;},
    noiseMRS(n){if(failNoise)throw Error('Native failure');return [.001,n*10];}};
  class Rect {constructor(x0,y0,x1,y1){this.area=(x1-x0)*(y1-y0);}}
  class StarDetector {stars(){return empty?[]:[
    {pos:{x:10,y:10},flux:2,nmax:1,rect:{x0:8,y0:8,x1:12,y1:12}},
    {pos:{x:11,y:11},flux:4,nmax:1,rect:{x0:9,y0:9,x1:13,y1:13}},
    {pos:{x:40,y:40},flux:9,nmax:2,rect:{x0:38,y0:38,x1:42,y1:42}}];}}
  class DynamicPSF {executeGlobal(){this.psf=[[0,1,2,1,.01,.1,11,11,2,1,0,.002]];return true;}}
  Object.assign(DynamicPSF,{Star_DetectedOk:1,PSF_FittedOk:1,psf_starIndex:0,
    psf_status:3,psf_B:4,psf_A:5,psf_cx:6,psf_cy:7,psf_sx:8,psf_sy:9,psf_theta:10,psf_mad:11});
  const context=vm.createContext({Rect,StarDetector,DynamicPSF});
  vm.runInContext(code,context);
  return {run:regions=>context.DSGMeasureNative({isNull:false,mainView:{id:'test',image}},regions),
    selections:()=>[pushes,pops]};
}
test('records native estimates and spatially bounded fits without inventing validity',()=>{
  const f=fixture(),r=f.run([[0,0,64,64]]);
  assert.equal(r.starSelection.selected,1);
  assert.equal(r.fits.length,1);
  assert.equal(r.noise[0].estimates.length,3);
  assert.equal(r.noise[0].estimates[0].support,40);
  assert.equal(r.backgroundValidity,'NOT_ESTABLISHED');
  assert.equal(r.linearity,'NOT_ESTABLISHED');
  assert.equal(r.registration,'NOT_ESTABLISHED');
  assert.deepEqual(f.selections(),[2,2]);
});
test('restores selection after native noise failure',()=>{
  const f=fixture({failNoise:true});assert.throws(()=>f.run([[0,0,64,64]]),/Native failure/);
  assert.deepEqual(f.selections(),[1,1]);
});
test('empty star field stays empty, not a fabricated PSF',()=>{
  const r=fixture({empty:true}).run([]);assert.equal(r.fits.length,0);assert.equal(r.noise.length,0);
});
test('rejects ROI outside image before measurement',()=>{
  const f=fixture();assert.throws(()=>f.run([[0,0,65,64]]),/ROI/);assert.deepEqual(f.selections(),[0,0]);
});
