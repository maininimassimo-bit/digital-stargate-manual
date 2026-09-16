import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const workflow = fs.readFileSync(
  path.join(root, ".github", "workflows", "bkl-031-f3-a3-exact-kernel-acquisition-upload.yml"),
  "utf8",
);
const acquisition = fs.readFileSync(
  path.join(root, ".github", "scripts", "acquire-bkl-031-f3-a3-kernel.mjs"),
  "utf8",
);
const approvalPath = path.join(root, "docs", "project", "BKL-031-F3-A3-F3-OD05-SPK-APPROVAL-2026-09-16.md");
const approvalBytes = fs.readFileSync(approvalPath);
const approval = approvalBytes.toString("utf8");
const platformEvidencePath = path.join(
  root,
  "infrastructure",
  "bkl-031-f3-a3-gcp",
  "platform",
  "BKL-031-F3-A3-PLATFORM-APPLY-EVIDENCE-001.json",
);
const platformEvidenceBytes = fs.readFileSync(platformEvidencePath);
const platformEvidence = JSON.parse(platformEvidenceBytes.toString("utf8"));

const officialSource = "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de442s.bsp";
const privateUri = "gs://digital-stargate-telemetry-183451329061-f3-data/bkl-031/f3-a3/artifacts/spk/de442s/sha256/54d97562a5b094d298b1b8eafa5a2e17e3e010ce85e1a366d07f003ad159323c/de442s.bsp";
const sha256 = "54d97562a5b094d298b1b8eafa5a2e17e3e010ce85e1a366d07f003ad159323c";
const md5 = "cc49327e06088124c0e39d8dde9f0b58";
const md5Base64 = "zEkyfgYIgSTA452N3p8LWA==";
const expectedApprovalSha256 = "833a5be5aee72b3a06620f60cc04fa0269b05ba1f7548d70b51bf4999e99ea18";
const expectedPlatformEvidenceSha256 = "ca5952b67904f514e2e05b7abfd8aeb4df71cfdba89958441ca233bd01e710b8";

const fail = (message) => { throw new Error(message); };
const requireText = (label, text, fragment) => {
  if (!text.includes(fragment)) fail(`${label} missing: ${fragment}`);
};
const exact = (actual, expected, label) => {
  if (!Object.is(actual, expected)) fail(`${label}: expected ${JSON.stringify(expected)}, received ${JSON.stringify(actual)}`);
};

for (const fragment of [
  "workflow_dispatch:",
  "expected_commit:",
  "contents: read",
  "id-token: write",
  "runs-on: ubuntu-24.04",
  "cancel-in-progress: false",
  "DSG_AUTHORIZED_COMMIT: ${{ inputs.expected_commit }}",
  officialSource,
  privateUri,
  `DSG_KERNEL_SHA256: ${sha256}`,
  `DSG_KERNEL_MD5: ${md5}`,
  `DSG_KERNEL_MD5_BASE64: ${md5Base64}`,
  'DSG_KERNEL_SIZE: "32701440"',
  'test "${GITHUB_REF}" = "refs/heads/main"',
  'test "${GITHUB_SHA}" = "${DSG_AUTHORIZED_COMMIT}"',
  "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
  "actions/setup-node@820762786026740c76f36085b0efc47a31fe5020",
  "google-github-actions/auth@7c6bc770dae815cd3e89ee6cdf493a5fab2cc093",
  "google-github-actions/setup-gcloud@aa5489c8933f4cc7a4f7d45035b3b1440c9c10db",
  'version: "583.0.0"',
  "projects/183451329061/locations/global/workloadIdentityPools/dsg-f3-a3-github/providers/github-main",
  "node .github/scripts/verify-bkl-031-f3-a3-platform-apply-gate.mjs",
  "node .github/scripts/verify-bkl-031-f3-a3-kernel-acquisition-upload.mjs",
  'gcloud storage buckets describe "gs://${GCP_DATA_BUCKET}"',
  'gcloud storage objects list "gs://${GCP_DATA_BUCKET}/bkl-031/f3-a3/artifacts/spk/de442s/**"',
  'hashlib.sha256(state_path.read_bytes()).hexdigest() != "11b1888ceac0f39552e735d134a134bbbd7a6a75d623ac5c06897583842cf0e4"',
  'state.get("serial") != 3 or len(state.get("resources", [])) != 4',
  "gcloud run jobs executions list --job=dsg-f3-a3-spike",
  'if json.loads(Path("/tmp/job-executions-before-kernel.json").read_text(encoding="utf-8")) != []:',
  "node .github/scripts/acquire-bkl-031-f3-a3-kernel.mjs",
  "--destination /tmp/de442s.bsp",
  "--evidence /tmp/kernel-acquisition.json",
  "gcloud storage cp \\",
  "--if-generation-match=0",
  '--content-md5="$DSG_KERNEL_MD5_BASE64"',
  "--content-type=application/octet-stream",
  "--cache-control=no-store",
  'gcloud storage objects describe "$DSG_KERNEL_URI"',
  'gcloud storage cat "$DSG_KERNEL_URI"',
  'hashlib.sha256(retrieved_bytes).hexdigest() != os.environ["DSG_KERNEL_SHA256"]',
  'hashlib.md5(retrieved_bytes).hexdigest() != os.environ["DSG_KERNEL_MD5"]',
  'if retrieved_bytes[:7] != b"DAF/SPK":',
  'if json.loads(Path("/tmp/job-executions-after-kernel.json").read_text(encoding="utf-8")) != []:',
  '"platformMutation": "NOT_EXECUTED"',
  '"scientificExecution": "NOT_EXECUTED"',
  '"externalReferenceTraffic": "NOT_EXECUTED"',
  '"protectedSiteUse": "NOT_EXECUTED"',
  '"runtimeActivation": "NOT_EXECUTED"',
  '"runtimeAuthority": False',
  "if: always()",
  "rm -f /tmp/de442s.bsp /tmp/de442s.bsp.part /tmp/de442s-from-gcs.bsp /tmp/kernel-acquisition.json",
]) requireText("kernel workflow", workflow, fragment);

for (const fragment of [
  officialSource,
  "https.request(",
  'method: "GET"',
  '"Accept-Encoding": "identity"',
  "response.statusCode !== 200",
  "redirects are not accepted",
  "response.headers.location",
  "expected.sizeBytes",
  `sha256: "${sha256}"`,
  `md5: "${md5}"`,
  'magic: "DAF/SPK"',
  "flags: \"wx\"",
  "requestCount: 1",
  "redirectAccepted: false",
  "fs.renameSync(partial, destination)",
  "fs.rmSync(partial, { force: true })",
]) requireText("kernel acquisition script", acquisition, fragment);

if ((acquisition.match(/https\.request\(/g) ?? []).length !== 1) {
  fail("kernel acquisition script must perform exactly one HTTPS request");
}
if (/https?:\/\/(?!naif\.jpl\.nasa\.gov\/pub\/naif\/generic_kernels\/spk\/planets\/de442s\.bsp)/i.test(acquisition)) {
  fail("kernel acquisition script contains an unapproved network source");
}

const uploadCommands = workflow.match(/^[ \t]*gcloud storage cp\b/gm) ?? [];
if (uploadCommands.length !== 1) fail(`kernel workflow must contain exactly one gcloud storage cp command, received ${uploadCommands.length}`);

for (const forbidden of [
  /^\s+(?:push|pull_request|schedule|workflow_run):/m,
  /\bgcloud\s+run\s+jobs\s+execute\b/i,
  /\bgcloud\s+(?:compute|run|artifacts)\s+[^\n]*(?:create|update|delete|deploy|replace)\b/i,
  /\bgcloud\s+storage\s+(?:rm|mv|rsync)\b/i,
  /\bterraform\s+[^\n]*(?:apply|destroy|force-unlock)\b/i,
  /\bdocker\s+(?:build|push|run)\b/i,
  /actions\/upload-artifact@/i,
  /horizons/i,
]) {
  if (forbidden.test(workflow)) fail(`kernel workflow contains forbidden operation or authority: ${forbidden}`);
}

const approvalSha256 = crypto.createHash("sha256").update(approvalBytes).digest("hex");
exact(approvalSha256, expectedApprovalSha256, "F3-OD05 approval SHA-256");
for (const fragment of [officialSource, "32701440", sha256, md5, "DAF/SPK", privateUri, "NO EXECUTION AUTHORITY"]) {
  requireText("F3-OD05 approval", approval, fragment);
}

const platformEvidenceSha256 = crypto.createHash("sha256").update(platformEvidenceBytes).digest("hex");
exact(platformEvidenceSha256, expectedPlatformEvidenceSha256, "platform apply evidence SHA-256");
exact(platformEvidence.evidenceId, "BKL-031-F3-A3-PLATFORM-APPLY-EVIDENCE-001", "platformEvidence.evidenceId");
exact(platformEvidence.status, "EXACT_FOUR_RESOURCE_PLATFORM_APPLIED_ZERO_DRIFT_JOB_UNEXECUTED", "platformEvidence.status");
exact(platformEvidence.backendState?.rawSha256, "11b1888ceac0f39552e735d134a134bbbd7a6a75d623ac5c06897583842cf0e4", "platformEvidence.backendState.rawSha256");
exact(platformEvidence.backendState?.resourceCount, 4, "platformEvidence.backendState.resourceCount");
exact(platformEvidence.postconditions?.jobExecutionCount, 0, "platformEvidence.postconditions.jobExecutionCount");
exact(platformEvidence.postconditions?.kernelArtifact, "NOT_UPLOADED", "platformEvidence.postconditions.kernelArtifact");
exact(platformEvidence.nextGate, "SEPARATELY_REVIEWED_EXACT_KERNEL_ARTIFACT_ACQUISITION_AND_UPLOAD", "platformEvidence.nextGate");

console.log(`BKL-031 F3-A3 exact kernel acquisition/upload gate verified: one official HTTPS request, one generation-guarded private upload, no job execution; platform evidence sha256:${expectedPlatformEvidenceSha256}`);
