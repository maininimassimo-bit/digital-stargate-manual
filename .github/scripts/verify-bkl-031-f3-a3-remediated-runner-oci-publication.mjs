import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const read = (...parts) => fs.readFileSync(path.join(root, ...parts));
const workflow = read(".github", "workflows", "bkl-031-f3-a3-remediated-runner-oci-publication.yml").toString("utf8");
const manifestBytes = read("infrastructure", "bkl-031-f3-a3-gcp", "container", "BKL-031-F3-A3-RUNNER-MANIFEST-004.json");
const manifest = JSON.parse(manifestBytes.toString("utf8"));
const validationBytes = read("infrastructure", "bkl-031-f3-a3-gcp", "container", "BKL-031-F3-A3-OFFLINE-EXACT-KERNEL-VALIDATION-EVIDENCE-001.json");
const validation = JSON.parse(validationBytes.toString("utf8"));
const expectedManifest = "sha256:f82acf36b79d6f3d8a3ba501b63bdba3ed446e7cf9070f477b01ed5d356ccb52";
const expectedConfig = "sha256:75bc408cdfb4e9fc1fe0db59c47f8ff71245b73d76ae66cfe02fd03910f74f87";
const preflightManifest = "sha256:de3331882e767c3a16fc479224da7c540385a6460e26df1ac73f8305676a0cce";
const originalRunnerManifest = "sha256:69a20a994fde9d5b1533b142760af5796b4ac795a1f00c658373a46d2648d60c";
const sha256 = (bytes) => crypto.createHash("sha256").update(bytes).digest("hex");
const fail = (message) => { throw new Error(message); };
const requireText = (fragment) => { if (!workflow.includes(fragment)) fail(`remediated publication workflow missing: ${fragment}`); };

for (const fragment of [
  "name: BKL-031 F3-A3 Remediated Runner OCI Publication", "workflow_dispatch:", "expected_commit:",
  "contents: read", "id-token: write", 'test "${GITHUB_REF}" = "refs/heads/main"',
  'test "${GITHUB_SHA}" = "${DSG_AUTHORIZED_COMMIT}"',
  `DSG_EXPECTED_MANIFEST_DIGEST: ${expectedManifest}`, `DSG_EXPECTED_CONFIG_DIGEST: ${expectedConfig}`,
  "node .github/scripts/verify-bkl-031-f3-a3-scientific-runner-gate.mjs",
  "node .github/scripts/verify-bkl-031-f3-a3-remediated-runner-oci-publication.mjs",
  "for candidate in a b; do", "--network=none --pull=false --no-cache --provenance=false --sbom=false",
  'test "$digest_a" = "$digest_b"', 'test "$digest_a" = "$DSG_EXPECTED_MANIFEST_DIGEST"',
  'test "$config_a" = "$config_b"', 'test "$config_a" = "$DSG_EXPECTED_CONFIG_DIGEST"',
  'tag="runner-${GITHUB_SHA:0:12}"', "push=false,oci-mediatypes=true", "push=true,oci-mediatypes=true",
  `"${preflightManifest}": ["candidate-3abc8aa04926"]`,
  `"${originalRunnerManifest}": ["runner-9db0267529b6"]`,
  "if len(images) != 2:", "if len(images) != 3:",
  "set(by_digest) != {expected_preflight_digest, expected_original_runner_digest, expected_digest}",
  "registryInventory=THREE_EXACT_IMAGES_PREFLIGHT_ORIGINAL_AND_REMEDIATED_RUNNER",
  "platformApply=NOT_EXECUTED", "scientificExecution=NOT_EXECUTED",
  "externalReferenceTraffic=NOT_EXECUTED", "protectedSiteUse=NOT_EXECUTED", "runtimeActivation=NOT_EXECUTED",
]) requireText(fragment);

if (/^\s+(?:push|pull_request|schedule):/m.test(workflow)) fail("remediated runner publication must remain explicit workflow_dispatch only");
if ((workflow.match(/docker buildx build /g) || []).length !== 3) fail("remediated publication must have the two-build loop, no-push preflight and one push site");
if ((workflow.match(/push=true/g) || []).length !== 1 || (workflow.match(/push=false/g) || []).length !== 1) fail("remediated publication must contain one push and one no-push registry exporter");
for (const forbidden of [
  /^\s*terraform\s/m, /\bgcloud\s+(?:run|compute|storage)\b/i,
  /\bgcloud\s+artifacts\s+repositories\s+(?:create|update|delete)\b/i,
  /\bgcloud\s+artifacts\s+docker\s+(?:delete|import)\b/i,
  /\bdocker\s+push\b/i, /actions\/upload-artifact@/i, /\bforce-unlock\b/i, /--target(?:\s|=)/i, /horizons/i,
]) if (forbidden.test(workflow)) fail(`remediated publication contains forbidden operation: ${forbidden}`);

if (sha256(manifestBytes) !== "11163d6ac4901341b409e686740a2090ae23f93eba08ed8b4aa8c8bb98c3f740") fail("runner manifest raw digest mismatch");
if (manifest.manifestId !== "BKL-031-F3-A3-RUNNER-MANIFEST-004" || manifest.controls?.scientificExecution !== "NOT_EXECUTED" || manifest.runner?.runtimeAuthority !== false) fail("runner manifest boundary mismatch");
if (sha256(validationBytes) !== "545b466b9305f9b5c1745686f2a337adea5221e414e96682d83e218430932c9e") fail("offline validation evidence raw digest mismatch");
if (validation.status !== "EXACT_KERNEL_OFFLINE_SCIENTIFIC_VALIDATION_PASS" || validation.source?.commit !== "90878ba9a495bf783eeac1637e61836ea95db646") fail("offline validation source identity mismatch");
if (validation.candidate?.manifestDigest !== expectedManifest || validation.candidate?.configDigest !== expectedConfig) fail("offline validation candidate identity mismatch");
if (validation.validation?.workflowRunId !== 35164615536 || validation.validation?.workflowJobId !== 105022805528 || validation.validation?.conclusion !== "SUCCESS") fail("offline validation run identity mismatch");
if (validation.validation?.metricPassCount !== 17 || validation.validation?.metricEvaluationCount !== 17 || validation.validation?.allEvaluatedMetricsPass !== true || validation.validation?.repeatabilityPass !== true || validation.validation?.transit?.pass !== true) fail("offline scientific acceptance mismatch");
if (validation.controls?.registryMutation !== "NOT_EXECUTED" || validation.controls?.jobExecution !== "NOT_EXECUTED" || validation.controls?.runtimeAuthority !== false) fail("offline validation overstates downstream authority");
if (validation.nextGate !== "EXACT_REMEDIATED_RUNNER_OCI_PUBLICATION") fail("offline validation next gate mismatch");

console.log(`BKL-031 F3-A3 remediated runner publication gate verified: ${expectedManifest}; ${expectedConfig}; one exact guarded push only`);
