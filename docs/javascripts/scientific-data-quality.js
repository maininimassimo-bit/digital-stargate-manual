import { evidenceCoverageView, validateProjectionFreshness, validateRealEvidenceFreshness } from './scientific-data-quality-core.mjs';
import { renderQualityTrend } from './scientific-quality-trend.mjs';

const host = document.querySelector('[data-scientific-data-quality]');

if (host) {
  let renderedKey = null;
  const esc = value => String(value ?? '').replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]);
  const pct = value => Number.isFinite(value) ? `${Number(value).toLocaleString('it-IT', { maximumFractionDigits: 2 })}%` : 'â€”';
  const number = value => Number.isFinite(value) ? Number(value).toLocaleString('it-IT', { maximumFractionDigits: 4 }) : 'â€”';
  const date = value => {
    const parsed = new Date(value);
    return Number.isFinite(parsed.getTime()) ? parsed.toLocaleString('it-IT', { dateStyle: 'medium', timeStyle: 'short' }) : 'non disponibile';
  };
  const labels = { AVAILABLE: 'Disponibile', UNAVAILABLE: 'Non disponibile', INVALID: 'Fuori profilo' };
  const fail = message => {
    renderedKey = null;
    const trend = document.querySelector('[data-quality-trend]');
    if (trend) trend.innerHTML = `<h2>Score nel tempo</h2><p role="alert">Grafico non disponibile: ${esc(message)}</p>`;
    host.innerHTML = `<section class="dsg-dq-panel dsg-dq-fail" role="alert"><span>FAIL-CLOSED</span><h2>Quality projection non disponibile</h2><p>${esc(message || 'La verifica di freshness non Ã¨ stata completata.')}</p><p>Nessuno score viene inferito o recuperato da dati precedenti.</p></section>`;
  };

  const bar = (label, value, suffix = '/ 100') => `<div class="dsg-dq-meter"><div><span>${esc(label)}</span><strong>${number(value)} ${esc(suffix)}</strong></div><div class="dsg-dq-meter__track"><i style="width:${Math.max(0, Math.min(100, Number(value) || 0))}%"></i></div></div>`;
  const dimension = item => `<tr><th scope="row">${esc(item.dimension)}</th><td>${esc(item.state)}</td><td>${number(item.rawValue)} ${esc(item.unit)}</td><td>${number(item.normalizedValue)}</td><td>${number(item.weight)}</td><td>${number(item.contribution)}</td><td>${esc(item.exclusionReason || 'â€”')}</td></tr>`;
  const evidence = (item, limitations) => {
    const coverage = evidenceCoverageView(item, limitations);
    const label = coverage.state === 'AVAILABLE' ? `coverage ${pct(coverage.value * 100)}`
      : coverage.reason === 'GUIDING_TEMPORAL_DENOMINATOR_MISSING' ? 'copertura temporale non disponibile' : 'copertura non disponibile';
    return `<li><strong>${esc(item.dimension)}</strong><span>${number(item.value)} ${esc(item.unit)} Â· ${esc(label)}</span></li>`;
  };

  const record = (item, limitations) => {
    const available = item.projectionRecordState === 'AVAILABLE';
    const assessment = item.assessment;
    const reasons = assessment?.decomposition?.filter(entry => entry.state !== 'AVAILABLE').map(entry => `${entry.dimension}: ${entry.exclusionReason}`) || [];
    if (item.generationError) reasons.push(`${item.generationError.code}: ${item.generationError.message}`);
    return `<article class="dsg-dq-record" data-state="${esc(item.projectionRecordState)}" data-search="${esc(`${item.sessionId} ${item.target}`.toLowerCase())}">
      <header><div><span>${esc(item.sessionId)}</span><h3>${esc(item.target)}</h3></div><span class="dsg-dq-state is-${esc(item.projectionRecordState.toLowerCase())}">${esc(labels[item.projectionRecordState] || item.projectionRecordState)}</span></header>
      ${available ? `<div class="dsg-dq-score-grid">${bar('Score sperimentale', assessment.score.value)}${bar('Confidence evidence', assessment.confidence.value)}${bar('Evidence coverage', assessment.evidenceCoverage * 100, '%')}</div>` : `<div class="dsg-dq-unavailable"><strong>Nessun valore aggregato pubblicabile</strong><p>${esc(reasons.join(' Â· ') || 'Evidence required non disponibile.')}</p></div>`}
      <div class="dsg-dq-meta"><span>Aggiornata: ${esc(date(item.observedAt))}</span><a href="../scientific-session-detail/?sessionId=${encodeURIComponent(item.sessionId)}">Apri sessione â†’</a></div>
      <details><summary>Evidence e spiegazione</summary>
        <ul class="dsg-dq-evidence">${item.inputEvidence.map(entry => evidence(entry, limitations)).join('') || '<li>Nessuna evidence eleggibile.</li>'}</ul>
        ${item.inputEvidence.some(entry => evidenceCoverageView(entry, limitations).reason === 'GUIDING_TEMPORAL_DENOMINATOR_MISSING') ? '<p class="dsg-dq-coverage-note">RMS di guida disponibile; copertura temporale non determinabile dal catalogo. Il numero di campioni validi non indica la frazione della notte coperta. Questa lacuna resta considerata nella confidence e nella copertura complessiva del modello sperimentale.</p>' : ''}
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
    <section class="dsg-dq-panel dsg-dq-validation"><div><span>F5 Â· REAL-EVIDENCE VALIDATION</span><h2>Capability sperimentale accettata Â· uso produttivo non pronto</h2><p>La cohort include tutte le ${validation.cohort.sessionCount} sessioni canoniche senza outcome filtering. ${validation.summary.failedCriteria}/${validation.summary.totalCriteria} gate di readiness produttiva non sono soddisfatti: nessun profilo produttivo Ã¨ autorizzato.</p></div><span class="dsg-dq-state is-unavailable">${esc(validation.decision.productionReadiness)}</span></section>
    <section class="dsg-dq-panel dsg-dq-fresh"><div><span>FRESHNESS VERIFIED</span><h2>Projection allineata al catalogo</h2><p>Generata ${esc(date(projection.generatedAt))} Â· profilo <code>${esc(projection.profile.profileVersion)}</code> Â· digest <code>${esc(projection.projectionDigest.slice(0, 12))}â€¦</code></p></div><span class="dsg-dq-fresh__badge">SHA-256 âœ“</span></section>
    <section class="dsg-dq-panel"><div class="dsg-dq-toolbar"><div><label for="dq-search">Cerca sessione o target</label><input id="dq-search" type="search" placeholder="es. M 27 o 2026-09"></div><div><label for="dq-filter">Stato</label><select id="dq-filter"><option value="ALL">Tutti</option><option value="AVAILABLE">Disponibile</option><option value="UNAVAILABLE">Non disponibile</option><option value="INVALID">Fuori profilo</option></select></div></div><p class="dsg-dq-result" data-dq-result></p><div class="dsg-dq-records">${items.map(item => record(item, projection.limitations)).join('')}</div></section>`;

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

  let loading = false;
  const refresh = () => {
  if (loading || !host.isConnected) return;
  loading = true;
  return Promise.all([
    fetch('../data/scientific-data-quality-projection.json', { cache: 'no-store' }),
    fetch('../data/scientific-session-catalog.json', { cache: 'no-store' }),
    fetch('../data/scientific-data-quality-f5-validation.json', { cache: 'no-store' })
  ]).then(async ([projectionResponse, catalogResponse, validationResponse]) => {
    if (!projectionResponse.ok || !catalogResponse.ok || !validationResponse.ok) throw new Error('Projection, catalogo o validation report repository assente.');
    const [projection, catalog, validation] = await Promise.all([projectionResponse.json(), catalogResponse.json(), validationResponse.json()]);
    await validateProjectionFreshness(projection, catalog);
    await validateRealEvidenceFreshness(validation, projection, catalog);
    const key = projection.projectionDigest + JSON.stringify(validation);
    if (key === renderedKey) return;
    render(projection, validation);
    const trend = document.querySelector('[data-quality-trend]');
    if (trend) renderQualityTrend(trend, projection, catalog);
    renderedKey = key;
  }).catch(error => fail(error.message)).finally(() => { loading = false; });
  };
  refresh();
  const timer = setInterval(() => {
    if (!host.isConnected) { clearInterval(timer); return; }
    if (!document.hidden) refresh();
  }, 300000);
}
