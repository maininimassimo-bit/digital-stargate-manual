import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const workflow = fs.readFileSync(path.join(root, ".github", "workflows", "bkl-031-f3-a3-scientific-execution-recovery.yml"), "utf8");
const incident = JSON.parse(fs.readFileSync(path.join(root, "infrastructure", "bkl-031-f3-a3-gcp", "platform", "BKL-031-F3-A3-SCIENTIFIC-EXECUTION-INCIDENT-001.json"), "utf8"));
const fail = (message) => { throw new Error(message); };
const requireText = (fragment) => { if (!workflow.includes(fragment)) fail(`scientific recovery workflow missing: ${fragment}`); };

for (const fragment of [
  "name: BKL-031 F3-A3 Scientific Execution Read-only Recovery", "workflow_dispatch:", "expected_commit:",
  'test "${GITHUB_REF}" = "refs/heads/main"', 'test "${GITHUB_SHA}" = "${DSG_AUTHORIZED_COMMIT}"',
  "gcloud run jobs executions list", "gcloud run jobs executions describe", "gcloud storage objects list",
  "expected the exclusive single execution", "if len(objects) > 1:",
  "DSG_EXECUTION_RECOVERY_FACTS=", "DSG_RECOVERED_EVIDENCE_FACTS=",
  "secondExecution': 'NOT_EXECUTED'", "cloudMutation': 'NOT_EXECUTED_BY_RECOVERY'",
]) requireText(fragment);

if (/^\s+(?:push|pull_request|schedule):/m.test(workflow)) fail("scientific recovery must remain explicit workflow_dispatch only");
for (const forbidden of [
  /\bgcloud\s+run\s+jobs\s+execute\b/i,
  /\bgcloud\s+run\s+jobs\s+(?:create|update|delete)\b/i,
  /\bterraform\b/i,
  /\bgcloud\s+storage\s+(?:cp|mv|rm)\b/i,
  /\bgcloud\s+artifacts\b/i,
  /\bdocker\b/i,
  /horizons/i,
]) if (forbidden.test(workflow)) fail(`scientific recovery contains forbidden mutation: ${forbidden}`);

if (incident.status !== "GITHUB_WAIT_TIMEOUT_SINGLE_EXECUTION_CREATED_TERMINAL_STATE_PENDING_RECOVERY") fail("scientific execution incident status mismatch");
if (incident.workflow?.runId !== 35155130422 || incident.workflow?.jobId !== 104992662577 || incident.workflow?.conclusion !== "failure") fail("scientific execution incident run identity mismatch");
if (incident.controls?.secondExecution !== "PROHIBITED_NOT_EXECUTED" || incident.controls?.recoveryMode !== "READ_ONLY_REQUIRED") fail("scientific execution incident recovery boundary mismatch");

console.log("BKL-031 F3-A3 scientific execution read-only recovery gate verified: exclusive single execution inspection, optional private evidence read, no mutation");
