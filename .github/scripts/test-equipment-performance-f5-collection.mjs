import test from 'node:test';
import assert from 'node:assert/strict';
import { buildCollection } from './generate-equipment-performance-f5-collection.mjs';
import { discoverRepository } from './discover-equipment-performance-populations-f5.mjs';

test('F5-B collection mirrors every eligible repository population',()=>{
  const d=discoverRepository();
  const c=buildCollection(d);
  assert.equal(c.population_count,d.eligible_populations.length);
  assert.deepEqual(c.views.map(v=>v.population_id),d.eligible_populations.map(v=>v.population_id));
  assert.ok(c.views.some(v=>v.target_name==='LDN 1320'));
  assert.ok(c.views.some(v=>v.target_name==='M 27'));
  assert.ok(c.views.some(v=>v.session_id==='2026-08-15_2026-08-16'&&v.filter_name==='Blu'));
  assert.ok(c.views.some(v=>v.session_id==='2026-08-15_2026-08-16'&&v.filter_name==='Green'));
});

test('F5-B preserves projection-only uncalibrated semantics and lineage',()=>{
  const c=buildCollection(discoverRepository());
  for(const v of c.views){
    assert.equal(v.authority,'projection');
    assert.equal(v.action_authority,'NONE');
    assert.equal(v.unit,'NINA_FILENAME_FWHM_SOURCE_UNIT');
    assert.equal(v.unit_semantics,'SOURCE_NATIVE_UNCALIBRATED');
    assert.equal(v.angular_calibration_state,'NOT_PROVEN');
    assert.equal(v.measurements.length,v.measurement_count);
    assert.ok(v.source_record_refs.length===v.measurement_count);
    assert.ok(v.citation_refs.length>0&&v.provenance_refs.length>0);
    assert.ok(v.limitations.includes('NO_EQUIPMENT_HEALTH_RANKING_THRESHOLD_OR_RECOMMENDATION'));
  }
});

test('F5-B keeps fail-closed exclusions outside views',()=>{
  const c=buildCollection(discoverRepository());
  assert.ok(c.exclusions.some(e=>e.session_id==='2026-08-14_2026-08-15'&&e.filter_name==='L-Pro'&&e.reason==='FWHM_SOURCE_VALUE_UNRESOLVED'));
  assert.ok(c.exclusions.some(e=>e.session_id==='2026-08-10_2026-08-11'&&e.reason==='METADATA_NOT_REGISTERED'));
  assert.equal(c.views.some(v=>v.session_id==='2026-08-14_2026-08-15'&&v.filter_name==='L-Pro'),false);
  assert.equal(c.views.some(v=>v.session_id==='2026-08-10_2026-08-11'),false);
});
