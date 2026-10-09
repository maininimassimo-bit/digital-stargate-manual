/* Presentation-only bootstrap. No data fetch, evaluator or telemetry binding. */
(() => {
  'use strict';
  const moduleURL = new URL('./immersive-renderer.mjs', document.currentScript.src).href;
  const storageKey = 'dsg-immersive-essential';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let essential = false;
  try { essential = localStorage.getItem(storageKey) === 'true'; } catch { /* Private mode. */ }
  let currentRoot, dispose = () => {};

  function initialize() {
    const root = document.querySelector('.dsg-immersive-page');
    if (root === currentRoot) return;
    dispose(); currentRoot = root;
    if (!root) return;
    const controller = new AbortController();
    const { signal } = controller;
    const stage = root.querySelector('[data-dsg-scene]');
    if (!stage) { dispose = () => controller.abort(); return; }
    if (stage.hasAttribute('data-dsg-allsky-live')) { dispose = () => controller.abort(); return; }
    const mode = stage.querySelector('[data-dsg-scene-mode]');
    const status = stage.querySelector('.dsg-scene__status');
    const views = stage.querySelector('.dsg-scene__views');
    let stopScene = () => {}, epoch = 0, sceneController;
    const disabled = () => essential || reduced.matches || navigator.connection?.saveData;
    const reset = () => {
      epoch++; sceneController?.abort(); stopScene(); stopScene = () => {};
      stage.classList.remove('is-ready'); views.hidden = true;
      root.querySelector('.dsg-magnetic-reticle')?.setAttribute('hidden', '');
    };
    const updateMode = () => {
      mode.hidden = false;
      mode.setAttribute('aria-pressed', String(essential));
      mode.textContent = essential ? 'Attiva il 3D' : 'Vista essenziale';
      stage.dataset.dsgSceneState = disabled() ? 'essential' : 'pending';
      status.textContent = disabled()
        ? 'Vista essenziale · rendering sospeso'
        : 'Scena illustrativa · caricamento 3D';
    };
    async function mount() {
      if (disabled() || signal.aborted || stage.dataset.dsgSceneState === 'ready' || stage.dataset.dsgSceneState === 'loading') return;
      const ticket = ++epoch;
      const pendingController = new AbortController();
      sceneController = pendingController;
      stage.dataset.dsgSceneState = 'loading';
      try {
        const { mountScene } = await import(moduleURL);
        if (signal.aborted || ticket !== epoch || disabled() || !root.isConnected) return;
        const cleanup = await mountScene(stage, { signal: pendingController.signal });
        if (signal.aborted || ticket !== epoch || disabled()) { cleanup(); return; }
        stopScene = cleanup;
        stage.dataset.dsgSceneState = 'ready';
        stage.classList.add('is-ready'); views.hidden = false;
        if (!stage.hasAttribute('data-dsg-dome-sync')) status.textContent = 'Modello 3D illustrativo · controlli solo visuali';
      } catch (error) {
        if (signal.aborted || ticket !== epoch) return;
        reset(); stage.dataset.dsgSceneState = 'unavailable';
        status.textContent = '3D non disponibile · vista statica, dati invariati';
        console.warn('Digital StarGate: static visual fallback', error);
      }
    }
    const modeChanged = () => { reset(); updateMode(); mount(); };
    mode.addEventListener('click', () => {
      essential = !essential;
      try { localStorage.setItem(storageKey, String(essential)); } catch { /* Private mode. */ }
      modeChanged();
      window.dispatchEvent(new CustomEvent('dsg:visual-mode-change', { detail: { essential } }));
    }, { signal });
    window.addEventListener('dsg:visual-mode-change', event => {
      let value = essential;
      if (typeof event.detail?.essential === 'boolean') value = event.detail.essential;
      else try { value = localStorage.getItem(storageKey) === 'true'; } catch { /* Private mode. */ }
      if (value !== essential) { essential = value; modeChanged(); }
    }, { signal });
    reduced.addEventListener('change', modeChanged, { signal });
    navigator.connection?.addEventListener('change', modeChanged, { signal });
    // The native pointer remains visible; the decorative reticle has no hit target.
    const fine = matchMedia('(hover: hover) and (pointer: fine)');
    const reticle = document.createElement('span'); reticle.className = 'dsg-magnetic-reticle';
    reticle.hidden = true;
    reticle.setAttribute('aria-hidden', 'true'); root.append(reticle);
    root.addEventListener('pointermove', event => {
      if (disabled() || !fine.matches) { reticle.hidden = true; return; }
      const card = event.target.closest('.dsg-domain-card');
      reticle.hidden = !card;
      if (!card) return;
      const r = card.getBoundingClientRect();
      const x = event.clientX + (r.left + r.width / 2 - event.clientX) * .12;
      const y = event.clientY + (r.top + r.height / 2 - event.clientY) * .12;
      reticle.style.transform = `translate(${x}px, ${y}px) translate(-50%, -50%)`;
    }, { passive: true, signal });
    root.addEventListener('pointerleave', () => { reticle.hidden = true; }, { signal });
    window.addEventListener('scroll', () => { reticle.hidden = true; }, { passive: true, signal });
    updateMode();
    mount();
    dispose = () => { reset(); controller.abort(); reticle.remove(); };
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialize, { once: true });
  else initialize();
  if (typeof document$ !== 'undefined') document$.subscribe(initialize);
  window.addEventListener('pagehide', event => { if (!event.persisted) dispose(); });
})();
