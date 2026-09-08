import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const projectionPath = process.env.DSG_NIGHT_TIMELINE_REPLAY || path.join(root, 'docs/data/night-timeline-replay.json');
const doc = JSON.parse(fs.readFileSync(projectionPath, 'utf8'));
const fail = m => { throw new Error(`Night Timeline Replay validation FAILED: ${m}`); };
const order = {NINA:10,PHD2:20,CLOUDWATCHER:30,SQM:40,EAGLE_HEALTH:50,SESSION_PROJECTION:90};
if (doc.authority !== 'projection') fail('authority must remain projection');
if (doc.baseline_commit !== '4a4d6b89b374e87ca7f945e7399b7e69f0c9ba87') fail('baseline_commit must bind accepted BKL-040 F1 merge');
if (doc.source_order_method_id !== 'BKL040-F1-SOURCE-ORDER-1') fail('source order method changed');
if (doc.sessions.length > doc.bounds.max_sessions) fail('session bound exceeded');
const citations = new Set(doc.citations.map(x => `${x.id}@${x.version}`));
const provenance = new Map(doc.provenance_records.map(x => [`${x.id}@${x.version}`, x]));
let count = 0;
for (const s of doc.sessions) {
  if (!fs.existsSync(path.join(root, s.source_ref))) fail(`missing session source ${s.source_ref}`);
  for (const e of s.events) {
    count++;
    if (e.source_order !== order[e.source_type]) fail(`${e.replay_event_id}: source_order mismatch`);
    if (e.temporal_state === 'PLACED') {
      if (!e.event_time_utc || !e.source_timestamp_raw) fail(`${e.replay_event_id}: placed event missing timestamp evidence`);
      if (Number.isNaN(Date.parse(e.event_time_utc)) || Number.isNaN(Date.parse(e.source_timestamp_raw))) fail(`${e.replay_event_id}: invalid timestamp`);
      if (new Date(e.event_time_utc).getTime() !== new Date(e.source_timestamp_raw).getTime()) fail(`${e.replay_event_id}: UTC normalization does not preserve source instant`);
    } else if (e.event_time_utc !== null || e.source_timestamp_raw !== null) fail(`${e.replay_event_id}: UNPLACED must not carry invented timestamps`);
    for (const r of e.citation_refs) if (!citations.has(r)) fail(`${e.replay_event_id}: unresolved citation ${r}`);
    for (const r of e.provenance_refs) {
      const p = provenance.get(r); if (!p) fail(`${e.replay_event_id}: unresolved provenance ${r}`);
      if (p.output_ref !== `replay-event:${e.replay_event_id}`) fail(`${e.replay_event_id}: provenance output mismatch`);
      for (const c of p.citation_refs) if (!e.citation_refs.includes(c)) fail(`${e.replay_event_id}: provenance citation not preserved`);
    }
    if (e.source_type === 'SESSION_PROJECTION') {
      const [file, fragment] = e.source_ref.split('#');
      const src = JSON.parse(fs.readFileSync(path.join(root, file), 'utf8'));
      const field = fragment === 'start_local' ? 'start_local' : fragment === 'end_local' ? 'end_local' : null;
      if (!field) fail(`${e.replay_event_id}: unsupported session projection locator`);
      if (src[field] !== e.source_timestamp_raw) fail(`${e.replay_event_id}: timestamp not exact source evidence`);
    }
  }
}
if (count > doc.bounds.max_events) fail('event bound exceeded');
console.log(`Night Timeline Replay validation PASS: sessions=${doc.sessions.length} events=${count}`);
