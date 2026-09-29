import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {buildQualityTrend} from '../../docs/javascripts/scientific-quality-trend.mjs';
const read = name => JSON.parse(fs.readFileSync(`docs/data/${name}.json`,'utf8'));
test('joins by identity, not array position; preserves all published scores',()=>{
 const p=read('scientific-data-quality-projection'), c=read('scientific-session-catalog');
 c.sessions.reverse();
 const result=buildQualityTrend(p,c);
 assert.equal(result.series.length,2); assert.equal(result.unknownSetup,2);
 const points=result.series.flatMap(g=>g.points).filter(p=>p.value!==null);
 assert.equal(points.length,10);
 for(const point of points) assert.equal(point.value,p.assessments.find(a=>a.sessionId===point.sessionId).assessment.score.value);
 assert.equal(result.series.find(g=>g.id==='QUATTRO200_TOUPTEK294_BIN1').points.filter(p=>p.value!==null).length,1);
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
