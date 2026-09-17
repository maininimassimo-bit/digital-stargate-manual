import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const read = (...parts) => fs.readFileSync(path.join(root, ...parts), "utf8");
const evidenceBytes = fs.readFileSync(path.join(root, "infrastructure", "bkl-031-f3-a3-gcp", "platform", "BKL-031-F3-A3-SCIENTIFIC-EXECUTION-EVIDENCE-001.json"));
const evidence = JSON.parse(evidenceBytes.toString("utf8"));
const adr = read("docs", "architecture", "ADR-010-Ephemeris-Lunar-Method-and-Validation-Profile.md");
const hosting = read("docs", "architecture", "infrastructure", "BKL-031-F3-A3-Google-Cloud-Validation-Spike-Hosting-Plan.md");
const plan = read("docs", "architecture", "validation", "BKL-031-F3-A3-Ephemeris-Lunar-Method-Validation-Spike-Plan.md");
const acceptance = read("docs", "project", "BKL-031-F3-A3-SCIENTIFIC-CAMPAIGN-ACCEPTANCE-2026-09-17.md");
const backlog = read("docs", "project", "BACKLOG.md");
const roadmap = JSON.parse(read(".github", "roadmap", "roadmap-source.json"));
const fail = (message) => { throw new Error(message); };
const exact = (actual, expected, message) => { if (actual !== expected) fail(message); };

exact(crypto.createHash("sha256").update(evidenceBytes).digest("hex"), "f420cefb2257e85e40c51d9b544e3fa8b5cf9fbe9450835f9772ef99e8930241", "scientific execution evidence raw digest mismatch");
exact(evidence.status, "EXACT_REMEDIATED_SCIENTIFIC_CAMPAIGN_PASS", "scientific evidence status mismatch");
exact(evidence.source?.gateCommit, "d7d7077e086fee5dfcd344021f806ee3b6cbaa16", "scientific gate commit mismatch");
exact(evidence.source?.runnerCommit, "5ce8214311757c974134494dcc8f1e232dd4c390", "runner source mismatch");
exact(evidence.source?.runnerImage, "europe-west8-docker.pkg.dev/digital-stargate-telemetry/dsg-f3-a3/spike@sha256:f82acf36b79d6f3d8a3ba501b63bdba3ed446e7cf9070f477b01ed5d356ccb52", "runner image mismatch");
exact(evidence.continuousIntegration?.runId, 35189574972, "scientific run mismatch");
exact(evidence.continuousIntegration?.jobId, 105098953021, "scientific job mismatch");
exact(evidence.continuousIntegration?.conclusion, "SUCCESS", "scientific workflow did not succeed");
exact(evidence.execution?.name, "dsg-f3-a3-spike-g4x8g", "scientific execution name mismatch");
exact(evidence.execution?.result, "COMPLETED_TRUE_SUCCEEDED_COUNT_1", "scientific execution result mismatch");
exact(evidence.campaign?.vectorCount, 8, "scientific vector count mismatch");
exact(evidence.campaign?.metricPassCount, 17, "scientific metric pass count mismatch");
exact(evidence.campaign?.metricEvaluationCount, 17, "scientific metric evaluation count mismatch");
exact(evidence.campaign?.allEvaluatedMetricsPass, true, "scientific metrics did not all pass");
exact(evidence.campaign?.repeatabilityPass, true, "scientific repeatability did not pass");
exact(evidence.campaign?.transitPass, true, "scientific transit did not pass");
if (evidence.campaign?.transitErrorSeconds > 5) fail("scientific transit exceeds approved threshold");
exact(evidence.campaign?.comparisonClassification, "IMPLEMENTATION_CROSS_CHECK_SHARED_GOVERNED_SPK", "cross-check classification mismatch");
exact(evidence.evidenceObject?.generation, "1789626252024638", "private evidence generation mismatch");
exact(evidence.evidenceObject?.rawSha256, "483794c9a8a373e8aff2f0dd2ab0f6342826c9bd210beeebcf92e744fad72494", "private evidence digest mismatch");
exact(evidence.evidenceObject?.normalizedResultSha256, "d4f5163f0ef9c5701fb98a6b9ceef8411c24100e4674298183c770afbc2318e2", "normalized result digest mismatch");
exact(evidence.evidenceObject?.creation, "IF_GENERATION_MATCH_ZERO", "private evidence was not create-only");
exact(evidence.postconditions?.executionCount, 3, "final execution count mismatch");
exact(evidence.postconditions?.successfulExecutionCount, 1, "successful execution count mismatch");
exact(evidence.postconditions?.platformStateSerial, 6, "final platform state serial mismatch");
exact(evidence.postconditions?.platformStateRawSha256, "e527e5f03e0d93a456abc2dc761b19d18479a042ac139960037569c52776f25e", "final platform state digest mismatch");
exact(evidence.controls?.externalReferenceCallCount, 0, "external reference traffic occurred");
exact(evidence.controls?.protectedSiteUse, "NOT_EXECUTED", "protected-site use occurred");
exact(evidence.controls?.runtimeActivation, "NOT_EXECUTED", "runtime activation occurred");

for (const [document, fragments] of [[adr, ["**ACCEPTED — EXACT SCIENTIFIC CAMPAIGN PASS / RUNTIME NOT AUTHORIZED**", "F3-B machine-readable contract and validator work", "S10 remains `UNAVAILABLE`"]], [hosting, ["**SCIENTIFIC CAMPAIGN PASS — PLATFORM RETAINED / RUNTIME NOT AUTHORIZED**", "dsg-f3-a3-spike-g4x8g", "F3-B is the next repository-only gate"]], [plan, ["**EXECUTED — EXACT SCIENTIFIC CAMPAIGN PASS / ADR-010 ACCEPTANCE REVIEW**", "17/17 passing metrics", "Stop before another cloud execution"]], [acceptance, ["**ACCEPTED — POST-MERGE VERIFICATION PENDING**", "dsg-f3-a3-spike-g4x8g", "F3-B becomes the next dependency-ready increment"]], [backlog, ["F3-A3 exact scientific campaign passed", "Materialize F3-B machine-readable contracts and validator"]]]) {
  for (const fragment of fragments) if (!document.includes(fragment)) fail(`acceptance document missing: ${fragment}`);
}
exact(roadmap.currentPackage, "BKL-031", "roadmap current package changed");
exact(roadmap.nextMilestone, "BKL-031 F3-B machine-readable contracts and validator", "roadmap next milestone mismatch");
if (!roadmap.projectStatus.includes("ADR-010 accepted") || !roadmap.projectStatus.includes("S10 runtime unavailable")) fail("roadmap project status mismatch");
if (!roadmap.milestones.some((item) => item.id === "M-BKL031-F3-A3-SCIENTIFIC-ACCEPTANCE")) fail("roadmap scientific acceptance milestone missing");

console.log("BKL-031 F3-A3 scientific execution evidence verified: dsg-f3-a3-spike-g4x8g; 8 vectors; 17/17 metrics; repeatability/transit pass; ADR-010 acceptance candidate; F3-B next");
