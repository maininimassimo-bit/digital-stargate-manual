(() => {
  'use strict';

  const escapeHtml = (value) => String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');

  const formatNumber = (value) => Number(value || 0).toLocaleString('it-IT');
  const formatDateTime = (value) => value ? new Date(value).toLocaleString('it-IT') : '—';

  const kpiCards = (items) => items.map(({ label, value, hint = '' }) => `
    <article class="dsg-operations-widget dsg-operations-widget--kpi">
      <span>${escapeHtml(label)}</span>
      <strong>${formatNumber(value)}</strong>
      ${hint ? `<small>${escapeHtml(hint)}</small>` : ''}
    </article>`).join('');

  const healthList = (items) => items.length
    ? items.map(({ name, state, detail = '' }) => `
      <article class="dsg-operations-widget dsg-operations-widget--health is-${escapeHtml(state)}">
        <strong>${escapeHtml(name)}</strong>
        <span>${escapeHtml(state)}</span>
        ${detail ? `<small>${escapeHtml(detail)}</small>` : ''}
      </article>`).join('')
    : '<div class="dsg-operations-dashboard__empty">Nessun dato disponibile.</div>';

  const serviceList = (items) => items.map(({ name, available, version }) => `
    <article class="dsg-operations-widget dsg-operations-widget--service ${available ? 'is-available' : 'is-unavailable'}">
      <strong>${escapeHtml(name)}</strong>
      <span>${available ? 'Available' : 'Unavailable'}</span>
      <small>${escapeHtml(version || 'versione non disponibile')}</small>
    </article>`).join('');

  const eventTimeline = (items, limit = 12) => items.length
    ? items.slice(0, limit).map(({ type, observedAt }) => `
      <article class="dsg-operations-widget dsg-operations-widget--event">
        <strong>${escapeHtml(type)}</strong>
        <time>${escapeHtml(formatDateTime(observedAt))}</time>
      </article>`).join('')
    : '<div class="dsg-operations-dashboard__empty">Nessun evento runtime osservato in questa sessione.</div>';

  const ap013Card = (ap013) => `
    <article class="dsg-operations-ap013 is-${escapeHtml(ap013.validationState.toLowerCase())}">
      <div>
        <span>${escapeHtml(ap013.package)} · ${escapeHtml(ap013.capability)}</span>
        <strong>${escapeHtml(ap013.validationState)}</strong>
      </div>
      <dl>
        <div><dt>Operatore</dt><dd>${ap013.operatorReportedCompletion ? 'Completato' : 'Non completato'}</dd></div>
        <div><dt>Evidenze repository</dt><dd>${ap013.repositoryEvidenceAvailable ? 'Disponibili' : 'Pending'}</dd></div>
        <div><dt>Modalità</dt><dd>${escapeHtml(ap013.constraints.mode)}</dd></div>
        <div><dt>Limite</dt><dd>${formatNumber(ap013.constraints.maxFilesPerRun)} file/run</dd></div>
        <div><dt>Integrità</dt><dd>${escapeHtml(ap013.constraints.hashAlgorithm)}</dd></div>
      </dl>
    </article>`;

  window.DSGOperationsWidgets = Object.freeze({
    kpiCards,
    healthList,
    serviceList,
    eventTimeline,
    ap013Card
  });
})();
