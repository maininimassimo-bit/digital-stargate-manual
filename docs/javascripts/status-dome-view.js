/* Read-only bridge from the displayed dome badge to a visual preset. No source requests. */
(() => {
  let current, dispose = () => {};
  function initialize() {
    const root = document.querySelector('.dsg-immersive-page[data-dsg-page="status/index.md"]');
    if (root === current) return;
    dispose(); current = root;
    if (!root) return;
    const badge = root.querySelector('[data-observatory-status="dome-state"]');
    const stage = root.querySelector('[data-dsg-dome-sync]');
    if (!badge || !stage) return;
    const update = () => {
      const match = badge.textContent.trim().match(/\b(OPEN|CLOSED)$/);
      const state = match ? match[1] : 'UNKNOWN';
      if (stage.dataset.dsgObservedDome !== state) stage.dataset.dsgObservedDome = state;
      const caption = stage.querySelector('.dsg-scene__caption');
      caption.textContent = state === 'UNKNOWN' ? `Cupola osservata: ${badge.textContent.trim() || 'UNKNOWN'} · vista neutra`
        : `Cupola osservata: ${state} · modello schematico`;
    };
    const observer = new MutationObserver(update); observer.observe(badge, { childList:true, characterData:true, subtree:true });
    update(); dispose = () => observer.disconnect();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialize, { once:true }); else initialize();
  if (typeof document$ !== 'undefined') document$.subscribe(initialize);
  window.addEventListener('pagehide', event => { if (!event.persisted) dispose(); });
})();
