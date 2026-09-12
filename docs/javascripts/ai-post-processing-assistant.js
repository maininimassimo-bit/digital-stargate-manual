import {
  validateAdvisoryProjectionFreshness,
  validateRealEvidenceEvaluationFreshness
} from './ai-post-processing-assistant-core.mjs';

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

const OUTCOME_LABELS = {
  technical: 'Esito tecnico',
  scientific: 'Efficacia scientifica',
  humanDecision: 'Decisioni umane',
  production: 'Produzione'
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
    <span>EVALUATION UNAVAILABLE · FAIL-CLOSED</span>
    <h2>${esc(message.title)}</h2>
    <p>${esc(message.detail)}</p>
    <details><summary>Dettaglio diagnostico</summary><code>${esc(error?.message || 'Errore non classificato')}</code></details>
  </section>`;
}

const outcomeMarkup = (axis, outcome) => `<article class="dsg-ai-evaluation__outcome">
  <span>${esc(OUTCOME_LABELS[axis])}</span>
  <strong>${esc(outcome.state)}</strong>
  <p>${esc(outcome.reasonCodes.join(' · ') || 'Nessun reason code')}</p>
</article>`;

function evaluationMarkup(evaluation) {
  const axes = ['technical', 'scientific', 'humanDecision', 'production'];
  const pendingGates = evaluation.technicalGates.filter(gate => gate.state !== 'PASS');
  return `<section class="dsg-ai-panel dsg-ai-evaluation" aria-labelledby="dsg-ai-evaluation-title">
    <div class="dsg-ai-evaluation__header">
      <div><span>F5 REAL-EVIDENCE EVALUATION</span><h2 id="dsg-ai-evaluation-title">Valutazione corrente verificata</h2><p>Generata ${esc(formatDate(evaluation.generatedAt))} · <code>${esc(evaluation.evaluationId)}</code></p></div>
      <span class="dsg-ai-state is-evaluation-open">Closure: ${esc(evaluation.outcomes.closureRecommendation)}</span>
    </div>
    <div class="dsg-ai-evaluation__grid">${axes.map(axis => outcomeMarkup(axis, evaluation.outcomes[axis])).join('')}</div>
    <div class="dsg-ai-evaluation__facts" role="list" aria-label="Copertura evidence">
      <span role="listitem"><strong>${evaluation.summary.canonicalSessions}</strong> sessioni canoniche</span>
      <span role="listitem"><strong>${evaluation.summary.provenanceEligible}</strong> con provenance esatta</span>
      <span role="listitem"><strong>${evaluation.summary.humanDecisionReceipts}</strong> decision receipt</span>
      <span role="listitem"><strong>${evaluation.summary.executionEvidence}</strong> execution evidence</span>
    </div>
    <p class="dsg-ai-evaluation__boundary"><strong>Modello AI implementato: NO.</strong> Questa valutazione non dimostra efficacia scientifica, readiness produttiva, accettazione automatica o autorità di esecuzione.</p>
    <details><summary>Gate non PASS e limitazioni</summary>
      <ul>${pendingGates.map(gate => `<li><strong>${esc(gate.gateId)}</strong>: ${esc(gate.state)} · ${esc(gate.reasonCodes.join(' · '))}</li>`).join('') || '<li>Nessun gate non PASS.</li>'}</ul>
      <ul>${evaluation.limitations.map(item => `<li>${esc(item)}</li>`).join('')}</ul>
    </details>
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

function renderProjection(host, projection, evaluation) {
  host.innerHTML = `<section class="dsg-ai-kpis" aria-label="Riepilogo advisory projection">
    <article><span>SESSIONI</span><strong>${projection.summary.totalSessions}</strong></article>
    <article><span>PROVENANCE MATCHED</span><strong>${projection.summary.provenanceMatched}</strong></article>
    <article><span>PROVENANCE UNAVAILABLE</span><strong>${projection.summary.provenanceUnavailable}</strong></article>
    <article><span>HISTORY FAIL-CLOSED</span><strong>${projection.summary.processingHistoryFailClosed}</strong></article>
  </section>
  <section class="dsg-ai-panel dsg-ai-verified" aria-live="polite">
    <div><span>FRESHNESS CHAIN VERIFIED</span><h2>Catalogo, projection F4 e valutazione F5 allineati</h2><p>Projection generata ${esc(formatDate(projection.generatedAt))} · metodo <code>${esc(projection.methodId)}</code></p></div>
    <span class="dsg-ai-verified__badge">3 snapshot verificati</span>
  </section>
  ${evaluationMarkup(evaluation)}
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
    const [projectionResponse, catalogResponse, evaluationResponse] = await Promise.all([
      fetch('../data/ai-post-processing-advisory-projection.json', { cache: 'no-store' }),
      fetch('../data/scientific-session-catalog.json', { cache: 'no-store' }),
      fetch('../data/ai-post-processing-advisory-f5-evaluation.json', { cache: 'no-store' })
    ]);
    if (!projectionResponse.ok || !catalogResponse.ok || !evaluationResponse.ok) throw new Error('SOURCE_FETCH_FAILED');
    const [projection, catalog, evaluation] = await Promise.all([projectionResponse.json(), catalogResponse.json(), evaluationResponse.json()]);
    await validateAdvisoryProjectionFreshness(projection, catalog);
    await validateRealEvidenceEvaluationFreshness(evaluation, projection, catalog);
    renderProjection(host, projection, evaluation);
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
