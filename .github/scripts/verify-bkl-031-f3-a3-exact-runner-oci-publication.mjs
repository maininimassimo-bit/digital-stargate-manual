import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

const root = process.cwd();
const workflow = fs.readFileSync(
  path.join(root, ".github", "workflows", "bkl-031-f3-a3-exact-runner-oci-publication.yml"),
  "utf8",
);
const runnerManifest = JSON.parse(fs.readFileSync(
  path.join(root, "infrastructure", "bkl-031-f3-a3-gcp", "container", "BKL-031-F3-A3-RUNNER-MANIFEST-001.json"),
  "utf8",
));
const publicationEvidenceBytes = fs.readFileSync(
  path.join(root, "infrastructure", "bkl-031-f3-a3-gcp", "container", "BKL-031-F3-A3-RUNNER-OCI-PUBLICATION-EVIDENCE-001.json"),
);
const publicationEvidence = JSON.parse(publicationEvidenceBytes.toString("utf8"));
const expectedManifest = "sha256:69a20a994fde9d5b1533b142760af5796b4ac795a1f00c658373a46d2648d60c";
const expectedConfig = "sha256:333e5d1b303dda4c5a4037f386b2f56a7f967a9197bbb4186ca6f33dfd4c4cc3";
const preflightManifest = "sha256:de3331882e767c3a16fc479224da7c540385a6460e26df1ac73f8305676a0cce";
const fail = (message) => { throw new Error(message); };
const requireText = (fragment) => {
  if (!workflow.includes(fragment)) fail(`runner publication workflow missing: ${fragment}`);
};

for (const fragment of [
  "name: BKL-031 F3-A3 Exact Runner OCI Publication",
  "workflow_dispatch:",
  "expected_commit:",
  "contents: read",
  "id-token: write",
  'test "${GITHUB_REF}" = "refs/heads/main"',
  'test "${GITHUB_SHA}" = "${DSG_AUTHORIZED_COMMIT}"',
  "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
  "actions/setup-node@820762786026740c76f36085b0efc47a31fe5020",
  "google-github-actions/auth@7c6bc770dae815cd3e89ee6cdf493a5fab2cc093",
  "google-github-actions/setup-gcloud@aa5489c8933f4cc7a4f7d45035b3b1440c9c10db",
  `DSG_EXPECTED_MANIFEST_DIGEST: ${expectedManifest}`,
  `DSG_EXPECTED_CONFIG_DIGEST: ${expectedConfig}`,
  "node .github/scripts/verify-bkl-031-f3-a3-exact-oci-publication.mjs",
  "node .github/scripts/verify-bkl-031-f3-a3-scientific-runner-gate.mjs",
  "node .github/scripts/verify-bkl-031-f3-a3-exact-runner-oci-publication.mjs",
  "for candidate in a b; do",
  "type=oci,dest=/tmp/dsg-candidate-${candidate}.tar,oci-mediatypes=true,rewrite-timestamp=true,compatibility-version=30",
  "--network=none --pull=false --no-cache --provenance=false --sbom=false",
  "--file infrastructure/bkl-031-f3-a3-gcp/container/Dockerfile.runner infrastructure/bkl-031-f3-a3-gcp",
  'test "$digest_a" = "$digest_b"',
  'test "$digest_a" = "$DSG_EXPECTED_MANIFEST_DIGEST"',
  'test "$config_a" = "$config_b"',
  'test "$config_a" = "$DSG_EXPECTED_CONFIG_DIGEST"',
  'tag="runner-${GITHUB_SHA:0:12}"',
  "type=image,name=${DSG_IMAGE_REPOSITORY}:${tag},push=false,oci-mediatypes=true,rewrite-timestamp=true,compatibility-version=30",
  'test "$preflight_digest" = "$DSG_EXPECTED_MANIFEST_DIGEST"',
  'test "$preflight_config" = "$DSG_EXPECTED_CONFIG_DIGEST"',
  `expected_digest = "${preflightManifest}"`,
  'if len(images) != 1:',
  'image.get("tags", []) != ["candidate-3abc8aa04926"]',
  "type=image,name=${tagged_reference},push=true,oci-mediatypes=true,rewrite-timestamp=true,compatibility-version=30",
  'test "$published_digest" = "$DSG_EXPECTED_MANIFEST_DIGEST"',
  'test "$published_config" = "$DSG_EXPECTED_CONFIG_DIGEST"',
  'docker buildx imagetools inspect --raw "$DSG_PUBLISHED_IMAGE_REFERENCE"',
  'if len(images) != 2:',
  `expected_preflight_digest = "${preflightManifest}"`,
  'set(by_digest) != {expected_preflight_digest, expected_digest}',
  'by_digest[expected_digest].get("tags", []) != [expected_tag]',
  "registryInventory=TWO_EXACT_IMAGES_PREFLIGHT_AND_RUNNER",
  "platformApply=NOT_EXECUTED",
  "scientificExecution=NOT_EXECUTED",
  "externalReferenceTraffic=NOT_EXECUTED",
  "protectedSiteUse=NOT_EXECUTED",
  "runtimeActivation=NOT_EXECUTED",
]) requireText(fragment);

if (/^\s+(?:push|pull_request|schedule):/m.test(workflow)) {
  fail("runner OCI publication must remain explicit workflow_dispatch only");
}
if ((workflow.match(/docker buildx build /g) || []).length !== 3) {
  fail("runner publication requires one two-iteration OCI build site, one no-push preflight and one push site");
}
if ((workflow.match(/push=true/g) || []).length !== 1) fail("runner publication must have exactly one push exporter");
if ((workflow.match(/push=false/g) || []).length !== 1) fail("runner publication must have exactly one no-push registry preflight");
for (const forbidden of [
  /^\s*terraform\s/m,
  /\bgcloud\s+(?:run|compute|storage)\b/i,
  /\bgcloud\s+artifacts\s+repositories\s+(?:create|update|delete)\b/i,
  /\bgcloud\s+artifacts\s+docker\s+(?:delete|import)\b/i,
  /\bdocker\s+push\b/i,
  /actions\/upload-artifact@/i,
  /\bforce-unlock\b/i,
  /--target(?:\s|=)/i,
  /horizons/i,
]) if (forbidden.test(workflow)) fail(`runner publication contains forbidden operation: ${forbidden}`);

if (runnerManifest.manifestId !== "BKL-031-F3-A3-RUNNER-MANIFEST-001") fail("unexpected runner manifest identity");
if (runnerManifest.status !== "RUNNER_SOURCE_MATERIALIZED_NOT_BUILT_NOT_PUBLISHED_NOT_EXECUTED") fail("runner manifest overstates execution state");
if (runnerManifest.runner?.runtimeAuthority !== false || runnerManifest.controls?.scientificExecution !== "NOT_EXECUTED") {
  fail("runner manifest must preserve no runtime authority and no scientific execution");
}

if (publicationEvidence.evidenceId !== "BKL-031-F3-A3-RUNNER-OCI-PUBLICATION-EVIDENCE-001") fail("unexpected runner publication evidence identity");
if (crypto.createHash("sha256").update(publicationEvidenceBytes).digest("hex") !== "0b7992c257580c964118a09954615c75620b2c1018a7184ae02be8d101cbb23f") fail("runner publication evidence raw digest mismatch");
if (publicationEvidence.status !== "EXACT_RUNNER_OCI_PUBLISHED_POST_VERIFIED") fail("runner publication evidence is not post-verified");
if (publicationEvidence.source?.commit !== "9db0267529b6d46a2510b415e4b3f51d668ff024") fail("unexpected runner publication source commit");
if (publicationEvidence.source?.runnerManifestRawSha256 !== "cee2ddb9d434cce1c0d635b2f111baf65fc016993bca1e17e72dca50bdd15ddd") fail("unexpected runner manifest raw digest");
if (publicationEvidence.continuousIntegration?.runId !== 35150960879 || publicationEvidence.continuousIntegration?.jobId !== 104978864591) fail("unexpected runner publication run identity");
if (publicationEvidence.continuousIntegration?.conclusion !== "SUCCESS") fail("runner publication did not succeed");
if (publicationEvidence.image?.manifestDigest !== expectedManifest || publicationEvidence.image?.configDigest !== expectedConfig) fail("runner publication evidence digest mismatch");
if (publicationEvidence.image?.candidateA !== expectedManifest || publicationEvidence.image?.candidateB !== expectedManifest || publicationEvidence.image?.registryExporterPreflight !== expectedManifest) fail("runner publication reproduction mismatch");
if (publicationEvidence.registry?.imageCountBefore !== 1 || publicationEvidence.registry?.imageCountAfter !== 2) fail("unexpected runner publication registry cardinality");
if (publicationEvidence.registry?.preflightImagePreserved !== preflightManifest || publicationEvidence.registry?.exclusiveExpectedPackageVersionTagsVerified !== true) fail("runner publication registry postcondition mismatch");
if (publicationEvidence.controls?.imagePush !== "EXECUTED_EXACT_DIGEST" || publicationEvidence.controls?.platformApply !== "NOT_EXECUTED" || publicationEvidence.controls?.jobExecution !== "NOT_EXECUTED" || publicationEvidence.controls?.scientificExecution !== "NOT_EXECUTED" || publicationEvidence.controls?.runtimeAuthority !== false) fail("runner publication evidence overstates downstream authority");
if (publicationEvidence.nextGate !== "EXACT_ONE_UPDATE_RUNNER_PLATFORM_PLAN_APPLY") fail("unexpected runner publication next gate");

console.log(
  `BKL-031 F3-A3 exact runner OCI publication gate verified: ${expectedManifest}; ` +
  `${expectedConfig}; one guarded push; platform and science NOT_EXECUTED`,
);
