import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { projectAnomalyTrend } from './anomaly-trend-engine.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const replayPath = path.join(root, 'docs/data/night-timeline-replay-f3.json');
const outputPath = path.join(root, 'docs/data/anomaly-trend-read-model.json');
export const F3B_ACCEPTED_MERGE = '615d46726c3998421bf04f9d6cc8cd8234023b62';
const read = p => JSON.parse(fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, ''));

export function buildAnomalyTrendReadModel(replay) {
  const projection = projectAnomalyTrend(replay);
  const count = type => projection.records.filter(record => record.semantic_type === type).length;
  return {
    schema_version: '1.0', component: 'DSG.AnomalyTrendCenter.F4ReadModel', authority: 'projection', action_authority: 'NONE',
    baseline_commit: F3B_ACCEPTED_MERGE, upstream_component: projection.component, upstream_method_version: projection.method_version,
    source_component: projection.source_component, source_baseline_commit: projection.source_baseline_commit, session_id: projection.session_id,
    interaction_mode: 'READ_ONLY', advisory_mode: 'DESCRIPTIVE_ONLY', safety_authority: 'UNCHANGED_LOCAL_AUTHORITY', command_actions: [],
    summary: { total_records: projection.records.length, observations: count('OBSERVATION'), trend_measurements: count('TREND_MEASUREMENT'), anomaly_candidates: count('ANOMALY_CANDIDATE'), correlation_candidates: count('CORRELATION_CANDIDATE'), recommendations: count('RECOMMENDATION') },
    source_drilldown: { enabled: true, fields: ['source_record_refs', 'citation_refs', 'provenance_refs'] },
    records: projection.records,
    limitations: ['HISTORICAL_PROJECTION_NOT_CURRENT_SAFETY_STATE','NO_ANOMALY_THRESHOLD_AUTHORIZED','CORRELATION_DOES_NOT_IMPLY_CAUSATION','NO_COMMAND_OR_REMEDIATION_AUTHORITY','BKL030_EAGLE_HISTORY_NOT_ONBOARDED']
  };
}

const replay = read(replayPath);
const projection = buildAnomalyTrendReadModel(replay);
if (process.argv.includes('--write')) {
  fs.writeFileSync(outputPath, `${JSON.stringify(projection, null, 2)}\n`, 'utf8');
  console.log(`BKL-038 F4 read model written: ${path.relative(root, outputPath)}`);
} else if (process.argv.includes('--check')) {
  let current;
  try { current = read(outputPath); } catch { current = null; }
  if (!current || JSON.stringify(current) !== JSON.stringify(projection)) {
    console.error('BKL-038 F4 read model drift detected. Run: node .github/scripts/generate-anomaly-trend-read-model.mjs --write');
    process.exit(1);
  }
  console.log(`BKL-038 F4 read model OK: records=${projection.summary.total_records} anomalies=${projection.summary.anomaly_candidates} authority=${projection.authority}`);
}
