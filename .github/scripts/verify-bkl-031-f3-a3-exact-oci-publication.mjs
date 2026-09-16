import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const workflowPath = path.join(root, ".github", "workflows", "bkl-031-f3-a3-exact-oci-publication.yml");
const workflow = fs.readFileSync(workflowPath, "utf8");
const foundationEvidencePath = path.join(
  root,
  "infrastructure",
  "bkl-031-f3-a3-gcp",
  "registry",
  "BKL-031-F3-A3-REGISTRY-FOUNDATION-EVIDENCE-001.json",
);
const foundationEvidenceBytes = fs.readFileSync(foundationEvidencePath);
const foundationEvidence = JSON.parse(foundationEvidenceBytes.toString("utf8"));
const expectedFoundationEvidenceSha256 = "3ef42c012c5c8d79a9751beb7c8e7c49ceab603a202c4a0cda359ef85ba08c30";
const publicationEvidencePath = path.join(
  root,
  "infrastructure",
  "bkl-031-f3-a3-gcp",
  "container",
  "BKL-031-F3-A3-OCI-PUBLICATION-EVIDENCE-001.json",
);
const publicationEvidenceBytes = fs.readFileSync(publicationEvidencePath);
const publicationEvidence = JSON.parse(publicationEvidenceBytes.toString("utf8"));
const expectedPublicationEvidenceSha256 = "be2d999b9383df1e55c1627cdf48fa2dcde4040f88c3198d224bc48bef60833d";
const expectedManifest = "sha256:de3331882e767c3a16fc479224da7c540385a6460e26df1ac73f8305676a0cce";
const expectedConfig = "sha256:411df908f3938e0ff21b47986d4d5d9fcd91e1d0da3b64ffb00618aa48bbd5d0";
const fail = (message) => { throw new Error(message); };
const requireText = (fragment, label = "publication workflow") => {
  if (!workflow.includes(fragment)) fail(`${label} missing: ${fragment}`);
};

for (const fragment of [
  "workflow_dispatch:",
  "expected_commit:",
  "contents: read",
  "id-token: write",
  'test "${GITHUB_REF}" = "refs/heads/main"',
  "DSG_AUTHORIZED_COMMIT: ${{ inputs.expected_commit }}",
  'test "${GITHUB_SHA}" = "${DSG_AUTHORIZED_COMMIT}"',
  "grep -Eq '^[0-9a-f]{40}$' <<<\"${DSG_AUTHORIZED_COMMIT}\"",
  "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
  "actions/setup-node@820762786026740c76f36085b0efc47a31fe5020",
  "google-github-actions/auth@7c6bc770dae815cd3e89ee6cdf493a5fab2cc093",
  "google-github-actions/setup-gcloud@aa5489c8933f4cc7a4f7d45035b3b1440c9c10db",
  "moby/buildkit:v0.30.0@sha256:57269d1784e49b46228c45a1a1b870fbe40e0a639ab60b37b032d83af5bccdfc",
  "python:3.12.14-slim-bookworm@sha256:9c47360a2a0355e2da18516d0b1c2126ec22c195d2185e97347c9d98398c5bef",
  `DSG_EXPECTED_MANIFEST_DIGEST: ${expectedManifest}`,
  `DSG_EXPECTED_CONFIG_DIGEST: ${expectedConfig}`,
  "DSG_IMAGE_REPOSITORY: europe-west8-docker.pkg.dev/digital-stargate-telemetry/dsg-f3-a3/spike",
  "node .github/scripts/verify-bkl-031-f3-a3-registry-foundation-verification.mjs",
  "node .github/scripts/verify-bkl-031-f3-a3-exact-oci-publication.mjs",
  "for candidate in a b; do",
  "--network=none --pull=false --no-cache --provenance=false --sbom=false",
  "type=oci,dest=/tmp/dsg-candidate-${candidate}.tar,oci-mediatypes=true,rewrite-timestamp=true,compatibility-version=30",
  'test "$digest_a" = "$digest_b"',
  'test "$digest_a" = "$DSG_EXPECTED_MANIFEST_DIGEST"',
  'test "$config_a" = "$config_b"',
  'test "$config_a" = "$DSG_EXPECTED_CONFIG_DIGEST"',
  "type=image,name=${DSG_IMAGE_REPOSITORY}:${tag},push=false,oci-mediatypes=true,rewrite-timestamp=true,compatibility-version=30",
  'test "$preflight_digest" = "$DSG_EXPECTED_MANIFEST_DIGEST"',
  'test "$preflight_config" = "$DSG_EXPECTED_CONFIG_DIGEST"',
  'gcloud artifacts repositories describe dsg-f3-a3 --project="$GCP_PROJECT_ID" --location="$GCP_REGION" --format=json',
  'gcloud artifacts docker images list "${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT_ID}/dsg-f3-a3" --include-tags --format=json',
  'if images != []:',
  'gcloud auth configure-docker "${GCP_REGION}-docker.pkg.dev" --quiet',
  "type=image,name=${tagged_reference},push=true,oci-mediatypes=true,rewrite-timestamp=true,compatibility-version=30",
  'test "$published_digest" = "$DSG_EXPECTED_MANIFEST_DIGEST"',
  'test "$published_config" = "$DSG_EXPECTED_CONFIG_DIGEST"',
  'docker buildx imagetools inspect --raw "$DSG_PUBLISHED_IMAGE_REFERENCE"',
  'test "$registry_digest" = "$DSG_EXPECTED_MANIFEST_DIGEST"',
  'test "$registry_config" = "$DSG_EXPECTED_CONFIG_DIGEST"',
  "if len(images) != 1:",
  "platformApply=NOT_EXECUTED",
  "scientificExecution=NOT_EXECUTED",
]) requireText(fragment);

if (/^\s+(?:push|pull_request|schedule):/m.test(workflow)) {
  fail("exact OCI publication must remain explicit workflow_dispatch only");
}

const buildInvocations = workflow.match(/docker buildx build /g) ?? [];
if (buildInvocations.length !== 3) {
  fail(`expected three buildx command sites (two candidates in one loop, preflight, publish), received ${buildInvocations.length}`);
}
const pushTrue = workflow.match(/push=true/g) ?? [];
if (pushTrue.length !== 1) fail(`expected exactly one push=true exporter, received ${pushTrue.length}`);
const pushFalse = workflow.match(/push=false/g) ?? [];
if (pushFalse.length !== 1) fail(`expected exactly one push=false preflight exporter, received ${pushFalse.length}`);

for (const forbidden of [
  /^\s*terraform\s/m,
  /\bgcloud\s+(?:run|compute|storage)\b/i,
  /\bgcloud\s+artifacts\s+repositories\s+(?:create|update|delete)\b/i,
  /\bgcloud\s+artifacts\s+docker\s+(?:delete|import)\b/i,
  /\bdocker\s+push\b/i,
  /actions\/upload-artifact@/i,
  /\bforce-unlock\b/i,
  /--target(?:\s|=)/i,
]) {
  if (forbidden.test(workflow)) fail(`publication workflow contains forbidden operation: ${forbidden}`);
}

const foundationEvidenceSha256 = crypto.createHash("sha256").update(foundationEvidenceBytes).digest("hex");
if (foundationEvidenceSha256 !== expectedFoundationEvidenceSha256) {
  fail(`registry foundation evidence digest mismatch: ${foundationEvidenceSha256}`);
}
if (foundationEvidence.status !== "REGISTRY_FOUNDATION_APPLIED_POST_VERIFIED_EMPTY") {
  fail(`unexpected registry foundation status: ${foundationEvidence.status}`);
}
if (foundationEvidence.repository?.imageCount !== 0 || foundationEvidence.verification?.postApplyDrift !== 0) {
  fail("registry foundation evidence does not prove empty image inventory and zero drift");
}
for (const name of ["imagePush", "platformApply", "artifactUpload", "scientificExecution", "runtimeActivation"]) {
  if (foundationEvidence.controls?.[name] !== "NOT_EXECUTED") {
    fail(`registry foundation evidence control ${name} is not NOT_EXECUTED`);
  }
}

const publicationEvidenceSha256 = crypto.createHash("sha256").update(publicationEvidenceBytes).digest("hex");
if (publicationEvidenceSha256 !== expectedPublicationEvidenceSha256) {
  fail(`OCI publication evidence digest mismatch: ${publicationEvidenceSha256}`);
}
const exact = (actual, expected, label) => {
  if (!Object.is(actual, expected)) fail(`${label}: expected ${JSON.stringify(expected)}, received ${JSON.stringify(actual)}`);
};
exact(publicationEvidence.schemaVersion, "1.0", "publicationEvidence.schemaVersion");
exact(publicationEvidence.evidenceId, "BKL-031-F3-A3-OCI-PUBLICATION-EVIDENCE-001", "publicationEvidence.evidenceId");
exact(publicationEvidence.status, "EXACT_OCI_PUBLISHED_POST_VERIFIED", "publicationEvidence.status");
exact(publicationEvidence.source?.commit, "3abc8aa049262336fd5a814593cdfc521e4fc594", "publicationEvidence.source.commit");
exact(publicationEvidence.continuousIntegration?.runId, 35138527237, "publicationEvidence.continuousIntegration.runId");
exact(publicationEvidence.continuousIntegration?.jobId, 104936888146, "publicationEvidence.continuousIntegration.jobId");
exact(publicationEvidence.continuousIntegration?.conclusion, "SUCCESS", "publicationEvidence.continuousIntegration.conclusion");
for (const name of ["manifestDigest", "candidateA", "candidateB", "registryExporterPreflight"]) {
  exact(publicationEvidence.image?.[name], expectedManifest, `publicationEvidence.image.${name}`);
}
exact(publicationEvidence.image?.configDigest, expectedConfig, "publicationEvidence.image.configDigest");
exact(publicationEvidence.image?.tag, "candidate-3abc8aa04926", "publicationEvidence.image.tag");
exact(publicationEvidence.image?.reference, `europe-west8-docker.pkg.dev/digital-stargate-telemetry/dsg-f3-a3/spike@${expectedManifest}`, "publicationEvidence.image.reference");
exact(publicationEvidence.image?.registryResolvedRawManifestSha256, expectedManifest.slice("sha256:".length), "publicationEvidence.image.registryResolvedRawManifestSha256");
exact(publicationEvidence.registry?.imageCountBefore, 0, "publicationEvidence.registry.imageCountBefore");
exact(publicationEvidence.registry?.imageCountAfter, 1, "publicationEvidence.registry.imageCountAfter");
exact(publicationEvidence.registry?.exclusiveExpectedPackageVersionTagVerified, true, "publicationEvidence.registry.exclusiveExpectedPackageVersionTagVerified");
exact(publicationEvidence.controls?.imagePush, "EXECUTED_EXACT_DIGEST", "publicationEvidence.controls.imagePush");
for (const name of ["platformApply", "artifactUpload", "scientificExecution", "externalReferenceTraffic", "protectedSiteUse", "runtimeActivation"]) {
  exact(publicationEvidence.controls?.[name], "NOT_EXECUTED", `publicationEvidence.controls.${name}`);
}
exact(publicationEvidence.controls?.runtimeAuthority, false, "publicationEvidence.controls.runtimeAuthority");
exact(publicationEvidence.nextGate, "AUTHENTICATED_REGISTRY_RESOLVED_FOUR_RESOURCE_PLATFORM_PLAN", "publicationEvidence.nextGate");

console.log(
  `BKL-031 F3-A3 exact OCI publication contract verified: ${expectedManifest}; ` +
  `publication evidence sha256:${expectedPublicationEvidenceSha256}; one guarded push exporter`,
);
