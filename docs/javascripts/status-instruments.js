/* Optional presentation enhancement; existing consumer owns all values and policy. */
(() => {
  const moduleURL = new URL('./immersive-instruments.mjs', document.currentScript.src).href;
  const key = 'dsg-immersive-essential';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let current, dispose = () => {};
  function initialize() {
    const root = document.querySelector('[data-observatory-domains]');
    if (root === current) return;
    dispose(); current = root;
    if (!root) return;
    const abort = new AbortController(), records = new Map();
    const button = document.querySelector('[data-instruments-mode]');
    let essential = false;
    try { essential = localStorage.getItem(key) === 'true'; } catch { /* Keep preference in memory. */ }
    const preference = () => essential;
    const disabled = () => preference() || reduced.matches || navigator.connection?.saveData;
    function updateLabel() { if (button) { button.hidden = false; button.textContent = preference() ? 'Attiva grafica 3D' : 'Vista essenziale'; button.setAttribute('aria-pressed', String(preference())); } }
    async function mount(panel, record) {
      if (record.started || disabled() || abort.signal.aborted) return;
      record.started = true;
      try {
        const { mountInstruments } = await import(moduleURL);
        if (record.abort.signal.aborted || !panel.isConnected || disabled()) return;
        record.cleanup = mountInstruments(panel, record.abort.signal);
      } catch (error) { panel.dataset.instrumentsState = 'unavailable'; console.warn('Digital StarGate: static instruments fallback', error); }
    }
    const intersection = new IntersectionObserver(entries => entries.forEach(entry => {
      const record = records.get(entry.target);
      if (record && entry.isIntersecting) mount(entry.target, record);
    }));
    function reconcile(reset = false) {
      for (const [panel, record] of records) if (reset || !root.contains(panel)) {
        record.abort.abort(); record.cleanup?.(); intersection.unobserve(panel); records.delete(panel);
      }
      root.querySelectorAll('.dsg-instrument-panel').forEach(panel => {
        if (records.has(panel)) return;
        const record = { abort: new AbortController(), started: false };
        records.set(panel, record); panel.dataset.instrumentsState = disabled() ? 'essential' : 'pending';
        if (!disabled()) intersection.observe(panel);
      });
      updateLabel();
    }
    // Observe only consumer replacement, not internal canvas/renderer changes.
    const observer = new MutationObserver(() => reconcile()); observer.observe(root, { childList: true });
    const modeChanged = event => {
      if (typeof event?.detail?.essential === 'boolean') essential = event.detail.essential;
      reconcile(true);
    };
    window.addEventListener('dsg:visual-mode-change', modeChanged, { signal: abort.signal });
    reduced.addEventListener('change', modeChanged, { signal: abort.signal });
    navigator.connection?.addEventListener('change', modeChanged, { signal: abort.signal });
    button?.addEventListener('click', () => {
      essential = !essential;
      try { localStorage.setItem(key, String(essential)); } catch { /* Keep preference in memory. */ }
      window.dispatchEvent(new CustomEvent('dsg:visual-mode-change', { detail: { essential } }));
    }, { signal: abort.signal });
    reconcile();
    dispose = () => { abort.abort(); observer.disconnect(); intersection.disconnect(); records.forEach(record => { record.abort.abort(); record.cleanup?.(); }); records.clear(); };
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialize, { once: true }); else initialize();
  if (typeof document$ !== 'undefined') document$.subscribe(initialize);
  window.addEventListener('pagehide', event => { if (!event.persisted) dispose(); });
})();
