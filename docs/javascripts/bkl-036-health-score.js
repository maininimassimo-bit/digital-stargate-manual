(() => {
  const livePath = 'https://dsg-observatory-status-relay-cfjug35c6q-ew.a.run.app/v1/eagle-health';
  const archivedPath = new URL('../data/bkl-036-f3-health-score.json', document.baseURI);
  const text = value => value == null || value === '' ? '—' : String(value);
  const render = score => {
    const set = (key, value) => document.querySelectorAll(`[data-bkl036-score="${key}"]`).forEach(node => { node.textContent = value; });
    set('status', score.score_status === 'AVAILABLE' && score.score !== null ? `✅ ${score.score}/100` : '🟡 UNAVAILABLE');
    set('timestamp', text(score.evaluated_at_utc));
    set('source', score.publication?.label || score.publication?.non_live_label || 'repository evidence / non-live / non-real-time');
    set('reason', Array.isArray(score.reasons) ? score.reasons.join(' · ') : '—');
    set('domains', score.required_signals ? `${score.required_signals.current}/${score.required_signals.total} segnali obbligatori correnti` : `${score.evidence.filter(item => item.compatibility === 'COMPARABLE' && item.freshness_state === 'CURRENT').length}/7 comparabili e correnti`);
  };
  const fromLive = payload => {
    const summary = payload.summary || {};
    return {
      score_status: summary.state === 'HEALTHY' || summary.state === 'DEGRADED' ? 'AVAILABLE' : 'UNAVAILABLE',
      score: typeof summary.score === 'number' ? summary.score : null,
      evaluated_at_utc: payload.observed_at_utc,
      reasons: summary.reason ? [summary.reason] : ['LIVE_PROJECTION_UNAVAILABLE'],
      required_signals: { current: summary.state === 'HEALTHY' || summary.state === 'DEGRADED' ? 5 : 0, total: 5 },
      publication: { label: 'Cloud Run relay · EAGLE30154 · live read-only' }
    };
  };
  const init = () => {
    if (!document.querySelector('[data-bkl036-score]')) return;
    fetch(livePath, { cache: 'no-store' })
      .then(response => { if (!response.ok) throw new Error('BKL-036-F5 live score unavailable'); return response.json(); })
      .then(payload => render(fromLive(payload)))
      .catch(() => fetch(archivedPath)
        .then(response => { if (!response.ok) throw new Error('BKL-036-F3 score projection unavailable'); return response.json(); })
        .then(render)
        .catch(() => render({score_status:'UNAVAILABLE',score:null,reasons:['LIVE_AND_STATIC_PROJECTION_UNAVAILABLE'],publication:{non_live_label:'repository evidence / non-live / non-real-time'},evidence:[],evaluated_at_utc:null})));
  };
  if (window.document$?.subscribe) window.document$.subscribe(init); else if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, {once:true}); else init();
})();
