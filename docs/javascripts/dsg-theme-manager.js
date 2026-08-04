(() => {
  'use strict';

  const CONTROL_SELECTOR = '[data-dsg-theme]';
  const PALETTE_SELECTOR = '[data-md-component="palette"] input[name="__palette"]';

  let listenersBound = false;

  const getPaletteInputs = () => [...document.querySelectorAll(PALETTE_SELECTOR)];

  const getActiveInput = () => {
    const inputs = getPaletteInputs();
    return inputs.find((input) => input.checked)
      || inputs.find((input) => input.dataset.mdColorScheme === document.body?.dataset.mdColorScheme)
      || inputs[0]
      || null;
  };

  const getNextInput = (activeInput) => {
    const inputs = getPaletteInputs();
    if (!inputs.length) return null;

    const currentIndex = Math.max(0, inputs.indexOf(activeInput));
    return inputs[(currentIndex + 1) % inputs.length];
  };

  const getThemeName = (input) => {
    if (!input) return 'unknown';
    if (input.dataset.mdColorScheme === 'slate') return 'dark';
    if (input.dataset.mdColorScheme === 'default') return 'light';
    return input.dataset.mdColorScheme || 'unknown';
  };

  const updateControls = () => {
    const activeInput = getActiveInput();
    const nextInput = getNextInput(activeInput);
    const currentTheme = getThemeName(activeInput);
    const action = nextInput?.getAttribute('aria-label') || 'Cambia tema';
    const icon = currentTheme === 'dark' ? '☀' : '☾';

    document.querySelectorAll(CONTROL_SELECTOR).forEach((control) => {
      control.textContent = `${icon} ${action.replace(/^Passa alla /, '').replace(/^Attiva /, '')}`;
      control.setAttribute('aria-label', action);
      control.setAttribute('title', action);
      control.setAttribute('aria-pressed', String(currentTheme === 'dark'));
      control.dataset.dsgThemeCurrent = currentTheme;
      control.dataset.dsgThemeNext = getThemeName(nextInput);
    });
  };

  const emitThemeChange = (theme) => {
    const detail = { theme, source: 'enterprise-control' };
    if (window.DSG?.events) {
      window.DSG.events.emit('theme-change', detail);
      return;
    }
    document.dispatchEvent(new CustomEvent('dsg:theme-change', { detail }));
  };

  const toggleTheme = () => {
    const activeInput = getActiveInput();
    const nextInput = getNextInput(activeInput);
    if (!nextInput) return;

    nextInput.click();
    window.requestAnimationFrame(() => {
      updateControls();
      emitThemeChange(getThemeName(getActiveInput()));
    });
  };

  const bindListeners = () => {
    if (listenersBound) return;
    listenersBound = true;

    document.addEventListener('click', (event) => {
      if (event.target.closest(CONTROL_SELECTOR)) toggleTheme();
    });

    document.addEventListener('change', (event) => {
      if (!event.target.matches(PALETTE_SELECTOR)) return;
      window.requestAnimationFrame(updateControls);
    });
  };

  const initialize = () => {
    bindListeners();
    updateControls();
  };

  if (window.DSG?.components) {
    window.DSG.components.register({
      name: 'theme-adapter',
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
