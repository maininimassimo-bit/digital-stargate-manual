import { readFile, readdir } from 'node:fs/promises';
import path from 'node:path';

const AMP_PATH = 'docs/architecture/assessments/AMP-002-Architecture-Program-Roadmap-Realignment.md';
const SOURCE_PATH = '.github/roadmap/roadmap-source.json';
const GENERATED_PATH = 'docs/data/roadmap.json';
const BACKLOG_PATH = 'docs/project/BACKLOG.md';
const DOCS_ROOT = 'docs';

const readJson = async (filePath) => JSON.parse(await readFile(filePath, 'utf8'));
const assert = (condition, message) => {
  if (!condition) throw new Error(message);
};

const normalizeTitle = (value) => String(value || '')
  .replace(/\s+Architecture$/i, '')
  .replace(/\s+/g, ' ')
  .trim()
  .toLowerCase();

const normalizeStatus = (value) => String(value || '')
  .replace(/\*+/g, '')
  .trim()
  .toLowerCase();

const extractMarkdownField = (markdown, field) => {
  const escaped = field.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const match = markdown.match(new RegExp(`^\\|\\s*${escaped}\\s*\\|\\s*([^|]+?)\\s*\\|\\s*$`, 'im'));
  return match ? match[1].trim() : null;
};

const parseAmpPackages = (markdown) => {
  const map = new Map();
  const heading = /\*\*(AP-\d{3})\s+—\s+([^*]+)\*\*/g;
  for (const match of markdown.matchAll(heading)) map.set(match[1], match[2].trim());

  const baseline = /^\|\s*(AP-\d{3})\s*\|\s*([^|]+?)\s*\|/gm;
  for (const match of markdown.matchAll(baseline)) {
    if (!map.has(match[1])) map.set(match[1], match[2].trim());
  }
  return map;
};

const parseBacklogStatuses = (markdown) => {
  const map = new Map();
  const row = /^\|\s*(BKL-\d{3})\s*\|\s*[^|]+\|\s*[^|]+\|\s*([^|]+?)\s*\|/gm;
  for (const match of markdown.matchAll(row)) map.set(match[1], match[2].trim().replace(/^\*\*|\*\*$/g, ''));
  return map;
};

const discoverAcceptedClosures = async () => {
  const files = await readdir(DOCS_ROOT, { recursive: true });
  const closureFiles = files
    .filter((entry) => /BKL-.*closure.*\.md$/i.test(entry))
    .map((entry) => path.join(DOCS_ROOT, entry));

  const accepted = [];
  for (const filePath of closureFiles) {
    const markdown = await readFile(filePath, 'utf8');
    const status = extractMarkdownField(markdown, 'Status') || extractMarkdownField(markdown, 'Stato') || '';
    if (!/accepted/i.test(status)) continue;

    const packageField = extractMarkdownField(markdown, 'Package') || '';
    const ids = new Set([
      ...(filePath.match(/BKL-\d{3}/g) || []),
      ...(packageField.match(/BKL-\d{3}/g) || [])
    ]);

    for (const id of ids) accepted.push({ id, filePath, status });
  }
  return accepted;
};

const main = async () => {
  const [amp, source, generated, backlog, acceptedClosures] = await Promise.all([
    readFile(AMP_PATH, 'utf8'),
    readJson(SOURCE_PATH),
    readJson(GENERATED_PATH),
    readFile(BACKLOG_PATH, 'utf8'),
    discoverAcceptedClosures()
  ]);

  const ampPackages = parseAmpPackages(amp);
  const expectedIds = Array.from({ length: 15 }, (_, i) => `AP-${String(i + 1).padStart(3, '0')}`);
  for (const id of expectedIds) assert(ampPackages.has(id), `AMP-002 does not define ${id}`);

  const sourceItems = source.streams.flatMap((stream) => stream.items);
  const sourceIndex = new Map(sourceItems.map((item) => [item.id, item]));
  const generatedItems = generated.waves.flatMap((wave) => wave.items);
  const generatedIndex = new Map(generatedItems.map((item) => [item.id, item]));

  for (const id of expectedIds) {
    const ampTitle = ampPackages.get(id);
    const sourceItem = sourceIndex.get(id);
    const generatedItem = generatedIndex.get(id);
    assert(sourceItem, `Roadmap source is missing ${id}`);
    assert(generatedItem, `Generated roadmap is missing ${id}`);
    assert(normalizeTitle(sourceItem.title) === normalizeTitle(ampTitle), `${id} title mismatch between AMP-002 and roadmap source: "${ampTitle}" vs "${sourceItem.title}"`);
    assert(normalizeTitle(generatedItem.title) === normalizeTitle(sourceItem.title), `${id} title mismatch between roadmap source and generated roadmap`);
  }

  assert(sourceIndex.has(source.currentPackage), `Roadmap currentPackage is not a defined roadmap item: ${source.currentPackage}`);
  assert(generated.currentPackage === source.currentPackage, 'Generated roadmap currentPackage differs from roadmap source');
  assert(generated.nextMilestone === source.nextMilestone, 'Generated roadmap nextMilestone differs from roadmap source');
  assert(generated.target === source.target, 'Generated roadmap target differs from roadmap source');

  const currentGenerated = generatedIndex.get(source.currentPackage);
  assert(currentGenerated, `Generated roadmap is missing currentPackage ${source.currentPackage}`);
  assert(currentGenerated.status === 'active', `Roadmap currentPackage ${source.currentPackage} must be active, found ${currentGenerated.status}`);
  assert(String(source.nextMilestone || '').includes(source.currentPackage), `Roadmap nextMilestone must reference currentPackage ${source.currentPackage}`);

  const backlogStatuses = parseBacklogStatuses(backlog);

  for (const [id, backlogStatusRaw] of backlogStatuses) {
    const generatedItem = generatedIndex.get(id);
    if (!generatedItem) continue;
    const backlogStatus = normalizeStatus(backlogStatusRaw);
    if (backlogStatus === 'done') {
      assert(generatedItem.status === 'completed', `${id} is Done in BACKLOG.md but ${generatedItem.status} in generated roadmap`);
    }
    if (backlogStatus === 'in progress') {
      assert(generatedItem.status === 'active', `${id} is In Progress in BACKLOG.md but ${generatedItem.status} in generated roadmap`);
    }
  }

  const milestoneBacklogRefs = String(source.nextMilestone || '').match(/BKL-\d{3}/g) || [];
  for (const id of milestoneBacklogRefs) {
    const status = backlogStatuses.get(id);
    assert(status, `Roadmap nextMilestone references ${id}, but it is missing from BACKLOG.md`);
    assert(normalizeStatus(status) !== 'done', `Roadmap nextMilestone references completed backlog item ${id}`);
  }

  for (const closure of acceptedClosures) {
    if (!generatedIndex.has(closure.id)) continue;
    const roadmapStatus = generatedIndex.get(closure.id).status;
    const backlogStatus = backlogStatuses.get(closure.id);
    assert(roadmapStatus === 'completed', `${closure.id} has accepted closure ${closure.filePath} but roadmap status is ${roadmapStatus}`);
    if (backlogStatus) {
      assert(normalizeStatus(backlogStatus) === 'done', `${closure.id} has accepted closure ${closure.filePath} but BACKLOG.md status is ${backlogStatus}`);
    }
  }

  console.log(`Roadmap consistency PASS: ${expectedIds.length} AMP packages aligned; ${acceptedClosures.length} accepted BKL closure bindings checked; currentPackage=${source.currentPackage}; nextMilestone=${source.nextMilestone}`);
};

main().catch((error) => {
  console.error(`Roadmap consistency FAILED: ${error.message}`);
  process.exitCode = 1;
});
