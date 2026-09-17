const ROOT_KEYS = new Set(['schemaVersion', 'projectionType', 'projectionId', 'generatedAtUtc', 'environment', 'authority', 'sourceContractRef', 'contextRef', 'sitePublicEvidenceRef', 'setupAvailabilityState', 'evidenceAvailabilityState', 'method', 'validity', 'facts', 'citations', 'provenance', 'limitations', 'boundary', 'projectionDigest']);
const METHOD_KEYS = new Set(['profileRef', 'methodId', 'methodVersion', 'adapterId', 'adapterVersion', 'outputFrame', 'refractionModel']);
const VALIDITY_KEYS = new Set(['fromUtc', 'toUtc']);
const FACT_KEYS = new Set(['factType', 'instantUtc', 'numericValue', 'instantValue', 'unit']);
const PROVENANCE_KEYS = new Set(['evidenceRef', 'fixtureRef', 'profileRef', 'evidenceClass']);
const BOUNDARY_KEYS = new Set(['publicationState', 'runtimeState', 'protectedSiteUsed', 'externalReferenceCalls', 'commandAuthority', 'safetyAuthority']);
const PROTECTED_KEYS = new Set(['latitudeDeg', 'longitudeDeg', 'elevationM', 'siteRecordRef', 'siteRecordDigest', 'assignmentRef', 'assignmentDigest', 'profileSourceSha256', 'dataDigest', 'inputDigest', 'outputDigest', 'contractDigest', 'rawLocator', 'absolutePath', 'uncPath', 'credential', 'secret', 'token']);
const FORBIDDEN_KEYS = new Set(['forecast', 'weatherForecast', 'weight', 'score', 'threshold', 'rank', 'ranking', 'targetOrder', 'readiness', 'goNoGo', 'safe', 'isSafe', 'scheduler', 'deviceCommand', 'command']);

const canonicalize = value => {
  if (value === null || typeof value !== 'object') return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(canonicalize).join(',')}]`;
  return `{${Object.keys(value).sort().map(key => `${JSON.stringify(key)}:${canonicalize(value[key])}`).join(',')}}`;
};

const sha256 = async value => {
  const bytes = new TextEncoder().encode(canonicalize(value));
  const digest = await crypto.subtle.digest('SHA-256', bytes);
  return [...new Uint8Array(digest)].map(byte => byte.toString(16).padStart(2, '0')).join('');
};

const fail = message => { throw new Error(message); };
const exactKeys = (value, expected, label) => {
  if (!value || typeof value !== 'object' || Array.isArray(value)) fail(`${label} non valido.`);
  const keys = Object.keys(value);
  if (keys.some(key => !expected.has(key)) || [...expected].some(key => !Object.hasOwn(value, key))) fail(`${label} contiene proprietà inattese o mancanti.`);
};

const inspectKeys = (value, path = 'projection') => {
  if (!value || typeof value !== 'object') return;
  if (Array.isArray(value)) return value.forEach((child, index) => inspectKeys(child, `${path}[${index}]`));
  for (const [key, child] of Object.entries(value)) {
    if (PROTECTED_KEYS.has(key)) fail(`${path}.${key} espone dati protetti.`);
    if (FORBIDDEN_KEYS.has(key)) fail(`${path}.${key} introduce una capability non autorizzata.`);
    inspectKeys(child, `${path}.${key}`);
  }
};

export async function validateObservationPlannerProjection(projection) {
  exactKeys(projection, ROOT_KEYS, 'Projection');
  if (projection.schemaVersion !== '1.0' || projection.projectionType !== 'BKL031_F3C_BOUNDED_SANITIZED_PROJECTION') fail('Identità della projection non valida.');
  if (!/^BKL031-F3C-[0-9A-F]{24}$/.test(projection.projectionId)) fail('Identificativo projection non valido.');
  if (projection.environment !== 'TEST' || projection.authority !== 'NONE') fail('La projection pubblica deve restare TEST/NONE.');
  if (!Array.isArray(projection.facts) || projection.facts.length < 1 || projection.facts.length > 72) fail('Numero di fatti fuori limite.');
  exactKeys(projection.method, METHOD_KEYS, 'Metodo');
  if (!projection.method || projection.method.adapterId !== 'BKL031-F3C-BOUNDED-ADAPTER' || projection.method.adapterVersion !== '1.0') fail('Identità adapter non valida.');
  if (projection.method.outputFrame !== 'TOPOCENTRIC_ALTAZ' || projection.method.refractionModel !== 'AIRLESS') fail('Semantica di output non valida.');
  exactKeys(projection.validity, VALIDITY_KEYS, 'Validità');
  if (!projection.validity || Date.parse(projection.validity.fromUtc) >= Date.parse(projection.validity.toUtc)) fail('Intervallo di validità non valido.');
  projection.facts.forEach((fact, index) => exactKeys(fact, FACT_KEYS, `Fatto ${index}`));
  if (!Array.isArray(projection.citations) || projection.citations.length !== 2 || new Set(projection.citations).size !== 2) fail('Citation non valide.');
  exactKeys(projection.provenance, PROVENANCE_KEYS, 'Provenance');
  if (projection.provenance.evidenceClass !== 'SYNTHETIC_VALIDATION') fail('Classe evidence non valida.');
  if (!Array.isArray(projection.limitations) || projection.limitations.length !== 4 || !projection.limitations.includes('S10_RUNTIME_UNAVAILABLE')) fail('Limitazioni della projection non valide.');
  exactKeys(projection.boundary, BOUNDARY_KEYS, 'Boundary');
  if (!projection.boundary || projection.boundary.publicationState !== 'TEST_ONLY' || projection.boundary.runtimeState !== 'UNAVAILABLE') fail('Boundary di pubblicazione/runtime non valida.');
  if (projection.boundary.protectedSiteUsed !== false || projection.boundary.externalReferenceCalls !== 0 || projection.boundary.commandAuthority !== 'NONE' || projection.boundary.safetyAuthority !== 'LOCAL_PHYSICAL_INTERLOCKS') fail('Boundary di sicurezza o autorità non valida.');
  inspectKeys(projection);
  const { projectionDigest, ...payload } = projection;
  if (!/^[0-9a-f]{64}$/.test(projectionDigest) || await sha256(payload) !== projectionDigest) fail('Digest della projection non valido.');
  return true;
}
