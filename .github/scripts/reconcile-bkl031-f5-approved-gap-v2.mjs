import fs from 'node:fs';

const NEXT = 'BKL-031 F6 real-evidence setup-aware E2E planner';
const read = (p) => fs.readFileSync(p, 'utf8');
const write = (p, c) => fs.writeFileSync(p, c);

function replaceOnce(path, oldText, newText) {
  const source = read(path);
  const count = source.split(oldText).length - 1;
  if (count !== 1) throw new Error(`${path}: expected exactly one match for ${JSON.stringify(oldText)}, found ${count}`);
  write(path, source.replace(oldText, newText));
}
function replaceLine(path, prefix, newLine) {
  const lines = read(path).split('\n');
  const indexes = [];
  lines.forEach((line, i) => { if (line.startsWith(prefix)) indexes.push(i); });
  if (indexes.length !== 1) throw new Error(`${path}: expected exactly one line starting ${prefix}, found ${indexes.length}`);
  lines[indexes[0]] = newLine;
  write(path, lines.join('\n'));
}
function replaceSuffixSection(path, marker, replacement) {
  const source = read(path);
  const index = source.indexOf(marker);
  if (index < 0) throw new Error(`${path}: missing section ${marker.trim()}`);
  write(path, `${source.slice(0, index)}${marker}${replacement}`);
}
function replaceRequired(path, oldText, newText) {
  const source = read(path);
  if (!source.includes(oldText)) throw new Error(`${path}: missing required text ${JSON.stringify(oldText)}`);
  write(path, source.replaceAll(oldText, newText));
}

const roadmapPath = '.github/roadmap/roadmap-source.json';
const roadmap = JSON.parse(read(roadmapPath));
roadmap.projectStatus = 'BKL-031 F3-C accepted and post-merge verified; ADR-010 accepted; F4-A/ADR-011, F4-B v1.1, F4-C evidence reconciliation, F4-D sanitized forecast projection/portal and F5 explainable ranking method/read-only consumer accepted and post-merge verified; F5 PR #273 merged as 777924e2638430f15bf717fa33dd71057751625a with 7/7 post-merge workflows; factor values remain synthetic EVALUATION evidence only; provider request budget 2/2 exhausted, acquisition path removed, zero protected-site use; no readiness/go-no-go, scheduling, automatic target selection, commands or Safety Authority; S10 production runtime unavailable';
roadmap.currentPackage = 'BKL-031';
roadmap.nextMilestone = NEXT;
roadmap.target = 'Integrate the accepted F4-C real forecast evidence values, governed setup compatibility, accepted astronomical/lunar evidence and the F5 explainable method into a deterministic read-only end-to-end planner projection and portal proof. F6 performs no new provider request and preserves the exhausted 2/2 budget, no protected-site use, no readiness/go-no-go, no scheduler, no automatic target selection, no command path and local physical-interlock Safety Authority. BKL-031 closure remains deferred pending a separately governed forecast-refresh/runtime gate.';
const bkl031 = roadmap.streams.flatMap((s) => s.items ?? []).find((item) => item.id === 'BKL-031');
if (!bkl031) throw new Error('roadmap BKL-031 item missing');
bkl031.status = 'active';
bkl031.note = 'F3/F4 evidence chain and F5 explainable ranking/read-only consumer are Accepted/Post-Merge Verified. F5 merged via PR #273 as 777924e2638430f15bf717fa33dd71057751625a after exact-head ARB/RQ and completed 7/7 post-merge workflows. F5 values are synthetic method-validation evidence only. Provider budget remains 2/2 exhausted; no protected-site acquisition, readiness/go-no-go, scheduler, automatic target selection, commands, Safety Authority or S10 production runtime is authorized. F6 real-evidence setup-aware E2E planner integration is next; capability closure is deferred pending a separately governed forecast-refresh/runtime gate.';
write(roadmapPath, `${JSON.stringify(roadmap, null, 2)}\n`);

replaceLine('docs/project/BACKLOG.md', '| BKL-031 |', '| BKL-031 | P1 | Observation Planner intelligente | In Progress | F3-C Accepted/Post-Merge Verified; F4-A/ADR-011 Accepted/Post-Merge Verified; F4-B v1.1 Accepted/Post-Merge Verified; F4-C evidence reconciliation Accepted/Post-Merge Verified; F4-D metadata-only projection and portal Accepted/Post-Merge Verified; F5 Accepted/Post-Merge Verified; F5 PR #273 merge `777924e2638430f15bf717fa33dd71057751625a`; provider budget 2/2 exhausted; no protected-site use; S10 unavailable | Execute F6 real-evidence setup-aware E2E planner integration using accepted F4-C real forecast evidence plus governed setup and astronomy; no new provider traffic in F6, readiness/go-no-go, scheduling, automatic target selection, command path or Safety Authority. Capability closure remains deferred pending a separately governed forecast-refresh/runtime gate | ADR-010; ADR-011; `BKL-031-F5-RANKING-001`; F5 acceptance; PR #273; merge `777924e2…`; evidence `350a7b9a…` |');

replaceLine('docs/project/DECISION_LOG.md', '| DLG-049 |', '| DLG-049 | 17/09/2026 | Accettare F5 come metodo di ranking spiegabile deterministico EVALUATION/NONE/READ_ONLY con fixture a valori sintetici, decomposition completa e nessuna autorità operativa; PR #273 merge `777924e2638430f15bf717fa33dd71057751625a` verificato 7/7 post-merge. A seguito della gap review owner-approved, differire la capability closure e promuovere esclusivamente F6 real-evidence setup-aware E2E planner integration. | Il metodo F5 è validato ma i valori sono sintetici e F4-D è metadata-only; BKL-031 non può essere chiuso prima di una prova E2E che consumi evidence meteo reale e setup governato. F6 riusa l’evidence F4-C già acquisita senza nuova provider traffic; il refresh forecast/runtime resta un gate successivo separato. | BKL-031 F5 / F6 transition | Accepted / Post-Merge Verified / Successor revised by owner approval | `BKL-031-F5-RANKING-001`; `BKL-031-F5-EXPLAINABLE-RANKING-ACCEPTANCE-2026-09-17`; PR #273; exact head `dfda963e7e9d088282516200a6bd8bb64dd0dd1d`; merge `777924e2638430f15bf717fa33dd71057751625a` |');

replaceOnce('docs/project/index.md', 'Factor values remain synthetic EVALUATION evidence only; provider budget remains 2/2 exhausted; F6 capability closure is next; S10 production runtime remains `UNAVAILABLE`.', 'Factor values remain synthetic EVALUATION evidence only; provider budget remains 2/2 exhausted; F6 real-evidence setup-aware E2E planner integration is next; capability closure is deferred pending a separately governed forecast-refresh/runtime gate; S10 production runtime remains `UNAVAILABLE`.');
replaceOnce('docs/project/index.md', 'BKL-031 [F1-F5 ACCEPTED / F6 CLOSURE NEXT / S10 PRODUCTION UNAVAILABLE]', 'BKL-031 [F1-F5 ACCEPTED / F6 REAL-EVIDENCE SETUP-AWARE E2E NEXT / CLOSURE DEFERRED / S10 PRODUCTION UNAVAILABLE]');

replaceSuffixSection('docs/architecture/scientific-assets/BKL-031-F5-Explainable-Ranking-Method-and-Read-Only-Consumer.md', '## 11. Successor boundary\n\n', 'With F5 Accepted/Post-Merge Verified, **F6 — real-evidence setup-aware E2E planner integration** becomes the next separately governed BKL-031 slice. F6 must bind the accepted F4-C real forecast evidence values, governed setup compatibility, accepted astronomical/lunar evidence and the F5 explainable ranking method into a deterministic read-only end-to-end planner proof and portal consumer. F6 performs no new provider request and must preserve the exhausted `2/2_EXHAUSTED` budget, no protected-site use, no readiness/go-no-go, no scheduling, no automatic target selection, no commands and no Safety Authority. BKL-031 capability closure is explicitly deferred until a later separately governed forecast-refresh/runtime gate proves how fresh forecast evidence is supplied without weakening ADR-011 lineage or the safety boundary.\n');
replaceSuffixSection('docs/project/BKL-031-F5-EXPLAINABLE-RANKING-ACCEPTANCE-2026-09-17.md', '## Transition\n\n', 'F5 acceptance authorizes only the separately governed **F6 real-evidence setup-aware E2E planner integration** package. F6 must consume the already accepted F4-C real forecast evidence, governed setup compatibility and accepted astronomical/lunar evidence through the F5 explainable method, then prove the resulting read-only planner path end to end on the portal. F6 performs no new provider request and does not authorize readiness/go-no-go, scheduling, automatic target selection, commands or Safety Authority. BKL-031 capability closure is deferred until a later separately governed forecast-refresh/runtime gate establishes fresh forecast supply while preserving ADR-011 lineage, the exhausted current request budget and S10/runtime boundaries.\n');

const oldF5 = 'BKL-031 F5 explainable ranking method and read-only consumer';
for (const path of [
  '.github/scripts/verify-observation-planner-ephemeris-lunar-f3b.mjs',
  '.github/scripts/verify-observation-planner-ephemeris-lunar-f3c.mjs',
  '.github/scripts/verify-observation-planner-forecast-f4a.mjs',
  '.github/scripts/verify-observation-planner-forecast-f4b.mjs',
  '.github/scripts/verify-observation-planner-forecast-f4c-gate.mjs'
]) replaceRequired(path, oldF5, NEXT);
for (const path of [
  '.github/scripts/verify-observation-planner-forecast-f4d.mjs',
  '.github/scripts/verify-observation-planner-ranking-f5.mjs'
]) replaceRequired(path, 'BKL-031 F6 capability closure', NEXT);

const messageReplacements = [
  ['F5 is the next separately governed slice.', 'F5 is accepted; F6 real-evidence setup-aware E2E planner integration is next.'],
  ['F5 is the next separately governed slice', 'F5 is accepted; F6 real-evidence setup-aware E2E planner integration is next'],
  ['F4 accepted and F5 next.', 'F4/F5 accepted; F6 real-evidence setup-aware E2E next.'],
  ['F5 next.', 'F5 accepted; F6 real-evidence setup-aware E2E next.'],
  ['F5 accepted and F6 closure next.', 'F5 accepted; F6 real-evidence setup-aware E2E planner integration next; closure deferred.'],
  ['F6 closure next.', 'F6 real-evidence setup-aware E2E planner integration next; closure deferred.']
];
for (const path of [
  '.github/scripts/verify-observation-planner-ephemeris-lunar-f3b.mjs',
  '.github/scripts/verify-observation-planner-ephemeris-lunar-f3c.mjs',
  '.github/scripts/verify-observation-planner-forecast-f4a.mjs',
  '.github/scripts/verify-observation-planner-forecast-f4b.mjs',
  '.github/scripts/verify-observation-planner-forecast-f4c-gate.mjs',
  '.github/scripts/verify-observation-planner-forecast-f4d.mjs',
  '.github/scripts/verify-observation-planner-ranking-f5.mjs'
]) {
  let source = read(path);
  for (const [oldText, newText] of messageReplacements) source = source.replaceAll(oldText, newText);
  write(path, source);
}

console.log(`Reconciled BKL-031 F5 acceptance successor to ${NEXT}`);
