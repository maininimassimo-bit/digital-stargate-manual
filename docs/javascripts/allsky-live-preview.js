/* Public image preview only: no credentials, commands or telemetry bindings. */
(() => {
  'use strict';
  const imageURL = 'https://digitalstargate.freeddns.it:23232/current/image.jpg';
  const key = 'dsg-immersive-essential';
  let currentStage, dispose = () => {};
  function initialize() {
    const stage = document.querySelector('[data-dsg-allsky-live]');
    if (stage === currentStage) return;
    dispose(); currentStage = stage;
    if (!stage) return;
    const controller = new AbortController(), { signal } = controller;
    const image = stage.querySelector('[data-dsg-allsky-image]');
    const mode = stage.querySelector('[data-dsg-scene-mode]');
    const status = stage.querySelector('.dsg-scene__status');
    let essential = false, timer, pending = false, lastReceived = '';
    try { essential = localStorage.getItem(key) === 'true'; } catch { /* Private mode. */ }
    const clear = () => { clearTimeout(timer); pending = false; };
    const schedule = () => { clearTimeout(timer); if (!essential && !document.hidden && !signal.aborted) timer = setTimeout(refresh, 30000); };
    function refresh() {
      if (essential || document.hidden || pending || signal.aborted) return;
      pending = true;
      image.src = `${imageURL}?preview=${Date.now()}`;
      timer = setTimeout(() => {
        if (!pending || signal.aborted) return;
        pending = false;
        stage.dataset.dsgSceneState = 'unavailable';
        status.textContent = 'Aggiornamento non disponibile · riprovo automaticamente';
        schedule();
      }, 15000);
    }
    function updateMode() {
      clear(); mode.hidden = false;
      mode.textContent = essential ? 'Attiva il live' : 'Vista essenziale';
      mode.setAttribute('aria-pressed', String(essential));
      stage.querySelector('.dsg-scene__views').hidden = false;
      if (essential) {
        stage.dataset.dsgSceneState = 'essential';
        status.textContent = 'Vista essenziale · aggiornamento sospeso';
      } else {
        stage.dataset.dsgSceneState = image.hidden ? 'pending' : 'ready';
        status.textContent = lastReceived ? `Ultima ricezione ${lastReceived} · aggiornamento ogni 30 s` : 'Collegamento alla ripresa Allsky…';
        refresh();
      }
    }
    image.addEventListener('load', () => {
      if (signal.aborted) return;
      clear(); image.hidden = false; stage.classList.add('is-ready');
      lastReceived = new Date().toLocaleTimeString('it-IT');
      if (essential) { updateMode(); return; }
      stage.dataset.dsgSceneState = 'ready';
      status.textContent = `Ultima ricezione ${lastReceived} · aggiornamento ogni 30 s`;
      schedule();
    }, { signal });
    image.addEventListener('error', () => {
      clear();
      if (essential) { updateMode(); return; }
      stage.dataset.dsgSceneState = 'unavailable';
      image.hidden = true; stage.classList.remove('is-ready');
      status.textContent = 'Ripresa non disponibile · apri Allsky o attendi il nuovo tentativo';
      schedule();
    }, { signal });
    mode.addEventListener('click', () => {
      essential = !essential;
      try { localStorage.setItem(key, String(essential)); } catch { /* Private mode. */ }
      updateMode();
      window.dispatchEvent(new CustomEvent('dsg:visual-mode-change', { detail: { essential } }));
    }, { signal });
    window.addEventListener('dsg:visual-mode-change', event => {
      if (typeof event.detail?.essential === 'boolean' && event.detail.essential !== essential) {
        essential = event.detail.essential; updateMode();
      }
    }, { signal });
    document.addEventListener('visibilitychange', () => { clear(); if (!document.hidden) refresh(); }, { signal });
    updateMode();
    dispose = () => { clear(); controller.abort(); image.removeAttribute('src'); };
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialize, { once: true });
  else initialize();
  if (typeof document$ !== 'undefined') document$.subscribe(initialize);
  window.addEventListener('pagehide', event => { if (!event.persisted) dispose(); });
})();
