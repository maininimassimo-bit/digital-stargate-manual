(() => {
  const host = document.querySelector('[data-session-comparison]');
  if (!host) return;

  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const list = (title, values) => `<details><summary>${esc(title)}</summary><code>${(values || []).map(esc).join('<br>')}</code></details>`;
  const fail = message => { host.innerHTML = `<section class="dsg-sc-panel dsg-sc-fail"><h2>Comparison projection non disponibile</h2><p>${esc(message || 'Fail-closed: nessun confronto viene inferito dal browser.')}</p></section>`; };

  const validate = data => {
    if (!data || data.projectionType !== 'SESSION_COMPARISON_PROJECTION') throw new Error('projection type non valido');
    if (data.consumerMode !== 'READ_ONLY') throw new Error('consumer mode non read-only');
    if (data.authority?.acceptanceAuthority !== false || data.authority?.actionAuthority !== 'NONE') throw new Error('authority drift');
    if (!Array.isArray(data.includedSessions) || !Array.isArray(data.exclusions) || !Array.isArray(data.limitations)) throw new Error('projection incompleta');
    if (!data.limitations.includes('NO_RANKING_OR_QUALITY_SCORE') || !data.limitations.includes('NO_SAFETY_OR_ACTION_AUTHORITY')) throw new Error('authority limitations mancanti');
  };

  const session = item => `<article class="dsg-sc-record"><div><strong>${esc(item.sessionId)}</strong><small>${esc(item.quality)} · ${esc(item.completeness)}</small></div><p class="dsg-sc-value">${esc(item.value)} ${esc(item.unit)}</p><p>Provenance: <code>${esc(item.provenanceRef)}</code></p></article>`;
  const exclusion = item => `<article class="dsg-sc-record dsg-sc-excluded"><div><strong>${esc(item.sessionId)}</strong><small>EXCLUDED</small></div><p>${esc(item.reason)}</p><p>Class: <code>${esc(item.comparabilityClass)}</code></p></article>`;
  const summary = s => s ? `<section class="dsg-sc-kpis"><article><span>SAMPLE</span><strong>${esc(s.sampleSize)}</strong></article><article><span>MIN</span><strong>${esc(s.minimum)}</strong></article><article><span>MAX</span><strong>${esc(s.maximum)}</strong></article><article><span>MEAN</span><strong>${esc(s.mean)}</strong></article><article><span>MEDIAN</span><strong>${esc(s.median)}</strong></article><article><span>RANGE</span><strong>${esc(s.range)}</strong></article></section>` : '<section class="dsg-sc-panel"><h2>Nessuna aggregazione numerica</h2><p>La projection non dispone di una cohort numerica comparabile sufficiente.</p></section>';

  fetch('../data/session-comparison-projection.json', { cache: 'no-store' })
    .then(response => { if (!response.ok) throw new Error('projection repository assente'); return response.json(); })
    .then(data => {
      validate(data);
      host.innerHTML = `${summary(data.descriptiveSummary)}<section class="dsg-sc-panel"><span>COMPARISON SET</span><h2>${esc(data.dimension)} · ${esc(data.unit)}</h2><p>State: <strong>${esc(data.comparisonState)}</strong> · Projection: <code>${esc(data.projectionId)}</code></p><h3>Sessioni incluse</h3><div class="dsg-sc-records">${data.includedSessions.map(session).join('') || '<p>Nessuna sessione inclusa.</p>'}</div><h3>Exclusions</h3><div class="dsg-sc-records">${data.exclusions.map(exclusion).join('') || '<p>Nessuna exclusion.</p>'}</div>${list('Limitations',data.limitations)}${list('Source refs',data.lineage?.sourceRefs)}</section>`;
    })
    .catch(error => fail(error.message));
})();
