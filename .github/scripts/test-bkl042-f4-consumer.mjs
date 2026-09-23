import fs from 'node:fs';
import assert from 'node:assert/strict';
const js = fs.readFileSync('docs/javascripts/bkl042-advisory.js', 'utf8');
const page = fs.readFileSync('docs/bkl042-advisory/index.md', 'utf8');
const css = fs.readFileSync('docs/styles/bkl042-advisory.css', 'utf8');
assert.ok(js.includes("cache:'no-store'")); assert.ok(js.includes('UNAVAILABLE · FAIL-CLOSED')); assert.ok(js.includes('BOUNDED_SYNTHETIC_NOT_CURRENT'));
assert.ok(js.includes("actionAuthority !== 'NONE'") && js.includes("commandAuthority !== 'NONE'") && js.includes("safetyAuthority !== 'NONE'"));
assert.ok(page.includes('data-bkl042-advisory') && page.includes('nessun modello AI')); assert.ok(css.includes('.dsg-bkl042__failure'));
console.log('BKL-042-F4 consumer PASS: static accessibility, bounded freshness and fail-closed authority checks present');
