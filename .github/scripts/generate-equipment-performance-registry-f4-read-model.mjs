import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../..');
const sourcePath = path.join(root, 'docs/data/equipment-performance-registry-f3.json');
const outputPath = path.join(root, 'docs/data/equipment-performance-registry-f4-read-model.json');

const fail = (message) => { throw new Error(`BKL-039 F4 generation failed: ${message}`); };
const readJson = (p) => JSON.parse(fs.readFileSync(p, 'utf8'));
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);

export function buildReadModel(source) {
  if (source?.component !== 'DSG.EquipmentPerformanceRegistry.F3') fail('unexpected F3 component');
  if (source?.authority !== 'projection' || source?.action_authority !== 'NONE') fail('F3 authority boundary changed');

  const sc = source.source_contract ?? {};
  const expected = {
    configuration_id: 'QUATTRO200_TOUPTEK294_BIN1',
    session_id: '2026-07-14_2026-07-15',
    target_name: 'LDN 1320',
    filter_name: 'LPRO',
    frame_type: 'LIGHT',
    unit: 'NINA_FILENAME_FWHM_SOURCE_UNIT',
    unit_semantics: 'SOURCE_NATIVE_UNCALIBRATED',
    angular_calibration_state: 'NOT_PROVEN'
  };
  for (const [key, value] of Object.entries(expected)) if (sc[key] !== value) fail(`F3 source_contract.${key} changed`);

  const records = Array.isArray(source.records) ? source.records : fail('F3 records missing');
  const measurements = records.filter((r) => r.semantic_type === 'PERFORMANCE_MEASUREMENT');
  const statistics = records.filter((r) => r.semantic_type === 'DESCRIPTIVE_PERFORMANCE_STATISTIC');
  if (measurements.length !== 19) fail(`expected 19 measurements, got ${measurements.length}`);
  if (statistics.length !== 4) fail(`expected 4 statistics, got ${statistics.length}`);

  const orderedMeasurements = [...measurements].sort((a, b) => String(a.sequence_number).localeCompare(String(b.sequence_number)));
  const expectedSequences = Array.from({ length: 19 }, (_, i) => String(i).padStart(4, '0'));
  if (!same(orderedMeasurements.map((r) => r.sequence_number), expectedSequences)) fail('measurement sequence is incomplete or non-deterministic');

  for (const r of orderedMeasurements) {
    if (r.configuration_id !== expected.configuration_id || r.session_id !== expected.session_id || r.target_name !== expected.target_name || r.filter_name !== expected.filter_name) fail(`measurement ${r.record_id} population changed`);
    if (r.metric_name !== 'FWHM' || r.unit !== expected.unit || r.unit_semantics !== expected.unit_semantics || r.angular_calibration_state !== expected.angular_calibration_state) fail(`measurement ${r.record_id} semantics changed`);
    if (r.method_id !== 'BKL039-F3-FWHM-NINA-FILENAME-EXTRACT-V1') fail(`measurement ${r.record_id} method changed`);
    if (r.authority !== 'projection' || r.action_authority !== 'NONE') fail(`measurement ${r.record_id} authority changed`);
    if (!Array.isArray(r.source_record_refs) || !r.source_record_refs.length || !Array.isArray(r.citation_refs) || !r.citation_refs.length || !Array.isArray(r.provenance_refs) || !r.provenance_refs.length) fail(`measurement ${r.record_id} lineage missing`);
  }

  const expectedStatisticMethods = {
    MEAN: 'BKL039-F3-FWHM-MEAN-V1',
    MINIMUM: 'BKL039-F3-FWHM-MIN-V1',
    MAXIMUM: 'BKL039-F3-FWHM-MAX-V1',
    SAMPLE_STDDEV: 'BKL039-F3-FWHM-SAMPLE-STDDEV-V1'
  };
  const byType = new Map();
  for (const r of statistics) {
    if (!expectedStatisticMethods[r.statistic_type]) fail(`unexpected statistic ${r.statistic_type}`);
    if (byType.has(r.statistic_type)) fail(`duplicate statistic ${r.statistic_type}`);
    if (r.method_id !== expectedStatisticMethods[r.statistic_type]) fail(`statistic ${r.statistic_type} method changed`);
    if (r.sample_count !== 19 || r.coverage !== 'COMPLETE_FOR_DECLARED_POPULATION') fail(`statistic ${r.statistic_type} population/coverage changed`);
    if (r.unit !== expected.unit || r.unit_semantics !== expected.unit_semantics || r.angular_calibration_state !== expected.angular_calibration_state) fail(`statistic ${r.statistic_type} semantics changed`);
    if (r.authority !== 'projection' || r.action_authority !== 'NONE') fail(`statistic ${r.statistic_type} authority changed`);
    if (!Array.isArray(r.source_record_refs) || r.source_record_refs.length !== 19 || !Array.isArray(r.citation_refs) || !r.citation_refs.length || !Array.isArray(r.provenance_refs) || !r.provenance_refs.length) fail(`statistic ${r.statistic_type} lineage missing`);
    byType.set(r.statistic_type, r);
  }
  for (const type of Object.keys(expectedStatisticMethods)) if (!byType.has(type)) fail(`missing statistic ${type}`);

  return {
    schema_version: '1.0',
    component: 'DSG.EquipmentPerformanceRegistry.F4.ReadModel',
    authority: 'projection',
    action_authority: 'NONE',
    source_contract: {
      f3_projection: 'docs/data/equipment-performance-registry-f3.json',
      f4_contract: 'docs/architecture/telemetry/BKL-039-F4-Equipment-Performance-Read-Only-Consumer-Contract.md',
      accepted_f3_merge: 'ce2482aa6b2da62296ebdc221f73f39c1acd3aa2'
    },
    view: {
      configuration_id: expected.configuration_id,
      session_id: expected.session_id,
      target_name: expected.target_name,
      filter_name: expected.filter_name,
      frame_type: expected.frame_type,
      metric_name: 'FWHM',
      unit: expected.unit,
      unit_semantics: expected.unit_semantics,
      angular_calibration_state: expected.angular_calibration_state,
      measurement_count: 19,
      coverage: 'COMPLETE_FOR_DECLARED_POPULATION',
      measurements: orderedMeasurements.map((r) => ({
        record_id: r.record_id,
        sequence_number: r.sequence_number,
        timestamp: r.timestamp,
        value: r.value,
        method_id: r.method_id,
        quality: r.quality,
        source_record_refs: r.source_record_refs,
        citation_refs: r.citation_refs,
        provenance_refs: r.provenance_refs
      })),
      statistics: ['MEAN', 'MINIMUM', 'MAXIMUM', 'SAMPLE_STDDEV'].map((type) => {
        const r = byType.get(type);
        return {
          record_id: r.record_id,
          statistic_type: r.statistic_type,
          value: r.value,
          method_id: r.method_id,
          sample_count: r.sample_count,
          coverage: r.coverage,
          quality: r.quality,
          source_record_refs: r.source_record_refs,
          citation_refs: r.citation_refs,
          provenance_refs: r.provenance_refs
        };
      }),
      limitations: [
        'SOURCE_NATIVE_FWHM_UNIT_IS_NOT_PHYSICALLY_CALIBRATED',
        'NO_EQUIPMENT_HEALTH_RANKING_THRESHOLD_OR_RECOMMENDATION',
        'HISTORICAL_READ_ONLY_PROJECTION_NOT_SAFETY_AUTHORITY'
      ]
    }
  };
}

export function generate({ write = false } = {}) {
  const source = readJson(sourcePath);
  const generated = buildReadModel(source);
  const text = `${JSON.stringify(generated, null, 2)}\n`;
  if (write) {
    fs.writeFileSync(outputPath, text, 'utf8');
    return generated;
  }
  if (!fs.existsSync(outputPath)) fail('generated read model missing; run with --write');
  const committed = readJson(outputPath);
  if (!same(committed, generated)) fail('generated read model is stale; run with --write');
  return generated;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const write = process.argv.includes('--write');
  generate({ write });
  console.log(`BKL-039 F4 read model ${write ? 'written' : 'verified'}.`);
}
