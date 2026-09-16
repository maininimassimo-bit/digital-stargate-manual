import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const read = (...parts) => fs.readFileSync(path.join(root, ...parts), "utf8");
const workflow = read(".github", "workflows", "bkl-031-f3-a3-offline-exact-kernel-validation.yml");
const rootCause = JSON.parse(read("infrastructure", "bkl-031-f3-a3-gcp", "platform", "BKL-031-F3-A3-REPLACEMENT-ROOT-CAUSE-EVIDENCE-001.json"));
const manifest = JSON.parse(read("infrastructure", "bkl-031-f3-a3-gcp", "container", "BKL-031-F3-A3-RUNNER-MANIFEST-003.json"));
const incident = JSON.parse(read("infrastructure", "bkl-031-f3-a3-gcp", "platform", "BKL-031-F3-A3-OFFLINE-VALIDATION-INCIDENT-001.json"));
const fail = (message) => { throw new Error(message); };
const requireText = (fragment) => { if (!workflow.includes(fragment)) fail(`offline exact-kernel workflow missing: ${fragment}`); };

for (const fragment of [
  "name: BKL-031 F3-A3 Offline Exact Kernel Validation", "workflow_dispatch:", "expected_commit:",
  'test "${GITHUB_REF}" = "refs/heads/main"', 'test "${GITHUB_SHA}" = "${DSG_AUTHORIZED_COMMIT}"',
  "gcloud storage objects describe", "gcloud storage cat", "generation')) != '1789590110146663'", "32701440",
  "docker buildx build", "--network=none", "--network none", "--read-only",
  "offline_exact_kernel_validation.py --kernel /kernel/de442s.bsp", "DSG_OFFLINE_EXACT_KERNEL_VALIDATION=",
  "jobExecution\":\"NOT_EXECUTED", "platformMutation\":\"NOT_EXECUTED", "evidenceUpload\":\"NOT_EXECUTED",
]) requireText(fragment);

if (/^\s+(?:push|pull_request|schedule):/m.test(workflow)) fail("offline exact-kernel validation must remain explicit workflow_dispatch only");
for (const forbidden of [
  /\bgcloud\s+run\s+jobs\s+execute\b/i,
  /\bgcloud\s+run\s+jobs\s+executions\s+(?:cancel|delete)\b/i,
  /\bterraform\b/i,
  /\bgcloud\s+storage\s+(?:cp|mv|rm)\b/i,
  /\bgcloud\s+artifacts\b/i,
  /\bdocker\s+(?:push|login)\b/i,
  /horizons/i,
]) if (forbidden.test(workflow)) fail(`offline exact-kernel validation contains forbidden mutation: ${forbidden}`);

if (rootCause.status !== "ROOT_CAUSE_CONFIRMED_RUNNER_SOURCE_REMEDIATION_REQUIRED" || rootCause.failedExecution !== "dsg-f3-a3-spike-jv646") fail("root-cause evidence identity mismatch");
if (rootCause.cloudLog?.exception !== "KeyError" || rootCause.cloudLog?.kernelSupportedMarsNaifId !== 4 || rootCause.cloudLog?.kernelMissingMarsCenterNaifId !== 499) fail("root-cause kernel facts mismatch");
if (rootCause.controls?.thirdExecution !== "NOT_EXECUTED" || rootCause.controls?.cloudMutation !== "NOT_EXECUTED_BY_ROOT_CAUSE_READ") fail("root-cause control boundary mismatch");
if (rootCause.nextGate !== "REVIEW_RUNNER_TARGET_RESOLUTION_AND_OFFLINE_EXACT_KERNEL_VALIDATION") fail("root-cause next gate mismatch");
if (incident.status !== "FAILED_CLOSED_RUNNER_JSON_NORMALIZATION_REQUIRED" || incident.workflowRunId !== 35163106441 || incident.execution?.exception !== "TypeError") fail("offline validation incident identity mismatch");
if (incident.analysis?.rootCause !== "NUMPY_BOOLEAN_SUM_PRODUCED_INT64_METRIC_PASS_COUNT" || incident.controls?.cloudRunJobExecution !== "NOT_EXECUTED" || incident.controls?.cloudMutation !== "NOT_EXECUTED") fail("offline validation incident control mismatch");
if (manifest.manifestId !== "BKL-031-F3-A3-RUNNER-MANIFEST-003" || manifest.runner?.targetResolution?.mars !== "mars barycenter" || manifest.runner?.targetResolution?.moon !== "moon") fail("remediated runner manifest mismatch");
if (manifest.remediation?.offlineValidationIncident !== incident.incidentId || manifest.remediation?.rootCause !== incident.analysis.rootCause) fail("offline validation remediation lineage mismatch");

console.log("BKL-031 F3-A3 offline exact-kernel validation gate verified: private kernel read only, container network none, no cloud mutation or scientific job execution");
