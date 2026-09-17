import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

const root = process.cwd();
const read = (...parts) => fs.readFileSync(path.join(root, ...parts), "utf8");
const workflow = read(".github", "workflows", "bkl-031-f3-a3-runner-platform-update.yml");
const main = read("infrastructure", "bkl-031-f3-a3-gcp", "platform", "main.tf");
const variables = read("infrastructure", "bkl-031-f3-a3-gcp", "platform", "variables.tf");
const evidence = JSON.parse(read("infrastructure", "bkl-031-f3-a3-gcp", "container", "BKL-031-F3-A3-RUNNER-OCI-PUBLICATION-EVIDENCE-001.json"));
const incident = JSON.parse(read("infrastructure", "bkl-031-f3-a3-gcp", "platform", "BKL-031-F3-A3-RUNNER-PLATFORM-UPDATE-INCIDENT-001.json"));
const updateEvidenceBytes = fs.readFileSync(path.join(root, "infrastructure", "bkl-031-f3-a3-gcp", "platform", "BKL-031-F3-A3-RUNNER-PLATFORM-UPDATE-EVIDENCE-001.json"));
const updateEvidence = JSON.parse(updateEvidenceBytes.toString("utf8"));

const runnerSource = "9db0267529b6d46a2510b415e4b3f51d668ff024";
const oldDigest = "sha256:de3331882e767c3a16fc479224da7c540385a6460e26df1ac73f8305676a0cce";
const runnerDigest = "sha256:69a20a994fde9d5b1533b142760af5796b4ac795a1f00c658373a46d2648d60c";
const oldImage = `europe-west8-docker.pkg.dev/digital-stargate-telemetry/dsg-f3-a3/spike@${oldDigest}`;
const runnerImage = `europe-west8-docker.pkg.dev/digital-stargate-telemetry/dsg-f3-a3/spike@${runnerDigest}`;
const fail = (message) => { throw new Error(message); };
const requireText = (text, fragment, context) => {
  if (!text.includes(fragment)) fail(`${context} missing: ${fragment}`);
};

for (const fragment of [
  "name: BKL-031 F3-A3 Exact Runner Platform Update",
  "workflow_dispatch:",
  "expected_commit:",
  "contents: read",
  "id-token: write",
  'test "${GITHUB_REF}" = "refs/heads/main"',
  'test "${GITHUB_SHA}" = "${DSG_AUTHORIZED_COMMIT}"',
  `DSG_RUNNER_SOURCE_COMMIT: ${runnerSource}`,
  `DSG_OLD_IMAGE_REFERENCE: ${oldImage}`,
  `DSG_RUNNER_IMAGE_REFERENCE: ${runnerImage}`,
  `TF_VAR_container_image_digest: ${runnerImage}`,
  `TF_VAR_runner_source_commit: ${runnerSource}`,
  "node .github/scripts/verify-bkl-031-f3-a3-exact-runner-oci-publication.mjs",
  "node .github/scripts/verify-bkl-031-f3-a3-runner-platform-update.mjs",
  "DSG_METHOD_PROFILE_PATH: infrastructure/bkl-031-f3-a3-gcp/method-profile/BKL-031-F3-A3-METHOD-PROFILE-001.json",
  "DSG_METHOD_PROFILE_SHA256: e69f60e5ed7f71cd982437f6ca3556b732d6ae9a46718995134aa64a7b7f67ca",
  "gcloud artifacts docker images list",
  "if len(images) != 2:",
  "gcloud run jobs executions list",
  "if 'DSG_SOURCE_COMMIT' in rendered:",
  "Create exact one-update saved plan",
  "-detailed-exitcode -out=/tmp/runner-update.tfplan",
  "if len(changes) != 1 or changes[0].get('address') != 'google_cloud_run_v2_job.spike':",
  "if change.get('actions') != ['update']:",
  "if before.get('image') != os.environ['DSG_OLD_IMAGE_REFERENCE']:",
  "if after.get('image') != os.environ['DSG_RUNNER_IMAGE_REFERENCE']:",
  "after_env != {**before_env, 'DSG_SOURCE_COMMIT': os.environ['DSG_RUNNER_SOURCE_COMMIT']}",
  "terraform -chdir=infrastructure/bkl-031-f3-a3-gcp/platform apply -input=false -lock-timeout=60s /tmp/runner-update.tfplan",
  "google_cloud_run_v2_job.spike",
  "google_cloud_run_v2_job_iam_member.deployer_invoker",
  "google_compute_network.spike",
  "google_compute_subnetwork.spike",
  "test \"$plan_status\" -eq 0",
  "savedPlan=0_ADD_1_CHANGE_0_DESTROY",
  "jobExecution=NOT_EXECUTED",
  "scientificExecution=NOT_EXECUTED",
  "externalReferenceTraffic=NOT_EXECUTED",
  "protectedSiteUse=NOT_EXECUTED",
  "runtimeActivation=NOT_EXECUTED",
]) requireText(workflow, fragment, "runner platform update workflow");

if (/^\s+(?:push|pull_request|schedule):/m.test(workflow)) fail("runner platform update must remain explicit workflow_dispatch only");
if ((workflow.match(/terraform -chdir=.*\sapply\s/g) || []).length !== 1) fail("runner platform update must contain exactly one Terraform apply");
if ((workflow.match(/gcloud run jobs execute/g) || []).length !== 0) fail("runner platform update must not execute the job");
for (const forbidden of [
  /\bgcloud\s+storage\s+(?:cp|mv|rm)\b/i,
  /\bgcloud\s+artifacts\s+(?:repositories|docker)\s+(?:create|update|delete|import)\b/i,
  /\bdocker\s+(?:build|push)\b/i,
  /\bterraform\s+destroy\b/i,
  /\bforce-unlock\b/i,
  /--target(?:\s|=)/i,
  /horizons/i,
]) if (forbidden.test(workflow)) fail(`runner platform update contains forbidden operation: ${forbidden}`);

requireText(main, 'name  = "DSG_SOURCE_COMMIT"', "platform job");
requireText(main, "value = var.runner_source_commit", "platform job");
requireText(variables, 'variable "runner_source_commit"', "platform variables");
requireText(variables, `"${runnerSource}"`, "platform variables historical source");

if (evidence.status !== "EXACT_RUNNER_OCI_PUBLISHED_POST_VERIFIED") fail("runner publication evidence is not post-verified");
if (evidence.source?.commit !== runnerSource || evidence.image?.reference !== runnerImage) fail("runner publication evidence does not bind the exact source and image");
if (evidence.controls?.jobExecution !== "NOT_EXECUTED" || evidence.controls?.scientificExecution !== "NOT_EXECUTED") fail("runner publication evidence overstates execution");
if (evidence.nextGate !== "EXACT_ONE_UPDATE_RUNNER_PLATFORM_PLAN_APPLY") fail("runner publication evidence does not authorize this gate");

if (incident.status !== "FAIL_CLOSED_BEFORE_AUTHENTICATION_NO_CLOUD_MUTATION") fail("runner platform update incident status mismatch");
if (incident.workflow?.runId !== 35152386533 || incident.workflow?.jobId !== 104983607065 || incident.workflow?.conclusion !== "failure") fail("runner platform update incident run identity mismatch");
if (incident.failure?.reason !== "METHOD_PROFILE_VERIFIER_ENVIRONMENT_NOT_EXPORTED") fail("runner platform update incident reason mismatch");
for (const control of ["cloudAuthentication", "registryRead", "kernelRead", "terraformInit", "terraformPlan", "terraformApply"]) {
  if (incident.controls?.[control] !== "SKIPPED") fail(`runner platform update incident ${control} must be SKIPPED`);
}
if (incident.controls?.jobExecution !== "NOT_EXECUTED" || incident.controls?.scientificExecution !== "NOT_EXECUTED" || incident.controls?.cloudMutation !== "NOT_EXECUTED") fail("runner platform update incident must preserve zero execution and mutation");

if (crypto.createHash("sha256").update(updateEvidenceBytes).digest("hex") !== "cb96049ac9f8723a573b3f3aae26edfb765a845594b427c2000c08040471a700") fail("runner platform update evidence raw digest mismatch");
if (updateEvidence.status !== "EXACT_RUNNER_PLATFORM_UPDATED_AND_READ_ONLY_POST_VERIFIED_JOB_UNEXECUTED") fail("runner platform update evidence status mismatch");
if (updateEvidence.apply?.runId !== 35153084496 || updateEvidence.apply?.jobId !== 104985932496 || updateEvidence.apply?.conclusion !== "success") fail("runner platform update apply run mismatch");
if (updateEvidence.postVerification?.runId !== 35154030354 || updateEvidence.postVerification?.jobId !== 104989054471 || updateEvidence.postVerification?.conclusion !== "success") fail("runner platform post-verification run mismatch");
if (updateEvidence.platformState?.serial !== 4 || updateEvidence.platformState?.lineage !== "2be9b82b-88d3-888f-4fcd-dded2f74f7f3" || updateEvidence.platformState?.rawSha256 !== "084b68da6d20d9523ceabce67766cfc211b71f97ee12d8f4e7a0b4a64f57b89b") fail("runner platform exact state identity mismatch");
if (updateEvidence.job?.image !== runnerImage || updateEvidence.job?.runnerSourceCommit !== runnerSource || updateEvidence.job?.executionCount !== 0) fail("runner platform job identity or execution count mismatch");
if (updateEvidence.controls?.jobExecution !== "NOT_EXECUTED" || updateEvidence.controls?.scientificExecution !== "NOT_EXECUTED" || updateEvidence.controls?.runtimeAuthority !== false) fail("runner platform update evidence overstates execution authority");
if (updateEvidence.nextGate !== "SEPARATELY_REVIEWED_EXACT_SINGLE_SCIENTIFIC_SPIKE_EXECUTION") fail("runner platform update evidence next gate mismatch");

console.log(`BKL-031 F3-A3 exact runner platform update verified: ${runnerImage}; one in-place job update; science NOT_EXECUTED`);
