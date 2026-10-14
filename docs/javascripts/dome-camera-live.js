/* Public media only. Private RTSP credentials and camera controls never enter the portal. */
(() => {
  'use strict';
  const base = 'https://digitalstargate.freeddns.it:23232/dome-camera/';
  const metadataUrl = base + 'status.json';
  let current, dispose = () => {};

  async function readStatus(signal) {
    const controller = new AbortController();
    const abort = () => controller.abort();
    signal.addEventListener('abort', abort, {once:true});
    if (signal.aborted) abort();
    const timer = setTimeout(abort, 3000);
    let reader;
    try {
      const response = await fetch(metadataUrl, {signal:controller.signal, cache:'no-store',
        credentials:'omit', redirect:'error'});
      if (!response.ok || response.url !== metadataUrl || !response.body) throw Error('CAMERA_UNAVAILABLE');
      reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8', {fatal:true});
      let raw = '', bytes = 0;
      while (true) {
        const part = await reader.read();
        if (part.done) break;
        bytes += part.value.byteLength;
        if (bytes > 4096) throw Error('CAMERA_UNAVAILABLE');
        raw += decoder.decode(part.value, {stream:true});
      }
      raw += decoder.decode();
      const value = JSON.parse(raw), now = Date.now();
      if (value?.schemaVersion !== '1.0' || value.kind !== 'DSG_DOME_CAMERA_PUBLIC_V1'
          || !['CURRENT','UNAVAILABLE'].includes(value.state) || value.commandAuthority !== false
          || value.safetyAuthority !== false || value.audio !== false
          || value.frameUrl !== base + 'frame.jpg' || value.streamUrl !== base + 'live.mjpg'
          || !Number.isSafeInteger(value.sequence) || value.sequence < 0) throw Error('CAMERA_UNAVAILABLE');
      if (value.state === 'CURRENT') {
        const received = Date.parse(value.receivedAt), until = Date.parse(value.freshUntil);
        if (!Number.isFinite(received) || !Number.isFinite(until) || received > now + 5000
            || until <= now || until - received !== 8000) throw Error('CAMERA_UNAVAILABLE');
      } else if (value.receivedAt !== null || value.freshUntil !== null) throw Error('CAMERA_UNAVAILABLE');
      if (controller.signal.aborted) throw Error('CAMERA_UNAVAILABLE');
      return value;
    } finally {
      clearTimeout(timer);
      signal.removeEventListener('abort', abort);
      if (reader) { await reader.cancel().catch(() => {}); reader.releaseLock(); }
    }
  }

  function initialize() {
    const stage = document.querySelector('[data-dsg-dome-camera]');
    if (stage === current) return;
    dispose(); current = stage;
    if (!stage) return;
    const controller = new AbortController(), {signal} = controller;
    const panel = stage.querySelector('[data-dsg-camera-panel]');
    const note = stage.querySelector('[data-dsg-camera-note]');
    const status = stage.querySelector('.dsg-scene__status');
    const views = stage.querySelector('.dsg-scene__views');
    const mode = stage.querySelector('[data-dsg-scene-mode]');
    let image = stage.querySelector('[data-dsg-camera-image]');
    let selected = false, timer, deadline, request, pending = false, epoch = 0, retryAt = 0;
    let last = null;
    const essential = () => {
      try { return localStorage.getItem('dsg-immersive-essential') === 'true'; } catch { return false; }
    };
    const automaticPaused = () => stage.dataset.dsgViewMode === 'auto'
      && (matchMedia('(prefers-reduced-motion: reduce)').matches || navigator.connection?.saveData);
    const active = () => selected && !essential() && !automaticPaused() && !document.hidden
      && stage.isConnected && !signal.aborted;
    const message = text => { note.textContent = text; if (selected) status.textContent = text; };
    const clearImage = () => {
      clearTimeout(deadline); deadline = null;
      image.hidden = true; image.removeAttribute('src');
      stage.dataset.dsgCameraState = 'unavailable';
    };
    const stop = () => {
      epoch++; clearTimeout(timer); clearTimeout(deadline); request?.abort(); request = null;
      pending = false; last = null; clearImage();
      if (selected) { note.hidden = false; message('Collegamento alla TVCC interna…'); }
    };
    const schedule = () => {
      clearTimeout(timer);
      if (active()) timer = setTimeout(refresh, 2000);
    };
    const ready = () => {
      if (!active() || !last || Date.parse(last.freshUntil) <= Date.now() || !image.naturalWidth) return;
      image.hidden = false; stage.dataset.dsgCameraState = 'ready';
      note.hidden = true;
      const time = new Date(last.receivedAt).toLocaleTimeString('it-IT');
      status.textContent = `TVCC interna · ripresa live senza audio · ricevuta dal ponte alle ${time}`;
    };
    function stream() {
      if (!active() || image.hasAttribute('src') || Date.now() < retryAt) return;
      const next = image.cloneNode(false), ticket = epoch;
      image.replaceWith(next); image = next;
      image.hidden = true; note.hidden = false;
      stage.dataset.dsgCameraState = 'pending';
      message('Collegamento alla TVCC interna…');
      image.addEventListener('load', () => { if (ticket === epoch) ready(); }, {signal});
      image.addEventListener('error', () => {
        if (ticket !== epoch || !active()) return;
        retryAt = Date.now() + 4000; clearImage(); note.hidden = false;
        message('Ripresa TVCC non disponibile · nuovo tentativo automatico');
      }, {signal});
      image.src = base + 'live.mjpg?view=' + Date.now();
    }
    async function refresh() {
      if (!active() || pending) return;
      pending = true; const ticket = epoch;
      request = new AbortController();
      try {
        const value = await readStatus(request.signal);
        if (ticket !== epoch || !active()) return;
        if (value.state !== 'CURRENT') throw Error('CAMERA_UNAVAILABLE');
        last = value;
        clearTimeout(deadline);
        deadline = setTimeout(() => {
          last = null; clearImage(); note.hidden = false;
          message('Ripresa TVCC scaduta · nessuna immagine corrente disponibile');
        }, Math.max(0, Date.parse(value.freshUntil) - Date.now()));
        stream(); ready();
      } catch {
        if (ticket !== epoch || !active()) return;
        last = null; clearImage(); note.hidden = false;
        message('TVCC non disponibile · riprovo automaticamente');
      } finally {
        if (ticket === epoch) { pending = false; request = null; schedule(); }
      }
    }
    const fit = () => {
      const heading = stage.querySelector('.dsg-scene__heading'), toolbar = stage.querySelector('.dsg-scene__toolbar');
      const top = heading.offsetTop + heading.offsetHeight + 12;
      panel.style.top = `${top}px`;
      panel.style.height = `${Math.max(1, toolbar.offsetTop - top - 12)}px`;
    };
    function sync() {
      const next = stage.dataset.dsgSelectedView === 'section';
      const changed = selected !== next;
      selected = next;
      stage.dataset.dsgCameraSelected = String(selected);
      panel.hidden = !selected;
      stage.setAttribute('aria-label', selected ? 'Ripresa pubblica TVCC interna della cupola' : 'Visualizzazione tridimensionale illustrativa');
      views.hidden = false;
      if (!selected) {
        if (changed) stop();
        mode.textContent = essential() ? 'Attiva il 3D' : 'Vista essenziale';
        if (changed && stage.dataset.dsgSceneState !== 'ready') {
          status.textContent = essential() ? 'Vista essenziale · rendering sospeso' : 'Vista 3D non disponibile · informazioni invariate';
        }
        return;
      }
      fit();
      mode.textContent = essential() ? 'Attiva ripresa' : 'Vista essenziale';
      if (!active()) {
        stop(); note.hidden = false;
        message(essential() ? 'Vista essenziale · ripresa TVCC sospesa' : document.hidden
          ? 'Ripresa TVCC sospesa mentre la pagina è nascosta'
          : 'Ripresa automatica sospesa per la preferenza di movimento o risparmio dati · seleziona Interno');
        return;
      }
      if (changed) stop();
      refresh();
    }
    const choose = (view, following) => {
      stage.dataset.dsgViewMode = following ? 'auto' : 'manual';
      stage.dataset.dsgSelectedView = view;
      stage.querySelector('[data-dsg-follow-dome]').setAttribute('aria-pressed', String(following));
      stage.querySelectorAll('[data-dsg-scene-view]').forEach(button =>
        button.setAttribute('aria-pressed', String(button.dataset.dsgSceneView === view)));
      sync();
    };
    const observed = () => ({OPEN:'section', CLOSED:'exterior'})[stage.dataset.dsgObservedDome] || 'neutral';
    stage.addEventListener('click', event => {
      const button = event.target.closest('[data-dsg-scene-view]');
      if (button) choose(button.dataset.dsgSceneView, false);
      if (event.target.closest('[data-dsg-follow-dome]')) choose(observed(), true);
    }, {signal});
    mode.addEventListener('click', () => queueMicrotask(sync), {signal});
    const observer = new MutationObserver(records => {
      if (records.some(record => record.attributeName === 'data-dsg-observed-dome')
          && stage.dataset.dsgViewMode === 'auto') choose(observed(), true);
      else sync();
    });
    observer.observe(stage, {attributes:true, attributeFilter:['data-dsg-selected-view','data-dsg-view-mode','data-dsg-observed-dome']});
    const size = new ResizeObserver(fit); size.observe(stage);
    size.observe(stage.querySelector('.dsg-scene__heading')); size.observe(stage.querySelector('.dsg-scene__toolbar'));
    document.addEventListener('visibilitychange', () => { stop(); sync(); }, {signal});
    window.addEventListener('dsg:visual-mode-change', sync, {signal});
    stage.dataset.dsgViewMode ||= 'auto'; stage.dataset.dsgSelectedView ||= observed();
    sync();
    dispose = () => { stop(); controller.abort(); observer.disconnect(); size.disconnect(); };
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialize, {once:true}); else initialize();
  if (typeof document$ !== 'undefined') document$.subscribe(initialize);
  window.addEventListener('pagehide', event => { if (!event.persisted) dispose(); });
})();
