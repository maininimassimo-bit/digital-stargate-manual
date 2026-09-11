const requiredLimitations = [
  'EXPERIMENTAL_F4_NOT_ACCEPTED_FOR_PRODUCTION_USE',
  'SYNTHETIC_DEMONSTRATOR_PROFILE_NOT_SCIENTIFIC_CALIBRATION',
  'NO_RANKING_THRESHOLD_RECOMMENDATION_OR_AUTOMATIC_ACCEPTANCE',
  'NO_SAFETY_OR_ACTION_AUTHORITY'
];

const assert = (condition, message) => { if (!condition) throw new Error(message); };
const nonEmpty = value => typeof value === 'string' && value.trim().length > 0;

export function canonicalJson(value) {
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(',')}]`;
  if (value && typeof value === 'object') {
    return `{${Object.keys(value).sort().map(key => `${JSON.stringify(key)}:${canonicalJson(value[key])}`).join(',')}}`;
  }
  return JSON.stringify(value);
}

export async function sha256(value) {
  assert(globalThis.crypto?.subtle && globalThis.TextEncoder, 'Web Crypto SHA-256 non disponibile');
  const bytes = new TextEncoder().encode(canonicalJson(value));
  const digest = await crypto.subtle.digest('SHA-256', bytes);
  return [...new Uint8Array(digest)].map(byte => byte.toString(16).padStart(2, '0')).join('');
}

export function validateProjectionContract(projection) {
  assert(projection?.schemaVersion === '1.0', 'schema version non supportata');
  assert(projection?.projectionType === 'SCIENTIFIC_DATA_QUALITY_PROJECTION', 'projection type non valido');
  assert(projection?.projectionState === 'EXPERIMENTAL_NOT_ACCEPTED', 'projection lifecycle non valido');
  assert(projection?.profile?.profileId === 'DSG-SCIENTIFIC-QUALITY-SYNTHETIC-DEMONSTRATOR', 'profilo non autorizzato');
  assert(projection?.profile?.profileVersion === '1.0.0-f3', 'versione profilo non autorizzata');
  assert(projection?.authority?.consumerMode === 'READ_ONLY', 'consumer mode non read-only');
  assert(projection?.authority?.productionUseAuthorized === false, 'production authority drift');
  assert(projection?.authority?.acceptanceAuthority === false, 'acceptance authority drift');
  assert(projection?.authority?.actionAuthority === 'NONE', 'action authority drift');
  assert(projection?.authority?.safetyAuthority === 'LOCAL_PHYSICAL_INTERLOCKS', 'Safety Authority drift');
  assert(Array.isArray(projection.assessments) && Array.isArray(projection.limitations), 'projection incompleta');
  assert(requiredLimitations.every(item => projection.limitations.includes(item)), 'limitations di authority mancanti');
  assert(projection.sourceCatalog?.path === 'docs/data/scientific-session-catalog.json', 'source catalog non autorizzato');
  assert(Array.isArray(projection.sourceCatalog?.sessionIds), 'session identity snapshot mancante');
  assert(/^[a-f0-9]{64}$/.test(projection.sourceCatalog?.digest ?? ''), 'source catalog digest non valido');
  assert(/^[a-f0-9]{64}$/.test(projection.projectionDigest ?? ''), 'projection digest non valido');
  for (const record of projection.assessments) {
    assert(nonEmpty(record.sessionId), 'assessment sessionId mancante');
    assert(['AVAILABLE', 'UNAVAILABLE', 'INVALID'].includes(record.projectionRecordState), 'assessment state non valido');
    if (record.projectionRecordState === 'AVAILABLE') {
      assert(record.assessment?.score && record.assessment?.confidence && Array.isArray(record.assessment?.decomposition), 'assessment disponibile incompleto');
    }
    if (record.projectionRecordState === 'INVALID') assert(record.assessment === null && nonEmpty(record.generationError?.code), 'record invalid non spiegato');
  }
  return true;
}

export async function validateProjectionFreshness(projection, catalog) {
  validateProjectionContract(projection);
  assert(catalog?.catalogStatus === 'VERSIONED_ANALYTICS_PROJECTION', 'catalog authority/status non valido');
  assert(Array.isArray(catalog.sessions), 'catalog sessions mancante');
  const catalogDigest = await sha256(catalog);
  assert(catalogDigest === projection.sourceCatalog.digest, 'STALE_SOURCE_CATALOG_DIGEST_MISMATCH');
  const ids = catalog.sessions.map(item => item.sessionId).sort();
  assert(JSON.stringify(ids) === JSON.stringify(projection.sourceCatalog.sessionIds), 'STALE_SESSION_SET_MISMATCH');
  assert(ids.length === projection.summary.totalSessions, 'STALE_SESSION_COUNT_MISMATCH');
  const projectionPreimage = structuredClone(projection);
  delete projectionPreimage.projectionDigest;
  assert(await sha256(projectionPreimage) === projection.projectionDigest, 'PROJECTION_DIGEST_MISMATCH');
  return true;
}

export async function validateRealEvidenceFreshness(validation, projection, catalog) {
  assert(validation?.schemaVersion === '1.0', 'F5 validation schema non supportato');
  assert(validation?.validationType === 'SCIENTIFIC_DATA_QUALITY_REAL_EVIDENCE_VALIDATION', 'F5 validation type non valido');
  assert(validation?.validationState === 'COMPLETE', 'F5 validation incompleta');
  assert(validation?.decision?.capabilityAcceptance === 'ACCEPTED_AS_READ_ONLY_EXPERIMENTAL_WITH_RETAINED_LIMITATIONS', 'capability acceptance non autorizzata');
  assert(validation?.decision?.productionReadiness === 'NOT_READY_FOR_PRODUCTION', 'production readiness non supportata dalla evidence corrente');
  assert(validation?.decision?.productionProfileAuthorized === false, 'production profile authority drift');
  assert(validation?.decision?.productionUseAuthorized === false, 'production use authority drift');
  assert(validation?.authority?.consumerMode === 'READ_ONLY', 'F5 consumer mode non read-only');
  assert(validation?.authority?.acceptanceAuthority === false, 'F5 acceptance authority drift');
  assert(validation?.authority?.actionAuthority === 'NONE', 'F5 action authority drift');
  assert(validation?.authority?.safetyAuthority === 'LOCAL_PHYSICAL_INTERLOCKS', 'F5 Safety Authority drift');
  assert(validation?.acceptancePolicy?.purpose === 'PRODUCTION_CALIBRATION_READINESS_NOT_SCIENTIFIC_QUALITY_THRESHOLD', 'readiness policy semantic drift');
  assert(Array.isArray(validation.results) && validation.results.length > 0, 'F5 readiness results mancanti');
  assert(validation.sourceCatalog?.digest === await sha256(catalog), 'STALE_F5_CATALOG_DIGEST_MISMATCH');
  assert(validation.sourceProjection?.digest === projection.projectionDigest, 'STALE_F5_PROJECTION_DIGEST_MISMATCH');
  assert(JSON.stringify(validation.sourceCatalog.sessionIds) === JSON.stringify(projection.sourceCatalog.sessionIds), 'STALE_F5_SESSION_SET_MISMATCH');
  const preimage = structuredClone(validation);
  delete preimage.validationDigest;
  assert(await sha256(preimage) === validation.validationDigest, 'F5_VALIDATION_DIGEST_MISMATCH');
  return true;
}
