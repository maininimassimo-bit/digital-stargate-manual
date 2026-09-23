import { access, readFile } from 'node:fs/promises';
import path from 'node:path';

const fixturePath = 'docs/data/bkl034-f2-image-archive-fixture.json';
const schemaPath = 'schemas/bkl034-f2-image-archive-ingestion.schema.json';
const packagePath = 'docs/architecture/packages/BKL-034-F2-Governed-Image-Ingestion-and-Metadata-Archive.md';
const fail = message => { throw new Error(message); };
const assert = (condition, message) => { if (!condition) fail(message); };
const fixture = JSON.parse(await readFile(fixturePath, 'utf8'));
const schema = JSON.parse(await readFile(schemaPath, 'utf8'));
const packageText = await readFile(packagePath, 'utf8');
assert(schema.$id.includes('bkl034-f2-image-archive-ingestion'), 'schema identity mismatch');
assert(fixture.schemaVersion === '1.0' && fixture.authority === 'archive_projection', 'archive authority mismatch');
assert(fixture.ingestionMode === 'governed_read_only_projection', 'ingestion mode must remain projection-only');
assert(fixture.writeAuthority === 'NONE' && fixture.commandAuthority === 'NONE' && fixture.safetyAuthority === 'NONE', 'authority boundary drift');
assert(fixture.assets.length === 3 && fixture.assets.length <= 8, 'fixture must remain bounded to three assets');
const states = new Set(fixture.assets.map(asset => asset.archiveState));
assert(states.has('CATALOGED') && states.has('QUARANTINED') && states.has('UNAVAILABLE'), 'archive state coverage missing');
for (const asset of fixture.assets) {
  assert(/^obj:/.test(asset.objectRef), `object reference missing: ${asset.imageId}`);
  assert(/^[a-f0-9]{64}$/.test(asset.sha256), `sha256 missing: ${asset.imageId}`);
  assert(asset.byteSize > 0 && asset.sourceRefs.every(ref => ref.startsWith('src:')), `asset evidence invalid: ${asset.imageId}`);
  assert(asset.sessionRef.startsWith('session:') && asset.targetRef.startsWith('target:'), `context refs invalid: ${asset.imageId}`);
  if (asset.archiveState === 'UNAVAILABLE') assert(asset.metadataState === 'UNAVAILABLE', `unavailable metadata drift: ${asset.imageId}`);
  if (asset.archiveState === 'QUARANTINED') assert(asset.metadataState !== 'COMPLETE', `quarantine cannot be complete: ${asset.imageId}`);
}
for (const marker of ['quarantine', 'SHA-256', 'PixInsight', 'PARTIAL', 'UNAVAILABLE', 'image mutation', 'Safety Authority']) assert(packageText.includes(marker), `package boundary marker missing: ${marker}`);
for (const file of [fixturePath, schemaPath, packagePath]) { assert(!path.isAbsolute(file) && !file.includes('..'), `unsafe repository path: ${file}`); await access(file); }
console.log(`BKL-034-F2 image archive contract PASS: assets=${fixture.assets.length}; states=${[...states].join(',')}; authority=archive_projection; write=NONE; command=NONE; safety=NONE`);
