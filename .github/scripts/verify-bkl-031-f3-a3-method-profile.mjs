import crypto from "node:crypto";
import fs from "node:fs";
import process from "node:process";

export const EXPECTED_PROFILE_ID = "BKL-031-F3-A3-METHOD-PROFILE-001";
export const EXPECTED_PROFILE_SHA256 = "e69f60e5ed7f71cd982437f6ca3556b732d6ae9a46718995134aa64a7b7f67ca";

const expectedValues = new Map([
  ["schemaVersion", "1.0"],
  ["profileId", EXPECTED_PROFILE_ID],
  ["status", "OWNER_APPROVED_DECISION_PROFILE_NOT_EXECUTED"],
  ["decisionAuthority", "BKL-031-F3-A3-OD-2026-09-15"],
  ["spkDecisionRef", "BKL-031-F3-A3-F3-OD05-APPROVAL-2026-09-16"],
  ["runtimeAuthority", false],
  ["method.primary.library", "astropy"],
  ["method.primary.version", "8.0.1"],
  ["method.primary.spkAdapter", "jplephem"],
  ["method.primary.spkAdapterVersion", "2.24"],
  ["method.crossCheck.library", "skyfield"],
  ["method.crossCheck.version", "1.55"],
  ["method.externalReference.provider", "JPL Horizons"],
  ["method.externalReference.apiVersion", "1.3"],
  ["method.externalReference.role", "VALIDATION_ONLY"],
  ["method.externalReference.runtimeFallback", false],
  ["kernel.artifact", "de442s.bsp"],
  ["kernel.sha256", "54d97562a5b094d298b1b8eafa5a2e17e3e010ce85e1a366d07f003ad159323c"],
  ["kernel.coverageStartEt", "1849-12-26T00:00:00 ET"],
  ["kernel.coverageEndEt", "2150-01-22T00:00:00 ET"],
  ["kernel.outsideCoverageResult", "OUT_OF_COVERAGE"],
  ["kernel.extrapolationAllowed", false],
  ["kernel.silentSubstitutionAllowed", false],
  ["scientificSemantics.altitudeAzimuthMode", "GEOMETRIC_AIRLESS"],
  ["scientificSemantics.pressurePascal", 0],
  ["scientificSemantics.inputTimeScale", "UTC"],
  ["scientificSemantics.refractionMode", "DISABLED"],
  ["scientificSemantics.zenithScalarAzimuthUpperAltitudeDegrees", 85],
  ["scientificSemantics.perMetricPassRequired", true],
  ["scientificSemantics.averagingAllowed", false],
  ["scientificSemantics.unexplainedOverBudgetBlocksAcceptance", true],
  ["thresholds.altitudeMinimumDegrees", 5],
  ["thresholds.altitudeMaximumErrorArcseconds", 60],
  ["thresholds.azimuthMinimumAltitudeDegrees", 5],
  ["thresholds.azimuthMaximumAltitudeDegrees", 85],
  ["thresholds.azimuthMaximumErrorArcseconds", 60],
  ["thresholds.nearZenithSphericalSeparationMaximumErrorArcseconds", 60],
  ["thresholds.targetMoonSeparationMaximumErrorArcseconds", 60],
  ["thresholds.transitCulminationMaximumErrorSeconds", 5],
  ["thresholds.lunarIlluminationMaximumAbsoluteDifference", 0.001],
  ["thresholds.riseSetGeometricMaximumErrorSecondsWhenIncluded", 60],
  ["timeData.snapshotKind", "IERS_A"],
  ["timeData.sha256Required", true],
  ["timeData.maximumAgeDaysAtCampaignPreparation", 30],
  ["timeData.autoDownloadDuringExecution", false],
  ["timeData.outsideCoverageResult", "TIME_DATA_UNAVAILABLE"],
  ["timeData.refreshPolicy", "GOVERNED_CAMPAIGN_REVISION"],
  ["privacy.siteProfile", "SYNTHETIC_OR_GENERALIZED_ONLY"],
  ["privacy.protectedSiteInRepository", false],
  ["privacy.protectedSiteInLogs", false],
  ["privacy.protectedSiteInExternalRequests", false],
  ["privacy.localArtifactsPrivate", true],
  ["hosting.kind", "GOOGLE_CLOUD_RUN_JOB"],
  ["hosting.region", "europe-west8"],
  ["hosting.cpu", 2],
  ["hosting.memoryMiB", 2048],
  ["hosting.taskCount", 1],
  ["hosting.parallelism", 1],
  ["hosting.taskTimeoutSeconds", 120],
  ["hosting.maxRetries", 0],
  ["hosting.publicInternetEgress", false],
  ["hosting.observatoryControlAccess", false],
  ["requestBounds.maximumTargets", 50],
  ["requestBounds.maximumInstantsPerTarget", 2016],
  ["requestBounds.maximumTargetInstantPairs", 10000],
  ["requestBounds.maximumSpanDays", 7],
  ["requestBounds.minimumGridStepSeconds", 60],
  ["requestBounds.maximumRequestBytes", 262144],
  ["requestBounds.maximumConcurrency", 2],
  ["requestBounds.serviceP95SecondsAfterWarmup", 5],
  ["requestBounds.hardTimeoutSeconds", 15],
  ["requestBounds.batchTaskTimeoutSeconds", 120],
  ["failurePolicy.failClosed", true],
  ["failurePolicy.silentFallbackAllowed", false],
  ["failurePolicy.remoteReferenceAsRuntimeFallback", false],
  ["failurePolicy.resultValueAllowedWhenUnavailableOrConflicted", false],
]);

const valueAt = (object, dottedPath) =>
  dottedPath.split(".").reduce((current, key) => current?.[key], object);

export function verifyMethodProfile(raw, expectedDigest) {
  if (!/^[0-9a-f]{64}$/.test(expectedDigest)) {
    throw new Error("DSG_METHOD_PROFILE_SHA256 must be an exact lowercase SHA-256.");
  }
  if (expectedDigest !== EXPECTED_PROFILE_SHA256) {
    throw new Error("Method-profile digest is not the reviewed ARB-213-MI01 digest.");
  }

  const actualDigest = crypto.createHash("sha256").update(raw).digest("hex");
  if (actualDigest !== expectedDigest) {
    throw new Error(`Method-profile digest mismatch: expected ${expectedDigest}, received ${actualDigest}.`);
  }

  const profile = JSON.parse(raw.toString("utf8"));
  const failures = [];
  for (const [dottedPath, expected] of expectedValues) {
    const actual = valueAt(profile, dottedPath);
    if (!Object.is(actual, expected)) {
      failures.push(`${dottedPath}: expected ${JSON.stringify(expected)}, received ${JSON.stringify(actual)}`);
    }
  }
  if (failures.length) throw new Error(failures.join("\n"));
  return profile;
}

const profilePath = process.env.DSG_METHOD_PROFILE_PATH;
const profileDigest = process.env.DSG_METHOD_PROFILE_SHA256;
if (!profilePath || !profileDigest) {
  throw new Error("DSG_METHOD_PROFILE_PATH and DSG_METHOD_PROFILE_SHA256 are required.");
}

const raw = fs.readFileSync(profilePath);
verifyMethodProfile(raw, profileDigest);

const mutated = Buffer.from(raw.toString("utf8").replace('"maximumConcurrency": 2', '"maximumConcurrency": 3'));
if (mutated.equals(raw)) throw new Error("Negative drift fixture did not mutate the profile.");

let driftRejected = false;
try {
  verifyMethodProfile(mutated, profileDigest);
} catch {
  driftRejected = true;
}
if (!driftRejected) throw new Error("Mutated method profile was not rejected.");

let digestRejected = false;
try {
  verifyMethodProfile(raw, "0".repeat(64));
} catch {
  digestRejected = true;
}
if (!digestRejected) throw new Error("Unreviewed method-profile digest was not rejected.");

console.log(`ARB-213-MI01 method profile verified: ${EXPECTED_PROFILE_ID}@sha256:${EXPECTED_PROFILE_SHA256}`);
