/* Aggregate public coverage, with explicit catalog denominators and no RAW inference. */
(() => {
  'use strict';
  const known = value => typeof value === 'string' && value.trim() && !['UNKNOWN','N/A','NOT_REPRESENTED','MISSING','UNREGISTERED','UNAVAILABLE','NOT_AVAILABLE'].includes(value.trim().toUpperCase());
  const describe = (sessions, gallery, transfer) => {
    const total = sessions?.length || 0;
    const catalogRow = (label,predicate) => {
      if (!sessions) return {label,state:'partial',detail:'Catalogo corrente non verificabile'};
      const count = sessions.filter(predicate).length;
      return {label,state:count === total && total ? 'represented' : count ? 'partial' : 'missing',detail:`${count}/${total} sessioni nel catalogo corrente`};
    };
    const ids = new Set((sessions || []).map(s=>s.sessionId));
    const records = sessions && gallery ? gallery.records.filter(r=>r.associationEvidence==='OWNER_DECLARED' && r.sessionIds.some(id=>ids.has(id))) : null;
    const associated = new Set((records || []).flatMap(r=>r.sessionIds.filter(id=>ids.has(id)))).size;
    const unavailable = !sessions ? 'Catalogo corrente non verificabile: associazioni non calcolabili' : 'Gallery corrente non verificabile';
    const coverage = records ? `${records.length} versioni pubblicate · ${associated}/${total} sessioni · associazioni dichiarate dall’autore` : unavailable;
    const packages = sessions && transfer ? transfer.records.filter(r=>ids.has(r.sessionId) && r.state==='VERIFIED').length : null;
    return [
      catalogRow('Target',s=>known(s.target)),
      catalogRow('Sessione',s=>known(s.sessionId)),
      catalogRow('Equipment',s=>known(s.telescope) && known(s.camera) && known(s.filter)),
      catalogRow('Metrics',s=>s.evidenceState==='SOURCE_METRICS_AVAILABLE'),
      {label:'Scientific assets',state:'partial',detail:`${coverage}; inventario RAW fotografici non esposto`},
      catalogRow('Manifest · catalogo',s=>s.manifestState==='VERSIONED'),
      {label:'Transfer · pacchetto sessione',state:packages===null?'partial':packages===total&&total?'represented':packages?'partial':'missing',detail:packages===null?'Catalogo o proiezione dei pacchetti non verificabile':`${packages}/${total} pacchetti verificati SHA-256 · documenti e telemetria, non RAW fotografici`},
      {label:'Processing',state:records?.length?'partial':records?'missing':'partial',detail:records ? `${records.filter(r=>r.steps.length).length}/${records.length} versioni con passaggi disponibili · workflow parziali · esecuzione non verificata` : unavailable},
      {label:'Publication',state:records?.length?'represented':records?'missing':'partial',detail:coverage}
    ];
  };
  window.DSGMissionLineage = Object.freeze({describe});
})();
