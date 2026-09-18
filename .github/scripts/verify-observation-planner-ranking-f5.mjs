import assert from 'node:assert/strict';
import fs from 'node:fs';
import { rankFixture, canonicalJson, FACTORS } from './observation-planner-ranking-f5.mjs';

const fixturePath='docs/data/observation-planner-ranking-f5-fixture.json';
const projectionPath='docs/data/observation-planner-ranking-f5-projection.json';
const schemaPath='schemas/observation-planner-ranking-f5.schema.json';
const architecturePath='docs/architecture/scientific-assets/BKL-031-F5-Explainable-Ranking-Method-and-Read-Only-Consumer.md';
const acceptancePath='docs/project/BKL-031-F5-EXPLAINABLE-RANKING-ACCEPTANCE-2026-09-17.md';
const developerPath='.github/workflows/developer-foundation.yml';
for (const p of [fixturePath,projectionPath,schemaPath,architecturePath,acceptancePath,developerPath,'docs/data/target-knowledge-read-model.json','docs/data/observation-planner-forecast-f4d-projection.json','.github/roadmap/roadmap-source.json']) assert.ok(fs.existsSync(p),`missing F5 artifact: ${p}`);

const fixture=JSON.parse(fs.readFileSync(fixturePath,'utf8'));
const projection=JSON.parse(fs.readFileSync(projectionPath,'utf8'));
const schema=JSON.parse(fs.readFileSync(schemaPath,'utf8'));
const targetKnowledge=JSON.parse(fs.readFileSync('docs/data/target-knowledge-read-model.json','utf8'));
const forecast=JSON.parse(fs.readFileSync('docs/data/observation-planner-forecast-f4d-projection.json','utf8'));
const roadmap=JSON.parse(fs.readFileSync('.github/roadmap/roadmap-source.json','utf8'));
const architecture=fs.readFileSync(architecturePath,'utf8');
const acceptance=fs.readFileSync(acceptancePath,'utf8');
const developer=fs.readFileSync(developerPath,'utf8');

assert.equal(schema.$schema,'https://json-schema.org/draft/2020-12/schema');
assert.equal(schema.additionalProperties,false);
assert.equal(schema.properties.environment.const,'EVALUATION');
assert.equal(schema.properties.authority.const,'NONE');
assert.equal(schema.properties.consumerMode.const,'READ_ONLY');
assert.equal(schema.properties.boundary.properties.readinessAuthority.const,false);
assert.equal(schema.properties.boundary.properties.actionAuthority.const,'NONE');

const targetByKey=new Map(targetKnowledge.targets.map(t=>[t.target_key,t]));
for (const c of fixture.candidates) {
  const governed=targetByKey.get(c.targetKey);
  assert.ok(governed,`candidate not found in target knowledge: ${c.targetKey}`);
  assert.equal(governed.target_id,c.targetId);
  assert.equal(governed.canonical_name,c.canonicalName);
  assert.equal(governed.identity_state,'validated');
}
assert.equal(fixture.lineage.forecastEvidenceDigest,forecast.sourceEvidence.evidenceDigest);
assert.equal(fixture.lineage.forecastCompleteness,`${forecast.sourceEvidence.acceptedHourlyInstantCount}/${forecast.sourceEvidence.rawHourlyInstantCount}`);
assert.equal(fixture.lineage.providerRequestBudget,'2/2_EXHAUSTED');
assert.ok(forecast.limitations.includes('NO_FORECAST_VALUES_PUBLISHED_IN_F4D'));

const regenerated=rankFixture(structuredClone(fixture));
assert.equal(canonicalJson(projection),canonicalJson(regenerated),'persisted F5 projection differs from deterministic engine output');
assert.equal(projection.results.length,2);
assert.deepEqual(projection.results.map(r=>[r.rank,r.targetKey,r.score]),[[1,'dsg-target:ldn-1320',76.3889],[2,'dsg-target:m-27',53.0556]]);
assert.ok(Math.abs(FACTORS.reduce((s,f)=>s+f.weight,0)-1)<=1e-12,'F5 factor weights must sum to 1 within IEEE-754 tolerance');
assert.equal(projection.boundary.readinessAuthority,false);
assert.equal(projection.boundary.automaticTargetSelection,false);
assert.equal(projection.boundary.schedulingAuthority,false);
assert.equal(projection.boundary.commandAuthority,'NONE');
assert.equal(projection.boundary.safetyAuthority,'LOCAL_PHYSICAL_INTERLOCKS');

const forbiddenKeys=new Set(['safe','isSafe','ready','readiness','goNoGo','scheduler','scheduleCommand','deviceCommand','command','safetyDecision','automaticSelection']);
function scan(value,path='$') {
  if (Array.isArray(value)) return value.forEach((v,i)=>scan(v,`${path}[${i}]`));
  if (!value || typeof value!=='object') return;
  for (const [k,v] of Object.entries(value)) {
    assert.ok(!forbiddenKeys.has(k),`forbidden F5 key ${path}.${k}`);
    scan(v,`${path}.${k}`);
  }
}
scan(projection);

for (const fragment of ['**ACCEPTED — POST-MERGE VERIFIED**','synthetic factor values','no readiness','BKL-032','S10','777924e2638430f15bf717fa33dd71057751625a','7/7 applicable push workflows successful']) assert.ok(architecture.toLowerCase().includes(fragment.toLowerCase()),`F5 architecture record missing: ${fragment}`);
for (const fragment of ['**ACCEPTED — POST-MERGE VERIFIED**','#273','dfda963e7e9d088282516200a6bd8bb64dd0dd1d','777924e2638430f15bf717fa33dd71057751625a','6/6 successful','7/7 successful','2/2_EXHAUSTED']) assert.ok(acceptance.includes(fragment),`F5 acceptance record missing: ${fragment}`);
for (const fragment of ['Verify Observation Planner F5 explainable ranking','Test Observation Planner F5 deterministic and fail-closed rules','Check Observation Planner F5 browser consumer syntax']) assert.ok(developer.includes(fragment),`Developer Foundation does not preserve F5 regression coverage: ${fragment}`);
assert.equal(roadmap.currentPackage,'BKL-031');
assert.equal(roadmap.nextMilestone,'BKL-031 F9 governed refresh, portal verification and acceptance reconciliation');
assert.ok(roadmap.milestones.some(entry=>entry.id==='M-BKL031-F5-ACCEPTANCE'),'roadmap F5 acceptance milestone missing');
const f5AcceptanceMilestone=roadmap.milestones.find(entry=>entry.id==='M-BKL031-F5-ACCEPTANCE');
assert.ok(f5AcceptanceMilestone.description.includes('F6 real-evidence setup-aware E2E planner integration is next'),'F5 acceptance milestone must promote F6 real-evidence setup-aware E2E planner');
assert.ok(f5AcceptanceMilestone.description.includes('capability closure remains deferred'),'F5 acceptance milestone must preserve deferred BKL-031 closure');
assert.ok(!f5AcceptanceMilestone.description.includes('F6 capability closure is next'),'F5 acceptance milestone must not re-authorize early capability closure');
console.log(`BKL-031 F5 verified: accepted/post-merge verified, ${projection.results.length} candidates, method ${projection.method.id}@${projection.method.version}, digest ${projection.projectionDigest}; F6 real-evidence setup-aware E2E planner integration next; closure deferred.`);
