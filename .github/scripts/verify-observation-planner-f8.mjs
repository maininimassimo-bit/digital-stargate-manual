import fs from 'node:fs';
const PATH='docs/data/observation-planner-f8-current-astronomy-suitability.json';
const req=(c,m,e)=>{if(!c)e.push(m)};
export function validateF8(d){
 const e=[];
 req(d.schemaVersion==='1.0','schemaVersion',e); req(d.projectionType==='BKL031_F8_CURRENT_ASTRONOMY_SETUP_SUITABILITY','projectionType',e);
 req(d.environment==='EVALUATION'&&d.authority==='NONE'&&d.consumerMode==='READ_ONLY','authority boundary',e);
 req(d.site?.coordinateDisclosure==='PROHIBITED','site coordinate disclosure',e); req(!('latitude' in (d.site||{}))&&!('longitude' in (d.site||{})),'protected coordinates leaked',e);
 req(d.sourceBindings?.forecastProjection==='docs/data/observation-planner-forecast-f7-site-projection.json','F7 binding',e);
 req(String(d.sourceBindings?.forecastWorkflowRunId)==='35255829165','F7 workflow lineage',e);
 req(d.sourceBindings?.siteAuthorityRef==='PROTECTED_RESOLVED_SERVER_SIDE','site authority binding',e);
 req(d.method?.id==='BKL031-F8-CURRENT-ASTRONOMY-SUITABILITY@1.0','method id',e);
 req(d.setupProfiles?.length===2,'setup count',e); req(d.targetProfiles?.length===2,'target count',e); req(d.hourly?.length===14,'hourly count',e); req(d.rankings?.length===2,'ranking count',e);
 const ids=new Set(d.setupProfiles?.map(x=>x.setupId)); req(ids.has('QUATTRO200_TOUPTEK294_BIN1')&&ids.has('C8_QHY695A_BIN1'),'governed setup ids',e);
 const tks=new Set(d.targetProfiles?.map(x=>x.targetKey)); req(tks.has('dsg-target:ldn-1320')&&tks.has('dsg-target:m-27'),'governed target ids',e);
 for(const r of d.rankings||[]){req(ids.has(r.setupId),`ranking setup ${r.setupId}`,e); req(r.targets?.length===2,`ranking targets ${r.setupId}`,e); for(const t of r.targets||[]){req(t.setupSuitabilityScore>=0&&t.setupSuitabilityScore<=100,'suitability range',e); req(t.bestWindows?.length>0,'best windows',e);}}
 const b=d.boundaries||{}; req(b.readinessAuthority===false&&b.automaticTargetSelection===false&&b.schedulingAuthority===false,'advisory boundaries',e); req(b.actionAuthority==='NONE'&&b.commandAuthority==='NONE','action boundaries',e); req(b.safetyAuthority==='LOCAL_PHYSICAL_INTERLOCKS','safety authority',e); req(b.runtimeState==='UNAVAILABLE','S10 boundary',e); req(b.protectedCoordinatesPublished===false,'privacy boundary',e);
 const raw=JSON.stringify(d); for(const forbidden of ['42.4802338365823','11.56340644166358']) req(!raw.includes(forbidden),'protected coordinate leak',e);
 return e;
}
if(process.argv[1]?.endsWith('verify-observation-planner-f8.mjs')){const d=JSON.parse(fs.readFileSync(PATH,'utf8'));const e=validateF8(d);if(e.length){console.error(e.join('\n'));process.exit(1)}console.log('BKL-031 F8 verification OK');}
