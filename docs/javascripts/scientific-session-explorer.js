(() => {
  'use strict';

  const initialize = async ({ events } = {}) => {
    const root = document.querySelector('[data-session-catalog]');
    if (!root || root.dataset.dsgSessionExplorerReady === 'true') return;

    const engine = window.DSGScientificDataEngine;
    if (!engine) {
      console.error('Scientific Data Engine is not available.');
      events?.emit('scientific-session-explorer-error', { reason: 'engine-unavailable' });
      return;
    }

    root.dataset.dsgSessionExplorerReady = 'true';
    root.classList.add('is-loading');

    const source = root.dataset.sessionCatalog;
    const grid = root.querySelector('[data-session-grid]');
    const kpis = root.querySelector('[data-session-kpis]');
    const count = root.querySelector('[data-session-count]');
    const search = root.querySelector('[data-session-search]');
    const year = root.querySelector('[data-session-year]');
    const target = root.querySelector('[data-session-target]');
    const quality = root.querySelector('[data-session-quality]');
    const reset = root.querySelector('[data-session-reset]');

    const state = { sessions: [], filtered: [] };

    const esc = (value) => String(value ?? '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');

    const dec = (value, digits = 2) => Number(value || 0).toFixed(digits).replace('.', ',');
    const coordinate = (value) => {
      const number = Number(value);
      return Number.isFinite(number) ? `${number.toFixed(4).replace('.', ',')}°` : 'Non disponibile';
    };
    const formatDate = (value) => {
      const date = new Date(`${value}T00:00:00`);
      return Number.isNaN(date.getTime()) ? value : new Intl.DateTimeFormat('it-IT', { dateStyle: 'medium' }).format(date);
    };

    const statusLabel = (session) => {
      if (session.qualityState === 'VALIDATED_ANALYTICS') return 'Validated analytics';
      if (session.qualityState === 'METADATA_INCOMPLETE') return 'Metadata incomplete';
      return 'Attention required';
    };

    const governedCoordinates = (session) => {
      const ra = Number(session.raDeg ?? session.ra_deg);
      const decValue = Number(session.decDeg ?? session.dec_deg);
      if (!Number.isFinite(ra) || !Number.isFinite(decValue)) return null;
      return { ra, dec: decValue, source: session.coordinateSource || 'governed-registry' };
    };

    const renderKpis = async () => {
      const values = await engine.getKPIs(source);
      const display = [String(values.sessionCount),String(values.targetCount),`${dec(values.integrationHours)} h`,`${values.validatedCount}/${values.sessionCount}`];
      [...kpis.querySelectorAll('strong')].forEach((node, index) => { node.textContent = display[index] || '—'; });
    };

    const populateFilters = async () => {
      const [years, targets] = await Promise.all([engine.getYears(source),engine.getTargets(source)]);
      years.forEach((value) => year.insertAdjacentHTML('beforeend', `<option value="${esc(value)}">${esc(value)}</option>`));
      targets.forEach((value) => target.insertAdjacentHTML('beforeend', `<option value="${esc(value)}">${esc(value)}</option>`));
    };

    const card = (session) => {
      const tone = session.qualityState === 'VALIDATED_ANALYTICS' ? 'is-green' : 'is-red';
      const detailUrl = `../scientific-session-detail/?sessionId=${encodeURIComponent(session.sessionId)}`;
      const coords = governedCoordinates(session);
      const sqmMedian = Number(session.sqm?.medianMagArcsec2);
      const sqmMetric = Number.isFinite(sqmMedian) ? `
            <div><span>SQM mediano</span><strong>${esc(dec(sqmMedian, 2))} mag/arcsec²</strong></div>` : '';
      const coordinateMetrics = coords ? `
            <div><span>RA (J2000)</span><strong>${esc(coordinate(coords.ra))}</strong></div>
            <div><span>DEC (J2000)</span><strong>${esc(coordinate(coords.dec))}</strong></div>` : '';
      const coordinateState = coords ? `<span>Coordinate: ${esc(coords.source)}</span>` : '';
      const analyticsState = session.severity ? `<span>Analytics: ${esc(session.severity)}</span>` : '';
      const sqmState = session.sqm?.state ? `<span>SQM: ${esc(session.sqm.state)}</span>` : '';
      return `
        <article class="dsg-session-card ${tone}">
          <div class="dsg-session-card__topline"><span>${esc(session.sessionId)}</span><span class="dsg-session-badge">${esc(statusLabel(session))}</span></div>
          <h2>${esc(session.target)}</h2>
          <p class="dsg-session-card__date">${esc(formatDate(session.observationDate))}</p>
          <div class="dsg-session-card__metrics">
            <div><span>Telescopio</span><strong>${esc(session.telescope)}</strong></div>
            <div><span>Camera</span><strong>${esc(session.camera)}</strong></div>
            <div><span>Filtro</span><strong>${esc(session.filter)}</strong></div>
            <div><span>Esposizione</span><strong>${esc(session.exposureSeconds)} s</strong></div>
            <div><span>Integrazione</span><strong>${dec(session.integrationHours)} h</strong></div>
            <div><span>Completamento</span><strong>${dec(session.completionPct)}%</strong></div>
            <div><span>RMS</span><strong>${dec(session.rmsTotalArcsec, 3)}″</strong></div>
            <div><span>Light</span><strong>${esc(session.lightCompleted)} / ${esc(session.lightStarted)}</strong></div>${sqmMetric}${coordinateMetrics}
          </div>
          <div class="dsg-session-card__states">
            <span>Evidence: ${esc(session.evidenceState)}</span><span>Manifest: ${esc(session.manifestState)}</span><span>Transfer: ${esc(session.transferState)}</span>${analyticsState}${sqmState}${coordinateState}
          </div>
          <a href="${detailUrl}">Apri sessione →</a>
        </article>`;
    };

    const render = () => {
      state.filtered = engine.filterSessions(state.sessions, {query: search.value,year: year.value,target: target.value,quality: quality.value});
      count.textContent = `${state.filtered.length} sessioni visualizzate su ${state.sessions.length}`;
      grid.innerHTML = state.filtered.length ? state.filtered.map(card).join('') : '<article class="dsg-session-empty">Nessuna sessione corrisponde ai filtri selezionati.</article>';
      events?.emit('scientific-session-explorer-filtered', {source,visible: state.filtered.length,total: state.sessions.length});
    };

    [search, year, target, quality].forEach((control) => control.addEventListener('input', render));
    reset.addEventListener('click', () => {search.value='';year.value='';target.value='';quality.value='';render();});

    try {
      const [sessions] = await Promise.all([engine.getSessions(source),renderKpis(),populateFilters()]);
      state.sessions = sessions;
      render();
      root.classList.remove('is-loading', 'is-error');
      root.classList.add('is-ready');
      events?.emit('scientific-session-explorer-ready', {source,sessions:sessions.length,metrics:engine.getMetrics?.() || null});
    } catch (error) {
      console.error(error);
      root.dataset.dsgSessionExplorerReady = 'error';
      root.classList.remove('is-loading', 'is-ready');
      root.classList.add('is-error');
      count.textContent = 'Catalogo non disponibile';
      grid.innerHTML = '<article class="dsg-session-empty is-error">Impossibile caricare il catalogo delle sessioni. Verificare il dataset versionato.</article>';
      events?.emit('scientific-session-explorer-error', {source,message:error.message});
    }
  };

  if (window.DSG?.components) {window.DSG.components.register({name:'scientific-session-explorer',order:65,initialize});return;}
  const fallback = () => initialize();
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fallback, { once: true }); else fallback();
  if (window.document$?.subscribe) window.document$.subscribe(fallback);
})();
