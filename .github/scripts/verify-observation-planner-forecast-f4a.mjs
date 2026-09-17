import assert from 'node:assert/strict';
import fs from 'node:fs';

const paths = {
  contract: 'docs/architecture/scientific-assets/BKL-031-F4-A-Forecast-Source-Discovery-and-Integration-Contract.md',
  adr: 'docs/architecture/ADR-011-Forecast-Source-and-Run-Lineage.md',
  validation: 'docs/architecture/validation/BKL-031-F4-A-Forecast-Source-Validation-Plan.md',
  acceptance: 'docs/project/BKL-031-F4-A-FORECAST-SOURCE-CONTRACT-ACCEPTANCE-2026-09-17.md',
  backlog: 'docs/project/BACKLOG.md',
  knowledge: 'docs/project/REPOSITORY_KNOWLEDGE_MAP.md',
  index: 'docs/project/index.md',
  decisions: 'docs/project/DECISION_LOG.md',
  nav: 'mkdocs.yml',
  roadmap: '.github/roadmap/roadmap-source.json'
};

for (const path of Object.values(paths)) assert.ok(fs.existsSync(path), `missing F4-A artifact: ${path}`);

const read = (name) => fs.readFileSync(paths[name], 'utf8');
const contract = read('contract');
const adr = read('adr');
const validation = read('validation');
const acceptance = read('acceptance');
const backlog = read('backlog');
const knowledge = read('knowledge');
const index = read('index');
const decisions = read('decisions');
const nav = read('nav');
const roadmap = JSON.parse(read('roadmap'));

for (const fragment of [
  '**ACCEPTED — POST-MERGE VERIFIED / NO PROVIDER TRAFFIC AUTHORIZED**',
  'providerId=OPEN_METEO',
  'upstreamAuthorityId=ITALIAMETEO_ARPAE',
  'modelId=italia_meteo_arpae_icon_2i',
  '`best_match`, seamless products, stitched time series and silent fallback are prohibited',
  'maximum run age',
  '18 hours',
  'maximum 72 hourly instants',
  'zero provider calls',
  'S10'
]) assert.ok(contract.includes(fragment), `F4-A contract missing: ${fragment}`);

for (const variable of ['temperature_2m', 'relative_humidity_2m', 'dew_point_2m', 'precipitation', 'cloud_cover', 'cloud_cover_low', 'cloud_cover_mid', 'cloud_cover_high', 'wind_speed_10m', 'wind_gusts_10m']) {
  assert.ok(contract.includes(`\`${variable}\``), `F4-A variable vocabulary missing ${variable}.`);
}

for (const url of [
  'https://www.arpae.it/it/temi-ambientali/meteo/previsioni-meteo/previsioni-meteo-modellistiche',
  'https://open-meteo.com/en/docs/italia-meteo-arpae-api',
  'https://open-meteo.com/en/docs/single-runs-api',
  'https://open-meteo.com/en/docs/model-updates',
  'https://open-meteo.com/en/terms',
  'https://open-meteo.com/en/pricing',
  'https://www.ecmwf.int/en/forecasts/datasets/open-data'
]) assert.ok(contract.includes(url), `F4-A official-source citation missing: ${url}`);

assert.ok(adr.includes('**ACCEPTED — REPOSITORY SOURCE AUTHORITY / PROVIDER TRAFFIC NOT AUTHORIZED**') && adr.includes('automatic model fallback are prohibited'), 'ADR-011 decision boundary mismatch.');
for (let id = 1; id <= 24; id += 1) assert.ok(validation.includes(`| N${String(id).padStart(2, '0')} |`), `F4-A validation case N${String(id).padStart(2, '0')} missing.`);
assert.ok(validation.includes('**ACCEPTED REPOSITORY VALIDATION PLAN — NOT EXECUTED AGAINST A PROVIDER**'), 'F4-A validation execution boundary missing.');
assert.ok(acceptance.includes('**ACCEPTED — POST-MERGE VERIFIED**') && acceptance.includes('16/16 successful') && acceptance.includes('13/13 successful') && acceptance.includes('02a829f21bf76a0dc5d9ef29998ca5690d71395c'), 'F4-A acceptance evidence mismatch.');
assert.ok(backlog.includes('F4-A/ADR-011') && backlog.includes('F4-D metadata-only projection and portal Accepted/Post-Merge Verified') && backlog.includes('provider budget 2/2 exhausted'), 'Backlog does not preserve accepted F4-A through F4-D state.');
assert.ok(knowledge.includes('F4-A and ADR-011 are Accepted / Post-Merge Verified'), 'Knowledge map does not identify accepted F4-A state.');
assert.ok(index.includes('F4-A Forecast Source Discovery and Integration Contract'), 'Project index does not expose F4-A.');
assert.ok(decisions.includes('DLG-042') && decisions.includes('fallback silenzioso') && decisions.includes('DLG-048'), 'Decision log does not preserve F4-A source decision through F4-D acceptance.');
assert.ok(nav.includes('BKL-031 F4-A - Forecast Source Discovery and Integration Contract') && nav.includes('ADR-011 - Forecast Source and Run Lineage'), 'MkDocs navigation does not expose F4-A.');

assert.equal(roadmap.currentPackage, 'BKL-031');
assert.equal(roadmap.nextMilestone, 'BKL-031 F9 repeatable current-night planner closure');
assert.ok(roadmap.projectStatus.includes('F4-A/ADR-011') && roadmap.projectStatus.includes('F4-D sanitized forecast projection/portal') && roadmap.projectStatus.includes('S10 production runtime unavailable'), 'Roadmap F4-A-to-F4-D status/boundary mismatch.');
assert.ok(roadmap.milestones.some((item) => item.id === 'M-BKL031-F4-A-SOURCE-CONTRACT'), 'Roadmap F4-A milestone missing.');
assert.ok(roadmap.milestones.some((item) => item.id === 'M-BKL031-F4-A-ACCEPTANCE'), 'Roadmap F4-A acceptance milestone missing.');
assert.ok(roadmap.milestones.some((item) => item.id === 'M-BKL031-F4-D-ACCEPTANCE'), 'Roadmap F4-D acceptance milestone missing.');

console.log('BKL-031 F4-A accepted and post-merge verified: ADR-011 source authority, 10 supported variables, visibility unavailable, 24 fail-closed cases; F4-B/F4-C/F4-D accepted; F5 is next; S10 unavailable.');
