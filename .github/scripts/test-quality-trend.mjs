import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {buildQualityTrend} from '../../docs/javascripts/scientific-quality-trend.mjs';
const read = name => JSON.parse(fs.readFileSync(`docs/data/${name}.json`,'utf8'));
test('joins by identity, not array position; preserves all published scores',()=>{
 const p=read('scientific-data-quality-projection'), c=read('scientific-session-catalog');
 c.sessions.reverse();
 const result=buildQualityTrend(p,c);
 const knownIds=new Set(c.sessions.filter(s=>s.configurationId && s.configurationId!=='UNKNOWN').map(s=>s.sessionId));
 const expected=p.assessments.filter(a=>knownIds.has(a.sessionId) && a.projectionRecordState==='AVAILABLE');
 assert.equal(result.unknownSetup,p.assessments.filter(a=>!knownIds.has(a.sessionId)).length);
 const points=result.series.flatMap(g=>g.points).filter(p=>p.value!==null);
 assert.deepEqual(points.map(point=>[point.sessionId,point.value]).sort(),expected.map(a=>[a.sessionId,a.assessment.score.value]).sort());
 for(const group of result.series) for(const point of group.points) assert.equal(c.sessions.find(s=>s.sessionId===point.sessionId).configurationId,group.id);
});
test('new imported session appears without a hardcoded setup/date/value; unavailable is not zero',()=>{
 const catalog={sessions:[{sessionId:'new',configurationId:'THIRD',telescope:'T',camera:'C',observationDate:'2026-10-01'}]};
 const projection={assessments:[{sessionId:'new',target:'Target',projectionRecordState:'AVAILABLE',assessment:{score:{value:0}}}]};
 assert.equal(buildQualityTrend(projection,catalog).series[0].points[0].value,0);
 projection.assessments[0].projectionRecordState='UNAVAILABLE';
 assert.equal(buildQualityTrend(projection,catalog).series[0].points[0].value,null);
});
test('invalid date, missing identity, and invalid score never produce chart points',()=>{
 const c={sessions:[{sessionId:'a',configurationId:'S',observationDate:'missing'}]};
 const p={assessments:[{sessionId:'a',projectionRecordState:'AVAILABLE',assessment:{score:{value:85}}},{sessionId:'orphan'}]};
 const r=buildQualityTrend(p,c); assert.equal(r.unknownSetup,1); assert.equal(r.series[0].points[0].value,null);
 c.sessions[0].observationDate='2026-09-30';p.assessments[0].assessment.score.value=101;
 assert.equal(buildQualityTrend(p,c).series[0].points[0].value,null);
});
