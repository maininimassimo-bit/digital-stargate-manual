import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const read = (...parts) => fs.readFileSync(path.join(root, ...parts), "utf8");
const workflow = read(".github", "workflows", "bkl-031-f3-a3-direct-vpc-subnet-remediation.yml");
const variables = read("infrastructure", "bkl-031-f3-a3-gcp", "platform", "variables.tf");
const incident = JSON.parse(read("infrastructure", "bkl-031-f3-a3-gcp", "platform", "BKL-031-F3-A3-SCIENTIFIC-EXECUTION-INCIDENT-001.json"));
const evidence = JSON.parse(read("infrastructure", "bkl-031-f3-a3-gcp", "platform", "BKL-031-F3-A3-SCIENTIFIC-EXECUTION-RECOVERY-EVIDENCE-002.json"));
const fail = (message) => { throw new Error(message); };
const requireText = (text, fragment, context) => { if (!text.includes(fragment)) fail(`${context} missing: ${fragment}`); };

for (const fragment of [
  "name: BKL-031 F3-A3 Exact Direct VPC Subnet Remediation", "workflow_dispatch:", "expected_commit:",
  'test "${GITHUB_REF}" = "refs/heads/main"', 'test "${GITHUB_SHA}" = "${DSG_AUTHORIZED_COMMIT}"',
  "DSG_EXECUTION_NAME: dsg-f3-a3-spike-9drzb", "DSG_PLATFORM_STATE_SHA256: 084b68da6d20d9523ceabce67766cfc211b71f97ee12d8f4e7a0b4a64f57b89b",
  "TF_VAR_subnet_cidr: 10.88.0.0/26", "Internal error running task.", "Create exact one-update saved plan",
  "-detailed-exitcode -out=/tmp/subnet-remediation.tfplan", "google_compute_subnetwork.spike",
  "change.get('actions') != ['update']", "10.88.0.0/28", "10.88.0.0/26",
  "terraform -chdir=infrastructure/bkl-031-f3-a3-gcp/platform apply -input=false -lock-timeout=60s /tmp/subnet-remediation.tfplan",
  "test \"$plan_status\" -eq 0", "DSG_SUBNET_REMEDIATION_FACTS=", "replacementExecution': 'NOT_EXECUTED'",
]) requireText(workflow, fragment, "subnet remediation workflow");

if (/^\s+(?:push|pull_request|schedule):/m.test(workflow)) fail("subnet remediation must remain explicit workflow_dispatch only");
if ((workflow.match(/terraform -chdir=.*\sapply\s/g) ?? []).length !== 1) fail("subnet remediation must contain exactly one Terraform apply");
for (const forbidden of [
  /\bgcloud\s+run\s+jobs\s+execute\b/i,
  /\bgcloud\s+run\s+jobs\s+executions\s+(?:cancel|delete)\b/i,
  /\bgcloud\s+storage\s+(?:cp|mv|rm)\b/i,
  /\bgcloud\s+artifacts\b/i,
  /\bdocker\s+(?:build|push)\b/i,
  /\bterraform\s+destroy\b/i,
  /\bforce-unlock\b/i,
  /--target(?:\s|=)/i,
  /horizons/i,
]) if (forbidden.test(workflow)) fail(`subnet remediation contains forbidden operation: ${forbidden}`);

requireText(variables, 'default = "10.88.0.0/26"', "platform subnet variable");
requireText(variables, 'var.subnet_cidr == "10.88.0.0/26"', "platform subnet validation");
if (incident.status !== "TERMINAL_FAILURE_ZERO_EVIDENCE_PLATFORM_REMEDIATION_REQUIRED" || incident.nextGate !== "EXACT_ONE_UPDATE_DIRECT_VPC_SUBNET_REMEDIATION") fail("incident does not authorize exact subnet remediation");
if (incident.cancellationGate?.cancelCommand !== "SKIPPED" || incident.cancellationGate?.cloudMutation !== "NOT_EXECUTED") fail("cancellation gate mutation boundary mismatch");
if (evidence.status !== "TERMINAL_FAILURE_ZERO_EVIDENCE_PLATFORM_REMEDIATION_REQUIRED" || evidence.execution?.failedCount !== 1) fail("terminal recovery evidence mismatch");
if (evidence.observed?.executionCount !== 1 || evidence.observed?.evidenceObjectCount !== 0 || evidence.observed?.secondExecution !== "NOT_EXECUTED") fail("terminal recovery inventory mismatch");
if (evidence.rootCause?.configuredSubnetCidr !== "10.88.0.0/28" || evidence.rootCause?.requiredMinimumSubnetPrefix !== "/26") fail("subnet root-cause evidence mismatch");
if (evidence.nextGate !== "EXACT_ONE_UPDATE_DIRECT_VPC_SUBNET_REMEDIATION") fail("terminal recovery next gate mismatch");

console.log("BKL-031 F3-A3 Direct VPC subnet remediation verified: exact /28 to /26 in-place saved-plan update; no execution or unrelated mutation");
