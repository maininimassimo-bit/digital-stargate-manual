import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const workflowPath = path.join(root, ".github", "workflows", "bkl-031-f3-a3-authenticated-platform-plan.yml");
const workflow = fs.readFileSync(workflowPath, "utf8");
const evidencePath = path.join(root, "infrastructure", "bkl-031-f3-a3-gcp", "platform", "BKL-031-F3-A3-AUTHENTICATED-PLATFORM-PLAN-EVIDENCE-001.json");
const evidenceBytes = fs.readFileSync(evidencePath);
const evidence = JSON.parse(evidenceBytes.toString("utf8"));
const expectedEvidenceSha256 = "06cf923ae2bad1e869782bffd6a7e5389f9a68419d6199d0d7df5319f50b12e6";

const fail = (message) => { throw new Error(message); };
const requireText = (fragment) => {
  if (!workflow.includes(fragment)) fail(`authenticated plan workflow missing: ${fragment}`);
};

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
  "projects/183451329061/locations/global/workloadIdentityPools/dsg-f3-a3-github/providers/github-main",
  "dsg-f3-a3-deployer@digital-stargate-telemetry.iam.gserviceaccount.com",
  "dsg-f3-a3-runtime@digital-stargate-telemetry.iam.gserviceaccount.com",
  "digital-stargate-telemetry-183451329061-f3-state",
  "digital-stargate-telemetry-183451329061-f3-data",
  "digital-stargate-telemetry-183451329061-f3-evidence",
  'gcloud storage ls "gs://${GCP_STATE_BUCKET}"',
  'state_uri="gs://${GCP_STATE_BUCKET}/bkl-031/f3-a3/platform/default.tfstate"',
  'test "${#state_objects[@]}" -eq 1',
  'state["outputs"] != {} or state["resources"] != [] or state["check_results"] is not None',
  'gcloud artifacts repositories describe dsg-f3-a3 --project="$GCP_PROJECT_ID" --location="$GCP_REGION" --format=json >/tmp/registry.json',
  'gcloud artifacts docker images describe "$DSG_CANDIDATE_IMAGE_REFERENCE" --format=json >/tmp/published-image.json',
  'grep -F "$DSG_CANDIDATE_MANIFEST_DIGEST" /tmp/published-image.json',
  'grep -F "Cannot find job [dsg-f3-a3-spike]." /tmp/job-describe.err',
  'grep -F "global/networks/dsg-f3-a3-private\' was not found" /tmp/network-describe.err',
  'grep -F "regions/${GCP_REGION}/subnetworks/dsg-f3-a3-private-ew8\' was not found" /tmp/subnetwork-describe.err',
  "type=oci,dest=/tmp/dsg-candidate-${candidate}.tar,oci-mediatypes=true,rewrite-timestamp=true,compatibility-version=30",
  "--network=none --pull=false --no-cache",
  'test "$digest_a" = "sha256:de3331882e767c3a16fc479224da7c540385a6460e26df1ac73f8305676a0cce"',
  'test "$config_a" = "sha256:411df908f3938e0ff21b47986d4d5d9fcd91e1d0da3b64ffb00618aa48bbd5d0"',
  "bkl-031/f3-a3/platform",
  "terraform -chdir=infrastructure/bkl-031-f3-a3-gcp/platform plan",
  "-lock-timeout=60s -detailed-exitcode -out=/tmp/platform.tfplan",
  'test "$plan_status" -eq 2',
  '"google_compute_network.spike"',
  '"google_compute_subnetwork.spike"',
  '"google_cloud_run_v2_job.spike"',
  '"google_cloud_run_v2_job_iam_member.deployer_invoker"',
  '"resourceActions": {"add": 4, "change": 0, "destroy": 0}',
  '"containerPublication": "PUBLISHED_EXACT_DIGEST"',
  '"artifactRegistryRepositoryApply": "EXECUTED_SEPARATE_GATE"',
  '"terraformBackendState": "PERSISTED_EMPTY_STATE_ONLY"',
  '"platformApply": "NOT_EXECUTED"',
  "terraformBackendState=PERSISTED_EMPTY_STATE_ONLY",
  "apply=NOT_EXECUTED",
  "imagePush=EXECUTED_SEPARATE_GATE",
]) requireText(fragment);

for (const forbidden of [
  /\bterraform\s+[^\n]*\bapply\b/i,
  /\bdocker\s+push\b/i,
  /--push(?:\s|=)/i,
  /\bgcloud\s+(?:artifacts|run|compute)\s+[^\n]*(?:create|update|delete|deploy|replace)\b/i,
  /actions\/upload-artifact@/i,
  /\bforce-unlock\b/i,
  /-lock=false\b/i,
]) {
  if (forbidden.test(workflow)) fail(`authenticated plan workflow contains forbidden mutation: ${forbidden}`);
}

if (/^\s+(?:push|pull_request|schedule):/m.test(workflow)) {
  fail("authenticated plan workflow must remain explicit workflow_dispatch only");
}

const evidenceSha256 = crypto.createHash("sha256").update(evidenceBytes).digest("hex");
if (evidenceSha256 !== expectedEvidenceSha256) fail(`authenticated plan evidence digest mismatch: ${evidenceSha256}`);
const exact = (actual, expected, label) => {
  if (!Object.is(actual, expected)) fail(`${label}: expected ${JSON.stringify(expected)}, received ${JSON.stringify(actual)}`);
};
exact(evidence.schemaVersion, "1.0", "evidence.schemaVersion");
exact(evidence.evidenceId, "BKL-031-F3-A3-AUTHENTICATED-PLATFORM-PLAN-EVIDENCE-001", "evidence.evidenceId");
exact(evidence.status, "AUTHENTICATED_EXACT_HEAD_PLAN_VERIFIED_NOT_APPLIED", "evidence.status");
exact(evidence.source?.commit, "380bd8c3d04f570acb21a9a7f532930111adcdc8", "evidence.source.commit");
exact(evidence.continuousIntegration?.runId, 35131365596, "evidence.continuousIntegration.runId");
exact(evidence.continuousIntegration?.jobId, 104912908086, "evidence.continuousIntegration.jobId");
exact(evidence.continuousIntegration?.conclusion, "SUCCESS", "evidence.continuousIntegration.conclusion");
exact(evidence.authentication?.mode, "GITHUB_OIDC_WIF_MAIN_ONLY", "evidence.authentication.mode");
exact(evidence.authentication?.staticServiceAccountKey, false, "evidence.authentication.staticServiceAccountKey");
exact(evidence.candidateImage?.publication, "BLOCKED_REPOSITORY_NOT_CREATED", "evidence.candidateImage.publication");
for (const name of ["manifestDigest", "candidateA", "candidateB"]) {
  exact(evidence.candidateImage?.[name], "sha256:de3331882e767c3a16fc479224da7c540385a6460e26df1ac73f8305676a0cce", `evidence.candidateImage.${name}`);
}
exact(evidence.candidateImage?.configDigest, "sha256:411df908f3938e0ff21b47986d4d5d9fcd91e1d0da3b64ffb00618aa48bbd5d0", "evidence.candidateImage.configDigest");
exact(evidence.terraformPlan?.actions?.add, 5, "evidence.terraformPlan.actions.add");
exact(evidence.terraformPlan?.actions?.change, 0, "evidence.terraformPlan.actions.change");
exact(evidence.terraformPlan?.actions?.destroy, 0, "evidence.terraformPlan.actions.destroy");
exact(evidence.terraformPlan?.resourceAddresses?.length, 5, "evidence.terraformPlan.resourceAddresses.length");
exact(evidence.backendState?.status, "PERSISTED_EMPTY_STATE_ONLY", "evidence.backendState.status");
exact(evidence.backendState?.rawSha256, "48d4052c2e1a3899e8d568b32ada5e81282873534b720fa36241f9d026166482", "evidence.backendState.rawSha256");
exact(evidence.backendState?.outputs, 0, "evidence.backendState.outputs");
exact(evidence.backendState?.resources, 0, "evidence.backendState.resources");
exact(evidence.backendState?.residualLock, false, "evidence.backendState.residualLock");
for (const name of ["imagePush", "artifactRegistryRepositoryApply", "platformApply", "artifactUpload", "scientificExecution", "externalReferenceTraffic", "protectedSiteUse", "runtimeActivation"]) {
  exact(evidence.controls?.[name], "NOT_EXECUTED", `evidence.controls.${name}`);
}
exact(evidence.controls?.runtimeAuthority, false, "evidence.controls.runtimeAuthority");

console.log(`BKL-031 F3-A3 authenticated exact-head plan gate and evidence verified: ${evidence.evidenceId}@sha256:${expectedEvidenceSha256}; no apply/push/upload`);
