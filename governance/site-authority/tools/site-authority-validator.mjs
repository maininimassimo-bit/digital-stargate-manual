import { createHash } from "node:crypto";
import { readFile, readdir } from "node:fs/promises";
import { extname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

export const CANONICALIZATION_METHOD = "DSG-F3A1-CANONICAL-JSON-SHA256-1";
export const PUBLIC_ALLOWLIST = Object.freeze([
  "publicSiteRef",
  "publicEvidenceDigest",
  "siteLabelGeneralized",
  "timezoneDisplay",
  "availabilityState",
  "reasonCode",
  "asOfUtc",
  "provenance",
]);

const FORBIDDEN_PUBLIC_KEYS = new Set([
  "siteRecordId",
  "observatoryId",
  "recordDigestInternal",
  "latitudeDeg",
  "longitudeDeg",
  "elevationM",
  "sourceLocator",
  "ownerRef",
  "custodianRef",
  "approvalAuthorityRef",
  "conflictEvidenceRef",
]);

const SENTINEL_ENDS = new Set([
  "9999-12-31T23:59:59Z",
  "9999-12-31T23:59:59.999Z",
]);

function isObject(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function isFiniteNumber(value) {
  return typeof value === "number" && Number.isFinite(value);
}

function hasExactKeys(value, expected) {
  if (!isObject(value)) return false;
  const actual = Object.keys(value).sort();
  const wanted = [...expected].sort();
  return actual.length === wanted.length && actual.every((key, index) => key === wanted[index]);
}

function sameStringSet(actual, expected) {
  return Array.isArray(actual) && actual.length === expected.length && [...actual].sort().every((key, index) => key === [...expected].sort()[index]);
}

function assertClosedSchemaNode(node, expectedRequired) {
  if (!isObject(node) || node.additionalProperties !== false || !sameStringSet(node.required, expectedRequired) || !sameStringSet(Object.keys(node.properties ?? {}), expectedRequired)) {
    throw new Error("SITE_AUTHORITY_SCHEMA_VALIDATOR_PARITY_FAILED");
  }
}

export function assertSchemaValidatorParity(recordSchema, decisionSchema, approvalSchema) {
  assertClosedSchemaNode(recordSchema, ["schemaVersion", "recordType", "lifecycle", "sitePayload", "payloadDigest", "validationEvidence"]);
  assertClosedSchemaNode(recordSchema.properties.lifecycle, ["state", "eligibleForResolution", "approvalEvidenceRef", "approvedAtUtc", "retiredAtUtc", "decisionEvidenceRef", "statement"]);
  assertClosedSchemaNode(recordSchema.$defs.sitePayload, ["siteRecordId", "observatoryId", "revision", "scope", "geodesy", "timezoneIana", "authority", "source", "validity", "classification", "retention", "publicationPolicy", "intendedUse", "prohibitedUses", "rollback"]);
  assertClosedSchemaNode(recordSchema.$defs.geodesy, ["datum", "latitudeDeg", "longitudeDeg", "coordinateFormat", "elevationM", "elevationUnit", "elevationReference", "acceptedElevationRangeM"]);
  assertClosedSchemaNode(recordSchema.$defs.authority, ["authoritySystem", "repository", "registryRoot", "authorityScope", "authorityRole", "ownerRef", "custodianRef", "approvalAuthorityRef", "custodianMayApprove"]);
  assertClosedSchemaNode(recordSchema.$defs.source, ["sourceKind", "application", "sourceLocator", "attestedByRef", "attestationChannel", "sourceAuthority"]);
  assertClosedSchemaNode(recordSchema.$defs.validity, ["validFromUtc", "validityEndMode", "validToUtc", "intervalSemantics"]);
  assertClosedSchemaNode(recordSchema.$defs.publicationPolicy, ["exactCoordinates", "elevation", "exactAddress", "siteLabelGeneralized", "timezoneDisplay", "publicRefPolicy", "publicDigestPolicy"]);
  assertClosedSchemaNode(recordSchema.$defs.payloadDigest, ["method", "canonicalization", "algorithm", "value"]);
  assertClosedSchemaNode(recordSchema.properties.validationEvidence, ["jsonParse", "schemaValidatorParity", "payloadDigestRecomputation", "protectedValueLeakScan", "executableContractCases", "runtimeOat"]);
  assertClosedSchemaNode(decisionSchema, ["schemaVersion", "recordType", "decisionId", "decision", "decisionRecordedAtUtc", "decidingAuthority", "candidateRef", "decisions", "sourceAuthorization", "lifecycleBoundary"]);
  assertClosedSchemaNode(approvalSchema, ["schemaVersion", "recordType", "receiptId", "decision", "subject", "approvingAuthority", "approval", "repositoryEvidence", "scopeBoundaries", "integrity"]);
  return { valid: true };
}

function isUtcTimestamp(value) {
  if (typeof value !== "string" || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?Z$/.test(value)) return false;
  const parsed = Date.parse(value);
  return Number.isFinite(parsed);
}

function isKnownIanaTimezone(value) {
  if (typeof value !== "string" || value.length === 0 || /^[+-]\d\d:\d\d$/.test(value)) return false;
  try {
    new Intl.DateTimeFormat("en", { timeZone: value }).format(new Date(0));
    return true;
  } catch {
    return false;
  }
}

export function canonicalize(value) {
  if (Array.isArray(value)) return `[${value.map(canonicalize).join(",")}]`;
  if (isObject(value)) {
    return `{${Object.keys(value)
      .sort()
      .map((key) => `${JSON.stringify(key)}:${canonicalize(value[key])}`)
      .join(",")}}`;
  }
  return JSON.stringify(value);
}

export function digestPayload(payload) {
  return `sha256:${createHash("sha256").update(canonicalize(payload), "utf8").digest("hex")}`;
}

function validateValidity(validity, errors) {
  if (!isObject(validity)) {
    errors.push("INVALID_VALIDITY_INTERVAL");
    return;
  }
  if (!hasExactKeys(validity, ["validFromUtc", "validityEndMode", "validToUtc", "intervalSemantics"])) errors.push("INVALID_SCHEMA_SHAPE");
  const { validFromUtc, validityEndMode, validToUtc, intervalSemantics } = validity;
  if (!isUtcTimestamp(validFromUtc) || intervalSemantics !== "HALF_OPEN") {
    errors.push("INVALID_VALIDITY_INTERVAL");
  }
  if (validityEndMode === "EXCLUSIVE") {
    if (!isUtcTimestamp(validToUtc) || SENTINEL_ENDS.has(validToUtc) || Date.parse(validToUtc) <= Date.parse(validFromUtc)) {
      errors.push("INVALID_VALIDITY_INTERVAL");
    }
  } else if (validityEndMode === "UNBOUNDED") {
    if (validToUtc !== null) errors.push("INVALID_VALIDITY_INTERVAL");
  } else {
    errors.push("INVALID_VALIDITY_INTERVAL");
  }
}

function validateLifecycle(lifecycle, errors) {
  if (!isObject(lifecycle) || !["DRAFT", "APPROVED", "RETIRED"].includes(lifecycle.state)) {
    errors.push("INVALID_LIFECYCLE");
    return;
  }
  if (!hasExactKeys(lifecycle, ["state", "eligibleForResolution", "approvalEvidenceRef", "approvedAtUtc", "retiredAtUtc", "decisionEvidenceRef", "statement"])) errors.push("INVALID_SCHEMA_SHAPE");
  if (typeof lifecycle.decisionEvidenceRef !== "string" || lifecycle.decisionEvidenceRef.length === 0 || typeof lifecycle.statement !== "string" || lifecycle.statement.length === 0) errors.push("INVALID_LIFECYCLE");
  if (typeof lifecycle.eligibleForResolution !== "boolean") errors.push("INVALID_LIFECYCLE");
  if (lifecycle.state === "DRAFT" && lifecycle.eligibleForResolution) errors.push("INVALID_LIFECYCLE");
  if (lifecycle.state === "APPROVED") {
    if (!lifecycle.eligibleForResolution || typeof lifecycle.approvalEvidenceRef !== "string" || !isUtcTimestamp(lifecycle.approvedAtUtc)) {
      errors.push("INVALID_APPROVAL_EVIDENCE");
    }
  }
  if (lifecycle.state === "RETIRED") {
    if (lifecycle.eligibleForResolution || !isUtcTimestamp(lifecycle.retiredAtUtc)) errors.push("INVALID_LIFECYCLE");
  }
}

function validateAuthority(authority, errors) {
  if (!isObject(authority)) {
    errors.push("INVALID_AUTHORITY");
    return;
  }
  if (!hasExactKeys(authority, ["authoritySystem", "repository", "registryRoot", "authorityScope", "authorityRole", "ownerRef", "custodianRef", "approvalAuthorityRef", "custodianMayApprove"])) errors.push("INVALID_SCHEMA_SHAPE");
  const required = ["authorityRole", "ownerRef", "custodianRef", "approvalAuthorityRef", "authoritySystem", "authorityScope"];
  if (required.some((key) => typeof authority[key] !== "string" || authority[key].length === 0)) errors.push("INVALID_AUTHORITY");
  if (authority.custodianMayApprove !== false) errors.push("INVALID_AUTHORITY");
  if (authority.authoritySystem !== "GITHUB_REPOSITORY_PROTECTED_REGISTRY" || authority.repository !== "maininimassimo-bit/digital-stargate-manual" || authority.registryRoot !== "governance/site-authority" || authority.authorityScope !== "SINGLE_OBSERVATORY" || authority.authorityRole !== "SITE_AUTHORITY") errors.push("INVALID_AUTHORITY");
  if (authority.ownerRef !== "github:user:maininimassimo-bit" || authority.custodianRef !== "role:digital-stargate-architecture-office" || authority.approvalAuthorityRef !== "github:user:maininimassimo-bit") errors.push("INVALID_AUTHORITY");
}

function validateSitePayload(payload, errors) {
  if (!isObject(payload)) {
    errors.push("INVALID_SITE_SEMANTICS");
    return;
  }
  if (typeof payload.siteRecordId !== "string" || typeof payload.observatoryId !== "string") errors.push("INVALID_IDENTITY");
  if (!hasExactKeys(payload, ["siteRecordId", "observatoryId", "revision", "scope", "geodesy", "timezoneIana", "authority", "source", "validity", "classification", "retention", "publicationPolicy", "intendedUse", "prohibitedUses", "rollback"])) errors.push("INVALID_SCHEMA_SHAPE");
  if (payload.observatoryId !== "DSG-OBSERVATORY-MANCIANO-001" || payload.scope !== "OBSERVATION_PLANNER_READ_ONLY_SITE_AUTHORITY") errors.push("INVALID_IDENTITY");
  if (!Number.isInteger(payload.revision) || payload.revision < 1) errors.push("INVALID_REVISION");
  const geo = payload.geodesy;
  if (!isObject(geo) || geo.datum !== "WGS84") {
    errors.push("INVALID_SITE_SEMANTICS");
  } else {
    if (!hasExactKeys(geo, ["datum", "latitudeDeg", "longitudeDeg", "coordinateFormat", "elevationM", "elevationUnit", "elevationReference", "acceptedElevationRangeM"])) errors.push("INVALID_SCHEMA_SHAPE");
    if (geo.coordinateFormat !== "DECIMAL_DEGREES") errors.push("INVALID_SITE_SEMANTICS");
    if (!isFiniteNumber(geo.latitudeDeg) || geo.latitudeDeg < -90 || geo.latitudeDeg > 90) errors.push("INVALID_SITE_SEMANTICS");
    if (!isFiniteNumber(geo.longitudeDeg) || geo.longitudeDeg < -180 || geo.longitudeDeg >= 180) errors.push("INVALID_SITE_SEMANTICS");
    if (!isFiniteNumber(geo.elevationM)) errors.push("INVALID_SITE_SEMANTICS");
    if (geo.elevationReference !== "ORTHOMETRIC_MEAN_SEA_LEVEL" || geo.elevationUnit !== "m") errors.push("INVALID_SITE_SEMANTICS");
    const range = geo.acceptedElevationRangeM;
    if (isObject(range) && !hasExactKeys(range, ["minInclusive", "maxInclusive"])) errors.push("INVALID_SCHEMA_SHAPE");
    if (!isObject(range) || !isFiniteNumber(range.minInclusive) || !isFiniteNumber(range.maxInclusive) || range.minInclusive !== -500 || range.maxInclusive !== 9000 || geo.elevationM < range.minInclusive || geo.elevationM > range.maxInclusive) {
      errors.push("INVALID_SITE_SEMANTICS");
    }
  }
  if (!isKnownIanaTimezone(payload.timezoneIana) || payload.timezoneIana !== "Europe/Rome") errors.push("INVALID_SITE_SEMANTICS");
  validateAuthority(payload.authority, errors);
  const source = payload.source;
  if (!hasExactKeys(source, ["sourceKind", "application", "sourceLocator", "attestedByRef", "attestationChannel", "sourceAuthority"])) errors.push("INVALID_SCHEMA_SHAPE");
  if (!isObject(source) || source.sourceKind !== "OWNER_ATTESTED_APPLICATION_CONFIGURATION" || source.application !== "N.I.N.A." || typeof source.sourceLocator !== "string" || source.sourceLocator.length === 0 || source.attestedByRef !== "github:user:maininimassimo-bit" || source.attestationChannel !== "OWNER_CONTROLLED_INTERACTION_CHANNEL" || source.sourceAuthority !== "HUMAN_REPOSITORY_OWNER_ATTESTATION") errors.push("INVALID_SOURCE");
  validateValidity(payload.validity, errors);
  if (payload.classification !== "PROTECTED_EXACT_SITE") errors.push("INVALID_CLASSIFICATION");
  if (payload.retention !== "REPOSITORY_HISTORY_UNBOUNDED") errors.push("INVALID_RETENTION");
  const policy = payload.publicationPolicy;
  if (isObject(policy) && !hasExactKeys(policy, ["exactCoordinates", "elevation", "exactAddress", "siteLabelGeneralized", "timezoneDisplay", "publicRefPolicy", "publicDigestPolicy"])) errors.push("INVALID_SCHEMA_SHAPE");
  if (!isObject(policy) || policy.exactCoordinates !== "PROHIBITED" || policy.elevation !== "PROHIBITED" || policy.exactAddress !== "PROHIBITED") {
    errors.push("INVALID_PUBLICATION_POLICY");
  }
  if (isObject(policy) && (policy.siteLabelGeneralized !== "Manciano (GR), Italia" || policy.timezoneDisplay !== "Europe/Rome" || policy.publicRefPolicy !== "INDEPENDENT_OPAQUE_IDENTIFIER" || policy.publicDigestPolicy !== "PUBLIC_PAYLOAD_ONLY")) errors.push("INVALID_PUBLICATION_POLICY");
  const prohibited = new Set(payload.prohibitedUses ?? []);
  for (const required of ["DEVICE_COMMAND", "SAFETY_AUTHORITY", "READINESS_OR_GO_NO_GO", "PUBLIC_EXACT_SITE_PROJECTION", "EAGLE_WORKLOAD"]) {
    if (!prohibited.has(required)) errors.push("INVALID_BOUNDARY");
  }
  if (payload.intendedUse !== "OBSERVATION_PLANNER_READ_ONLY_SITE_CONTEXT_AFTER_SEPARATE_APPROVAL") errors.push("INVALID_BOUNDARY");
  if (!isObject(payload.rollback) || !hasExactKeys(payload.rollback, ["draft", "futureApproval"]) || Object.values(payload.rollback).some((value) => typeof value !== "string" || value.length === 0)) errors.push("INVALID_ROLLBACK");
}

function validateEvidence(validationEvidence, errors) {
  const keys = ["jsonParse", "schemaValidatorParity", "payloadDigestRecomputation", "protectedValueLeakScan", "executableContractCases", "runtimeOat"];
  if (!hasExactKeys(validationEvidence, keys)) {
    errors.push("INVALID_VALIDATION_EVIDENCE");
    return;
  }
  for (const value of Object.values(validationEvidence)) {
    if (!isObject(value) || !["VERIFIED", "NOT_EXECUTED", "NOT_APPLICABLE"].includes(value.state)) errors.push("INVALID_VALIDATION_EVIDENCE");
    if (isObject(value) && Object.keys(value).some((key) => !["state", "evidence", "reason"].includes(key))) errors.push("INVALID_SCHEMA_SHAPE");
  }
}

export function validateRecord(record) {
  const errors = [];
  if (!isObject(record) || record.schemaVersion !== "1.0.0-draft" || record.recordType !== "DSG_GOVERNED_SITE_RECORD") {
    return { valid: false, errors: ["INVALID_SCHEMA_ENVELOPE"] };
  }
  if (!hasExactKeys(record, ["schemaVersion", "recordType", "lifecycle", "sitePayload", "payloadDigest", "validationEvidence"])) errors.push("INVALID_SCHEMA_SHAPE");
  validateLifecycle(record.lifecycle, errors);
  validateSitePayload(record.sitePayload, errors);
  const digest = record.payloadDigest;
  if (!hasExactKeys(digest, ["method", "canonicalization", "algorithm", "value"])) errors.push("INVALID_SCHEMA_SHAPE");
  if (!isObject(digest) || digest.method !== CANONICALIZATION_METHOD || digest.canonicalization !== "recursive object-key sort; array order preserved; compact JSON; UTF-8" || digest.algorithm !== "SHA-256" || digest.value !== digestPayload(record.sitePayload)) {
    errors.push("INTEGRITY_FAILURE");
  }
  validateEvidence(record.validationEvidence, errors);
  return { valid: errors.length === 0, errors: [...new Set(errors)] };
}

export function validateDecisionEvidence(decision) {
  const errors = [];
  const keys = ["schemaVersion", "recordType", "decisionId", "decision", "decisionRecordedAtUtc", "decidingAuthority", "candidateRef", "decisions", "sourceAuthorization", "lifecycleBoundary"];
  if (!hasExactKeys(decision, keys)) errors.push("INVALID_DECISION_SCHEMA");
  if (decision?.schemaVersion !== "1.0.0-draft" || decision?.recordType !== "DSG_SITE_SOURCE_DECISION_EVIDENCE" || decision?.decision !== "AUTHORIZED_FOR_DRAFT_MATERIALIZATION" || decision?.lifecycleBoundary !== "NOT_AN_EXACT_DIGEST_APPROVAL") errors.push("INVALID_DECISION");
  if (!isUtcTimestamp(decision?.decisionRecordedAtUtc) || decision?.decidingAuthority !== "github:user:maininimassimo-bit" || typeof decision?.candidateRef !== "string" || !isObject(decision?.decisions) || !isObject(decision?.sourceAuthorization)) errors.push("INVALID_DECISION");
  if (decision?.sourceAuthorization?.exactValuesStoredOnlyInCandidate !== true || decision?.sourceAuthorization?.sourceApplication !== "N.I.N.A." || decision?.sourceAuthorization?.sourceChannel !== "OWNER_CONTROLLED_INTERACTION_CHANNEL") errors.push("INVALID_DECISION");
  return { valid: errors.length === 0, errors: [...new Set(errors)] };
}

function intervalContains(validity, instant) {
  const t = Date.parse(instant);
  if (!Number.isFinite(t) || !isUtcTimestamp(instant)) return false;
  const start = Date.parse(validity.validFromUtc);
  if (t < start) return false;
  return validity.validityEndMode === "UNBOUNDED" || t < Date.parse(validity.validToUtc);
}

function intervalsOverlap(left, right) {
  const leftStart = Date.parse(left.validFromUtc);
  const rightStart = Date.parse(right.validFromUtc);
  const leftEnd = left.validityEndMode === "UNBOUNDED" ? Infinity : Date.parse(left.validToUtc);
  const rightEnd = right.validityEndMode === "UNBOUNDED" ? Infinity : Date.parse(right.validToUtc);
  return Math.max(leftStart, rightStart) < Math.min(leftEnd, rightEnd);
}

export function resolveSiteAuthority(records, { observatoryId, asOfUtc, authorized = false } = {}) {
  if (!isUtcTimestamp(asOfUtc)) return { state: "INVALID", reasonCode: "INVALID_VALIDITY_INTERVAL" };
  const sameAuthority = records.filter((record) => record?.sitePayload?.observatoryId === observatoryId);
  const invalidApproved = sameAuthority.find((record) => record?.lifecycle?.state === "APPROVED" && !validateRecord(record).valid);
  if (invalidApproved) {
    const result = validateRecord(invalidApproved);
    return { state: "INVALID", reasonCode: result.errors.includes("INTEGRITY_FAILURE") ? "INTEGRITY_FAILURE" : "INVALID_SITE_SEMANTICS" };
  }
  const eligible = sameAuthority.filter((record) => record.lifecycle.state === "APPROVED" && record.lifecycle.eligibleForResolution);
  for (let i = 0; i < eligible.length; i += 1) {
    for (let j = i + 1; j < eligible.length; j += 1) {
      if (intervalsOverlap(eligible[i].sitePayload.validity, eligible[j].sitePayload.validity) && intervalContains(eligible[i].sitePayload.validity, asOfUtc) && intervalContains(eligible[j].sitePayload.validity, asOfUtc)) {
        return { state: "CONFLICTED", reasonCode: "OVERLAPPING_APPROVED_INTERVALS" };
      }
    }
  }
  const current = eligible.filter((record) => intervalContains(record.sitePayload.validity, asOfUtc));
  if (current.length === 0) {
    const hasBeforeAndAfter = eligible.some((record) => Date.parse(record.sitePayload.validity.validFromUtc) > Date.parse(asOfUtc)) && eligible.some((record) => {
      const end = record.sitePayload.validity.validityEndMode === "UNBOUNDED" ? Infinity : Date.parse(record.sitePayload.validity.validToUtc);
      return end <= Date.parse(asOfUtc);
    });
    return { state: "UNAVAILABLE", reasonCode: hasBeforeAndAfter ? "VALIDITY_GAP" : "NO_APPROVED_INTERVAL" };
  }
  if (!authorized) return { state: "UNAVAILABLE", reasonCode: "ACCESS_DENIED", audit: true };
  return { state: "AVAILABLE", reasonCode: "APPROVED_INTERVAL", site: current[0].sitePayload };
}

export function assertPublicPayload(payload, internalRecord) {
  if (!isObject(payload)) return { valid: false, reasonCode: "PUBLIC_PROJECTION_POLICY" };
  const keys = Object.keys(payload);
  if (keys.some((key) => !PUBLIC_ALLOWLIST.includes(key) || FORBIDDEN_PUBLIC_KEYS.has(key))) return { valid: false, reasonCode: "PUBLIC_PROJECTION_POLICY" };
  const serialized = JSON.stringify(payload);
  const internal = internalRecord?.sitePayload;
  const forbiddenValues = [internal?.siteRecordId, internal?.observatoryId, internalRecord?.payloadDigest?.value, internal?.source?.sourceLocator]
    .filter((value) => typeof value === "string" && value.length > 0);
  if (forbiddenValues.some((value) => serialized.includes(value))) return { valid: false, reasonCode: "PUBLIC_PROJECTION_POLICY" };
  return { valid: true };
}

export function buildPublicReference(record, { publicSiteRef, asOfUtc }) {
  const internalValues = [record.sitePayload.siteRecordId, record.sitePayload.observatoryId, record.payloadDigest.value];
  if (typeof publicSiteRef !== "string" || !publicSiteRef.startsWith("PUBLIC-SITE-") || internalValues.some((value) => publicSiteRef.includes(value))) {
    throw new Error("PUBLIC_PROJECTION_POLICY");
  }
  const payload = {
    publicSiteRef,
    siteLabelGeneralized: record.sitePayload.publicationPolicy.siteLabelGeneralized,
    timezoneDisplay: record.sitePayload.publicationPolicy.timezoneDisplay,
    availabilityState: record.lifecycle.state === "APPROVED" ? "AVAILABLE" : "UNAVAILABLE",
    reasonCode: record.lifecycle.state === "APPROVED" ? "APPROVED_INTERVAL" : "NO_APPROVED_INTERVAL",
    asOfUtc,
    provenance: "GOVERNED_SITE_AUTHORITY_SANITIZED",
  };
  payload.publicEvidenceDigest = digestPayload(payload);
  if (!assertPublicPayload(payload, record).valid) throw new Error("PUBLIC_PROJECTION_POLICY");
  return payload;
}

export function redactAuditEvent(event) {
  const result = {};
  for (const [key, value] of Object.entries(event ?? {})) {
    if (!FORBIDDEN_PUBLIC_KEYS.has(key) && !["coordinates", "locator", "internalDigest"].includes(key)) result[key] = value;
  }
  return result;
}

export function assertBoundarySource(source) {
  const violations = [];
  if (/from\s+["'](?:node:)?(?:fs|path|sqlite|pg|mysql)/.test(source)) violations.push("DOMAIN_INFRASTRUCTURE_DEPENDENCY");
  if (/Astropy|Skyfield|JPL Horizons/.test(source)) violations.push("EPHEMERIS_PROVIDER_SCOPE");
  if (/readiness|go[-_ ]?no[-_ ]?go|deviceCommand|roofCommand/i.test(source)) violations.push("SAFETY_OR_COMMAND_SCOPE");
  if (/EAGLE_WORKLOAD_REQUIRED|runOnEagle\s*:\s*true/.test(source)) violations.push("EAGLE_SCOPE");
  return { valid: violations.length === 0, violations };
}

async function walkTextFiles(root) {
  const result = [];
  async function visit(directory) {
    for (const entry of await readdir(directory, { withFileTypes: true })) {
      const full = join(directory, entry.name);
      if (entry.isDirectory()) await visit(full);
      else if ([".md", ".json", ".js", ".mjs", ".yml", ".yaml", ".html", ".css"].includes(extname(entry.name))) result.push(full);
    }
  }
  await visit(root);
  return result;
}

export async function verifyProtectedValuesAbsentFromDocs(record, docsRoot) {
  const forbidden = [
    String(record.sitePayload.geodesy.latitudeDeg),
    String(record.sitePayload.geodesy.longitudeDeg),
    record.sitePayload.siteRecordId,
    record.sitePayload.observatoryId,
    record.payloadDigest.value,
    record.sitePayload.source.sourceLocator,
  ];
  for (const path of await walkTextFiles(docsRoot)) {
    const content = await readFile(path, "utf8");
    if (forbidden.some((value) => content.includes(value))) {
      throw new Error(`PROTECTED_VALUE_IN_PUBLIC_TREE:${relative(docsRoot, path)}`);
    }
  }
}

async function runCli() {
  const repositoryRoot = resolve(fileURLToPath(new URL("../../..", import.meta.url)));
  const recordPath = join(repositoryRoot, "governance/site-authority/site-records/DSG-SITE-RECORD-MANCIANO-001.draft.json");
  const decisionPath = join(repositoryRoot, "governance/site-authority/decision-evidence/DSG-SITE-MANCIANO-001.owner-decision.json");
  const record = JSON.parse(await readFile(recordPath, "utf8"));
  const decision = JSON.parse(await readFile(decisionPath, "utf8"));
  const schemaRoot = join(repositoryRoot, "governance/site-authority/schemas");
  const recordSchema = JSON.parse(await readFile(join(schemaRoot, "governed-site-record.schema.json"), "utf8"));
  const decisionSchema = JSON.parse(await readFile(join(schemaRoot, "site-source-decision.schema.json"), "utf8"));
  const approvalSchema = JSON.parse(await readFile(join(schemaRoot, "site-authority-approval-receipt.schema.json"), "utf8"));
  assertSchemaValidatorParity(recordSchema, decisionSchema, approvalSchema);
  const validation = validateRecord(record);
  if (!validation.valid) throw new Error(`SITE_AUTHORITY_VALIDATION_FAILED:${validation.errors.join(",")}`);
  const decisionValidation = validateDecisionEvidence(decision);
  if (!decisionValidation.valid) throw new Error(`SITE_AUTHORITY_DECISION_FAILED:${decisionValidation.errors.join(",")}`);
  if (record.lifecycle.decisionEvidenceRef !== relative(repositoryRoot, decisionPath).replaceAll("\\", "/") || decision.candidateRef !== relative(repositoryRoot, recordPath).replaceAll("\\", "/") || record.sitePayload.validity.validFromUtc !== decision.decisionRecordedAtUtc) throw new Error("SITE_AUTHORITY_DECISION_BINDING_FAILED");
  await verifyProtectedValuesAbsentFromDocs(record, join(repositoryRoot, "docs"));
  process.stdout.write("Site Authority protected draft validation passed; sensitive values omitted.\n");
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  runCli().catch((error) => {
    process.stderr.write(`${String(error.message).replace(/sha256:[a-f0-9]{64}/g, "[REDACTED_DIGEST]")}\n`);
    process.exitCode = 1;
  });
}
