import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const implPr = 279;
const reviewedHead = '3f05693482208df2b56b66dcb71162589880e72b';
const implMerge = '20669f7164460297d7318fc3b5874e4bc7f4bcde';
const nextMilestone = 'BKL-031 F9 repeatable current-night planner closure';
const nextTarget = 'Establish a repeatable current-night planner refresh/integration that combines governed fresh forecast supply, current astronomical geometry, explicit OTA/camera/filter suitability and explainable portal ranking. Preserve exact provider/model/run lineage, freshness/missingness, protected-site privacy, BKL-032 readiness separation and local physical-interlock Safety Authority. No recurring provider traffic, scheduler, automatic target selection, device command, readiness/go-no-go or Safety Authority is authorized by F8 acceptance.';

const read = p => fs.readFileSync(p, 'utf8');
const write = (p, c) => { fs.mkdirSync(path.dirname(p), { recursive: true }); fs.writeFileSync(p, c.endsWith('\n') ? c : c + '\n'); };
const replaceRequired = (p, from, to) => {
  const s = read(p);
  if (!s.includes(from)) throw new Error(`Required anchor not found in ${p}: ${from.slice(0,120)}`);
  write(p, s.replace(from, to));
};

// 1. Promote F8 architecture document only after implementation post-merge verification.
replaceRequired(
  'docs/architecture/scientific-assets/BKL-031-F8-Current-Astronomy-and-Setup-Suitability.md',
  '| Status | REVIEW CANDIDATE |',
  '| Status | **ACCEPTED — POST-MERGE VERIFIED** |'
);

// 2. Acceptance record.
write('docs/project/BKL-031-F8-CURRENT-ASTRONOMY-SETUP-SUITABILITY-ACCEPTANCE-2026-09-17.md', `# BKL-031 F8 — Current Astronomy and Setup Suitability Acceptance

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F8-ACCEPTANCE-001 |
| Stato | **ACCEPTED — POST-MERGE VERIFIED** |
| Data | 17/09/2026 |
| Capability | BKL-031 — Observation Planner intelligente |
| Incremento | F8 — Current Astronomy + Explicit Setup Suitability |
| Implementation PR | #${implPr} |
| Exact head reviewed | \`${reviewedHead}\` |
| Implementation merge | \`${implMerge}\` |
| Acceptance reconciliation PR | RECONCILIATION_PR_PENDING |
| Successore | **${nextMilestone}** |

## Evidence di acceptance

- exact-head PR workflow matrix: **9/9 SUCCESS** sul commit \`${reviewedHead}\`;
- ARB exact-head: **APPROVED WITH CONDITIONS**, 0 Blocker, 0 Major, 0 Minor, 2 Observations, nessun waiver;
- Release Quality exact-head: **CONDITIONALLY READY FOR MERGE**, nessun waiver;
- expected-head merge: \`${implMerge}\`;
- post-merge push workflow matrix: **10/10 SUCCESS**, incluso Developer Foundation;
- verifier F8 source-bound: meteo F7 verificato per istante, setup ottico verificato contro baseline approvata, FOV ricalcolato, coordinate target legate alla source scientifica registrata, suitability e advisory-window score ricalcolati;
- mutation tests fail-closed attivi su lineage F7, meteo, setup, suitability, projection, finestre advisory, privacy e authority boundaries.

## Risultato scientifico bounded

F8 accetta come evidence di integrazione la notte 17–18 settembre 2026. La projection combina forecast reale F7 site-specific, geometria astronomica night-specific e suitability esplicita OTA/camera/filter per i setup governati e i target bounded LDN 1320 / M 27. La projection pubblica non contiene coordinate protette.

Questa acceptance **non** equivale a runtime ricorrente o production readiness: F7 resta one-shot, F8 non effettua provider request e S10 resta \`UNAVAILABLE\`.

## Boundary preservati

- \`authority = NONE\`, consumer read-only/advisory;
- readinessAuthority=false;
- automaticTargetSelection=false;
- schedulingAuthority=false;
- actionAuthority=NONE;
- commandAuthority=NONE;
- Safety Authority = local physical interlocks;
- BKL-032 mantiene l'ownership di Session Readiness / Go-No-Go;
- nessun provider traffic ricorrente è autorizzato da questa acceptance.

## Transition

BKL-031 resta **In Progress**. F8 chiude il gap di astronomia corrente + suitability esplicita per una notte bounded, ma non dimostra ancora una supply ripetibile per la notte corrente. Il solo successore promosso è **${nextMilestone}**.

F9 deve dimostrare, in modo governato e ripetibile, il criterio finale: selezione setup → forecast della notte → target compatibili → classifica spiegabile → finestre migliori, mantenendo separati readiness/safety/action authority e ogni autorizzazione di traffico provider ricorrente.
`);

// 3. Compact owner-defined nine-field handover.
write('docs/project/HANDOVER_2026-09-17.md', `# Digital StarGate — Handover 17/09/2026

## 1. stato corrente
BKL-031 è **In Progress**. F3–F8 sono Accepted/Post-Merge Verified. F8 ha integrato forecast reale F7, astronomia night-specific e suitability esplicita OTA/camera/filter in ranking e finestre advisory read-only per la notte 17–18/09/2026. S10 resta \`UNAVAILABLE\`; BKL-032 conserva la readiness/go-no-go authority; gli interlock fisici locali restano Safety Authority. F9 è il solo gate successivo.

## 2. branch
Acceptance reconciliation: \`chore/bkl-031-f8-acceptance-reconciliation\`. Branch F8 implementativo: \`feat/bkl-031-f8-current-astronomy-setup-suitability\` (merged).

## 3. PR
Implementation PR #279 merged. Acceptance reconciliation PR: RECONCILIATION_PR_PENDING.

## 4. commit rilevanti
Reviewed F8 head \`${reviewedHead}\`; F8 merge \`${implMerge}\`. F7 merge \`59a1d690406d733b6e61e64220f84cef9b6fb1a2\`. Il merge SHA della reconciliation sarà registrato a chiusura del relativo PR.

## 5. decisioni ADR
ADR-010 è accepted repository method authority per ephemeris/lunar; ADR-011 è accepted repository source authority per forecast ItaliaMeteo/ARPAE ICON-2I via Open-Meteo Single Runs con run esplicito e no fallback/stitching. Nessun ADR attribuisce readiness, scheduling, command o Safety Authority al Planner.

## 6. file interessati
F8 architecture/projection/schema/verifier/test/browser consumer; acceptance F8; \`AI_BOOTSTRAP.md\`; questo handover; \`CURRENT_TECHNICAL_BASELINE_2026-09-17.md\`; \`ENTERPRISE_ARCHITECTURE_CONTEXT.md\`; \`BACKLOG.md\`; \`.github/roadmap/roadmap-source.json\`; generated roadmap/platform projections; \`DECISION_LOG.md\`; \`docs/project/index.md\`; \`mkdocs.yml\`; predecessor continuity verifiers.

## 7. comandi eseguiti
Repository operations tramite GitHub connector e GitHub Actions: F8 validator/test/browser syntax, exact-head 9/9, ARB/RQ exact-head, expected-head merge, post-merge 10/10. La reconciliation usa generatori governati \`node .github/scripts/generate-roadmap.mjs --write\` e \`node .github/scripts/generate-scientific-platform-status.mjs --write\`.

## 8. errori ancora aperti
Nessun errore F8 aperto. Limiti intenzionali: evidence F8 bounded a una notte e due target; F7 protected-site request budget \`1/1_EXHAUSTED\`; historical F4-C generalized budget \`2/2_EXHAUSTED\`; recurring provider traffic non autorizzato; S10 production runtime \`UNAVAILABLE\`.

## 9. prossimo passo
**${nextMilestone}**: dimostrare un ciclo repeatable/current-night che acquisisca o riceva forecast governato fresco, ricalcoli astronomia e suitability dai source approvati e pubblichi ranking/finestre read-only. Qualunque traffico provider ricorrente richiede una separata authority/budget decision; nessuna readiness/safety/action authority deve essere introdotta.
`);

// 4. Current technical baseline.
write('docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-17.md', `# Digital StarGate — Current Technical Baseline 17/09/2026

| Campo | Valore |
|---|---|
| Stato | Current governed baseline |
| Repository | \`maininimassimo-bit/digital-stargate-manual\` |
| Baseline implementation merge | \`${implMerge}\` |
| Current package | BKL-031 |
| Current next gate | ${nextMilestone} |

## Observation Planner baseline

F3–F8 sono Accepted/Post-Merge Verified. F8 accetta la pipeline scientifica bounded della notte 17–18/09/2026: forecast reale F7 site-specific, geometria astronomica corrente per la notte, suitability esplicita setup-target e ranking/finestre advisory nel portale. Il metodo resta \`EVALUATION/NONE/READ_ONLY\` e non è un readiness/safety engine.

## Authority baseline

- Site Authority: protected GitHub-governed record; coordinate esatte non pubblicabili.
- Setup Authority: approved GitHub-governed assignment/baseline.
- Ephemeris/lunar method: ADR-010 accepted repository authority.
- Forecast source/run lineage: ADR-011 accepted repository authority.
- Session Readiness / Go-No-Go: BKL-032, non BKL-031.
- Safety Authority: local physical interlocks.
- S10 production runtime: \`UNAVAILABLE\`.

## Provider/request baseline

- F4-C generalized validation budget: \`2/2_EXHAUSTED\`.
- F7 protected-site one-shot budget: \`1/1_EXHAUSTED\`.
- F8 provider requests: 0.
- Recurring provider traffic: **NOT AUTHORIZED** by F8 acceptance; requires separate authority/budget/service decision.

## F8 verified implementation

PR #279 exact reviewed head \`${reviewedHead}\`: 9/9 PR workflows SUCCESS; ARB APPROVED WITH CONDITIONS with no Blocker/Major and no waiver; Release Quality CONDITIONALLY READY with no waiver. Expected-head merge \`${implMerge}\`: 10/10 applicable push workflows SUCCESS.

## Open closure gap

BKL-031 is not closed. F9 must prove repeatable/current-night operation of the complete advisory chain — governed fresh forecast, current astronomy, explicit setup suitability, explainable target ordering and best windows — while preserving privacy, fail-closed freshness/missingness and all authority separations.
`);

// 5. Root bootstrap: replace stale long-form bootstrap with compact current authority.
write('AI_BOOTSTRAP.md', `# Digital StarGate AI Bootstrap

| Campo | Valore |
|---|---|
| Versione | 7.2 |
| Baseline | 17/09/2026 |
| Stato | Current root bootstrap — BKL-031 F8 Accepted/Post-Merge Verified; F9 repeatable current-night closure next; S10 unavailable |

Questo file è il punto di ingresso obbligatorio per ogni nuova sessione di lavoro sul repository \`maininimassimo-bit/digital-stargate-manual\`.

## 1. Regola fondamentale
Il repository GitHub è l'unica fonte autorevole. Memoria, conversazioni e projection non prevalgono sul repository corrente.

## 2. Sequenza obbligatoria di lettura
1. \`AI_BOOTSTRAP.md\`
2. \`docs/project/HANDOVER_2026-09-17.md\`
3. \`docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-17.md\`
4. \`docs/project/ENTERPRISE_ARCHITECTURE_CONTEXT.md\`
5. \`docs/project/REPOSITORY_KNOWLEDGE_MAP.md\`
6. \`docs/project/BACKLOG.md\`
7. \`.github/roadmap/roadmap-source.json\`
8. \`docs/data/roadmap.json\` — generated projection, non authority
9. \`docs/project/TECHNICAL_DEBT.md\`
10. \`docs/project/DECISION_LOG.md\`
11. \`docs/project/DEVELOPMENT_WORKFLOW.md\`
12. \`docs/project/DSG-AEM-001-CONTINUOUS-AUTONOMOUS-EXECUTION-MANDATE-2026-09-15.md\`
13. \`docs/project/CODING_STANDARDS.md\`
14. \`docs/project/RELEASE_PLAYBOOK.md\`
15. \`docs/architecture/assessments/AMP-002-Architecture-Program-Roadmap-Realignment.md\`
16. package, ADR, review, evidence e componenti direttamente coinvolti.

Gli handover e le baseline precedenti restano snapshot storici.

## 3. Stato corrente
- BKL-031: **In Progress**.
- F3–F8: Accepted/Post-Merge Verified.
- F8 implementation: PR #279, reviewed head \`${reviewedHead}\`, merge \`${implMerge}\`, 9/9 exact-head e 10/10 post-merge SUCCESS.
- F8 evidence: notte bounded 17–18/09/2026, forecast reale F7 site-specific, astronomia night-specific, suitability OTA/camera/filter esplicita, ranking/finestre advisory read-only.
- Next gate: **${nextMilestone}**.
- S10 production runtime: \`UNAVAILABLE\`.

## 4. Boundary non negoziabili
- local physical interlocks = Safety Authority;
- BKL-032 = Session Readiness / Go-No-Go authority;
- BKL-031 = advisory/read-only, nessuna readiness/safety/action authority;
- nessun scheduler, automatic target selection o device command;
- coordinate sito protette mai in projection pubbliche;
- missing/stale/conflicted evidence fail-closed;
- provider/model/run lineage esplicita, nessun fallback/stitching silenzioso;
- recurring provider traffic non autorizzato senza separata authority/budget decision.

## 5. Provider budget corrente
- F4-C generalized validation: \`2/2_EXHAUSTED\`;
- F7 protected-site one-shot: \`1/1_EXHAUSTED\`;
- F8: zero provider requests;
- F9 non eredita automaticamente alcuna autorizzazione di traffico ricorrente.

## 6. Disciplina di delivery
Exact-head CI → ARB → Release Quality sullo stesso SHA → expected-head merge → post-merge verification → acceptance reconciliation. Nessuna acceptance o runtime claim può precedere l'evidence reale.

## 7. Punto di ripresa
Riprendere da **${nextMilestone}** usando \`docs/project/HANDOVER_2026-09-17.md\` come handover compatto e \`docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-17.md\` come baseline tecnica corrente.
`);

// 6. Backlog: update only BKL-031 row plus version/baseline, preserve all history.
{
  const p = 'docs/project/BACKLOG.md';
  let s = read(p);
  s = s.replace('| Versione | 5.34 |', '| Versione | 5.35 |');
  s = s.replace('| Data baseline | 15/09/2026 |', '| Data baseline | 17/09/2026 |');
  const lines = s.split(/\r?\n/);
  const idx = lines.findIndex(l => l.startsWith('| BKL-031 |'));
  if (idx < 0) throw new Error('BKL-031 backlog row not found');
  lines[idx] = '| BKL-031 | P1 | Observation Planner intelligente | In Progress | BKL-035; BKL-040; BKL-037; F3–F8 Accepted/Post-Merge Verified; F8 PR #279 merge `20669f7164460297d7318fc3b5874e4bc7f4bcde`; F7 protected-site one-shot budget 1/1 exhausted; S10 unavailable | Execute F9 repeatable current-night planner closure: governed fresh forecast supply + current astronomy + explicit OTA/camera/filter suitability + explainable portal ranking/windows. Preserve privacy/freshness fail-closed, BKL-032 readiness separation and local physical-interlock Safety Authority. Recurring provider traffic requires separate authority/budget decision. | F8 acceptance 17/09/2026; PR #279; `BKL-031-F8-CURRENT-ASTRONOMY-SETUP-SUITABILITY-ACCEPTANCE-2026-09-17.md` |';
  write(p, lines.join('\n'));
}

// 7. Canonical roadmap structured update and F8 acceptance milestone.
{
  const p = '.github/roadmap/roadmap-source.json';
  const r = JSON.parse(read(p));
  r.updatedAt = '2026-09-17';
  r.projectStatus = 'BKL-031 F3-C and F4-A/B/C/D/F5/F6/F7/F8 accepted and post-merge verified; F8 PR #279 merge 20669f7164460297d7318fc3b5874e4bc7f4bcde proves bounded 17–18 Sep current astronomy plus explicit setup suitability over real F7 protected-site forecast. F4-C generalized budget 2/2 exhausted; F7 protected-site one-shot budget 1/1 exhausted; F8 performed zero provider requests; recurring refresh remains unauthorized; BKL-031 remains In Progress; no readiness/go-no-go, scheduling, automatic target selection, commands or Safety Authority; S10 production runtime unavailable.';
  r.nextMilestone = nextMilestone;
  r.target = nextTarget;
  for (const stream of r.streams ?? []) for (const item of stream.items ?? []) if (item.id === 'BKL-031') {
    item.status = 'active';
    item.note = 'F3/F4/F5/F6/F7/F8 are Accepted/Post-Merge Verified. F8 PR #279 merged as 20669f7164460297d7318fc3b5874e4bc7f4bcde after 9/9 exact-head and 10/10 post-merge workflows, binding real F7 protected-site forecast to night-specific astronomy and explicit OTA/camera/filter suitability in a sanitized read-only planner. F8 is bounded to the 17–18 Sep 2026 night and does not prove recurring runtime. F9 repeatable current-night planner closure is next; recurring provider traffic is not authorized, BKL-031 remains In Progress, S10 unavailable, and no readiness/go-no-go, scheduler, automatic target selection, commands or Safety Authority is authorized.';
  }
  r.milestones ??= [];
  if (!r.milestones.some(m => m.id === 'M-BKL031-F8-ACCEPTANCE')) r.milestones.push({
    id: 'M-BKL031-F8-ACCEPTANCE', itemRef: 'BKL-031', title: 'BKL-031 F8 current astronomy and setup suitability acceptance', date: '2026-09-17', status: 'active',
    description: `PR #279 passed 9/9 exact-head workflows on ${reviewedHead}, merged with expected-head control as ${implMerge}, and passed 10/10 applicable post-merge workflows. F8 is Accepted/Post-Merge Verified as bounded EVALUATION/NONE/READ_ONLY evidence for the 17–18 Sep 2026 night. F9 repeatable current-night planner closure is next; BKL-031 remains In Progress and recurring provider traffic is not authorized by F8 acceptance.`
  });
  write(p, JSON.stringify(r, null, 2));
}

// 8. Decision Log continuity without changing ADR semantics.
{
  const p = 'docs/project/DECISION_LOG.md';
  let s = read(p);
  s = s.replace('| Versione | 3.0 |', '| Versione | 3.1 |').replace('| Data baseline | 15/09/2026 |', '| Data baseline | 17/09/2026 |');
  if (!s.includes('| DLG-052 |')) {
    const row = '| DLG-052 | 17/09/2026 | Accettare F8 come bounded current-night astronomy + explicit setup-suitability integration proof, senza chiudere BKL-031, e promuovere esclusivamente F9 repeatable current-night planner closure | F8 dimostra il criterio scientifico su una notte reale ma non un ciclo ricorrente; mantenere separati provider operating authority, BKL-032 readiness e local Safety Authority | BKL-031 F8/F9 | Accepted / Post-Merge Verified | PR #279; exact head `3f05693482208df2b56b66dcb71162589880e72b`; merge `20669f7164460297d7318fc3b5874e4bc7f4bcde`; F8 acceptance |\n\n';
    const anchor = '## 5. Delega operativa GitHub';
    if (!s.includes(anchor)) throw new Error('Decision log section anchor not found');
    s = s.replace(anchor, row + anchor);
  }
  write(p, s);
}

// 9. Enterprise context current pointers.
{
  const p = 'docs/project/ENTERPRISE_ARCHITECTURE_CONTEXT.md';
  let s = read(p);
  s = s.replace('| Versione | 4.0 |', '| Versione | 4.1 |');
  s = s.replace('| Data baseline | 16/09/2026 |', '| Data baseline | 17/09/2026 |');
  s = s.replace('| Continuity handover | `docs/project/HANDOVER_2026-09-15.md` |', '| Continuity handover | `docs/project/HANDOVER_2026-09-17.md` |');
  s = s.replace('| Technical baseline | `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-15.md` |', '| Technical baseline | `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-17.md` |');
  s = s.replace(/^\| Current governed package \|.*$/m, '| Current governed package | BKL-031 F8 Accepted/Post-Merge Verified; F9 repeatable current-night planner closure next; S10 unavailable |');
  write(p, s);
}

// 10. Governance Center continuity pointers + F8 entries.
{
  const p = 'docs/project/index.md';
  let s = read(p);
  s = s.replace('| [Handover 15/09/2026](HANDOVER_2026-09-15.md) | Handover corrente |', '| [Handover 17/09/2026](HANDOVER_2026-09-17.md) | Handover corrente |');
  s = s.replace('| [Current Technical Baseline 15/09/2026](CURRENT_TECHNICAL_BASELINE_2026-09-15.md) | Baseline tecnica corrente |', '| [Current Technical Baseline 17/09/2026](CURRENT_TECHNICAL_BASELINE_2026-09-17.md) | Baseline tecnica corrente |');
  if (!s.includes('BKL-031-F8-CURRENT-ASTRONOMY-SETUP-SUITABILITY-ACCEPTANCE-2026-09-17.md')) {
    const marker = '| [F7 Fresh Protected-Site Forecast Supply Acceptance](BKL-031-F7-FRESH-FORECAST-SUPPLY-ACCEPTANCE-2026-09-17.md) | 9/9 exact-head and 10/10 post-merge workflows; F8 current astronomy and explicit setup suitability integration next; BKL-031 remains In Progress |';
    if (!s.includes(marker)) throw new Error('Project index F7 acceptance anchor not found');
    s = s.replace(marker, marker + '\n| [F8 Current Astronomy and Setup Suitability](../architecture/scientific-assets/BKL-031-F8-Current-Astronomy-and-Setup-Suitability.md) | Accepted/Post-Merge Verified via PR #279 and merge `20669f71`; real F7 weather + night-specific astronomy + explicit setup suitability; bounded one-night advisory evidence |\n| [F8 Current Astronomy and Setup Suitability Acceptance](BKL-031-F8-CURRENT-ASTRONOMY-SETUP-SUITABILITY-ACCEPTANCE-2026-09-17.md) | 9/9 exact-head and 10/10 post-merge workflows; F9 repeatable current-night planner closure next; BKL-031 remains In Progress |');
  }
  write(p, s);
}

// 11. MkDocs current continuity pointers and F8 acceptance navigation.
{
  const p = 'mkdocs.yml';
  let s = read(p);
  s = s.replace('- Current Handover 15/09/2026: project/HANDOVER_2026-09-15.md', '- Current Handover 17/09/2026: project/HANDOVER_2026-09-17.md');
  s = s.replace('- Current Technical Baseline 15/09/2026: project/CURRENT_TECHNICAL_BASELINE_2026-09-15.md', '- Current Technical Baseline 17/09/2026: project/CURRENT_TECHNICAL_BASELINE_2026-09-17.md');
  if (!s.includes('BKL-031 F8 Acceptance: project/BKL-031-F8-CURRENT-ASTRONOMY-SETUP-SUITABILITY-ACCEPTANCE-2026-09-17.md')) {
    const anchor = '- BKL-031 F7 Fresh Forecast Supply Acceptance: project/BKL-031-F7-FRESH-FORECAST-SUPPLY-ACCEPTANCE-2026-09-17.md';
    if (!s.includes(anchor)) throw new Error('MkDocs F7 acceptance anchor not found');
    s = s.replace(anchor, anchor + '\n      - BKL-031 F8 Acceptance: project/BKL-031-F8-CURRENT-ASTRONOMY-SETUP-SUITABILITY-ACCEPTANCE-2026-09-17.md');
  }
  write(p, s);
}

// 12. Predecessor continuity validators must recognize the promoted milestone, without changing historical docs.
for (const name of fs.readdirSync('.github/scripts')) {
  if (!name.endsWith('.mjs') || name === 'reconcile-bkl-031-f8-acceptance.mjs') continue;
  const p = path.join('.github/scripts', name);
  const s = read(p);
  const old = 'BKL-031 F8 current astronomy and explicit setup suitability integration';
  if (s.includes(old)) write(p, s.split(old).join(nextMilestone));
}

// 13. Regenerate governed projections from canonical source.
for (const [cmd, args] of [
  ['node', ['.github/scripts/generate-roadmap.mjs', '--write']],
  ['node', ['.github/scripts/generate-scientific-platform-status.mjs', '--write']]
]) {
  const r = spawnSync(cmd, args, { stdio: 'inherit' });
  if (r.status !== 0) throw new Error(`${cmd} ${args.join(' ')} failed with ${r.status}`);
}

console.log('BKL-031 F8 acceptance reconciliation materialized; F9 promoted; projections regenerated.');
