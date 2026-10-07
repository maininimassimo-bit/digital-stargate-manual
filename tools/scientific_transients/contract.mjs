// Proposed S1 intake contract. This module has no network or image-processing I/O.
export const CONTRACT = 'BKL051_S1_INTAKE_PROPOSED_V1';
const keys = (value, expected) => value && typeof value === 'object' && !Array.isArray(value)
  && Object.keys(value).length === expected.length && expected.every(key => Object.hasOwn(value, key));
const finite = value => typeof value === 'number' && Number.isFinite(value);
const hash = value => typeof value === 'string' && /^[a-f0-9]{64}$/.test(value);
const token = value => typeof value === 'string' && /^[A-Za-z0-9_-]{1,96}$/.test(value);
const instant = value => {
  if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/.test(value)) return false;
  const parsed = new Date(value);
  return Number.isFinite(parsed.getTime()) && parsed.toISOString().replace('.000Z', 'Z') === value;
};
const known = (value, vocabulary) => vocabulary.includes(value);
const fail = () => { throw new Error('INVALID_S1_INTAKE'); };

export function parseIntake(text) {
  // Native JSON.parse cannot attest duplicate-key rejection: this boundary accepts
  // objects only through the strict parser below, retaining the source externally.
  if (typeof text !== 'string' || Buffer.byteLength(text, 'utf8') > 65536) fail();
  let offset = 0;
  const whitespace = () => { while (/[ \t\r\n]/.test(text[offset] ?? '') && offset < text.length) offset++; };
  const string = () => {
    const start = offset++;
    while (offset < text.length) {
      if (text[offset] === '\\') { offset += 2; continue; }
      if (text[offset++] === '"') return JSON.parse(text.slice(start, offset));
    }
    fail();
  };
  let count = 0;
  const value = depth => {
    if (depth > 12 || ++count > 4096) fail();
    whitespace();
    if (text[offset] === '"') return string();
    if (text[offset] === '{') {
      offset++; whitespace();
      const result = Object.create(null);
      if (text[offset] === '}') { offset++; return result; }
      while (offset < text.length) {
        whitespace(); if (text[offset] !== '"') fail();
        const key = string(); whitespace();
        if (Object.hasOwn(result, key) || text[offset++] !== ':') fail();
        result[key] = value(depth + 1); whitespace();
        const delimiter = text[offset++];
        if (delimiter === '}') return result;
        if (delimiter !== ',') fail();
      }
      fail();
    }
    if (text[offset] === '[') {
      offset++; whitespace(); const result = [];
      if (text[offset] === ']') { offset++; return result; }
      while (offset < text.length) {
        result.push(value(depth + 1)); whitespace();
        const delimiter = text[offset++];
        if (delimiter === ']') return result;
        if (delimiter !== ',') fail();
      }
      fail();
    }
    const match = /^(?:true|false|null|-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?)/.exec(text.slice(offset));
    if (!match) fail(); offset += match[0].length;
    const result = JSON.parse(match[0]); if (typeof result === 'number' && !finite(result)) fail();
    return result;
  };
  try {
    const result = value(0); whitespace(); if (offset !== text.length) fail();
    validateIntake(result); return result;
  } catch { fail(); }
}

export function validateIntake(input) {
  if (!keys(input, ['kind', 'classification', 'origin', 'asset', 'acquisition', 'passband', 'astrometry', 'processing', 'independentEvidence'])
      || input.kind !== CONTRACT || input.classification !== 'PRIVATE'
      || !known(input.origin, ['OBSERVATORY', 'EXTERNAL_RETROSPECTIVE', 'SYNTHETIC_TEST'])) fail();
  const a = input.asset;
  if (!keys(a, ['assetId', 'revision', 'sha256', 'byteSize', 'format', 'channels', 'linearity'])
      || !token(a.assetId) || !Number.isSafeInteger(a.revision) || a.revision < 1 || !hash(a.sha256)
      || !Number.isSafeInteger(a.byteSize) || a.byteSize < 1 || !known(a.format, ['FITS', 'XISF', 'TIFF', 'JPEG'])
      || !Number.isSafeInteger(a.channels) || a.channels < 1 || a.channels > 3
      || !known(a.linearity, ['VERIFIED_LINEAR', 'NONLINEAR', 'UNKNOWN'])) fail();
  const e = input.acquisition;
  if (!keys(e, ['status', 'intervals', 'evidenceSha256']) || !known(e.status, ['KNOWN', 'UNKNOWN'])
      || !Array.isArray(e.intervals) || e.intervals.length > 256) fail();
  if (e.status === 'UNKNOWN') {
    if (e.intervals.length || e.evidenceSha256 !== null) fail();
  } else {
    if (!e.intervals.length || !hash(e.evidenceSha256)) fail();
    let prior = null;
    for (const interval of e.intervals) {
      if (!keys(interval, ['startUtc', 'endUtc']) || !instant(interval.startUtc) || !instant(interval.endUtc)
          || interval.startUtc > interval.endUtc || (prior !== null && interval.startUtc <= prior)) fail();
      prior = interval.endUtc;
    }
  }
  const p = input.passband;
  if (!keys(p, ['name', 'class', 'responseSha256']) || !token(p.name)
      || !known(p.class, ['BROADBAND', 'NARROWBAND', 'PALETTE', 'UNKNOWN'])
      || !(p.responseSha256 === null || hash(p.responseSha256))) fail();
  const w = input.astrometry;
  if (!keys(w, ['status', 'frame', 'solutionSha256']) || !known(w.status, ['VERIFIED', 'HEADER_ONLY', 'UNKNOWN'])
      || !known(w.frame, ['ICRS', 'UNKNOWN']) || !(w.solutionSha256 === null || hash(w.solutionSha256))
      || (w.status === 'VERIFIED' && (w.frame !== 'ICRS' || !hash(w.solutionSha256)))) fail();
  const history = input.processing;
  if (!keys(history, ['lineage', 'journalSha256', 'measurementAlterations'])
      || !known(history.lineage, ['VERIFIED', 'DECLARED', 'UNKNOWN'])
      || !(history.journalSha256 === null || hash(history.journalSha256))
      || (history.lineage === 'VERIFIED' && !hash(history.journalSha256))
      || !Array.isArray(history.measurementAlterations) || history.measurementAlterations.length > 8
      || new Set(history.measurementAlterations).size !== history.measurementAlterations.length
      || !history.measurementAlterations.every(v => known(v, ['STRETCH', 'DENOISE', 'DECONVOLUTION', 'STAR_REMOVAL', 'PALETTE_MAPPING', 'UNKNOWN']))) fail();
  const frames = input.independentEvidence;
  if (!Array.isArray(frames) || frames.length > 256) fail();
  const identities = new Set([a.sha256]);
  for (const frame of frames) {
    if (!keys(frame, ['assetId', 'sha256', 'independence']) || !token(frame.assetId) || !hash(frame.sha256)
        || identities.has(frame.sha256) || !known(frame.independence, ['VERIFIED_DISJOINT', 'UNVERIFIED'])) fail();
    identities.add(frame.sha256);
  }
  // Structure does not prove any assertion or authorize a real analysis.
  return true;
}

export function inspectIntake(input) {
  validateIntake(input);
  const reasons = [];
  if (input.origin === 'SYNTHETIC_TEST') reasons.push('SYNTHETIC_NOT_REAL_EVIDENCE');
  if (input.asset.linearity !== 'VERIFIED_LINEAR') reasons.push('LINEARITY_NOT_VERIFIED');
  if (!['FITS', 'XISF'].includes(input.asset.format) || input.asset.channels !== 1) reasons.push('MEASUREMENT_INPUT_NOT_MONO_SCIENTIFIC');
  if (input.acquisition.status !== 'KNOWN') reasons.push('ACQUISITION_EPOCH_UNKNOWN');
  if (input.astrometry.status !== 'VERIFIED') reasons.push('ASTROMETRY_NOT_VERIFIED');
  if (input.passband.class === 'PALETTE' || input.passband.class === 'UNKNOWN') reasons.push('PASSBAND_NOT_MEASURABLE');
  if (input.passband.responseSha256 === null) reasons.push('PASSBAND_RESPONSE_UNKNOWN');
  if (input.processing.lineage !== 'VERIFIED') reasons.push('MEASUREMENT_LINEAGE_NOT_VERIFIED');
  if (input.processing.measurementAlterations.length) reasons.push('MEASUREMENT_ALTERED_OR_UNKNOWN');
  if (!input.independentEvidence.some(f => f.independence === 'VERIFIED_DISJOINT')) reasons.push('INDEPENDENT_CONFIRMATION_NOT_ESTABLISHED');
  return Object.freeze({kind: 'BKL051_S1_INTAKE_INSPECTION_V1', state: 'NO_ANALYSIS_EXECUTED',
    operationalGate: 'OWNER_CONTRACT_DECISIONS_PENDING', scientificClassification: 'NOT_EVALUATED',
    reasons: Object.freeze(reasons), structureOnly: true, externalRequests: 0});
}
