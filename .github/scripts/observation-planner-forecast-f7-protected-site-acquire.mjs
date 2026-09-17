import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

const VARS = ['temperature_2m','relative_humidity_2m','dew_point_2m','precipitation','cloud_cover','cloud_cover_low','cloud_cover_mid','cloud_cover_high','wind_speed_10m','wind_gusts_10m'];
const AUTH_ID = 'BKL031-F7-PROTECTED-SITE-PROVIDER-REQUEST-AUTH-001';
const PRIVACY_ID = 'BKL031-F7-PROTECTED-SITE-OUTBOUND-PRIVACY-AUTH-001';
const REQUIRED_RUN = '2026-09-17T12:00Z';
const SITE_REF = 'governance/site-authority/site-records/DSG-SITE-RECORD-MANCIANO-001.approved.json';
const args = Object.fromEntries(process.argv.slice(2).map((entry) => { const [k,...v]=entry.replace(/^--/,'').split('='); return [k,v.join('=') || true]; }));
const authPath = String(args.auth ?? 'governance/forecast-evidence/BKL031-F7-PROTECTED-SITE-PROVIDER-REQUEST-AUTH-001.json');
const privacyPath = String(args.privacy ?? 'governance/forecast-evidence/BKL031-F7-PROTECTED-SITE-OUTBOUND-PRIVACY-AUTH-001.json');
const assert = (condition,message) => { if(!condition) throw new Error(message); };
const auth = JSON.parse(fs.readFileSync(authPath,'utf8'));
const privacy = JSON.parse(fs.readFileSync(privacyPath,'utf8'));
const site = JSON.parse(fs.readFileSync(SITE_REF,'utf8'));

assert(auth.authorizationId===AUTH_ID,'provider authorization id mismatch.');
assert(auth.scope==='BKL-031-F7-PROTECTED-SITE-FRESH-FORECAST','provider authorization scope mismatch.');
assert(auth.status==='AUTHORIZED','provider authorization is not active.');
assert(auth.maxProviderRequests===1,'protected-site gate must authorize exactly one provider request.');
assert(auth.providerId==='OPEN_METEO'&&auth.modelId==='italia_meteo_arpae_icon_2i','provider/model authorization mismatch.');
assert(auth.runInitialisationUtc===REQUIRED_RUN,'authorized run mismatch.');
assert(auth.siteAuthorityRef===SITE_REF&&auth.protectedSiteUsed===true,'protected site authority mismatch.');
assert(auth.privacyDecisionRef===privacyPath,'privacy decision reference mismatch.');
assert(auth.recurringTraffic===false&&auth.productionUse===false,'recurring or production traffic is forbidden.');

assert(privacy.decisionId===PRIVACY_ID&&privacy.status==='AUTHORIZED','outbound privacy authorization is not active.');
assert(privacy.siteAuthorityRef===SITE_REF,'privacy site authority mismatch.');
assert(privacy.permittedRecipient?.host==='single-runs-api.open-meteo.com','privacy recipient mismatch.');
assert(privacy.coordinatePolicy?.source==='GOVERNED_APPROVED_SITE_RECORD','privacy coordinate source mismatch.');
assert(privacy.coordinatePolicy?.use==='SERVER_SIDE_PROVIDER_REQUEST_ONLY','privacy coordinate use mismatch.');
assert(privacy.coordinatePolicy?.logCoordinates===false&&privacy.coordinatePolicy?.publishCoordinates===false,'privacy publication boundary mismatch.');

assert(site.lifecycle?.state==='APPROVED'&&site.lifecycle?.eligibleForResolution===true,'site record is not approved/resolver eligible.');
assert(site.sitePayload?.siteRecordId==='DSG-SITE-RECORD-MANCIANO-001','site record id mismatch.');
assert(site.sitePayload?.scope==='OBSERVATION_PLANNER_READ_ONLY_SITE_AUTHORITY','site scope mismatch.');
assert(site.sitePayload?.classification==='PROTECTED_EXACT_SITE','site classification mismatch.');
assert(site.sitePayload?.geodesy?.datum==='WGS84','site datum mismatch.');
assert(site.sitePayload?.publicationPolicy?.exactCoordinates==='PROHIBITED','site public-coordinate policy mismatch.');
assert(site.sitePayload?.publicationPolicy?.elevation==='PROHIBITED','site elevation publication policy mismatch.');
const latitude = site.sitePayload.geodesy.latitudeDeg;
const longitude = site.sitePayload.geodesy.longitudeDeg;
assert(Number.isFinite(latitude)&&latitude>=-90&&latitude<=90,'governed latitude is invalid.');
assert(Number.isFinite(longitude)&&longitude>=-180&&longitude<=180,'governed longitude is invalid.');

const runMs=Date.parse(REQUIRED_RUN); const now=Date.now(); const ageHours=(now-runMs)/3_600_000;
assert(runMs<=now && ageHours<=18,'authorized run is stale or in the future.');

const url=new URL('https://single-runs-api.open-meteo.com/v1/forecast');
for(const [key,value] of Object.entries({latitude:String(latitude),longitude:String(longitude),hourly:VARS.join(','),models:'italia_meteo_arpae_icon_2i',run:REQUIRED_RUN.slice(0,-1),timezone:'GMT',timeformat:'iso8601',cell_selection:'land',elevation:'nan',forecast_hours:'72'})) url.searchParams.set(key,value);
const plan={
  gateId:'BKL031-F7-PROTECTED-SITE-ONE-FRESH-FORECAST-REQUEST-001',
  authorizationId:AUTH_ID,
  privacyDecisionId:PRIVACY_ID,
  expectedHost:'single-runs-api.open-meteo.com',
  method:'GET', redirects:'DENY', maxRequestsThisGate:1, timeoutMs:10000, maxResponseBytes:2000000,
  location:{classification:'PROTECTED_EXACT_SITE',siteAuthorityRef:'DSG-SITE-RECORD-MANCIANO-001',publicLabel:privacy.publicLocationLabel,coordinatesPersisted:false,coordinatesPublished:false},
  providerId:'OPEN_METEO', upstreamAuthorityId:'ITALIAMETEO_ARPAE', modelId:'italia_meteo_arpae_icon_2i',
  runInitialisationUtc:REQUIRED_RUN, variables:VARS, protectedSiteUsed:true, recurringTraffic:false, productionUse:false
};
assert(url.hostname===plan.expectedHost,'request host mismatch.');
if(args.preflight){ console.log(JSON.stringify(plan,null,2)); process.exit(0); }
assert(args.execute && args.confirm==='F7_PROTECTED_SITE_ONE_REQUEST','execution requires exact protected-site confirmation.');

const out=path.resolve(String(args.out ?? 'work/f7-protected-site-evidence')); fs.mkdirSync(out,{recursive:true});
fs.writeFileSync(path.join(out,'request-plan.json'),JSON.stringify(plan,null,2)+'\n');
const failure=(details)=>fs.writeFileSync(path.join(out,'failure-summary.json'),JSON.stringify({gateId:plan.gateId,authorizationId:AUTH_ID,requestCountThisGate:1,budgetState:'1/1_EXHAUSTED',protectedSiteUsed:true,...details},null,2)+'\n');
const controller=new AbortController(); const timer=setTimeout(()=>controller.abort(),plan.timeoutMs); let response;
try { response=await fetch(url,{method:'GET',redirect:'manual',headers:{accept:'application/json','user-agent':'digital-stargate-bkl031-f7-protected-site/1.0'},signal:controller.signal}); }
catch(error){ clearTimeout(timer); failure({failureClass:'TRANSPORT',errorName:error?.name??'Error'}); throw new Error('provider transport failure.'); }
if(response.status>=300&&response.status<400){ clearTimeout(timer); failure({failureClass:'REDIRECT_DENIED',httpStatus:response.status}); await response.body?.cancel().catch(()=>undefined); throw new Error('redirect denied.'); }
const chunks=[]; let byteLength=0; const declared=Number(response.headers.get('content-length'));
if(Number.isFinite(declared)&&declared>plan.maxResponseBytes){ clearTimeout(timer); failure({failureClass:'RESPONSE_TOO_LARGE',declaredByteLength:declared}); await response.body?.cancel().catch(()=>undefined); throw new Error('response too large.'); }
try { const reader=response.body?.getReader(); assert(reader,'provider response body unavailable.'); while(true){ const {done,value}=await reader.read(); if(done) break; byteLength+=value.byteLength; if(byteLength>plan.maxResponseBytes){ failure({failureClass:'RESPONSE_TOO_LARGE',observedByteLength:byteLength}); controller.abort(); await reader.cancel().catch(()=>undefined); throw new Error('response too large.'); } chunks.push(value); } } finally { clearTimeout(timer); }
const bytes=new Uint8Array(byteLength); let offset=0; for(const chunk of chunks){ bytes.set(chunk,offset); offset+=chunk.byteLength; }
const rawSha256=crypto.createHash('sha256').update(bytes).digest('hex');
fs.writeFileSync(path.join(out,'raw-response.sha256'),rawSha256+'\n');
if(response.status!==200){ failure({failureClass:'PROVIDER_HTTP',httpStatus:response.status,rawSha256,byteLength}); throw new Error(`provider HTTP ${response.status}.`); }
let raw; try { raw=JSON.parse(new TextDecoder().decode(bytes)); } catch { failure({failureClass:'INVALID_JSON',rawSha256,byteLength}); throw new Error('provider response is not JSON.'); }
if(raw.error){ failure({failureClass:'PROVIDER_ERROR',rawSha256,byteLength}); throw new Error('provider returned an error payload.'); }
assert(raw.timezone==='GMT'&&raw.utc_offset_seconds===0,'provider timezone mismatch.');
assert(raw.hourly&&Array.isArray(raw.hourly.time)&&raw.hourly.time.length>=1&&raw.hourly.time.length<=72,'hourly time array outside bounds.');
for(const variable of VARS) assert(Array.isArray(raw.hourly[variable])&&raw.hourly[variable].length===raw.hourly.time.length,`${variable} array mismatch.`);

const retrievedAtUtc=new Date().toISOString(); const retrievedMs=Date.parse(retrievedAtUtc); const accepted=[]; const excluded=[];
for(let i=0;i<raw.hourly.time.length;i++){
  const values={}; const missing=[];
  for(const variable of VARS){ const value=raw.hourly[variable][i]; if(typeof value!=='number'||!Number.isFinite(value)) missing.push(variable); else values[variable]=value; }
  const instantUtc=raw.hourly.time[i].endsWith('Z')?raw.hourly.time[i]:raw.hourly.time[i]+'Z';
  if(missing.length) excluded.push({instantUtc,reason:'MISSING_OR_NON_FINITE_GOVERNED_VARIABLE',variables:missing}); else accepted.push({instantUtc,values});
}
const futureAcceptedInstantCount=accepted.filter(x=>Date.parse(x.instantUtc)>=retrievedMs).length;
const runAgeHoursAtRetrieval=(retrievedMs-runMs)/3_600_000; const freshnessState=runAgeHoursAtRetrieval<=18?'FRESH':'STALE';
const availabilityState=accepted.length===0||futureAcceptedInstantCount===0?'UNAVAILABLE':excluded.length?'DEGRADED':'AVAILABLE';
const supply={
  schemaVersion:'1.1', contractType:'BKL031_F7_FORECAST_RUNTIME_SUPPLY', supplyId:`BKL031-F7-PROTECTED-SITE-SUPPLY-${process.env.GITHUB_RUN_ID??'LOCAL'}`,
  environment:'EVALUATION', authority:'NONE', authorizationId:AUTH_ID, privacyDecisionId:PRIVACY_ID,
  providerId:'OPEN_METEO', upstreamAuthorityId:'ITALIAMETEO_ARPAE', modelId:'italia_meteo_arpae_icon_2i', runInitialisationUtc:REQUIRED_RUN, retrievedAtUtc,
  rawSha256, responseByteLength:byteLength,
  location:{classification:'PROTECTED_EXACT_SITE',siteAuthorityRef:'DSG-SITE-RECORD-MANCIANO-001',publicLabel:privacy.publicLocationLabel,protectedSiteUsed:true,coordinatesPersisted:false,coordinatesPublished:false},
  freshness:{maxRunAgeHours:18,runAgeHoursAtRetrieval:Number(runAgeHoursAtRetrieval.toFixed(6)),state:freshnessState},
  requestAccounting:{maxProviderRequests:1,requestOrdinal:1,budgetState:'1/1_EXHAUSTED'},
  series:{rawInstantCount:raw.hourly.time.length,acceptedInstantCount:accepted.length,excludedInstantCount:excluded.length,futureAcceptedInstantCount,imputedValueCount:0,units:raw.hourly_units??{},accepted,excluded},
  availabilityState,
  boundaries:{recurringTraffic:false,productionRuntimeActivated:false,readinessAuthority:false,schedulingAuthority:false,automaticTargetSelection:false,commandAuthority:'NONE',safetyAuthority:'LOCAL_PHYSICAL_INTERLOCKS'}
};
fs.writeFileSync(path.join(out,'normalized-supply.json'),JSON.stringify(supply,null,2)+'\n');
fs.writeFileSync(path.join(out,'summary.json'),JSON.stringify({gateId:plan.gateId,authorizationId:AUTH_ID,privacyDecisionId:PRIVACY_ID,requestCountThisGate:1,budgetState:'1/1_EXHAUSTED',rawSha256,byteLength,runInitialisationUtc:REQUIRED_RUN,retrievedAtUtc,availabilityState,rawInstantCount:supply.series.rawInstantCount,acceptedInstantCount:supply.series.acceptedInstantCount,excludedInstantCount:supply.series.excludedInstantCount,futureAcceptedInstantCount,protectedSiteUsed:true,coordinatesPersisted:false,coordinatesPublished:false},null,2)+'\n');
if(freshnessState!=='FRESH'||availabilityState==='UNAVAILABLE'){ failure({failureClass:'SUPPLY_NOT_FRESH_OR_AVAILABLE',rawSha256,byteLength,freshnessState,availabilityState,futureAcceptedInstantCount}); throw new Error('fresh protected-site forecast supply unavailable.'); }
console.log(JSON.stringify({rawSha256,byteLength,availabilityState,acceptedInstantCount:accepted.length,excludedInstantCount:excluded.length,futureAcceptedInstantCount,protectedSiteUsed:true,coordinatesLogged:false,coordinatesPersisted:false,out},null,2));
