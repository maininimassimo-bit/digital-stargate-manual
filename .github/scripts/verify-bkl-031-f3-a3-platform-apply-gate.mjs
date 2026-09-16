import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const workflowPath = path.join(root, ".github", "workflows", "bkl-031-f3-a3-platform-apply.yml");
const workflow = fs.readFileSync(workflowPath, "utf8");
const evidencePath = path.join(
  root,
  "infrastructure",
  "bkl-031-f3-a3-gcp",
  "platform",
  "BKL-031-F3-A3-AUTHENTICATED-PLATFORM-PLAN-EVIDENCE-002.json",
);
const evidenceBytes = fs.readFileSync(evidencePath);
const evidence = JSON.parse(evidenceBytes.toString("utf8"));
const expectedEvidenceSha256 = "8d1864d0a766d11ff51c8461adc12714a845ef41ee624dbd1e17826cf2d5fbbb";
const applyEvidencePath = path.join(
  root,
  "infrastructure",
  "bkl-031-f3-a3-gcp",
  "platform",
  "BKL-031-F3-A3-PLATFORM-APPLY-EVIDENCE-001.json",
);
const applyEvidenceBytes = fs.readFileSync(applyEvidencePath);
const applyEvidence = JSON.parse(applyEvidenceBytes.toString("utf8"));
const expectedApplyEvidenceSha256 = "ca5952b67904f514e2e05b7abfd8aeb4df71cfdba89958441ca233bd01e710b8";
const expectedImage = "europe-west8-docker.pkg.dev/digital-stargate-telemetry/dsg-f3-a3/spike@sha256:de3331882e767c3a16fc479224da7c540385a6460e26df1ac73f8305676a0cce";
const expectedKernel = "gs://digital-stargate-telemetry-183451329061-f3-data/bkl-031/f3-a3/artifacts/spk/de442s/sha256/54d97562a5b094d298b1b8eafa5a2e17e3e010ce85e1a366d07f003ad159323c/de442s.bsp";
const expectedAddresses = [
  "google_cloud_run_v2_job.spike",
  "google_cloud_run_v2_job_iam_member.deployer_invoker",
  "google_compute_network.spike",
  "google_compute_subnetwork.spike",
];

const fail = (message) => { throw new Error(message); };
const requireText = (fragment) => {
  if (!workflow.includes(fragment)) fail(`platform apply workflow missing: ${fragment}`);
};
const exact = (actual, expected, label) => {
  if (!Object.is(actual, expected)) fail(`${label}: expected ${JSON.stringify(expected)}, received ${JSON.stringify(actual)}`);
};

for (const fragment of [
  "workflow_dispatch:",
  "expected_commit:",
  "contents: read",
  "id-token: write",
  "group: bkl-031-f3-a3-authenticated-platform-plan",
  "cancel-in-progress: false",
  "DSG_AUTHORIZED_COMMIT: ${{ inputs.expected_commit }}",
  'test "${GITHUB_REF}" = "refs/heads/main"',
  'test "${GITHUB_SHA}" = "${DSG_AUTHORIZED_COMMIT}"',
  "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
  "actions/setup-node@820762786026740c76f36085b0efc47a31fe5020",
  "google-github-actions/auth@7c6bc770dae815cd3e89ee6cdf493a5fab2cc093",
  "google-github-actions/setup-gcloud@aa5489c8933f4cc7a4f7d45035b3b1440c9c10db",
  "hashicorp/setup-terraform@dfe3c3f87815947d99a8997f908cb6525fc44e9e",
  "terraform_version: 1.16.2",
  "TF_VAR_job_name: dsg-f3-a3-spike",
  "TF_VAR_subnet_cidr: 10.88.0.0/28",
  "projects/183451329061/locations/global/workloadIdentityPools/dsg-f3-a3-github/providers/github-main",
  "dsg-f3-a3-deployer@digital-stargate-telemetry.iam.gserviceaccount.com",
  "dsg-f3-a3-runtime@digital-stargate-telemetry.iam.gserviceaccount.com",
  expectedImage,
  expectedKernel,
  'test "${#state_objects[@]}" -eq 1',
  'test "${state_objects[0]}" = "$state_uri"',
  'state.get("outputs") != {} or state.get("resources") != [] or state.get("check_results") is not None',
  'grep -F "Cannot find job [dsg-f3-a3-spike]." /tmp/job-before.err',
  'grep -F "global/networks/dsg-f3-a3-private\' was not found" /tmp/network-before.err',
  'grep -F "regions/${GCP_REGION}/subnetworks/dsg-f3-a3-private-ew8\' was not found" /tmp/subnetwork-before.err',
  'grep -F "One or more URLs matched no objects." /tmp/kernel-before.err',
  "terraform -chdir=infrastructure/bkl-031-f3-a3-gcp/platform plan -input=false -lock-timeout=60s -detailed-exitcode -out=/tmp/platform.tfplan",
  'test "$plan_status" -eq 2',
  'if addresses != expected_addresses:',
  'if change.get("change", {}).get("actions") != ["create"]:',
  '"kernel_artifact_sha256": "54d97562a5b094d298b1b8eafa5a2e17e3e010ce85e1a366d07f003ad159323c"',
  '"kernel_artifact_uri": os.environ["DSG_KERNEL_URI"]',
  '"method_profile_sha256": "e69f60e5ed7f71cd982437f6ca3556b732d6ae9a46718995134aa64a7b7f67ca"',
  '"iers_artifact_sha256": "43786a0a9b60c7a55a85e12307c0050d75ea0679710378141255ded9d1bd8ebc"',
  '"owner_decision_ref": "BKL-031-F3-A3-F3-OD05-APPROVAL-2026-09-16"',
  '"job_name": "dsg-f3-a3-spike"',
  '"subnet_cidr": "10.88.0.0/28"',
  "DSG_APPLY_PLAN_BINARY_SHA256",
  "DSG_APPLY_PLAN_JSON_SHA256",
  "DSG_APPLY_PLAN_TEXT_SHA256",
  "terraform -chdir=infrastructure/bkl-031-f3-a3-gcp/platform apply -input=false -lock-timeout=60s /tmp/platform.tfplan",
  "terraform -chdir=infrastructure/bkl-031-f3-a3-gcp/platform state list | sort",
  "terraform -chdir=infrastructure/bkl-031-f3-a3-gcp/platform show -json",
  "gcloud run jobs get-iam-policy dsg-f3-a3-spike",
  "gcloud run jobs executions list --job=dsg-f3-a3-spike",
  'if executions != []:',
  'grep -F "One or more URLs matched no objects." /tmp/kernel-after.err',
  "terraform -chdir=infrastructure/bkl-031-f3-a3-gcp/platform plan -input=false -lock-timeout=60s -detailed-exitcode -out=/tmp/platform-post-apply.tfplan",
  'test "$plan_status" -eq 0',
  '"resourceActions": {"add": 4, "change": 0, "destroy": 0}',
  '"postApplyDrift": 0',
  '"jobExecutionCount": 0',
  '"kernelArtifact": "NOT_UPLOADED"',
  '"artifactUpload": "NOT_EXECUTED"',
  '"scientificExecution": "NOT_EXECUTED"',
  '"externalReferenceTraffic": "NOT_EXECUTED"',
  '"protectedSiteUse": "NOT_EXECUTED"',
  '"runtimeActivation": "NOT_EXECUTED"',
  '"runtimeAuthority": False',
]) requireText(fragment);

for (const address of expectedAddresses) requireText(`"${address}"`);

const applyCommands = workflow.match(/^[ \t]*terraform[^\n]*[ \t]apply[ \t][^\n]*$/gim) ?? [];
if (applyCommands.length !== 1) fail(`platform apply workflow must contain exactly one Terraform apply command, received ${applyCommands.length}`);
if (!applyCommands[0].includes("/tmp/platform.tfplan")) fail("the sole Terraform apply must consume the verified saved plan");

for (const forbidden of [
  /(?:^|\s)-target(?:=|\s)/im,
  /\bterraform\s+[^\n]*\bdestroy\b/i,
  /\bforce-unlock\b/i,
  /-lock=false\b/i,
  /\bdocker\s+(?:build|push)\b/i,
  /--push(?:\s|=)/i,
  /\bgcloud\s+(?:artifacts|run|compute)\s+[^\n]*(?:create|update|delete|deploy|replace)\b/i,
  /\bgcloud\s+run\s+jobs\s+execute\b/i,
  /\bgcloud\s+storage\s+(?:cp|mv|rm)\b/i,
  /actions\/upload-artifact@/i,
]) {
  if (forbidden.test(workflow)) fail(`platform apply workflow contains forbidden operation: ${forbidden}`);
}

if (/^\s+(?:push|pull_request|schedule|workflow_run):/m.test(workflow)) {
  fail("platform apply workflow must remain explicit workflow_dispatch only");
}

const evidenceSha256 = crypto.createHash("sha256").update(evidenceBytes).digest("hex");
exact(evidenceSha256, expectedEvidenceSha256, "authenticated plan evidence SHA-256");
exact(evidence.schemaVersion, "1.0", "evidence.schemaVersion");
exact(evidence.evidenceId, "BKL-031-F3-A3-AUTHENTICATED-PLATFORM-PLAN-EVIDENCE-002", "evidence.evidenceId");
exact(evidence.status, "PUBLISHED_DIGEST_FOUR_RESOURCE_PLAN_VERIFIED_NOT_APPLIED", "evidence.status");
exact(evidence.source?.commit, "3abc8aa049262336fd5a814593cdfc521e4fc594", "evidence.source.commit");
exact(evidence.continuousIntegration?.runId, 35138798214, "evidence.continuousIntegration.runId");
exact(evidence.continuousIntegration?.conclusion, "SUCCESS", "evidence.continuousIntegration.conclusion");
exact(evidence.candidateImage?.publication, "PUBLISHED_EXACT_DIGEST", "evidence.candidateImage.publication");
exact(evidence.candidateImage?.reference, expectedImage, "evidence.candidateImage.reference");
exact(evidence.terraformPlan?.actions?.add, 4, "evidence.terraformPlan.actions.add");
exact(evidence.terraformPlan?.actions?.change, 0, "evidence.terraformPlan.actions.change");
exact(evidence.terraformPlan?.actions?.destroy, 0, "evidence.terraformPlan.actions.destroy");
exact(
  JSON.stringify([...(evidence.terraformPlan?.resourceAddresses ?? [])].sort()),
  JSON.stringify([...expectedAddresses].sort()),
  "evidence.terraformPlan.resourceAddresses",
);
exact(evidence.backendState?.status, "PERSISTED_EMPTY_STATE_ONLY", "evidence.backendState.status");
exact(evidence.backendState?.objectCount, 1, "evidence.backendState.objectCount");
exact(evidence.backendState?.resources, 0, "evidence.backendState.resources");
exact(evidence.controls?.platformApply, "NOT_EXECUTED", "evidence.controls.platformApply");
for (const name of ["artifactUpload", "scientificExecution", "externalReferenceTraffic", "protectedSiteUse", "runtimeActivation"]) {
  exact(evidence.controls?.[name], "NOT_EXECUTED", `evidence.controls.${name}`);
}
exact(evidence.controls?.runtimeAuthority, false, "evidence.controls.runtimeAuthority");
exact(evidence.nextGate, "SEPARATELY_REVIEWED_EXACT_FOUR_RESOURCE_PLATFORM_APPLY", "evidence.nextGate");

const applyEvidenceSha256 = crypto.createHash("sha256").update(applyEvidenceBytes).digest("hex");
exact(applyEvidenceSha256, expectedApplyEvidenceSha256, "platform apply evidence SHA-256");
exact(applyEvidence.schemaVersion, "1.0", "applyEvidence.schemaVersion");
exact(applyEvidence.evidenceId, "BKL-031-F3-A3-PLATFORM-APPLY-EVIDENCE-001", "applyEvidence.evidenceId");
exact(applyEvidence.status, "EXACT_FOUR_RESOURCE_PLATFORM_APPLIED_ZERO_DRIFT_JOB_UNEXECUTED", "applyEvidence.status");
exact(applyEvidence.source?.commit, "af81b807c8f6d8861ede3ecf3ae9b34e66df7790", "applyEvidence.source.commit");
exact(applyEvidence.source?.gatePullRequest, 233, "applyEvidence.source.gatePullRequest");
exact(applyEvidence.continuousIntegration?.runId, 35141947085, "applyEvidence.continuousIntegration.runId");
exact(applyEvidence.continuousIntegration?.jobId, 104948354087, "applyEvidence.continuousIntegration.jobId");
exact(applyEvidence.continuousIntegration?.conclusion, "SUCCESS", "applyEvidence.continuousIntegration.conclusion");
exact(applyEvidence.authentication?.mode, "GITHUB_OIDC_WIF_MAIN_ONLY", "applyEvidence.authentication.mode");
exact(applyEvidence.authentication?.staticServiceAccountKey, false, "applyEvidence.authentication.staticServiceAccountKey");
exact(applyEvidence.preconditions?.publishedImageReference, expectedImage, "applyEvidence.preconditions.publishedImageReference");
exact(applyEvidence.preconditions?.registryPackageCount, 1, "applyEvidence.preconditions.registryPackageCount");
exact(applyEvidence.preconditions?.registryVersionCount, 1, "applyEvidence.preconditions.registryVersionCount");
exact(applyEvidence.preconditions?.platformBackendStatus, "PERSISTED_EMPTY_STATE_ONLY", "applyEvidence.preconditions.platformBackendStatus");
exact(applyEvidence.preconditions?.targetResourcesAbsent, true, "applyEvidence.preconditions.targetResourcesAbsent");
exact(applyEvidence.preconditions?.kernelArtifactAbsent, true, "applyEvidence.preconditions.kernelArtifactAbsent");
exact(applyEvidence.terraformPlan?.binarySha256, "0499c10b6caa189e68b7f4a01b5ca684d787950e76cf563691a6eef03eb9871e", "applyEvidence.terraformPlan.binarySha256");
exact(applyEvidence.terraformPlan?.jsonSha256, "59b2a3504bedda1338434d2b3bdada091fac1a6bafbfd3a7369316e168571b63", "applyEvidence.terraformPlan.jsonSha256");
exact(applyEvidence.terraformPlan?.textSha256, "5a2c204553d8feae1640f978a74f18f4cdc7ba828c1b351a8f940e1c7a73d0b4", "applyEvidence.terraformPlan.textSha256");
exact(applyEvidence.terraformPlan?.actions?.add, 4, "applyEvidence.terraformPlan.actions.add");
exact(applyEvidence.terraformPlan?.actions?.change, 0, "applyEvidence.terraformPlan.actions.change");
exact(applyEvidence.terraformPlan?.actions?.destroy, 0, "applyEvidence.terraformPlan.actions.destroy");
exact(
  JSON.stringify([...(applyEvidence.terraformPlan?.resourceAddresses ?? [])].sort()),
  JSON.stringify([...expectedAddresses].sort()),
  "applyEvidence.terraformPlan.resourceAddresses",
);
exact(applyEvidence.terraformApply?.status, "EXECUTED_EXACT_SAVED_PLAN_ONLY", "applyEvidence.terraformApply.status");
exact(applyEvidence.terraformApply?.applyCommandCount, 1, "applyEvidence.terraformApply.applyCommandCount");
exact(applyEvidence.terraformApply?.targetedApply, false, "applyEvidence.terraformApply.targetedApply");
exact(applyEvidence.backendState?.status, "PERSISTED_EXACT_FOUR_RESOURCE_STATE", "applyEvidence.backendState.status");
exact(applyEvidence.backendState?.serial, 3, "applyEvidence.backendState.serial");
exact(applyEvidence.backendState?.lineage, "2be9b82b-88d3-888f-4fcd-dded2f74f7f3", "applyEvidence.backendState.lineage");
exact(applyEvidence.backendState?.rawSha256, "11b1888ceac0f39552e735d134a134bbbd7a6a75d623ac5c06897583842cf0e4", "applyEvidence.backendState.rawSha256");
exact(applyEvidence.backendState?.resourceCount, 4, "applyEvidence.backendState.resourceCount");
exact(
  JSON.stringify([...(applyEvidence.backendState?.resourceAddresses ?? [])].sort()),
  JSON.stringify([...expectedAddresses].sort()),
  "applyEvidence.backendState.resourceAddresses",
);
exact(applyEvidence.postconditions?.jobExecutionCount, 0, "applyEvidence.postconditions.jobExecutionCount");
exact(applyEvidence.postconditions?.kernelArtifact, "NOT_UPLOADED", "applyEvidence.postconditions.kernelArtifact");
exact(applyEvidence.postconditions?.postApplyDrift, 0, "applyEvidence.postconditions.postApplyDrift");
exact(applyEvidence.controls?.platformApply, "EXECUTED_THIS_GATE", "applyEvidence.controls.platformApply");
for (const name of ["artifactUpload", "scientificExecution", "externalReferenceTraffic", "protectedSiteUse", "runtimeActivation"]) {
  exact(applyEvidence.controls?.[name], "NOT_EXECUTED", `applyEvidence.controls.${name}`);
}
exact(applyEvidence.controls?.runtimeAuthority, false, "applyEvidence.controls.runtimeAuthority");
exact(applyEvidence.nextGate, "SEPARATELY_REVIEWED_EXACT_KERNEL_ARTIFACT_ACQUISITION_AND_UPLOAD", "applyEvidence.nextGate");

console.log(`BKL-031 F3-A3 platform apply gate and evidence verified: exact four-resource state, zero drift/executions; ${applyEvidence.evidenceId}@sha256:${expectedApplyEvidenceSha256}`);
