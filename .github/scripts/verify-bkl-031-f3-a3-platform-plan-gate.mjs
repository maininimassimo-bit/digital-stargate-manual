import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const workflowPath = path.join(root, ".github", "workflows", "bkl-031-f3-a3-authenticated-platform-plan.yml");
const workflow = fs.readFileSync(workflowPath, "utf8");

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
  'gcloud storage buckets describe "gs://${GCP_STATE_BUCKET}"',
  'grep -F "NOT_FOUND" /tmp/repository-describe.err',
  'grep -F "NOT_FOUND" /tmp/job-describe.err',
  "type=oci,dest=/tmp/dsg-candidate-${candidate}.tar,oci-mediatypes=true,rewrite-timestamp=true,compatibility-version=30",
  "--network=none --pull=false --no-cache",
  'test "$config_a" = "sha256:411df908f3938e0ff21b47986d4d5d9fcd91e1d0da3b64ffb00618aa48bbd5d0"',
  "bkl-031/f3-a3/platform",
  "terraform -chdir=infrastructure/bkl-031-f3-a3-gcp/platform plan",
  "-lock-timeout=60s -detailed-exitcode -out=/tmp/platform.tfplan",
  'test "$plan_status" -eq 2',
  '"google_artifact_registry_repository.spike"',
  '"google_compute_network.spike"',
  '"google_compute_subnetwork.spike"',
  '"google_cloud_run_v2_job.spike"',
  '"google_cloud_run_v2_job_iam_member.deployer_invoker"',
  '"containerPublication": "BLOCKED_REPOSITORY_NOT_CREATED"',
  '"platformApply": "NOT_EXECUTED"',
  "apply=NOT_EXECUTED",
  "imagePush=NOT_EXECUTED",
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

console.log("BKL-031 F3-A3 authenticated exact-head plan gate verified: manual main-only WIF, reproducible unpublished candidate, saved plan, no apply/push/upload");
