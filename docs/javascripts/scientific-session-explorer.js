(() => {
  const root = document.querySelector('[data-session-catalog]');
  if (!root) return;

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
  const formatDate = (value) => {
    const date = new Date(`${value}T00:00:00`);
    return Number.isNaN(date.getTime()) ? value : new Intl.DateTimeFormat('it-IT', { dateStyle: 'medium' }).format(date);
  };

  const statusLabel = (session) => session.qualityState === 'VALIDATED_ANALYTICS'
    ? 'Validated analytics'
    : 'Attention required';

  const renderKpis = () => {
    const sessions = state.sessions;
    const targets = new Set(sessions.map((item) => item.target));
    const integration = sessions.reduce((sum, item) => sum + Number(item.integrationHours || 0), 0);
    const validated = sessions.filter((item) => item.qualityState === 'VALIDATED_ANALYTICS').length;
    const values = [
      String(sessions.length),
      String(targets.size),
      `${dec(integration)} h`,
      `${validated}/${sessions.length}`
    ];
    [...kpis.querySelectorAll('strong')].forEach((node, index) => { node.textContent = values[index] || '—'; });
  };

  const populateFilters = () => {
    const years = [...new Set(state.sessions.map((item) => item.observationDate.slice(0, 4)))].sort().reverse();
    const targets = [...new Set(state.sessions.map((item) => item.target))].sort();
    years.forEach((value) => year.insertAdjacentHTML('beforeend', `<option value="${esc(value)}">${esc(value)}</option>`));
    targets.forEach((value) => target.insertAdjacentHTML('beforeend', `<option value="${esc(value)}">${esc(value)}</option>`));
  };

  const card = (session) => {
    const tone = session.qualityState === 'VALIDATED_ANALYTICS' ? 'is-green' : 'is-red';
    return `
      <article class="dsg-session-card ${tone}">
        <div class="dsg-session-card__topline">
          <span>${esc(session.sessionId)}</span>
          <span class="dsg-session-badge">${esc(statusLabel(session))}</span>
        </div>
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
          <div><span>Light</span><strong>${esc(session.lightCompleted)} / ${esc(session.lightStarted)}</strong></div>
        </div>
        <div class="dsg-session-card__states">
          <span>Evidence: ${esc(session.evidenceState)}</span>
          <span>Manifest: ${esc(session.manifestState)}</span>
          <span>Transfer: ${esc(session.transferState)}</span>
        </div>
        <a href="../../${esc(session.sourceMetricsPath)}">Apri metriche sorgente →</a>
      </article>`;
  };

  const render = () => {
    const query = search.value.trim().toLowerCase();
    const selectedYear = year.value;
    const selectedTarget = target.value;
    const selectedQuality = quality.value;

    state.filtered = state.sessions.filter((item) => {
      const haystack = [item.sessionId, item.target, item.telescope, item.camera, item.filter, item.configurationId]
        .join(' ').toLowerCase();
      return (!query || haystack.includes(query))
        && (!selectedYear || item.observationDate.startsWith(selectedYear))
        && (!selectedTarget || item.target === selectedTarget)
        && (!selectedQuality || item.qualityState === selectedQuality);
    });

    count.textContent = `${state.filtered.length} sessioni visualizzate su ${state.sessions.length}`;
    grid.innerHTML = state.filtered.length
      ? state.filtered.map(card).join('')
      : '<article class="dsg-session-empty">Nessuna sessione corrisponde ai filtri selezionati.</article>';
  };

  [search, year, target, quality].forEach((control) => control.addEventListener('input', render));
  reset.addEventListener('click', () => {
    search.value = '';
    year.value = '';
    target.value = '';
    quality.value = '';
    render();
  });

  fetch(source)
    .then((response) => {
      if (!response.ok) throw new Error(`Catalog request failed: ${response.status}`);
      return response.json();
    })
    .then((catalog) => {
      state.sessions = [...(catalog.sessions || [])]
        .sort((a, b) => String(b.observationDate).localeCompare(String(a.observationDate)));
      renderKpis();
      populateFilters();
      render();
    })
    .catch((error) => {
      console.error(error);
      count.textContent = 'Catalogo non disponibile';
      grid.innerHTML = '<article class="dsg-session-empty is-error">Impossibile caricare il catalogo delle sessioni. Verificare il dataset versionato.</article>';
    });
})();
