import { createHash } from 'node:crypto';

export const ID_METHOD = 'BKL038-F3-DERIVED-ID-SHA256-1';
export const ID_METHOD_VERSION = '1.0';

const requiredString = (value, field) => {
  if (typeof value !== 'string' || value.length === 0) throw new Error(`BKL-038 F3 ID FAILED: ${field} is required`);
  return value;
};

export function canonicalIdentityTuple(record) {
  if (!record || typeof record !== 'object' || Array.isArray(record)) throw new Error('BKL-038 F3 ID FAILED: record must be an object');
  if (!Array.isArray(record.source_record_refs) || record.source_record_refs.length === 0) throw new Error('BKL-038 F3 ID FAILED: source_record_refs are required');
  const source_record_refs = record.source_record_refs.map((value, index) => requiredString(value, `source_record_refs[${index}]`));
  const window = record.analysis_window;
  if (!window || typeof window !== 'object' || Array.isArray(window)) throw new Error('BKL-038 F3 ID FAILED: analysis_window is required');

  return {
    semantic_type: requiredString(record.semantic_type, 'semantic_type'),
    method_id: requiredString(record.method_id, 'method_id'),
    method_version: requiredString(record.method_version, 'method_version'),
    source_record_refs,
    analysis_window: {
      start_utc: window.start_utc === null ? null : requiredString(window.start_utc, 'analysis_window.start_utc'),
      end_utc: window.end_utc === null ? null : requiredString(window.end_utc, 'analysis_window.end_utc')
    }
  };
}

export function canonicalIdentitySerialization(record) {
  return JSON.stringify(canonicalIdentityTuple(record));
}

export function deriveRecordId(record) {
  const canonical = canonicalIdentitySerialization(record);
  const digest = createHash('sha256').update(canonical, 'utf8').digest('hex');
  return `AT-SHA256-${digest}`;
}
