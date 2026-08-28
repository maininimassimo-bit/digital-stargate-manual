import { readFile } from 'node:fs/promises';

const AMP_PATH = 'docs/architecture/assessments/AMP-002-Architecture-Program-Roadmap-Realignment.md';
const SOURCE_PATH = '.github/roadmap/roadmap-source.json';
const GENERATED_PATH = 'docs/data/roadmap.json';
const BACKLOG_PATH = 'docs/project/BACKLOG.md';

const readJson = async (path) => JSON.parse(await readFile(path, 'utf8'));
const assert = (condition, message) => {
  if (!condition) throw new Error(message);
};

const normalizeTitle = (value) => String(value || '')
  .replace(/\s+Architecture$/i, '')
  .replace(/\s+/g, ' ')
  .trim()
  .toLowerCase();

const parseAmpPackages = (markdown) => {
  const map = new Map();
  const heading = /\*\*(AP-\d{3})\s+—\s+([^*]+)\*\*/g;
  for (const match of markdown.matchAll(heading)) {
    map.set(match[1], match[2].trim());
  }

  // AP-001..AP-006 are represented in the verified baseline table rather than bold headings.
  const baseline = /^\|\s*(AP-\d{3})\s*\|\s*([^|]+?)\s*\|/gm;
  for (const match of markdown.matchAll(baseline)) {
    if (!map.has(match[1])) map.set(match[1], match[2].trim());
  }
  return map;
};

const parseBacklogStatuses = (markdown) => {
  const map = new Map();
  const row = /^\|\s*(BKL-\d{3})\s*\|\s*[^|]+\|\s*[^|]+\|\s*\*\*?([^|*]+?)\*\*?\s*\|/gm;
  for (const match of markdown.matchAll(row)) map.set(match[1], match[2].trim());

  const plainRow = /^\|\s*(BKL-\d{3})\s*\|\s*[^|]+\|\s*[^|]+\|\s*([^|]+?)\s*\|/gm;
  for (const match of markdown.matchAll(plainRow)) {
    if (!map.has(match[1])) map.set(match[1], match[2].trim().replace(/^\*\*|\*\*$/g, ''));
  }
  return map;
};

const main = async () => {
  const [amp, source, generated, backlog] = await Promise.all([
    readFile(AMP_PATH, 'utf8'),
    readJson(SOURCE_PATH),
    readJson(GENERATED_PATH),
    readFile(BACKLOG_PATH, 'utf8')
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

  const backlogStatuses = parseBacklogStatuses(backlog);
  const milestoneBacklogRefs = String(source.nextMilestone || '').match(/BKL-\d{3}/g) || [];
  for (const id of milestoneBacklogRefs) {
    const status = backlogStatuses.get(id);
    assert(status, `Roadmap nextMilestone references ${id}, but it is missing from BACKLOG.md`);
    assert(status.toLowerCase() !== 'done', `Roadmap nextMilestone references completed backlog item ${id}`);
  }

  console.log(`Roadmap consistency PASS: ${expectedIds.length} AMP packages aligned; currentPackage=${source.currentPackage}; nextMilestone=${source.nextMilestone}`);
};

main().catch((error) => {
  console.error(`Roadmap consistency FAILED: ${error.message}`);
  process.exitCode = 1;
});
