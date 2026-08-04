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

    const service = window.DSGSearchService;
    if (!service) {
      root.innerHTML = '<div class="dsg-search-center__error">Search Service non disponibile.</div>';
      events?.emit('search-center-error', { reason: 'service-unavailable' });
      return;
    }

    root.dataset.dsgSearchCenterReady = 'true';
    root.classList.add('is-loading');

    const queryInput = root.querySelector('[data-search-query]');
    const typeFilter = root.querySelector('[data-search-type]');
    const yearFilter = root.querySelector('[data-search-year]');
    const targetFilter = root.querySelector('[data-search-target]');
    const qualityFilter = root.querySelector('[data-search-quality]');
    const resetButton = root.querySelector('[data-search-reset]');
    const statusNode = root.querySelector('[data-search-status]');
    const resultNode = root.querySelector('[data-search-results]');
    const statsNode = root.querySelector('[data-search-stats]');

    let timer = null;

    const fillSelect = (select, values) => {
      values.forEach((value) => {
        select.insertAdjacentHTML('beforeend', `<option value="${escapeHtml(value)}">${escapeHtml(value)}</option>`);
      });
    };

    const filters = () => ({
      type: typeFilter.value,
      year: yearFilter.value,
      target: targetFilter.value,
      quality: qualityFilter.value
    });

    const render = async () => {
      root.classList.add('is-searching');
      const query = queryInput.value.trim();
      const results = await service.search(query, { filters: filters(), limit: 50 });

      statusNode.textContent = query
        ? `${results.length} risultati per “${query}”`
        : `${results.length} risultati disponibili`;

      resultNode.innerHTML = results.length
        ? results.map((item) => `
          <article class="dsg-search-result is-${escapeHtml(item.type)}">
            <div class="dsg-search-result__meta">
              <span>${item.type === 'scientific-session' ? 'Sessione scientifica' : 'Documentazione'}</span>
              <span>${escapeHtml(item.section)}</span>
            </div>
            <h2><a href="${escapeHtml(item.location)}">${escapeHtml(item.title)}</a></h2>
            <p>${escapeHtml(excerpt(item.text))}</p>
            ${item.metadata ? `<div class="dsg-search-result__facts">
              <span>${escapeHtml(item.metadata.observationDate || '')}</span>
              <span>${escapeHtml(item.metadata.telescope || '')}</span>
              <span>${escapeHtml(item.metadata.camera || '')}</span>
              <span>${escapeHtml(item.metadata.filter || '')}</span>
            </div>` : ''}
          </article>`).join('')
        : '<div class="dsg-search-center__empty">Nessun risultato corrisponde ai criteri selezionati.</div>';

      const serviceStatus = service.getStatus();
      statsNode.textContent = `${serviceStatus.documentCount} documenti · ${serviceStatus.scientificCount} sessioni scientifiche`;
      root.classList.remove('is-searching');
      events?.emit('search-center-results', { query, resultCount: results.length, filters: filters() });
    };

    const scheduleRender = () => {
      window.clearTimeout(timer);
      timer = window.setTimeout(() => render().catch(handleError), 160);
    };

    const handleError = (error) => {
      console.error(error);
      root.classList.remove('is-loading', 'is-searching', 'is-ready');
      root.classList.add('is-error');
      statusNode.textContent = 'Ricerca non disponibile';
      resultNode.innerHTML = '<div class="dsg-search-center__error">Impossibile caricare gli indici federati.</div>';
      events?.emit('search-center-error', { message: error.message });
    };

    try {
      await service.load();
      const facets = await service.getFacets();
      fillSelect(typeFilter, facets.types);
      fillSelect(yearFilter, facets.years);
      fillSelect(targetFilter, facets.targets);
      fillSelect(qualityFilter, facets.qualities);

      [queryInput, typeFilter, yearFilter, targetFilter, qualityFilter]
        .forEach((control) => control.addEventListener('input', scheduleRender));

      resetButton.addEventListener('click', () => {
        queryInput.value = '';
        typeFilter.value = '';
        yearFilter.value = '';
        targetFilter.value = '';
        qualityFilter.value = '';
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

  if (window.DSG?.components) {
    window.DSG.components.register({
      name: 'search-center',
      order: 75,
      initialize
    });
  } else if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => initialize(), { once: true });
  } else {
    initialize();
  }
})();
