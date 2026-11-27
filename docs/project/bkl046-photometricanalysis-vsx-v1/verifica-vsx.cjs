'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const crypto = require('node:crypto');
const [dataPath, enginePath, output] = process.argv.slice(2);
function read(path, expected) {
  const bytes=fs.readFileSync(path);
  assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'),expected);
  return bytes.toString('utf8').replace(/\r\n/g,'\n');
}
const dataSha='b9b710d28267d9a60258406c44893faacc81c557a7f149b0b5642c7d1e9dec47';
const engineSha='948f93e09d8a3f227c6e1dc86ee375834762a7e9229fed8b058fd093421edca7';
const d=read(dataPath,dataSha),e=read(enginePath,engineSha);
const start=d.indexOf('var VariableStarIndex = class');
const end=d.indexOf('\n};',start);
const a=e.indexOf('\n   ApplyVariables( found, pixelScale )');
const b=e.indexOf('\n   }',a);
assert(start>=0&&end>start&&a>=0&&b>a);
const ctx=vm.createContext({});
vm.runInContext(`
const VIZIER_MIRROR='fixture-only';
var useLocal=true, fail=false, downloaded=0, last;
const XESDServer={isAvailable:()=>useLocal};
class ExtendedSources {
  static objects_magnitude=0; static objects_fieldValues=1;
  static objects_name=2; static objects_ra=3; static objects_dec=4;
  executeGlobal() {
    last={database:this.database, command:this.command, radius:this.radius, exclusionFlags:this.exclusionFlags, fieldIds:this.fieldIds};
    this.objects=[[2,'["RR"]','one',0,0],[12,'[null]','two',1,2]];
    return !fail;
  }
}
class BackgroundDownload { constructor(){downloaded++; throw new Error('unexpected in fixture');} }
Math.rad=x=>x*Math.PI/180;
function AngularDistance(ra,dec,ra2,dec2){
  const s=(x)=>Math.sin(Math.rad(x)/2)**2;
  return 2*Math.asin(Math.sqrt(s(dec2-dec)+Math.cos(Math.rad(dec))*Math.cos(Math.rad(dec2))*s(ra2-ra)))*180/Math.PI;
}
`+d.slice(start,end+3)+'\nvar matcher=new class {'+e.slice(a,b+5)+'\n};',ctx);
const local=vm.runInContext('VariableStarIndex.Query(VariableStarIndex.Request(0,0,200,null))',ctx);
assert.equal(local.stars[0].magnitude,null);
assert.equal(local.stars[1].type,'');
assert.equal(local.stars[1].magnitude,12);
const parameters=JSON.parse(vm.runInContext('JSON.stringify(last)',ctx));
assert.deepEqual(parameters,{database:'VSX',command:'search',radius:180,exclusionFlags:2,fieldIds:'varType'});
const failed=vm.runInContext(`fail=true;
try{VariableStarIndex.Query(VariableStarIndex.Request(0,0,1,null));false}
catch(e){e.message==='Failure to search the local VSX database.'}`,ctx);
assert(failed);
assert.equal(ctx.downloaded,0);
function match(star,candidates,pixelScale){
  ctx.star=star;ctx.candidates=candidates;ctx.pixelScale=pixelScale;
  return vm.runInContext(`matcher.results={stars:[star]};
     matcher.ApplyVariables({stars:candidates,source:'invented'},pixelScale);
     matcher.variables.get(star)?.name || null`,ctx);
}
const star={ra:0,dec:0,catalogMagnitude:13};
const wrap={name:'wrap',ra:359.9998,dec:0,magnitude:13};
const closeFaint={name:'faint',ra:0.0001,dec:0,magnitude:17};
const farther={name:'fourArcsec',ra:4/3600,dec:0,magnitude:13};
assert.equal(match(star,[closeFaint,wrap],0),'wrap');
assert.equal(match(star,[farther],0),null);
assert.equal(match(star,[farther],4),'fourArcsec');
const report={
  schema:'BKL046_PHOTOMETRIC_ANALYSIS_VSX_BRANCHES_V1',
  sourceSha256:{data:dataSha,engine:engineSha},
  localParameters:parameters,
  localFailure:{threw:true,remoteDownloads:ctx.downloaded},
  matches:{rightAscensionWrapAccepted:true,faintCandidateRejected:true,
           fourArcsecAtDefaultScale:false,fourArcsecAtFourArcsecPixelScale:true},
  catalogMocked:true,nativeExecutions:0,scientificClosures:0,
};
const raw=Buffer.from(JSON.stringify(report,null,2)+'\n');
if(fs.existsSync(output)) assert(fs.readFileSync(output).equals(raw));
else fs.writeFileSync(output,raw,{flag:'wx'});
console.log(JSON.stringify(report));
