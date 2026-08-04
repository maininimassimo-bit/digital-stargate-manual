(() => {
  'use strict';

  const VERSION = '2.1.0-rc2';
  const STORAGE_KEY = 'dsg-theme-preference';
  const CONTROL_SELECTOR = '[data-dsg-theme]';
  const PALETTE_SELECTOR = '[data-md-component="palette"] input[name="__palette"]';
  const VALID_PREFERENCES = Object.freeze(['light', 'dark', 'system']);
  const SYSTEM_QUERY = '(prefers-color-scheme: dark)';
  const TOKEN_STYLESHEET_ID = 'dsg-theme-tokens';
  const SCRIPT_URL = document.currentScript?.src || null;

  let listenersBound = false;
  let systemListenerBound = false;
  let preference = 'system';
  const subscribers = new Set();
  const systemMedia = window.matchMedia(SYSTEM_QUERY);

  const ensureThemeTokens = () => {
    if (document.getElementById(TOKEN_STYLESHEET_ID)) return;

    const stylesheet = document.createElement('link');
    stylesheet.id = TOKEN_STYLESHEET_ID;
    stylesheet.rel = 'stylesheet';
    stylesheet.href = SCRIPT_URL
      ? new URL('../styles/theme-tokens.css', SCRIPT_URL).href
      : new URL('styles/theme-tokens.css', document.baseURI).href;
    stylesheet.dataset.dsgThemeAsset = 'tokens';
    document.head.appendChild(stylesheet);
  };

  const getPaletteInputs = () => [...document.querySelectorAll(PALETTE_SELECTOR)];

  const getInputForTheme = (theme) => getPaletteInputs().find((input) => {
    if (theme === 'dark') return input.dataset.mdColorScheme === 'slate';
    if (theme === 'light') return input.dataset.mdColorScheme === 'default';
    return false;
  }) || null;

  const getActiveInput = () => {
    const inputs = getPaletteInputs();
    return inputs.find((input) => input.checked)
      || inputs.find((input) => input.dataset.mdColorScheme === document.body?.dataset.mdColorScheme)
      || inputs[0]
      || null;
  };

  const themeFromInput = (input) => {
    if (!input) return 'unknown';
    if (input.dataset.mdColorScheme === 'slate') return 'dark';
    if (input.dataset.mdColorScheme === 'default') return 'light';
    return input.dataset.mdColorScheme || 'unknown';
  };

  const resolveTheme = (value = preference) => {
    if (value === 'system') return systemMedia.matches ? 'dark' : 'light';
    return value;
  };

  const readPreference = () => {
    try {
      const stored = window.localStorage.getItem(STORAGE_KEY);
      return VALID_PREFERENCES.includes(stored) ? stored : 'system';
    } catch {
      return 'system';
    }
  };

  const persistPreference = (value) => {
    try {
      window.localStorage.setItem(STORAGE_KEY, value);
    } catch {
      // Storage may be unavailable in privacy-restricted contexts.
    }
  };

  const state = () => Object.freeze({
    preference,
    resolvedTheme: resolveTheme(),
    materialTheme: themeFromInput(getActiveInput()),
    followsSystem: preference === 'system',
    version: VERSION
  });

  const publish = (source) => {
    const detail = Object.freeze({ ...state(), source });

    if (window.DSG?.events) {
      window.DSG.events.emit('theme-change', detail);
    } else {
      document.dispatchEvent(new CustomEvent('dsg:theme-change', { detail }));
    }

    subscribers.forEach((listener) => {
      try {
        listener(detail);
      } catch (error) {
        console.error('Digital StarGate theme subscriber failed', error);
      }
    });
  };

  const applyResolvedTheme = (source = 'theme-service') => {
    const resolvedTheme = resolveTheme();
    const targetInput = getInputForTheme(resolvedTheme);

    document.documentElement.dataset.dsgThemePreference = preference;
    document.documentElement.dataset.dsgThemeResolved = resolvedTheme;

    if (targetInput && !targetInput.checked) targetInput.click();

    window.requestAnimationFrame(() => {
      updateControls();
      publish(source);
    });
  };

  const setTheme = (value, options = {}) => {
    if (!VALID_PREFERENCES.includes(value)) {
      throw new TypeError(`Unsupported theme preference: ${value}`);
    }

    const changed = preference !== value;
    preference = value;
    if (options.persist !== false) persistPreference(value);
    applyResolvedTheme(options.source || (changed ? 'set-theme' : 'theme-refresh'));
    return state();
  };

  const cycleTheme = () => {
    const index = VALID_PREFERENCES.indexOf(preference);
    return setTheme(VALID_PREFERENCES[(index + 1) % VALID_PREFERENCES.length], {
      source: 'enterprise-control'
    });
  };

  const labels = Object.freeze({
    light: { icon: '☀', text: 'Tema chiaro', next: 'Passa al tema scuro' },
    dark: { icon: '☾', text: 'Tema scuro', next: 'Segui il tema di sistema' },
    system: { icon: '◐', text: 'Tema sistema', next: 'Passa al tema chiaro' }
  });

  function updateControls() {
    const current = labels[preference] || labels.system;
    const currentState = state();

    document.querySelectorAll(CONTROL_SELECTOR).forEach((control) => {
      control.textContent = `${current.icon} ${current.text}`;
      control.setAttribute('aria-label', current.next);
      control.setAttribute('title', `${current.text} · ${current.next}`);
      control.setAttribute('aria-pressed', String(currentState.resolvedTheme === 'dark'));
      control.dataset.dsgThemeCurrent = currentState.resolvedTheme;
      control.dataset.dsgThemePreference = currentState.preference;
      control.dataset.dsgThemeNext = VALID_PREFERENCES[(VALID_PREFERENCES.indexOf(preference) + 1) % VALID_PREFERENCES.length];
    });
  }

  const bindListeners = () => {
    if (!listenersBound) {
      listenersBound = true;

      document.addEventListener('click', (event) => {
        if (event.target.closest(CONTROL_SELECTOR)) cycleTheme();
      });

      document.addEventListener('change', (event) => {
        if (!event.target.matches(PALETTE_SELECTOR)) return;

        const materialTheme = themeFromInput(event.target);
        if (preference !== 'system' && VALID_PREFERENCES.includes(materialTheme)) {
          preference = materialTheme;
          persistPreference(preference);
        }

        window.requestAnimationFrame(() => {
          updateControls();
          publish('material-palette');
        });
      });
    }

    if (!systemListenerBound) {
      systemListenerBound = true;
      systemMedia.addEventListener('change', () => {
        if (preference === 'system') applyResolvedTheme('system-preference-change');
      });
    }
  };

  const onThemeChanged = (listener) => {
    if (typeof listener !== 'function') throw new TypeError('Theme listener must be a function');
    subscribers.add(listener);
    return () => subscribers.delete(listener);
  };

  const themeService = Object.freeze({
    version: VERSION,
    getTheme: () => state(),
    setTheme,
    toggleTheme: cycleTheme,
    onThemeChanged,
    refresh: () => applyResolvedTheme('manual-refresh')
  });

  window.DSGThemeService = themeService;

  const initialize = () => {
    ensureThemeTokens();
    bindListeners();
    preference = readPreference();
    applyResolvedTheme('initialize');
  };

  if (window.DSG?.components) {
    window.DSG.components.register({
      name: 'theme-service',
      order: 30,
      initialize
    });
    return;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize, { once: true });
  } else {
    initialize();
  }

  if (window.document$?.subscribe) window.document$.subscribe(initialize);
})();
