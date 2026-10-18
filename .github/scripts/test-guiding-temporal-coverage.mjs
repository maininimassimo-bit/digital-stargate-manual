import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {buildGuidingTemporalCoverage as build} from './guiding-temporal-coverage.mjs';
const nina=(start='2026-10-14T23:59:58',seconds=10)=>[
  `${start}|INFO|PHD2Guider.cs|Connect|205|Connecting to PHD2 server at 127.0.0.1:4400`,
  `${start}|INFO|SequenceItem.cs|Run|208|Starting Category: Camera, Item: TakeExposure, ExposureTime ${seconds}, ImageType LIGHT`,
  `${start}|INFO|CameraVM.cs|Capture|742|Starting Exposure - Exposure Time: ${seconds}s`,
  '2026-10-15T00:00:08|INFO|SequenceItem.cs|Run|254|Finishing Category: Camera, Item: TakeExposure, ImageType LIGHT'
].join('\n');
const row=(t,error=0)=>`1,${t},"Mount",0,0,0,0,0.2,0.3,0,,0,,,,500,30,${error}`;
const guide=(rows)=>['Guiding Begins at 2026-10-14 23:59:58','Exposure = 2000 ms',...rows,'Guiding Ends at 2026-10-15 00:00:08'].join('\n');
const run=(n,g,count=1)=>build([{path:'nina.log',text:n}],[{path:'guide.txt',text:g}],count);
test('midnight LIGHT overlap uses duration denominator and no extrapolated tails',()=>{
  const result=run(nina(),guide([row(2),row(4),row(6),row(8)]));
  assert.equal(result.coverage,0.6);assert.equal(result.lightSeconds,10);assert.equal(result.coveredSeconds,6);
  assert.equal(result.sourceRefs.length,2);assert.match(result.sourceRefs[0].sha256,/^[a-f0-9]{64}$/);
});
test('settling, invalid samples and long gaps do not bridge time',()=>{
  assert.equal(run(nina(),guide([row(0),row(2,2),row(4),row(6),row(8)])).coverage,0.4);
  assert.equal(run(nina(),guide([row(0),row(2),'INFO: SETTLING STATE CHANGE, Settling started',row(4),'INFO: SETTLING STATE CHANGE, Settling complete',row(6),row(8)])).coverage,0.4);
  assert.equal(run(nina(),guide([row(0),row(1),row(8),row(9)])).coverage,0.2);
});
test('pause persists until resume and never bridges either boundary',()=>{
  assert.equal(run(nina(),guide([row(0),row(2),'INFO: Guiding paused',row(4),row(6),'INFO: Guiding resumed',row(8),row(10)])).coverage,0.4);
});
test('unknown remote clock and unpaired/mismatched LIGHTs fail closed',()=>{
  const g=guide([row(0),row(2)]);
  for (const n of [nina().replace('127.0.0.1','192.168.1.2'),nina().split('\n').slice(0,-1).join('\n')]) assert.equal(run(n,g).state,'UNAVAILABLE');
  assert.equal(run(nina(),g,2).reason,'LIGHT_COUNT_MISMATCH');
});
test('invalid guide time order fails closed, absent guide remains unknown',()=>{
  assert.equal(run(nina(),guide([row(4),row(2)])).reason,'NON_MONOTONIC_GUIDE_CLOCK');
  assert.equal(run(nina(),'').coverage,null);
});
test('known valid guiding outside LIGHT intervals is measured zero',()=>{
  const g=guide([row(0),row(2)]).replace('Guiding Begins at 2026-10-14 23:59:58','Guiding Begins at 2026-10-14 20:00:00');
  assert.equal(run(nina(),g).coverage,0);
});
test('duplicate guide sources cannot double count covered seconds',()=>{
  const g={path:'guide.txt',text:guide([row(0),row(2),row(4)])};
  assert.equal(build([{path:'nina.log',text:nina()}],[g,g],1).coverage,0.4);
});
test('clock reversal across guide segments (including DST fallback) is unavailable',()=>{
  const g=guide([row(0),row(2)])+'\n'+guide([row(0),row(2)]).replace('23:59:58','22:59:58');
  assert.equal(run(nina(),g).reason,'NON_MONOTONIC_GUIDE_CLOCK');
  assert.equal(run(nina().replace('2026-10-14T23:59:58|INFO|SequenceItem','bad-time|INFO|SequenceItem'),guide([row(0),row(2)])).reason,'INVALID_LIGHT_INTERVAL');
});
test('non-UTF8 source bytes cannot be mislabeled with a reconstructed digest',()=>{
  const bytes=Buffer.from([0xff]);
  const result=build([{path:'nina.log',bytes,text:bytes.toString('utf8')}],[]);
  assert.equal(result.reason,'INVALID_SOURCE_ENCODING');
});
test('latest real imported logs reproduce the catalog numerator and denominator',()=>{
  const catalog=JSON.parse(readFileSync('docs/data/scientific-session-catalog.json','utf8'));
  const latest=catalog.sessions.find(s=>s.sessionId==='2026-10-14_2026-10-15');
  const t=latest.guiding.temporalCoverage;
  const sources=t.sourceRefs.map(r=>({path:r.path,text:readFileSync(r.path,'utf8')}));
  const metrics=JSON.parse(readFileSync(latest.sourceMetricsPath,'utf8'));
  const actual=build(sources.filter(s=>s.path.includes('/nina/')),sources.filter(s=>s.path.includes('/phd2/')),latest.lightStarted,metrics.nina.acquisition_scope);
  assert.deepEqual(actual,t);assert.equal(t.lightSeconds,56*600);assert(t.coverage>0&&t.coverage<1);
});
