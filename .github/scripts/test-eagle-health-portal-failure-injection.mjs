import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const source = fs.readFileSync('docs/javascripts/observatory-status.js', 'utf8');

function makeElement() { return { textContent: '' }; }
function makeDocument() {
  const byKey = new Map();
  return {
    baseURI: 'https://example.test/status/',
    readyState: 'complete',
    querySelector(selector) { return selector.includes('data-eagle-health') ? makeElement() : makeElement(); },
    querySelectorAll(selector) {
      const match = selector.match(/data-eagle-health=\"([^\"]+)\"/);
      if (!match) return [];
      if (!byKey.has(match[1])) byKey.set(match[1], [makeElement()]);
      return byKey.get(match[1]);
    },
    addEventListener() {},
    values: byKey
  };
}

function runWithFetch(fetchImpl, now = Date.parse('2026-09-04T16:38:00Z')) {
  const document = makeDocument();
  const timers = [];
  const context = {
    console: { warn() {}, log() {} },
    document,
    window: { document$: null, DSG: null, setInterval(fn){timers.push(fn);return 1;} },
    fetch: fetchImpl,
    URL,
    Date: class extends Date { static now(){ return now; } },
    clearInterval() {},
    setInterval(fn){timers.push(fn);return 1;}
  };
  vm.createContext(context);
  vm.runInContext(source, context);
  return { document, timers };
}

const current = {
  schema_version:'1.0', component:'DSG.EagleHealthPortalProjection', host:'EAGLE30154',
  observed_at_utc:'2026-09-04T16:37:19.443Z', fresh_until_utc:'2026-09-04T16:39:19.443Z', quality:'CURRENT',
  source_component:'DSG.EagleHostHealthCollector', summary:{state:'UNKNOWN',reason:'POLICY_NOT_ACTIVATED'},
  signals:{ cpu:{state:'OBSERVED',quality:'CURRENT',observed_at_utc:'2026-09-04T16:37:19.443Z',fresh_until_utc:'2026-09-04T16:39:19.443Z',source:'Win32_Processor',cadence_class:'FAST',reason:null,data:{model:'CPU',physical_cores:4,logical_processors:8,load_pct:10}} }
};

function response(data, ok=true, status=200){return Promise.resolve({ok,status,json:async()=>data});}

await test('G7-D current projection renders policy-not-activated without health severity invention', async () => {
  const {document} = runWithFetch(url => String(url).includes('eagle-health.json') ? response(current) : Promise.reject(new Error('ignore')));
  await new Promise(r=>setTimeout(r,0));
  assert.equal(document.values.get('summary')[0].textContent, 'UNKNOWN / POLICY_NOT_ACTIVATED');
  assert.match(document.values.get('quality')[0].textContent, /CURRENT/);
});

await test('G7-D stale projection is forced STALE and does not present CPU as current', async () => {
  const {document} = runWithFetch(url => String(url).includes('eagle-health.json') ? response(current) : Promise.reject(new Error('ignore')), Date.parse('2026-09-04T17:00:00Z'));
  await new Promise(r=>setTimeout(r,0));
  assert.match(document.values.get('quality')[0].textContent, /STALE/);
  assert.doesNotMatch(document.values.get('cpu')[0].textContent, /load 10/);
});

await test('G7-D malformed projection fails closed to UNKNOWN', async () => {
  const malformed = {...current, component:'WRONG'};
  const {document} = runWithFetch(url => String(url).includes('eagle-health.json') ? response(malformed) : Promise.reject(new Error('ignore')));
  await new Promise(r=>setTimeout(r,0));
  assert.match(document.values.get('quality')[0].textContent, /UNKNOWN/);
  assert.equal(document.values.get('summary')[0].textContent, 'UNKNOWN / POLICY_NOT_ACTIVATED');
});

await test('G7-D missing EAGLE projection fails closed without breaking other refresh paths', async () => {
  const {document} = runWithFetch(() => Promise.reject(new Error('offline')));
  await new Promise(r=>setTimeout(r,0));
  assert.match(document.values.get('quality')[0].textContent, /UNKNOWN/);
});

await test('G7-D public projection source contains no browser credential material', () => {
  assert.doesNotMatch(source, /Authorization\s*:/i);
  assert.doesNotMatch(source, /Bearer\s+[A-Za-z0-9]/i);
  assert.doesNotMatch(source, /DSG_TELEMETRY_INGEST_TOKEN/);
});
