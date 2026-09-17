import fs from 'node:fs';
const PATH='docs/data/observation-planner-f8-current-astronomy-suitability.json';
const EVIDENCE_PATH='docs/data/observation-planner-f8-suitability-evidence.json';
const F7_PATH='docs/data/observation-planner-forecast-f7-site-projection.json';
const BASELINE_PATH='governance/setup-authority/configuration-baselines/DSG-SETUP-BASELINE-001.approved.json';
const METADATA_PATH='data/analytics/metadata/session-scientific-metadata.csv';
const req=(c,m,e)=>{if(!c)e.push(m)};
const eq=(a,b,t=1e-9)=>Math.abs(Number(a)-Number(b))<=t;
const r1=n=>Math.round((Number(n)+Number.EPSILON)*10)/10;
const isoKey=s=>new Date(s).toISOString();
function windowRows(d,w){const a=new Date(w.fromUtc),b=new Date(w.toUtcExclusive);return d.hourly.filter(h=>{const t=new Date(h.validAtUtc);return t>=a&&t<b});}
export function validateF8(d,ev,f7,baseline,metadata){
 const e=[];
 req(d.schemaVersion==='1.0','schemaVersion',e); req(d.projectionType==='BKL031_F8_CURRENT_ASTRONOMY_SETUP_SUITABILITY','projectionType',e);
 req(d.environment==='EVALUATION'&&d.authority==='NONE'&&d.consumerMode==='READ_ONLY','authority boundary',e);
 req(d.site?.coordinateDisclosure==='PROHIBITED','site coordinate disclosure',e); req(!('latitude' in (d.site||{}))&&!('longitude' in (d.site||{})),'protected coordinates leaked',e);
 req(d.sourceBindings?.forecastProjection===F7_PATH,'F7 binding',e); req(String(d.sourceBindings?.forecastWorkflowRunId)==='35255829165','F7 workflow lineage',e); req(d.sourceBindings?.siteAuthorityRef==='PROTECTED_RESOLVED_SERVER_SIDE','site authority binding',e);
 req(d.method?.id==='BKL031-F8-CURRENT-ASTRONOMY-SUITABILITY@1.0','method id',e);
 req(d.setupProfiles?.length===2,'setup count',e); req(d.targetProfiles?.length===2,'target count',e); req(d.hourly?.length===14,'hourly count',e); req(d.rankings?.length===2,'ranking count',e);
 const ids=new Set(d.setupProfiles?.map(x=>x.setupId)); req(ids.has('QUATTRO200_TOUPTEK294_BIN1')&&ids.has('C8_QHY695A_BIN1'),'governed setup ids',e);
 const tks=new Set(d.targetProfiles?.map(x=>x.targetKey)); req(tks.has('dsg-target:ldn-1320')&&tks.has('dsg-target:m-27'),'governed target ids',e);

 // Exact source bindings for the analytical evidence.
 req(ev?.methodId==='BKL031-F8-SETUP-SUITABILITY@1.1','suitability method evidence',e);
 req(ev?.sourceBindings?.setupBaseline?.path===BASELINE_PATH,'baseline path binding',e);
 req(ev?.sourceBindings?.setupBaseline?.payloadDigest===baseline?.payloadDigest?.value,'baseline digest binding',e);
 req(ev?.sourceBindings?.forecast?.path===F7_PATH,'evidence F7 path',e);
 req(ev?.sourceBindings?.forecast?.workflowRunId===f7?.sourceEvidence?.workflowRunId,'evidence F7 run',e);
 req(ev?.sourceBindings?.forecast?.artifactDigest===f7?.sourceEvidence?.artifactDigest,'evidence F7 digest',e);
 req(ev?.sourceBindings?.targetCoordinates?.path===METADATA_PATH,'target coordinate path',e);
 req(ev?.sourceBindings?.targetCoordinates?.blobSha==='4b6cc44ec992e3223134737eab9e1c49ff5a0d83','target coordinate blob binding',e);

 // Every F8 weather row must be an exact sanitized subset of F7 real site-specific evidence.
 const f7h=new Map((f7?.forecast?.hourly||[]).map(x=>[isoKey(x.validAtUtc),x]));
 for(const h of d.hourly||[]){const s=f7h.get(isoKey(h.validAtUtc));req(!!s,`F7 weather instant ${h.validAtUtc}`,e);if(!s)continue;for(const [a,b] of [['cloudCoverPct','cloudCoverPct'],['relativeHumidityPct','relativeHumidityPct'],['precipitationMm','precipitationMm'],['windSpeedKmh','windSpeedKmh'],['windGustKmh','windGustKmh']])req(eq(h.weather?.[a],s[b]),`F7 weather mismatch ${h.validAtUtc} ${a}`,e);}

 // Governed setup optical facts and derived FOV.
 const bp=new Map((baseline?.baselinePayload?.configurationProfiles||[]).map(x=>[x.configurationId,x]));
 for(const s of d.setupProfiles||[]){const g=bp.get(s.setupId);req(!!g,`baseline setup ${s.setupId}`,e);if(!g)continue;req(eq(s.effectiveFocalLengthMm,g.telescope?.effectiveFocalLengthMm),`focal length ${s.setupId}`,e);req(eq(s.effectiveFRatio,g.telescope?.effectiveFRatio),`f-ratio ${s.setupId}`,e);req(eq(s.imageScaleArcsecPx,g.camera?.imageScaleArcsecPx),`image scale ${s.setupId}`,e);const fw=2*Math.atan(s.sensorAreaMm.width/(2*s.effectiveFocalLengthMm))*180/Math.PI,fh=2*Math.atan(s.sensorAreaMm.height/(2*s.effectiveFocalLengthMm))*180/Math.PI;req(eq(s.fovDeg.width,fw,0.015),`FOV width ${s.setupId}`,e);req(eq(s.fovDeg.height,fh,0.015),`FOV height ${s.setupId}`,e);}

 // Governed target coordinates are pinned to the registered scientific metadata source.
 req(metadata.includes('LDN 1320,TGT-LDN-1320,63.8000,85.6331'),'LDN 1320 coordinate evidence',e);req(metadata.includes('M 27,TGT-MESSIER-M27,299.9017,22.7211'),'M27 coordinate evidence',e);
 for(const t of d.targetProfiles||[]){if(t.targetKey==='dsg-target:ldn-1320'){req(eq(t.raDegJ2000,63.8)&&eq(t.decDegJ2000,85.6331),'LDN 1320 coordinates',e)}if(t.targetKey==='dsg-target:m-27'){req(eq(t.raDegJ2000,299.9017)&&eq(t.decDegJ2000,22.7211),'M27 coordinates',e)}}

 // Suitability aggregate is auditable from machine-readable components; history is never authority.
 const w=ev?.componentWeights||{};req(eq((w.framing||0)+(w.filterSignal||0)+(w.imageScaleObjectClass||0),1),'suitability weights sum',e);
 const rankMap=new Map();for(const r of d.rankings||[])for(const t of r.targets||[])rankMap.set(`${r.setupId}|${t.targetKey}`,t);
 const setupMap=new Map((d.setupProfiles||[]).map(s=>[s.setupId,s]));
 for(const c of ev?.cases||[]){const key=`${c.setupId}|${c.targetKey}`,r=rankMap.get(key),s=setupMap.get(c.setupId);req(!!r,`suitability case ${key}`,e);if(!r)continue;const calc=w.framing*c.components.framing+w.filterSignal*c.components.filterSignal+w.imageScaleObjectClass*c.components.imageScaleObjectClass;req(eq(calc,c.aggregateScore,1e-8),`suitability aggregate evidence ${key}`,e);req(eq(r.setupSuitabilityScore,c.aggregateScore,1e-8),`projection suitability ${key}`,e);req(eq(r.framingRatioToShortFov,c.inputs.framingRatioToShortFov,1e-8),`framing ratio ${key}`,e);req(eq(s?.imageScaleArcsecPx,c.inputs.imageScaleArcsecPx,1e-8),`suitability image scale ${key}`,e);req(Array.isArray(c.reasonCodes)&&c.reasonCodes.length>=3,`reason codes ${key}`,e);
  for(const bw of r.bestWindows||[]){const rows=windowRows(d,bw);req(rows.length===2,`window row count ${key}`,e);if(rows.length!==2)continue;const astro=rows.reduce((z,h)=>z+h.targets[c.targetKey].astronomyFactor,0)/rows.length,weather=rows.reduce((z,h)=>z+h.targets[c.targetKey].weatherFactor,0)/rows.length,alt=rows.reduce((z,h)=>z+h.targets[c.targetKey].altitudeDeg,0)/rows.length,cloud=rows.reduce((z,h)=>z+h.weather.cloudCoverPct,0)/rows.length;const score=100*(d.method.scoreWeights.astronomy*astro+d.method.scoreWeights.weather*weather+d.method.scoreWeights.setupSuitability*(c.aggregateScore/100));req(eq(bw.advisoryScore,r1(score),0.051),`advisory score ${key} ${bw.fromUtc}`,e);req(eq(bw.meanAltitudeDeg,r1(alt),0.051),`mean altitude ${key} ${bw.fromUtc}`,e);req(eq(bw.meanCloudCoverPct,r1(cloud),0.051),`mean cloud ${key} ${bw.fromUtc}`,e);}
 }
 req(ev?.boundaries?.historicalAcquisitionUsedAsSuitabilityAuthority===false,'history suitability authority boundary',e);

 const b=d.boundaries||{}; req(b.readinessAuthority===false&&b.automaticTargetSelection===false&&b.schedulingAuthority===false,'advisory boundaries',e); req(b.actionAuthority==='NONE'&&b.commandAuthority==='NONE','action boundaries',e); req(b.safetyAuthority==='LOCAL_PHYSICAL_INTERLOCKS','safety authority',e); req(b.runtimeState==='UNAVAILABLE','S10 boundary',e); req(b.protectedCoordinatesPublished===false,'privacy boundary',e);
 const raw=JSON.stringify(d); for(const forbidden of ['42.4802338365823','11.56340644166358']) req(!raw.includes(forbidden),'protected coordinate leak',e);
 return e;
}
export function readInputs(){return {d:JSON.parse(fs.readFileSync(PATH,'utf8')),ev:JSON.parse(fs.readFileSync(EVIDENCE_PATH,'utf8')),f7:JSON.parse(fs.readFileSync(F7_PATH,'utf8')),baseline:JSON.parse(fs.readFileSync(BASELINE_PATH,'utf8')),metadata:fs.readFileSync(METADATA_PATH,'utf8')}}
if(process.argv[1]?.endsWith('verify-observation-planner-f8.mjs')){const x=readInputs(),e=validateF8(x.d,x.ev,x.f7,x.baseline,x.metadata);if(e.length){console.error(e.join('\n'));process.exit(1)}console.log('BKL-031 F8 verification OK — source-bound weather, setup/FOV and suitability known answers verified');}
