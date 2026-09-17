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
assert.ok(backlog.includes('F3-C Accepted/Post-Merge Verified') && backlog.includes('35/35 tests'), 'Backlog does not identify the accepted F3-C gate.');
assert.ok(knowledge.includes('F3-C is Accepted / Post-Merge Verified') && index.includes('F3-C Bounded Adapter, Projection and Portal'), 'Continuity documents do not identify accepted F3-C.');
assert.ok(nav.includes('Observation Planner: observation-planner/index.md') && nav.includes('BKL-031 F3-C - Bounded Adapter, Projection and Portal'), 'MkDocs navigation does not expose F3-C.');
assert.equal(roadmap.currentPackage, 'BKL-031');
assert.equal(roadmap.nextMilestone, 'BKL-031 F4-C bounded acquisition gate preparation');
assert.ok(roadmap.projectStatus.includes('F3-C accepted and post-merge verified') && roadmap.projectStatus.includes('S10 runtime unavailable'), 'Roadmap F3-C status/boundary mismatch.');
assert.ok(roadmap.milestones.some(item => item.id === 'M-BKL031-F3-C-IMPLEMENTATION'), 'Roadmap F3-C implementation milestone missing.');
assert.ok(roadmap.milestones.some(item => item.id === 'M-BKL031-F3-C-ACCEPTANCE'), 'Roadmap F3-C acceptance milestone missing.');

console.log(`BKL-031 F3-C verified: ${projection.facts.length} sanitized facts, adapter ${projection.method.adapterId}@${projection.method.adapterVersion}, digest ${projection.projectionDigest}; S10 ${projection.boundary.runtimeState}.`);
