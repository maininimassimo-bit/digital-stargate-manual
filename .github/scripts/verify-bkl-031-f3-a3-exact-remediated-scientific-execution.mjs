import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const read = (...parts) => fs.readFileSync(path.join(root, ...parts), "utf8");
const workflow = read(".github", "workflows", "bkl-031-f3-a3-exact-remediated-scientific-execution.yml");
const evidenceBytes = fs.readFileSync(path.join(root, "infrastructure", "bkl-031-f3-a3-gcp", "platform", "BKL-031-F3-A3-REMEDIATED-RUNNER-PLATFORM-UPDATE-EVIDENCE-001.json"));
const evidence = JSON.parse(evidenceBytes.toString("utf8"));
const incidentBytes = fs.readFileSync(path.join(root, "infrastructure", "bkl-031-f3-a3-gcp", "platform", "BKL-031-F3-A3-REMEDIATED-SCIENTIFIC-PREFLIGHT-INCIDENT-001.json"));
const incident = JSON.parse(incidentBytes.toString("utf8"));
const runner = read("infrastructure", "bkl-031-f3-a3-gcp", "runner", "scientific_runner.py");
const source = "5ce8214311757c974134494dcc8f1e232dd4c390";
const image = "europe-west8-docker.pkg.dev/digital-stargate-telemetry/dsg-f3-a3/spike@sha256:f82acf36b79d6f3d8a3ba501b63bdba3ed446e7cf9070f477b01ed5d356ccb52";
const stateSha = "e527e5f03e0d93a456abc2dc761b19d18479a042ac139960037569c52776f25e";
const fail = (message) => { throw new Error(message); };
const requireText = (fragment) => { if (!workflow.includes(fragment)) fail(`remediated execution workflow missing: ${fragment}`); };

for (const fragment of [
  "name: BKL-031 F3-A3 Exact Remediated Scientific Execution", "workflow_dispatch:", "expected_commit:",
  'test "${GITHUB_REF}" = "refs/heads/main"', 'test "${GITHUB_SHA}" = "${DSG_AUTHORIZED_COMMIT}"',
  `DSG_RUNNER_SOURCE_COMMIT: ${source}`, `DSG_RUNNER_IMAGE_REFERENCE: ${image}`,
  `DSG_EVIDENCE_PREFIX: bkl-031/f3-a3/scientific-spike/${source}`, `DSG_PLATFORM_STATE_SHA256: ${stateSha}`,
  "node .github/scripts/verify-bkl-031-f3-a3-exact-remediated-scientific-execution.mjs",
  "state.get('serial') != 6", "10.88.0.0/26", "job.get('metadata', {}).get('generation') != 3",
  "dsg-f3-a3-spike-9drzb", "dsg-f3-a3-spike-jv646", "remediated source evidence prefix is not empty",
  "gcloud run jobs execute dsg-f3-a3-spike", "two historical failures plus one remediated execution",
  "expected one remediated evidence object", "requestSha256': 'dfac74fd72aa2a835c961cf20c16d88e2ec262cfdca8c45011342436bd05a312'",
  "len(scientific.get('vectors', [])) != 8", "metricPassCount') != 17", "metricEvaluationCount') != 17",
  "repeatabilityPass", "allEvaluatedMetricsPass", "normalized result digest mismatch",
  "DSG_REMEDIATED_SCIENTIFIC_EVIDENCE_FACTS=", "exact three-execution history postcondition failed",
  "ONE_JOB_EXECUTION_AND_ONE_CREATE_ONLY_EVIDENCE_OBJECT", "externalReferenceCallCount': 0",
  "protectedSiteUse': 'NOT_EXECUTED'", "runtimeActivation': 'NOT_EXECUTED'",
]) requireText(fragment);

if (/^\s+(?:push|pull_request|schedule):/m.test(workflow)) fail("remediated scientific execution must remain explicit workflow_dispatch only");
if ((workflow.match(/gcloud run jobs execute dsg-f3-a3-spike/g) ?? []).length !== 1) fail("remediated gate must contain exactly one execute command");
for (const forbidden of [
  /\bgcloud\s+run\s+jobs\s+executions\s+(?:cancel|delete)\b/i,
  /\bgcloud\s+run\s+jobs\s+(?:create|update|delete)\b/i,
  /\bterraform\b/i,
  /\bgcloud\s+storage\s+(?:cp|mv|rm)\b/i,
  /\bgcloud\s+artifacts\s+(?:repositories|docker)\s+(?:create|update|delete|import)\b/i,
  /\bdocker\s+(?:build|push)\b/i,
  /horizons/i,
]) if (forbidden.test(workflow)) fail(`remediated execution contains forbidden operation: ${forbidden}`);

if (crypto.createHash("sha256").update(evidenceBytes).digest("hex") !== "0e5c68ba84ccaeaaedf6f7fcca9c78034db22586fa9b3de1f46a93e5896675fb") fail("remediated platform update evidence raw digest mismatch");
if (crypto.createHash("sha256").update(incidentBytes).digest("hex") !== "681d14ce2b71a02f5976321961ff6a7f9e918d491e4aa5b44b9d846fc42638f2") fail("remediated preflight incident raw digest mismatch");
if (evidence.status !== "EXACT_REMEDIATED_RUNNER_PLATFORM_UPDATED_POST_VERIFIED" || evidence.source?.gateCommit !== "50290eb0c1fdcb1405f871b88cbf3367886c3163" || evidence.source?.runnerCommit !== source || evidence.source?.runnerImage !== image) fail("remediated platform source identity mismatch");
if (evidence.continuousIntegration?.runId !== 35166175815 || evidence.continuousIntegration?.jobId !== 105027664096 || evidence.continuousIntegration?.conclusion !== "SUCCESS") fail("remediated platform run identity mismatch");
if (evidence.apply?.savedPlan !== "0_ADD_1_CHANGE_0_DESTROY" || evidence.apply?.resource !== "google_cloud_run_v2_job.spike" || evidence.apply?.action !== "UPDATE") fail("remediated platform apply scope mismatch");
if (evidence.platformState?.serial !== 6 || evidence.platformState?.rawSha256 !== stateSha || evidence.platformState?.rawAcquisition !== "BYTE_PRESERVING_GCLOUD_STORAGE_CP" || evidence.platformState?.resourceCount !== 4 || evidence.platformState?.immediateDrift !== "ZERO") fail("remediated platform state mismatch");
if (evidence.postconditions?.jobGeneration !== 3 || evidence.postconditions?.subnetCidr !== "10.88.0.0/26" || evidence.postconditions?.registryImageCount !== 3 || evidence.postconditions?.executionCount !== 2) fail("remediated platform postcondition mismatch");
if (JSON.stringify(evidence.postconditions?.executionNames) !== JSON.stringify(["dsg-f3-a3-spike-9drzb", "dsg-f3-a3-spike-jv646"])) fail("failed execution history mismatch");
if (evidence.controls?.jobExecution !== "NOT_EXECUTED" || evidence.controls?.scientificExecution !== "NOT_EXECUTED" || evidence.controls?.runtimeAuthority !== false) fail("platform evidence overstates execution authority");
if (evidence.nextGate !== "EXACT_SINGLE_REMEDIATED_SCIENTIFIC_EXECUTION") fail("platform evidence next gate mismatch");
if (incident.status !== "PREFLIGHT_FAILED_CLOUD_EXECUTION_NOT_STARTED" || incident.sourceCommit !== "8a4360cf7c7b834e4a043691e0f4a30494a01b23") fail("preflight incident identity mismatch");
if (incident.workflow?.runId !== 35188870937 || incident.workflow?.jobId !== 105096784195 || incident.workflow?.conclusion !== "FAILURE") fail("preflight incident run identity mismatch");
if (incident.cause?.classification !== "LOCAL_EVIDENCE_ACQUISITION_CHANGED_STATE_BYTES" || incident.cause?.exactCloudRawSha256 !== stateSha) fail("preflight incident cause mismatch");
if (incident.verifiedPostconditions?.executionCount !== 2 || incident.verifiedPostconditions?.remediatedEvidenceObjectCount !== 0) fail("preflight incident postcondition mismatch");
if (incident.controls?.executeStep !== "SKIPPED" || incident.controls?.jobExecution !== "NOT_EXECUTED" || incident.controls?.cloudMutation !== "NOT_EXECUTED") fail("preflight incident mutation boundary mismatch");
if (incident.nextGate !== "REVIEW_CORRECTED_EXACT_SINGLE_REMEDIATED_SCIENTIFIC_EXECUTION") fail("preflight incident next gate mismatch");
if (!runner.includes('"ifGenerationMatch": "0"')) fail("runner evidence upload is not create-only");

console.log(`BKL-031 F3-A3 exact remediated scientific execution gate verified: ${image}; two failed histories; one bounded execution; one create-only evidence object`);
