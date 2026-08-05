(() => {
  'use strict';

  const escapeHtml = (value) => String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');

  const excerpt = (text, max = 220) => {
    const compact = String(text || '').replace(/\s+/g, ' ').trim();
    return compact.length > max ? `${compact.slice(0, max).trim()}…` : compact;
  };

  const initialize = async ({ events } = {}) => {
    const root = document.querySelector('[data-dsg-search-center]');
    if (!root || root.dataset.dsgSearchCenterReady === 'true') return;

    const scope = root.closest('[data-dsg-documentation-center]') || document;
    const service = window.DSGSearchService;
    if (!service) {
      root.innerHTML = '<div class="dsg-search-center__error">Search Service non disponibile.</div>';
      events?.emit('search-center-error', { reason: 'service-unavailable' });
      return;
    }

    const queryInput = scope.querySelector('[data-search-query]');
    const typeFilter = scope.querySelector('[data-search-type]');
    const yearFilter = scope.querySelector('[data-search-year]');
    const targetFilter = scope.querySelector('[data-search-target]');
    const qualityFilter = scope.querySelector('[data-search-quality]');
    const resetButton = scope.querySelector('[data-search-reset]');
    const statusNode = scope.querySelector('[data-search-status]');
    const resultNode = scope.querySelector('[data-search-results]');
    const statsNode = scope.querySelector('[data-search-stats]');
    const filterPanel = scope.querySelector('.dsg-search-center__filters');

    const controls = { queryInput, typeFilter, yearFilter, targetFilter, qualityFilter, resetButton, statusNode, resultNode, statsNode, filterPanel };
    const missing = Object.entries(controls).filter(([, value]) => !value).map(([name]) => name);

    if (missing.length) {
      console.error('Search Center DOM incomplete', { missing });
      root.classList.add('is-error');
      if (statusNode) statusNode.textContent = 'Ricerca non disponibile';
      if (resultNode) resultNode.innerHTML = '<div class="dsg-search-center__error">Struttura del Search Center incompleta.</div>';
      events?.emit('search-center-error', { reason: 'dom-incomplete', missing });
      return;
    }

    filterPanel.insertAdjacentHTML('beforeend', `
      <label>Filtro
        <select data-search-filter><option value="">Tutti i filtri</option></select>
      </label>
      <label>Telescopio
        <select data-search-telescope><option value="">Tutti i telescopi</option></select>
      </label>
      <label>Camera
        <select data-search-camera><option value="">Tutte le camere</option></select>
      </label>
      <label>Ordina per
        <select data-search-sort>
          <option value="relevance">Rilevanza</option>
          <option value="year-desc">Data più recente</option>
          <option value="quality">Qualità</option>
          <option value="title">Titolo</option>
        </select>
      </label>`);

    const filterFilter = scope.querySelector('[data-search-filter]');
    const telescopeFilter = scope.querySelector('[data-search-telescope]');
    const cameraFilter = scope.querySelector('[data-search-camera]');
    const sortFilter = scope.querySelector('[data-search-sort]');

    const suggestionList = document.createElement('datalist');
    suggestionList.id = 'dsg-search-suggestions';
    queryInput.setAttribute('list', suggestionList.id);
    queryInput.insertAdjacentElement('afterend', suggestionList);
    queryInput.placeholder = 'Cerca oppure usa target:, year:, filter:, quality:, telescope:…';

    root.dataset.dsgSearchCenterReady = 'true';
    root.classList.add('is-loading');
    let timer = null;

    const fillSelect = (select, values) => {
      select.querySelectorAll('option:not(:first-child)').forEach((option) => option.remove());
      values.forEach((value) => select.insertAdjacentHTML('beforeend', `<option value="${escapeHtml(value)}">${escapeHtml(value)}</option>`));
    };

    const filters = () => ({
      type: typeFilter.value,
      year: yearFilter.value,
      target: targetFilter.value,
      quality: qualityFilter.value,
      filter: filterFilter.value,
      telescope: telescopeFilter.value,
      camera: cameraFilter.value
    });

    const rankingExplanation = (item) => {
      const explanation = item.scoreExplanation;
      if (!explanation) return '';
      const terms = explanation.matchedTerms?.length ? ` · termini: ${explanation.matchedTerms.join(', ')}` : '';
      return `<details class="dsg-search-result__explanation"><summary>Perché questo risultato?</summary><p>Punteggio ${escapeHtml(item.score)}: testo ${escapeHtml(explanation.text)}, autorità ${escapeHtml(explanation.authority)}, qualità ${escapeHtml(explanation.quality)}${escapeHtml(terms)}.</p></details>`;
    };

    const render = async () => {
      root.classList.add('is-searching');
      const query = queryInput.value.trim();
      const results = await service.search(query, { filters: filters(), sort: sortFilter.value, limit: 50 });
      const parsed = service.parseQuery?.(query);

      statusNode.textContent = query
        ? `${results.length} risultati per “${query}”`
        : `${results.length} risultati disponibili`;

      resultNode.innerHTML = results.length
        ? results.map((item) => `
          <article class="dsg-search-result is-${escapeHtml(item.type)}">
            <div class="dsg-search-result__meta">
              <span>${item.type === 'scientific-session' ? 'Sessione scientifica' : 'Documentazione'}</span>
              <span>${escapeHtml(item.section)}</span>
              <span>Score ${escapeHtml(item.score)}</span>
            </div>
            <h2><a href="${escapeHtml(item.location)}">${escapeHtml(item.title)}</a></h2>
            <p>${escapeHtml(excerpt(item.text))}</p>
            ${item.type === 'scientific-session' ? `<div class="dsg-search-result__facts">
              <span>${escapeHtml(item.metadata?.year || '')}</span>
              <span>${escapeHtml(item.metadata?.target || '')}</span>
              <span>${escapeHtml(item.metadata?.telescope || '')}</span>
              <span>${escapeHtml(item.metadata?.camera || '')}</span>
              <span>${escapeHtml(item.metadata?.filter || '')}</span>
              <span>${escapeHtml(item.metadata?.qualityState || '')}</span>
            </div>` : ''}
            ${rankingExplanation(item)}
          </article>`).join('')
        : '<div class="dsg-search-center__empty">Nessun risultato corrisponde ai criteri selezionati.</div>';

      const serviceStatus = service.getStatus();
      const structuredCount = Object.keys(parsed?.filters || {}).length;
      statsNode.textContent = `${serviceStatus.documentCount} documenti · ${serviceStatus.scientificCount} sessioni scientifiche${structuredCount ? ` · ${structuredCount} filtri nella query` : ''}`;
      root.classList.remove('is-searching');
      events?.emit('search-center-results', { query, parsed, resultCount: results.length, filters: filters(), sort: sortFilter.value });
    };

    const handleError = (error) => {
      console.error(error);
      root.classList.remove('is-loading', 'is-searching', 'is-ready');
      root.classList.add('is-error');
      statusNode.textContent = 'Ricerca non disponibile';
      resultNode.innerHTML = '<div class="dsg-search-center__error">Impossibile caricare gli indici federati.</div>';
      events?.emit('search-center-error', { message: error.message });
    };

    const scheduleRender = () => {
      window.clearTimeout(timer);
      timer = window.setTimeout(() => render().catch(handleError), 160);
    };

    try {
      await service.load();
      const facets = await service.getFacets();
      fillSelect(typeFilter, facets.types);
      fillSelect(yearFilter, facets.years);
      fillSelect(targetFilter, facets.targets);
      fillSelect(qualityFilter, facets.qualities);
      fillSelect(filterFilter, facets.filters || []);
      fillSelect(telescopeFilter, facets.telescopes || []);
      fillSelect(cameraFilter, facets.cameras || []);

      const suggestions = [
        ...(facets.targets || []).map((value) => `target:${value}`),
        ...(facets.years || []).map((value) => `year:${value}`),
        ...(facets.filters || []).map((value) => `filter:${value}`),
        ...(facets.qualities || []).map((value) => `quality:${value}`),
        ...(facets.telescopes || []).map((value) => `telescope:\"${value}\"`),
        ...(facets.cameras || []).map((value) => `camera:\"${value}\"`)
      ];
      suggestionList.innerHTML = suggestions.map((value) => `<option value="${escapeHtml(value)}"></option>`).join('');

      [queryInput, typeFilter, yearFilter, targetFilter, qualityFilter, filterFilter, telescopeFilter, cameraFilter, sortFilter]
        .forEach((control) => control.addEventListener('input', scheduleRender));

      resetButton.addEventListener('click', () => {
        queryInput.value = '';
        [typeFilter, yearFilter, targetFilter, qualityFilter, filterFilter, telescopeFilter, cameraFilter].forEach((control) => { control.value = ''; });
        sortFilter.value = 'relevance';
        render().catch(handleError);
      });

      root.classList.remove('is-loading');
      root.classList.add('is-ready');
      await render();
      queryInput.focus({ preventScroll: true });
      events?.emit('search-center-ready', service.getStatus());
    } catch (error) {
      handleError(error);
    }
  };

  if (window.DSG?.components) window.DSG.components.register({ name: 'search-center', order: 75, initialize });
  else if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => initialize(), { once: true });
  else initialize();
})();
