import assert from 'node:assert/strict';
import fs from 'node:fs';
import { canonicalJson } from './observation-planner-ephemeris-lunar-f3b-contract.mjs';
import { buildF3CProjection, validateF3CProjection } from './observation-planner-ephemeris-lunar-f3c-adapter.mjs';

const paths = {
  fixture: 'docs/data/observation-planner-ephemeris-lunar-f3b-fixture.json',
  schema: 'schemas/observation-planner-ephemeris-lunar-projection-f3c.schema.json',
  projection: 'docs/data/observation-planner-ephemeris-lunar-f3c-projection.json',
  architecture: 'docs/architecture/scientific-assets/BKL-031-F3-C-Bounded-Adapter-Sanitized-Projection-and-Portal.md',
  acceptance: 'docs/project/BKL-031-F3-C-BOUNDED-INTEGRATION-ACCEPTANCE-2026-09-17.md',
  f8Acceptance: 'docs/project/BKL-031-F8-CURRENT-ASTRONOMY-SETUP-SUITABILITY-ACCEPTANCE-2026-09-17.md',
  handover: 'docs/project/HANDOVER_2026-09-17.md',
  baseline: 'docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-17.md',
  bootstrap: 'AI_BOOTSTRAP.md',
  page: 'docs/observation-planner/index.md',
  browser: 'docs/javascripts/observation-planner.js',
  browserCore: 'docs/javascripts/observation-planner-core.mjs',
  style: 'docs/styles/observation-planner.css',
  workflow: '.github/workflows/bkl-031-f3-c-governance.yml',
  developer: '.github/workflows/developer-foundation.yml',
  backlog: 'docs/project/BACKLOG.md',
  knowledge: 'docs/project/REPOSITORY_KNOWLEDGE_MAP.md',
  index: 'docs/project/index.md',
  nav: 'mkdocs.yml',
  roadmap: '.github/roadmap/roadmap-source.json'
};

for (const path of Object.values(paths)) assert.ok(fs.existsSync(path), `missing F3-C artifact: ${path}`);
const fixture = JSON.parse(fs.readFileSync(paths.fixture, 'utf8'));
const schema = JSON.parse(fs.readFileSync(paths.schema, 'utf8'));
const projection = JSON.parse(fs.readFileSync(paths.projection, 'utf8'));
const expected = buildF3CProjection(structuredClone(fixture));

assert.equal(validateF3CProjection(projection, fixture), true);
assert.equal(canonicalJson(projection), canonicalJson(expected), 'persisted projection differs from deterministic adapter output.');
assert.equal(schema.$schema, 'https://json-schema.org/draft/2020-12/schema');
assert.equal(schema.additionalProperties, false);
for (const field of ['projectionId', 'method', 'facts', 'boundary', 'projectionDigest']) assert.ok(schema.required.includes(field), `F3-C schema does not require ${field}.`);
assert.equal(schema.properties.environment.const, 'TEST');
assert.equal(schema.properties.authority.const, 'NONE');
assert.equal(schema.properties.boundary.properties.runtimeState.const, 'UNAVAILABLE');

const architecture = fs.readFileSync(paths.architecture, 'utf8');
const acceptance = fs.readFileSync(paths.acceptance, 'utf8');
const f8Acceptance = fs.readFileSync(paths.f8Acceptance, 'utf8');
const handover = fs.readFileSync(paths.handover, 'utf8');
const baseline = fs.readFileSync(paths.baseline, 'utf8');
const bootstrap = fs.readFileSync(paths.bootstrap, 'utf8');
const page = fs.readFileSync(paths.page, 'utf8');
const browser = fs.readFileSync(paths.browser, 'utf8');
const browserCore = fs.readFileSync(paths.browserCore, 'utf8');
const workflow = fs.readFileSync(paths.workflow, 'utf8');
const developer = fs.readFileSync(paths.developer, 'utf8');
const backlog = fs.readFileSync(paths.backlog, 'utf8');
const knowledge = fs.readFileSync(paths.knowledge, 'utf8');
const index = fs.readFileSync(paths.index, 'utf8');
const nav = fs.readFileSync(paths.nav, 'utf8');
const roadmap = JSON.parse(fs.readFileSync(paths.roadmap, 'utf8'));

for (const fragment of ['**ACCEPTED — POST-MERGE VERIFIED**', '35-case adapter/projection/browser suite', 'Pull request #261', 'all 12 applicable post-merge workflows', 'S10 remains `UNAVAILABLE`', 'Production runtime activation remains separately authorized']) assert.ok(architecture.includes(fragment), `F3-C architecture record missing: ${fragment}`);
for (const fragment of ['**ACCEPTED — POST-MERGE VERIFIED**', '35/35 passing locally and in governed CI', 'fba1287efea0d1f36b147bc42a4fec5498990756', 'https://maininimassimo-bit.github.io/digital-stargate-manual/observation-planner/', '35194573308', 'S10 remains `UNAVAILABLE`']) assert.ok(acceptance.includes(fragment), `F3-C acceptance record missing: ${fragment}`);
for (const fragment of ['data-observation-planner', 'F4-B accettata', 'fixture astronomica sintetica F3-C']) assert.ok(page.includes(fragment), `Observation Planner page missing: ${fragment}`);
for (const fragment of ['validateObservationPlannerProjection', "fetch('../data/observation-planner-ephemeris-lunar-f3c-projection.json'", 'S10 runtime resta']) assert.ok(browser.includes(fragment), `Observation Planner browser consumer missing: ${fragment}`);
for (const fragment of ['crypto.subtle.digest', 'TEST/NONE', 'projectionDigest']) assert.ok(browserCore.includes(fragment), `Observation Planner browser validator missing: ${fragment}`);
assert.ok(workflow.includes('F3-C bounded adapter, projection and portal') && workflow.includes('test-observation-planner-ephemeris-lunar-f3c.mjs'), 'F3-C workflow is incomplete.');
assert.ok(developer.includes('Verify Observation Planner F3-C bounded integration') && developer.includes('Test Observation Planner F3-C adapter and portal boundaries'), 'Developer Foundation does not execute F3-C gates.');
assert.ok(backlog.includes('F3-C Accepted/Post-Merge Verified') && backlog.includes('F4-D metadata-only projection and portal Accepted/Post-Merge Verified'), 'Backlog does not preserve the accepted F3-C through F4-D gates.');
assert.ok(knowledge.includes('F3-C are Accepted / Post-Merge Verified') && index.includes('F3-C Bounded Adapter, Projection and Portal'), 'Continuity documents do not identify accepted F3-C.');
for (const fragment of [
  'HANDOVER_2026-09-21-AP-007.md',
  'CURRENT_TECHNICAL_BASELINE_2026-09-21.md',
  'F8 is Accepted / Post-Merge Verified',
  'BKL-032 Session Readiness / Go-No-Go Decision Support',
  '2/2_EXHAUSTED',
  '1/1_EXHAUSTED',
  'Recurring provider traffic is not authorized',
  'local physical interlocks remain Safety Authority'
]) assert.ok(knowledge.includes(fragment), `Repository Knowledge Map continuity drift: missing ${fragment}`);
assert.equal(knowledge.includes('current handover e technical baseline 15/09/2026'), false, 'Repository Knowledge Map must not retain the superseded 15/09 continuity pointer.');
for (const [name, text] of [['F8 acceptance', f8Acceptance], ['handover', handover], ['technical baseline', baseline], ['bootstrap', bootstrap]]) {
  for (const fragment of ['84d1b889a6c739c9e5d053e1f073fe1d87b8c5d4', '19/19']) assert.ok(text.includes(fragment), `${name} missing F8 reconciliation post-merge evidence: ${fragment}`);
}
for (const fragment of ['#280', 'bca410dcde804483052beded16c29a9f58f43872', 'GitHub Pages']) assert.ok(f8Acceptance.includes(fragment), `F8 acceptance missing reconciliation evidence: ${fragment}`);
assert.ok(handover.includes('BKL-032') && baseline.includes('BKL-032 Session Readiness / Go-No-Go Decision Support') && bootstrap.includes('BKL-032 Session Readiness / Go-No-Go Decision Support'), 'BKL-031 closure must hand off to BKL-032.');
assert.ok(nav.includes('Observation Planner: observation-planner/index.md') && nav.includes('BKL-031 F3-C - Bounded Adapter, Projection and Portal'), 'MkDocs navigation does not expose F3-C.');
assert.ok(['BKL-036', 'BKL-036-F5', 'AP-007', 'AP-008', 'AP-015', 'BKL-033', 'BKL-034', 'BKL-034-F2', 'BKL-042'].includes(roadmap.currentPackage));
assert.ok(['BKL-036 Observatory Health Score', 'BKL-036-F5 Live Read-Only Health Score', 'AP-007 Enterprise Operations and Service Management Architecture', 'AP-008 Enterprise Integration Architecture', 'AP-015', 'BKL-033', 'BKL-034', 'BKL-034-F2', 'BKL-042'].includes(roadmap.nextMilestone));
assert.ok(roadmap.projectStatus.includes('BKL-031 and BKL-032 are CLOSED / ACCEPTED / POST-MERGE VERIFIED') && roadmap.projectStatus.includes('S10 production runtime unavailable') && roadmap.projectStatus.includes('no scheduling, automatic target selection, commands or Safety Authority is authorized'), 'Roadmap F3-C-to-F4-D status/boundary mismatch.');
assert.ok(roadmap.milestones.some(item => item.id === 'M-BKL031-F3-C-IMPLEMENTATION'), 'Roadmap F3-C implementation milestone missing.');
assert.ok(roadmap.milestones.some(item => item.id === 'M-BKL031-F3-C-ACCEPTANCE'), 'Roadmap F3-C acceptance milestone missing.');
assert.ok(roadmap.milestones.some(item => item.id === 'M-BKL031-F4-D-ACCEPTANCE'), 'Roadmap F4-D acceptance milestone missing.');

console.log(`BKL-031 F3-C verified: ${projection.facts.length} sanitized facts, adapter ${projection.method.adapterId}@${projection.method.adapterVersion}, digest ${projection.projectionDigest}; S10 ${projection.boundary.runtimeState}; F3-C through F8 accepted; F8 reconciliation post-merge evidence retained; F9 repeatable current-night planner closure next.`);
