(() => {
  const root = document.querySelector('[data-session-detail]');
  if (!root) return;

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

  const render = (session) => {
    title.textContent = `${session.target} · ${session.sessionId}`;
    subtitle.textContent = `${displayDate(session.observationDate)} · ${session.telescope} · ${session.camera}`;

    summary.innerHTML = [
      metric('Qualità', session.qualityState),
      metric('Integrazione', `${dec(session.integrationHours)} h`),
      metric('Completamento', `${dec(session.completionPct)}%`),
      metric('RMS totale', `${dec(session.rmsTotalArcsec, 3)}″`)
    ].join('');

    const fields = [
      ['Session ID', session.sessionId],
      ['Data osservativa', displayDate(session.observationDate)],
      ['Configuration ID', session.configurationId],
      ['Target', session.target],
      ['Telescopio', session.telescope],
      ['Camera', session.camera],
      ['Filtro', session.filter],
      ['Binning', session.binning],
      ['Gain / Offset', `${session.gain} / ${session.offset}`],
      ['Esposizione', `${session.exposureSeconds} s`],
      ['Light completati', `${session.lightCompleted} / ${session.lightStarted}`],
      ['Evidence state', session.evidenceState]
    ];
    metadata.innerHTML = fields.map(([label, value]) => metric(label, value)).join('');

    graph.innerHTML = `
      <div class="dsg-graph-row">
        ${node('TARGET', session.target, 'Scientific object', 'is-target')}
      </div>
      <div class="dsg-graph-connector">↓ observed in</div>
      <div class="dsg-graph-row">
        ${node('SESSION', session.sessionId, displayDate(session.observationDate), 'is-session')}
      </div>
      <div class="dsg-graph-connector">↓ acquired with</div>
      <div class="dsg-graph-row dsg-graph-row--triple">
        ${node('TELESCOPE', session.telescope, session.configurationId)}
        ${node('CAMERA', session.camera, `${session.binning} · gain ${session.gain}`)}
        ${node('FILTER', session.filter, `${session.exposureSeconds} s exposures`)}
      </div>
      <div class="dsg-graph-connector">↓ produces</div>
      <div class="dsg-graph-row dsg-graph-row--triple">
        ${node('METRICS', 'Session metrics', session.evidenceState, 'is-available')}
        ${node('MANIFEST', 'Not represented', session.manifestState, 'is-missing')}
        ${node('TRANSFER', 'Not represented', session.transferState, 'is-missing')}
      </div>`;

    const lineageSteps = [
      ['Observation session', 'represented', session.sessionId],
      ['Acquisition metrics', 'represented', `${session.lightCompleted} completed light frames`],
      ['Scientific assets', 'partial', 'paths and binary inventory not exposed in this catalog'],
      ['Manifest', 'missing', session.manifestState],
      ['Processing', 'missing', 'not represented'],
      ['Publication', 'missing', 'not represented']
    ];
    lineage.innerHTML = lineageSteps.map(([label, state, detail], index) => `
      <article class="dsg-lineage-step is-${esc(state)}">
        <span>${String(index + 1).padStart(2, '0')}</span>
        <strong>${esc(label)}</strong>
        <small>${esc(detail)}</small>
      </article>`).join('');

    const sourceHref = `../../${session.sourceMetricsPath}`;
    sources.innerHTML = `
      <a href="${esc(sourceHref)}"><strong>Session metrics</strong><span>${esc(session.sourceMetricsPath)}</span></a>
      <a href="../architecture/scientific-assets/DSDM-001-Scientific-Data-Manager-Conceptual-Model/"><strong>DSDM-001</strong><span>Scientific Data Manager Conceptual Model</span></a>
      <a href="../architecture/scientific-assets/DSDM-003-Contract-and-Manifest-Model/"><strong>DSDM-003</strong><span>Contract and Manifest Model</span></a>
      <a href="../architecture/validation/AP-013-Session-Discovery-Execution-Evidence/"><strong>Discovery Evidence</strong><span>AP-013 execution evidence</span></a>`;
  };

  const fail = (message) => {
    errorBox.hidden = false;
    errorBox.textContent = message;
    title.textContent = 'Sessione non disponibile';
    subtitle.textContent = 'Impossibile costruire la vista richiesta.';
  };

  if (!sessionId) {
    fail('Parametro sessionId mancante. Aprire la sessione dal Scientific Session Catalog.');
    return;
  }

  fetch(source)
    .then((response) => {
      if (!response.ok) throw new Error(`Catalog request failed: ${response.status}`);
      return response.json();
    })
    .then((catalog) => {
      const session = (catalog.sessions || []).find((item) => item.sessionId === sessionId);
      if (!session) throw new Error(`Session not found: ${sessionId}`);
      render(session);
    })
    .catch((error) => {
      console.error(error);
      fail('La sessione richiesta non è presente nel catalogo versionato oppure il catalogo non è disponibile.');
    });
})();
