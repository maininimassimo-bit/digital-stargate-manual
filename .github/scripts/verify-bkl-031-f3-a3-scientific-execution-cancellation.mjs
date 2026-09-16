import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const workflow = fs.readFileSync(path.join(root, ".github", "workflows", "bkl-031-f3-a3-scientific-execution-cancellation.yml"), "utf8");
const incident = JSON.parse(fs.readFileSync(path.join(root, "infrastructure", "bkl-031-f3-a3-gcp", "platform", "BKL-031-F3-A3-SCIENTIFIC-EXECUTION-INCIDENT-001.json"), "utf8"));
const evidence = JSON.parse(fs.readFileSync(path.join(root, "infrastructure", "bkl-031-f3-a3-gcp", "platform", "BKL-031-F3-A3-SCIENTIFIC-EXECUTION-RECOVERY-EVIDENCE-001.json"), "utf8"));
const fail = (message) => { throw new Error(message); };
const requireText = (fragment) => { if (!workflow.includes(fragment)) fail(`scientific cancellation workflow missing: ${fragment}`); };

for (const fragment of [
  "name: BKL-031 F3-A3 Exact Stuck Scientific Execution Cancellation", "workflow_dispatch:", "expected_commit:",
  'test "${GITHUB_REF}" = "refs/heads/main"', 'test "${GITHUB_SHA}" = "${DSG_AUTHORIZED_COMMIT}"',
  "DSG_EXECUTION_NAME: dsg-f3-a3-spike-9drzb", "2026-09-16T21:57:42.096014Z",
  "Waiting for execution to start.", "WaitingForOperation", "gcloud run jobs executions cancel",
  "--no-async", "--quiet", "completed[0].get('reason') != 'Cancelled'",
  "DSG_SCIENTIFIC_CANCELLATION_FACTS=", "EXACT_EXECUTION_CANCELLATION_ONLY",
]) requireText(fragment);

if (/^\s+(?:push|pull_request|schedule):/m.test(workflow)) fail("scientific cancellation must remain explicit workflow_dispatch only");
if ((workflow.match(/gcloud run jobs executions cancel/g) ?? []).length !== 1) fail("scientific cancellation must contain exactly one cancel command");
for (const forbidden of [
  /\bgcloud\s+run\s+jobs\s+execute\b/i,
  /\bgcloud\s+run\s+jobs\s+(?:create|update|delete)\b/i,
  /\bterraform\b/i,
  /\bgcloud\s+storage\s+(?:cp|mv|rm)\b/i,
  /\bgcloud\s+artifacts\b/i,
  /\bdocker\b/i,
  /horizons/i,
]) if (forbidden.test(workflow)) fail(`scientific cancellation contains forbidden mutation: ${forbidden}`);

if (incident.status !== "TERMINAL_FAILURE_ZERO_EVIDENCE_PLATFORM_REMEDIATION_REQUIRED") fail("incident terminal recovery status mismatch");
if (incident.recovery?.runId !== 35157173081 || incident.recovery?.executionName !== "dsg-f3-a3-spike-9drzb") fail("incident recovery identity mismatch");
if (incident.controls?.secondExecution !== "PROHIBITED_NOT_EXECUTED") fail("incident second-execution boundary changed");
if (incident.cancellationGate?.runId !== 35158064462 || incident.cancellationGate?.cancelCommand !== "SKIPPED" || incident.cancellationGate?.cloudMutation !== "NOT_EXECUTED") fail("cancellation gate fail-closed result mismatch");
if (evidence.status !== "READ_ONLY_RECOVERY_COMPLETE_CANCELLATION_REQUIRED" || evidence.observed?.evidenceObjectCount !== 0) fail("read-only recovery evidence mismatch");
if (evidence.rootCause?.configuredSubnetCidr !== "10.88.0.0/28" || evidence.rootCause?.requiredMinimumSubnetPrefix !== "/26") fail("root-cause network evidence mismatch");
if (evidence.controls?.scientificCalculation !== "NOT_STARTED" || evidence.controls?.secondExecution !== "PROHIBITED_PENDING_CANCELLATION_AND_PLATFORM_REMEDIATION") fail("recovery scientific boundary mismatch");

console.log("BKL-031 F3-A3 exact cancellation gate verified: one identified non-started execution, one cancel command, no second execution or unrelated mutation");
