import { validateProjectionFreshness, validateRealEvidenceFreshness } from './scientific-data-quality-core.mjs';

const host = document.querySelector('[data-scientific-data-quality]');

if (host) {
  const esc = value => String(value ?? '').replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]);
  const pct = value => Number.isFinite(value) ? `${Number(value).toLocaleString('it-IT', { maximumFractionDigits: 2 })}%` : '—';
  const number = value => Number.isFinite(value) ? Number(value).toLocaleString('it-IT', { maximumFractionDigits: 4 }) : '—';
  const date = value => {
    const parsed = new Date(value);
    return Number.isFinite(parsed.getTime()) ? parsed.toLocaleString('it-IT', { dateStyle: 'medium', timeStyle: 'short' }) : 'non disponibile';
  };
  const labels = { AVAILABLE: 'Disponibile', UNAVAILABLE: 'Non disponibile', INVALID: 'Fuori profilo' };
  const fail = message => {
    host.innerHTML = `<section class="dsg-dq-panel dsg-dq-fail" role="alert"><span>FAIL-CLOSED</span><h2>Quality projection non disponibile</h2><p>${esc(message || 'La verifica di freshness non è stata completata.')}</p><p>Nessuno score viene inferito o recuperato da dati precedenti.</p></section>`;
  };

  const bar = (label, value, suffix = '/ 100') => `<div class="dsg-dq-meter"><div><span>${esc(label)}</span><strong>${number(value)} ${esc(suffix)}</strong></div><div class="dsg-dq-meter__track"><i style="width:${Math.max(0, Math.min(100, Number(value) || 0))}%"></i></div></div>`;
  const dimension = item => `<tr><th scope="row">${esc(item.dimension)}</th><td>${esc(item.state)}</td><td>${number(item.rawValue)} ${esc(item.unit)}</td><td>${number(item.normalizedValue)}</td><td>${number(item.weight)}</td><td>${number(item.contribution)}</td><td>${esc(item.exclusionReason || '—')}</td></tr>`;
  const evidence = item => `<li><strong>${esc(item.dimension)}</strong><span>${number(item.value)} ${esc(item.unit)} · coverage ${pct((item.coverage ?? 0) * 100)}</span></li>`;

  const record = item => {
    const available = item.projectionRecordState === 'AVAILABLE';
    const assessment = item.assessment;
    const reasons = assessment?.decomposition?.filter(entry => entry.state !== 'AVAILABLE').map(entry => `${entry.dimension}: ${entry.exclusionReason}`) || [];
    if (item.generationError) reasons.push(`${item.generationError.code}: ${item.generationError.message}`);
    return `<article class="dsg-dq-record" data-state="${esc(item.projectionRecordState)}" data-search="${esc(`${item.sessionId} ${item.target}`.toLowerCase())}">
      <header><div><span>${esc(item.sessionId)}</span><h3>${esc(item.target)}</h3></div><span class="dsg-dq-state is-${esc(item.projectionRecordState.toLowerCase())}">${esc(labels[item.projectionRecordState] || item.projectionRecordState)}</span></header>
      ${available ? `<div class="dsg-dq-score-grid">${bar('Score sperimentale', assessment.score.value)}${bar('Confidence evidence', assessment.confidence.value)}${bar('Evidence coverage', assessment.evidenceCoverage * 100, '%')}</div>` : `<div class="dsg-dq-unavailable"><strong>Nessun valore aggregato pubblicabile</strong><p>${esc(reasons.join(' · ') || 'Evidence required non disponibile.')}</p></div>`}
      <div class="dsg-dq-meta"><span>Aggiornata: ${esc(date(item.observedAt))}</span><a href="../scientific-session-detail/?sessionId=${encodeURIComponent(item.sessionId)}">Apri sessione →</a></div>
      <details><summary>Evidence e spiegazione</summary>
        <ul class="dsg-dq-evidence">${item.inputEvidence.map(evidence).join('') || '<li>Nessuna evidence eleggibile.</li>'}</ul>
        ${assessment ? `<div class="dsg-dq-table-wrap"><table><thead><tr><th>Dimensione</th><th>Stato</th><th>Raw</th><th>Normalizzato</th><th>Peso</th><th>Contributo</th><th>Esclusione</th></tr></thead><tbody>${assessment.decomposition.map(dimension).join('')}</tbody></table></div>` : ''}
        <p class="dsg-dq-source">Source: <code>${esc(item.sourceMetricsPath || 'UNAVAILABLE')}</code></p>
      </details>
    </article>`;
  };

  const render = (projection, validation) => {
    const items = [...projection.assessments].reverse();
    host.innerHTML = `<section class="dsg-dq-kpis" aria-label="Riepilogo quality projection">
      <article><span>SESSIONI</span><strong>${projection.summary.totalSessions}</strong></article>
      <article><span>SCORE DISPONIBILI</span><strong>${projection.summary.availableAssessments}</strong></article>
      <article><span>UNAVAILABLE</span><strong>${projection.summary.unavailableAssessments}</strong></article>
      <article><span>FUORI PROFILO</span><strong>${projection.summary.invalidAssessments}</strong></article>
    </section>
    <section class="dsg-dq-panel dsg-dq-validation"><div><span>F5 · REAL-EVIDENCE VALIDATION</span><h2>Capability sperimentale accettata · uso produttivo non pronto</h2><p>La cohort include tutte le ${validation.cohort.sessionCount} sessioni canoniche senza outcome filtering. ${validation.summary.failedCriteria}/${validation.summary.totalCriteria} gate di readiness produttiva non sono soddisfatti: nessun profilo produttivo è autorizzato.</p></div><span class="dsg-dq-state is-unavailable">${esc(validation.decision.productionReadiness)}</span></section>
    <section class="dsg-dq-panel dsg-dq-fresh"><div><span>FRESHNESS VERIFIED</span><h2>Projection allineata al catalogo</h2><p>Generata ${esc(date(projection.generatedAt))} · profilo <code>${esc(projection.profile.profileVersion)}</code> · digest <code>${esc(projection.projectionDigest.slice(0, 12))}…</code></p></div><span class="dsg-dq-fresh__badge">SHA-256 ✓</span></section>
    <section class="dsg-dq-panel"><div class="dsg-dq-toolbar"><div><label for="dq-search">Cerca sessione o target</label><input id="dq-search" type="search" placeholder="es. M 27 o 2026-09"></div><div><label for="dq-filter">Stato</label><select id="dq-filter"><option value="ALL">Tutti</option><option value="AVAILABLE">Disponibile</option><option value="UNAVAILABLE">Non disponibile</option><option value="INVALID">Fuori profilo</option></select></div></div><p class="dsg-dq-result" data-dq-result></p><div class="dsg-dq-records">${items.map(record).join('')}</div></section>`;

    const search = host.querySelector('#dq-search');
    const filter = host.querySelector('#dq-filter');
    const result = host.querySelector('[data-dq-result]');
    const apply = () => {
      const query = search.value.trim().toLowerCase();
      let visible = 0;
      host.querySelectorAll('.dsg-dq-record').forEach(card => {
        const show = (!query || card.dataset.search.includes(query)) && (filter.value === 'ALL' || card.dataset.state === filter.value);
        card.hidden = !show;
        if (show) visible += 1;
      });
      result.textContent = `${visible} sessioni visualizzate`;
    };
    search.addEventListener('input', apply);
    filter.addEventListener('change', apply);
    apply();
  };

  Promise.all([
    fetch('../data/scientific-data-quality-projection.json', { cache: 'no-store' }),
    fetch('../data/scientific-session-catalog.json', { cache: 'no-store' }),
    fetch('../data/scientific-data-quality-f5-validation.json', { cache: 'no-store' })
  ]).then(async ([projectionResponse, catalogResponse, validationResponse]) => {
    if (!projectionResponse.ok || !catalogResponse.ok || !validationResponse.ok) throw new Error('Projection, catalogo o validation report repository assente.');
    const [projection, catalog, validation] = await Promise.all([projectionResponse.json(), catalogResponse.json(), validationResponse.json()]);
    await validateProjectionFreshness(projection, catalog);
    await validateRealEvidenceFreshness(validation, projection, catalog);
    render(projection, validation);
  }).catch(error => fail(error.message));
}
