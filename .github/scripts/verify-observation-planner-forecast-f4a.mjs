import assert from 'node:assert/strict';
import fs from 'node:fs';

const paths = {
  contract: 'docs/architecture/scientific-assets/BKL-031-F4-A-Forecast-Source-Discovery-and-Integration-Contract.md',
  adr: 'docs/architecture/ADR-011-Forecast-Source-and-Run-Lineage.md',
  validation: 'docs/architecture/validation/BKL-031-F4-A-Forecast-Source-Validation-Plan.md',
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
const backlog = read('backlog');
const knowledge = read('knowledge');
const index = read('index');
const decisions = read('decisions');
const nav = read('nav');
const roadmap = JSON.parse(read('roadmap'));

for (const fragment of [
  '**REVIEW CANDIDATE — NO PROVIDER TRAFFIC AUTHORIZED**',
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

for (const variable of ['temperature_2m', 'relative_humidity_2m', 'dew_point_2m', 'precipitation', 'cloud_cover', 'cloud_cover_low', 'cloud_cover_mid', 'cloud_cover_high', 'visibility', 'wind_speed_10m', 'wind_gusts_10m']) {
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

assert.ok(adr.includes('**PROPOSED — F4-A REVIEW CANDIDATE**') && adr.includes('automatic model fallback are prohibited'), 'ADR-011 decision boundary mismatch.');
for (let id = 1; id <= 24; id += 1) assert.ok(validation.includes(`| N${String(id).padStart(2, '0')} |`), `F4-A validation case N${String(id).padStart(2, '0')} missing.`);
assert.ok(validation.includes('**REVIEW CANDIDATE — NOT EXECUTED AGAINST A PROVIDER**'), 'F4-A validation execution boundary missing.');
assert.ok(backlog.includes('F4-A source discovery') && backlog.includes('zero-traffic review candidate'), 'Backlog does not identify the F4-A candidate.');
assert.ok(knowledge.includes('F4-A now records a zero-traffic review candidate'), 'Knowledge map does not identify F4-A.');
assert.ok(index.includes('F4-A Forecast Source Discovery and Integration Contract'), 'Project index does not expose F4-A.');
assert.ok(decisions.includes('DLG-042') && decisions.includes('fallback silenzioso'), 'Decision log does not record F4-A source decision.');
assert.ok(nav.includes('BKL-031 F4-A - Forecast Source Discovery and Integration Contract') && nav.includes('ADR-011 - Forecast Source and Run Lineage'), 'MkDocs navigation does not expose F4-A.');

assert.equal(roadmap.currentPackage, 'BKL-031');
assert.equal(roadmap.nextMilestone, 'BKL-031 F4-A exact-head forecast source-contract acceptance');
assert.ok(roadmap.projectStatus.includes('F4-A forecast source discovery') && roadmap.projectStatus.includes('zero provider traffic') && roadmap.projectStatus.includes('S10 runtime unavailable'), 'Roadmap F4-A status/boundary mismatch.');
assert.ok(roadmap.milestones.some((item) => item.id === 'M-BKL031-F4-A-SOURCE-CONTRACT'), 'Roadmap F4-A milestone missing.');

console.log('BKL-031 F4-A verified: ICON-2I explicit single-run contract, 11 variables, 24 fail-closed cases, zero provider traffic; S10 unavailable.');
