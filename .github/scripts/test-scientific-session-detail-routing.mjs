import assert from 'node:assert/strict';
import fs from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';

const source = fs.readFileSync('docs/javascripts/scientific-session-detail-routing.js', 'utf8');
const detailSource = fs.readFileSync('docs/javascripts/scientific-session-detail.js', 'utf8');
const detailPage = fs.readFileSync('docs/scientific-session-detail/index.md', 'utf8');
const sandbox = { URL, window: {} };
vm.runInNewContext(source, sandbox, { filename: 'scientific-session-detail-routing.js' });
const routing = sandbox.window.DSGScientificSessionDetailRouting;

const sessions = [
  { sessionId: '2026-09-05_2026-09-06', observationDate: '2026-09-05' },
  { sessionId: '2026-09-07_2026-09-08', observationDate: '2026-09-07' },
  { sessionId: '2026-09-06_2026-09-07', observationDate: '2026-09-06' }
];

test('an explicit sessionId remains authoritative', () => {
  assert.deepEqual(
    { ...routing.resolve('2026-09-05_2026-09-06', sessions) },
    { sessionId: '2026-09-05_2026-09-06', source: 'requested' }
  );
});

test('a missing sessionId resolves to the newest catalog session', () => {
  assert.deepEqual(
    { ...routing.resolve(null, sessions) },
    { sessionId: '2026-09-07_2026-09-08', source: 'latest' }
  );
});

test('latest resolution is deterministic when observation dates match', () => {
  const tied = [
    { sessionId: '2026-09-07_A', observationDate: '2026-09-07' },
    { sessionId: '2026-09-07_B', observationDate: '2026-09-07' }
  ];
  assert.equal(routing.latestSession(tied).sessionId, '2026-09-07_B');
});

test('an empty catalog fails closed', () => {
  assert.equal(routing.resolve('', []), null);
});

test('the canonical detail URL preserves other query parameters and fragments', () => {
  assert.equal(
    routing.withSessionId('https://example.test/detail/?theme=dark#weather', 'SESSION-002'),
    'https://example.test/detail/?theme=dark&sessionId=SESSION-002#weather'
  );
});

test('the detail consumer resolves a missing ID from the versioned catalog', () => {
  assert.match(detailSource, /engine\.getSessions\(source\)/);
  assert.match(detailSource, /routing\.resolve\(requestedSessionId,sessions\)/);
  assert.match(detailSource, /history\.replaceState\(null,'',routing\.withSessionId/);
  assert.doesNotMatch(detailSource, /missing-session-id/);
});

test('the detail page loads routing before the consumer and exposes the selector', () => {
  const routingIndex = detailPage.indexOf('scientific-session-detail-routing.js');
  const consumerIndex = detailPage.indexOf('scientific-session-detail.js');
  assert.ok(routingIndex >= 0 && consumerIndex > routingIndex);
  assert.match(detailPage, /data-detail-session-selector/);
});
