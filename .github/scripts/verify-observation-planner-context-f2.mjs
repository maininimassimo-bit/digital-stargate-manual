import fs from 'node:fs';

const ROOT_KEYS = [
  'schema_version','component','authority','action_authority','safety_authority',
  'execution_zone','baseline_commit','bounds','sources','target_candidates',
  'planning_contexts','evidence_dimensions','ranking_factors',
  'ranking_explanations','citations','provenance_records'
];
const DIMENSION_TYPES = [
  'TARGET_IDENTITY','SETUP_COMPATIBILITY','CELESTIAL_GEOMETRY',
  'LUNAR_CONTEXT','FORECAST','OBSERVED_WEATHER_SQM','SCIENTIFIC_HISTORY'
];
const DIMENSION_STATES = ['AVAILABLE','PARTIAL','UNAVAILABLE','UNKNOWN','STALE','CONFLICTED'];
const SOURCE_CONTRACT = {
  'BKL031-S01':['AVAILABLE_BOUNDED','docs/data/target-knowledge-read-model.json#targets[].target_key','BKL035_PROJECTION_CHAIN','STATIC',true],
  'BKL031-S02':['AVAILABLE_HISTORICAL','data/analytics/metadata/session-scientific-metadata.csv#session_id','AP014_METADATA_PROJECTION','HISTORICAL',false],
  'BKL031-S03':['AVAILABLE_HISTORICAL','docs/data/scientific-session-catalog.json#sessions[].sessionId','AP014_SCIENTIFIC_PROJECTION','HISTORICAL',true],
  'BKL031-S04':['AVAILABLE_HISTORICAL','data/sessions/<YYYY>/<MM>/<session_id>/normalized/session-metrics.json','GOVERNED_SESSION_PROJECTION','HISTORICAL',false],
  'BKL031-S05':['AVAILABLE_DERIVED','data/analytics/history/sessions.csv;data/analytics/history/configuration-summary.csv','ANALYTICS_PROJECTION','HISTORICAL',true],
  'BKL031-S06':['AVAILABLE','docs/architecture/telemetry/BKL-029-SQM-Source-Discovery-and-Architecture-Contract.md','BKL029_SEMANTIC_AUTHORITY','STATIC',true],
  'BKL031-S07':['UNAVAILABLE_CURRENT_BASELINE','docs/data/realtime/observatory-status.json','OBSERVATORY_STATUS_PROJECTION','CURRENT',false],
  'BKL031-S08':['UNAVAILABLE',null,'NOT_ESTABLISHED','NOT_ESTABLISHED',false],
  'BKL031-S09':['UNAVAILABLE_CURRENT',null,'NOT_ESTABLISHED','NOT_ESTABLISHED',false],
  'BKL031-S10':['UNAVAILABLE',null,'NOT_ESTABLISHED','NOT_ESTABLISHED',false],
  'BKL031-S11':['UNAVAILABLE',null,'NOT_ESTABLISHED','NOT_ESTABLISHED',false]
};
const PROHIBITED_KEYS = new Set([
  'weight','score','score_contribution','threshold','normalization',
  'normalization_curve','rank','ranking_order','target_order','priority',
  'readiness','go_no_go','safe','approved','authorized','command',
  'device_command','scheduler','schedule','sequence_edit'
]);
const OPERATIONAL_WORDS = /\b(?:safe|ready|go|no-go|approved|authorized)\b/i;
const PROHIBITED_FACT_SEMANTICS = /(?:READINESS|READY|SAFE|SAFETY|AUTHORI[ZS]|APPROV|SCORE|WEIGHT|THRESHOLD|NORMALI[ZS]|RANK|ORDER|PRIORITY|GO_NO_GO|NO_GO)/i;
const FACT_CONTRACTS = {
  TARGET_IDENTITY: {
    TARGET_KEY: {unit:null, sources:['BKL031-S01'], temporal:'STATIC', kind:'DECLARED'}
  },
  SETUP_COMPATIBILITY: {},
  CELESTIAL_GEOMETRY: {
    TARGET_RA_DEG: {unit:'DEG', sources:['BKL031-S02','BKL031-S04'], temporal:'HISTORICAL', kind:'DECLARED'},
    TARGET_DEC_DEG: {unit:'DEG', sources:['BKL031-S02','BKL031-S04'], temporal:'HISTORICAL', kind:'DECLARED'},
    COORDINATE_EPOCH: {unit:null, sources:['BKL031-S02','BKL031-S04'], temporal:'HISTORICAL', kind:'DECLARED'}
  },
  LUNAR_CONTEXT: {},
  FORECAST: {},
  OBSERVED_WEATHER_SQM: {
    SQM_SESSION_MEDIAN: {unit:'MAG_PER_ARCSEC2', sources:['BKL031-S05'], temporal:'HISTORICAL', kind:'OBSERVED'}
  },
  SCIENTIFIC_HISTORY: {
    SCIENTIFIC_SESSION_REF: {unit:null, sources:['BKL031-S03'], temporal:'HISTORICAL', kind:'OBSERVED'}
  }
};
const UTC = /^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]+)?Z$/;

const isObject = value => value !== null && typeof value === 'object' && !Array.isArray(value);
const asArray = value => Array.isArray(value) ? value : [];
const ref = value => isObject(value) ? String(value.id) + '@' + String(value.version) : '<invalid-ref>';
const sameSet = (a, b) => JSON.stringify([...asArray(a)].sort()) === JSON.stringify([...asArray(b)].sort());
const numberEqual = (left, right) => Number.isFinite(Number(left)) && Number.isFinite(Number(right)) && Math.abs(Number(left) - Number(right)) < 1e-9;
const instantEqual = (left, right) => validUtc(left) && validUtc(right) && Date.parse(left) === Date.parse(right);
const unique = values => Array.isArray(values) && new Set(values).size === values.length;
const nonEmptyRefs = values => unique(values) && values.every(value => typeof value === 'string' && value.length > 1);

function exactKeys(value, allowed, label, fail) {
  if (!isObject(value)) { fail(label + ': must be an object'); return; }
  for (const key of Object.keys(value)) if (!allowed.includes(key)) fail(label + ': unexpected property ' + key);
  for (const key of allowed) if (!Object.hasOwn(value, key)) fail(label + ': required property ' + key + ' missing');
}

function validUtc(value) {
  return typeof value === 'string' && UTC.test(value) && Number.isFinite(Date.parse(value));
}

function validateInterval(interval, label, fail) {
  exactKeys(interval, ['start_utc','end_utc'], label, fail);
  if (!validUtc(interval?.start_utc) || !validUtc(interval?.end_utc)) fail(label + ': UTC instants must use explicit Z');
  else if (Date.parse(interval.start_utc) >= Date.parse(interval.end_utc)) fail(label + ': start_utc must precede end_utc');
}

function scanProhibited(value, path, fail) {
  if (Array.isArray(value)) {
    value.forEach((item, index) => scanProhibited(item, path + '[' + index + ']', fail));
    return;
  }
  if (!isObject(value)) return;
  for (const [key, child] of Object.entries(value)) {
    if (PROHIBITED_KEYS.has(key)) fail(path + ': prohibited F2 field ' + key);
    if (/resolution_basis|selection_basis/i.test(key) && /RECENCY|FILE_ORDER|UI_TEXT/i.test(String(child))) {
      fail(path + ': prohibited conflict resolution basis ' + child);
    }
    scanProhibited(child, path + '.' + key, fail);
  }
}

export function parseCsv(text) {
  const rows = []; let row = []; let field = ''; let quoted = false;
  for (let i = 0; i < text.length; i += 1) {
    const char = text[i];
    if (char === '"') {
      if (quoted && text[i + 1] === '"') { field += '"'; i += 1; }
      else quoted = !quoted;
    } else if (char === ',' && !quoted) { row.push(field); field = ''; }
    else if ((char === '\n' || char === '\r') && !quoted) {
      if (char === '\r' && text[i + 1] === '\n') i += 1;
      row.push(field); field = '';
      if (row.some(value => value.length)) rows.push(row);
      row = [];
    } else field += char;
  }
  if (field.length || row.length) { row.push(field); rows.push(row); }
  const headers = rows.shift() || [];
  return rows.map(values => Object.fromEntries(headers.map((header, index) => [header, values[index] ?? ''])));
}

function structuralChecks(doc, fail) {
  exactKeys(doc, ROOT_KEYS, 'root', fail);
  if (doc.schema_version !== '1.0') fail('schema_version must be 1.0');
  if (doc.component !== 'DSG.ObservationPlannerContextContract') fail('component mismatch');
  if (doc.authority !== 'projection') fail('authority must remain projection');
  if (doc.action_authority !== 'NONE') fail('action_authority must remain NONE');
  if (doc.safety_authority !== 'NONE') fail('safety_authority must remain NONE');
  if (doc.execution_zone !== 'PORTAL_CI') fail('execution_zone must remain PORTAL_CI; EAGLE workload is prohibited');
  if (!/^[0-9a-f]{40}$/.test(doc.baseline_commit || '')) fail('baseline_commit must be a full commit SHA');

  const boundKeys = ['max_sources','max_candidates','max_contexts','max_dimensions_per_candidate','max_factor_definitions','max_explanations'];
  exactKeys(doc.bounds, boundKeys, 'bounds', fail);
  const expectedBounds = [11,2,1,7,7,2];
  boundKeys.forEach((key, index) => { if (doc.bounds?.[key] !== expectedBounds[index]) fail('bounds.' + key + ' mismatch'); });
  if (!Array.isArray(doc.sources) || doc.sources.length !== 11) fail('source inventory must contain exactly BKL031-S01 through S11');
  if (!Array.isArray(doc.target_candidates) || doc.target_candidates.length < 1 || doc.target_candidates.length > 2) fail('candidate bound violated');
  if (!Array.isArray(doc.planning_contexts) || doc.planning_contexts.length !== 1) fail('context bound violated');
  if (!Array.isArray(doc.evidence_dimensions) || doc.evidence_dimensions.length > 14) fail('evidence dimension bound violated');
  if (!Array.isArray(doc.ranking_factors) || doc.ranking_factors.length !== 7) fail('factor-definition bound violated');
  if (!Array.isArray(doc.ranking_explanations) || doc.ranking_explanations.length < 1 || doc.ranking_explanations.length > 2) fail('explanation bound violated');
  if (!Array.isArray(doc.citations)) fail('citations must be an array');
  if (!Array.isArray(doc.provenance_records)) fail('provenance_records must be an array');
  scanProhibited(doc, 'root', fail);
}

function sourceChecks(doc, fail) {
  const keys = ['source_id','availability_state','authority','exact_locator','temporal_scope','public_projection_eligible','reason_codes'];
  const seen = new Set();
  for (const [index, source] of asArray(doc.sources).entries()) {
    const label = 'source[' + index + ']';
    exactKeys(source, keys, label, fail);
    if (!isObject(source)) continue;
    if (!SOURCE_CONTRACT[source.source_id]) { fail(label + ': unknown source_id ' + source.source_id); continue; }
    if (seen.has(source.source_id)) fail(label + ': duplicate source_id ' + source.source_id);
    seen.add(source.source_id);
    const expected = SOURCE_CONTRACT[source.source_id];
    if (source.availability_state !== expected[0]) fail(source.source_id + ': availability must remain ' + expected[0]);
    if (source.exact_locator !== expected[1]) fail(source.source_id + ': exact locator drift');
    if (source.authority !== expected[2]) fail(source.source_id + ': authority drift');
    if (source.temporal_scope !== expected[3]) fail(source.source_id + ': temporal scope drift');
    if (source.public_projection_eligible !== expected[4]) fail(source.source_id + ': public projection eligibility drift');
    if (!unique(source.reason_codes) || asArray(source.reason_codes).some(value => typeof value !== 'string' || value.length < 2)) fail(source.source_id + ': reason_codes must be unique refs');
  }
  for (const id of Object.keys(SOURCE_CONTRACT)) if (!seen.has(id)) fail('missing source ' + id);
}

function citationChecks(doc, sources, repositorySources, fail) {
  const keys = ['id','version','source_ref','locator','public_safe'];
  const locatorKeys = ['path','record_key','record_value'];
  const citations = new Map();
  const targetModel = repositorySources?.targetKnowledgeReadModel;
  const catalog = repositorySources?.scientificSessionCatalog;
  const sessionRows = parseCsv(repositorySources?.analyticsSessionsCsv || '');
  for (const [index, citation] of asArray(doc.citations).entries()) {
    const label = 'citation[' + index + ']';
    exactKeys(citation, keys, label, fail);
    if (!isObject(citation)) continue;
    exactKeys(citation.locator, locatorKeys, label + '.locator', fail);
    if (typeof citation.id !== 'string' || citation.id.length < 2 || typeof citation.version !== 'string' || !citation.version.length) fail(label + ': id/version must be non-empty');
    if (typeof citation.source_ref !== 'string' || citation.source_ref.length < 2) fail(label + ': source_ref must be non-empty');
    for (const key of locatorKeys) if (typeof citation.locator?.[key] !== 'string' || !citation.locator[key].length) fail(label + '.locator: ' + key + ' must be non-empty');
    const citationRef = ref(citation);
    if (citations.has(citationRef)) fail(label + ': duplicate Citation ' + citationRef);
    citations.set(citationRef, citation);
    if (!sources.has(citation.source_ref)) fail(citationRef + ': unresolved source_ref');
    if (citation.public_safe !== true) fail(citationRef + ': fixture Citation must be public_safe');
    const locatorText = Object.values(citation.locator || {}).join(' ');
    if (/[/\\]raw[/\\]|password|credential|secret|token|https?:\/\/|^[A-Za-z]:\\/i.test(locatorText)) {
      fail(citationRef + ': raw operational locator or credential is prohibited in public projection');
    }
    const path = citation.locator?.path;
    const key = citation.locator?.record_key;
    const value = citation.locator?.record_value;
    const metadataRows = parseCsv(repositorySources?.scientificMetadataCsv || '');
    if (path === 'docs/data/target-knowledge-read-model.json' && key === 'targets[].target_key') {
      if (citation.source_ref !== 'BKL031-S01') fail(citationRef + ': target locator requires BKL031-S01');
      if (!asArray(targetModel?.targets).some(target => target.target_key === value)) fail(citationRef + ': unresolved target Citation');
    } else if (path === 'docs/data/scientific-session-catalog.json' && key === 'sessions[].sessionId') {
      if (citation.source_ref !== 'BKL031-S03') fail(citationRef + ': catalog locator requires BKL031-S03');
      if (!asArray(catalog?.sessions).some(session => session.sessionId === value)) fail(citationRef + ': unresolved session Citation');
    } else if (path === 'data/analytics/history/sessions.csv' && key === 'session_id') {
      if (citation.source_ref !== 'BKL031-S05') fail(citationRef + ': analytics locator requires BKL031-S05');
      if (!sessionRows.some(row => row.session_id === value)) fail(citationRef + ': unresolved analytics session Citation');
    } else if (path === 'data/analytics/metadata/session-scientific-metadata.csv' && key === 'session_id') {
      if (citation.source_ref !== 'BKL031-S02') fail(citationRef + ': metadata locator requires BKL031-S02');
      if (!metadataRows.some(row => row.session_id === value)) fail(citationRef + ': unresolved scientific metadata Citation');
    } else if (key === 'session_id' && asArray(catalog?.sessions).some(session => session.sessionId === value && session.sourceMetricsPath === path)) {
      if (citation.source_ref !== 'BKL031-S04') fail(citationRef + ': normalized session locator requires BKL031-S04');
    } else fail(citationRef + ': locator is outside the bounded F2 allowlist');
  }
  return citations;
}

function provenanceChecks(doc, citations, fail) {
  const keys = ['id','version','method_id','input_refs','output_ref','citation_refs','evidence_kind'];
  const methods = new Set(['BKL031-F2-SOURCE-SNAPSHOT-1','BKL031-F2-CANDIDATE-BINDING-1','BKL031-F2-EVIDENCE-BINDING-1','BKL031-F2-NO-RANKING-1']);
  const kinds = new Set(['OBSERVED','DECLARED','SUGGESTED']);
  const provenance = new Map();
  for (const [index, item] of asArray(doc.provenance_records).entries()) {
    const label = 'provenance[' + index + ']';
    exactKeys(item, keys, label, fail);
    if (!isObject(item)) continue;
    const itemRef = ref(item);
    if (provenance.has(itemRef)) fail(label + ': duplicate Provenance ' + itemRef);
    provenance.set(itemRef, item);
    if (!methods.has(item.method_id)) fail(itemRef + ': ungoverned provenance method');
    if (!kinds.has(item.evidence_kind)) fail(itemRef + ': invalid evidence_kind');
    if (typeof item.id !== 'string' || item.id.length < 2 || typeof item.version !== 'string' || !item.version.length || typeof item.output_ref !== 'string' || item.output_ref.length < 2) fail(label + ': id/version/output_ref must be non-empty');
    if (!nonEmptyRefs(item.input_refs) || !item.input_refs.length) fail(itemRef + ': input_refs must be unique non-empty refs');
    if (!nonEmptyRefs(item.citation_refs) || !item.citation_refs.length) fail(itemRef + ': citation_refs must be unique non-empty refs');
    for (const citationRef of asArray(item.citation_refs)) if (!citations.has(citationRef)) fail(itemRef + ': unresolved Citation ' + citationRef);
  }
  return provenance;
}

function candidateChecks(doc, sources, citations, provenance, repositorySources, fail) {
  const keys = ['candidate_id','target_key','target_id','canonical_name','aliases','identity_state','source_refs','citation_refs','provenance_refs','conflict_refs','evidence_dimension_refs'];
  const candidates = new Map();
  const targets = asArray(repositorySources?.targetKnowledgeReadModel?.targets);
  for (const [index, candidate] of asArray(doc.target_candidates).entries()) {
    const label = 'candidate[' + index + ']';
    exactKeys(candidate, keys, label, fail);
    if (!isObject(candidate)) continue;
    if (candidates.has(candidate.candidate_id)) fail(label + ': duplicate candidate_id');
    candidates.set(candidate.candidate_id, candidate);
    if (typeof candidate.candidate_id !== 'string' || candidate.candidate_id.length < 2 || typeof candidate.canonical_name !== 'string' || !candidate.canonical_name.length) fail(label + ': candidate_id/canonical_name must be non-empty');
    if (!(candidate.target_id === null || (typeof candidate.target_id === 'string' && candidate.target_id.length))) fail(label + ': target_id must be non-empty or null');
    if (!['validated','conflicted','incomplete','unknown'].includes(candidate.identity_state)) fail(label + ': invalid identity_state');
    if (!/^dsg-target:[a-z0-9]+(?:-[a-z0-9]+)*$/.test(candidate.target_key || '')) fail(label + ': invalid target_key');
    for (const field of ['aliases','conflict_refs']) {
      if (!unique(candidate[field]) || asArray(candidate[field]).some(value => typeof value !== 'string' || !value.length)) fail(label + ': ' + field + ' must be unique refs');
    }
    for (const field of ['source_refs','citation_refs','provenance_refs','evidence_dimension_refs']) {
      if (!nonEmptyRefs(candidate[field]) || !candidate[field].length) fail(label + ': ' + field + ' requires unique non-empty refs');
    }
    const exact = targets.find(target => target.target_key === candidate.target_key);
    if (!exact) { fail(label + ': no exact BKL-035 identity; fuzzy matching prohibited'); continue; }
    if (candidate.canonical_name !== exact.canonical_name || candidate.target_id !== exact.target_id) fail(label + ': candidate identity does not preserve BKL-035 fields');
    if (candidate.identity_state !== exact.identity_state) fail(label + ': BKL-035 identity state conflict must be preserved');
    if (exact.identity_state !== 'validated' && candidate.identity_state === 'validated') fail(label + ': conflicted/unknown identity cannot be validated');
    if (!asArray(candidate.source_refs).includes('BKL031-S01')) fail(label + ': candidate must bind to BKL031-S01');
    for (const sourceRef of asArray(candidate.source_refs)) if (!sources.has(sourceRef)) fail(label + ': unresolved source ' + sourceRef);
    for (const citationRef of asArray(candidate.citation_refs)) if (!citations.has(citationRef)) fail(label + ': unresolved Citation ' + citationRef);
    for (const provenanceRef of asArray(candidate.provenance_refs)) {
      const item = provenance.get(provenanceRef);
      if (!item) fail(label + ': unresolved Provenance ' + provenanceRef);
      else if (item.output_ref !== candidate.candidate_id) fail(label + ': Provenance output must bind to candidate');
    }
  }
  return candidates;
}

function dimensionChecks(doc, sources, citations, provenance, candidates, fail) {
  const keys = ['dimension_id','candidate_ref','dimension_type','availability_state','semantic_type','unit','source_refs','citation_refs','provenance_refs','evidence_kind','reason_codes','facts'];
  const factKeys = ['fact_id','semantic_type','value','unit','temporal_scope','observed_at_utc','issue_at_utc','valid_interval','spatial_scope_ref','method_ref','source_ref','citation_refs','provenance_refs','evidence_kind'];
  const dimensions = new Map(); const perCandidate = new Map();
  for (const [index, dimension] of asArray(doc.evidence_dimensions).entries()) {
    const label = 'dimension[' + index + ']';
    exactKeys(dimension, keys, label, fail);
    if (!isObject(dimension)) continue;
    if (dimensions.has(dimension.dimension_id)) fail(label + ': duplicate dimension_id');
    dimensions.set(dimension.dimension_id, dimension);
    if (!candidates.has(dimension.candidate_ref)) fail(label + ': unresolved candidate_ref');
    if (!DIMENSION_TYPES.includes(dimension.dimension_type)) fail(label + ': invalid dimension_type');
    if (!DIMENSION_STATES.includes(dimension.availability_state)) fail(label + ': invalid availability_state');
    if (typeof dimension.dimension_id !== 'string' || dimension.dimension_id.length < 2 || typeof dimension.semantic_type !== 'string' || !dimension.semantic_type.length) fail(label + ': dimension_id/semantic_type must be non-empty');
    if (!(dimension.unit === null || (typeof dimension.unit === 'string' && dimension.unit.length))) fail(label + ': unit must be non-empty or null');
    if (!nonEmptyRefs(dimension.source_refs) || !dimension.source_refs.length) fail(label + ': source_refs must be unique non-empty refs');
    for (const sourceRef of asArray(dimension.source_refs)) if (!sources.has(sourceRef)) fail(label + ': unresolved source ' + sourceRef);
    if (!unique(dimension.citation_refs) || !unique(dimension.provenance_refs) || !unique(dimension.reason_codes)) fail(label + ': references/reasons must be arrays of unique values');
    if (!Array.isArray(dimension.facts)) fail(label + ': facts must be an array');
    const usable = ['AVAILABLE','PARTIAL'].includes(dimension.availability_state);
    if (usable && (!asArray(dimension.facts).length || !dimension.evidence_kind || !asArray(dimension.citation_refs).length || !asArray(dimension.provenance_refs).length)) {
      fail(label + ': usable evidence requires facts, kind, Citation and Provenance');
    }
    if (!usable && (asArray(dimension.facts).length || dimension.evidence_kind !== null)) fail(label + ': unavailable/stale/conflicted evidence must expose no facts and null kind');
    if (!usable && !asArray(dimension.reason_codes).length) fail(label + ': non-available evidence requires reason_codes');
    for (const citationRef of asArray(dimension.citation_refs)) if (!citations.has(citationRef)) fail(label + ': unresolved Citation ' + citationRef);
    for (const provenanceRef of asArray(dimension.provenance_refs)) if (!provenance.has(provenanceRef)) fail(label + ': unresolved Provenance ' + provenanceRef);

    const types = perCandidate.get(dimension.candidate_ref) || [];
    types.push(dimension.dimension_type); perCandidate.set(dimension.candidate_ref, types);
    for (const [factIndex, fact] of asArray(dimension.facts).entries()) {
      const factLabel = label + '.fact[' + factIndex + ']';
      exactKeys(fact, factKeys, factLabel, fail);
      if (!isObject(fact)) continue;
      if (typeof fact.fact_id !== 'string' || fact.fact_id.length < 2 || typeof fact.semantic_type !== 'string' || !fact.semantic_type.length) fail(factLabel + ': fact_id/semantic_type must be non-empty');
      if (!['string','number','boolean'].includes(typeof fact.value) || fact.value === '' || (fact.semantic_type === 'SQM_SESSION_MEDIAN' && (!(fact.value > 0) || fact.value > 30))) fail(factLabel + ': null, zero, empty or semantically invalid value');
      if (!(fact.unit === null || (typeof fact.unit === 'string' && fact.unit.length))) fail(factLabel + ': unit must be non-empty or null');
      if (!['STATIC','HISTORICAL','CURRENT','FORECAST'].includes(fact.temporal_scope)) fail(factLabel + ': invalid temporal_scope');
      if (!['OBSERVED','DECLARED','SUGGESTED'].includes(fact.evidence_kind)) fail(factLabel + ': invalid evidence_kind');
      if (!sources.has(fact.source_ref) || !asArray(dimension.source_refs).includes(fact.source_ref)) fail(factLabel + ': source must bind to its dimension');
      else if (!sources.get(fact.source_ref).availability_state.startsWith('AVAILABLE')) fail(factLabel + ': unavailable source cannot publish a fact value');
      if (!nonEmptyRefs(fact.citation_refs) || !fact.citation_refs.length || !nonEmptyRefs(fact.provenance_refs) || !fact.provenance_refs.length) fail(factLabel + ': Citation and Provenance are required');
      for (const citationRef of asArray(fact.citation_refs)) if (!citations.has(citationRef)) fail(factLabel + ': unresolved Citation ' + citationRef);
      for (const provenanceRef of asArray(fact.provenance_refs)) {
        const item = provenance.get(provenanceRef);
        if (!item) fail(factLabel + ': unresolved Provenance ' + provenanceRef);
        else if (fact.evidence_kind === 'OBSERVED' && item.evidence_kind === 'SUGGESTED') fail(factLabel + ': suggested result cannot be re-ingested as observed evidence');
      }
      if (fact.observed_at_utc !== null && !validUtc(fact.observed_at_utc)) fail(factLabel + ': observed_at_utc must use explicit Z');
      if (fact.issue_at_utc !== null && !validUtc(fact.issue_at_utc)) fail(factLabel + ': issue_at_utc must use explicit Z');
      if (fact.valid_interval !== null) validateInterval(fact.valid_interval, factLabel + '.valid_interval', fail);
      if (dimension.dimension_type === 'TARGET_IDENTITY' && fact.source_ref !== 'BKL031-S01') fail(factLabel + ': analytics/read model cannot override BKL-035 target authority');
      if (dimension.dimension_type === 'FORECAST') {
        if (fact.source_ref !== 'BKL031-S11') fail(factLabel + ': historical weather cannot substitute forecast');
        if (!fact.issue_at_utc || !fact.valid_interval || !fact.spatial_scope_ref || !fact.method_ref) fail(factLabel + ': forecast requires provider run, issue time, valid interval and spatial applicability');
      }
      if (dimension.dimension_type === 'CELESTIAL_GEOMETRY') {
        const semanticTypes = new Set(asArray(dimension.facts).map(item => item.semantic_type));
        if ((semanticTypes.has('TARGET_RA_DEG') || semanticTypes.has('TARGET_DEC_DEG')) && !semanticTypes.has('COORDINATE_EPOCH')) fail(label + ': target coordinates require epoch');
        if (['ALTITUDE_DEG','TRANSIT_UTC','DARKNESS_STATE'].includes(fact.semantic_type) && (!fact.method_ref || fact.source_ref !== 'BKL031-S10')) fail(factLabel + ': ephemeris output requires governed source and method/version');
      }
      if (dimension.dimension_type === 'LUNAR_CONTEXT' && (!fact.method_ref || fact.source_ref !== 'BKL031-S10')) fail(factLabel + ': lunar output requires governed source and method/version');
      if (fact.temporal_scope === 'CURRENT') {
        const context = doc.planning_contexts?.[0];
        if (fact.source_ref !== 'BKL031-S07' || !fact.valid_interval || !fact.observed_at_utc) fail(factLabel + ': current evidence requires governed realtime source and explicit freshness');
        else if (Date.parse(fact.valid_interval.end_utc) < Date.parse(context.evaluation_instant_utc)) fail(factLabel + ': realtime evidence expired and must be STALE with value excluded');
      }
      if (fact.temporal_scope === 'FORECAST' && dimension.dimension_type !== 'FORECAST') fail(factLabel + ': forecast temporal scope is restricted to forecast dimension');
    }
  }
  for (const [candidateRef, types] of perCandidate) {
    if (types.length !== 7 || !sameSet(types, DIMENSION_TYPES)) fail(candidateRef + ': exactly seven distinct evidence dimensions are required');
    const candidate = candidates.get(candidateRef);
    if (candidate && !sameSet(candidate.evidence_dimension_refs, [...dimensions.values()].filter(item => item.candidate_ref === candidateRef).map(item => item.dimension_id))) fail(candidateRef + ': evidence_dimension_refs mismatch');
  }
  return dimensions;
}

function contextChecks(doc, candidates, dimensions, fail) {
  const keys = ['context_id','generated_at_utc','evaluation_instant_utc','requested_interval','display_timezone_ref','site_ref','active_setup_ref','candidate_refs','evidence_snapshot_refs','unavailable_dimension_refs','stale_dimension_refs','conflicted_dimension_refs'];
  const context = doc.planning_contexts?.[0];
  exactKeys(context, keys, 'context[0]', fail);
  if (typeof context?.context_id !== 'string' || context.context_id.length < 2) fail('context[0]: context_id must be non-empty');
  if (!validUtc(context?.generated_at_utc) || !validUtc(context?.evaluation_instant_utc)) fail('context[0]: generation/evaluation instants must use explicit Z');
  validateInterval(context?.requested_interval, 'context[0].requested_interval', fail);
  for (const field of ['candidate_refs','evidence_snapshot_refs']) if (!nonEmptyRefs(context?.[field]) || !context[field].length) fail('context[0]: ' + field + ' requires unique non-empty refs');
  for (const field of ['unavailable_dimension_refs','stale_dimension_refs','conflicted_dimension_refs']) if (!unique(context?.[field]) || asArray(context[field]).some(value => typeof value !== 'string' || value.length < 2)) fail('context[0]: ' + field + ' must contain unique refs');
  if (context?.site_ref === null && context?.display_timezone_ref !== null) fail('context[0]: display timezone cannot be guessed without governed site');
  if (context?.active_setup_ref !== null) fail('context[0]: historical configuration cannot become current without governed validity interval');
  for (const candidateRef of asArray(context?.candidate_refs)) if (!candidates.has(candidateRef)) fail('context[0]: unresolved candidate_ref ' + candidateRef);
  for (const dimensionRef of asArray(context?.evidence_snapshot_refs)) if (!dimensions.has(dimensionRef)) fail('context[0]: unresolved evidence ref ' + dimensionRef);
  const contextDimensions = [...dimensions.values()].filter(item => asArray(context?.candidate_refs).includes(item.candidate_ref));
  const unavailable = contextDimensions.filter(item => ['UNAVAILABLE','UNKNOWN'].includes(item.availability_state)).map(item => item.dimension_id);
  const stale = contextDimensions.filter(item => item.availability_state === 'STALE').map(item => item.dimension_id);
  const conflicted = contextDimensions.filter(item => item.availability_state === 'CONFLICTED').map(item => item.dimension_id);
  if (!sameSet(context?.unavailable_dimension_refs, unavailable)) fail('context[0]: unavailable dimension list must be complete');
  if (!sameSet(context?.stale_dimension_refs, stale)) fail('context[0]: stale dimension list must be complete');
  if (!sameSet(context?.conflicted_dimension_refs, conflicted)) fail('context[0]: conflicted dimension list must be complete');
  for (const dimension of contextDimensions) {
    if (context?.site_ref === null && ['CELESTIAL_GEOMETRY','LUNAR_CONTEXT'].includes(dimension.dimension_type) && dimension.availability_state !== 'UNAVAILABLE') fail('context[0]: missing site requires unavailable celestial/lunar evidence');
    if (context?.active_setup_ref === null && dimension.dimension_type === 'SETUP_COMPATIBILITY' && dimension.availability_state !== 'UNAVAILABLE') fail('context[0]: missing active setup requires unavailable setup evidence');
  }
  return context;
}

function factorChecks(doc, fail) {
  const keys = ['factor_id','name','input_dimension_type','expected_semantic_type','expected_unit','interpretation_direction','missing_behavior','conflict_behavior'];
  const factors = new Map(); const types = [];
  for (const [index, factor] of asArray(doc.ranking_factors).entries()) {
    const label = 'factor[' + index + ']';
    exactKeys(factor, keys, label, fail);
    if (!isObject(factor)) continue;
    if (factors.has(factor.factor_id)) fail(label + ': duplicate factor_id');
    factors.set(factor.factor_id, factor); types.push(factor.input_dimension_type);
    if (typeof factor.factor_id !== 'string' || factor.factor_id.length < 2 || typeof factor.name !== 'string' || !factor.name.length || typeof factor.expected_semantic_type !== 'string' || !factor.expected_semantic_type.length) fail(label + ': identifiers and semantic type must be non-empty');
    if (!(factor.expected_unit === null || (typeof factor.expected_unit === 'string' && factor.expected_unit.length))) fail(label + ': expected_unit must be non-empty or null');
    if (!DIMENSION_TYPES.includes(factor.input_dimension_type)) fail(label + ': invalid input dimension');
    if (!['HIGHER_BETTER','LOWER_BETTER','CONTEXTUAL','NONE'].includes(factor.interpretation_direction)) fail(label + ': invalid interpretation_direction');
    if (factor.missing_behavior !== 'EXCLUDE_AND_EXPLAIN' || factor.conflict_behavior !== 'EXCLUDE_AND_EXPLAIN') fail(label + ': fail-closed factor behavior required');
  }
  if (!sameSet(types, DIMENSION_TYPES)) fail('factors must define each evidence dimension exactly once');
  return factors;
}

function explanationChecks(doc, candidates, dimensions, factors, citations, provenance, context, fail) {
  const keys = ['explanation_id','candidate_ref','context_ref','method_id','evaluation_state','factor_refs','evidence_refs','citation_refs','provenance_refs','excluded_dimension_refs','stale_dimension_refs','conflicted_dimension_refs','missing_reason_codes','message'];
  for (const [index, explanation] of asArray(doc.ranking_explanations).entries()) {
    const label = 'explanation[' + index + ']';
    exactKeys(explanation, keys, label, fail);
    if (!isObject(explanation)) continue;
    if (typeof explanation.explanation_id !== 'string' || explanation.explanation_id.length < 2 || typeof explanation.message !== 'string' || !explanation.message.length) fail(label + ': explanation_id/message must be non-empty');
    for (const field of ['factor_refs','evidence_refs','citation_refs','provenance_refs']) if (!nonEmptyRefs(explanation[field]) || !explanation[field].length) fail(label + ': ' + field + ' requires unique non-empty refs');
    for (const field of ['excluded_dimension_refs','stale_dimension_refs','conflicted_dimension_refs','missing_reason_codes']) if (!unique(explanation[field]) || asArray(explanation[field]).some(value => typeof value !== 'string' || value.length < 2)) fail(label + ': ' + field + ' must contain unique refs');
    if (!candidates.has(explanation.candidate_ref) || explanation.context_ref !== context?.context_id) fail(label + ': candidate/context binding mismatch');
    if (explanation.method_id !== 'BKL031-F2-NO-RANKING-1' || explanation.evaluation_state !== 'NOT_EVALUATED') fail(label + ': F2 explanation must remain NOT_EVALUATED with no-ranking method');
    for (const factorRef of asArray(explanation.factor_refs)) if (!factors.has(factorRef)) fail(label + ': unresolved factor ' + factorRef);
    for (const evidenceRef of asArray(explanation.evidence_refs)) if (!dimensions.has(evidenceRef)) fail(label + ': unresolved evidence ' + evidenceRef);
    for (const citationRef of asArray(explanation.citation_refs)) if (!citations.has(citationRef)) fail(label + ': unresolved Citation ' + citationRef);
    for (const provenanceRef of asArray(explanation.provenance_refs)) {
      const item = provenance.get(provenanceRef);
      if (!item) fail(label + ': unresolved Provenance ' + provenanceRef);
      else if (item.output_ref !== explanation.explanation_id || item.evidence_kind !== 'SUGGESTED') fail(label + ': explanation Provenance binding/kind mismatch');
    }
    const candidateDimensions = [...dimensions.values()].filter(item => item.candidate_ref === explanation.candidate_ref);
    const excluded = candidateDimensions.filter(item => !['AVAILABLE','PARTIAL'].includes(item.availability_state)).map(item => item.dimension_id);
    const stale = candidateDimensions.filter(item => item.availability_state === 'STALE').map(item => item.dimension_id);
    const conflicted = candidateDimensions.filter(item => item.availability_state === 'CONFLICTED').map(item => item.dimension_id);
    if (!sameSet(explanation.evidence_refs, candidateDimensions.map(item => item.dimension_id))) fail(label + ': all evidence dimensions must be enumerated');
    if (!sameSet(explanation.excluded_dimension_refs, excluded)) fail(label + ': explanation must enumerate every excluded dimension');
    if (!sameSet(explanation.stale_dimension_refs, stale)) fail(label + ': explanation must enumerate every stale dimension');
    if (!sameSet(explanation.conflicted_dimension_refs, conflicted)) fail(label + ': explanation must enumerate every conflicted dimension');
    const reasons = [...new Set(candidateDimensions.filter(item => !['AVAILABLE'].includes(item.availability_state)).flatMap(item => asArray(item.reason_codes)))];
    if (!sameSet(explanation.missing_reason_codes, reasons)) fail(label + ': missing reason codes must preserve all partial/unavailable evidence');
    if (OPERATIONAL_WORDS.test(explanation.message || '')) fail(label + ': operational conclusion vocabulary is prohibited');
  }
}


function governedEpoch(row) {
  const match = typeof row?.notes === 'string' ? row.notes.match(/\b(J[0-9]{4}(?:\.[0-9]+)?)\b/i) : null;
  return match ? match[1].toUpperCase() : null;
}

function semanticBindingChecks(doc, citations, provenance, candidates, dimensions, repositorySources, fail) {
  const analyticsRows = parseCsv(repositorySources?.analyticsSessionsCsv || '');
  const metadataRows = parseCsv(repositorySources?.scientificMetadataCsv || '');
  const catalogSessions = asArray(repositorySources?.scientificSessionCatalog?.sessions);
  const targetRows = asArray(repositorySources?.targetKnowledgeReadModel?.targets);

  for (const candidate of candidates.values()) {
    const label = 'candidate ' + candidate.candidate_id;
    const candidateCitations = asArray(candidate.citation_refs).map(value => citations.get(value)).filter(Boolean);
    if (candidateCitations.length !== 1) fail(label + ': exact BKL-035 Citation set requires one target Citation');
    for (const citation of candidateCitations) {
      if (citation.source_ref !== 'BKL031-S01' ||
          citation.locator?.path !== 'docs/data/target-knowledge-read-model.json' ||
          citation.locator?.record_key !== 'targets[].target_key' ||
          citation.locator?.record_value !== candidate.target_key) {
        fail(label + ': Citation must bind exactly to its BKL-035 target_key');
      }
    }
    if (asArray(candidate.provenance_refs).length !== 1) fail(label + ': exactly one candidate-binding Provenance is required');
    for (const provenanceRef of asArray(candidate.provenance_refs)) {
      const item = provenance.get(provenanceRef);
      if (!item) continue;
      if (item.method_id !== 'BKL031-F2-CANDIDATE-BINDING-1' ||
          item.output_ref !== candidate.candidate_id ||
          item.evidence_kind !== 'DECLARED' ||
          !sameSet(item.input_refs, ['BKL031-S01', ...asArray(candidate.citation_refs)]) ||
          !sameSet(item.citation_refs, candidate.citation_refs)) {
        fail(label + ': candidate Provenance input/output/Citation binding mismatch');
      }
    }
  }

  for (const dimension of dimensions.values()) {
    const label = 'dimension ' + dimension.dimension_id;
    const candidate = candidates.get(dimension.candidate_ref);
    const facts = asArray(dimension.facts).filter(isObject);
    const unionCitationRefs = [...new Set(facts.flatMap(fact => asArray(fact.citation_refs)))];
    if (facts.length && !sameSet(dimension.citation_refs, unionCitationRefs)) {
      fail(label + ': dimension Citation set must equal the union of fact Citations');
    }

    for (const fact of facts) {
      const factLabel = label + ' fact ' + fact.fact_id;
      if (PROHIBITED_FACT_SEMANTICS.test(String(fact.semantic_type)) ||
          (typeof fact.value === 'string' && PROHIBITED_FACT_SEMANTICS.test(fact.value))) {
        fail(factLabel + ': readiness/safety/authorization/score/threshold/normalization/ordering semantics are prohibited');
      }
      const contract = FACT_CONTRACTS[dimension.dimension_type]?.[fact.semantic_type];
      if (!contract) {
        fail(factLabel + ': semantic_type is outside the closed vocabulary for ' + dimension.dimension_type);
        continue;
      }
      if (fact.unit !== contract.unit) fail(factLabel + ': unit must be ' + String(contract.unit));
      if (!contract.sources.includes(fact.source_ref)) fail(factLabel + ': source class is not authorized for this semantic_type');
      if (fact.temporal_scope !== contract.temporal) fail(factLabel + ': temporal_scope must be ' + contract.temporal);
      if (fact.evidence_kind !== contract.kind) fail(factLabel + ': evidence_kind must be ' + contract.kind);

      const factCitations = asArray(fact.citation_refs).map(value => citations.get(value)).filter(Boolean);
      if (factCitations.length !== asArray(fact.citation_refs).length || !factCitations.length) {
        fail(factLabel + ': every fact Citation must resolve');
      }
      for (const citation of factCitations) {
        if (citation.source_ref !== fact.source_ref) fail(factLabel + ': Citation source must equal fact source');
      }
      for (const provenanceRef of asArray(fact.provenance_refs)) {
        const item = provenance.get(provenanceRef);
        if (!item) continue;
        if (item.method_id !== 'BKL031-F2-EVIDENCE-BINDING-1' ||
            item.output_ref !== dimension.dimension_id ||
            item.evidence_kind !== fact.evidence_kind ||
            !sameSet(item.citation_refs, dimension.citation_refs)) {
          fail(factLabel + ': Provenance must bind exactly to its dimension output and Citation set');
        }
      }

      if (dimension.dimension_type === 'TARGET_IDENTITY' && candidate) {
        const target = targetRows.find(item => item.target_key === candidate.target_key);
        if (fact.value !== target?.target_key) fail(factLabel + ': value does not equal the cited BKL-035 target_key');
        if (factCitations.some(citation => citation.locator?.record_value !== fact.value)) {
          fail(factLabel + ': value does not equal its Citation record_value');
        }
      }

      if (dimension.dimension_type === 'OBSERVED_WEATHER_SQM') {
        if (factCitations.length !== 1) fail(factLabel + ': SQM fact requires exactly one analytics Citation');
        const row = analyticsRows.find(item => item.session_id === factCitations[0]?.locator?.record_value);
        if (!row) fail(factLabel + ': cited analytics row is unresolved');
        else {
          if (!numberEqual(fact.value, row.sqm_median_mag_arcsec2)) fail(factLabel + ': value does not equal cited sqm_median_mag_arcsec2');
          if (candidate && row.target_name !== candidate.canonical_name) fail(factLabel + ': cited analytics row target does not match candidate');
          if (!instantEqual(fact.observed_at_utc, row.sqm_start)) fail(factLabel + ': observed_at_utc does not equal cited sqm_start');
          if (!instantEqual(fact.valid_interval?.start_utc, row.sqm_start) || !instantEqual(fact.valid_interval?.end_utc, row.sqm_end)) {
            fail(factLabel + ': valid_interval does not equal cited SQM interval');
          }
        }
      }

      if (dimension.dimension_type === 'SCIENTIFIC_HISTORY') {
        if (factCitations.length !== 1) fail(factLabel + ': session fact requires exactly one catalog Citation');
        const sessionId = factCitations[0]?.locator?.record_value;
        const session = catalogSessions.find(item => item.sessionId === sessionId);
        if (fact.value !== 'session:' + sessionId) fail(factLabel + ': value does not equal cited session reference');
        if (candidate && session?.target !== candidate.canonical_name) fail(factLabel + ': cited session target does not match candidate');
      }
    }

    if (facts.length) {
      if (asArray(dimension.provenance_refs).length !== 1) fail(label + ': exactly one dimension-binding Provenance is required');
      const item = provenance.get(asArray(dimension.provenance_refs)[0]);
      let expectedInputs = null;
      if (dimension.dimension_type === 'TARGET_IDENTITY') expectedInputs = [dimension.candidate_ref, 'BKL031-S01'];
      if (dimension.dimension_type === 'OBSERVED_WEATHER_SQM') {
        expectedInputs = [
          ...asArray(dimension.citation_refs).map(value => citations.get(value)).filter(Boolean).map(citation => 'session:' + citation.locator.record_value),
          'BKL031-S05','BKL031-S06'
        ];
      }
      if (dimension.dimension_type === 'SCIENTIFIC_HISTORY') {
        expectedInputs = [...facts.map(fact => fact.value), 'BKL031-S03'];
      }
      if (dimension.dimension_type === 'CELESTIAL_GEOMETRY') {
        expectedInputs = [
          ...asArray(dimension.citation_refs).map(value => citations.get(value)).filter(Boolean).map(citation => 'session:' + citation.locator.record_value),
          ...new Set(facts.map(fact => fact.source_ref))
        ];
      }
      if (!item || item.method_id !== 'BKL031-F2-EVIDENCE-BINDING-1' ||
          item.output_ref !== dimension.dimension_id ||
          item.evidence_kind !== dimension.evidence_kind ||
          !sameSet(item.citation_refs, dimension.citation_refs) ||
          (expectedInputs && !sameSet(item.input_refs, expectedInputs))) {
        fail(label + ': dimension Provenance input/output/Citation binding mismatch');
      }
    }

    if (dimension.dimension_type === 'CELESTIAL_GEOMETRY') {
      const coordinateFacts = facts.filter(fact => ['TARGET_RA_DEG','TARGET_DEC_DEG','COORDINATE_EPOCH'].includes(fact.semantic_type));
      const governedRows = metadataRows.filter(row =>
        row.metadata_state === 'REGISTERED' &&
        candidate &&
        row.target_id === candidate.target_id &&
        row.target_name === candidate.canonical_name &&
        Number.isFinite(Number(row.ra_deg)) &&
        Number.isFinite(Number(row.dec_deg)) &&
        governedEpoch(row)
      );
      const coordinateSets = [...new Set(governedRows.map(row => [Number(row.ra_deg), Number(row.dec_deg), governedEpoch(row)].join('|')))];
      if (coordinateSets.length > 1 && !['CONFLICTED','UNAVAILABLE'].includes(dimension.availability_state)) {
        fail(label + ': conflicting governed S02 coordinate evidence must remain CONFLICTED or UNAVAILABLE');
      }
      if (coordinateFacts.length) {
        const byType = new Map(coordinateFacts.map(fact => [fact.semantic_type, fact]));
        if (coordinateFacts.length !== 3 || !byType.has('TARGET_RA_DEG') || !byType.has('TARGET_DEC_DEG') || !byType.has('COORDINATE_EPOCH')) {
          fail(label + ': target coordinates require exact RA, Dec and epoch triplet');
        }
        const ra = byType.get('TARGET_RA_DEG')?.value;
        const dec = byType.get('TARGET_DEC_DEG')?.value;
        const epoch = byType.get('COORDINATE_EPOCH')?.value;
        if (!(typeof ra === 'number' && ra >= 0 && ra < 360)) fail(label + ': RA must be in [0,360) degrees');
        if (!(typeof dec === 'number' && dec >= -90 && dec <= 90)) fail(label + ': Dec must be in [-90,90] degrees');
        if (typeof epoch !== 'string' || !/^J[0-9]{4}(?:\.[0-9]+)?$/.test(epoch)) fail(label + ': coordinate epoch must be explicit');
        if (!governedRows.length) fail(label + ': no eligible governed S02 coordinate evidence for candidate');
        if (coordinateSets.length === 1) {
          const [expectedRa, expectedDec, expectedEpoch] = coordinateSets[0].split('|');
          if (!numberEqual(ra, expectedRa) || !numberEqual(dec, expectedDec) || epoch !== expectedEpoch) {
            fail(label + ': coordinate value conflicts with governed S02 evidence');
          }
        }
        for (const fact of coordinateFacts) {
          for (const citationRef of asArray(fact.citation_refs)) {
            const citation = citations.get(citationRef);
            const sessionId = citation?.locator?.record_value;
            const row = governedRows.find(item => item.session_id === sessionId);
            if (!row || !['BKL031-S02','BKL031-S04'].includes(citation?.source_ref)) {
              fail(label + ': coordinate Citation must resolve to eligible S02/S04 evidence for candidate');
            }
          }
        }
      }
    }
  }

  for (const explanation of asArray(doc.ranking_explanations).filter(isObject)) {
    const candidateDimensions = [...dimensions.values()].filter(item => item.candidate_ref === explanation.candidate_ref);
    const candidate = candidates.get(explanation.candidate_ref);
    const expectedCitations = [...new Set([
      ...asArray(candidate?.citation_refs),
      ...candidateDimensions.flatMap(item => asArray(item.citation_refs))
    ])];
    if (!sameSet(explanation.citation_refs, expectedCitations)) {
      fail('explanation ' + explanation.explanation_id + ': Citation set must equal candidate and dimension evidence');
    }
    for (const provenanceRef of asArray(explanation.provenance_refs)) {
      const item = provenance.get(provenanceRef);
      const expectedInputs = [explanation.context_ref, explanation.candidate_ref, ...candidateDimensions.map(value => value.dimension_id)];
      if (!item || item.method_id !== 'BKL031-F2-NO-RANKING-1' ||
          item.output_ref !== explanation.explanation_id ||
          item.evidence_kind !== 'SUGGESTED' ||
          !sameSet(item.input_refs, expectedInputs) ||
          !sameSet(item.citation_refs, explanation.citation_refs)) {
        fail('explanation ' + explanation.explanation_id + ': Provenance input/output/Citation binding mismatch');
      }
    }
  }
}

export function validateObservationPlannerContext(doc, repositorySources) {
  const errors = []; const fail = message => errors.push(String(message));
  if (!isObject(doc)) return ['observation planner contract must be an object'];
  const run = (label, action, fallback) => {
    try { return action(); }
    catch { fail(label + ': validation aborted for malformed input'); return fallback; }
  };
  run('structure', () => structuralChecks(doc, fail));
  run('sources', () => sourceChecks(doc, fail));
  const sources = new Map(asArray(doc.sources).filter(isObject).map(item => [item.source_id, item]));
  const citations = run('citations', () => citationChecks(doc, sources, repositorySources, fail), new Map());
  const provenance = run('provenance', () => provenanceChecks(doc, citations, fail), new Map());
  const candidates = run('candidates', () => candidateChecks(doc, sources, citations, provenance, repositorySources, fail), new Map());
  const dimensions = run('dimensions', () => dimensionChecks(doc, sources, citations, provenance, candidates, fail), new Map());
  const context = run('context', () => contextChecks(doc, candidates, dimensions, fail), undefined);
  const factors = run('factors', () => factorChecks(doc, fail), new Map());
  run('explanations', () => explanationChecks(doc, candidates, dimensions, factors, citations, provenance, context, fail));
  run('semantic bindings', () => semanticBindingChecks(doc, citations, provenance, candidates, dimensions, repositorySources, fail));
  return errors;
}

export function loadRepositorySources() {
  return {
    targetKnowledgeReadModel: JSON.parse(fs.readFileSync('docs/data/target-knowledge-read-model.json', 'utf8')),
    scientificSessionCatalog: JSON.parse(fs.readFileSync('docs/data/scientific-session-catalog.json', 'utf8')),
    analyticsSessionsCsv: fs.readFileSync('data/analytics/history/sessions.csv', 'utf8'),
    scientificMetadataCsv: fs.readFileSync('data/analytics/metadata/session-scientific-metadata.csv', 'utf8')
  };
}

if (process.argv[1]?.endsWith('verify-observation-planner-context-f2.mjs')) {
  const doc = JSON.parse(fs.readFileSync('docs/data/observation-planner-context-f2-fixture.json', 'utf8'));
  const errors = validateObservationPlannerContext(doc, loadRepositorySources());
  if (errors.length) { console.error(errors.join('\n')); process.exit(1); }
  console.log('BKL-031 F2 context contract OK: 11 sources / ' + doc.target_candidates.length + ' candidate / 7 dimensions / no ranking');
}
