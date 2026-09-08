import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const sessionId = '2026-08-15_2026-08-16';
const base = `data/sessions/2026/08/${sessionId}`;
const manifestPath = path.join(root, base, 'manifest.json');
const ninaRel = `${base}/raw/nina/20260815-204018-3.2.0.9001.6188-202608.log`;
const phdRel = `${base}/raw/phd2/PHD2_GuideLog_2026-08-15_203750.txt`;
const cwRel = `${base}/raw/weather/CloudWatcher_2026-08-15_2026-08-16.csv`;
const read = p => fs.readFileSync(path.join(root, p), 'utf8').replace(/^\uFEFF/, '');
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8').replace(/^\uFEFF/, ''));
if (manifest.timezone_id !== 'Europe/Rome') throw new Error(`Unsupported governed timezone ${manifest.timezone_id}`);

function partsAt(ms, zone) {
  const parts = new Intl.DateTimeFormat('en-CA',{timeZone:zone,year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',second:'2-digit',hourCycle:'h23'}).formatToParts(new Date(ms));
  return Object.fromEntries(parts.filter(x=>x.type!=='literal').map(x=>[x.type,Number(x.value)]));
}
function localToUtc(local, zone) {
  const m = /^(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2}):(\d{2})(?:\.(\d+))?$/.exec(local);
  if (!m) throw new Error(`Invalid local timestamp ${local}`);
  const naiveSecond = Date.UTC(+m[1],+m[2]-1,+m[3],+m[4],+m[5],+m[6],0);
  let guess = naiveSecond;
  for (let i=0;i<3;i++) {
    const p=partsAt(guess,zone);
    const represented=Date.UTC(p.year,p.month-1,p.day,p.hour,p.minute,p.second,0);
    guess -= represented - naiveSecond;
  }
  const isoSecond = new Date(guess).toISOString().replace('.000Z','');
  return `${isoSecond}${m[7] ? `.${m[7]}` : ''}Z`;
}
function epochMicros(utc) {
  const m=/^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})(?:\.(\d+))?Z$/.exec(utc);
  if (!m) throw new Error(`Invalid canonical UTC ${utc}`);
  const sec=BigInt(Date.parse(`${m[1]}Z`))*1000n;
  const micro=BigInt((m[2]??'').padEnd(6,'0').slice(0,6));
  return sec+micro;
}
function deltaMs(left,right){return Number(epochMicros(right)-epochMicros(left))/1000;}
function ref(id){return `${id}@1.0`;}
function citation(id, authority, p, pointer){return {id,version:'1.0',source_authority:authority,locator:{path:p,json_pointer:pointer}};}
function provenance(id, method, input, eventId, citationId){return {id,version:'1.0',method_id:method,input_refs:[input],output_ref:`replay-event:${eventId}`,citation_refs:[ref(citationId)]};}

const nina = read(ninaRel);
const ninaLine = nina.split(/\r?\n/).find(x => /^2026-08-15T\d{2}:\d{2}:\d+(?:\.\d+)?\|/.test(x) && x.includes('|DomeVM.cs|OpenShutter|') && x.includes('Opening dome shutter.'));
if (!ninaLine) throw new Error('Bounded NINA dome-open evidence not found');
const ninaLocal = ninaLine.split('|',1)[0];
const phd = read(phdRel);
const phdMatch = /^Guiding Begins at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})$/m.exec(phd);
if (!phdMatch) throw new Error('Bounded PHD2 guiding anchor not found');
const phdLocal = phdMatch[1];
const cw = read(cwRel);
const cwLines = cw.split(/\r?\n/).filter(Boolean);
if (!cwLines[0].includes('"Date"') || cwLines.length < 2) throw new Error('CloudWatcher header/data not found');
const fields = [...cwLines[1].matchAll(/"([^"]*)"/g)].map(x=>x[1]);
if (fields.length < 17) throw new Error('CloudWatcher first row malformed');
const cwLocal = `${fields[0]} ${fields[1]}`;

const events = [
  {replay_event_id:'RPL-20260815-CLOUDWATCHER-FIRST',temporal_state:'PLACED',event_time_utc:localToUtc(cwLocal,manifest.timezone_id),source_timestamp_raw:cwLocal,source_type:'CLOUDWATCHER',source_order:30,source_authority:'CloudWatcher CSV historical evidence',event_kind:'WEATHER_SAMPLE',summary:`CloudWatcher ${fields[2]}/${fields[3]} safety=${fields[16]}`,source_ref:`${cwRel}#row=2`,citation_refs:[ref('CIT-RPL-F3-CW-FIRST')],provenance_refs:[ref('PRV-RPL-F3-CW-FIRST')],quality_state:'CURRENT'},
  {replay_event_id:'RPL-20260815-NINA-DOME-OPEN',temporal_state:'PLACED',event_time_utc:localToUtc(ninaLocal,manifest.timezone_id),source_timestamp_raw:ninaLocal,source_type:'NINA',source_order:10,source_authority:'N.I.N.A. raw log evidence',event_kind:'DOME_OPEN_REQUEST',summary:'N.I.N.A. recorded opening dome shutter request',source_ref:`${ninaRel}#contains=Opening%20dome%20shutter`,citation_refs:[ref('CIT-RPL-F3-NINA-DOME-OPEN')],provenance_refs:[ref('PRV-RPL-F3-NINA-DOME-OPEN')],quality_state:'CURRENT'},
  {replay_event_id:'RPL-20260815-PHD2-GUIDING-BEGIN',temporal_state:'PLACED',event_time_utc:localToUtc(phdLocal,manifest.timezone_id),source_timestamp_raw:phdLocal,source_type:'PHD2',source_order:20,source_authority:'PHD2 GuideLog historical evidence',event_kind:'GUIDING_BEGIN',summary:'PHD2 guiding section begins',source_ref:`${phdRel}#contains=Guiding%20Begins%20at`,citation_refs:[ref('CIT-RPL-F3-PHD2-GUIDING-BEGIN')],provenance_refs:[ref('PRV-RPL-F3-PHD2-GUIDING-BEGIN')],quality_state:'CURRENT'}
].sort((a,b)=>epochMicros(a.event_time_utc)<epochMicros(b.event_time_utc)?-1:epochMicros(a.event_time_utc)>epochMicros(b.event_time_utc)?1:a.source_order-b.source_order||a.replay_event_id.localeCompare(b.replay_event_id));
const citations = [citation('CIT-RPL-F3-CW-FIRST','CloudWatcher CSV historical evidence',cwRel,'/row/2'),citation('CIT-RPL-F3-NINA-DOME-OPEN','N.I.N.A. raw log evidence',ninaRel,'/line/contains:Opening dome shutter'),citation('CIT-RPL-F3-PHD2-GUIDING-BEGIN','PHD2 GuideLog historical evidence',phdRel,'/line/contains:Guiding Begins at')];
const provenanceRecords = [provenance('PRV-RPL-F3-CW-FIRST','BKL040-F3-CLOUDWATCHER-LOCAL-TO-UTC-1',`${cwRel}#/row/2`,'RPL-20260815-CLOUDWATCHER-FIRST','CIT-RPL-F3-CW-FIRST'),provenance('PRV-RPL-F3-NINA-DOME-OPEN','BKL040-F3-NINA-LOCAL-TO-UTC-1',`${ninaRel}#/line/contains:Opening dome shutter`,'RPL-20260815-NINA-DOME-OPEN','CIT-RPL-F3-NINA-DOME-OPEN'),provenance('PRV-RPL-F3-PHD2-GUIDING-BEGIN','BKL040-F3-PHD2-GUIDE-ANCHOR-1',`${phdRel}#/line/contains:Guiding Begins at`,'RPL-20260815-PHD2-GUIDING-BEGIN','CIT-RPL-F3-PHD2-GUIDING-BEGIN')];
const byId = Object.fromEntries(events.map(e=>[e.replay_event_id,e]));
function corr(id,left,right){const l=byId[left],r=byId[right];return {correlation_id:id,session_id:sessionId,left_event_ref:`replay-event:${left}`,right_event_ref:`replay-event:${right}`,relationship_type:'SEQUENTIAL',delta_ms:deltaMs(l.event_time_utc,r.event_time_utc),classification_method_id:'BKL040-F3-EXACT-DELTA-1',classification_state:'NOT_ASSESSED',citation_refs:[...l.citation_refs,...r.citation_refs],provenance_refs:[...l.provenance_refs,...r.provenance_refs],conflict_refs:[]};}
const correlations=[corr('CORR-F3-CW-NINA','RPL-20260815-CLOUDWATCHER-FIRST','RPL-20260815-NINA-DOME-OPEN'),corr('CORR-F3-NINA-PHD2','RPL-20260815-NINA-DOME-OPEN','RPL-20260815-PHD2-GUIDING-BEGIN')];
const output={schema_version:'1.0',component:'DSG.NightTimelineReplay.F3',authority:'projection',baseline_commit:'ba17df5584a82c4396bd7dccf6bf593c518d8429',session_id:sessionId,timezone_id:manifest.timezone_id,source_order_method_id:'BKL040-F1-SOURCE-ORDER-1',bounds:{max_events:6,max_correlations:6},events,citations,provenance_records:provenanceRecords,correlations};
process.stdout.write(JSON.stringify(output,null,2)+'\n');
