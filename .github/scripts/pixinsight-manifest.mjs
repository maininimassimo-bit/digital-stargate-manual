import { createHash } from 'node:crypto';

const isObject = (value) => value !== null && typeof value === 'object' && !Array.isArray(value);
const isDateTime = (value) => typeof value === 'string' && !Number.isNaN(Date.parse(value));
const isNonEmptyString = (value, maxLength) => typeof value === 'string' && value.length > 0 && value.length <= maxLength;

const allowedKeys = {
  root: ['schemaVersion', 'manifestId', 'exportedAt', 'source', 'observationContext', 'processingRun'],
  source: ['product', 'productVersion', 'hostId', 'workspaceId'],
  observationContext: ['sessionId', 'target', 'projectId', 'campaignId'],
  processingRun: ['externalRunId', 'startedAt', 'completedAt', 'processes', 'inputs', 'outputs', 'parameters']
};

const unexpectedKeys = (value, allowed) => Object.keys(value).filter((key) => !allowed.includes(key));

export const canonicalize = (value) => {
  if (Array.isArray(value)) return `[${value.map(canonicalize).join(',')}]`;
  if (isObject(value)) {
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonicalize(value[key])}`).join(',')}}`;
  }
  return JSON.stringify(value);
};

export const digestManifest = (manifest) => createHash('sha256').update(canonicalize(manifest), 'utf8').digest('hex');

export const idempotencyKey = (manifest) => {
  const digest = digestManifest(manifest);
  return createHash('sha256').update(`${manifest.schemaVersion}${manifest.manifestId}${digest}`, 'utf8').digest('hex');
};

export const validateManifest = (manifest) => {
  const errors = [];
  const add = (path, code, message) => errors.push({ path, code, message });

  if (!isObject(manifest)) return { valid: false, errors: [{ path: '$', code: 'type', message: 'Manifest must be an object.' }] };

  unexpectedKeys(manifest, allowedKeys.root).forEach((key) => add(`$.${key}`, 'additional-property', 'Property is not allowed.'));
  if (manifest.schemaVersion !== '1.0') add('$.schemaVersion', 'unsupported-schema', 'Only schemaVersion 1.0 is supported.');
  if (!isNonEmptyString(manifest.manifestId, 128) || !/^PXM-[A-Za-z0-9._:-]{8,}$/.test(manifest.manifestId)) add('$.manifestId', 'format', 'manifestId is invalid.');
  if (!isDateTime(manifest.exportedAt)) add('$.exportedAt', 'date-time', 'exportedAt must be an ISO date-time.');

  if (!isObject(manifest.source)) add('$.source', 'type', 'source must be an object.');
  else {
    unexpectedKeys(manifest.source, allowedKeys.source).forEach((key) => add(`$.source.${key}`, 'additional-property', 'Property is not allowed.'));
    if (manifest.source.product !== 'PixInsight') add('$.source.product', 'const', 'source.product must be PixInsight.');
    for (const [key, max] of [['productVersion', 64], ['hostId', 128], ['workspaceId', 128]]) {
      if (!isNonEmptyString(manifest.source[key], max)) add(`$.source.${key}`, 'string', `${key} must be a non-empty string.`);
    }
  }

  if (!isObject(manifest.observationContext)) add('$.observationContext', 'type', 'observationContext must be an object.');
  else {
    unexpectedKeys(manifest.observationContext, allowedKeys.observationContext).forEach((key) => add(`$.observationContext.${key}`, 'additional-property', 'Property is not allowed.'));
    for (const [key, max] of [['sessionId', 128], ['target', 256], ['projectId', 128], ['campaignId', 128]]) {
      if (!isNonEmptyString(manifest.observationContext[key], max)) add(`$.observationContext.${key}`, 'string', `${key} must be a non-empty string.`);
    }
  }

  if (!isObject(manifest.processingRun)) add('$.processingRun', 'type', 'processingRun must be an object.');
  else {
    const run = manifest.processingRun;
    unexpectedKeys(run, allowedKeys.processingRun).forEach((key) => add(`$.processingRun.${key}`, 'additional-property', 'Property is not allowed.'));
    if (!isNonEmptyString(run.externalRunId, 128)) add('$.processingRun.externalRunId', 'string', 'externalRunId must be a non-empty string.');
    for (const key of ['startedAt', 'completedAt']) if (run[key] !== null && !isDateTime(run[key])) add(`$.processingRun.${key}`, 'date-time', `${key} must be null or an ISO date-time.`);
    for (const [key, maxItems, maxLength] of [['processes', 512, 256], ['inputs', 4096, 1024], ['outputs', 4096, 1024]]) {
      if (!Array.isArray(run[key])) add(`$.processingRun.${key}`, 'type', `${key} must be an array.`);
      else {
        if (run[key].length > maxItems) add(`$.processingRun.${key}`, 'max-items', `${key} exceeds the allowed item count.`);
        run[key].forEach((value, index) => { if (!isNonEmptyString(value, maxLength)) add(`$.processingRun.${key}[${index}]`, 'string', 'Array item must be a non-empty string.'); });
      }
    }
    if (!isObject(run.parameters)) add('$.processingRun.parameters', 'type', 'parameters must be an object.');
    else if (Object.keys(run.parameters).length > 1024) add('$.processingRun.parameters', 'max-properties', 'parameters exceeds the allowed property count.');
  }

  return { valid: errors.length === 0, errors };
};
