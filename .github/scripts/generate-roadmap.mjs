import { createHash } from 'node:crypto';
import { readFile, writeFile } from 'node:fs/promises';
import process from 'node:process';

const SOURCE_PATH = '.github/roadmap/roadmap-source.json';
const OUTPUT_PATH = 'docs/data/roadmap.json';
const VALID_STATUSES = new Set(['completed', 'active', 'planned']);

const readJson = async (path) => JSON.parse(await readFile(path, 'utf8'));
const stableJson = (value) => `${JSON.stringify(value, null, 2)}\n`;

const assert = (condition, message) => {
  if (!condition) throw new Error(message);
};

const validateSource = (source) => {
  assert(source && typeof source === 'object', 'Roadmap source must be an object');
  assert(source.schemaVersion === '2.0', 'Roadmap source schemaVersion must be 2.0');
  assert(typeof source.updatedAt === 'string' && source.updatedAt, 'updatedAt is required');
  assert(typeof source.authority === 'string' && source.authority, 'authority is required');
  assert(Array.isArray(source.streams) && source.streams.length > 0, 'At least one stream is required');
  assert(Array.isArray(source.milestones), 'milestones must be an array');

  const ids = new Set();
  for (const stream of source.streams) {
    assert(typeof stream.id === 'string' && stream.id, 'Each stream requires an id');
    assert(typeof stream.title === 'string' && stream.title, `Stream ${stream.id} requires a title`);
    assert(Array.isArray(stream.items) && stream.items.length > 0, `Stream ${stream.id} requires items`);

    for (const item of stream.items) {
      assert(typeof item.id === 'string' && item.id, `Stream ${stream.id} contains an item without id`);
      assert(!ids.has(item.id), `Duplicate roadmap item id: ${item.id}`);
      ids.add(item.id);
      assert(typeof item.title === 'string' && item.title, `Item ${item.id} requires a title`);
      assert(VALID_STATUSES.has(item.status), `Item ${item.id} has invalid status: ${item.status}`);
    }
  }

  assert(ids.has(source.currentPackage), `currentPackage does not exist: ${source.currentPackage}`);

  const milestoneIds = new Set();
  for (const milestone of source.milestones) {
    assert(typeof milestone.id === 'string' && milestone.id, 'Each milestone requires an id');
    assert(!milestoneIds.has(milestone.id), `Duplicate milestone id: ${milestone.id}`);
    milestoneIds.add(milestone.id);
    assert(VALID_STATUSES.has(milestone.status), `Milestone ${milestone.id} has invalid status`);
  }
};

const streamStatus = (items) => {
  if (items.every((item) => item.status === 'completed')) return 'completed';
  if (items.some((item) => item.status === 'active')) return 'active';
  return 'planned';
};

const buildOutput = (source) => {
  validateSource(source);

  const sourceDigest = createHash('sha256')
    .update(stableJson(source))
    .digest('hex');

  const waves = source.streams.map((stream) => ({
    id: stream.id,
    title: stream.title,
    status: streamStatus(stream.items),
    items: stream.items
  }));

  const items = waves.flatMap((wave) => wave.items);
  const completed = items.filter((item) => item.status === 'completed').length;
  const active = items.filter((item) => item.status === 'active').length;
  const planned = items.filter((item) => item.status === 'planned').length;

  return {
    schemaVersion: source.schemaVersion,
    updatedAt: source.updatedAt,
    generatedFrom: SOURCE_PATH,
    sourceDigest,
    authority: source.authority,
    projectStatus: source.projectStatus,
    currentPackage: source.currentPackage,
    nextMilestone: source.nextMilestone,
    target: source.target,
    summary: {
      total: items.length,
      completed,
      active,
      planned,
      percentCompleted: items.length ? Math.round((completed / items.length) * 100) : 0
    },
    waves,
    milestones: source.milestones
  };
};

const main = async () => {
  const mode = process.argv[2] || '--check';
  assert(['--check', '--write', '--print'].includes(mode), `Unsupported mode: ${mode}`);

  const source = await readJson(SOURCE_PATH);
  const generated = stableJson(buildOutput(source));

  if (mode === '--print') {
    process.stdout.write(generated);
    return;
  }

  if (mode === '--write') {
    await writeFile(OUTPUT_PATH, generated, 'utf8');
    process.stdout.write(`Generated ${OUTPUT_PATH} from ${SOURCE_PATH}\n`);
    return;
  }

  const current = await readFile(OUTPUT_PATH, 'utf8').catch(() => '');
  if (current !== generated) {
    process.stderr.write(
      `Roadmap drift detected. Run: node .github/scripts/generate-roadmap.mjs --write\n`
    );
    process.exitCode = 1;
    return;
  }

  process.stdout.write('Roadmap artifact is aligned with the canonical source.\n');
};

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
