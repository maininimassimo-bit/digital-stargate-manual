import { readFileSync, readdirSync } from 'node:fs';
import { createHash } from 'node:crypto';
import assert from 'node:assert/strict';
const vendor = 'docs/assets/vendor/three-0.180.0';
const manifest = JSON.parse(readFileSync(`${vendor}/manifest.json`, 'utf8'));
for (const [name, expected] of Object.entries(manifest.files)) {
  assert.equal(createHash('sha256').update(readFileSync(`${vendor}/${name}`)).digest('hex'), expected, name);
}
for (const name of readdirSync('docs/javascripts').filter(name => name.startsWith('immersive-'))) {
  const source = readFileSync(`docs/javascripts/${name}`, 'utf8');
  assert(!/\bfetch\s*\(|XMLHttpRequest|WebSocket|sendBeacon/.test(source), `${name}: visual renderer must not access sources`);
  assert(!/data-observatory-status|data-eagle-health|data-bkl036-score|data-home-latest/.test(source), `${name}: visual renderer must not rewrite governed bindings`);
  assert(!/https:\/\/cdn|@latest/.test(source), `${name}: production uses pinned same-origin modules`);
}
console.log('PASS: vendored integrity and read-only presentation boundary.');
