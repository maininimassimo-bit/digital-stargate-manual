import fs from 'node:fs';

function write(path, text) { fs.writeFileSync(path, text.endsWith('\n') ? text : `${text}\n`); }
function insertAfterLine(text, needle, linesToInsert) {
  if (linesToInsert.every((line) => text.includes(line))) return text;
  const lines = text.split('\n');
  const index = lines.findIndex((line) => line.includes(needle));
  if (index < 0) throw new Error(`Anchor not found: ${needle}`);
  lines.splice(index + 1, 0, ...linesToInsert);
  return lines.join('\n');
}

// Permanent Developer Foundation regression.
const devPath = '.github/workflows/developer-foundation.yml';
let dev = fs.readFileSync(devPath, 'utf8');
const triggerMarker = '"docs/data/observation-planner-e2e-f6-projection.json",';
if (!dev.includes('"governance/forecast-evidence/BKL031-F7-**"')) {
  const occurrences = dev.split(triggerMarker).length - 1;
  if (occurrences !== 2) throw new Error(`Expected two Developer Foundation trigger anchors, found ${occurrences}.`);
  dev = dev.replaceAll(triggerMarker, `${triggerMarker}"governance/forecast-evidence/BKL031-F7-**",`);
}
const f7Steps = [
  '      - { name: Verify Observation Planner F7 fresh forecast supply, run: node .github/scripts/verify-observation-planner-forecast-f7.mjs }',
  '      - { name: Test Observation Planner F7 fail-closed fresh forecast evidence, run: node --test .github/scripts/test-observation-planner-forecast-f7.mjs }'
];
dev = insertAfterLine(dev, 'Check Observation Planner F6 browser consumer syntax', f7Steps);
write(devPath, dev);

// Decision Log owner authorization / execution record.
const decisionPath = 'docs/project/DECISION_LOG.md';
let decisions = fs.readFileSync(decisionPath, 'utf8');
if (decisions.includes('| Versione | 2.9 |')) decisions = decisions.replace('| Versione | 2.9 |', '| Versione | 3.0 |');
const dlg051 = '| DLG-051 | 17/09/2026 | Autorizzare esattamente una nuova richiesta provider di validazione F7, separata dal budget F4-C esaurito, sul punto `SYNTHETIC_GENERALIZED 42.0,12.0` e sul run ICON-2I `2026-09-17T12:00Z`; consumare il budget a `1/1_EXHAUSTED` dopo qualsiasi tentativo e rimuovere il dispatch path dopo l’acquisizione | Provare una supply forecast fresca preservando ADR-011, privacy del sito protetto, no retry/recurring traffic, no production runtime e nessuna readiness/command/Safety Authority | BKL-031 F7 | Executed / Evidence acquired / 1/1 exhausted | `BKL031-F7-PROVIDER-REQUEST-AUTH-001`; run `35243920092`; artifact `10506402579`; raw `7c6805d7…`; normalized `7d8205a4…` |';
if (!decisions.includes('| DLG-051 |')) decisions = insertAfterLine(decisions, '| DLG-050 |', [dlg051]);
write(decisionPath, decisions);

// Project Governance Center candidate links.
const projectPath = 'docs/project/index.md';
let project = fs.readFileSync(projectPath, 'utf8');
const projectRows = [
  '| [F7 Fresh Forecast Supply and Runtime Boundary](../architecture/scientific-assets/BKL-031-F7-Fresh-Forecast-Supply-and-Runtime-Boundary.md) | Review Candidate; one owner-authorized request consumed in run `35243920092`; fresh ICON-2I supply, generalized location only; budget `1/1_EXHAUSTED` |',
  '| [F7 Fresh Forecast Supply Validation Evidence](../architecture/validation/BKL-031-F7-Fresh-Forecast-Supply-Evidence-2026-09-17.md) | Run `35243920092`; artifact `10506402579`; 72 raw / 71 accepted / 1 excluded / 67 future; zero imputation; `FRESH` + `DEGRADED` |'
];
project = insertAfterLine(project, '[F6 Real-Evidence Setup-Aware E2E Acceptance]', projectRows);
write(projectPath, project);

// MkDocs navigation.
const mkdocsPath = 'mkdocs.yml';
let mkdocs = fs.readFileSync(mkdocsPath, 'utf8');
const navLines = [
  '          - BKL-031 F7 - Fresh Forecast Supply and Runtime Boundary: architecture/scientific-assets/BKL-031-F7-Fresh-Forecast-Supply-and-Runtime-Boundary.md',
  '          - BKL-031 F7 - Fresh Forecast Supply Validation Evidence: architecture/validation/BKL-031-F7-Fresh-Forecast-Supply-Evidence-2026-09-17.md'
];
mkdocs = insertAfterLine(mkdocs, 'BKL-031 F6 - Real-Evidence Setup-Aware E2E Acceptance:', navLines);
write(mkdocsPath, mkdocs);

console.log('BKL-031 F7 candidate governance reconciliation applied.');
