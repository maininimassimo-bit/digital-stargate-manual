import fs from 'node:fs';
import assert from 'node:assert/strict';

const DOMAINS = ['weather', 'dome', 'mount', 'camera', 'power', 'network', 'eagle_health'];
const score = JSON.parse(fs.readFileSync('docs/data/bkl-036-f5-live-health-score-fixture.json', 'utf8'));

assert.equal(score.schema_version, '1.0');
assert.equal(score.contract_id, 'DSG.BKL036.F5.LiveHealthScore');
assert.equal(score.projection_kind, 'live_read_only_descriptive');
assert.equal(score.source_plane, 'live_read_only_transport');
assert.equal(score.domain_count, 7);
assert.deepEqual(score.domains.map(item => item.domain), DOMAINS);
assert.equal(new Set(score.domains.map(item => item.domain)).size, 7);
assert.equal(score.policy.complete_set_required, true);
assert.equal(score.policy.incomplete_result, 'UNAVAILABLE');
assert.equal(score.policy.readiness_authority, 'BKL-032');
assert.equal(score.policy.safety_authority, 'LOCAL_PHYSICAL_INTERLOCKS');
assert.equal(score.score_status, 'UNAVAILABLE');
assert.equal(score.score, null);
assert.ok(score.reasons.includes('NO_PARTIAL_SCORE_ALLOWED'));
for (const item of score.domains) {
  assert.equal(item.evidence_status, 'UNAVAILABLE');
  assert.notEqual(item.compatibility, 'COMPARABLE');
  assert.equal(item.quality, 'UNKNOWN');
}
assert.deepEqual(score.boundaries, {
  read_only: true,
  runtime_event_published: false,
  command_authority: 'NONE',
  safety_authority: 'NONE',
  broker_used: false,
  scheduler_used: false,
  remediation_used: false
});
console.log('BKL-036-F5 live health score validator PASS: seven-domain envelope is fail-closed and non-authoritative.');
