'use strict';
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const [corePath, source, protocolPath, report] = process.argv.slice(2);
const sha = value => crypto.createHash('sha256').update(value).digest('hex');
const protocolBytes = fs.readFileSync(protocolPath);
const protocol = JSON.parse(protocolBytes);
const manifestBytes = fs.readFileSync(path.join(source, 'manifest.json'));
assert.equal(sha(manifestBytes), protocol.inputManifestSha256);
const manifest = JSON.parse(manifestBytes);
const context = vm.createContext({});
const script = fs.readFileSync(corePath);
new vm.Script(script.toString('utf8')).runInContext(context);
const sample = context.bkl046BilinearSampleControl;
const idx = (x,y) => y*64+x;

function readFits(entry) {
  const file = fs.readFileSync(path.join(source,entry.name));
  assert.equal(sha(file),entry.sha256);
  const h = {};
  let end = -1;
  for(let i=0; i<file.length; i+=80) {
    const card = file.subarray(i,i+80).toString('ascii');
    const key = card.slice(0,8).trim();
    if (key==='END') {end=i+80; break;}
    if (card.slice(8,10)==='= ') h[key]=card.slice(10).split('/')[0].trim();
  }
  assert.ok(end > 0);
  assert.equal(h.BITPIX,'-32'); assert.equal(h.NAXIS,'2');
  assert.equal(h.NAXIS1,'64'); assert.equal(h.NAXIS2,'64');
  const offset=Math.ceil(end/2880)*2880;
  return Array.from({length:4096},(_,i)=>file.readFloatBE(offset+4*i));
}

function host(input, fault) {
  const channels = {width:64,height:64,numberOfChannels:1};
  let mode=2;
  const source = {...channels, seen:0,
    get interpolation() {return mode;},
    set interpolation(value) {
      if (value===2 && fault==='read-and-restore') throw Error('FIXTURE_RESTORE');
      mode=value;
    },
    interpolate(x,y,c) {
      assert.equal(this.interpolation,1);
      assert.equal(c,0);
      this.seen++;
      if ((fault==='read' || fault==='read-and-restore') && this.seen===7) throw Error('FIXTURE_READ');
      if(fault==='nan' && this.seen===7) return NaN;
      const ix=Math.floor(x), iy=Math.floor(y), dx=x-ix, dy=y-iy;
      // Model the built-in only for this offline fixture. All real samples
      // will have to come from the observed PJSR call.
      return input[idx(ix,iy)]*(1-dx)*(1-dy)+input[idx(ix+1,iy)]*dx*(1-dy)+
             input[idx(ix,iy+1)]*(1-dx)*dy+input[idx(ix+1,iy+1)]*dx*dy;
    }
  };
  const target = {...channels, data: new Float32Array(64*64).fill(-1), n:0,
    setSample(value,x,y,c) {
      assert.equal(c,0);
      assert.ok(x>0 && x<63 && y>0 && y<63);
      assert.equal(this.data[idx(x,y)],-1);
      this.data[idx(x,y)]=value;
      if (fault==='write' && this.n===6) throw Error('FIXTURE_WRITE');
      this.n++;
    }
  };
  return {source,target};
}

function expected(buffer,x,y,fx,fy) {
  const lo = buffer[idx(x,y)]*(16-fx) + buffer[idx(x+1,y)]*fx;
  const hi = buffer[idx(x,y+1)]*(16-fx) + buffer[idx(x+1,y+1)]*fx;
  return ((16-fy)*lo+fy*hi)/256;
}

const results=[];
for(const row of manifest.fixtures) {
  const data=readFits(row);
  for(const [fx,fy] of protocol.phaseSixteenths) {
    const lab=host(data);
    const n=sample(lab.source,lab.target,fx,fy,1);
    assert.equal(n,3844);
    assert.equal(lab.target.n,n);
    assert.equal(lab.source.seen,n);
    assert.equal(lab.source.interpolation,2);
    let maxError=0;
    for(let y=1;y<63;y++) for(let x=1;x<63;x++)
      maxError=Math.max(maxError,Math.abs(lab.target.data[idx(x,y)]-expected(data,x,y,fx,fy)));
    assert.ok(maxError<=protocol.absoluteToleranceEncoded);
    results.push({id:row.id, phase:[fx,fy], samples:n, maxAbsoluteError:maxError});
  }
}
assert.equal(results.length,85);
const negative={};
const first=readFits(manifest.fixtures[0]);
for(const [fault,err] of [['read','FIXTURE_READ'],['write','FIXTURE_WRITE'],['nan','BKL046_CONTROL_INVALID_SAMPLE']]) {
  const lab=host(first,fault);
  assert.throws(()=>sample(lab.source,lab.target,4,12,1),{message:err});
  assert.equal(lab.source.interpolation,2);
  negative[fault]={error:err, completedWrites:lab.target.n, interpolationRestored:true};
}
const combined=host(first,'read-and-restore');
assert.throws(()=>sample(combined.source,combined.target,4,12,1), error => {
  assert.equal(error.message,'BKL046_CONTROL_RESTORE_FAILED');
  assert.equal(error.primaryFailed,true);
  assert.equal(error.primaryFailure.message,'FIXTURE_READ');
  assert.equal(error.restoreFailure.message,'FIXTURE_RESTORE');
  return true;
});
assert.equal(combined.source.interpolation,1);
negative.combined={error:'BKL046_CONTROL_RESTORE_FAILED',primary:'FIXTURE_READ',restore:'FIXTURE_RESTORE'};
const unsupported=host(first);
assert.throws(()=>sample(unsupported.source,unsupported.target,12,4,1),/INVALID_BINDING/);
assert.throws(()=>sample(unsupported.source,unsupported.source,0,0,1),/INVALID_BINDING/);
assert.throws(()=>sample(unsupported.source,unsupported.target,0,0,2),/INVALID_BINDING/);
assert.equal(unsupported.source.seen,0);
assert.equal(unsupported.target.n,0);
const reportValue={schema:'BKL046_PJSR_BILINEAR_CONTROL_SHIM_RESULT_V1',protocolSha256:sha(protocolBytes),
  callableSha256:sha(script),programSha256:sha(fs.readFileSync(__filename)), numericCases:results.length,
  results,negative,preconditionRefusals:3,usesNodeShim:true,actualPjsrInterpolationObserved:false,
  dynamicAlignmentObserved:false,admissionRequested:false,nativeExecutions:0,scientificClosures:0};
fs.writeFileSync(report,JSON.stringify(reportValue,null,2)+'\n',{flag:'wx'});
