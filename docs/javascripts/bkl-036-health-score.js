(() => {
  const path = new URL('../data/bkl-036-f3-health-score.json', document.baseURI);
  const text = value => value == null || value === '' ? '—' : String(value);
  const render = score => {
    const set = (key, value) => document.querySelectorAll(`[data-bkl036-score="${key}"]`).forEach(node => { node.textContent = value; });
    set('status', score.score_status === 'AVAILABLE' && score.score !== null ? `✅ ${score.score}/100` : '🟡 UNAVAILABLE');
    set('timestamp', text(score.evaluated_at_utc));
    set('source', score.publication?.non_live_label || 'repository evidence / non-live / non-real-time');
    set('reason', Array.isArray(score.reasons) ? score.reasons.join(' · ') : '—');
    set('domains', `${score.evidence.filter(item => item.compatibility === 'COMPARABLE' && item.freshness_state === 'CURRENT').length}/7 comparabili e correnti`);
  };
  const init = () => {
    if (!document.querySelector('[data-bkl036-score]')) return;
    fetch(path).then(response => { if (!response.ok) throw new Error('BKL-036-F3 score projection unavailable'); return response.json(); }).then(render).catch(() => render({score_status:'UNAVAILABLE',score:null,reasons:['STATIC_PROJECTION_UNAVAILABLE'],publication:{non_live_label:'repository evidence / non-live / non-real-time'},evidence:[],evaluated_at_utc:null}));
  };
  if (window.document$?.subscribe) window.document$.subscribe(init); else if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, {once:true}); else init();
})();
