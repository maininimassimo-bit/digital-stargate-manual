import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

const VARS = ['temperature_2m','relative_humidity_2m','dew_point_2m','precipitation','cloud_cover','cloud_cover_low','cloud_cover_mid','cloud_cover_high','wind_speed_10m','wind_gusts_10m'];
const AUTH_ID = 'BKL031-F7-PROVIDER-REQUEST-AUTH-001';
const REQUIRED_RUN = '2026-09-17T12:00Z';
const args = Object.fromEntries(process.argv.slice(2).map((entry) => { const [k,...v]=entry.replace(/^--/,'').split('='); return [k,v.join('=') || true]; }));
const authPath = String(args.auth ?? 'governance/forecast-evidence/BKL031-F7-PROVIDER-REQUEST-AUTH-001.json');
const auth = JSON.parse(fs.readFileSync(authPath,'utf8'));
function assert(condition,message){ if(!condition) throw new Error(message); }
assert(auth.authorizationId===AUTH_ID,'authorization id mismatch.');
assert(auth.scope==='BKL-031-F7-FRESH-FORECAST-SUPPLY','authorization scope mismatch.');
assert(auth.status==='AUTHORIZED','authorization is not active.');
assert(auth.maxProviderRequests===1,'F7 authorization must allow exactly one provider request.');
assert(auth.providerId==='OPEN_METEO'&&auth.modelId==='italia_meteo_arpae_icon_2i','authorization provider/model mismatch.');
assert(auth.runInitialisationUtc===REQUIRED_RUN,'authorization run mismatch.');
assert(auth.location?.classification==='SYNTHETIC_GENERALIZED'&&auth.location?.latitudeDeg===42&&auth.location?.longitudeDeg===12,'authorization location mismatch.');
assert(auth.location?.siteAuthorityRef==='SITE-PUBLIC-SYNTHETIC-FORECAST-IT-01'&&auth.protectedSiteUsed===false,'protected-site use is forbidden.');
assert(auth.recurringTraffic===false&&auth.productionUse===false,'recurring or production traffic is forbidden.');
const runMs=Date.parse(REQUIRED_RUN); const now=Date.now(); const ageHours=(now-runMs)/3_600_000;
assert(runMs<=now && ageHours<=18,'authorized run is stale or in the future.');

const url=new URL('https://single-runs-api.open-meteo.com/v1/forecast');
for(const [key,value] of Object.entries({latitude:'42.0',longitude:'12.0',hourly:VARS.join(','),models:'italia_meteo_arpae_icon_2i',run:REQUIRED_RUN.slice(0,-1),timezone:'GMT',timeformat:'iso8601',cell_selection:'land',elevation:'nan',forecast_hours:'72'})) url.searchParams.set(key,value);
const plan={gateId:'BKL031-F7-ONE-FRESH-FORECAST-VALIDATION-REQUEST-001',authorizationId:AUTH_ID,expectedHost:'single-runs-api.open-meteo.com',method:'GET',redirects:'DENY',maxRequestsThisGate:1,timeoutMs:10000,maxResponseBytes:2000000,location:auth.location,providerId:'OPEN_METEO',upstreamAuthorityId:'ITALIAMETEO_ARPAE',modelId:'italia_meteo_arpae_icon_2i',runInitialisationUtc:REQUIRED_RUN,variables:VARS,protectedSiteUsed:false,recurringTraffic:false,productionUse:false};
assert(url.hostname===plan.expectedHost,'request host mismatch.');
if(args.preflight){ console.log(JSON.stringify(plan,null,2)); process.exit(0); }
assert(args.execute && args.confirm==='F7_ONE_VALIDATION_REQUEST','execution requires exact F7 confirmation.');
const out=path.resolve(String(args.out ?? 'work/f7-evidence')); fs.mkdirSync(out,{recursive:true});
fs.writeFileSync(path.join(out,'request-plan.json'),JSON.stringify(plan,null,2)+'\n');
const failure=(details)=>fs.writeFileSync(path.join(out,'failure-summary.json'),JSON.stringify({gateId:plan.gateId,authorizationId:AUTH_ID,requestCountThisGate:1,budgetState:'1/1_EXHAUSTED',...details},null,2)+'\n');
const controller=new AbortController(); const timer=setTimeout(()=>controller.abort(),plan.timeoutMs); let response;
try { response=await fetch(url,{method:'GET',redirect:'manual',headers:{accept:'application/json','user-agent':'digital-stargate-bkl031-f7/1.0'},signal:controller.signal}); }
catch(error){ clearTimeout(timer); failure({failureClass:'TRANSPORT',errorName:error?.name??'Error',errorMessage:error?.message??'unknown'}); throw error; }
if(response.status>=300&&response.status<400){ clearTimeout(timer); failure({failureClass:'REDIRECT_DENIED',httpStatus:response.status}); await response.body?.cancel().catch(()=>undefined); throw new Error('redirect denied.'); }
const chunks=[]; let byteLength=0; const declared=Number(response.headers.get('content-length'));
if(Number.isFinite(declared)&&declared>plan.maxResponseBytes){ clearTimeout(timer); failure({failureClass:'RESPONSE_TOO_LARGE',declaredByteLength:declared}); await response.body?.cancel().catch(()=>undefined); throw new Error('response too large.'); }
try { const reader=response.body?.getReader(); assert(reader,'provider response body unavailable.'); while(true){ const {done,value}=await reader.read(); if(done) break; byteLength+=value.byteLength; if(byteLength>plan.maxResponseBytes){ failure({failureClass:'RESPONSE_TOO_LARGE',observedByteLength:byteLength}); controller.abort(); await reader.cancel().catch(()=>undefined); throw new Error('response too large.'); } chunks.push(value); } } finally { clearTimeout(timer); }
const bytes=new Uint8Array(byteLength); let offset=0; for(const chunk of chunks){ bytes.set(chunk,offset); offset+=chunk.byteLength; }
const rawSha256=crypto.createHash('sha256').update(bytes).digest('hex'); fs.writeFileSync(path.join(out,'raw-response.json'),bytes);
if(response.status!==200){ failure({failureClass:'PROVIDER_HTTP',httpStatus:response.status,rawSha256,byteLength}); throw new Error(`provider HTTP ${response.status}.`); }
let raw; try { raw=JSON.parse(new TextDecoder().decode(bytes)); } catch { failure({failureClass:'INVALID_JSON',rawSha256,byteLength}); throw new Error('provider response is not JSON.'); }
if(raw.error){ failure({failureClass:'PROVIDER_ERROR',rawSha256,byteLength,providerReason:raw.reason??'unknown'}); throw new Error(`provider error: ${raw.reason??'unknown'}`); }
assert(raw.timezone==='GMT'&&raw.utc_offset_seconds===0,'provider timezone mismatch.');
assert(raw.hourly&&Array.isArray(raw.hourly.time)&&raw.hourly.time.length>=1&&raw.hourly.time.length<=72,'hourly time array outside bounds.');
for(const variable of VARS) assert(Array.isArray(raw.hourly[variable])&&raw.hourly[variable].length===raw.hourly.time.length,`${variable} array mismatch.`);
const retrievedAtUtc=new Date().toISOString(); const retrievedMs=Date.parse(retrievedAtUtc); const accepted=[]; const excluded=[];
for(let i=0;i<raw.hourly.time.length;i++){ const values={}; const missing=[]; for(const variable of VARS){ const value=raw.hourly[variable][i]; if(typeof value!=='number'||!Number.isFinite(value)) missing.push(variable); else values[variable]=value; } const instantUtc=raw.hourly.time[i].endsWith('Z')?raw.hourly.time[i]:raw.hourly.time[i]+'Z'; if(missing.length) excluded.push({instantUtc,reason:'MISSING_OR_NON_FINITE_GOVERNED_VARIABLE',variables:missing}); else accepted.push({instantUtc,values}); }
const futureAcceptedInstantCount=accepted.filter(x=>Date.parse(x.instantUtc)>=retrievedMs).length;
const runAgeHoursAtRetrieval=(retrievedMs-runMs)/3_600_000; const freshnessState=runAgeHoursAtRetrieval<=18?'FRESH':'STALE';
const availabilityState=accepted.length===0||futureAcceptedInstantCount===0?'UNAVAILABLE':excluded.length?'DEGRADED':'AVAILABLE';
const supply={schemaVersion:'1.0',contractType:'BKL031_F7_FORECAST_RUNTIME_SUPPLY',supplyId:`BKL031-F7-SUPPLY-${process.env.GITHUB_RUN_ID??'LOCAL'}`,environment:'EVALUATION',authority:'NONE',authorizationId:AUTH_ID,providerId:'OPEN_METEO',upstreamAuthorityId:'ITALIAMETEO_ARPAE',modelId:'italia_meteo_arpae_icon_2i',runInitialisationUtc:REQUIRED_RUN,retrievedAtUtc,rawSha256,responseByteLength:byteLength,location:{classification:'SYNTHETIC_GENERALIZED',siteAuthorityRef:'SITE-PUBLIC-SYNTHETIC-FORECAST-IT-01',protectedSiteUsed:false},freshness:{maxRunAgeHours:18,runAgeHoursAtRetrieval:Number(runAgeHoursAtRetrieval.toFixed(6)),state:freshnessState},requestAccounting:{maxProviderRequests:1,requestOrdinal:1,budgetState:'1/1_EXHAUSTED'},series:{rawInstantCount:raw.hourly.time.length,acceptedInstantCount:accepted.length,excludedInstantCount:excluded.length,futureAcceptedInstantCount,imputedValueCount:0,units:raw.hourly_units??{},accepted,excluded},availabilityState,boundaries:{recurringTraffic:false,productionRuntimeActivated:false,readinessAuthority:false,schedulingAuthority:false,automaticTargetSelection:false,commandAuthority:'NONE',safetyAuthority:'LOCAL_PHYSICAL_INTERLOCKS'}};
fs.writeFileSync(path.join(out,'normalized-supply.json'),JSON.stringify(supply,null,2)+'\n');
fs.writeFileSync(path.join(out,'summary.json'),JSON.stringify({gateId:plan.gateId,authorizationId:AUTH_ID,requestCountThisGate:1,budgetState:'1/1_EXHAUSTED',rawSha256,byteLength,runInitialisationUtc:REQUIRED_RUN,retrievedAtUtc,availabilityState,rawInstantCount:supply.series.rawInstantCount,acceptedInstantCount:supply.series.acceptedInstantCount,excludedInstantCount:supply.series.excludedInstantCount,futureAcceptedInstantCount,protectedSiteUsed:false},null,2)+'\n');
if(freshnessState!=='FRESH'||availabilityState==='UNAVAILABLE'){ failure({failureClass:'SUPPLY_NOT_FRESH_OR_AVAILABLE',rawSha256,byteLength,freshnessState,availabilityState,futureAcceptedInstantCount}); throw new Error('fresh forecast supply unavailable.'); }
console.log(JSON.stringify({rawSha256,byteLength,availabilityState,acceptedInstantCount:accepted.length,excludedInstantCount:excluded.length,futureAcceptedInstantCount,out},null,2));
