// Same session facts already eligible for BKL-042 retrieval; no detailed telemetry.
export const CHAT_CATALOG_PATH = 'docs/data/bkl042-session-catalog.json';
export const MAX_CHAT_SOURCE_BYTES = 1_000_000;
const fields = ['sessionId','observationDate','target','analyticsState','metadataState','evidenceState','integrationHours','completionPct','severity'];
export const buildChatCatalog = catalog => {
  const projection = {schemaVersion:'1.0',kind:'BKL042_SESSION_CATALOG',authority:'projection',sessions:catalog.sessions.map(session => Object.fromEntries(fields.filter(key => Object.hasOwn(session,key)).map(key => [key,session[key]])))};
  const bytes = JSON.stringify(projection) + '\n';
  if(Buffer.byteLength(bytes,'utf8') > MAX_CHAT_SOURCE_BYTES) throw new Error('BKL042 compact session source exceeds retrieval byte budget');
  return bytes;
};
