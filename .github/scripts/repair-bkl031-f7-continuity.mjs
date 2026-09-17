import fs from 'node:fs';

const oldMilestone = 'BKL-031 F7 fresh forecast supply and runtime boundary';
const newMilestone = 'BKL-031 F8 current astronomy and explicit setup suitability integration';
const verifierPaths = [
  '.github/scripts/verify-observation-planner-ephemeris-lunar-f3c.mjs',
  '.github/scripts/verify-observation-planner-forecast-f4a.mjs',
  '.github/scripts/verify-observation-planner-forecast-f4b.mjs',
  '.github/scripts/verify-observation-planner-forecast-f4c-gate.mjs',
  '.github/scripts/verify-observation-planner-forecast-f4d.mjs',
  '.github/scripts/verify-observation-planner-ranking-f5.mjs',
  '.github/scripts/verify-observation-planner-e2e-f6.mjs'
];

for (const path of verifierPaths) {
  let text = fs.readFileSync(path, 'utf8');
  if (text.includes(oldMilestone)) {
    text = text.split(oldMilestone).join(newMilestone);
    fs.writeFileSync(path, text);
  }
}

const roadmapPath = '.github/roadmap/roadmap-source.json';
const roadmap = JSON.parse(fs.readFileSync(roadmapPath, 'utf8'));
roadmap.projectStatus = 'BKL-031 F3-C accepted and post-merge verified; ADR-010 accepted; F4-A/ADR-011 accepted and post-merge verified; F4-B v1.1 accepted; F4-C evidence reconciliation accepted with historical generalized provider budget 2/2 exhausted; F4-D sanitized forecast projection/portal accepted; F5 explainable ranking method/read-only consumer accepted; F6 real-evidence setup-aware E2E accepted; F7 protected-site forecast supply accepted and post-merge verified via PR #277 and merge 59a1d690406d733b6e61e64220f84cef9b6fb1a2; F7 protected-site one-shot budget 1/1 exhausted; recurring refresh not activated; current astronomical geometry and explicit OTA/camera/filter suitability remain unresolved; no readiness/go-no-go, scheduling, automatic target selection, commands or Safety Authority; S10 production runtime unavailable';
roadmap.nextMilestone = newMilestone;
fs.writeFileSync(roadmapPath, `${JSON.stringify(roadmap, null, 2)}\n`);

const backlogPath = 'docs/project/BACKLOG.md';
let backlog = fs.readFileSync(backlogPath, 'utf8');
const row = '| BKL-031 | P1 | Observation Planner intelligente | In Progress | F3-C Accepted/Post-Merge Verified (35/35 tests); F4-A/ADR-011; F4-B v1.1 Accepted/Post-Merge Verified; historical generalized provider budget 2/2 exhausted; F4-D metadata-only projection and portal Accepted/Post-Merge Verified; F5/F6/F7 Accepted/Post-Merge Verified; F7 PR #277 merge `59a1d690406d733b6e61e64220f84cef9b6fb1a2`; protected-site F7 budget 1/1 exhausted; recurring refresh not activated; S10 unavailable | Execute F8 current astronomy and explicit OTA/camera/filter target suitability integration, combining those inputs with governed current weather in explainable read-only ranking. Preserve fail-closed freshness/privacy; recurring provider runtime requires separate operating authorization before closure | ADR-010; ADR-011; `BKL-031-F7-SOLUTION-001`; F7 acceptance; PR #277; merge `59a1d690…` |';
if (!/^\| BKL-031 \|.*$/m.test(backlog)) throw new Error('BKL-031 backlog row missing');
backlog = backlog.replace(/^\| BKL-031 \|.*$/m, row);
fs.writeFileSync(backlogPath, backlog);

console.log('BKL-031 predecessor continuity repaired through F8 promotion without weakening scientific, privacy or safety assertions.');
