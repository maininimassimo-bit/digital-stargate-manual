import assert from "node:assert/strict";
import test from "node:test";
import {
  assertBoundarySource,
  assertPublicPayload,
  buildPublicReference,
  digestPayload,
  redactAuditEvent,
  resolveSiteAuthority,
  validateRecord,
} from "./site-authority-validator.mjs";

// Synthetic-only fixtures exercise the protected validator without reproducing owner-supplied values.

const START = "2026-01-01T00:00:00.000Z";
const END = "2026-02-01T00:00:00.000Z";

function basePayload(overrides = {}) {
  const payload = {
    siteRecordId: "SYNTHETIC-SITE-RECORD-001",
    observatoryId: "DSG-OBSERVATORY-MANCIANO-001",
    revision: 1,
    scope: "OBSERVATION_PLANNER_READ_ONLY_SITE_AUTHORITY",
    geodesy: {
      datum: "WGS84",
      latitudeDeg: 0,
      longitudeDeg: 0,
      coordinateFormat: "DECIMAL_DEGREES",
      elevationM: 0,
      elevationUnit: "m",
      elevationReference: "ORTHOMETRIC_MEAN_SEA_LEVEL",
      acceptedElevationRangeM: { minInclusive: -500, maxInclusive: 9000 },
    },
    timezoneIana: "Europe/Rome",
    authority: {
      authoritySystem: "GITHUB_REPOSITORY_PROTECTED_REGISTRY",
      authorityScope: "SINGLE_OBSERVATORY",
      authorityRole: "SITE_AUTHORITY",
      repository: "maininimassimo-bit/digital-stargate-manual",
      registryRoot: "governance/site-authority",
      ownerRef: "github:user:maininimassimo-bit",
      custodianRef: "role:digital-stargate-architecture-office",
      approvalAuthorityRef: "github:user:maininimassimo-bit",
      custodianMayApprove: false,
    },
    source: {
      sourceKind: "OWNER_ATTESTED_APPLICATION_CONFIGURATION",
      application: "N.I.N.A.",
      sourceLocator: "synthetic:test-only",
      attestedByRef: "github:user:maininimassimo-bit",
      attestationChannel: "OWNER_CONTROLLED_INTERACTION_CHANNEL",
      sourceAuthority: "HUMAN_REPOSITORY_OWNER_ATTESTATION",
    },
    validity: {
      validFromUtc: START,
      validityEndMode: "EXCLUSIVE",
      validToUtc: END,
      intervalSemantics: "HALF_OPEN",
    },
    classification: "PROTECTED_EXACT_SITE",
    retention: "REPOSITORY_HISTORY_UNBOUNDED",
    publicationPolicy: {
      exactCoordinates: "PROHIBITED",
      elevation: "PROHIBITED",
      exactAddress: "PROHIBITED",
      siteLabelGeneralized: "Manciano (GR), Italia",
      timezoneDisplay: "Europe/Rome",
      publicRefPolicy: "INDEPENDENT_OPAQUE_IDENTIFIER",
      publicDigestPolicy: "PUBLIC_PAYLOAD_ONLY",
    },
    intendedUse: "OBSERVATION_PLANNER_READ_ONLY_SITE_CONTEXT_AFTER_SEPARATE_APPROVAL",
    prohibitedUses: ["DEVICE_COMMAND", "SAFETY_AUTHORITY", "READINESS_OR_GO_NO_GO", "PUBLIC_EXACT_SITE_PROJECTION", "EAGLE_WORKLOAD"],
    rollback: {
      draft: "Synthetic repository revert.",
      futureApproval: "Synthetic retirement."
    },
  };
  return deepMerge(payload, overrides);
}

function deepMerge(target, source) {
  const result = structuredClone(target);
  for (const [key, value] of Object.entries(source)) {
    result[key] = value && typeof value === "object" && !Array.isArray(value) && result[key] && typeof result[key] === "object"
      ? deepMerge(result[key], value)
      : value;
  }
  return result;
}

function envelope({ state = "APPROVED", payload = basePayload(), lifecycle = {} } = {}) {
  const approved = state === "APPROVED";
  const record = {
    schemaVersion: "1.0.0-draft",
    recordType: "DSG_GOVERNED_SITE_RECORD",
    lifecycle: {
      state,
      eligibleForResolution: approved,
      approvalEvidenceRef: approved ? "governance/site-authority/approval-evidence/synthetic.json" : null,
      approvedAtUtc: approved ? "2026-01-01T00:00:00.000Z" : null,
      retiredAtUtc: state === "RETIRED" ? "2026-03-01T00:00:00.000Z" : null,
      decisionEvidenceRef: "governance/site-authority/decision-evidence/synthetic.json",
      statement: "Synthetic test envelope.",
      ...lifecycle,
    },
    sitePayload: payload,
    payloadDigest: {
      method: "DSG-F3A1-CANONICAL-JSON-SHA256-1",
      canonicalization: "recursive object-key sort; array order preserved; compact JSON; UTF-8",
      algorithm: "SHA-256",
      value: digestPayload(payload),
    },
    validationEvidence: {
      jsonParse: { state: "VERIFIED" },
      schemaValidatorParity: { state: "VERIFIED" },
      payloadDigestRecomputation: { state: "VERIFIED" },
      protectedValueLeakScan: { state: "VERIFIED" },
      executableContractCases: { state: "VERIFIED" },
      runtimeOat: { state: "NOT_APPLICABLE" }
    },
  };
  return record;
}

function expectError(record, code) {
  const result = validateRecord(record);
  assert.equal(result.valid, false);
  assert.ok(result.errors.includes(code), `${code} missing from ${result.errors.join(",")}`);
}

test("A1-P01 APPROVED finite interval resolves internally", () => assert.equal(resolveSiteAuthority([envelope()], { observatoryId: "DSG-OBSERVATORY-MANCIANO-001", asOfUtc: "2026-01-15T00:00:00.000Z", authorized: true }).state, "AVAILABLE"));
test("A1-P02 start is inclusive", () => assert.equal(resolveSiteAuthority([envelope()], { observatoryId: "DSG-OBSERVATORY-MANCIANO-001", asOfUtc: START, authorized: true }).state, "AVAILABLE"));
test("A1-P03 instant before exclusive end is available", () => assert.equal(resolveSiteAuthority([envelope()], { observatoryId: "DSG-OBSERVATORY-MANCIANO-001", asOfUtc: "2026-01-31T23:59:59.999Z", authorized: true }).state, "AVAILABLE"));
test("A1-P04 UNBOUNDED interval resolves after start", () => { const payload = basePayload({ validity: { validityEndMode: "UNBOUNDED", validToUtc: null } }); assert.equal(resolveSiteAuthority([envelope({ payload })], { observatoryId: payload.observatoryId, asOfUtc: "2030-01-01T00:00:00.000Z", authorized: true }).state, "AVAILABLE"); });
test("A1-P05 adjacent intervals select only second at boundary", () => { const first = envelope(); const payload = basePayload({ revision: 2, validity: { validFromUtc: END, validToUtc: "2026-03-01T00:00:00.000Z" } }); const second = envelope({ payload }); const result = resolveSiteAuthority([first, second], { observatoryId: payload.observatoryId, asOfUtc: END, authorized: true }); assert.equal(result.state, "AVAILABLE"); assert.equal(result.site.revision, 2); });
test("A1-P06 WGS84 coordinate limits are valid", () => { for (const [lat, lon] of [[-90, -180], [90, 179.999999]]) assert.equal(validateRecord(envelope({ payload: basePayload({ geodesy: { latitudeDeg: lat, longitudeDeg: lon } }) })).valid, true); });
test("A1-P07 valid IANA timezone does not alter UTC", () => { const record = envelope(); assert.equal(validateRecord(record).valid, true); assert.equal(record.sitePayload.validity.validFromUtc, START); });
test("A1-P08 public projection is allowlisted", () => { const record = envelope({ state: "DRAFT" }); const output = buildPublicReference(record, { publicSiteRef: "PUBLIC-SITE-SYNTHETIC-001", asOfUtc: START }); assert.equal(assertPublicPayload(output, record).valid, true); assert.equal("latitudeDeg" in output, false); });
test("A1-P09 public digest is independent from internal digest", () => { const record = envelope(); const output = buildPublicReference(record, { publicSiteRef: "PUBLIC-SITE-SYNTHETIC-002", asOfUtc: START }); assert.notEqual(output.publicEvidenceDigest, record.payloadDigest.value); });
test("A1-P10 rollback is repository-local boundary metadata", () => { const record = envelope({ state: "DRAFT" }); assert.ok(record.sitePayload.prohibitedUses.includes("EAGLE_WORKLOAD")); assert.equal(record.lifecycle.eligibleForResolution, false); });

test("A1-N01 timestamp without Z is invalid", () => expectError(envelope({ payload: basePayload({ validity: { validFromUtc: "2026-01-01T00:00:00+00:00" } }) }), "INVALID_VALIDITY_INTERVAL"));
test("A1-N02 equal end and start is invalid", () => expectError(envelope({ payload: basePayload({ validity: { validToUtc: START } }) }), "INVALID_VALIDITY_INTERVAL"));
test("A1-N03 end before start is invalid", () => expectError(envelope({ payload: basePayload({ validity: { validToUtc: "2025-12-31T00:00:00.000Z" } }) }), "INVALID_VALIDITY_INTERVAL"));
test("A1-N04 EXCLUSIVE requires end", () => expectError(envelope({ payload: basePayload({ validity: { validToUtc: null } }) }), "INVALID_VALIDITY_INTERVAL"));
test("A1-N05 UNBOUNDED requires null end", () => expectError(envelope({ payload: basePayload({ validity: { validityEndMode: "UNBOUNDED", validToUtc: END } }) }), "INVALID_VALIDITY_INTERVAL"));
test("A1-N06 sentinel end is rejected", () => expectError(envelope({ payload: basePayload({ validity: { validToUtc: "9999-12-31T23:59:59.999Z" } }) }), "INVALID_VALIDITY_INTERVAL"));
test("A1-N07 exact exclusive end without successor is unavailable", () => assert.equal(resolveSiteAuthority([envelope()], { observatoryId: "DSG-OBSERVATORY-MANCIANO-001", asOfUtc: END, authorized: true }).state, "UNAVAILABLE"));
test("A1-N08 a temporal gap is explicit", () => { const first = envelope({ payload: basePayload({ validity: { validToUtc: "2026-01-10T00:00:00.000Z" } }) }); const second = envelope({ payload: basePayload({ revision: 2, validity: { validFromUtc: "2026-01-20T00:00:00.000Z" } }) }); assert.equal(resolveSiteAuthority([first, second], { observatoryId: "DSG-OBSERVATORY-MANCIANO-001", asOfUtc: "2026-01-15T00:00:00.000Z", authorized: true }).reasonCode, "VALIDITY_GAP"); });
test("A1-N09 overlapping approved records conflict", () => { const second = envelope({ payload: basePayload({ revision: 2, validity: { validFromUtc: "2026-01-15T00:00:00.000Z", validToUtc: "2026-03-01T00:00:00.000Z" } }) }); assert.equal(resolveSiteAuthority([envelope(), second], { observatoryId: "DSG-OBSERVATORY-MANCIANO-001", asOfUtc: "2026-01-20T00:00:00.000Z", authorized: true }).state, "CONFLICTED"); });
test("A1-N10 unbounded followed by approved record conflicts", () => { const firstPayload = basePayload({ validity: { validityEndMode: "UNBOUNDED", validToUtc: null } }); const secondPayload = basePayload({ revision: 2, validity: { validFromUtc: "2027-01-01T00:00:00.000Z", validToUtc: "2028-01-01T00:00:00.000Z" } }); assert.equal(resolveSiteAuthority([envelope({ payload: firstPayload }), envelope({ payload: secondPayload })], { observatoryId: firstPayload.observatoryId, asOfUtc: "2027-06-01T00:00:00.000Z", authorized: true }).state, "CONFLICTED"); });
test("A1-N11 overlap never uses highest revision", () => { const second = envelope({ payload: basePayload({ revision: 99, validity: { validFromUtc: "2026-01-15T00:00:00.000Z", validToUtc: "2026-03-01T00:00:00.000Z" } }) }); const result = resolveSiteAuthority([envelope(), second], { observatoryId: "DSG-OBSERVATORY-MANCIANO-001", asOfUtc: "2026-01-20T00:00:00.000Z", authorized: true }); assert.equal(result.state, "CONFLICTED"); assert.equal("site" in result, false); });
test("A1-N12 overlap never uses file order or mtime", () => { const second = envelope({ payload: basePayload({ revision: 2, validity: { validFromUtc: "2026-01-15T00:00:00.000Z", validToUtc: "2026-03-01T00:00:00.000Z" } }) }); assert.equal(resolveSiteAuthority([second, envelope()], { observatoryId: "DSG-OBSERVATORY-MANCIANO-001", asOfUtc: "2026-01-20T00:00:00.000Z", authorized: true }).state, "CONFLICTED"); });

test("A1-N13 DRAFT is unavailable", () => assert.equal(resolveSiteAuthority([envelope({ state: "DRAFT" })], { observatoryId: "DSG-OBSERVATORY-MANCIANO-001", asOfUtc: START, authorized: true }).state, "UNAVAILABLE"));
test("A1-N14 RETIRED is unavailable", () => assert.equal(resolveSiteAuthority([envelope({ state: "RETIRED" })], { observatoryId: "DSG-OBSERVATORY-MANCIANO-001", asOfUtc: START, authorized: true }).state, "UNAVAILABLE"));
test("A1-N15 APPROVED requires approver receipt and timestamp", () => expectError(envelope({ lifecycle: { approvalEvidenceRef: null, approvedAtUtc: null } }), "INVALID_APPROVAL_EVIDENCE"));
test("A1-N16 revision must be positive", () => expectError(envelope({ payload: basePayload({ revision: 0 }) }), "INVALID_REVISION"));
test("A1-N17 internal digest mismatch fails integrity", () => { const record = envelope(); record.payloadDigest.value = "sha256:" + "0".repeat(64); expectError(record, "INTEGRITY_FAILURE"); });
test("A1-N18 authority role is required", () => expectError(envelope({ payload: basePayload({ authority: { authorityRole: "" } }) }), "INVALID_AUTHORITY"));
test("A1-N19 owner and custodian are required", () => expectError(envelope({ payload: basePayload({ authority: { ownerRef: "", custodianRef: "" } }) }), "INVALID_AUTHORITY"));
test("A1-N20 datum must be WGS84", () => expectError(envelope({ payload: basePayload({ geodesy: { datum: "ETRS89" } }) }), "INVALID_SITE_SEMANTICS"));
test("A1-N21 latitude out of range is invalid", () => expectError(envelope({ payload: basePayload({ geodesy: { latitudeDeg: 90.0001 } }) }), "INVALID_SITE_SEMANTICS"));
test("A1-N22 longitude out of range is invalid", () => expectError(envelope({ payload: basePayload({ geodesy: { longitudeDeg: 180 } }) }), "INVALID_SITE_SEMANTICS"));
test("A1-N23 non-finite coordinates are invalid", () => { for (const value of [NaN, Infinity]) expectError(envelope({ payload: basePayload({ geodesy: { latitudeDeg: value } }) }), "INVALID_SITE_SEMANTICS"); });
test("A1-N24 timezone offset-only is invalid", () => expectError(envelope({ payload: basePayload({ timezoneIana: "+01:00" }) }), "INVALID_SITE_SEMANTICS"));
test("A1-N25 unknown IANA timezone is invalid", () => expectError(envelope({ payload: basePayload({ timezoneIana: "Europe/Unknown" }) }), "INVALID_SITE_SEMANTICS"));
test("A1-N26 resolver does not fall back to zero coordinates", () => { const result = resolveSiteAuthority([], { observatoryId: "UNKNOWN", asOfUtc: START, authorized: true }); assert.equal(result.state, "UNAVAILABLE"); assert.equal("site" in result, false); });
test("A1-N27 resolver does not fall back to host timezone", () => { const result = resolveSiteAuthority([], { observatoryId: "UNKNOWN", asOfUtc: START, authorized: true }); assert.equal("timezoneIana" in result, false); });

test("A1-N28 public coordinates fail allowlist", () => assert.equal(assertPublicPayload({ latitudeDeg: 1 }, envelope()).valid, false));
test("A1-N29 public elevation fails allowlist", () => assert.equal(assertPublicPayload({ elevationM: 1 }, envelope()).valid, false));
test("A1-N30 public source locator fails allowlist", () => assert.equal(assertPublicPayload({ sourceLocator: "x" }, envelope()).valid, false));
test("A1-N31 public internal ID or digest fails", () => { const record = envelope(); assert.equal(assertPublicPayload({ publicSiteRef: record.sitePayload.observatoryId }, record).valid, false); });
test("A1-N32 derived public ref is rejected", () => { const record = envelope(); assert.throws(() => buildPublicReference(record, { publicSiteRef: `PUBLIC-SITE-${record.sitePayload.observatoryId}`, asOfUtc: START }), /PUBLIC_PROJECTION_POLICY/); });
test("A1-N33 protected field in public digest payload is rejected", () => assert.equal(assertPublicPayload({ publicSiteRef: "PUBLIC-SITE-X", latitudeDeg: 1 }, envelope()).valid, false));
test("A1-N34 audit redaction removes coordinates and locator", () => { const output = redactAuditEvent({ event: "DENY", latitudeDeg: 1, sourceLocator: "secret", internalDigest: "secret" }); assert.deepEqual(output, { event: "DENY" }); });
test("A1-N35 unauthorized exact request is denied and audited", () => { const result = resolveSiteAuthority([envelope()], { observatoryId: "DSG-OBSERVATORY-MANCIANO-001", asOfUtc: START, authorized: false }); assert.deepEqual(result, { state: "UNAVAILABLE", reasonCode: "ACCESS_DENIED", audit: true }); });
test("A1-N36 conflict evidence cannot pass public allowlist", () => assert.equal(assertPublicPayload({ conflictEvidenceRef: "protected" }, envelope()).valid, false));
test("A1-N37 unsanitizable projection fails closed", () => assert.equal(assertPublicPayload({ arbitrary: "field" }, envelope()).reasonCode, "PUBLIC_PROJECTION_POLICY"));

test("A1-N38 Domain filesystem dependency fails architecture boundary", () => assert.deepEqual(assertBoundarySource("import fs from 'node:fs';").violations, ["DOMAIN_INFRASTRUCTURE_DEPENDENCY"]));
test("A1-N39 ephemeris provider selection violates scope", () => assert.ok(assertBoundarySource("use Skyfield here").violations.includes("EPHEMERIS_PROVIDER_SCOPE")));
test("A1-N40 readiness or command semantics violate boundary", () => assert.ok(assertBoundarySource("const readiness = true; deviceCommand();").violations.includes("SAFETY_OR_COMMAND_SCOPE")));
test("A1-N41 EAGLE workload requirement violates scope", () => assert.ok(assertBoundarySource("EAGLE_WORKLOAD_REQUIRED").violations.includes("EAGLE_SCOPE")));
