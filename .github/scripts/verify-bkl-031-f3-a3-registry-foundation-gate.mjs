import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const workflowPath = path.join(root, ".github", "workflows", "bkl-031-f3-a3-registry-foundation.yml");
const workflow = fs.readFileSync(workflowPath, "utf8");
const registryRoot = path.join(root, "infrastructure", "bkl-031-f3-a3-gcp", "registry");
const registryMain = fs.readFileSync(path.join(registryRoot, "main.tf"), "utf8");
const registryVariables = fs.readFileSync(path.join(registryRoot, "variables.tf"), "utf8");
const registryVersions = fs.readFileSync(path.join(registryRoot, "versions.tf"), "utf8");
const platformMain = fs.readFileSync(path.join(root, "infrastructure", "bkl-031-f3-a3-gcp", "platform", "main.tf"), "utf8");

const fail = (message) => { throw new Error(message); };
const requireText = (source, fragment, label) => {
  if (!source.includes(fragment)) fail(`${label} missing: ${fragment}`);
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
  "digital-stargate-telemetry-183451329061-f3-state",
  "bkl-031/f3-a3/registry",
  "terraform -chdir=infrastructure/bkl-031-f3-a3-gcp/registry plan",
  "-lock-timeout=60s -detailed-exitcode -out=/tmp/registry.tfplan",
  'test "$plan_status" -eq 2',
  'changes[0].get("address") != "google_artifact_registry_repository.spike"',
  'changes[0].get("change", {}).get("actions") != ["create"]',
  "terraform -chdir=infrastructure/bkl-031-f3-a3-gcp/registry apply -input=false -lock-timeout=60s -auto-approve /tmp/registry.tfplan",
  'test "${#resources[@]}" -eq 1',
  'test "${resources[0]}" = "google_artifact_registry_repository.spike"',
  '"resourceActions": {"add": 1, "change": 0, "destroy": 0}',
  '"imagePush": "NOT_EXECUTED"',
  '"platformApply": "NOT_EXECUTED"',
  '"scientificExecution": "NOT_EXECUTED"',
]) requireText(workflow, fragment, "registry foundation workflow");

if (/^\s+(?:push|pull_request|schedule):/m.test(workflow)) {
  fail("registry foundation workflow must remain explicit workflow_dispatch only");
}

const applyCommands = workflow.match(/terraform\s+-chdir=[^\n]+\s+apply[^\n]*/g) ?? [];
if (applyCommands.length !== 1 || !applyCommands[0].includes("/registry apply") || !applyCommands[0].includes("/tmp/registry.tfplan")) {
  fail(`registry workflow must contain exactly one saved-plan registry apply: ${JSON.stringify(applyCommands)}`);
}

for (const forbidden of [
  /terraform\s+-chdir=[^\n]*\/platform\s+apply/i,
  /terraform\s+-chdir=[^\n]*\/bootstrap\s+apply/i,
  /\bdocker\s+(?:build|push|buildx)\b/i,
  /\bgcloud\s+artifacts\s+docker\b/i,
  /\bgcloud\s+(?:run|compute|storage)\s+[^\n]*(?:create|update|delete|deploy|replace|cp)\b/i,
  /actions\/upload-artifact@/i,
  /\bforce-unlock\b/i,
  /-lock=false\b/i,
  /--target(?:\s|=)/i,
]) {
  if (forbidden.test(workflow)) fail(`registry workflow contains forbidden operation: ${forbidden}`);
}

const registryResources = [...registryMain.matchAll(/^resource\s+"([^"]+)"\s+"([^"]+)"/gm)]
  .map((match) => `${match[1]}.${match[2]}`);
if (registryResources.length !== 1 || registryResources[0] !== "google_artifact_registry_repository.spike") {
  fail(`registry root must own exactly one resource: ${JSON.stringify(registryResources)}`);
}

for (const fragment of [
  'repository_id = "dsg-f3-a3"',
  'location      = var.region',
  'format        = "DOCKER"',
  'description   = "Digest-pinned F3-A3 validation images."',
]) requireText(registryMain, fragment, "registry root");

for (const fragment of [
  'var.project_id == "digital-stargate-telemetry"',
  'var.region == "europe-west8"',
]) requireText(registryVariables, fragment, "registry variables");

for (const fragment of [
  'required_version = ">= 1.16.2, < 2.0.0"',
  'backend "gcs" {}',
  'version = "~> 7.23"',
]) requireText(registryVersions, fragment, "registry versions");

if (/google_artifact_registry_repository/.test(platformMain)) {
  fail("platform root must not retain Artifact Registry ownership");
}

console.log("BKL-031 F3-A3 registry foundation gate verified: one-resource saved-plan apply, no image/platform/scientific execution");
