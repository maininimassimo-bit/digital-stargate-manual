import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const fixturePath = process.env.BKL039_F2_FIXTURE || 'docs/data/equipment-performance-registry-f2-fixture.json';
const schemaPath = 'schemas/equipment-performance-registry.schema.json';
const equipmentPath = 'data/analytics/configurations/equipment-registry.csv';
const sessionPath = 'data/analytics/metadata/session-scientific-metadata.csv';

function fail(message) { throw new Error(`BKL-039 F2 validation failed: ${message}`); }
function read(rel) { return fs.readFileSync(path.join(root, rel), 'utf8'); }
function csv(text) {
  const lines = text.trim().split(/\r?\n/);
  const headers = lines[0].split(',');
  return lines.slice(1).map(line => {
    const values=[]; let value=''; let quoted=false;
    for (let i=0;i<line.length;i++) {
      const c=line[i];
      if (c==='"') { if (quoted && line[i+1]==='"') { value+='"'; i++; } else quoted=!quoted; }
      else if (c===',' && !quoted) { values.push(value); value=''; }
      else value+=c;
    }
    values.push(value);
    return Object.fromEntries(headers.map((h,i)=>[h,values[i] ?? '']));
  });
}
function existsRef(ref) {
  const rel=ref.split('#')[0];
  return rel && fs.existsSync(path.join(root, rel));
}
function assertObjectShape(value, definition, label) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) fail(`${label} must be an object`);
  const required=new Set(definition.required || []);
  const properties=definition.properties || {};
  for (const key of required) if (!(key in value)) fail(`${label} missing required field ${key}`);
  if (definition.additionalProperties === false) {
    for (const key of Object.keys(value)) if (!(key in properties)) fail(`${label} has unexpected field ${key}`);
  }
  for (const [key, rule] of Object.entries(properties)) {
    if (!(key in value) || rule === true) continue;
    const item=value[key];
    if ('const' in rule && item !== rule.const) fail(`${label}.${key} violates const`);
    if (rule.enum && !rule.enum.includes(item)) fail(`${label}.${key} violates enum`);
    if (rule.type === 'string' && (typeof item !== 'string' || (rule.minLength && item.length < rule.minLength))) fail(`${label}.${key} invalid string`);
    if (rule.type === 'integer' && (!Number.isInteger(item) || ('minimum' in rule && item < rule.minimum))) fail(`${label}.${key} invalid integer`);
    if (rule.type === 'array') {
      if (!Array.isArray(item) || (rule.minItems && item.length < rule.minItems)) fail(`${label}.${key} invalid array`);
      if (rule.items?.type === 'string' && item.some(v=>typeof v !== 'string' || (rule.items.minLength && v.length < rule.items.minLength))) fail(`${label}.${key} invalid array item`);
    }
  }
}

const fixture=JSON.parse(read(fixturePath));
const schema=JSON.parse(read(schemaPath));
assertObjectShape(fixture, schema, 'fixture');
assertObjectShape(fixture.source_contract, schema.properties.source_contract, 'source_contract');
if (fixture.schema_version !== '1.0') fail('unsupported schema_version');
if (fixture.component !== 'DSG.EquipmentPerformanceRegistry.F2') fail('unexpected component');
if (fixture.authority !== 'projection' || fixture.action_authority !== 'NONE') fail('authority boundary changed');
if (fixture.source_contract.equipment_registry !== equipmentPath || fixture.source_contract.session_metadata !== sessionPath || fixture.source_contract.identity_namespace !== 'configuration_id') fail('source contract changed');
if (!Array.isArray(fixture.records) || fixture.records.length !== 4) fail('bounded fixture must contain exactly four records');

const equipment=csv(read(equipmentPath));
const sessions=csv(read(sessionPath));
const active=new Map(equipment.filter(r=>r.status==='ACTIVE').map(r=>[r.configuration_id,r]));
const registered=new Map(sessions.filter(r=>r.metadata_state==='REGISTERED').map(r=>[r.session_id,r]));
const ids=new Set();
const allowed=new Set(['EQUIPMENT_IDENTITY','EQUIPMENT_USAGE_OBSERVATION']);

for (const record of fixture.records) {
  const defName=record.semantic_type === 'EQUIPMENT_IDENTITY' ? 'equipmentIdentity' : record.semantic_type === 'EQUIPMENT_USAGE_OBSERVATION' ? 'equipmentUsageObservation' : null;
  if (!defName || !allowed.has(record.semantic_type)) fail(`unsupported semantic_type ${record.semantic_type}`);
  const specific=schema.$defs[defName].allOf[1];
  assertObjectShape(record, specific, `record ${record.record_id || '<missing>'}`);
  if (!record.record_id || ids.has(record.record_id)) fail('missing or duplicate record_id'); ids.add(record.record_id);
  if (record.authority !== 'projection' || record.action_authority !== 'NONE') fail(`record ${record.record_id} changed authority`);
  if (record.quality !== 'REGISTERED') fail(`record ${record.record_id} is not REGISTERED`);
  for (const group of ['source_record_refs','citation_refs','provenance_refs']) {
    if (!Array.isArray(record[group]) || record[group].length===0 || record[group].some(ref=>!existsRef(ref))) fail(`${record.record_id} has unresolved ${group}`);
  }
  const eq=active.get(record.configuration_id);
  if (!eq) fail(`${record.record_id} references non-active/unknown configuration`);
  if (record.semantic_type==='EQUIPMENT_IDENTITY') {
    if (record.identity_namespace !== 'DSG_ANALYTICS_CONFIGURATION_ID') fail(`${record.record_id} identity namespace changed`);
    if (record.dsdm_materialization_state !== 'NOT_SEPARATELY_PROVEN') fail(`${record.record_id} overclaims DSDM materialization`);
    for (const field of ['configuration_name','telescope','camera','mount']) if (record[field] !== eq[field]) fail(`${record.record_id} equipment ${field} mismatch`);
  } else {
    const session=registered.get(record.session_id);
    if (!session) fail(`${record.record_id} references non-REGISTERED/unknown session`);
    for (const field of ['configuration_id','target_name','telescope','camera']) if (record[field] !== session[field]) fail(`${record.record_id} session ${field} mismatch`);
    if (Number(record.binning) !== Number(session.binning)) fail(`${record.record_id} session binning mismatch`);
    if (record.source_reference !== session.source_reference || !existsRef(record.source_reference)) fail(`${record.record_id} unresolved source_reference`);
  }
}

const identityConfigs=new Set(fixture.records.filter(r=>r.semantic_type==='EQUIPMENT_IDENTITY').map(r=>r.configuration_id));
const usage=fixture.records.filter(r=>r.semantic_type==='EQUIPMENT_USAGE_OBSERVATION');
if (identityConfigs.size !== 2 || usage.length !== 2) fail('fixture must contain two equipment identities and two usage observations');
if (new Set(usage.map(r=>r.configuration_id)).size !== 2) fail('fixture must bind one usage observation per configuration');
if (usage.some(r=>r.session_id==='2026-08-10_2026-08-11')) fail('PARTIAL session entered fixture');
console.log('BKL-039 F2 fixture verification OK');
