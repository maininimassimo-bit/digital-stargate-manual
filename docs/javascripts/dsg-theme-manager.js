(() => {
  'use strict';

  const STORAGE_KEY = 'dsg.theme.preference';
  const THEMES = Object.freeze({
    light: Object.freeze({ scheme: 'default', icon: '☾', action: 'Attiva tema scuro' }),
    dark: Object.freeze({ scheme: 'slate', icon: '☀', action: 'Attiva tema chiaro' })
  });
  const MODES = new Set(['light', 'dark', 'system']);

  let currentTheme = null;
  let initialized = false;

  const getStoredPreference = () => {
    try {
      const preference = window.localStorage.getItem(STORAGE_KEY);
      return MODES.has(preference) ? preference : null;
    } catch {
      return null;
    }
  };

  const savePreference = (preference) => {
    if (!MODES.has(preference)) return;
    try {
      window.localStorage.setItem(STORAGE_KEY, preference);
    } catch {
      // Storage can be unavailable in private or restricted browser contexts.
    }
  };

  const detectSystemTheme = () =>
    window.matchMedia?.('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';

  const detectMaterialTheme = () => {
    const scheme = document.body?.getAttribute('data-md-color-scheme')
      || document.documentElement.getAttribute('data-md-color-scheme');

    if (scheme === THEMES.dark.scheme) return 'dark';
    if (scheme === THEMES.light.scheme) return 'light';

    const selectedPalette = document.querySelector(
      '[data-md-component="palette"] input[data-md-color-scheme]:checked'
    );

    if (selectedPalette?.dataset.mdColorScheme === THEMES.dark.scheme) return 'dark';
    if (selectedPalette?.dataset.mdColorScheme === THEMES.light.scheme) return 'light';

    return null;
  };

  const resolveTheme = (preference) => {
    if (preference === 'system') return detectSystemTheme();
    if (preference === 'light' || preference === 'dark') return preference;
    return detectMaterialTheme() || detectSystemTheme();
  };

  const getPaletteInput = (theme) => document.querySelector(
    `[data-md-component="palette"] input[data-md-color-scheme="${THEMES[theme].scheme}"]`
  );

  const updateControls = (theme) => {
    const nextTheme = theme === 'dark' ? 'light' : 'dark';
    const next = THEMES[theme];

    document.querySelectorAll('[data-dsg-theme]').forEach((control) => {
      control.textContent = `${next.icon} ${next.action.replace('Attiva ', '')}`;
      control.setAttribute('aria-label', next.action);
      control.setAttribute('title', next.action);
      control.setAttribute('aria-pressed', String(theme === 'dark'));
      control.dataset.dsgThemeCurrent = theme;
      control.dataset.dsgThemeNext = nextTheme;
    });
  };

  const dispatchThemeChange = (theme, source) => {
    document.dispatchEvent(new CustomEvent('dsg:theme-change', {
      detail: { theme, source }
    }));
  };

  const applyTheme = (theme, { persist = false, source = 'initialization' } = {}) => {
    if (!THEMES[theme]) return;

    const paletteInput = getPaletteInput(theme);
    if (paletteInput && !paletteInput.checked) {
      paletteInput.checked = true;
      paletteInput.dispatchEvent(new Event('input', { bubbles: true }));
      paletteInput.dispatchEvent(new Event('change', { bubbles: true }));
    }

    // Fallback and immediate synchronization for Material and custom components.
    document.body?.setAttribute('data-md-color-scheme', THEMES[theme].scheme);
    document.documentElement.setAttribute('data-dsg-theme', theme);

    currentTheme = theme;
    updateControls(theme);

    if (persist) savePreference(theme);
    dispatchThemeChange(theme, source);
  };

  const toggleTheme = () => {
    const activeTheme = detectMaterialTheme() || currentTheme || resolveTheme(getStoredPreference());
    applyTheme(activeTheme === 'dark' ? 'light' : 'dark', {
      persist: true,
      source: 'enterprise-control'
    });
  };

  const synchronizeFromMaterial = () => {
    const materialTheme = detectMaterialTheme();
    if (!materialTheme || materialTheme === currentTheme) return;
    currentTheme = materialTheme;
    updateControls(materialTheme);
    dispatchThemeChange(materialTheme, 'material-palette');
  };

  const initialize = () => {
    const preference = getStoredPreference();
    applyTheme(resolveTheme(preference), { source: 'initialization' });

    if (initialized) return;
    initialized = true;

    document.addEventListener('click', (event) => {
      if (event.target.closest('[data-dsg-theme]')) toggleTheme();
    });

    document.addEventListener('change', (event) => {
      if (event.target.matches('[data-md-component="palette"] input[data-md-color-scheme]')) {
        window.setTimeout(synchronizeFromMaterial, 0);
      }
    });

    window.matchMedia?.('(prefers-color-scheme: dark)').addEventListener('change', () => {
      if (getStoredPreference() === 'system') {
        applyTheme(detectSystemTheme(), { source: 'system-preference' });
      }
    });
  };

  document.addEventListener('DOMContentLoaded', initialize);
  if (typeof document$ !== 'undefined') document$.subscribe(initialize);
})();
