import { readFile } from 'node:fs/promises';

const [mkdocs, enhancements, navigationStyles] = await Promise.all([
  readFile('mkdocs.yml', 'utf8'),
  readFile('docs/javascripts/page-enhancements.js', 'utf8'),
  readFile('docs/styles/enterprise-navigation.css', 'utf8')
]);

const checks = [
  ['MkDocs search plugin is enabled', /\n\s*- search:\s*\n/.test(mkdocs)],
  ['search toggle is opened explicitly', /toggle\.checked = true;/.test(enhancements)],
  ['search state is reflected on the body', /classList\.toggle\('dsg-search-open', open\)/.test(enhancements)],
  ['search UI is restored while open', /body\.dsg-search-open \.md-header__inner[\s\S]*?overflow: visible;/.test(navigationStyles)],
  ['legacy label click is absent', !/label\[for=["']__search["']\][\s\S]{0,40}\.click\(\)/.test(enhancements)]
];

const failures = checks.filter(([, passed]) => !passed).map(([label]) => label);
if (failures.length) {
  console.error(`Portal search contract failed:\n- ${failures.join('\n- ')}`);
  process.exit(1);
}

console.log(`Portal search contract passed (${checks.length} checks).`);
