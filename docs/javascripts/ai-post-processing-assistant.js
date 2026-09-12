import { validateAdvisoryProjectionFreshness } from './ai-post-processing-assistant-core.mjs';

const CORRELATION_LABELS = {
  PROVENANCE_MATCHED: 'Provenance correlata',
  PROVENANCE_UNAVAILABLE: 'Provenance non disponibile',
  CORRELATION_AMBIGUOUS: 'Correlazione ambigua',
  CORRELATION_INVALID: 'Correlazione non valida'
};

const RULE_LABELS = {
  GOVERNANCE_READINESS: 'Governance readiness',
  PROCESSING_HISTORY_AVAILABILITY: 'Processing history'
};

const esc = value => String(value ?? '').replace(/[&<>"']/g, char => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
})[char]);

const formatDate = value => {
  const parsed = new Date(value);
  return Number.isFinite(parsed.getTime())
    ? parsed.toLocaleString('it-IT', { dateStyle: 'medium', timeStyle: 'short' })
    : 'non disponibile';
};

const sourceHref = sourceRef => {
  const value = String(sourceRef ?? '');
  if (!value.startsWith('docs/') || value.includes('..') || value.includes('\\')) return null;
  return `../${value.slice(5)}`;
};

const sourceLink = sourceRef => {
  const href = sourceHref(sourceRef);
  return href
    ? `<a href="${esc(href)}"><code>${esc(sourceRef)}</code></a>`
    : `<code>${esc(sourceRef)}</code>`;
};

function failureMessage(error) {
  const code = String(error?.message || 'FRESHNESS_VERIFICATION_NOT_COMPLETED');
  if (code.includes('STALE_') || code.includes('SESSION_SET') || code.includes('SESSION_COUNT')) {
    return {
      title: 'Dati non allineati',
      detail: 'Catalogo e advisory projection non rappresentano la stessa baseline. Nessuna raccomandazione viene mostrata come corrente.'
    };
  }
  if (code.includes('WEB_CRYPTO')) {
    return {
      title: 'Verifica crittografica non disponibile',
      detail: 'Il browser non può verificare i digest SHA-256. Il consumer rimane indisponibile senza fallback permissivi.'
    };
  }
  return {
    title: 'Verifica fallita',
    detail: 'Identity, authority o digest della projection non hanno superato il controllo fail-closed.'
  };
}

function renderFailure(host, error) {
  const message = failureMessage(error);
  host.innerHTML = `<section class="dsg-ai-panel dsg-ai-failure" role="alert" aria-live="assertive">
    <span>VERIFICA FALLITA · FAIL-CLOSED</span>
    <h2>${esc(message.title)}</h2>
    <p>${esc(message.detail)}</p>
    <details><summary>Dettaglio diagnostico</summary><code>${esc(error?.message || 'Errore non classificato')}</code></details>
  </section>`;
}

const ruleMarkup = evaluation => `<li class="dsg-ai-rule is-${evaluation.decision === 'PASS' ? 'pass' : 'fail'}">
  <div><strong>${esc(RULE_LABELS[evaluation.ruleId] || evaluation.ruleId)}</strong><span>${esc(evaluation.decision)}</span></div>
  <p>${evaluation.reasonCodes.length ? esc(evaluation.reasonCodes.join(' · ')) : 'Nessun reason code.'}</p>
</li>`;

const recommendationMarkup = recommendation => `<article class="dsg-ai-recommendation" data-lifecycle="${esc(recommendation.lifecycleState)}">
  <header>
    <div><span>${esc(recommendation.category)}</span><h4>Indicazione deterministica</h4></div>
    <span class="dsg-ai-pill">${esc(recommendation.lifecycleState)}</span>
  </header>
  <p><strong>Azione proposta:</strong> ${esc(recommendation.proposedAction)}</p>
  <p><strong>Razionale:</strong> ${esc(recommendation.rationale)}</p>
  ${recommendation.unknowns.length ? `<p class="dsg-ai-unknown"><strong>Unknown:</strong> ${esc(recommendation.unknowns.join(' · '))}</p>` : ''}
  <p class="dsg-ai-muted">Confidence: ${esc(recommendation.confidence.state)} · nessun valore numerico calibrato.</p>
  <details><summary>Limitazioni</summary><ul>${recommendation.limitations.map(item => `<li>${esc(item)}</li>`).join('')}</ul></details>
</article>`;

function recordMarkup(record) {
  const citations = [...new Set(record.sourceBindings.flatMap(binding => binding.citationRefs || []))];
  const searchText = `${record.sessionId} ${record.target || ''} ${record.correlationState}`.toLowerCase();
  const statusClass = record.correlationState.toLowerCase().replaceAll('_', '-');
  return `<article class="dsg-ai-record" data-state="${esc(record.correlationState)}" data-search="${esc(searchText)}">
    <header>
      <div><span>${esc(record.sessionId)}</span><h3>${esc(record.target || 'Target non dichiarato')}</h3></div>
      <span class="dsg-ai-state is-${esc(statusClass)}">${esc(CORRELATION_LABELS[record.correlationState])}</span>
    </header>
    <ul class="dsg-ai-rules" aria-label="Esiti delle regole">${record.ruleEvaluations.map(ruleMarkup).join('')}</ul>
    <div class="dsg-ai-record__meta">
      <span>Decisione umana: <strong>non presente</strong></span>
      <a href="../scientific-session-detail/?sessionId=${encodeURIComponent(record.sessionId)}">Apri sessione →</a>
    </div>
    <details class="dsg-ai-record__details">
      <summary>Raccomandazioni, evidence e citation</summary>
      <div class="dsg-ai-recommendations">${record.recommendations.map(recommendationMarkup).join('')}</div>
      <div class="dsg-ai-citations"><strong>Fonti governate</strong><ul>${citations.map(item => `<li>${sourceLink(item)}</li>`).join('') || '<li>Nessuna citation disponibile.</li>'}</ul></div>
      <p class="dsg-ai-muted">Record digest: <code>${esc(record.recordDigest)}</code></p>
    </details>
  </article>`;
}

function renderProjection(host, projection) {
  host.innerHTML = `<section class="dsg-ai-kpis" aria-label="Riepilogo advisory projection">
    <article><span>SESSIONI</span><strong>${projection.summary.totalSessions}</strong></article>
    <article><span>PROVENANCE MATCHED</span><strong>${projection.summary.provenanceMatched}</strong></article>
    <article><span>PROVENANCE UNAVAILABLE</span><strong>${projection.summary.provenanceUnavailable}</strong></article>
    <article><span>HISTORY FAIL-CLOSED</span><strong>${projection.summary.processingHistoryFailClosed}</strong></article>
  </section>
  <section class="dsg-ai-panel dsg-ai-verified" aria-live="polite">
    <div><span>FRESHNESS VERIFIED</span><h2>Projection allineata al catalogo</h2><p>Generata ${esc(formatDate(projection.generatedAt))} · metodo <code>${esc(projection.methodId)}</code></p></div>
    <span class="dsg-ai-verified__badge">SHA-256 verificato</span>
  </section>
  <section class="dsg-ai-panel dsg-ai-source-state">
    <span>SOURCE STATE</span>
    <h2>Evidence reale preservata senza inferenze</h2>
    <p>${projection.sourceSet.entries.length} source BKL-045 validate al build; ${projection.summary.uncorrelatedSources} non correlate al catalogo. I dati operativi privati non sono pubblicati.</p>
  </section>
  <section class="dsg-ai-panel">
    <div class="dsg-ai-toolbar">
      <div><label for="ai-advisory-search">Cerca sessione o target</label><input id="ai-advisory-search" type="search" placeholder="es. M 27 o 2026-09"></div>
      <div><label for="ai-advisory-filter">Stato provenance</label><select id="ai-advisory-filter">
        <option value="ALL">Tutti gli stati</option>
        <option value="PROVENANCE_MATCHED">Provenance correlata</option>
        <option value="PROVENANCE_UNAVAILABLE">Provenance non disponibile</option>
        <option value="CORRELATION_AMBIGUOUS">Correlazione ambigua</option>
        <option value="CORRELATION_INVALID">Correlazione non valida</option>
      </select></div>
    </div>
    <p class="dsg-ai-result" data-ai-result aria-live="polite"></p>
    <div class="dsg-ai-records">${projection.records.map(recordMarkup).join('')}</div>
  </section>`;

  const search = host.querySelector('#ai-advisory-search');
  const filter = host.querySelector('#ai-advisory-filter');
  const result = host.querySelector('[data-ai-result]');
  const applyFilters = () => {
    const query = search.value.trim().toLowerCase();
    let visible = 0;
    host.querySelectorAll('.dsg-ai-record').forEach(card => {
      const matchesText = !query || card.dataset.search.includes(query);
      const matchesState = filter.value === 'ALL' || card.dataset.state === filter.value;
      card.hidden = !(matchesText && matchesState);
      if (!card.hidden) visible += 1;
    });
    result.textContent = `${visible} sessioni visualizzate · ordine canonico per sessionId`;
  };
  search.addEventListener('input', applyFilters);
  filter.addEventListener('change', applyFilters);
  applyFilters();
}

export async function initializeAiPostProcessingAssistant(root = document) {
  const host = root.querySelector('[data-ai-post-processing-assistant]');
  if (!host || host.dataset.initialized === 'true') return;
  host.dataset.initialized = 'true';
  try {
    const [projectionResponse, catalogResponse] = await Promise.all([
      fetch('../data/ai-post-processing-advisory-projection.json', { cache: 'no-store' }),
      fetch('../data/scientific-session-catalog.json', { cache: 'no-store' })
    ]);
    if (!projectionResponse.ok || !catalogResponse.ok) throw new Error('SOURCE_FETCH_FAILED');
    const [projection, catalog] = await Promise.all([projectionResponse.json(), catalogResponse.json()]);
    await validateAdvisoryProjectionFreshness(projection, catalog);
    renderProjection(host, projection);
  } catch (error) {
    renderFailure(host, error);
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => initializeAiPostProcessingAssistant(), { once: true });
} else {
  initializeAiPostProcessingAssistant();
}

globalThis.document$?.subscribe(() => initializeAiPostProcessingAssistant());
