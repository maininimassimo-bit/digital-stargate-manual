(() => {
  const host = document.querySelector('[data-anomaly-trend-center]');
  if (!host) return;
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const refs = (title, values) => `<details><summary>${esc(title)}</summary><code>${(values || []).map(esc).join('<br>')}</code></details>`;
  const record = r => `<article class="dsg-at-record"><div><strong>${esc(r.semantic_type)}</strong><small>${esc(r.quality_state)}</small></div><code>${esc(r.derived_record_id)}</code><p>${r.measurement ? `${esc(r.measurement.value)} ${esc(r.measurement.unit)} · descriptive only` : 'Source-backed observation'}</p><p>${esc(r.analysis_window.start_utc)} → ${esc(r.analysis_window.end_utc)}</p>${refs('Source records',r.source_record_refs)}${refs('Citation',r.citation_refs)}${refs('Provenance',r.provenance_refs)}</article>`;
  const fail = () => { host.innerHTML = '<section class="dsg-at-panel dsg-at-fail"><h2>Projection non disponibile</h2><p>Fail-closed: nessuno stato analitico viene inferito dal browser.</p></section>'; };
  fetch('../data/anomaly-trend-read-model.json', { cache: 'no-store' })
    .then(r => { if (!r.ok) throw new Error('projection unavailable'); return r.json(); })
    .then(data => {
      if (data.authority !== 'projection' || data.action_authority !== 'NONE' || data.interaction_mode !== 'READ_ONLY' || data.advisory_mode !== 'DESCRIPTIVE_ONLY' || !Array.isArray(data.command_actions) || data.command_actions.length) throw new Error('authority drift');
      host.innerHTML = `<section class="dsg-at-kpis"><article><span>RECORDS</span><strong>${esc(data.summary.total_records)}</strong></article><article><span>OBSERVATIONS</span><strong>${esc(data.summary.observations)}</strong></article><article><span>TRENDS</span><strong>${esc(data.summary.trend_measurements)}</strong></article><article><span>ANOMALY CANDIDATES</span><strong>${esc(data.summary.anomaly_candidates)}</strong></article></section><section class="dsg-at-panel"><span>SESSION</span><h2>${esc(data.session_id)}</h2><p>Authority: ${esc(data.authority)} · Mode: ${esc(data.interaction_mode)} · Advisory: ${esc(data.advisory_mode)}</p><div class="dsg-at-records">${data.records.map(record).join('')}</div></section>`;
    }).catch(fail);
})();
