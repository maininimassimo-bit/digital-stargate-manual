import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const containerDir = path.join(root, "infrastructure", "bkl-031-f3-a3-gcp", "container");
const historicalManifestPath = path.join(containerDir, "BKL-031-F3-A3-CONTAINER-MANIFEST-001.json");
const manifestPath = path.join(containerDir, "BKL-031-F3-A3-CONTAINER-MANIFEST-002.json");
const historicalManifestSha256 = "7923206d85c5670ef56f9310a813c165c7d516d226c994561516c843b338412e";
const expectedManifestSha256 = "2dff1ebeb851ec99e7c6c7ecc73fb5aa7305a8a4937b6720ecb977ba6900c16c";
const expectedProfileSha256 = "e69f60e5ed7f71cd982437f6ca3556b732d6ae9a46718995134aa64a7b7f67ca";
const expectedIersSha256 = "43786a0a9b60c7a55a85e12307c0050d75ea0679710378141255ded9d1bd8ebc";
const expectedBasePlatformDigest = "sha256:9c47360a2a0355e2da18516d0b1c2126ec22c195d2185e97347c9d98398c5bef";

const expectedPackages = new Map([
  ["astropy", ["8.0.1", "fa11d56855e10107ea2231a6b6a33dbf1edbea6890adf34634c1f1d8f25c5a5a"]],
  ["astropy-iers-data", ["0.2026.9.14.0.56.43", expectedIersSha256]],
  ["certifi", ["2026.7.22", "62f22742b58a1a33014a2b6b706588a8d7e2a88ae7bd1a6ebe8c992928483775"]],
  ["jplephem", ["2.24", "2de15608a0f13010a71a0a8af8765646d5884402006dac0dd7639d7db13629ac"]],
  ["numpy", ["2.5.3", "b7e18c623bb5c95acb3b3328861272816ba199fb531921c5d6d0b675f1fde9e3"]],
  ["packaging", ["26.3", "d7193f7c8e4e93f444fde0262bf90af30e16fa0ad0ad44cb553c87339b23cd1c"]],
  ["pyerfa", ["2.0.1.5", "0e43c7194e3242083f2350b46c09fd4bf8ba1bcc0ebd1460b98fc47fe2389906"]],
  ["PyYAML", ["6.0.3", "ba1cc08a7ccde2d2ec775841541641e4548226580ab850948cbfda66a1befcdc"]],
  ["sgp4", ["2.27", "4d3775313120dcb6239535fa0c94cb6d5b089fd84bbfb15220923ae38dec7296"]],
  ["skyfield", ["1.55", "9f98964855067460c94aa81a337194136f4a97a62ba8bbbfac1b8556f2b66ad4"]],
]);
const expectedSourceFiles = new Map([
  ["infrastructure/bkl-031-f3-a3-gcp/.dockerignore", "8ce1cb34679acf2cca7ea9847358821de2c36e7720e77ccfdf8e19294230329d"],
  ["infrastructure/bkl-031-f3-a3-gcp/container/Dockerfile", "02c2099eb39cfc41acdbb390b43856b4fbaa52c50610443f5c7fbd89dd6bcdb7"],
  ["infrastructure/bkl-031-f3-a3-gcp/container/requirements.lock", "b9356f05eebf75501ef11f698b780837ebdde3fc64162d1c1b42420b30edf490"],
  ["infrastructure/bkl-031-f3-a3-gcp/container/astropy.cfg", "00aa2cd71966f5c98d7864db1fac834d263f44139c5364d8c1b3efce8aa8cf2a"],
  ["infrastructure/bkl-031-f3-a3-gcp/container/entrypoint.sh", "fcfe2d5b623e99f643f530b24e683cfc82d39b1c69381406f5f2906d0775e347"],
  ["infrastructure/bkl-031-f3-a3-gcp/container/preflight.py", "698aee0c6da5db322e13348c471359dbdd2a297616de42a9039aa080c44040bf"],
  ["infrastructure/bkl-031-f3-a3-gcp/method-profile/BKL-031-F3-A3-METHOD-PROFILE-001.json", expectedProfileSha256],
]);

const sha256 = (value) => crypto.createHash("sha256").update(value).digest("hex");
const read = (relativePath) => fs.readFileSync(path.join(root, relativePath));
const fail = (message) => { throw new Error(message); };
const equal = (actual, expected, label) => {
  if (!Object.is(actual, expected)) fail(`${label}: expected ${JSON.stringify(expected)}, received ${JSON.stringify(actual)}`);
};
const exactSha = (value, label) => {
  if (!/^[0-9a-f]{64}$/.test(value || "")) fail(`${label} must be an exact lowercase SHA-256`);
};

function validateManifest(manifest) {
  equal(manifest.schemaVersion, "1.0", "schemaVersion");
  equal(manifest.manifestId, "BKL-031-F3-A3-CONTAINER-MANIFEST-002", "manifestId");
  equal(manifest.status, "BUILD_INPUT_EXACT_ARTIFACTS_REQUIRED_NOT_BUILT", "status");
  equal(manifest.predecessorManifest?.manifestId, "BKL-031-F3-A3-CONTAINER-MANIFEST-001", "predecessorManifest.manifestId");
  equal(manifest.predecessorManifest?.sha256, historicalManifestSha256, "predecessorManifest.sha256");
  equal(manifest.methodProfile?.profileId, "BKL-031-F3-A3-METHOD-PROFILE-001", "methodProfile.profileId");
  equal(manifest.methodProfile?.sha256, expectedProfileSha256, "methodProfile.sha256");
  equal(manifest.target?.os, "linux", "target.os");
  equal(manifest.target?.architecture, "amd64", "target.architecture");
  equal(manifest.target?.python, "3.12.14", "target.python");
  equal(manifest.target?.baseImage, "python:3.12.14-slim-bookworm", "target.baseImage");
  equal(manifest.target?.baseImagePlatformDigest, expectedBasePlatformDigest, "target.baseImagePlatformDigest");
  if (!String(manifest.target?.source).startsWith("https://hub.docker.com/_/python/")) fail("base image source must be the Docker Hub official image");

  equal(manifest.iersSnapshot?.snapshotKind, "IERS_A", "iersSnapshot.snapshotKind");
  equal(manifest.iersSnapshot?.version, "0.2026.9.14.0.56.43", "iersSnapshot.version");
  equal(manifest.iersSnapshot?.sha256, expectedIersSha256, "iersSnapshot.sha256");
  equal(manifest.iersSnapshot?.ageDaysAtCampaignPreparation, 2, "iersSnapshot.ageDaysAtCampaignPreparation");
  equal(manifest.iersSnapshot?.maximumAgeDays, 30, "iersSnapshot.maximumAgeDays");
  equal(manifest.iersSnapshot?.freshnessStatus, "PASS_STATIC_METADATA", "iersSnapshot.freshnessStatus");
  equal(manifest.iersSnapshot?.coverageStatus, "NOT_INSPECTED_ARTIFACT_NOT_ACQUIRED", "iersSnapshot.coverageStatus");
  equal(manifest.iersSnapshot?.runtimeAutoDownload, false, "iersSnapshot.runtimeAutoDownload");
  equal(manifest.iersSnapshot?.acquisitionStatus, "NOT_ACQUIRED", "iersSnapshot.acquisitionStatus");
  if (!String(manifest.iersSnapshot?.source).startsWith("https://files.pythonhosted.org/")) fail("IERS artifact source must be files.pythonhosted.org");

  equal(manifest.packages?.length, expectedPackages.size, "packages.length");
  const seenPackages = new Set();
  for (const entry of manifest.packages || []) {
    const expected = expectedPackages.get(entry.name);
    if (!expected) fail(`unreviewed package: ${entry.name}`);
    if (seenPackages.has(entry.name)) fail(`duplicate package: ${entry.name}`);
    seenPackages.add(entry.name);
    equal(entry.version, expected[0], `${entry.name}.version`);
    equal(entry.sha256, expected[1], `${entry.name}.sha256`);
    exactSha(entry.sha256, `${entry.name}.sha256`);
    if (!String(entry.source).startsWith("https://files.pythonhosted.org/")) fail(`${entry.name} source is not official PyPI file hosting`);
    if (!entry.licenseExpression) fail(`${entry.name} license expression is required`);
  }

  const sourceFiles = new Map((manifest.sourceFiles || []).map((entry) => [entry.path, entry.sha256]));
  equal(manifest.sourceFiles?.length, expectedSourceFiles.size, "sourceFiles.length");
  equal(sourceFiles.size, expectedSourceFiles.size, "sourceFiles unique count");
  for (const [relativePath, expectedDigest] of expectedSourceFiles) {
    equal(sourceFiles.get(relativePath), expectedDigest, `${relativePath} declared digest`);
    exactSha(expectedDigest, `${relativePath} expected digest`);
    const sourceBytes = read(relativePath);
    if (sourceBytes.includes(0x0d)) fail(`${relativePath} must use canonical LF line endings`);
    const actualDigest = sha256(sourceBytes);
    equal(actualDigest, expectedDigest, `${relativePath} content digest`);
  }

  const controls = manifest.controls || {};
  for (const name of [
    "dependencyInstallation",
    "artifactAcquisition",
    "containerBuild",
    "containerPush",
    "platformPlan",
    "platformApply",
    "scientificExecution",
    "externalReferenceTraffic",
    "protectedSiteUse",
  ]) equal(controls[name], "NOT_EXECUTED", `controls.${name}`);
  equal(controls.containerImageDigest, "UNAVAILABLE_NOT_BUILT", "controls.containerImageDigest");
  equal(controls.runtimeAuthority, false, "controls.runtimeAuthority");
  equal(controls.entrypointPreflightRequired, true, "controls.entrypointPreflightRequired");
  equal(controls.networkRetrievalDuringScientificExecution, false, "controls.networkRetrievalDuringScientificExecution");
  equal(controls.nonRootUid, 65532, "controls.nonRootUid");
}

equal(sha256(fs.readFileSync(historicalManifestPath)), historicalManifestSha256, "historical manifest raw digest");
const rawManifest = fs.readFileSync(manifestPath);
equal(sha256(rawManifest), expectedManifestSha256, "manifest raw digest");
const manifest = JSON.parse(rawManifest.toString("utf8"));
validateManifest(manifest);

const dockerfile = fs.readFileSync(path.join(containerDir, "Dockerfile"), "utf8");
for (const fragment of [
  `FROM --platform=linux/amd64 python:3.12.14-slim-bookworm@${expectedBasePlatformDigest}`,
  "--only-binary=:all:",
  "--require-hashes",
  "--no-compile",
  "--no-deps",
  "SOURCE_DATE_EPOCH=0",
  "/app/dsg/method-profile/BKL-031-F3-A3-METHOD-PROFILE-001.json",
  "/app/dsg/container/BKL-031-F3-A3-CONTAINER-MANIFEST-002.json",
  "container/.build/wheels/",
  "--no-index",
  "/app/dsg/artifacts/iers/astropy_iers_data-0.2026.9.14.0.56.43-py3-none-any.whl",
  `DSG_IERS_SHA256=${expectedIersSha256}`,
  "USER 65532:65532",
  'ENTRYPOINT ["/app/dsg/container/entrypoint.sh"]',
  "NOT_EXECUTED: scientific runner is not materialized",
]) if (!dockerfile.includes(fragment)) fail(`Dockerfile missing: ${fragment}`);
if (/\b(latest|curl|wget)\b/i.test(dockerfile) || /pip\s+download/i.test(dockerfile)) fail("Dockerfile contains a mutable tag or network downloader");

const dockerignore = fs.readFileSync(path.join(root, "infrastructure", "bkl-031-f3-a3-gcp", ".dockerignore"), "utf8");
for (const required of [
  "**",
  "!container/.build/wheels/**",
  "!container/BKL-031-F3-A3-CONTAINER-MANIFEST-002.json",
  "!method-profile/BKL-031-F3-A3-METHOD-PROFILE-001.json",
]) if (!dockerignore.split("\n").includes(required)) fail(`isolated build context missing rule: ${required}`);
for (const forbidden of ["!bootstrap/", "!platform/", "!../", "!docs/"]) {
  if (dockerignore.includes(forbidden)) fail(`isolated build context unexpectedly includes: ${forbidden}`);
}

const workflow = fs.readFileSync(path.join(root, ".github", "workflows", "bkl-031-f3-a3-gcp-iac.yml"), "utf8");
const isolatedBuild = "--file infrastructure/bkl-031-f3-a3-gcp/container/Dockerfile infrastructure/bkl-031-f3-a3-gcp";
equal(workflow.split(isolatedBuild).length - 1, 2, "isolated no-cache build count");
if (!workflow.includes("docker build --network=none --pull=false --no-cache --build-arg SOURCE_DATE_EPOCH=0")) fail("workflow must build reproducibly without network, pull, or cache");

const acquisition = fs.readFileSync(path.join(root, ".github", "scripts", "acquire-bkl-031-f3-a3-container-artifacts.mjs"), "utf8");
for (const fragment of [
  'source.hostname !== "files.pythonhosted.org"',
  "response.url !== artifact.source",
  "digest !== artifact.sha256",
  'flag: "wx"',
  "EPHEMERAL_IGNORED_BUILD_INPUT",
  'artifactUpload: "NOT_EXECUTED"',
]) if (!acquisition.includes(fragment)) fail(`bounded acquisition missing: ${fragment}`);

const requirements = fs.readFileSync(path.join(containerDir, "requirements.lock"), "utf8");
equal((requirements.match(/--hash=sha256:/g) || []).length, expectedPackages.size, "requirements hash count");
if (/[^=<>!~]=?latest|>=|<=|~=|https?:\/\//i.test(requirements)) fail("requirements lock contains a range, latest, or direct URL");
for (const [name, [version, digest]] of expectedPackages) {
  if (!requirements.includes(`${name}==${version}`)) fail(`requirements missing exact ${name} version`);
  if (!requirements.includes(`--hash=sha256:${digest}`)) fail(`requirements missing ${name} hash`);
}

const entrypoint = fs.readFileSync(path.join(containerDir, "entrypoint.sh"), "utf8");
if (entrypoint.indexOf("preflight.py") < 0 || entrypoint.indexOf("preflight.py") > entrypoint.indexOf('exec "$@"')) fail("entrypoint must run preflight before the supplied command");
const astropyConfig = fs.readFileSync(path.join(containerDir, "astropy.cfg"), "utf8");
if (!astropyConfig.includes("auto_download = False") || !astropyConfig.includes("iers_degraded_accuracy = error")) fail("Astropy IERS configuration is not fail-closed");
const preflight = fs.readFileSync(path.join(containerDir, "preflight.py"), "utf8");
for (const fragment of [expectedProfileSha256, expectedIersSha256, '"astropy": "8.0.1"', '"skyfield": "1.55"', "iers.conf.auto_download is not False"]) {
  if (!preflight.includes(fragment)) fail(`preflight missing: ${fragment}`);
}
if (/\b(requests|urllib|httpx|socket)\b/.test(preflight)) fail("runtime preflight must not retrieve network content");

for (const forbiddenExtension of [".whl", ".bsp", ".fits", ".all"]) {
  const materialized = fs.readdirSync(containerDir).find((name) => name.endsWith(forbiddenExtension));
  if (materialized) fail(`artifact bytes must not be committed at this gate: ${materialized}`);
}

const mutations = [
  (value) => { value.iersSnapshot.sha256 = "0".repeat(64); },
  (value) => { value.target.baseImagePlatformDigest = "latest"; },
  (value) => { value.packages[0].version = "latest"; },
  (value) => { value.packages[1] = structuredClone(value.packages[0]); },
  (value) => { value.sourceFiles[0].path = "README.md"; },
  (value) => { value.iersSnapshot.acquisitionStatus = "ACQUIRED"; },
];
for (const mutate of mutations) {
  const candidate = JSON.parse(JSON.stringify(manifest));
  mutate(candidate);
  let rejected = false;
  try { validateManifest(candidate); } catch { rejected = true; }
  if (!rejected) fail("negative container-evidence mutation was not rejected");
}

console.log(`BKL-031 F3-A3 static container/IERS evidence verified: ${manifest.manifestId}@sha256:${expectedManifestSha256}`);
