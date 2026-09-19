import { readFile, writeFile } from 'node:fs/promises';
import { validateArchivedTelemetry } from './verify-bkl-036-f4-archived-telemetry.mjs';

const input = process.argv[2] || 'docs/data/bkl-036-f4-telemetry-ingest-fixture.json';
const output = process.argv[3] || 'docs/data/bkl-036-f4-telemetry-archive.json';
const batch = JSON.parse(await readFile(input, 'utf8'));
validateArchivedTelemetry(batch);
if (batch.fixture_kind !== 'repository_archived_snapshot') batch.fixture_kind = 'repository_archived_snapshot';
await writeFile(output, JSON.stringify(batch, null, 2) + '\n', 'utf8');
console.log('Archived BKL-036-F4 telemetry: ' + output);

