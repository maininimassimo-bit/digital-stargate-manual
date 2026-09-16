import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const read = (...parts) => fs.readFileSync(path.join(root, ...parts), "utf8");
const workflow = read(".github", "workflows", "bkl-031-f3-a3-replacement-execution-forensics.yml");
const incident = JSON.parse(read("infrastructure", "bkl-031-f3-a3-gcp", "platform", "BKL-031-F3-A3-REPLACEMENT-EXECUTION-INCIDENT-001.json"));
const fail = (message) => { throw new Error(message); };
const requireText = (fragment) => { if (!workflow.includes(fragment)) fail(`replacement forensics workflow missing: ${fragment}`); };

for (const fragment of [
  "name: BKL-031 F3-A3 Replacement Execution Read-only Forensics", "workflow_dispatch:", "expected_commit:",
  'test "${GITHUB_REF}" = "refs/heads/main"', 'test "${GITHUB_SHA}" = "${DSG_AUTHORIZED_COMMIT}"',
  "DSG_HISTORICAL_EXECUTION: dsg-f3-a3-spike-9drzb", "DSG_REPLACEMENT_EXECUTION: dsg-f3-a3-spike-jv646",
  "DSG_PLATFORM_STATE_SHA256: b12cbd6c107cd7e38d47fbe353ab125ee909dc77d0bc8c26172bfa484b722889",
  "exact two-execution inventory changed", "expected zero scientific evidence objects", "dsg-f3-a3-spike-jv646-task0",
  "gcloud run jobs executions tasks list", "gcloud run jobs executions tasks describe",
  "gcloud alpha run jobs executions logs read", "DSG_REPLACEMENT_LOG_FORENSICS=", "DSG_REPLACEMENT_LOG_ENTRY=",
  "DSG_REPLACEMENT_FORENSICS_POSTCONDITION=", "thirdExecution': 'NOT_EXECUTED'", "cloudMutation': 'NOT_EXECUTED_BY_FORENSICS'",
]) requireText(fragment);

if (/^\s+(?:push|pull_request|schedule):/m.test(workflow)) fail("replacement forensics must remain explicit workflow_dispatch only");
for (const forbidden of [
  /\bgcloud\s+run\s+jobs\s+execute\b/i,
  /\bgcloud\s+run\s+jobs\s+executions\s+(?:cancel|delete)\b/i,
  /\bgcloud\s+run\s+jobs\s+(?:create|update|delete|replace)\b/i,
  /\bterraform\b/i,
  /\bgcloud\s+storage\s+(?:cp|mv|rm)\b/i,
  /\bgcloud\s+artifacts\b/i,
  /\bdocker\b/i,
  /horizons/i,
]) if (forbidden.test(workflow)) fail(`replacement forensics contains forbidden mutation: ${forbidden}`);

if (incident.status !== "TERMINAL_REPLACEMENT_FAILURE_READ_ONLY_FORENSICS_REQUIRED") fail("replacement incident status mismatch");
if (incident.sourceCommit !== "d9fd69d978dd97e680309b55db547b34c84c877f") fail("replacement incident source mismatch");
if (incident.workflow?.runId !== 35160489890 || incident.workflow?.jobId !== 105009877318 || incident.workflow?.conclusion !== "failure") fail("replacement incident workflow identity mismatch");
if (incident.observed?.executionName !== "dsg-f3-a3-spike-jv646" || incident.observed?.executionCount !== 2 || incident.observed?.executionResult !== "COMPLETED_FALSE_NON_ZERO_EXIT_CODE_1") fail("replacement execution facts mismatch");
if (incident.controls?.thirdExecution !== "PROHIBITED_NOT_EXECUTED" || incident.controls?.platformStateRawSha256 !== "b12cbd6c107cd7e38d47fbe353ab125ee909dc77d0bc8c26172bfa484b722889") fail("replacement incident control boundary mismatch");
if (incident.nextGate !== "SEPARATELY_REVIEWED_READ_ONLY_REPLACEMENT_EXECUTION_FORENSICS") fail("replacement incident next gate mismatch");

console.log("BKL-031 F3-A3 replacement execution forensics gate verified: exact two-execution inventory, task and logs read, immutable platform and zero mutation");
