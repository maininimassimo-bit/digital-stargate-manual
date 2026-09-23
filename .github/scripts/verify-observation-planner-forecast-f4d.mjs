import assert from 'node:assert/strict';
import fs from 'node:fs';

const projectionPath='docs/data/observation-planner-forecast-f4d-projection.json';
const schemaPath='schemas/observation-planner-forecast-projection-f4d.schema.json';
const sourcePath='governance/forecast-evidence/BKL031-F4C-RUN-35214129960/normalized-evidence.json';
const acceptancePath='docs/architecture/scientific-assets/BKL-031-F4-D-Sanitized-Forecast-Projection-and-Portal.md';
const projection=JSON.parse(fs.readFileSync(projectionPath,'utf8'));
const source=JSON.parse(fs.readFileSync(sourcePath,'utf8'));
const schema=JSON.parse(fs.readFileSync(schemaPath,'utf8'));
const acceptance=fs.readFileSync(acceptancePath,'utf8');

assert.equal(schema.$schema,'https://json-schema.org/draft/2020-12/schema');
assert.equal(projection.projectionType,'BKL031_F4D_SANITIZED_FORECAST_PROJECTION');
assert.equal(projection.environment,'EVALUATION');
assert.equal(projection.authority,'NONE');
assert.equal(projection.publicationState,'READ_ONLY');
assert.equal(projection.sourceEvidence.evidenceId,source.evidenceId);
assert.equal(projection.sourceEvidence.workflowRunId,source.workflowRunId);
assert.equal(projection.sourceEvidence.evidenceDigest,source.evidenceDigest);
assert.equal(projection.sourceEvidence.rawHourlyInstantCount,source.normalization.rawHourlyInstantCount);
assert.equal(projection.sourceEvidence.acceptedHourlyInstantCount,source.normalization.acceptedHourlyInstantCount);
assert.equal(projection.sourceEvidence.excludedHourlyInstantCount,source.normalization.excludedHourlyInstantCount);
assert.equal(projection.sourceEvidence.imputedValueCount,source.normalization.imputedValueCount);
assert.equal(projection.model.providerId,source.source.providerId);
assert.equal(projection.model.upstreamAuthorityId,source.source.upstreamAuthorityId);
assert.equal(projection.model.modelId,source.source.modelId);
assert.equal(projection.model.deliveryInterface,source.source.deliveryInterface);
assert.equal(projection.model.runInitialisationUtc,source.source.runInitialisationUtc);
assert.equal(projection.validity.fromUtc,source.validFromUtc);
assert.equal(projection.validity.toUtcExclusive,source.validToUtcExclusive);
assert.equal(projection.validity.acceptedHourlyInstants,source.forecastInstantsUtc.length);
assert.deepEqual(projection.excludedInstants.map(x=>x.validAtUtc),source.normalization.excludedInstants.map(x=>x.validAtUtc));
assert.deepEqual(projection.excludedInstants[0].missingVariables,source.normalization.excludedInstants[0].missingVariables);
assert.equal(projection.normalizationPolicy,source.normalization.policy);
assert.equal(projection.attribution,source.attribution);
assert.equal(projection.variables.length,11);
for(const [id,unit] of Object.entries(source.units)){
  const item=projection.variables.find(x=>x.id===id);
  assert.ok(item,`missing public variable ${id}`);
  assert.equal(item.unit,unit);
  assert.equal(item.availability,'AVAILABLE');
}
const visibility=projection.variables.find(x=>x.id==='visibility');
assert.deepEqual(visibility,{id:'visibility',unit:null,availability:'UNAVAILABLE'});

const forbidden=new Set(['latitudeDeg','longitudeDeg','elevationM','returnedGrid','rawResponseSha256','artifactId','requestId','requestRef','siteAuthorityRef','forecastInstantsUtc','series','score','rank','ranking','readiness','goNoGo','safe','isSafe','scheduler','command','deviceCommand','safetyAuthority']);
const walk=(v,path='projection')=>{ if(!v||typeof v!=='object')return; if(Array.isArray(v)){v.forEach((x,i)=>walk(x,`${path}[${i}]`));return;} for(const [k,x] of Object.entries(v)){assert.equal(forbidden.has(k),false,`${path}.${k} is forbidden in public projection`);walk(x,`${path}.${k}`);} };
walk(projection);
assert.equal(source.requestAccounting.furtherRequestsAuthorized,false);
assert.equal(source.boundaries.publicProjection,false);
assert.equal(source.location.protectedSiteUsed,false);
assert.ok(projection.limitations.includes('NO_ADDITIONAL_PROVIDER_TRAFFIC'));
assert.ok(projection.limitations.includes('NO_FORECAST_VALUES_PUBLISHED_IN_F4D'));
assert.ok(projection.limitations.includes('S10_RUNTIME_UNAVAILABLE'));

for(const expected of [
  '**ACCEPTED — POST-MERGE VERIFIED**',
  '#271',
  'f6aa9c5dffbc172d554872f9072029f56d1195ec',
  '8f948ba9593dc2bfde291d2658fe92eafd4cce28',
  '7/7 applicable push workflows successful',
  'F5 — Explainable Ranking Method and Read-Only Consumer'
]) assert.ok(acceptance.includes(expected),`F4-D acceptance record missing ${expected}`);

const roadmap=JSON.parse(fs.readFileSync('.github/roadmap/roadmap-source.json','utf8'));
assert.ok(['BKL-036', 'BKL-036-F5', 'AP-007', 'AP-008', 'AP-015', 'BKL-033', 'BKL-034', 'BKL-042'].includes(roadmap.currentPackage));
assert.ok(['BKL-036 Observatory Health Score', 'BKL-036-F5 Live Read-Only Health Score', 'AP-007 Enterprise Operations and Service Management Architecture', 'AP-008 Enterprise Integration Architecture', 'AP-015', 'BKL-033', 'BKL-034', 'BKL-042'].includes(roadmap.nextMilestone));
assert.ok(roadmap.milestones.some(entry=>entry.id==='M-BKL031-F4-D-ACCEPTANCE'));
assert.ok(roadmap.milestones.some(entry=>entry.id==='M-BKL031-F5-ACCEPTANCE'));

console.log('BKL-031 F4-D projection verified: accepted/post-merge verified sanitized metadata-only read-only projection derived exclusively from reconciled F4-C evidence; no coordinates, values, ranking, readiness, command or Safety Authority; F5 accepted; F6 real-evidence setup-aware E2E planner integration next; closure deferred.');
