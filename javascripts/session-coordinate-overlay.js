(() => {
  'use strict';

  const formatCoordinate = (value, suffix) => {
    const number = Number(value);
    return Number.isFinite(number) ? `${number.toLocaleString('it-IT', { minimumFractionDigits: 4, maximumFractionDigits: 4 })}° ${suffix}` : 'Non disponibile';
  };

  const initialize = async () => {
    const root = document.querySelector('[data-session-detail]');
    const metadata = root?.querySelector('[data-detail-metadata]');
    const sessionId = new URLSearchParams(window.location.search).get('sessionId');
    if (!root || !metadata || !sessionId || metadata.dataset.coordinatesReady === 'true') return;

    let ra = null;
    let dec = null;
    let source = null;

    try {
      const catalogResponse = await fetch(new URL('../data/scientific-session-catalog.json', document.baseURI), { cache: 'no-store' });
      if (catalogResponse.ok) {
        const catalog = await catalogResponse.json();
        const session = catalog.sessions?.find(item => item.sessionId === sessionId);
        ra = session?.raDeg ?? session?.ra_deg ?? null;
        dec = session?.decDeg ?? session?.dec_deg ?? null;
        if (Number.isFinite(Number(ra)) && Number.isFinite(Number(dec))) source = 'scientific-session-catalog';
      }

      if (!source) {
        const latestResponse = await fetch(new URL('../data/realtime/latest-observation.json', document.baseURI), { cache: 'no-store' });
        if (latestResponse.ok) {
          const latest = await latestResponse.json();
          if (latest.session_id === sessionId) {
            ra = latest.target?.ra_deg ?? null;
            dec = latest.target?.dec_deg ?? null;
            source = latest.target?.coordinate_source || 'latest-observation';
          }
        }
      }
    } catch (error) {
      console.warn('Digital StarGate: session coordinates unavailable', error);
    }

    const article = (label, value) => `<article><span>${label}</span><strong>${value}</strong></article>`;
    metadata.insertAdjacentHTML('beforeend', article('RA (J2000)', formatCoordinate(ra, 'RA')) + article('DEC (J2000)', formatCoordinate(dec, 'DEC')) + article('Coordinate source', source || 'Non disponibile'));
    metadata.dataset.coordinatesReady = 'true';
  };

  const schedule = () => window.setTimeout(initialize, 0);
  if (window.document$?.subscribe) window.document$.subscribe(schedule);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', schedule, { once: true });
  else schedule();
})();
