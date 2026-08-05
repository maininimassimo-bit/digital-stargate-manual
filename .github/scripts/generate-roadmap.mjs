import { createHash } from 'node:crypto';
import { readFile, writeFile } from 'node:fs/promises';
import process from 'node:process';

const SOURCE_PATH = '.github/roadmap/roadmap-source.json';
const OUTPUT_PATH = 'docs/data/roadmap.json';
const VALID_STATUSES = new Set(['completed', 'active', 'planned']);
const VALID_STATUS_SOURCES = new Set(['completion-report', 'evidence-manifest']);

const readJson = async (path) => JSON.parse(await readFile(path, 'utf8'));
const stableJson = (value) => `${JSON.stringify(value, null, 2)}\n`;
const fileExists = async (path) => readFile(path, 'utf8').then(() => true).catch(() => false);

const assert = (condition, message) => {
  if (!condition) throw new Error(message);
};

const extractMarkdownField = (markdown, field) => {
  const escaped = field.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const match = markdown.match(new RegExp(`^\\|\\s*${escaped}\\s*\\|\\s*([^|]+?)\\s*\\|\\s*$`, 'im'));
  return match ? match[1].trim() : null;
};

const validateSource = (source) => {
  assert(source?.schemaVersion === '2.2', 'Roadmap source schemaVersion must be 2.2');
  assert(typeof source.updatedAt === 'string' && source.updatedAt, 'updatedAt is required');
  assert(typeof source.authority === 'string' && source.authority, 'authority is required');
  assert(Array.isArray(source.streams) && source.streams.length > 0, 'At least one stream is required');
  assert(Array.isArray(source.milestones), 'milestones must be an array');

  const ids = new Set();
  for (const stream of source.streams) {
    assert(typeof stream.id === 'string' && stream.id, 'Each stream requires an id');
    assert(Array.isArray(stream.items) && stream.items.length > 0, `Stream ${stream.id} requires items`);
    for (const item of stream.items) {
      assert(typeof item.id === 'string' && item.id, `Stream ${stream.id} contains an item without id`);
      assert(!ids.has(item.id), `Duplicate roadmap item id: ${item.id}`);
      ids.add(item.id);
      const explicit = typeof item.status === 'string';
      const derived = typeof item.statusSource === 'string';
      assert(explicit !== derived, `Item ${item.id} must define exactly one of status or statusSource`);
      if (explicit) assert(VALID_STATUSES.has(item.status), `Item ${item.id} has invalid status`);
      if (derived) {
        assert(VALID_STATUS_SOURCES.has(item.statusSource), `Item ${item.id} has invalid statusSource`);
        assert(typeof item.evidencePath === 'string' && item.evidencePath, `Item ${item.id} requires evidencePath`);
      }
    }
  }

  assert(ids.has(source.currentPackage), `currentPackage does not exist: ${source.currentPackage}`);
  const milestoneIds = new Set();
  for (const milestone of source.milestones) {
    assert(!milestoneIds.has(milestone.id), `Duplicate milestone id: ${milestone.id}`);
    milestoneIds.add(milestone.id);
    assert(ids.has(milestone.itemRef), `Milestone ${milestone.id} has invalid itemRef`);
  }
};

const deriveCompletionReport = async (item, records) => {
  const markdown = await readFile(item.evidencePath, 'utf8').catch(() => null);
  assert(markdown !== null, `Completion report not found for ${item.id}: ${item.evidencePath}`);
  const status = extractMarkdownField(markdown, 'Stato');
  assert(status, `Completion report for ${item.id} does not contain a Stato field`);
  records.push({ itemId: item.id, source: 'completion-report', path: item.evidencePath, status });
  return {
    status: status.toLowerCase() === 'accepted' ? 'completed' : 'active',
    evidenceStatus: status,
    evidence: { present: 1, accepted: status.toLowerCase() === 'accepted' ? 1 : 0, required: 1 }
  };
};

const evaluateManifestEntry = async (entry) => {
  const present = await fileExists(entry.path);
  if (!present) return { id: entry.id, type: entry.type, path: entry.path, required: entry.required, present: false, accepted: false, value: null };

  if (entry.acceptance?.mode === 'exists') {
    return { id: entry.id, type: entry.type, path: entry.path, required: entry.required, present: true, accepted: true, value: 'exists' };
  }

  if (entry.acceptance?.mode === 'markdown-field') {
    const markdown = await readFile(entry.path, 'utf8');
    const value = extractMarkdownField(markdown, entry.acceptance.field);
    const acceptedValues = entry.acceptance.acceptedValues || [];
    const accepted = value !== null && acceptedValues.some((candidate) => candidate.toLowerCase() === value.toLowerCase());
    return { id: entry.id, type: entry.type, path: entry.path, required: entry.required, present: true, accepted, value };
  }

  throw new Error(`Unsupported acceptance mode for ${entry.id}`);
};

const deriveEvidenceManifest = async (item, records) => {
  const manifest = await readJson(item.evidencePath).catch(() => null);
  assert(manifest, `Evidence manifest not found for ${item.id}: ${item.evidencePath}`);
  assert(manifest.packageId === item.id, `Evidence manifest packageId mismatch for ${item.id}`);
  assert(Array.isArray(manifest.evidence) && manifest.evidence.length > 0, `Evidence manifest for ${item.id} has no evidence entries`);

  const evaluations = [];
  for (const entry of manifest.evidence) evaluations.push(await evaluateManifestEntry(entry));

  const required = evaluations.filter((entry) => entry.required);
  const presentRequired = required.filter((entry) => entry.present).length;
  const acceptedRequired = required.filter((entry) => entry.accepted).length;
  const status = presentRequired === 0 ? 'planned' : acceptedRequired === required.length ? 'completed' : 'active';

  records.push({
    itemId: item.id,
    source: 'evidence-manifest',
    path: item.evidencePath,
    status,
    required: required.length,
    present: presentRequired,
    accepted: acceptedRequired
  });

  return {
    status,
    evidenceStatus: status,
    evidence: {
      manifest: item.evidencePath,
      required: required.length,
      present: presentRequired,
      accepted: acceptedRequired,
      missing: required.filter((entry) => !entry.present).map((entry) => entry.id),
      rejected: required.filter((entry) => entry.present && !entry.accepted).map((entry) => entry.id)
    }
  };
};

const deriveItem = async (item, records) => {
  if (!item.statusSource) return Object.freeze({ ...item });
  const derived = item.statusSource === 'completion-report'
    ? await deriveCompletionReport(item, records)
    : await deriveEvidenceManifest(item, records);
  const { statusSource, ...publicItem } = item;
  return Object.freeze({ ...publicItem, ...derived });
};

const streamStatus = (items) => {
  if (items.every((item) => item.status === 'completed')) return 'completed';
  if (items.some((item) => item.status === 'active')) return 'active';
  return 'planned';
};

const buildOutput = async (source) => {
  validateSource(source);
  const evidenceRecords = [];
  const waves = [];

  for (const stream of source.streams) {
    const items = [];
    for (const item of stream.items) items.push(await deriveItem(item, evidenceRecords));
    waves.push({ id: stream.id, title: stream.title, status: streamStatus(items), items });
  }

  const itemIndex = new Map(waves.flatMap((wave) => wave.items).map((item) => [item.id, item]));
  const milestones = source.milestones.map((milestone) => ({ ...milestone, status: itemIndex.get(milestone.itemRef).status }));
  evidenceRecords.sort((left, right) => left.itemId.localeCompare(right.itemId));

  const sourceDigest = createHash('sha256')
    .update(stableJson({ source, evidence: evidenceRecords }))
    .digest('hex');

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
    summary: { total: items.length, completed, active, planned, percentCompleted: items.length ? Math.round((completed / items.length) * 100) : 0 },
    evidenceSummary: {
      sources: evidenceRecords.length,
      completionReports: evidenceRecords.filter((record) => record.source === 'completion-report').length,
      evidenceManifests: evidenceRecords.filter((record) => record.source === 'evidence-manifest').length
    },
    waves,
    milestones
  };
};

const main = async () => {
  const mode = process.argv[2] || '--check';
  assert(['--check', '--write', '--print'].includes(mode), `Unsupported mode: ${mode}`);
  const source = await readJson(SOURCE_PATH);
  const generated = stableJson(await buildOutput(source));

  if (mode === '--print') return void process.stdout.write(generated);
  if (mode === '--write') {
    await writeFile(OUTPUT_PATH, generated, 'utf8');
    process.stdout.write(`Generated ${OUTPUT_PATH} from governed evidence.\n`);
    return;
  }

  const current = await readFile(OUTPUT_PATH, 'utf8').catch(() => '');
  if (current !== generated) {
    process.stderr.write('Roadmap drift detected. Run: node .github/scripts/generate-roadmap.mjs --write\n');
    process.exitCode = 1;
    return;
  }

  process.stdout.write('Roadmap artifact is aligned with canonical source and governed evidence.\n');
};

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
