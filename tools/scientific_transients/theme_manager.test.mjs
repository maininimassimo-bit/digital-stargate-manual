import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const source = readFileSync(new URL('../../docs/javascripts/dsg-theme-manager.js', import.meta.url), 'utf8');

function page({ darkSystem = true, storage = new Map(), materialSubscriber = true } = {}) {
  const handlers = new Map();
  const system = { matches: darkSystem, addEventListener: (_, fn) => { system.changed = fn; } };
  const root = { dataset: {} };
  const body = { dataset: { mdColorScheme: darkSystem ? 'slate' : 'default' } };
  const frames = [];
  const emit = (type, target) => { for (const fn of handlers.get(type) || []) fn({ target }); };
  const radios = ['default', 'slate'].map(scheme => ({
    dataset: { mdColorScheme: scheme },
    checked: body.dataset.mdColorScheme === scheme,
    matches: () => true,
    click() {
      for (const radio of radios) radio.checked = radio === this;
      if (materialSubscriber) body.dataset.mdColorScheme = scheme;
      emit('change', this);
    }
  }));
  const document = {
    documentElement: root, body, readyState: 'complete',
    currentScript: { src: 'https://example.test/javascripts/dsg-theme-manager.js' },
    getElementById: () => ({}),
    querySelectorAll: selector => selector.includes('__palette') ? radios : [],
    addEventListener(type, fn) { handlers.set(type, [...handlers.get(type) || [], fn]); },
    dispatchEvent() {}
  };
  const window = {
    matchMedia: () => system,
    localStorage: { getItem: key => storage.get(key), setItem: (key, value) => storage.set(key, value) },
    requestAnimationFrame: fn => frames.push(fn)
  };
  vm.runInNewContext(source, { document, window, URL, console, CustomEvent: class {} });
  const flush = () => { while (frames.length) frames.shift()(); };
  flush();
  return { root, body, storage, system, flush, service: window.DSGThemeService,
    select: scheme => { radios.find(r => r.dataset.mdColorScheme === scheme).click(); flush(); } };
}

test('Material light selection replaces a dark system theme in both theme layers', () => {
  const p = page();
  p.select('default');
  assert.equal(p.body.dataset.mdColorScheme, 'default');
  assert.equal(p.root.dataset.dsgThemeResolved, 'light');
  assert.equal(p.service.getTheme().preference, 'light');
  assert.equal(p.service.getTheme().materialTheme, 'light');
});

test('theme changes immediately without the Material subscriber in a local preview', () => {
  const p = page({ materialSubscriber: false });
  p.service.setTheme('light');
  assert.equal(p.body.dataset.mdColorScheme, 'default');
  assert.equal(p.root.dataset.dsgThemeResolved, 'light');
  p.service.setTheme('dark');
  assert.equal(p.body.dataset.mdColorScheme, 'slate');
  p.select('default');
  assert.equal(p.body.dataset.mdColorScheme, 'default');
  assert.equal(page({ storage: p.storage, materialSubscriber: false }).body.dataset.mdColorScheme, 'default');
});

test('explicit Material choice survives refresh and overrides the system preference', () => {
  const p = page();
  p.select('default');
  const refreshed = page({ storage: p.storage });
  assert.equal(refreshed.body.dataset.mdColorScheme, 'default');
  assert.equal(refreshed.root.dataset.dsgThemeResolved, 'light');
});

test('Material selection after an enterprise theme choice keeps both layers synchronized', () => {
  const p = page();
  p.service.setTheme('dark'); p.flush();
  p.select('default');
  assert.equal(p.service.getTheme().resolvedTheme, 'light');
  assert.equal(p.root.dataset.dsgThemePreference, 'light');
  assert.equal(p.root.dataset.dsgThemeResolved, 'light');
});

test('programmatic palette synchronization preserves system mode through OS changes', () => {
  const p = page({ darkSystem: false });
  p.system.matches = true; p.system.changed(); p.flush();
  assert.equal(p.body.dataset.mdColorScheme, 'slate');
  assert.equal(p.service.getTheme().preference, 'system');
  assert.equal(p.root.dataset.dsgThemeResolved, 'dark');
  p.system.matches = false; p.system.changed(); p.flush();
  assert.equal(p.body.dataset.mdColorScheme, 'default');
  assert.equal(p.service.getTheme().preference, 'system');
  assert.equal(p.root.dataset.dsgThemeResolved, 'light');
});
