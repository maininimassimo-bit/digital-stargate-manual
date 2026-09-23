import { access, readFile } from 'node:fs/promises';
import path from 'node:path';

const fixturePath = 'docs/data/bkl034-scientific-image-gallery-fixture.json';
const schemaPath = 'schemas/bkl034-scientific-image-gallery.schema.json';
const contractPath = 'docs/architecture/packages/BKL-034-Scientific-Image-Gallery.md';
const pagePath = 'docs/scientific-image-gallery/index.md';
const scriptPath = 'docs/javascripts/bkl-034-image-gallery.js';
const stylePath = 'docs/styles/bkl-034-image-gallery.css';
const fail = (message) => { throw new Error(message); };
const assert = (condition, message) => { if (!condition) fail(message); };
const fixture = JSON.parse(await readFile(fixturePath, 'utf8'));
const schema = JSON.parse(await readFile(schemaPath, 'utf8'));
const contract = await readFile(contractPath, 'utf8');
const page = await readFile(pagePath, 'utf8');
const script = await readFile(scriptPath, 'utf8');

assert(schema.$id.includes('bkl034-scientific-image-gallery'), 'schema must identify BKL-034');
assert(fixture.schemaVersion === '1.0' && fixture.authority === 'projection', 'projection/version boundary mismatch');
assert(fixture.commandAuthority === 'NONE' && fixture.safetyAuthority === 'NONE', 'authority boundary drift');
assert(fixture.items.length === 3 && fixture.items.length <= 12, 'fixture must remain bounded to three items');
const sessions = new Set();
const targets = new Set();
for (const item of fixture.items) {
  assert(item.assetType === 'scientific_image', `asset type mismatch: ${item.id}`);
  assert(item.sessionRef.startsWith('session:'), `unsafe session ref: ${item.id}`);
  assert(item.targetRef.startsWith('target:'), `unsafe target ref: ${item.id}`);
  assert(item.provenanceRefs.length > 0, `provenance missing: ${item.id}`);
  assert(item.sourceRefs.every((ref) => ref.startsWith('src:')), `unsafe source ref: ${item.id}`);
  sessions.add(item.sessionRef); targets.add(item.targetRef);
}
assert(sessions.size === fixture.items.length && targets.size === fixture.items.length, 'fixture must preserve explicit session/target links');
assert(fixture.items.some((item) => item.state === 'observed' && item.freshness === 'current'), 'current observed image missing');
assert(fixture.items.some((item) => item.state === 'stale' && item.freshness === 'stale'), 'stale image state missing');
assert(fixture.items.some((item) => item.state === 'unknown' && item.freshness === 'unknown'), 'unknown image state missing');
for (const forbidden of ['image mutation', 'processing execution', 'command path', 'remediation', 'scheduler decisionale', 'Safety Authority']) assert(contract.includes(forbidden), `boundary marker missing: ${forbidden}`);
for (const marker of ['data-bkl034-gallery', 'data-gallery-search', 'data-gallery-state', 'data-gallery-grid', 'read-only']) assert(page.includes(marker), `portal page marker missing: ${marker}`);
for (const marker of ['failClosed', 'commandAuthority', 'safetyAuthority', 'stale', 'unknown']) assert(script.includes(marker), `portal consumer boundary missing: ${marker}`);
for (const file of [fixturePath, schemaPath, contractPath, pagePath, scriptPath, stylePath]) { assert(!path.isAbsolute(file) && !file.includes('..'), `unsafe repository path: ${file}`); await access(file); }
console.log(`BKL-034 scientific image gallery portal PASS: items=${fixture.items.length}; sessions=${sessions.size}; targets=${targets.size}; authority=projection; command=NONE; safety=NONE; portal=bounded-read-only`);
