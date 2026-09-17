import assert from 'node:assert/strict';
import fs from 'node:fs';
import zlib from 'node:zlib';

const p='governance/forecast-evidence/BKL031-F7-PROTECTED-SITE-RUN-35255829165/normalized-supply.json.gz.b64';
const original=JSON.parse(zlib.gunzipSync(Buffer.from(fs.readFileSync(p,'utf8').trim(),'base64')).toString('utf8'));
const projection=JSON.parse(fs.readFileSync('docs/data/observation-planner-forecast-f7-site-projection.json','utf8'));

function validateSupply(s){
  assert.equal(s.schemaVersion,'1.1');
  assert.equal(s.contractType,'BKL031_F7_FORECAST_RUNTIME_SUPPLY');
  assert.equal(s.environment,'EVALUATION');
  assert.equal(s.authority,'NONE');
  assert.equal(s.location.classification,'PROTECTED_EXACT_SITE');
  assert.equal(s.location.protectedSiteUsed,true);
  assert.equal(s.location.coordinatesPersisted,false);
  assert.equal(s.location.coordinatesPublished,false);
  assert.equal(s.freshness.maxRunAgeHours,18);
  assert.equal(s.freshness.state,'FRESH');
  assert.ok(s.freshness.runAgeHoursAtRetrieval>=0&&s.freshness.runAgeHoursAtRetrieval<=18);
  assert.equal(s.requestAccounting.maxProviderRequests,1);
  assert.equal(s.requestAccounting.requestOrdinal,1);
  assert.equal(s.requestAccounting.budgetState,'1/1_EXHAUSTED');
  assert.equal(s.series.rawInstantCount,s.series.acceptedInstantCount+s.series.excludedInstantCount);
  assert.equal(s.series.rawInstantCount,72);
  assert.equal(s.series.acceptedInstantCount,71);
  assert.equal(s.series.excludedInstantCount,1);
  assert.equal(s.series.futureAcceptedInstantCount,66);
  assert.equal(s.series.imputedValueCount,0);
  assert.equal(s.availabilityState,'DEGRADED');
  assert.equal(s.boundaries.recurringTraffic,false);
  assert.equal(s.boundaries.productionRuntimeActivated,false);
  assert.equal(s.boundaries.readinessAuthority,false);
  assert.equal(s.boundaries.schedulingAuthority,false);
  assert.equal(s.boundaries.automaticTargetSelection,false);
  assert.equal(s.boundaries.commandAuthority,'NONE');
  assert.equal(s.boundaries.safetyAuthority,'LOCAL_PHYSICAL_INTERLOCKS');
  assert.ok(!Object.hasOwn(s.location,'latitudeDeg')&&!Object.hasOwn(s.location,'longitudeDeg')&&!Object.hasOwn(s.location,'elevationM'));
}

function validateProjection(p){
  assert.equal(p.projectionType,'BKL031_F7_PROTECTED_SITE_SANITIZED_FORECAST_PROJECTION');
  assert.equal(p.environment,'EVALUATION');
  assert.equal(p.authority,'NONE');
  assert.equal(p.publicationState,'READ_ONLY');
  assert.equal(p.site.coordinateDisclosure,'PROHIBITED');
  assert.equal(p.sourceEvidence.acceptedHourlyInstantCount,71);
  assert.equal(p.sourceEvidence.excludedHourlyInstantCount,1);
  assert.equal(p.sourceEvidence.imputedValueCount,0);
  assert.equal(p.model.freshnessState,'FRESH');
  assert.ok(p.model.runAgeHoursAtRetrieval<=18);
  assert.equal(p.forecast.hourly.length,71);
  assert.equal(p.forecast.availabilityState,'DEGRADED');
  assert.equal(p.boundaries.readinessAuthority,false);
  assert.equal(p.boundaries.commandAuthority,'NONE');
}

validateSupply(original);
validateProjection(projection);

for(const mutate of [
  s=>{s.location.protectedSiteUsed=false;},
  s=>{s.location.coordinatesPersisted=true;},
  s=>{s.location.latitudeDeg=1;},
  s=>{s.freshness.state='STALE';},
  s=>{s.freshness.runAgeHoursAtRetrieval=19;},
  s=>{s.requestAccounting.maxProviderRequests=2;},
  s=>{s.requestAccounting.budgetState='0/1_AUTHORIZED';},
  s=>{s.series.imputedValueCount=1;},
  s=>{s.series.futureAcceptedInstantCount=0;},
  s=>{s.availabilityState='AVAILABLE';},
  s=>{s.boundaries.readinessAuthority=true;},
  s=>{s.boundaries.commandAuthority='MOUNT';}
]){ const copy=structuredClone(original); mutate(copy); assert.throws(()=>validateSupply(copy)); }

for(const mutate of [
  p=>{p.site.coordinateDisclosure='ALLOWED';},
  p=>{p.sourceEvidence.imputedValueCount=1;},
  p=>{p.model.freshnessState='STALE';},
  p=>{p.model.runAgeHoursAtRetrieval=19;},
  p=>{p.forecast.hourly.pop();},
  p=>{p.forecast.availabilityState='AVAILABLE';},
  p=>{p.boundaries.readinessAuthority=true;},
  p=>{p.boundaries.commandAuthority='MOUNT';}
]){ const copy=structuredClone(projection); mutate(copy); assert.throws(()=>validateProjection(copy)); }

console.log('BKL-031 F7 protected-site fail-closed mutation tests passed; zero network traffic.');
