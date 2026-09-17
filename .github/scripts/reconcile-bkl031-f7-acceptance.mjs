import fs from 'node:fs';

const read = p => fs.readFileSync(p, 'utf8');
const write = (p, s) => fs.writeFileSync(p, s.endsWith('\n') ? s : `${s}\n`);
const replaceOnce = (text, from, to, label) => {
  if (!text.includes(from)) throw new Error(`Missing reconciliation marker: ${label}`);
  return text.replace(from, to);
};

const acceptancePath = 'docs/project/BKL-031-F7-FRESH-FORECAST-SUPPLY-ACCEPTANCE-2026-09-17.md';
const acceptance = `# BKL-031 F7 — Fresh Protected-Site Forecast Supply Acceptance

| Field | Value |
|---|---|
| Decision | **ACCEPTED — POST-MERGE VERIFIED** |
| Date | 2026-09-17 |
| Capability | BKL-031 F7 |
| Solution | \`BKL-031-F7-SOLUTION-001\` |
| Environment / authority | \`EVALUATION\` / \`NONE\` |
| Consumer mode | \`READ_ONLY\` |
| Reviewed head | \`000fc81558060b45e71b9f1a69122249b6a5fe8e\` |
| Pull request | [#277](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/277) |
| Merge commit | \`59a1d690406d733b6e61e64220f84cef9b6fb1a2\` |
| Exact-head workflows | 9/9 successful |
| Post-merge workflows | 10/10 successful |
| Protected-site provider request | workflow run \`35255829165\`, attempt 1, SUCCESS |
| F7 provider request budget | \`1/1_EXHAUSTED\` |
| Runtime effect | One-shot evaluation supply only; S10 remains \`UNAVAILABLE\` |
| Safety effect | None; local physical interlocks remain authoritative |

## Accepted decision

F7 is accepted as the first governed Observation Planner forecast supply that uses the approved protected observatory coordinates for a real provider request while keeping those coordinates outside the public portal projection. The exact site coordinates are resolved only inside the server-side provider adapter under the explicit owner authorization and outbound privacy decision; they are neither logged into the public contract nor persisted in the public projection.

The accepted provider lineage is Open-Meteo Single Runs with upstream authority ItaliaMeteo/ARPAE and exact model selector \`italia_meteo_arpae_icon_2i\`, run initialization \`2026-09-17T12:00Z\`. The provider response contained 72 hourly positions; 71 complete positions were accepted, one initialization instant was excluded because precipitation was null/non-finite, zero values were imputed, and 66 accepted instants were future-valued at retrieval. Freshness at retrieval was within the ADR-011 18-hour ceiling.

The public projection \`BKL031_F7_PROTECTED_SITE_SANITIZED_FORECAST_PROJECTION\` contains the real normalized weather values and generalized public site label but no latitude, longitude, elevation, returned-grid coordinates, raw request URL or raw provider body. The browser consumer recomputes run age and fails closed instead of presenting stale evidence as a current forecast.

## Verification

The exact reviewed head \`000fc81558060b45e71b9f1a69122249b6a5fe8e\` completed all 9 applicable pull-request workflows successfully. Architecture Review Board returned **APPROVED WITH CONDITIONS** with 0 Blocker, 0 Major and 0 Minor findings. Release Quality returned **CONDITIONALLY READY FOR MERGE** with 0 blockers and 0 waivers.

PR #277 was merged under expected-head control as \`59a1d690406d733b6e61e64220f84cef9b6fb1a2\`. All 10 applicable post-merge push workflows completed successfully on that exact merge SHA, including F7 governance, Developer Foundation, documentation/manual pipelines and portal deployment paths.

## Retained limitations

- the accepted F7 provider acquisition is a one-shot evaluation request; recurring forecast refresh is not activated;
- the F7 protected-site request budget is permanently \`1/1_EXHAUSTED\` and does not authorize replay or additional provider traffic;
- recurring provider traffic requires a separately governed operating authorization covering cadence, provider/license mode, failure handling and freshness monitoring;
- ranking geometry from the earlier F5/F6 chain is not yet current-night astronomical evidence;
- setup compatibility from F6 is historical acquisition evidence, not explicit OTA/camera/filter suitability;
- no readiness/go-no-go, scheduler, automatic target selection, device command or Safety Authority is introduced;
- BKL-032 remains the separate owner of readiness/go-no-go decision support;
- S10 production runtime remains \`UNAVAILABLE\`.

## Transition

BKL-031 remains **In Progress**. F7 acceptance promotes **BKL-031 F8 current astronomy and explicit setup suitability integration** as the next dependency-ordered scientific gate.

F8 must calculate current target astronomical windows/altitude/transit/lunar geometry from governed site/time inputs, implement explicit OTA/camera/filter/target suitability rather than historical compatibility alone, and integrate those results with the current weather supply in an explainable read-only planner ranking. A later closure gate must additionally prove the governed recurring forecast operating model so the page remains fresh night after night rather than relying on one-shot evidence.
`;
write(acceptancePath, acceptance);

const archPath = 'docs/architecture/scientific-assets/BKL-031-F7-Fresh-Forecast-Supply-and-Runtime-Boundary.md';
let arch = read(archPath);
arch = replaceOnce(
  arch,
  '| Status | **REVIEW CANDIDATE — PROTECTED-SITE FORECAST EVIDENCE ACQUIRED / SITE BUDGET 1/1 EXHAUSTED** |',
  '| Status | **ACCEPTED — POST-MERGE VERIFIED / SITE BUDGET 1/1 EXHAUSTED** |',
  'F7 architecture status'
);
if (!arch.includes('## 13. Acceptance reconciliation')) {
  arch += `\n## 13. Acceptance reconciliation\n\nF7 is **ACCEPTED — POST-MERGE VERIFIED**. Exact-head review used \`000fc81558060b45e71b9f1a69122249b6a5fe8e\` with 9/9 applicable PR workflows successful. PR #277 merged under expected-head control as \`59a1d690406d733b6e61e64220f84cef9b6fb1a2\`, followed by 10/10 successful applicable push workflows. ARB returned APPROVED WITH CONDITIONS with no blocker/major/minor finding; Release Quality returned CONDITIONALLY READY FOR MERGE with no blocker or waiver.\n\nThe formal acceptance record is \`${acceptancePath}\`. Acceptance preserves the one-shot/production distinction: the real protected-site forecast path is accepted, but recurring refresh remains separately governed and S10 remains unavailable. BKL-031 remains In Progress and F8 is promoted for current astronomy plus explicit setup suitability integration.\n`;
}
write(archPath, arch);

const verifierPath = '.github/scripts/verify-observation-planner-forecast-f7.mjs';
let verifier = read(verifierPath);
verifier = replaceOnce(verifier,
  "for(const marker of ['PROTECTED-SITE FORECAST EVIDENCE ACQUIRED','35255829165','71 complete positions','66 future accepted instants','does not close BKL-031'])",
  "for(const marker of ['ACCEPTED — POST-MERGE VERIFIED','35255829165','71 complete positions','66 future accepted instants','does not close BKL-031'])",
  'F7 accepted doc markers');
verifier = replaceOnce(verifier,
  "assert.equal(roadmap.nextMilestone,'BKL-031 F7 fresh forecast supply and runtime boundary');",
  "assert.equal(roadmap.nextMilestone,'BKL-031 F8 current astronomy and explicit setup suitability integration');\nconst acceptance=fs.readFileSync('docs/project/BKL-031-F7-FRESH-FORECAST-SUPPLY-ACCEPTANCE-2026-09-17.md','utf8');\nfor(const marker of ['ACCEPTED — POST-MERGE VERIFIED','000fc81558060b45e71b9f1a69122249b6a5fe8e','59a1d690406d733b6e61e64220f84cef9b6fb1a2','10/10 successful','1/1_EXHAUSTED']) assert.ok(acceptance.includes(marker),`F7 acceptance missing ${marker}`);",
  'F7 roadmap successor assertion');
write(verifierPath, verifier);

const roadmapPath = '.github/roadmap/roadmap-source.json';
const roadmap = JSON.parse(read(roadmapPath));
roadmap.updatedAt = '2026-09-17';
roadmap.projectStatus = 'BKL-031 F3-C and F4-A/F4-B/F4-C/F4-D/F5/F6/F7 accepted and post-merge verified; F7 PR #277 reviewed on 000fc81558060b45e71b9f1a69122249b6a5fe8e, merged as 59a1d690406d733b6e61e64220f84cef9b6fb1a2 and verified 10/10 post-merge; F7 proves real protected-site forecast acquisition and sanitized public delivery with site budget 1/1 exhausted, but recurring refresh is not activated; current astronomical geometry and explicit OTA/camera/filter suitability remain unresolved; no readiness/go-no-go, scheduling, automatic target selection, commands or Safety Authority; S10 production runtime unavailable';
roadmap.nextMilestone = 'BKL-031 F8 current astronomy and explicit setup suitability integration';
roadmap.target = 'Establish F8 current astronomical windows/altitude/transit/lunar geometry and explicit OTA/camera/filter/target suitability, then combine them with governed current weather supply in an explainable read-only planner ranking. F7 protected-site forecast evidence is accepted but remains one-shot; recurring provider refresh still requires separately governed operating authorization before BKL-031 closure. Preserve privacy, fail-closed freshness/missingness, BKL-032 readiness separation and local physical-interlock Safety Authority.';
const stream = roadmap.streams.find(s => s.id === 'observatory-intelligence');
if (!stream) throw new Error('observatory-intelligence stream missing');
const item = stream.items.find(i => i.id === 'BKL-031');
if (!item) throw new Error('BKL-031 roadmap item missing');
item.status = 'active';
item.note = 'F3/F4/F5/F6/F7 are Accepted/Post-Merge Verified. F7 PR #277 merged as 59a1d690406d733b6e61e64220f84cef9b6fb1a2 after 9/9 exact-head and 10/10 post-merge workflows, proving real protected-site forecast acquisition and sanitized read-only portal delivery without publishing coordinates. The one-shot site budget is 1/1 exhausted and recurring refresh is not activated. F8 current astronomy plus explicit OTA/camera/filter suitability is next; BKL-031 remains In Progress, S10 unavailable, and no readiness/go-no-go, scheduler, automatic target selection, commands or Safety Authority is authorized.';
if (!roadmap.milestones.some(m => m.id === 'M-BKL031-F7-ACCEPTANCE')) {
  roadmap.milestones.push({
    id: 'M-BKL031-F7-ACCEPTANCE',
    itemRef: 'BKL-031',
    title: 'BKL-031 F7 protected-site forecast acceptance',
    date: '2026-09-17',
    description: 'F7 accepted/post-merge verified via PR #277 and merge 59a1d690406d733b6e61e64220f84cef9b6fb1a2; real protected-site forecast delivered through sanitized read-only projection; one-shot budget 1/1 exhausted; recurring runtime not activated.'
  });
}
write(roadmapPath, `${JSON.stringify(roadmap, null, 2)}\n`);

const backlogPath = 'docs/project/BACKLOG.md';
let backlog = read(backlogPath);
backlog = replaceOnce(backlog, '| Versione | 5.33 |', '| Versione | 5.34 |', 'backlog version');
const backlogRow = '| BKL-031 | P1 | Observation Planner intelligente | In Progress | F3-C/F4-A/F4-B/F4-C/F4-D/F5/F6/F7 Accepted/Post-Merge Verified; F7 PR #277 merge `59a1d690406d733b6e61e64220f84cef9b6fb1a2`; protected-site F7 budget 1/1 exhausted; recurring refresh not activated; S10 unavailable | Execute F8 current astronomy and explicit OTA/camera/filter target suitability integration, combining those inputs with governed current weather in explainable read-only ranking. Preserve fail-closed freshness/privacy; recurring provider runtime requires separate operating authorization before closure | ADR-010; ADR-011; `BKL-031-F7-SOLUTION-001`; F7 acceptance; PR #277; merge `59a1d690…` |';
if (!/^\| BKL-031 \|.*$/m.test(backlog)) throw new Error('BKL-031 backlog row missing');
backlog = backlog.replace(/^\| BKL-031 \|.*$/m, backlogRow);
write(backlogPath, backlog);

const decisionPath = 'docs/project/DECISION_LOG.md';
let decisions = read(decisionPath);
decisions = replaceOnce(decisions, '| Versione | 2.9 |', '| Versione | 3.0 |', 'decision log version');
if (!decisions.includes('| DLG-051 |')) {
  const row = '| DLG-051 | 17/09/2026 | Accettare F7 come primo forecast reale site-specific del Planner, con coordinate protette usate solo server-side, budget one-shot 1/1 esaurito e proiezione pubblica sanitizzata; promuovere F8 senza chiudere BKL-031 | F7 soddisfa il requisito di evidence meteo reale riferita al sito senza trasformare il one-shot in runtime ricorrente né introdurre readiness/safety/action authority | BKL-031 F7/F8 | Accepted | PR #277; merge `59a1d690406d733b6e61e64220f84cef9b6fb1a2`; F7 acceptance |\n';
  const m = decisions.match(/\| DLG-050 \|[^\n]*\n/);
  if (!m) throw new Error('DLG-050 marker missing');
  decisions = decisions.replace(m[0], `${m[0]}${row}`);
}
write(decisionPath, decisions);

const indexPath = 'docs/project/index.md';
let index = read(indexPath);
if (!index.includes('BKL-031-F7-FRESH-FORECAST-SUPPLY-ACCEPTANCE-2026-09-17.md')) {
  const marker = '| [F6 Real-Evidence Setup-Aware E2E Acceptance](BKL-031-F6-REAL-EVIDENCE-SETUP-AWARE-E2E-ACCEPTANCE-2026-09-17.md) | 13/13 exact-head and 14/14 post-merge workflows; F7 fresh forecast supply/runtime boundary next; provider validation budget remains 2/2 exhausted |';
  const rows = `${marker}\n| [F7 Fresh Forecast Supply and Runtime Boundary](../architecture/scientific-assets/BKL-031-F7-Fresh-Forecast-Supply-and-Runtime-Boundary.md) | Accepted/Post-Merge Verified via PR #277 and merge \`59a1d690\`; real protected-site forecast delivered through sanitized public projection; one-shot budget 1/1 exhausted; recurring runtime not activated |\n| [F7 Fresh Protected-Site Forecast Supply Acceptance](BKL-031-F7-FRESH-FORECAST-SUPPLY-ACCEPTANCE-2026-09-17.md) | 9/9 exact-head and 10/10 post-merge workflows; F8 current astronomy and explicit setup suitability integration next; BKL-031 remains In Progress |`;
  index = replaceOnce(index, marker, rows, 'project index F6 row');
}
write(indexPath, index);

const mkdocsPath = 'mkdocs.yml';
let mkdocs = read(mkdocsPath);
if (!mkdocs.includes('BKL-031 F7 - Fresh Protected-Site Forecast Supply Acceptance')) {
  const marker = '          - BKL-031 F6 - Real-Evidence Setup-Aware E2E Acceptance: project/BKL-031-F6-REAL-EVIDENCE-SETUP-AWARE-E2E-ACCEPTANCE-2026-09-17.md';
  const insert = `${marker}\n          - BKL-031 F7 - Fresh Forecast Supply and Runtime Boundary: architecture/scientific-assets/BKL-031-F7-Fresh-Forecast-Supply-and-Runtime-Boundary.md\n          - BKL-031 F7 - Fresh Protected-Site Forecast Supply Acceptance: project/BKL-031-F7-FRESH-FORECAST-SUPPLY-ACCEPTANCE-2026-09-17.md`;
  mkdocs = replaceOnce(mkdocs, marker, insert, 'mkdocs F6 acceptance nav');
}
write(mkdocsPath, mkdocs);

console.log('BKL-031 F7 acceptance reconciled; F8 promoted; BKL-031 remains In Progress.');
