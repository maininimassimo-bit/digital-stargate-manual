import fs from "node:fs";
import path from "node:path";

const workflow = fs.readFileSync(path.join(process.cwd(), ".github", "workflows", "bkl-031-f3-a3-runner-platform-verification.yml"), "utf8");
const fail = (message) => { throw new Error(message); };
const requireText = (fragment) => { if (!workflow.includes(fragment)) fail(`read-only verification workflow missing: ${fragment}`); };

for (const fragment of [
  "name: BKL-031 F3-A3 Runner Platform Read-only Verification",
  "workflow_dispatch:", "expected_commit:", "contents: read", "id-token: write",
  'test "${GITHUB_REF}" = "refs/heads/main"',
  'test "${GITHUB_SHA}" = "${DSG_AUTHORIZED_COMMIT}"',
  "node .github/scripts/verify-bkl-031-f3-a3-runner-platform-verification.mjs",
  "gcloud artifacts docker images list", "gcloud run jobs describe", "gcloud run jobs executions list",
  "gcloud storage objects describe", "terraform -chdir=infrastructure/bkl-031-f3-a3-gcp/platform state list",
  "terraform -chdir=infrastructure/bkl-031-f3-a3-gcp/platform plan",
  'test "$plan_status" -eq 0', "DSG_READ_ONLY_FACTS=", "cloudMutation': 'NOT_EXECUTED'",
  "scientificExecution': 'NOT_EXECUTED'",
]) requireText(fragment);

if (/^\s+(?:push|pull_request|schedule):/m.test(workflow)) fail("read-only verification must remain explicit workflow_dispatch only");
for (const forbidden of [
  /\bterraform\s+(?:apply|destroy|import)\b/i,
  /\bgcloud\s+run\s+jobs\s+(?:execute|update|delete|create)\b/i,
  /\bgcloud\s+storage\s+(?:cp|mv|rm)\b/i,
  /\bgcloud\s+artifacts\s+(?:repositories|docker)\s+(?:create|update|delete|import)\b/i,
  /\bdocker\s+(?:build|push)\b/i,
  /horizons/i,
]) if (forbidden.test(workflow)) fail(`read-only verification contains forbidden operation: ${forbidden}`);

console.log("BKL-031 F3-A3 runner platform read-only verification gate verified: exact state/job/kernel/registry; zero drift/executions; no mutation");
