import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const workflow = fs.readFileSync(path.join(root, ".github", "workflows", "bkl-031-f3-a3-registry-foundation-verification.yml"), "utf8");
const foundationWorkflow = fs.readFileSync(path.join(root, ".github", "workflows", "bkl-031-f3-a3-registry-foundation.yml"), "utf8");
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

console.log("BKL-031 F3-A3 registry foundation verification gate verified: existing one-resource state, zero drift, empty image inventory, no mutation");
