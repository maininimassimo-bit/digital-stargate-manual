import { readFile, writeFile } from 'node:fs/promises';

const ROADMAP_PATH = 'docs/data/roadmap.json';
const DISCOVERY_PATH = 'docs/architecture/validation/AP-013-Session-Discovery-Execution-Evidence.md';
const ACCEPTANCE_PATH = 'docs/architecture/validation/AP-013-Operational-Acceptance.md';
const SCHEDULER_PATH = 'docs/architecture/validation/AP-013-Morning-Transfer-Scheduler-Evidence.md';
const OUTPUT_PATH = 'docs/data/scientific-platform-status.json';

const readJson = async (filePath) => JSON.parse(await readFile(filePath, 'utf8'));
const stableJson = (value) => `${JSON.stringify(value, null, 2)}\n`;
const assert = (condition, message) => { if (!condition) throw new Error(message); };

const extractTableValue = (markdown, label) => {
  const escaped = label.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const match = markdown.match(new RegExp(`^\\|\\s*${escaped}\\s*\\|\\s*([^|]+?)\\s*\\|\\s*$`, 'im'));
  return match ? match[1].trim() : null;
};

const extractNumber = (markdown, label) => {
  const raw = extractTableValue(markdown, label);
  assert(raw !== null, `Missing metric: ${label}`);
  const normalized = raw.replace(/[^0-9-]/g, '');
  assert(normalized !== '', `Metric ${label} is not numeric: ${raw}`);
  return Number.parseInt(normalized, 10);
};

const toIsoDate = (value) => {
  const match = String(value || '').match(/^(\d{2})\/(\d{2})\/(\d{4})$/);
  assert(match, `Unsupported date format: ${value}`);
  return `${match[3]}-${match[2]}-${match[1]}`;
};

const findRoadmapItem = (roadmap, id) => {
  for (const wave of roadmap.waves || []) {
    const item = (wave.items || []).find((candidate) => candidate.id === id);
    if (item) return item;
  }
  throw new Error(`Roadmap item not found: ${id}`);
};

const requireStatus = (roadmap, id) => {
  const item = findRoadmapItem(roadmap, id);
  return { id: item.id, title: item.title, status: item.status };
};

const buildProjection = async () => {
  const [roadmap, discovery, acceptance, scheduler] = await Promise.all([
    readJson(ROADMAP_PATH),
    readFile(DISCOVERY_PATH, 'utf8'),
    readFile(ACCEPTANCE_PATH, 'utf8'),
    readFile(SCHEDULER_PATH, 'utf8')
  ]);

  assert(roadmap.generatedFrom === '.github/roadmap/roadmap-source.json', 'Roadmap projection must identify the canonical roadmap source');
  assert(typeof roadmap.currentPackage === 'string' && roadmap.currentPackage, 'Roadmap currentPackage is required');

  const maxFilesMatch = acceptance.match(/`MaxFilesPerRun\s*<=\s*(\d+)`/i);
  assert(maxFilesMatch, 'AP-013 Operational Acceptance does not define MaxFilesPerRun');

  const schedulerTimeMatch = scheduler.match(/trigger giornaliero alle\s+(\d{2}:\d{2})/i);
  assert(schedulerTimeMatch, 'Morning scheduler evidence does not define the daily trigger time');

  const acceptanceState = extractTableValue(acceptance, 'Stato');
  const operationalIncrement = extractTableValue(acceptance, 'Operational increment');
  assert(String(acceptanceState).toLowerCase() === 'accepted', `AP-013 acceptance is not Accepted: ${acceptanceState}`);
  assert(/limited production/i.test(String(operationalIncrement)), `AP-013 operational increment is not Limited Production: ${operationalIncrement}`);

  const discoveryDate = toIsoDate(extractTableValue(discovery, 'Data verifica'));
  const discoveryEvidenceId = String(extractTableValue(discovery, 'Evidence ID') || '').replace(/`/g, '');
  assert(discoveryEvidenceId, 'AP-013 discovery Evidence ID is required');

  const currentItem = findRoadmapItem(roadmap, roadmap.currentPackage);
  assert(currentItem.status === 'active', `Current roadmap package ${roadmap.currentPackage} must be active`);

  return {
    schemaVersion: '1.0',
    updatedAt: roadmap.updatedAt,
    generatedFrom: {
      roadmap: ROADMAP_PATH,
      discovery: DISCOVERY_PATH,
      operationalAcceptance: ACCEPTANCE_PATH,
      schedulerEvidence: SCHEDULER_PATH
    },
    authorityBoundary: {
      roadmapAuthority: roadmap.authority,
      projectionOnly: true,
      runtimeTelemetry: false,
      safetyAuthority: 'LOCAL_PHYSICAL_INTERLOCKS'
    },
    current: {
      package: { id: currentItem.id, title: currentItem.title, status: currentItem.status },
      nextMilestone: roadmap.nextMilestone,
      target: roadmap.target
    },
    architecture: {
      ap013: requireStatus(roadmap, 'AP-013'),
      ap013c: requireStatus(roadmap, 'AP-013C'),
      ap014: requireStatus(roadmap, 'AP-014'),
      ap015: requireStatus(roadmap, 'AP-015')
    },
    intelligence: {
      knowledgeAiEvidenceContract: requireStatus(roadmap, 'BKL-044'),
      targetKnowledgeBase: requireStatus(roadmap, 'BKL-035'),
      nightTimelineReplay: requireStatus(roadmap, 'BKL-040'),
      anomalyTrendCenter: requireStatus(roadmap, 'BKL-038'),
      pixInsightProvenance: requireStatus(roadmap, 'BKL-045')
    },
    historicalDiscovery: {
      evidenceId: discoveryEvidenceId,
      asOf: discoveryDate,
      files: extractNumber(discovery, 'File sorgente'),
      sessions: extractNumber(discovery, 'Sessioni individuate'),
      parsed: extractNumber(discovery, 'Filename parsed'),
      ambiguous: extractNumber(discovery, 'Filename ambiguous'),
      failed: extractNumber(discovery, 'Filename failed')
    },
    transfer: {
      status: 'Limited Production',
      mode: 'COPY_ONLY',
      maxFilesPerRun: Number.parseInt(maxFilesMatch[1], 10),
      hashAlgorithm: 'SHA-256',
      overwriteExisting: false,
      sourceCleanupAuthorized: false,
      transportRole: 'STAGING_ONLY'
    },
    scheduler: {
      state: 'Ready',
      timeLocal: schedulerTimeMatch[1]
    },
    safety: {
      commandAuthority: false,
      automaticRemediationAuthority: false,
      presentTimeSafetyInferenceFromHistoricalEvidence: false
    }
  };
};

const main = async () => {
  const mode = process.argv[2] || '--check';
  assert(['--check', '--write', '--print'].includes(mode), `Unsupported mode: ${mode}`);

  const projection = await buildProjection();
  const serialized = stableJson(projection);

  if (mode === '--print') {
    process.stdout.write(serialized);
    return;
  }

  if (mode === '--write') {
    await writeFile(OUTPUT_PATH, serialized, 'utf8');
    process.stdout.write(`Generated ${OUTPUT_PATH} from governed repository evidence.\n`);
    return;
  }

  const current = await readJson(OUTPUT_PATH).catch(() => null);
  if (!current || JSON.stringify(current) !== JSON.stringify(projection)) {
    process.stderr.write('Scientific Platform status drift detected. Run: node .github/scripts/generate-scientific-platform-status.mjs --write\n');
    process.exitCode = 1;
    return;
  }

  process.stdout.write('Scientific Platform status is aligned with governed repository evidence.\n');
};

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
