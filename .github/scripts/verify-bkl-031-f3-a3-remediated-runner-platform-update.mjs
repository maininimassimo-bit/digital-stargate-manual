import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const read = (...parts) => fs.readFileSync(path.join(root, ...parts), "utf8");
const workflow = read(".github", "workflows", "bkl-031-f3-a3-remediated-runner-platform-update.yml");
const variables = read("infrastructure", "bkl-031-f3-a3-gcp", "platform", "variables.tf");
const evidenceBytes = fs.readFileSync(path.join(root, "infrastructure", "bkl-031-f3-a3-gcp", "container", "BKL-031-F3-A3-REMEDIATED-RUNNER-OCI-PUBLICATION-EVIDENCE-001.json"));
const evidence = JSON.parse(evidenceBytes.toString("utf8"));
const source = "5ce8214311757c974134494dcc8f1e232dd4c390";
const priorSource = "9db0267529b6d46a2510b415e4b3f51d668ff024";
const oldDigest = "sha256:69a20a994fde9d5b1533b142760af5796b4ac795a1f00c658373a46d2648d60c";
const newDigest = "sha256:f82acf36b79d6f3d8a3ba501b63bdba3ed446e7cf9070f477b01ed5d356ccb52";
const repo = "europe-west8-docker.pkg.dev/digital-stargate-telemetry/dsg-f3-a3/spike@";
const fail = (message) => { throw new Error(message); };
const requireText = (fragment) => { if (!workflow.includes(fragment)) fail(`remediated platform workflow missing: ${fragment}`); };

for (const fragment of [
  "name: BKL-031 F3-A3 Remediated Runner Platform Update", "workflow_dispatch:", "expected_commit:",
  'test "${GITHUB_REF}" = "refs/heads/main"', 'test "${GITHUB_SHA}" = "${DSG_AUTHORIZED_COMMIT}"',
  `DSG_RUNNER_SOURCE_COMMIT: ${source}`, `DSG_OLD_IMAGE_REFERENCE: ${repo}${oldDigest}`,
  `DSG_RUNNER_IMAGE_REFERENCE: ${repo}${newDigest}`, `TF_VAR_runner_source_commit: ${source}`,
  "TF_VAR_subnet_cidr: 10.88.0.0/26", "node .github/scripts/verify-bkl-031-f3-a3-remediated-runner-oci-publication.mjs",
  "node .github/scripts/verify-bkl-031-f3-a3-remediated-runner-platform-update.mjs",
  "if len(images) != 3:", "dsg-f3-a3-spike-9drzb", "dsg-f3-a3-spike-jv646",
  `before_env.get('DSG_SOURCE_COMMIT') != '${priorSource}'`,
  "after_env != {**before_env, 'DSG_SOURCE_COMMIT': os.environ['DSG_RUNNER_SOURCE_COMMIT']}",
  "if len(changes) != 1 or changes[0].get('address') != 'google_cloud_run_v2_job.spike':",
  "if change.get('actions') != ['update']:",
  "terraform -chdir=infrastructure/bkl-031-f3-a3-gcp/platform apply -input=false -lock-timeout=60s /tmp/runner-update.tfplan",
  "test \"$plan_status\" -eq 0", "savedPlan=0_ADD_1_CHANGE_0_DESTROY",
  "jobExecution=NOT_EXECUTED", "scientificExecution=NOT_EXECUTED", "runtimeActivation=NOT_EXECUTED",
]) requireText(fragment);

if (/^\s+(?:push|pull_request|schedule):/m.test(workflow)) fail("remediated platform update must remain workflow_dispatch only");
if ((workflow.match(/terraform -chdir=.*\sapply\s/g) || []).length !== 1) fail("remediated platform update must contain one Terraform apply");
if (/gcloud run jobs execute/i.test(workflow)) fail("remediated platform update must not execute the job");
for (const forbidden of [
  /\bgcloud\s+storage\s+(?:cp|mv|rm)\b/i, /\bgcloud\s+artifacts\s+(?:repositories|docker)\s+(?:create|update|delete|import)\b/i,
  /\bdocker\s+(?:build|push)\b/i, /\bterraform\s+destroy\b/i, /\bforce-unlock\b/i, /--target(?:\s|=)/i, /horizons/i,
]) if (forbidden.test(workflow)) fail(`remediated platform update contains forbidden operation: ${forbidden}`);

for (const commit of [priorSource, source]) if (!variables.includes(`"${commit}"`)) fail(`platform source allowlist missing ${commit}`);
if (!variables.includes('var.subnet_cidr == "10.88.0.0/26"')) fail("platform /26 invariant missing");
if (crypto.createHash("sha256").update(evidenceBytes).digest("hex") !== "82cdb77ce9d2e889ef714d67a884e5e7f0ae54b75439543d5d9aa0ac2695ed03") fail("publication evidence raw digest mismatch");
if (evidence.status !== "EXACT_REMEDIATED_RUNNER_OCI_PUBLISHED_POST_VERIFIED" || evidence.source?.commit !== source) fail("publication source identity mismatch");
if (evidence.continuousIntegration?.runId !== 35165348826 || evidence.continuousIntegration?.jobId !== 105025082896 || evidence.continuousIntegration?.conclusion !== "SUCCESS") fail("publication run identity mismatch");
if (evidence.image?.reference !== `${repo}${newDigest}` || evidence.image?.configDigest !== "sha256:75bc408cdfb4e9fc1fe0db59c47f8ff71245b73d76ae66cfe02fd03910f74f87") fail("publication image identity mismatch");
if (evidence.registry?.imageCountBefore !== 2 || evidence.registry?.imageCountAfter !== 3 || evidence.registry?.exclusiveExpectedPackageVersionTagsVerified !== true) fail("publication registry postcondition mismatch");
if (evidence.controls?.platformApply !== "NOT_EXECUTED" || evidence.controls?.jobExecution !== "NOT_EXECUTED" || evidence.controls?.runtimeAuthority !== false) fail("publication evidence overstates downstream authority");
if (evidence.nextGate !== "EXACT_ONE_UPDATE_REMEDIATED_RUNNER_PLATFORM_PLAN_APPLY") fail("publication next gate mismatch");

console.log(`BKL-031 F3-A3 remediated platform update gate verified: ${repo}${newDigest}; one saved-plan job update; execution history unchanged`);
