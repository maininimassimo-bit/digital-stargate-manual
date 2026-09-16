import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const read = (...parts) => fs.readFileSync(path.join(root, ...parts), "utf8");
const workflow = read(".github", "workflows", "bkl-031-f3-a3-exact-replacement-scientific-execution.yml");
const remediationBytes = fs.readFileSync(path.join(root, "infrastructure", "bkl-031-f3-a3-gcp", "platform", "BKL-031-F3-A3-SUBNET-REMEDIATION-EVIDENCE-001.json"));
const remediation = JSON.parse(remediationBytes.toString("utf8"));
const incident = JSON.parse(read("infrastructure", "bkl-031-f3-a3-gcp", "platform", "BKL-031-F3-A3-SCIENTIFIC-EXECUTION-INCIDENT-001.json"));
const fail = (message) => { throw new Error(message); };
const requireText = (fragment) => { if (!workflow.includes(fragment)) fail(`replacement execution workflow missing: ${fragment}`); };

for (const fragment of [
  "name: BKL-031 F3-A3 Exact Single Replacement Scientific Execution", "workflow_dispatch:", "expected_commit:",
  'test "${GITHUB_REF}" = "refs/heads/main"', 'test "${GITHUB_SHA}" = "${DSG_AUTHORIZED_COMMIT}"',
  "DSG_HISTORICAL_EXECUTION: dsg-f3-a3-spike-9drzb", "DSG_PLATFORM_STATE_SHA256: b12cbd6c107cd7e38d47fbe353ab125ee909dc77d0bc8c26172bfa484b722889",
  "10.88.0.0/26", "historical plus one replacement execution", "gcloud run jobs execute dsg-f3-a3-spike",
  "--wait", "expected one replacement evidence object", "requestSha256': 'dfac74fd72aa2a835c961cf20c16d88e2ec262cfdca8c45011342436bd05a312'",
  "len(scientific.get('vectors', [])) != 8", "repeatabilityPass", "allEvaluatedMetricsPass",
  "DSG_REPLACEMENT_SCIENTIFIC_EVIDENCE_FACTS=", "exact two-execution history postcondition failed",
  "externalReferenceCallCount': 0", "protectedSiteUse': 'NOT_EXECUTED'", "runtimeActivation': 'NOT_EXECUTED'",
]) requireText(fragment);

if (/^\s+(?:push|pull_request|schedule):/m.test(workflow)) fail("replacement execution must remain explicit workflow_dispatch only");
if ((workflow.match(/gcloud run jobs execute dsg-f3-a3-spike/g) ?? []).length !== 1) fail("replacement gate must contain exactly one execute command");
for (const forbidden of [
  /\bgcloud\s+run\s+jobs\s+executions\s+(?:cancel|delete)\b/i,
  /\bgcloud\s+run\s+jobs\s+(?:create|update|delete)\b/i,
  /\bterraform\b/i,
  /\bgcloud\s+storage\s+(?:cp|mv|rm)\b/i,
  /\bgcloud\s+artifacts\b/i,
  /\bdocker\s+(?:build|push)\b/i,
  /horizons/i,
]) if (forbidden.test(workflow)) fail(`replacement execution contains forbidden operation: ${forbidden}`);

if (crypto.createHash("sha256").update(remediationBytes).digest("hex") !== "9b7218814c6da3964d96489787c60fe8f79411b80d25a790e89d8b5290f20d38") fail("subnet remediation evidence raw digest mismatch");
if (remediation.status !== "DIRECT_VPC_SUBNET_REMEDIATED_POST_VERIFIED" || remediation.apply?.afterCidr !== "10.88.0.0/26") fail("subnet remediation evidence status mismatch");
if (remediation.platformState?.serial !== 5 || remediation.platformState?.rawSha256 !== "b12cbd6c107cd7e38d47fbe353ab125ee909dc77d0bc8c26172bfa484b722889" || remediation.platformState?.immediateDrift !== "ZERO") fail("remediated platform state mismatch");
if (remediation.controls?.historicalExecutionCount !== 1 || remediation.controls?.replacementExecution !== "NOT_EXECUTED" || remediation.controls?.scientificEvidenceObjectCount !== 0) fail("replacement precondition evidence mismatch");
if (remediation.nextGate !== "SEPARATELY_REVIEWED_EXACT_SINGLE_REPLACEMENT_SCIENTIFIC_EXECUTION") fail("remediation next gate mismatch");
if (incident.status !== "PLATFORM_REMEDIATED_REPLACEMENT_EXECUTION_REVIEW_REQUIRED" || incident.nextGate !== "SEPARATELY_REVIEWED_EXACT_SINGLE_REPLACEMENT_SCIENTIFIC_EXECUTION") fail("incident lifecycle mismatch");

console.log("BKL-031 F3-A3 exact replacement execution gate verified: one failed history, remediated /26 platform, one bounded replacement and one private evidence object");
