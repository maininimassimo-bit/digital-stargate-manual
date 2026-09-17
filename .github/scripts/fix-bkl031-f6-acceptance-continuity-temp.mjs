import fs from 'node:fs';

const roadmapPath = '.github/roadmap/roadmap-source.json';
const backlogPath = 'docs/project/BACKLOG.md';

const roadmap = JSON.parse(fs.readFileSync(roadmapPath, 'utf8'));
roadmap.projectStatus = 'BKL-031 F3-C accepted and post-merge verified; ADR-010 accepted; F4-A/ADR-011, F4-B v1.1, F4-C evidence reconciliation, F4-D sanitized forecast projection/portal, F5 explainable ranking method/read-only consumer and F6 real-evidence setup-aware E2E proof accepted and post-merge verified; F6 PR #275 reviewed on ad7cad8267eaee1e27e7b1373d34f422efd8f088, merged as f75303c9575c77f23de777d55c6067bf08bc99f1 and verified 14/14 post-merge; F5 factor values remain synthetic EVALUATION evidence only; F6 forecast evidence is real bounded/generalized but not a fresh runtime feed and setup compatibility remains historical-only; provider budget 2/2 exhausted, zero protected-site use; no readiness/go-no-go, scheduling, automatic target selection, commands or Safety Authority; S10 production runtime unavailable';
fs.writeFileSync(roadmapPath, `${JSON.stringify(roadmap, null, 2)}\n`);

let backlog = fs.readFileSync(backlogPath, 'utf8');
const row = /^\| BKL-031 \|.*$/m;
if (!row.test(backlog)) throw new Error('BKL-031 backlog row missing');
backlog = backlog.replace(row, '| BKL-031 | P1 | Observation Planner intelligente | In Progress | F3-C Accepted/Post-Merge Verified (35/35 tests); F4-A/ADR-011 Accepted/Post-Merge Verified; F4-B v1.1 Accepted/Post-Merge Verified; F4-C evidence reconciliation Accepted/Post-Merge Verified; F4-D metadata-only projection and portal Accepted/Post-Merge Verified; F5 Accepted/Post-Merge Verified; F6 Accepted/Post-Merge Verified via PR #275 merge `f75303c9575c77f23de777d55c6067bf08bc99f1`; provider budget 2/2 exhausted; no protected-site use; S10 unavailable | Execute F7 fresh forecast supply and runtime boundary without treating F6 acceptance as provider-request authority. Preserve ADR-011 exact model/run lineage, freshness/missingness, privacy and request accounting; any new provider traffic requires separate explicit authority/budget approval. Closure remains deferred pending current astronomical windows plus explicit OTA/camera/filter target suitability and final read-only ranking proof | ADR-010; ADR-011; `BKL-031-F6-SOLUTION-001`; F6 acceptance; PR #275; merge `f75303c9…`; evidence `350a7b9a…` |');
fs.writeFileSync(backlogPath, backlog.endsWith('\n') ? backlog : `${backlog}\n`);

console.log('Restored historical BKL-031 continuity markers while retaining F6 acceptance and F7 promotion.');
