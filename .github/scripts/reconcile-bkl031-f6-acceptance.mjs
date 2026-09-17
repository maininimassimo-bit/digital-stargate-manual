import fs from 'node:fs';

const read = p => fs.readFileSync(p, 'utf8');
const write = (p, c) => fs.writeFileSync(p, c.endsWith('\n') ? c : `${c}\n`, 'utf8');
const replaceOne = (text, pattern, replacement, label) => {
  const rx = typeof pattern === 'string' ? null : new RegExp(pattern.source, pattern.flags.includes('g') ? pattern.flags : `${pattern.flags}g`);
  const matches = typeof pattern === 'string' ? text.split(pattern).length - 1 : [...text.matchAll(rx)].length;
  if (matches !== 1) throw new Error(`${label}: expected exactly one match, got ${matches}`);
  return text.replace(pattern, replacement);
};

const OLD_MILESTONE = 'BKL-031 F6 real-evidence setup-aware E2E planner';
const NEXT_MILESTONE = 'BKL-031 F7 fresh forecast supply and runtime boundary';

// Canonical roadmap source.
const roadmapPath = '.github/roadmap/roadmap-source.json';
const roadmap = JSON.parse(read(roadmapPath));
if (roadmap.currentPackage !== 'BKL-031') throw new Error('roadmap currentPackage is not BKL-031');
if (roadmap.nextMilestone !== OLD_MILESTONE) throw new Error(`unexpected previous milestone: ${roadmap.nextMilestone}`);
roadmap.projectStatus = 'BKL-031 F3/F4 evidence chain, F5 explainable ranking method/read-only consumer and F6 real-evidence setup-aware E2E proof accepted and post-merge verified; F6 PR #275 reviewed on ad7cad8267eaee1e27e7b1373d34f422efd8f088, merged as f75303c9575c77f23de777d55c6067bf08bc99f1 and verified 14/14 post-merge; F6 consumes real bounded generalized forecast values and governed setup/session evidence but forecast is not a fresh runtime feed, F5 geometry remains synthetic and setup compatibility remains historical-only; provider validation request budget 2/2 exhausted; no readiness/go-no-go, scheduler, automatic target selection, commands or Safety Authority; S10 production runtime unavailable';
roadmap.nextMilestone = NEXT_MILESTONE;
roadmap.target = 'Establish F7 as a governed fresh forecast supply and runtime boundary for current forecast series at an approved generalized/public location, preserving ADR-011 exact provider/model/run lineage, freshness and missingness semantics, privacy and request accounting. The current validation request budget remains 2/2_EXHAUSTED and no provider request is authorized by F6 acceptance; any new provider traffic requires a separate explicit authority/budget decision before execution. BKL-031 remains In Progress after F7 until a later scientific integration gate provides current astronomical windows plus explicit OTA/camera/filter target suitability and proves final read-only best-target ranking end to end.';
const bkl = roadmap.streams.flatMap(s => s.items ?? []).find(i => i.id === 'BKL-031');
if (!bkl) throw new Error('BKL-031 roadmap item missing');
bkl.note = 'F3/F4 evidence chain, F5 ranking method/read-only consumer and F6 real-evidence setup-aware E2E proof are Accepted/Post-Merge Verified. F6 PR #275 merged as f75303c9575c77f23de777d55c6067bf08bc99f1 after 13/13 exact-head workflows and passed all 14 applicable post-merge workflows. F6 proves real bounded forecast-value flow plus governed setup/session evidence, but not fresh runtime forecast, real current target geometry or explicit OTA/camera/filter suitability. Provider validation budget remains 2/2 exhausted; no new provider traffic, readiness/go-no-go, scheduler, automatic target selection, commands, Safety Authority or S10 production runtime is authorized. F7 fresh forecast supply and runtime boundary is next; BKL-031 remains In Progress.';
if (!roadmap.milestones.some(m => m.id === 'M-BKL031-F6-ACCEPTANCE')) roadmap.milestones.push({
  id: 'M-BKL031-F6-ACCEPTANCE',
  itemRef: 'BKL-031',
  title: 'BKL-031 F6 Real-Evidence Setup-Aware E2E Acceptance',
  date: '2026-09-17',
  description: 'PR #275 passed 13/13 exact-head workflows on ad7cad8267eaee1e27e7b1373d34f422efd8f088, merged with expected-head control as f75303c9575c77f23de777d55c6067bf08bc99f1 and passed 14/14 applicable post-merge workflows. The bounded EVALUATION/NONE/READ_ONLY F6 integration proof is Accepted/Post-Merge Verified with zero provider requests. F7 fresh forecast supply and runtime boundary is next. BKL-031 remains In Progress pending fresh forecast supply, current astronomical windows, explicit OTA/camera/filter suitability and final read-only ranking proof.'
});
write(roadmapPath, JSON.stringify(roadmap, null, 2));

// Backlog remains In Progress.
const backlogPath = 'docs/project/BACKLOG.md';
let backlog = read(backlogPath);
backlog = replaceOne(backlog, '| Versione | 5.32 |', '| Versione | 5.33 |', 'backlog version');
backlog = replaceOne(
  backlog,
  /^\| BKL-031 \|.*$/m,
  '| BKL-031 | P1 | Observation Planner intelligente | In Progress | F3/F4 evidence chain, F5 and F6 Accepted/Post-Merge Verified; F6 PR #275 merge `f75303c9575c77f23de777d55c6067bf08bc99f1`; 13/13 exact-head and 14/14 post-merge; provider validation budget 2/2 exhausted; no protected-site provider use; S10 unavailable | Execute F7 fresh forecast supply and runtime boundary without treating F6 acceptance as provider-request authority. Preserve ADR-011 exact model/run lineage, freshness/missingness, privacy and request accounting; any new provider traffic requires separate explicit authority/budget approval. Closure remains deferred pending current astronomical windows plus explicit OTA/camera/filter target suitability and final read-only ranking proof | ADR-010; ADR-011; `BKL-031-F6-SOLUTION-001`; F6 acceptance; PR #275; merge `f75303c9…`; evidence `350a7b9a…` |',
  'BKL-031 backlog row'
);
write(backlogPath, backlog);

// Decision Log.
const decisionPath = 'docs/project/DECISION_LOG.md';
let decisions = read(decisionPath);
decisions = replaceOne(decisions, '| Versione | 2.8 |', '| Versione | 2.9 |', 'decision log version');
if (!decisions.includes('| DLG-050 |')) {
  const lines = decisions.split('\n');
  const idx = lines.findIndex(l => l.startsWith('| DLG-049 |'));
  if (idx < 0) throw new Error('DLG-049 anchor missing');
  lines.splice(idx + 1, 0, '| DLG-050 | 17/09/2026 | Accettare F6 come bounded E2E integration proof `EVALUATION/NONE/READ_ONLY` che lega real F4-C forecast values, setup authority governata e session evidence senza nuova provider traffic; PR #275 merge `f75303c9575c77f23de777d55c6067bf08bc99f1` verificato 14/14 post-merge. Promuovere esclusivamente F7 fresh forecast supply and runtime boundary e mantenere BKL-031 In Progress. | F6 dimostra il percorso dati reale ma non un forecast runtime fresco, non geometria astronomica corrente e non suitability OTA/camera/filtri. Il budget di validazione resta `2/2_EXHAUSTED`; F6 acceptance non autorizza ulteriori request. | BKL-031 F6 / F7 transition | Accepted / Post-Merge Verified | `BKL-031-F6-SOLUTION-001`; `BKL-031-F6-REAL-EVIDENCE-SETUP-AWARE-E2E-ACCEPTANCE-2026-09-17`; PR #275; exact head `ad7cad8267eaee1e27e7b1373d34f422efd8f088`; merge `f75303c9575c77f23de777d55c6067bf08bc99f1` |');
  decisions = lines.join('\n');
}
write(decisionPath, decisions);

// Governance Center.
const indexPath = 'docs/project/index.md';
let index = read(indexPath);
const f6OldRow = '| [F6 Real-Evidence Setup-Aware E2E Planner](../architecture/scientific-assets/BKL-031-F6-Real-Evidence-Setup-Aware-E2E-Planner.md) | Review Candidate; binds real F4-C forecast values to governed setup/session evidence in a sanitized read-only E2E proof; BKL-031 closure remains deferred |';
const f6NewRow = '| [F6 Real-Evidence Setup-Aware E2E Planner](../architecture/scientific-assets/BKL-031-F6-Real-Evidence-Setup-Aware-E2E-Planner.md) | Accepted/Post-Merge Verified via PR #275 and merge `f75303c9`; real bounded forecast-value + governed setup/session E2E proof; zero provider requests; BKL-031 closure remains deferred |';
if (index.includes(f6OldRow)) index = replaceOne(index, f6OldRow, f6NewRow, 'project index F6 row');
else if (!index.includes(f6NewRow)) throw new Error('project index F6 row anchor missing');
if (!index.includes('BKL-031-F6-REAL-EVIDENCE-SETUP-AWARE-E2E-ACCEPTANCE-2026-09-17.md')) {
  index = replaceOne(index, f6NewRow, `${f6NewRow}\n| [F6 Real-Evidence Setup-Aware E2E Acceptance](BKL-031-F6-REAL-EVIDENCE-SETUP-AWARE-E2E-ACCEPTANCE-2026-09-17.md) | 13/13 exact-head and 14/14 post-merge workflows; F7 fresh forecast supply/runtime boundary next; provider validation budget remains 2/2 exhausted |`, 'project index F6 acceptance anchor');
}
index = replaceOne(
  index,
  /^- BKL-031 F3\/F4 evidence chain and F5 explainable ranking\/read-only consumer are Accepted\/Post-Merge Verified\..*$/m,
  '- BKL-031 F3/F4 evidence chain, F5 explainable ranking/read-only consumer and F6 real-evidence setup-aware E2E proof are Accepted/Post-Merge Verified. F6 merged via PR #275 as `f75303c9575c77f23de777d55c6067bf08bc99f1` after 13/13 exact-head workflows and 14/14 post-merge workflows. Forecast evidence is real bounded/generalized but not a fresh runtime feed; F5 geometry remains synthetic and setup compatibility historical-only. Provider validation budget remains 2/2 exhausted; F7 fresh forecast supply and runtime boundary is next; BKL-031 remains In Progress and S10 production runtime remains `UNAVAILABLE`.',
  'project index current status'
);
index = replaceOne(
  index,
  /^`\.\.\. -> BKL-037 CLOSED.*$/m,
  '`... -> BKL-037 CLOSED -> BKL-041 CLOSED -> BKL-046 CLOSED -> BKL-031 [F1-F6 ACCEPTED / F7 FRESH FORECAST SUPPLY NEXT / CLOSURE DEFERRED / S10 PRODUCTION UNAVAILABLE] -> BKL-032 -> BKL-036 -> BKL-033 -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.',
  'project index sequence'
);
write(indexPath, index);

// MkDocs navigation.
const navPath = 'mkdocs.yml';
let nav = read(navPath);
const navAnchor = '          - BKL-031 F6 - Real-Evidence Setup-Aware E2E Planner: architecture/scientific-assets/BKL-031-F6-Real-Evidence-Setup-Aware-E2E-Planner.md';
if (!nav.includes('BKL-031 F6 - Real-Evidence Setup-Aware E2E Acceptance:')) {
  nav = replaceOne(nav, navAnchor, `${navAnchor}\n          - BKL-031 F6 - Real-Evidence Setup-Aware E2E Acceptance: project/BKL-031-F6-REAL-EVIDENCE-SETUP-AWARE-E2E-ACCEPTANCE-2026-09-17.md`, 'MkDocs F6 anchor');
}
write(navPath, nav);

// Continuity verifiers that are part of the current BKL-031 regression chain.
const verifierPaths = [
  '.github/scripts/verify-observation-planner-ephemeris-lunar-f3b.mjs',
  '.github/scripts/verify-observation-planner-ephemeris-lunar-f3c.mjs',
  '.github/scripts/verify-observation-planner-forecast-f4a.mjs',
  '.github/scripts/verify-observation-planner-forecast-f4b.mjs',
  '.github/scripts/verify-observation-planner-forecast-f4c-gate.mjs',
  '.github/scripts/verify-observation-planner-forecast-f4d.mjs',
  '.github/scripts/verify-observation-planner-ranking-f5.mjs'
];
for (const path of verifierPaths) {
  let text = read(path);
  const patterns = [
    /(roadmap\.nextMilestone\s*,\s*['"])BKL-031 F6 real-evidence setup-aware E2E planner(['"]\s*\))/,
    /(roadmap\.nextMilestone\s*,\s*['"])BKL-031 F6 real-evidence setup-aware E2E planner(['"]\s*,)/
  ];
  let changed = false;
  for (const pattern of patterns) {
    if (pattern.test(text)) {
      text = text.replace(pattern, `$1${NEXT_MILESTONE}$2`);
      changed = true;
      break;
    }
  }
  if (!changed) throw new Error(`${path}: live roadmap nextMilestone assertion not found for ${OLD_MILESTONE}`);
  write(path, text);
}

console.log('BKL-031 F6 acceptance reconciliation applied; F7 fresh forecast supply/runtime boundary promoted; BKL-031 remains In Progress.');
