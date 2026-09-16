import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const workflow = fs.readFileSync(path.join(root, ".github", "workflows", "bkl-031-f3-a3-registry-foundation-verification.yml"), "utf8");
const foundationWorkflow = fs.readFileSync(path.join(root, ".github", "workflows", "bkl-031-f3-a3-registry-foundation.yml"), "utf8");
const evidencePath = path.join(root, "infrastructure", "bkl-031-f3-a3-gcp", "registry", "BKL-031-F3-A3-REGISTRY-FOUNDATION-EVIDENCE-001.json");
const evidenceBytes = fs.readFileSync(evidencePath);
const evidence = JSON.parse(evidenceBytes.toString("utf8"));
const expectedEvidenceSha256 = "3ef42c012c5c8d79a9751beb7c8e7c49ceab603a202c4a0cda359ef85ba08c30";
const fail = (message) => { throw new Error(message); };
const requireText = (source, fragment, label) => {
  if (!source.includes(fragment)) fail(`${label} missing: ${fragment}`);
};

const expectedLabels = '{"capability": "bkl-031", "goog-terraform-provisioned": "true", "increment": "f3-a3", "purpose": "validation-spike", "safety": "none"}';
requireText(foundationWorkflow, expectedLabels, "foundation workflow corrected label assertion");

for (const fragment of [
  "workflow_dispatch:",
  "expected_commit:",
  "contents: read",
  "id-token: write",
  'test "${GITHUB_REF}" = "refs/heads/main"',
  'test "${GITHUB_SHA}" = "${{ inputs.expected_commit }}"',
  "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
  "actions/setup-node@820762786026740c76f36085b0efc47a31fe5020",
  "google-github-actions/auth@7c6bc770dae815cd3e89ee6cdf493a5fab2cc093",
  "google-github-actions/setup-gcloud@aa5489c8933f4cc7a4f7d45035b3b1440c9c10db",
  "hashicorp/setup-terraform@dfe3c3f87815947d99a8997f908cb6525fc44e9e",
  'gcloud artifacts repositories describe dsg-f3-a3 --project="$GCP_PROJECT_ID" --location="$GCP_REGION" --format=json',
  'gcloud artifacts docker images list "${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT_ID}/dsg-f3-a3" --include-tags --format=json',
  '"goog-terraform-provisioned": "true"',
  "terraform -chdir=infrastructure/bkl-031-f3-a3-gcp/registry state list",
  "terraform -chdir=infrastructure/bkl-031-f3-a3-gcp/registry show -json",
  "terraform -chdir=infrastructure/bkl-031-f3-a3-gcp/registry plan -input=false -lock-timeout=60s -detailed-exitcode",
  'test "$plan_status" -eq 0',
  'test "${#state_objects[@]}" -eq 1',
  '"sourceApplyRunId": 35134193946',
  '"repositoryImageCount": 0',
  '"imagePush": "NOT_EXECUTED"',
  '"platformApply": "NOT_EXECUTED"',
]) requireText(workflow, fragment, "registry verification workflow");

if (/^\s+(?:push|pull_request|schedule):/m.test(workflow)) {
  fail("registry verification workflow must remain explicit workflow_dispatch only");
}

for (const forbidden of [
  /\bterraform\s+[^\n]*\bapply\b/i,
  /\bterraform\s+[^\n]*\bdestroy\b/i,
  /\bdocker\s+(?:build|push|buildx)\b/i,
  /\bgcloud\s+artifacts\s+(?:repositories|docker)\s+[^\n]*(?:create|update|delete|upload|import)\b/i,
  /\bgcloud\s+(?:run|compute|storage)\s+[^\n]*(?:create|update|delete|deploy|replace|cp)\b/i,
  /actions\/upload-artifact@/i,
  /\bforce-unlock\b/i,
  /-lock=false\b/i,
  /--target(?:\s|=)/i,
]) {
  if (forbidden.test(workflow)) fail(`registry verification workflow contains forbidden mutation: ${forbidden}`);
}

const evidenceSha256 = crypto.createHash("sha256").update(evidenceBytes).digest("hex");
if (evidenceSha256 !== expectedEvidenceSha256) fail(`registry foundation evidence digest mismatch: ${evidenceSha256}`);
const exact = (actual, expected, label) => {
  if (!Object.is(actual, expected)) fail(`${label}: expected ${JSON.stringify(expected)}, received ${JSON.stringify(actual)}`);
};
exact(evidence.schemaVersion, "1.0", "evidence.schemaVersion");
exact(evidence.evidenceId, "BKL-031-F3-A3-REGISTRY-FOUNDATION-EVIDENCE-001", "evidence.evidenceId");
exact(evidence.status, "REGISTRY_FOUNDATION_APPLIED_POST_VERIFIED_EMPTY", "evidence.status");
exact(evidence.foundationApply?.runId, 35134193946, "evidence.foundationApply.runId");
exact(evidence.foundationApply?.sourceCommit, "ccf23e68f4bf8d321ccf707d0918e231c1ec2be1", "evidence.foundationApply.sourceCommit");
exact(evidence.foundationApply?.resourceActions?.add, 1, "evidence.foundationApply.resourceActions.add");
exact(evidence.foundationApply?.resourceActions?.change, 0, "evidence.foundationApply.resourceActions.change");
exact(evidence.foundationApply?.resourceActions?.destroy, 0, "evidence.foundationApply.resourceActions.destroy");
exact(evidence.verification?.runId, 35135376900, "evidence.verification.runId");
exact(evidence.verification?.sourceCommit, "9c0bc79f3d7fc12c27f36d8b41c51058f5b3decd", "evidence.verification.sourceCommit");
exact(evidence.verification?.conclusion, "SUCCESS", "evidence.verification.conclusion");
exact(evidence.repository?.imageCount, 0, "evidence.repository.imageCount");
exact(evidence.repository?.labels?.["goog-terraform-provisioned"], "true", "evidence.repository.labels.goog-terraform-provisioned");
exact(evidence.terraformState?.resourceCount, 1, "evidence.terraformState.resourceCount");
exact(evidence.terraformState?.serial, 2, "evidence.terraformState.serial");
exact(evidence.terraformState?.rawSha256, "1429875a7626c9faf51f76060ae79f352b1f1e7a96e6bd5f59c152cbeb71ac7f", "evidence.terraformState.rawSha256");
exact(evidence.incident?.id, "BKL-031-F3-A3-RF-I01", "evidence.incident.id");
exact(evidence.incident?.disposition, "CORRECTED_AND_READ_ONLY_POST_VERIFIED", "evidence.incident.disposition");
for (const name of ["imagePush", "platformApply", "artifactUpload", "scientificExecution", "externalReferenceTraffic", "protectedSiteUse", "runtimeActivation"]) {
  exact(evidence.controls?.[name], "NOT_EXECUTED", `evidence.controls.${name}`);
}
exact(evidence.controls?.runtimeAuthority, false, "evidence.controls.runtimeAuthority");

console.log(`BKL-031 F3-A3 registry foundation gate and evidence verified: ${evidence.evidenceId}@sha256:${expectedEvidenceSha256}; one resource, zero drift, zero images`);
