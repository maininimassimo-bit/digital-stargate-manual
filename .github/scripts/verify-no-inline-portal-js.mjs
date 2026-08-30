import { readdir, readFile } from 'node:fs/promises';
import { extname, join, relative } from 'node:path';

const ROOT = 'docs';
const EXTENSIONS = new Set(['.md', '.html', '.htm']);
const violations = [];

const walk = async (dir) => {
  const entries = await readdir(dir, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) files.push(...await walk(path));
    else if (EXTENSIONS.has(extname(entry.name).toLowerCase())) files.push(path);
  }
  return files;
};

const stripMarkdownCode = (text) => {
  const lines = text.split(/\r?\n/);
  const kept = [];
  let fence = null;

  for (const line of lines) {
    const match = line.match(/^\s*(```+|~~~+)/);
    if (match) {
      const marker = match[1][0];
      if (fence === null) fence = marker;
      else if (fence === marker) fence = null;
      kept.push('');
      continue;
    }

    if (fence !== null) {
      kept.push('');
      continue;
    }

    kept.push(line.replace(/`[^`]*`/g, ''));
  }

  return kept;
};

const rules = [
  { name: 'inline <script> block', regex: /<script\b(?![^>]*\bsrc\s*=)[^>]*>/i },
  { name: 'inline event handler', regex: /\son(?:click|change|input|load|error|submit|focus|blur|keydown|keyup|keypress|mouseover|mouseout|mouseenter|mouseleave|touchstart|touchend)\s*=/i },
  { name: 'javascript: URL', regex: /(?:href|src)\s*=\s*["']\s*javascript\s*:/i }
];

for (const file of await walk(ROOT)) {
  const text = await readFile(file, 'utf8');
  const lines = extname(file).toLowerCase() === '.md' ? stripMarkdownCode(text) : text.split(/\r?\n/);

  lines.forEach((line, index) => {
    for (const rule of rules) {
      if (rule.regex.test(line)) {
        violations.push({
          file: relative('.', file).replaceAll('\\', '/'),
          line: index + 1,
          rule: rule.name,
          sample: line.trim().slice(0, 180)
        });
      }
    }
  });
}

if (violations.length > 0) {
  console.error(`Inline portal JavaScript gate FAILED: ${violations.length} violation(s).`);
  for (const item of violations) {
    console.error(`${item.file}:${item.line} [${item.rule}] ${item.sample}`);
  }
  console.error('Move executable page behavior into docs/javascripts modules loaded by MkDocs.');
  process.exit(1);
}

console.log('Inline portal JavaScript gate PASS: no executable inline JavaScript found in docs Markdown/HTML pages.');
