import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

const relay = fs.readFileSync('infrastructure/telemetry-relay/app.py', 'utf8');
const publisher = fs.readFileSync('scripts/telemetry/Publish-SessionCompletedShadowEvent.ps1', 'utf8');

await test('SessionCompleted shadow relay has isolated append-only channel', () => {
  assert.match(relay, /\/v1\/session-completed-shadow/);
  assert.match(relay, /SESSION_COMPLETED_SHADOW_STORE/);
  assert.match(relay, /append_session_event/);
  assert.match(relay, /runtime_event_published.*is not False/);
  assert.match(relay, /safety_authority.*NONE/);
  assert.match(relay, /command_authority.*NONE/);
  assert.match(relay, /Idempotency-Key.*message_id/);
});

await test('SessionCompleted shadow relay rejects command routes', () => {
  assert.doesNotMatch(relay, /\/v1\/(command|control|remediate|reboot)/i);
});

await test('SessionCompleted publisher is HTTPS-only outside localhost', () => {
  assert.match(publisher, /requires HTTPS/);
  assert.match(publisher, /Idempotency-Key/);
  assert.match(publisher, /runtime_event_published/);
  assert.match(publisher, /BearerToken/);
  assert.doesNotMatch(publisher, /Write-Host.*Bearer|Write-Output.*Bearer/i);
});
