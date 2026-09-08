import fs from 'node:fs';
const read=p=>JSON.parse(fs.readFileSync(p,'utf8').replace(/^\uFEFF/,''));
const key=x=>JSON.stringify(x);
export function validateNightTimelineReadModel(rm,f3){
 const e=[];
 if(rm.schema_version!=='1.0')e.push('schema_version must be 1.0');
 if(rm.component!=='DSG.NightTimelineReadModel')e.push('component mismatch');
 if(rm.authority!=='projection')e.push('authority must remain projection');
 if(rm.baseline_commit!=='7dc867c50ee588d46f4e23e2880d10373f3fbbc5')e.push('baseline_commit must bind accepted F3 merge');
 if(rm.upstream_component!==f3.component)e.push('upstream_component mismatch');
 if(rm.session_id!==f3.session_id)e.push('session_id mismatch');
 if(rm.timezone_id!==f3.timezone_id)e.push('timezone_id mismatch');
 if(rm.interaction_mode!=='READ_ONLY')e.push('interaction_mode must be READ_ONLY');
 if(rm.playback_mode!=='VISUAL_ONLY')e.push('playback_mode must be VISUAL_ONLY');
 if(rm.safety_authority!=='UNCHANGED_LOCAL_AUTHORITY')e.push('safety_authority changed');
 if(!Array.isArray(rm.command_actions)||rm.command_actions.length)e.push('command_actions must be empty');
 if(!rm.bounds||rm.bounds.max_events!==f3.bounds.max_events||rm.bounds.max_correlations!==f3.bounds.max_correlations)e.push('bounds mismatch');
 if(!Array.isArray(rm.timeline)||rm.timeline.length!==f3.events.length)e.push('timeline event count mismatch');
 const fields=['replay_event_id','event_time_utc','source_timestamp_raw','source_type','source_order','source_authority','event_kind','summary','quality_state','citation_refs','provenance_refs'];
 for(let i=0;i<f3.events.length;i++){const a=rm.timeline?.[i],b=f3.events[i];if(!a)continue;for(const f of fields)if(key(a[f])!==key(b[f]))e.push(`timeline[${i}].${f} does not preserve F3`);}
 const upstreamUnplaced=f3.events.filter(x=>x.temporal_state==='UNPLACED');
 if(!Array.isArray(rm.unplaced_events))e.push('unplaced_events must be explicit array');
 else if(upstreamUnplaced.length===0&&rm.unplaced_events.length!==0)e.push('unplaced_events cannot invent evidence absent from accepted F3');
 if(!Array.isArray(rm.conflicts))e.push('conflicts must be explicit array');
 else {const upstreamConflictRefs=[...new Set((f3.correlations??[]).flatMap(x=>x.conflict_refs??[]))];if(upstreamConflictRefs.length===0&&rm.conflicts.length!==0)e.push('conflicts cannot invent evidence absent from accepted F3');}
 if(!Array.isArray(rm.correlations)||rm.correlations.length!==f3.correlations.length)e.push('correlation count mismatch');
 const cf=['correlation_id','left_event_ref','right_event_ref','relationship_type','delta_ms','classification_method_id','classification_state','citation_refs','provenance_refs','conflict_refs'];
 for(let i=0;i<f3.correlations.length;i++){const a=rm.correlations?.[i],b=f3.correlations[i];if(!a)continue;for(const f of cf)if(key(a[f])!==key(b[f]))e.push(`correlations[${i}].${f} does not preserve F3`);if(a.classification_state!=='NOT_ASSESSED')e.push(`correlations[${i}] skew classification promoted`);}
 return e;
}
if(process.argv[1]&&process.argv[1].endsWith('verify-night-timeline-read-model.mjs')){const rm=read('docs/data/night-timeline-read-model.json'),f3=read('docs/data/night-timeline-replay-f3.json'),errors=validateNightTimelineReadModel(rm,f3);if(errors.length){console.error(errors.join('\n'));process.exit(1);}console.log(`BKL-040 F4 read model OK: events=${rm.timeline.length} correlations=${rm.correlations.length} authority=${rm.authority} mode=${rm.interaction_mode}`);}
