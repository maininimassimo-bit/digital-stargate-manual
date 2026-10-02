/* Bounded public read model. Validation is not scientific acceptance. */
((root, factory) => {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.DSGBkl049WorkflowContract = api;
})(globalThis, () => {
  'use strict';
  const MAX_BYTES = 2 * 1024 * 1024;
  const MAX_LIFETIME_MS = 24 * 60 * 60 * 1000;
  const citation = 'architecture/assessments/BKL-049-F1-Workflow-Archive-Architecture/';
  const gaps = ['PARTIAL_HISTORY', 'EXECUTION_NOT_OBSERVED', 'UPSTREAM_RELATIONS_UNRESOLVED',
    'PROCESS_VERSIONS_UNAVAILABLE', 'PUBLIC_FIELDS_OMITTED'];
  const need = condition => { if (!condition) throw new Error('WORKFLOW_UNAVAILABLE'); };
  const closed = (value, keys) => need(value && typeof value === 'object' && !Array.isArray(value)
    && Object.keys(value).length === keys.length && keys.every(key => Object.hasOwn(value, key)));
  const id = (value, prefix) => typeof value === 'string'
    && new RegExp(`^${prefix}-[A-Za-z0-9_-]{1,64}(?![\\s\\S])`, 'u').test(value);
  const symbol = value => typeof value === 'string' && /^[A-Za-z_][A-Za-z0-9_]{0,127}(?![\s\S])/u.test(value);
  const count = value => Number.isSafeInteger(value) && value >= 0;
  const stamp = value => {
    need(typeof value === 'string' && /^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$/u.test(value));
    const time = Date.parse(value);
    need(Number.isFinite(time) && new Date(time).toISOString() === value.replace('Z', '.000Z'));
    return time;
  };
  const canonical = value => JSON.stringify(value, function (key, item) {
    if (item && typeof item === 'object' && !Array.isArray(item)) {
      return Object.fromEntries(Object.keys(item).sort().map(name => [name, item[name]]));
    }
    return item;
  }).replace(/[\u007f-\uffff]/g, char => '\\u' + char.charCodeAt(0).toString(16).padStart(4, '0'));
  const freeze = value => {
    if (value && typeof value === 'object') { Object.values(value).forEach(freeze); Object.freeze(value); }
    return value;
  };
  const validateWorkflow = value => {
    const external = value?.kind === 'BKL049_PUBLIC_EXTERNAL_WORKFLOW';
    const keys = ['schemaVersion', 'kind', 'authority', 'actionAuthority', 'imageId', 'imageVersionId',
      'workflowId', 'bindingEvidenceClass', 'captureCompleteness', 'executionEvidence', 'orderSemantics',
      'methodCitation', 'steps', 'omittedStepCount', 'gaps'];
    if (external) keys.push('scientificContext', 'title', 'attribution', 'preview');
    closed(value, keys);
    const expectedCitation = external ? 'architecture/ADR-019-External-Retrospective-Scientific-Records/' : citation;
    if (external) {
      closed(value.scientificContext, ['origin', 'metadataState', 'qualityState', 'subjectIdentification']);
      need(value.scientificContext.origin === 'EXTERNAL' && value.scientificContext.metadataState === 'PARTIAL'
        && value.scientificContext.qualityState === 'UNKNOWN'
        && value.scientificContext.subjectIdentification === 'DECLARED_NOT_INDEPENDENTLY_VERIFIED');
      const text = (item, limit) => typeof item === 'string' && item.trim().length > 0
        && item.length <= limit && !/[\u0000-\u001f]/u.test(item);
      closed(value.preview, ['url', 'alt']);
      need(text(value.title, 200) && text(value.attribution, 256) && text(value.preview.alt, 300)
        && typeof value.preview.url === 'string' && value.preview.url.length <= 1024
        && /^https:\/\/storage\.googleapis\.com\/[a-z0-9][a-z0-9.-]{1,220}\/[A-Za-z0-9_-][A-Za-z0-9_/-]*\.(?:jpg|jpeg|png|webp)(?![\s\S])/u.test(value.preview.url));
    }
    need(value.schemaVersion === (external ? '2.0' : '1.0')
      && value.kind === (external ? 'BKL049_PUBLIC_EXTERNAL_WORKFLOW' : 'BKL049_PUBLIC_WORKFLOW')
      && value.authority === 'processing_evidence' && value.actionAuthority === 'NONE'
      && id(value.imageId, 'IMG') && id(value.imageVersionId, 'VER') && id(value.workflowId, 'WF')
      && value.bindingEvidenceClass === 'DECLARED' && value.executionEvidence === 'NOT_ESTABLISHED'
      && value.orderSemantics === 'EXPORTED_CONFIGURATION_ORDER' && value.methodCitation === expectedCitation
      && count(value.omittedStepCount) && Array.isArray(value.steps) && value.steps.length <= 512
      && value.omittedStepCount + value.steps.length <= 512
      && value.captureCompleteness === (value.steps.length ? 'PARTIAL' : 'UNAVAILABLE')
      && Array.isArray(value.gaps) && JSON.stringify(value.gaps) === JSON.stringify(gaps));
    let ordinal = 0;
    for (const step of value.steps) {
      closed(step, ['sourceOrdinal', 'processId', 'evidenceClass', 'parameters', 'omittedParameterCount']);
      need(count(step.sourceOrdinal) && step.sourceOrdinal > ordinal && step.sourceOrdinal <= 512
        && step.sourceOrdinal <= value.omittedStepCount + value.steps.length
        && symbol(step.processId) && step.evidenceClass === 'DECLARED' && count(step.omittedParameterCount)
        && Array.isArray(step.parameters) && step.parameters.length <= 128);
      need(step.omittedParameterCount + step.parameters.length <= 2048);
      ordinal = step.sourceOrdinal;
      const names = new Set();
      for (const parameter of step.parameters) {
        closed(parameter, ['name', 'lexicalJson']);
        need(symbol(parameter.name) && !names.has(parameter.name) && typeof parameter.lexicalJson === 'string'
          && parameter.lexicalJson.length > 0 && parameter.lexicalJson.length <= 4096);
        names.add(parameter.name);
      }
    }
    need(new TextEncoder().encode(canonical(value)).length <= 256 * 1024);
    return value;
  };
  const validateCollection = (value, now = Date.now()) => {
    closed(value, ['schemaVersion', 'kind', 'authority', 'actionAuthority', 'publishedAt', 'validUntil', 'records']);
    need(Number.isFinite(now) && value.schemaVersion === '1.0' && value.kind === 'BKL049_PUBLIC_COLLECTION'
      && value.authority === 'processing_evidence' && value.actionAuthority === 'NONE'
      && Array.isArray(value.records) && value.records.length <= 8);
    if (!value.records.length) {
      need(value.publishedAt === null && value.validUntil === null);
    } else {
      const start = stamp(value.publishedAt), end = stamp(value.validUntil);
      need(start <= now && now < end && end > start && end - start <= MAX_LIFETIME_MS);
    }
    const images = new Set(), workflows = new Set();
    value.records.forEach(record => {
      validateWorkflow(record);
      const key = record.imageId + '/' + record.imageVersionId;
      need(!images.has(key) && !workflows.has(record.workflowId));
      images.add(key); workflows.add(record.workflowId);
    });
    need(new TextEncoder().encode(canonical(value)).length <= MAX_BYTES);
    return value;
  };
  const parseCollection = (raw, now = Date.now()) => {
    need(typeof raw === 'string' && new TextEncoder().encode(raw).length <= MAX_BYTES);
    const value = JSON.parse(raw);
    // Duplicate keys, alternate encodings and trailing payloads fail closed.
    need([canonical(value), canonical(value) + '\n', canonical(value) + '\r\n'].includes(raw));
    return freeze(validateCollection(value, now));
  };
  const resolve = (collection, imageId, versionId, workflowId, now = Date.now()) => {
    validateCollection(collection, now);
    need(id(imageId, 'IMG') && id(versionId, 'VER') && id(workflowId, 'WF'));
    return collection.records.find(record => record.imageId === imageId
      && record.imageVersionId === versionId && record.workflowId === workflowId) || null;
  };
  return Object.freeze({MAX_BYTES, MAX_LIFETIME_MS, canonical, validateWorkflow, validateCollection, parseCollection, resolve});
});
