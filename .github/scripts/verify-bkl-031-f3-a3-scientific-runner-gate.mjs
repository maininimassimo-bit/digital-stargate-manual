import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const base = path.join("infrastructure", "bkl-031-f3-a3-gcp");
const manifestRelative = path.join(base, "container", "BKL-031-F3-A3-RUNNER-MANIFEST-001.json");
const expectedManifestSha256 = "cee2ddb9d434cce1c0d635b2f111baf65fc016993bca1e17e72dca50bdd15ddd";
const expectedProfileSha256 = "e69f60e5ed7f71cd982437f6ca3556b732d6ae9a46718995134aa64a7b7f67ca";
const expectedKernelSha256 = "54d97562a5b094d298b1b8eafa5a2e17e3e010ce85e1a366d07f003ad159323c";
const expectedKernelUri = `gs://digital-stargate-telemetry-183451329061-f3-data/bkl-031/f3-a3/artifacts/spk/de442s/sha256/${expectedKernelSha256}/de442s.bsp`;
const sha256 = (value) => crypto.createHash("sha256").update(value).digest("hex");
const fail = (message) => { throw new Error(message); };
const equal = (actual, expected, label) => {
  if (!Object.is(actual, expected)) fail(`${label}: expected ${JSON.stringify(expected)}, received ${JSON.stringify(actual)}`);
};
const read = (relative) => fs.readFileSync(path.join(root, relative));

const rawManifest = read(manifestRelative);
equal(sha256(rawManifest), expectedManifestSha256, "runner manifest raw SHA-256");
const manifest = JSON.parse(rawManifest);
equal(manifest.schemaVersion, "1.0", "schemaVersion");
equal(manifest.manifestId, "BKL-031-F3-A3-RUNNER-MANIFEST-001", "manifestId");
equal(manifest.status, "RUNNER_SOURCE_MATERIALIZED_NOT_BUILT_NOT_PUBLISHED_NOT_EXECUTED", "status");
equal(manifest.predecessorManifest?.manifestId, "BKL-031-F3-A3-CONTAINER-MANIFEST-002", "predecessor manifest");
equal(manifest.predecessorManifest?.sha256, "02ceba17c1ac97f780cd545554b254ee668d840fcd85e11310d07c4ecc37e879", "predecessor digest");
equal(manifest.methodProfile?.sha256, expectedProfileSha256, "method profile digest");
equal(manifest.kernel?.sha256, expectedKernelSha256, "kernel digest");
equal(manifest.kernel?.privateUri, expectedKernelUri, "kernel URI");
equal(manifest.kernel?.gcsGeneration, "1789590110146663", "kernel generation");
equal(manifest.kernel?.containerEmbedded, false, "kernel embedding");
equal(manifest.campaign?.campaignId, "BKL-031-F3-A3-SYNTHETIC-CAMPAIGN-001", "campaign ID");
equal(manifest.campaign?.siteClassification, "SYNTHETIC_PUBLIC", "site classification");
equal(manifest.campaign?.targetCount, 2, "target count");
equal(manifest.campaign?.instantCount, 4, "instant count");
equal(manifest.campaign?.targetInstantPairCount, 8, "pair count");
equal(manifest.campaign?.externalReference, "NOT_AUTHORIZED", "external reference");
equal(manifest.runner?.comparisonClass, "SAME_SPK_IMPLEMENTATION_CROSS_CHECK_NOT_INDEPENDENT_REFERENCE", "comparison class");
equal(manifest.runner?.externalProviderPolicy, "DENY", "external provider policy");
equal(manifest.runner?.runtimeAuthority, false, "runner runtime authority");
equal(manifest.runner?.defaultCommand?.join(" "), "python /app/dsg/runner/scientific_runner.py --request /app/dsg/runner/BKL-031-F3-A3-SYNTHETIC-CAMPAIGN-001.json", "default command");

const controls = manifest.controls || {};
equal(controls.runnerSource, "MATERIALIZED_CONTRACT_SELF_TESTED", "runner source control");
for (const name of ["dependencyInstallation", "artifactAcquisition", "containerBuild", "containerPush", "platformPlan", "platformApply", "jobExecution", "scientificExecution", "externalReferenceTraffic", "protectedSiteUse", "runtimeActivation"]) {
  equal(controls[name], "NOT_EXECUTED", `controls.${name}`);
}
equal(controls.runtimeAuthority, false, "controls.runtimeAuthority");
equal(controls.publicInternetEgress, false, "controls.publicInternetEgress");

const sources = new Map((manifest.sourceFiles || []).map((entry) => [entry.path.replaceAll("\\", "/"), entry.sha256]));
equal(sources.size, 9, "unique source-file count");
for (const [relative, expected] of sources) {
  if (!/^[0-9a-f]{64}$/.test(expected)) fail(`${relative}: invalid SHA-256`);
  const bytes = read(relative);
  if (bytes.includes(0x0d)) fail(`${relative}: CRLF is not canonical`);
  equal(sha256(bytes), expected, `${relative} digest`);
}
equal(sources.get(`${base}/runner/scientific_runner.py`.replaceAll("\\", "/")), manifest.runner.sha256, "runner source digest");
equal(sources.get(`${base}/runner/BKL-031-F3-A3-SYNTHETIC-CAMPAIGN-001.json`.replaceAll("\\", "/")), manifest.campaign.fixtureSha256, "campaign fixture digest");

const runner = read(path.join(base, "runner", "scientific_runner.py")).toString("utf8");
for (const fragment of [
  expectedKernelSha256,
  "gs://digital-stargate-telemetry-183451329061-f3-data/",
  "bkl-031/f3-a3/artifacts/spk/de442s/sha256/",
  "VALIDATION_SPIKE",
  "SYNTHETIC_ONLY",
  "DSG_EXTERNAL_PROVIDER_POLICY",
  "OUT_OF_COVERAGE",
  "REQUEST_BOUND_EXCEEDED",
  "ifGenerationMatch",
  "externalReferenceCallCount\": 0",
  "GEOCENTRIC_APPARENT_ELONGATION_COSINE_APPROXIMATION",
  "--contract-self-test",
]) if (!runner.includes(fragment)) fail(`runner missing governed fragment: ${fragment}`);
for (const forbidden of ["horizons", "astroquery", "nina", "eagle", "forecast", "readiness", "safetyState"]) {
  if (runner.toLowerCase().includes(forbidden.toLowerCase())) fail(`runner contains forbidden scope/provider fragment: ${forbidden}`);
}
const urls = [...runner.matchAll(/https?:\/\/[^\s"']+/g)].map((match) => match[0]);
equal(urls.length, 3, "runner literal URL count");
for (const url of urls) {
  if (!url.startsWith("http://metadata.google.internal/") && !url.startsWith("https://storage.googleapis.com/")) {
    fail(`runner contains unapproved network destination: ${url}`);
  }
}

const fixture = JSON.parse(read(path.join(base, "runner", "BKL-031-F3-A3-SYNTHETIC-CAMPAIGN-001.json")));
equal(fixture.environment, "TEST", "fixture environment");
equal(fixture.authority, "NONE", "fixture authority");
equal(fixture.site?.classification, "SYNTHETIC_PUBLIC", "fixture site classification");
equal(fixture.refractionMode, "DISABLED", "fixture refraction");
equal(fixture.targets?.join(","), "mars,moon", "fixture targets");
equal(fixture.instantsUtc?.length, 4, "fixture instant count");
equal(fixture.transit?.gridStepSeconds, 60, "fixture grid step");

const dockerfile = read(path.join(base, "container", "Dockerfile.runner")).toString("utf8");
for (const fragment of [
  "python:3.12.14-slim-bookworm@sha256:9c47360a2a0355e2da18516d0b1c2126ec22c195d2185e97347c9d98398c5bef",
  "--no-index",
  "--require-hashes",
  "BKL-031-F3-A3-RUNNER-MANIFEST-001.json",
  "runner/scientific_runner.py",
  "USER 65532:65532",
  'ENTRYPOINT ["/app/dsg/container/entrypoint.sh"]',
  'CMD ["python", "/app/dsg/runner/scientific_runner.py", "--request", "/app/dsg/runner/BKL-031-F3-A3-SYNTHETIC-CAMPAIGN-001.json"]',
]) if (!dockerfile.includes(fragment)) fail(`runner Dockerfile missing: ${fragment}`);
if (/\b(latest|curl|wget)\b/i.test(dockerfile) || /pip\s+download/i.test(dockerfile)) fail("runner Dockerfile contains mutable or network acquisition instructions");

const mutations = [
  (value) => { value.controls.scientificExecution = "EXECUTED"; },
  (value) => { value.campaign.siteClassification = "PROTECTED"; },
  (value) => { value.runner.externalProviderPolicy = "ALLOW"; },
  (value) => { value.kernel.sha256 = "0".repeat(64); },
];
const validateGovernance = (value) => {
  equal(value.controls?.scientificExecution, "NOT_EXECUTED", "mutated controls.scientificExecution");
  equal(value.campaign?.siteClassification, "SYNTHETIC_PUBLIC", "mutated campaign.siteClassification");
  equal(value.runner?.externalProviderPolicy, "DENY", "mutated runner.externalProviderPolicy");
  equal(value.kernel?.sha256, expectedKernelSha256, "mutated kernel.sha256");
};
validateGovernance(manifest);
for (const mutate of mutations) {
  const candidate = structuredClone(manifest);
  mutate(candidate);
  let rejected = false;
  try { validateGovernance(candidate); } catch { rejected = true; }
  if (!rejected) fail("negative runner-manifest mutation was accepted");
}

console.log(`BKL-031 F3-A3 scientific runner source gate verified: ${manifest.manifestId}@sha256:${expectedManifestSha256}; scientific execution NOT_EXECUTED`);
