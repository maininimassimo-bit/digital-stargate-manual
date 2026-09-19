import fs from 'node:fs';

const inputPath = 'docs/data/bkl-036-f3-archived-evidence-input.json';
const outputPath = 'docs/data/bkl-036-f3-health-score.json';
const domains = ['weather','dome','mount','camera','power','network','eagle_health'];
const comparableStatuses = new Set(['PRESENT']);

function read(path) { return JSON.parse(fs.readFileSync(path, 'utf8')); }
function project(input) {
  if (input.live_data_used !== false) throw new Error('F3 input must be archived repository evidence only.');
  if (input.evidence.length !== domains.length || new Set(input.evidence.map(x=>x.domain)).size !== domains.length) throw new Error('F3 input must contain exactly seven unique domains.');
  const evidence = domains.map(domain => input.evidence.find(x => x.domain === domain));
  const allComparable = evidence.every(x => comparableStatuses.has(x.evidence_status) && x.compatibility === 'COMPARABLE' && x.freshness_state === 'CURRENT');
  const scoreStatus = allComparable ? 'AVAILABLE' : 'UNAVAILABLE';
  return {
    schema_version: '1.0', contract_id: 'DSG.BKL036.F3.HealthScore', projection_kind: 'repository_archived_evidence',
    source_plane: 'repository_evidence', live_data_used: false, scale: '0-100', domain_count: 7,
    policy: {equal_weight:true, comparable_domain_value:100, incomplete_result:'UNAVAILABLE', readiness_authority:'BKL-032', safety_authority:'LOCAL_PHYSICAL_INTERLOCKS'},
    score_status: scoreStatus, score: allComparable ? 100 : null, evaluated_at_utc: input.evaluated_at_utc,
    reasons: allComparable ? ['ALL_MANDATORY_DOMAINS_COMPARABLE','EQUAL_WEIGHT_BINARY_COMPARABILITY_SCORE','NOT_LIVE_AND_NOT_REAL_TIME'] : ['BKL036_F3_ARCHIVED_EVIDENCE_ONLY','ONE_OR_MORE_MANDATORY_DOMAINS_NOT_COMPARABLE','NO_PARTIAL_SCORE_ALLOWED','NOT_LIVE_AND_NOT_REAL_TIME'],
    evidence,
    publication: {target:'public_digital_stargate_portal', read_only:true, non_live_label:'repository evidence / non-live / non-real-time', timestamp_label:true, source_label:true}
  };
}
const actual = project(read(inputPath));
if (process.argv.includes('--write')) fs.writeFileSync(outputPath, JSON.stringify(actual, null, 2) + '\n');
else if (JSON.stringify(actual) !== JSON.stringify(read(outputPath))) throw new Error('F3 health score projection is stale; run with --write.');
console.log(`BKL-036-F3 health score projection ${process.argv.includes('--write') ? 'written' : 'matches'}: ${actual.score_status}`);
