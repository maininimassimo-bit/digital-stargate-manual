import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

const source = await readFile(new URL('../../docs/javascripts/dsg-search-center.js', import.meta.url), 'utf8');

const expectAll = (patterns) => {
  for (const pattern of patterns) assert.match(source, pattern);
};

test('publishes the governed Enterprise Search API 1.1 contract', () => {
  expectAll([
    /window\.DSGEnterpriseSearch = api/,
    /version: '1\.1\.0'/,
    /openResult:/,
    /closeResult:/,
    /getResults:/,
    /setState:/,
    /exportJson:/,
    /exportCsv:/,
    /clearHistory:/
  ]);
});

test('implements result detail, breadcrumb and sequential navigation', () => {
  expectAll([
    /data-search-detail/,
    /aria-label="Percorso risultato"/,
    /data-search-detail-previous/,
    /data-search-detail-next/,
    /data-search-detail-close/,
    /data-search-detail-index/,
    /search-center-detail-opened/,
    /search-center-detail-closed/
  ]);
});

test('implements governed contextual navigation for scientific metadata', () => {
  expectAll([
    /data-search-context-name/,
    /data-search-context-value/,
    /\['target', metadata\.target\]/,
    /\['year', metadata\.year\]/,
    /\['telescope', metadata\.telescope\]/,
    /\['camera', metadata\.camera\]/,
    /\['filter', metadata\.filter\]/,
    /\['quality', metadata\.qualityState\]/
  ]);
});

test('escapes dynamic result content before rendering', () => {
  expectAll([
    /const escapeHtml/,
    /escapeHtml\(item\.title\)/,
    /escapeHtml\(item\.text \|\| ''\)/,
    /escapeHtml\(item\.location\)/,
    /escapeHtml\(value\)/
  ]);
});

test('retains shareable URL, history and export capabilities', () => {
  expectAll([
    /HISTORY_KEY/,
    /window\.history\.replaceState/,
    /navigator\.clipboard\.writeText/,
    /application\/json/,
    /text\/csv;charset=utf-8/
  ]);
});
