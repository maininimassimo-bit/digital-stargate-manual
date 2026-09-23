import { access, readFile } from 'node:fs/promises';
import path from 'node:path';

const fixturePath = 'docs/data/bkl034-f2-ingestion-request-fixture.json';
const schemaPath = 'schemas/bkl034-f2-ingestion-request.schema.json';
const packagePath = 'docs/architecture/packages/BKL-034-F2-Storage-Boundary-Preflight.md';
const fail = message => { throw new Error(message); };
const assert = (condition, message) => { if (!condition) fail(message); };
const request = JSON.parse(await readFile(fixturePath, 'utf8'));
const schema = JSON.parse(await readFile(schemaPath, 'utf8'));
const packageText = await readFile(packagePath, 'utf8');
assert(schema.$id.includes('bkl034-f2-ingestion-request'), 'schema identity mismatch');
assert(request.mode === 'DRY_RUN_PREFLIGHT', 'preflight mode must be dry-run');
assert(request.securityPreflight.writeAttempted === false, 'preflight must not attempt a write');
assert(request.securityPreflight.mimeChecked === true && request.securityPreflight.magicBytesChecked === true, 'binary checks missing');
assert(request.securityPreflight.exifPolicy === 'SANITIZE_BEFORE_PUBLISH', 'EXIF policy must sanitize before publish');
assert(request.securityPreflight.malwareScanState === 'PASS', 'fixture must represent a passed malware scan');
assert(request.metadata.metadataState === 'COMPLETE', 'fixture must have complete metadata');
assert(request.metadata.workflowRefs.length > 0 && request.metadata.workflowRefs.every(ref => ref.startsWith('workflow:pixinsight:')), 'PixInsight workflow relation missing');
assert(/^[a-f0-9]{64}$/.test(request.asset.sha256), 'SHA-256 missing');
for (const marker of ['QUARANTINED', 'writeAttempted', 'Cloud Run write path', 'Safety Authority']) assert(packageText.includes(marker), `preflight boundary marker missing: ${marker}`);
for (const file of [fixturePath, schemaPath, packagePath]) { assert(!path.isAbsolute(file) && !file.includes('..'), `unsafe repository path: ${file}`); await access(file); }
console.log(`BKL-034-F2 ingestion preflight PASS: mode=${request.mode}; malware=${request.securityPreflight.malwareScanState}; metadata=${request.metadata.metadataState}; workflowRefs=${request.metadata.workflowRefs.length}; writeAttempted=false`);
