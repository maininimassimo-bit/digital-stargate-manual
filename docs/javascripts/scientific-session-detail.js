(() => {
  'use strict';

  const initialize = async ({ events } = {}) => {
    const root = document.querySelector('[data-session-detail]');
    if (!root || root.dataset.dsgSessionDetailReady === 'true') return;

    const engine = window.DSGScientificDataEngine;
    if (!engine) {
      console.error('Scientific Data Engine is not available.');
      events?.emit('scientific-session-detail-error', { reason: 'engine-unavailable' });
      return;
    }

    root.dataset.dsgSessionDetailReady = 'true';
    root.classList.add('is-loading');

    const source = root.dataset.sessionCatalog;
    const params = new URLSearchParams(window.location.search);
    const sessionId = params.get('sessionId');

    const title = root.querySelector('[data-detail-title]');
    const subtitle = root.querySelector('[data-detail-subtitle]');
    const summary = root.querySelector('[data-detail-summary]');
    const metadata = root.querySelector('[data-detail-metadata]');
    const graph = root.querySelector('[data-detail-graph]');
    const lineage = root.querySelector('[data-detail-lineage]');
    const sources = root.querySelector('[data-detail-sources]');
    const errorBox = root.querySelector('[data-detail-error]');

    const esc = (value) => String(value ?? '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');

    const isKnown = (value) => {
      const normalized = String(value ?? '').trim().toUpperCase();
      return Boolean(normalized) && normalized !== 'UNKNOWN' && normalized !== 'N/A';
    };
    const displayValue = (value, fallback = 'Non disponibile') => isKnown(value) ? value : fallback;
    const dec = (value, digits = 2) => Number(value || 0).toFixed(digits).replace('.', ',');
    const displayDate = (value) => {
      const date = new Date(`${value}T00:00:00`);
      return Number.isNaN(date.getTime()) ? value : new Intl.DateTimeFormat('it-IT', { dateStyle: 'long' }).format(date);
    };

    const metric = (label, value) => `<article><span>${esc(label)}</span><strong>${esc(value)}</strong></article>`;
    const node = (kind, label, value, state = '') => `
      <article class="dsg-graph-node ${state}">
        <span>${esc(kind)}</span>
        <strong>${esc(label)}</strong>
        <small>${esc(value)}</small>
      </article>`;

    const renderGraph = (session, graphModel) => {
      const equipment = graphModel.equipment.filter((item) => isKnown(item.label));
      const equipmentNodes = equipment.length
        ? equipment.map((item) => {
            if (item.type === 'TELESCOPE') return node(item.type, item.label, displayValue(session.configurationId));
            if (item.type === 'CAMERA') return node(item.type, item.label, isKnown(session.binning) ? `${session.binning}${session.gain !== null ? ` · gain ${session.gain}` : ''}` : 'Metadata parziali');
            return node(item.type, item.label, session.exposureSeconds !== null ? `${session.exposureSeconds} s exposures` : 'Metadata parziali');
          }).join('')
        : node('EQUIPMENT', 'Metadata non attestati', session.metadataState || 'INCOMPLETE', 'is-missing');

      graph.innerHTML = `
        <div class="dsg-graph-row">
          ${node(graphModel.target.type, graphModel.target.label, 'Scientific object', 'is-target')}
        </div>
        <div class="dsg-graph-connector">↓ observed in</div>
        <div class="dsg-graph-row">
          ${node(graphModel.session.type, graphModel.session.label, displayDate(session.observationDate), 'is-session')}
        </div>
        <div class="dsg-graph-connector">↓ acquired with</div>
        <div class="dsg-graph-row dsg-graph-row--triple">${equipmentNodes}</div>
        <div class="dsg-graph-connector">↓ produces</div>
        <div class="dsg-graph-row dsg-graph-row--triple">
          ${graphModel.outputs.map((output) => node(
            output.type,
            output.available ? 'Session metrics' : 'Not represented',
            output.state,
            output.available ? 'is-available' : 'is-missing'
          )).join('')}
        </div>`;
    };

    const renderLineage = (steps) => {
      lineage.innerHTML = steps.map((step, index) => `
        <article class="dsg-lineage-step is-${esc(step.state)}">
          <span>${String(index + 1).padStart(2, '0')}</span>
          <strong>${esc(step.label)}</strong>
          <small>${esc(step.detail)}</small>
        </article>`).join('');
    };

    const render = (session) => {
      title.textContent = `${session.target} · ${session.sessionId}`;
      const subtitleParts = [displayDate(session.observationDate)];
      if (isKnown(session.telescope)) subtitleParts.push(session.telescope);
      if (isKnown(session.camera)) subtitleParts.push(session.camera);
      if (session.qualityState === 'METADATA_INCOMPLETE') subtitleParts.push('metadata scientifici incompleti');
      subtitle.textContent = subtitleParts.join(' · ');

      summary.innerHTML = [
        metric('Qualità catalogo', session.qualityState),
        metric('Esito analytics', session.analyticsState || session.severity),
        metric('Integrazione', `${dec(session.integrationHours)} h`),
        metric('RMS totale', `${dec(session.rmsTotalArcsec, 3)}″`)
      ].join('');

      const fields = [
        ['Session ID', session.sessionId],
        ['Data osservativa', displayDate(session.observationDate)],
        ['Metadata state', session.metadataState || 'UNREGISTERED'],
        ['Configuration ID', displayValue(session.configurationId)],
        ['Target', displayValue(session.target)],
        ['Telescopio', displayValue(session.telescope)],
        ['Camera', displayValue(session.camera)],
        ['Filtro', displayValue(session.filter)],
        ['Binning', displayValue(session.binning)],
        ['Gain / Offset', session.gain !== null || session.offset !== null ? `${session.gain ?? '—'} / ${session.offset ?? '—'}` : 'Non disponibile'],
        ['Esposizione', session.exposureSeconds !== null ? `${session.exposureSeconds} s` : 'Non disponibile'],
        ['Light completati', `${session.lightCompleted} / ${session.lightStarted}`],
        ['Evidence state', session.evidenceState]
      ];
      metadata.innerHTML = fields.map(([label, value]) => metric(label, value)).join('');

      renderGraph(session, engine.getKnowledgeGraph(session));
      renderLineage(engine.getLineage(session));

      const sourceHref = `../../${session.sourceMetricsPath}`;
      sources.innerHTML = `
        <a href="${esc(sourceHref)}"><strong>Session metrics</strong><span>${esc(session.sourceMetricsPath)}</span></a>
        <a href="../architecture/scientific-assets/DSDM-001-Scientific-Data-Manager-Conceptual-Model/"><strong>DSDM-001</strong><span>Scientific Data Manager Conceptual Model</span></a>
        <a href="../architecture/scientific-assets/DSDM-003-Contract-and-Manifest-Model/"><strong>DSDM-003</strong><span>Contract and Manifest Model</span></a>
        <a href="../architecture/validation/AP-013-Session-Discovery-Execution-Evidence/"><strong>Discovery Evidence</strong><span>AP-013 execution evidence</span></a>`;
    };

    const fail = (message, reason) => {
      errorBox.hidden = false;
      errorBox.textContent = message;
      title.textContent = 'Sessione non disponibile';
      subtitle.textContent = 'Impossibile costruire la vista richiesta.';
      root.dataset.dsgSessionDetailReady = 'error';
      root.classList.remove('is-loading', 'is-ready');
      root.classList.add('is-error');
      events?.emit('scientific-session-detail-error', { source, sessionId, reason });
    };

    if (!sessionId) {
      fail('Parametro sessionId mancante. Aprire la sessione dal Scientific Session Catalog.', 'missing-session-id');
      return;
    }

    try {
      const session = await engine.getSession(source, sessionId);
      if (!session) throw new Error(`Session not found: ${sessionId}`);
      render(session);
      root.classList.remove('is-loading', 'is-error');
      root.classList.add('is-ready');
      events?.emit('scientific-session-detail-ready', {
        source,
        sessionId,
        target: session.target,
        metrics: engine.getMetrics?.() || null
      });
    } catch (error) {
      console.error(error);
      fail('La sessione richiesta non è presente nel catalogo versionato oppure il catalogo non è disponibile.', error.message);
    }
  };

  if (window.DSG?.components) {
    window.DSG.components.register({
      name: 'scientific-session-detail',
      order: 66,
      initialize
    });
    return;
  }

  const fallback = () => initialize();
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', fallback, { once: true });
  } else {
    fallback();
  }
  if (window.document$?.subscribe) window.document$.subscribe(fallback);
})();
