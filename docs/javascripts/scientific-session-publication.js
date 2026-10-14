/* Read-only associations from the validated public gallery, never inferred by target. */
(() => {
  'use strict';
  const select = (sessionId, collection) => collection.records.filter(record =>
    record.associationEvidence === 'OWNER_DECLARED' && record.sessionIds.includes(sessionId));
  const describe = (records, state = 'ready') => {
    if (state !== 'ready') {
      const detail = state === 'loading' ? 'Verifica della gallery in corso…' : 'Gallery non disponibile: stato non verificabile';
      return {processing: {state:'partial', detail}, publication: {state:'partial', detail}};
    }
    if (!records.length) return {
      processing: {state:'missing', detail:'Nessun workflow pubblico associato alla sessione'},
      publication: {state:'missing', detail:'Nessuna immagine attualmente pubblicata con questa sessione dichiarata'}
    };
    return {
      processing: {state:'partial', detail:records.map(r => `${r.workflowId}: ${r.steps.length} passaggi disponibili; workflow ${r.captureCompleteness === 'PARTIAL' ? 'parziale' : 'non disponibile'}; esecuzione non verificata`).join(' · ')},
      publication: {state:'represented', detail:records.map(r => `${r.title} · ${r.imageVersionId} · sessione dichiarata dall’autore`).join(' · ')}
    };
  };
  const galleryUrl = (base, sessionId, versionId) => {
    const url = new URL('scientific-image-gallery/', base);
    url.searchParams.set('sessionId', sessionId);
    url.hash = versionId;
    return url.href;
  };
  const metricsUrl = path => {
    if (typeof path !== 'string' || !/^data\/sessions\/\d{4}\/\d{2}\/[A-Za-z0-9_-]+\/normalized\/session-metrics\.json$/.test(path)) return null;
    return `https://github.com/maininimassimo-bit/digital-stargate-manual/blob/main/${path}`;
  };
  window.DSGSessionPublication = Object.freeze({select, describe, galleryUrl, metricsUrl});
})();
