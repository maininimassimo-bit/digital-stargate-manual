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
  assertClosedSchemaNode(approvalSchema.properties.subject, ["siteRecordId", "revision", "observatoryId", "payloadDigest", "validFromUtc", "validityEndMode", "validToUtc", "intervalSemantics"]);
  assertClosedSchemaNode(approvalSchema.properties.approvingAuthority, ["authorityRef", "authorityKind", "custodianIsApprover"]);
  assertClosedSchemaNode(approvalSchema.properties.approval, ["approvalTimestampUtc", "sourceChannel", "sourceStatement", "validityAcknowledged"]);
  assertClosedSchemaNode(approvalSchema.properties.repositoryEvidence, ["repository", "branch", "candidatePath", "approvedPath", "receiptPath", "authorizationBaselineCommit"]);
  assertClosedSchemaNode(approvalSchema.properties.integrity, ["canonicalizationMethod", "payloadDigestVerified", "payloadMutatedDuringApproval", "approvalSourceMatchesOwner"]);
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

export function validateApprovalReceipt(receipt) {
  const errors = [];
  if (!isObject(receipt) || !hasExactKeys(receipt, ["schemaVersion", "recordType", "receiptId", "decision", "subject", "approvingAuthority", "approval", "repositoryEvidence", "scopeBoundaries", "integrity"])) {
    return { valid: false, errors: ["INVALID_APPROVAL_RECEIPT_SCHEMA"] };
  }
  if (receipt.schemaVersion !== "1.0.0-draft" || receipt.recordType !== "DSG_SITE_AUTHORITY_APPROVAL_RECEIPT" || receipt.receiptId !== "DSG-SITE-RECORD-MANCIANO-001-APPROVAL-001" || receipt.decision !== "APPROVED") errors.push("INVALID_APPROVAL_RECEIPT");
  const subject = receipt.subject;
  if (!hasExactKeys(subject, ["siteRecordId", "revision", "observatoryId", "payloadDigest", "validFromUtc", "validityEndMode", "validToUtc", "intervalSemantics"])) errors.push("INVALID_APPROVAL_RECEIPT_SCHEMA");
  if (!isObject(subject) || typeof subject.siteRecordId !== "string" || !Number.isInteger(subject.revision) || typeof subject.observatoryId !== "string" || !/^sha256:[a-f0-9]{64}$/.test(subject.payloadDigest ?? "") || !isUtcTimestamp(subject.validFromUtc) || subject.validityEndMode !== "UNBOUNDED" || subject.validToUtc !== null || subject.intervalSemantics !== "HALF_OPEN") errors.push("INVALID_APPROVAL_SUBJECT");
  const authority = receipt.approvingAuthority;
  if (!hasExactKeys(authority, ["authorityRef", "authorityKind", "custodianIsApprover"]) || authority.authorityRef !== "github:user:maininimassimo-bit" || authority.authorityKind !== "HUMAN_REPOSITORY_OWNER" || authority.custodianIsApprover !== false) errors.push("INVALID_APPROVING_AUTHORITY");
  const approval = receipt.approval;
  if (!hasExactKeys(approval, ["approvalTimestampUtc", "sourceChannel", "sourceStatement", "validityAcknowledged"]) || !isUtcTimestamp(approval.approvalTimestampUtc) || approval.sourceChannel !== "OWNER_CONTROLLED_INTERACTION_CHANNEL" || typeof approval.sourceStatement !== "string" || approval.sourceStatement.length === 0 || approval.validityAcknowledged !== true) errors.push("INVALID_APPROVAL_DECISION");
  const repositoryEvidence = receipt.repositoryEvidence;
  if (!hasExactKeys(repositoryEvidence, ["repository", "branch", "candidatePath", "approvedPath", "receiptPath", "authorizationBaselineCommit"]) || repositoryEvidence.repository !== "maininimassimo-bit/digital-stargate-manual" || repositoryEvidence.branch !== "feat/bkl-031-f3-a1-m4-site-authority-approval" || !/^[a-f0-9]{40}$/.test(repositoryEvidence.authorizationBaselineCommit ?? "")) errors.push("INVALID_REPOSITORY_EVIDENCE");
  const requiredBoundaries = ["NO_PUBLIC_EXACT_COORDINATES", "NO_PUBLIC_ELEVATION", "NO_PUBLIC_EXACT_ADDRESS", "NO_SETUP_ASSIGNMENT_APPROVAL", "NO_RUNTIME_OR_EAGLE_OPERATION", "NO_READINESS_OR_GO_NO_GO_AUTHORITY", "NO_SAFETY_AUTHORITY_CHANGE"];
  if (!Array.isArray(receipt.scopeBoundaries) || new Set(receipt.scopeBoundaries).size !== receipt.scopeBoundaries.length || requiredBoundaries.some((boundary) => !receipt.scopeBoundaries.includes(boundary))) errors.push("INVALID_APPROVAL_SCOPE");
  const integrity = receipt.integrity;
  if (!hasExactKeys(integrity, ["canonicalizationMethod", "payloadDigestVerified", "payloadMutatedDuringApproval", "approvalSourceMatchesOwner"]) || integrity.canonicalizationMethod !== CANONICALIZATION_METHOD || integrity.payloadDigestVerified !== true || integrity.payloadMutatedDuringApproval !== false || integrity.approvalSourceMatchesOwner !== true) errors.push("INVALID_APPROVAL_INTEGRITY");
  return { valid: errors.length === 0, errors: [...new Set(errors)] };
}

export function validatePromotion(candidate, approved, receipt) {
  const errors = [];
  const candidateValidation = validateRecord(candidate);
  const approvedValidation = validateRecord(approved);
  const receiptValidation = validateApprovalReceipt(receipt);
  if (!candidateValidation.valid) errors.push("INVALID_DRAFT_CANDIDATE");
  if (!approvedValidation.valid) errors.push("INVALID_APPROVED_ENVELOPE");
  if (!receiptValidation.valid) errors.push(...receiptValidation.errors);
  if (candidate?.lifecycle?.state !== "DRAFT" || candidate?.lifecycle?.eligibleForResolution !== false || candidate?.lifecycle?.approvalEvidenceRef !== null) errors.push("INVALID_DRAFT_CANDIDATE");
  if (approved?.lifecycle?.state !== "APPROVED" || approved?.lifecycle?.eligibleForResolution !== true) errors.push("INVALID_APPROVED_ENVELOPE");
  if (canonicalize(candidate?.sitePayload) !== canonicalize(approved?.sitePayload) || candidate?.payloadDigest?.value !== approved?.payloadDigest?.value) errors.push("PAYLOAD_MUTATED_DURING_APPROVAL");
  if (candidate?.lifecycle?.decisionEvidenceRef !== approved?.lifecycle?.decisionEvidenceRef) errors.push("DECISION_EVIDENCE_CHANGED_DURING_APPROVAL");
  const subject = receipt?.subject ?? {};
  const validity = approved?.sitePayload?.validity ?? {};
  if (subject.siteRecordId !== approved?.sitePayload?.siteRecordId || subject.revision !== approved?.sitePayload?.revision || subject.observatoryId !== approved?.sitePayload?.observatoryId || subject.payloadDigest !== approved?.payloadDigest?.value || subject.validFromUtc !== validity.validFromUtc || subject.validityEndMode !== validity.validityEndMode || subject.validToUtc !== validity.validToUtc || subject.intervalSemantics !== validity.intervalSemantics) errors.push("APPROVAL_SUBJECT_BINDING_FAILED");
  if (approved?.lifecycle?.approvedAtUtc !== receipt?.approval?.approvalTimestampUtc || approved?.lifecycle?.approvalEvidenceRef !== receipt?.repositoryEvidence?.receiptPath || receipt?.repositoryEvidence?.candidatePath !== "governance/site-authority/site-records/DSG-SITE-RECORD-MANCIANO-001.draft.json" || receipt?.repositoryEvidence?.approvedPath !== "governance/site-authority/site-records/DSG-SITE-RECORD-MANCIANO-001.approved.json") errors.push("APPROVAL_EVIDENCE_BINDING_FAILED");
  if (!receipt?.approval?.sourceStatement?.includes(subject.payloadDigest ?? "") || !receipt?.approval?.sourceStatement?.includes(subject.validFromUtc ?? "")) errors.push("APPROVAL_STATEMENT_BINDING_FAILED");
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
  const candidatePath = join(repositoryRoot, "governance/site-authority/site-records/DSG-SITE-RECORD-MANCIANO-001.draft.json");
  const approvedPath = join(repositoryRoot, "governance/site-authority/site-records/DSG-SITE-RECORD-MANCIANO-001.approved.json");
  const decisionPath = join(repositoryRoot, "governance/site-authority/decision-evidence/DSG-SITE-MANCIANO-001.owner-decision.json");
  const receiptPath = join(repositoryRoot, "governance/site-authority/approval-evidence/DSG-SITE-RECORD-MANCIANO-001.approval.json");
  const candidate = JSON.parse(await readFile(candidatePath, "utf8"));
  const approved = JSON.parse(await readFile(approvedPath, "utf8"));
  const decision = JSON.parse(await readFile(decisionPath, "utf8"));
  const receipt = JSON.parse(await readFile(receiptPath, "utf8"));
  const schemaRoot = join(repositoryRoot, "governance/site-authority/schemas");
  const recordSchema = JSON.parse(await readFile(join(schemaRoot, "governed-site-record.schema.json"), "utf8"));
  const decisionSchema = JSON.parse(await readFile(join(schemaRoot, "site-source-decision.schema.json"), "utf8"));
  const approvalSchema = JSON.parse(await readFile(join(schemaRoot, "site-authority-approval-receipt.schema.json"), "utf8"));
  assertSchemaValidatorParity(recordSchema, decisionSchema, approvalSchema);
  const promotion = validatePromotion(candidate, approved, receipt);
  if (!promotion.valid) throw new Error(`SITE_AUTHORITY_PROMOTION_FAILED:${promotion.errors.join(",")}`);
  const decisionValidation = validateDecisionEvidence(decision);
  if (!decisionValidation.valid) throw new Error(`SITE_AUTHORITY_DECISION_FAILED:${decisionValidation.errors.join(",")}`);
  if (candidate.lifecycle.decisionEvidenceRef !== relative(repositoryRoot, decisionPath).replaceAll("\\", "/") || decision.candidateRef !== relative(repositoryRoot, candidatePath).replaceAll("\\", "/") || candidate.sitePayload.validity.validFromUtc !== decision.decisionRecordedAtUtc || receipt.repositoryEvidence.receiptPath !== relative(repositoryRoot, receiptPath).replaceAll("\\", "/") || receipt.repositoryEvidence.approvedPath !== relative(repositoryRoot, approvedPath).replaceAll("\\", "/")) throw new Error("SITE_AUTHORITY_EVIDENCE_BINDING_FAILED");
  const available = resolveSiteAuthority([candidate, approved], { observatoryId: approved.sitePayload.observatoryId, asOfUtc: approved.sitePayload.validity.validFromUtc, authorized: true });
  const denied = resolveSiteAuthority([candidate, approved], { observatoryId: approved.sitePayload.observatoryId, asOfUtc: approved.sitePayload.validity.validFromUtc, authorized: false });
  if (available.state !== "AVAILABLE" || denied.reasonCode !== "ACCESS_DENIED") throw new Error("SITE_AUTHORITY_RESOLUTION_GATE_FAILED");
  await verifyProtectedValuesAbsentFromDocs(approved, join(repositoryRoot, "docs"));
  process.stdout.write("Site Authority approval promotion validation passed; sensitive values omitted.\n");
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  runCli().catch((error) => {
    process.stderr.write(`${String(error.message).replace(/sha256:[a-f0-9]{64}/g, "[REDACTED_DIGEST]")}\n`);
    process.exitCode = 1;
  });
}
