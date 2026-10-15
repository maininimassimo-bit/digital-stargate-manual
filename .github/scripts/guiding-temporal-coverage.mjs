import { createHash } from 'node:crypto';
import { parseCsvRecord } from './phd2-guiding.mjs';

export const METHOD = 'DSG-GUIDING-LIGHT-TEMPORAL-1.0';
// A continuity bound, not a guiding-quality threshold. No extrapolated tails.
export const MAX_GAP_EXPOSURES = 3;
const stamp = value => {
  if (!/^\d{4}-\d\d-\d\d[T ]\d\d:\d\d:\d\d(?:\.\d+)?$/.test(value)) return NaN;
  // Treat both logs as the same local wall clock, never as an asserted UTC instant.
  return Date.parse(value.replace(' ', 'T').replace(/(\.\d{3})\d+$/, '$1') + 'Z');
};
const union = intervals => {
  const out = [];
  for (const [a,b] of intervals.sort((x,y)=>x[0]-y[0])) {
    if (!(b>a)) continue;
    if (out.length && a<=out.at(-1)[1]) out.at(-1)[1]=Math.max(b,out.at(-1)[1]);
    else out.push([a,b]);
  }
  return out;
};
const duration = intervals => intervals.reduce((s,[a,b])=>s+b-a,0)/1000;
const ref = source => ({path:source.path.replaceAll('\\','/'),sha256:createHash('sha256').update(source.bytes ?? source.text).digest('hex')});

export function buildGuidingTemporalCoverage(ninaSources, guideSources, expectedLightStarts = null) {
  const sourceRefs=[...ninaSources,...guideSources].map(ref);
  const unavailable = reason => ({methodVersion:METHOD,state:'UNAVAILABLE',reason,coverage:null,lightSeconds:null,coveredSeconds:null,clockBasis:'NOT_VERIFIED',maxGapExposures:MAX_GAP_EXPOSURES,sourceRefs});
  if ([...ninaSources,...guideSources].some(s=>s.bytes && !Buffer.from(s.text,'utf8').equals(s.bytes))) return unavailable('INVALID_SOURCE_ENCODING');
  const lights=[];
  let starts=0;
  for (const source of ninaSources) {
    // A remote/unknown PHD2 clock cannot be silently aligned by overlapping dates.
    const hosts=[...source.text.matchAll(/Connecting to PHD2 server at ([^\s:]+):\d+/g)].map(m=>m[1]);
    if (!hosts.length || hosts.some(host=>!['127.0.0.1','localhost'].includes(host))) return unavailable('SHARED_CLOCK_NOT_EVIDENCED');
    let active=null, lastTime=-Infinity;
    for (const line of source.text.split(/\r?\n/)) {
      const t=stamp(line.split('|')[0]);
      if (Number.isFinite(t)) {if(t<lastTime)return unavailable('NON_MONOTONIC_NINA_CLOCK');lastTime=t;}
      if (line.includes('SequenceItem.cs|Run|') && line.includes('Starting Category:') && line.includes('Item: TakeExposure')) {
        if (active) return unavailable('UNPAIRED_LIGHT_EXPOSURE');
        if (/ImageType LIGHT\b/.test(line)) {starts++;active={start:t,capture:null,seconds:Number(line.match(/ExposureTime ([\d.]+)/)?.[1])};}
      }
      if (active && line.includes('CameraVM.cs|Capture|') && line.includes('Starting Exposure -')) {
        if (active.capture!==null) return unavailable('AMBIGUOUS_LIGHT_CAPTURE');
        active.capture=t;
      }
      if (active && line.includes('SequenceItem.cs|Run|') && line.includes('Finishing Category:') && line.includes('Item: TakeExposure')) {
        if (!/ImageType LIGHT\b/.test(line) || !Number.isFinite(active.start) || !Number.isFinite(active.capture) || !Number.isFinite(t) || !(active.seconds>0) || active.capture<active.start || active.capture+active.seconds*1000>t) return unavailable('INVALID_LIGHT_INTERVAL');
        lights.push([active.capture,active.capture+active.seconds*1000]);active=null;
      }
    }
    if (active) return unavailable('UNPAIRED_LIGHT_EXPOSURE');
  }
  if (!starts) return unavailable('LIGHT_TIMESTAMPS_NOT_AVAILABLE');
  if (expectedLightStarts!==null && starts!==expectedLightStarts) return unavailable('LIGHT_COUNT_MISMATCH');
  const intervals=[];
  for (const source of guideSources) {
    let anchor=NaN, lastAnchor=-Infinity, exposure=NaN, previous=null, settling=false, paused=false, lastElapsed=-1;
    for (const line of source.text.split(/\r?\n/)) {
      if (line.startsWith('Guiding Begins at ')) {anchor=stamp(line.slice(18));if(!Number.isFinite(anchor)||anchor<lastAnchor)return unavailable('NON_MONOTONIC_GUIDE_CLOCK');lastAnchor=anchor;exposure=NaN;previous=null;settling=false;paused=false;lastElapsed=-1;continue;}
      if (line.startsWith('Guiding Ends at ')) {anchor=NaN;previous=null;continue;}
      const exposureChange=line.match(/(?:^Exposure = |Guiding parameter change, Exposure = )([\d.]+) ms$/);
      if (exposureChange) {exposure=Number(exposureChange[1]);previous=null;}
      if (/settling started/i.test(line)) {settling=true;previous=null;continue;}
      if (/settling complete/i.test(line)) {settling=false;previous=null;continue;}
      if (/resum|guiding enabled/i.test(line)) {paused=false;previous=null;continue;}
      if (/pause|guiding disabled/i.test(line)) {paused=true;previous=null;continue;}
      if (!/^\d+,/.test(line)) continue;
      const row=parseCsvRecord(line), elapsed=Number(row[1]);
      if (Number.isFinite(anchor) && (!Number.isFinite(elapsed) || elapsed<0 || elapsed<=lastElapsed)) return unavailable('NON_MONOTONIC_GUIDE_CLOCK');
      lastElapsed=elapsed;
      const valid=Number.isFinite(anchor)&&exposure>0&&!settling&&!paused&&row.length===18&&row[2]==='Mount'&&row[17].trim()==='0'&&row.slice(7,9).every(v=>v.trim()!==''&&Number.isFinite(Number(v)));
      if (!valid) {previous=null;continue;}
      const current=anchor+elapsed*1000;
      if (previous!==null && current-previous<=MAX_GAP_EXPOSURES*exposure) intervals.push([previous,current]);
      previous=current;
    }
  }
  const guide=union(intervals);
  if (!guide.length) return unavailable('VALID_GUIDE_TIMESTAMPS_NOT_AVAILABLE');
  const light=union(lights), intersections=[];
  for (const [a,b] of light) for (const [c,d] of guide) if (Math.min(b,d)>Math.max(a,c)) intersections.push([Math.max(a,c),Math.min(b,d)]);
  const lightSeconds=duration(light), coveredSeconds=duration(union(intersections));
  return {methodVersion:METHOD,state:'AVAILABLE',reason:null,coverage:Math.round(coveredSeconds/lightSeconds*1e6)/1e6,lightSeconds,coveredSeconds:Math.round(coveredSeconds*1000)/1000,lightExposureCount:starts,clockBasis:'SHARED_LOCAL_WALL_CLOCK',maxGapExposures:MAX_GAP_EXPOSURES,sourceRefs};
}
