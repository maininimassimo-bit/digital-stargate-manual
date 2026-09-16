import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const workflow = fs.readFileSync(path.join(root, ".github", "workflows", "bkl-031-f3-a3-exact-scientific-execution.yml"), "utf8");
const platformEvidence = JSON.parse(fs.readFileSync(path.join(root, "infrastructure", "bkl-031-f3-a3-gcp", "platform", "BKL-031-F3-A3-RUNNER-PLATFORM-UPDATE-EVIDENCE-001.json"), "utf8"));
const fail = (message) => { throw new Error(message); };
const requireText = (fragment) => { if (!workflow.includes(fragment)) fail(`scientific execution workflow missing: ${fragment}`); };

for (const fragment of [
  "name: BKL-031 F3-A3 Exact Single Scientific Execution", "workflow_dispatch:", "expected_commit:",
  "contents: read", "id-token: write", 'test "${GITHUB_REF}" = "refs/heads/main"',
  'test "${GITHUB_SHA}" = "${DSG_AUTHORIZED_COMMIT}"',
  "node .github/scripts/verify-bkl-031-f3-a3-exact-scientific-execution.mjs",
  "DSG_PLATFORM_STATE_SHA256: 084b68da6d20d9523ceabce67766cfc211b71f97ee12d8f4e7a0b4a64f57b89b",
  "if json.loads(Path('/tmp/executions-before.json').read_text()) != []:",
  "if json.loads(Path('/tmp/evidence-before.json').read_text()) != []:",
  "gcloud run jobs execute dsg-f3-a3-spike",
  "--wait", "expected exactly one execution", "expected one evidence object",
  "if len(scientific.get('vectors', [])) != 8", "scientific.get('repeatabilityPass') is not True",
  "scientific.get('allEvaluatedMetricsPass') is not True", "normalized result digest mismatch",
  "externalReferenceCallCount': 0", "protectedSiteUse': 'NOT_EXECUTED'", "runtimeActivation': 'NOT_EXECUTED'",
  "platform state changed during scientific execution",
]) requireText(fragment);

if (/^\s+(?:push|pull_request|schedule):/m.test(workflow)) fail("scientific execution must remain explicit workflow_dispatch only");
if ((workflow.match(/gcloud run jobs execute dsg-f3-a3-spike/g) || []).length !== 1) fail("scientific gate must contain exactly one job execution command");
for (const forbidden of [
  /\bterraform\s+(?:apply|destroy|import)\b/i,
  /\bgcloud\s+storage\s+(?:cp|mv|rm)\b/i,
  /\bgcloud\s+artifacts\s+(?:repositories|docker)\s+(?:create|update|delete|import)\b/i,
  /\bgcloud\s+run\s+jobs\s+(?:create|update|delete)\b/i,
  /\bdocker\s+(?:build|push)\b/i,
  /horizons/i,
  /protected[-_ ]site/i,
]) if (forbidden.test(workflow)) fail(`scientific execution contains forbidden operation or boundary: ${forbidden}`);

if (platformEvidence.status !== "EXACT_RUNNER_PLATFORM_UPDATED_AND_READ_ONLY_POST_VERIFIED_JOB_UNEXECUTED") fail("platform evidence does not authorize scientific execution");
if (platformEvidence.job?.executionCount !== 0 || platformEvidence.controls?.scientificExecution !== "NOT_EXECUTED") fail("platform evidence does not establish zero prior executions");
if (platformEvidence.nextGate !== "SEPARATELY_REVIEWED_EXACT_SINGLE_SCIENTIFIC_SPIKE_EXECUTION") fail("platform evidence next gate mismatch");

console.log("BKL-031 F3-A3 exact single scientific execution gate verified: one synthetic job execution, one private create-only evidence object, no external reference or runtime activation");
