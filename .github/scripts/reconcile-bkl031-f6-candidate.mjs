import assert from 'node:assert/strict';
import fs from 'node:fs';

function insertAfter(path, anchor, addition, sentinel) {
  const original = fs.readFileSync(path, 'utf8');
  if (original.includes(sentinel)) return false;
  const occurrences = original.split(anchor).length - 1;
  assert.equal(occurrences, 1, `${path}: expected exactly one reconciliation anchor, found ${occurrences}`);
  const updated = original.replace(anchor, `${anchor}${addition}`);
  fs.writeFileSync(path, updated);
  return true;
}

const mkdocsAnchor = '          - BKL-031 F5 - Explainable Ranking Acceptance: project/BKL-031-F5-EXPLAINABLE-RANKING-ACCEPTANCE-2026-09-17.md\n';
const mkdocsAddition = '          - BKL-031 F6 - Real-Evidence Setup-Aware E2E Planner: architecture/scientific-assets/BKL-031-F6-Real-Evidence-Setup-Aware-E2E-Planner.md\n';
const indexAnchor = '| [F5 Explainable Ranking Acceptance](BKL-031-F5-EXPLAINABLE-RANKING-ACCEPTANCE-2026-09-17.md) | 6/6 exact-head and 7/7 post-merge workflows; provider budget remains 2/2 exhausted |\n';
const indexAddition = '| [F6 Real-Evidence Setup-Aware E2E Planner](../architecture/scientific-assets/BKL-031-F6-Real-Evidence-Setup-Aware-E2E-Planner.md) | Review Candidate; binds real F4-C forecast values to governed setup/session evidence in a sanitized read-only E2E proof; BKL-031 closure remains deferred |\n';

const changed = [
  insertAfter('mkdocs.yml', mkdocsAnchor, mkdocsAddition, 'BKL-031 F6 - Real-Evidence Setup-Aware E2E Planner:'),
  insertAfter('docs/project/index.md', indexAnchor, indexAddition, '[F6 Real-Evidence Setup-Aware E2E Planner]')
].some(Boolean);

console.log(changed ? 'BKL-031 F6 candidate navigation/index reconciled.' : 'BKL-031 F6 candidate navigation/index already reconciled.');
