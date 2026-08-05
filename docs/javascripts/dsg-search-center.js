(() => {
  'use strict';

  const HISTORY_KEY = 'dsg.enterpriseSearch.history.v1';
  const MAX_HISTORY = 8;

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

  const downloadText = (filename, content, mimeType) => {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = filename;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    URL.revokeObjectURL(url);
  };

  const csvCell = (value) => `"${String(value ?? '').replace(/"/g, '""')}"`;

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
    const toolbar = scope.querySelector('.dsg-search-center__toolbar');

    const controls = { queryInput, typeFilter, yearFilter, targetFilter, qualityFilter, resetButton, statusNode, resultNode, statsNode, filterPanel, toolbar };
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
      <label>Filtro<select data-search-filter><option value="">Tutti i filtri</option></select></label>
      <label>Telescopio<select data-search-telescope><option value="">Tutti i telescopi</option></select></label>
      <label>Camera<select data-search-camera><option value="">Tutte le camere</option></select></label>
      <label>Ordina per<select data-search-sort>
        <option value="relevance">Rilevanza</option><option value="year-desc">Data più recente</option>
        <option value="quality">Qualità</option><option value="title">Titolo</option>
      </select></label>`);

    resetButton.insertAdjacentHTML('beforebegin', `
      <button class="dsg-search-center__reset" type="button" data-search-export-json>Esporta JSON</button>
      <button class="dsg-search-center__reset" type="button" data-search-export-csv>Esporta CSV</button>
      <button class="dsg-search-center__reset" type="button" data-search-share>Condividi ricerca</button>`);

    toolbar.insertAdjacentHTML('afterend', `
      <section class="dsg-search-center__history" data-search-history hidden><strong>Ricerche recenti</strong><div data-search-history-items></div></section>
      <aside class="dsg-search-center__detail" data-search-detail hidden aria-live="polite"></aside>`);

    const filterFilter = scope.querySelector('[data-search-filter]');
    const telescopeFilter = scope.querySelector('[data-search-telescope]');
    const cameraFilter = scope.querySelector('[data-search-camera]');
    const sortFilter = scope.querySelector('[data-search-sort]');
    const shareButton = scope.querySelector('[data-search-share]');
    const exportJsonButton = scope.querySelector('[data-search-export-json]');
    const exportCsvButton = scope.querySelector('[data-search-export-csv]');
    const historyPanel = scope.querySelector('[data-search-history]');
    const historyItems = scope.querySelector('[data-search-history-items]');
    const detailPanel = scope.querySelector('[data-search-detail]');

    const suggestionList = document.createElement('datalist');
    suggestionList.id = 'dsg-search-suggestions';
    queryInput.setAttribute('list', suggestionList.id);
    queryInput.insertAdjacentElement('afterend', suggestionList);
    queryInput.placeholder = 'Cerca oppure usa target:, year:, filter:, quality:, telescope:…';

    root.dataset.dsgSearchCenterReady = 'true';
    root.classList.add('is-loading');
    let timer = null;
    let restoringState = false;
    let lastResults = [];
    let selectedResultIndex = -1;

    const fillSelect = (select, values) => {
      select.querySelectorAll('option:not(:first-child)').forEach((option) => option.remove());
      values.forEach((value) => select.insertAdjacentHTML('beforeend', `<option value="${escapeHtml(value)}">${escapeHtml(value)}</option>`));
    };

    const controlsByParameter = { type: typeFilter, year: yearFilter, target: targetFilter, quality: qualityFilter, filter: filterFilter, telescope: telescopeFilter, camera: cameraFilter, sort: sortFilter };
    const filters = () => ({ type: typeFilter.value, year: yearFilter.value, target: targetFilter.value, quality: qualityFilter.value, filter: filterFilter.value, telescope: telescopeFilter.value, camera: cameraFilter.value });

    const buildSearchUrl = () => {
      const url = new URL(window.location.href);
      const parameters = new URLSearchParams();
      if (queryInput.value.trim()) parameters.set('q', queryInput.value.trim());
      Object.entries(controlsByParameter).forEach(([name, control]) => {
        const value = control.value;
        if (value && !(name === 'sort' && value === 'relevance')) parameters.set(name, value);
      });
      url.search = parameters.toString();
      url.hash = 'enterprise-search-center';
      return url;
    };

    const currentState = () => ({ query: queryInput.value.trim(), filters: filters(), sort: sortFilter.value, url: buildSearchUrl().href });
    const loadHistory = () => {
      try { const value = JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]'); return Array.isArray(value) ? value : []; }
      catch { return []; }
    };
    const renderHistory = () => {
      const history = loadHistory();
      historyPanel.hidden = history.length === 0;
      historyItems.innerHTML = history.map((item, index) => `<button type="button" class="dsg-search-center__reset" data-search-history-index="${index}">${escapeHtml(item.label)}</button>`).join('');
    };
    const saveHistory = () => {
      const state = currentState();
      if (!(state.query || Object.values(state.filters).some(Boolean) || state.sort !== 'relevance')) return;
      const label = state.query || [state.filters.target, state.filters.year, state.filters.filter, state.filters.quality].filter(Boolean).join(' · ') || 'Ricerca filtrata';
      const history = loadHistory().filter((entry) => entry.url !== state.url);
      history.unshift({ ...state, label, savedAt: new Date().toISOString() });
      localStorage.setItem(HISTORY_KEY, JSON.stringify(history.slice(0, MAX_HISTORY)));
      renderHistory();
    };

    const persistUrlState = () => {
      if (restoringState) return;
      const url = buildSearchUrl();
      window.history.replaceState({ dsgSearch: true }, '', url.href);
      events?.emit('search-center-url-updated', { url: url.href });
    };
    const restoreUrlState = () => {
      restoringState = true;
      const parameters = new URLSearchParams(window.location.search);
      queryInput.value = parameters.get('q') || '';
      Object.entries(controlsByParameter).forEach(([name, control]) => {
        const value = parameters.get(name);
        control.value = value && [...control.options].some((option) => option.value === value) ? value : (name === 'sort' ? 'relevance' : '');
      });
      restoringState = false;
    };
    const applyState = (state) => {
      restoringState = true;
      queryInput.value = state.query || '';
      Object.entries(controlsByParameter).forEach(([name, control]) => {
        const value = name === 'sort' ? state.sort : state.filters?.[name];
        control.value = value && [...control.options].some((option) => option.value === value) ? value : (name === 'sort' ? 'relevance' : '');
      });
      restoringState = false;
    };

    const rankingExplanation = (item) => {
      const explanation = item.scoreExplanation;
      if (!explanation) return '';
      const terms = explanation.matchedTerms?.length ? ` · termini: ${explanation.matchedTerms.join(', ')}` : '';
      return `<details class="dsg-search-result__explanation"><summary>Perché questo risultato?</summary><p>Punteggio ${escapeHtml(item.score)}: testo ${escapeHtml(explanation.text)}, autorità ${escapeHtml(explanation.authority)}, qualità ${escapeHtml(explanation.quality)}${escapeHtml(terms)}.</p></details>`;
    };

    const contextualLinks = (item) => {
      const metadata = item.metadata || {};
      return [['target', metadata.target], ['year', metadata.year], ['telescope', metadata.telescope], ['camera', metadata.camera], ['filter', metadata.filter], ['quality', metadata.qualityState]]
        .filter(([, value]) => value)
        .map(([name, value]) => `<button type="button" class="dsg-search-center__reset" data-search-context-name="${name}" data-search-context-value="${escapeHtml(value)}">${escapeHtml(name)}: ${escapeHtml(value)}</button>`)
        .join('');
    };

    const showDetail = (index, { focus = true } = {}) => {
      const item = lastResults[index];
      if (!item) return;
      selectedResultIndex = index;
      const typeLabel = item.type === 'scientific-session' ? 'Sessione scientifica' : 'Documentazione';
      const previousDisabled = index <= 0 ? ' disabled' : '';
      const nextDisabled = index >= lastResults.length - 1 ? ' disabled' : '';
      detailPanel.hidden = false;
      detailPanel.innerHTML = `
        <nav aria-label="Percorso risultato"><a href="#enterprise-search-center">Search Center</a> <span aria-hidden="true">›</span> <span>${escapeHtml(item.section || typeLabel)}</span> <span aria-hidden="true">›</span> <strong>${escapeHtml(item.title)}</strong></nav>
        <div class="dsg-search-result__meta"><span>${typeLabel}</span><span>${escapeHtml(item.section)}</span><span>Score ${escapeHtml(item.score)}</span></div>
        <h2 tabindex="-1" data-search-detail-title>${escapeHtml(item.title)}</h2>
        <p>${escapeHtml(item.text || '')}</p>
        ${item.type === 'scientific-session' ? `<div class="dsg-search-result__facts">${contextualLinks(item)}</div>` : ''}
        ${rankingExplanation(item)}
        <div class="dsg-search-center__toolbar">
          <div><button type="button" class="dsg-search-center__reset" data-search-detail-previous${previousDisabled}>Precedente</button> <button type="button" class="dsg-search-center__reset" data-search-detail-next${nextDisabled}>Successivo</button></div>
          <div><a class="dsg-search-center__reset" href="${escapeHtml(item.location)}">Apri contenuto</a> <button type="button" class="dsg-search-center__reset" data-search-detail-close>Chiudi</button></div>
        </div>`;
      if (focus) detailPanel.querySelector('[data-search-detail-title]')?.focus({ preventScroll: true });
      events?.emit('search-center-detail-opened', { index, type: item.type, location: item.location });
    };

    const closeDetail = () => {
      detailPanel.hidden = true;
      detailPanel.innerHTML = '';
      selectedResultIndex = -1;
      events?.emit('search-center-detail-closed');
    };

    const render = async ({ persist = true, remember = true } = {}) => {
      root.classList.add('is-searching');
      const query = queryInput.value.trim();
      const results = await service.search(query, { filters: filters(), sort: sortFilter.value, limit: 50 });
      const parsed = service.parseQuery?.(query);
      lastResults = results;
      closeDetail();
      statusNode.textContent = query ? `${results.length} risultati per “${query}”` : `${results.length} risultati disponibili`;
      resultNode.innerHTML = results.length ? results.map((item, index) => `
        <article class="dsg-search-result is-${escapeHtml(item.type)}">
          <div class="dsg-search-result__meta"><span>${item.type === 'scientific-session' ? 'Sessione scientifica' : 'Documentazione'}</span><span>${escapeHtml(item.section)}</span><span>Score ${escapeHtml(item.score)}</span></div>
          <h2><a href="${escapeHtml(item.location)}">${escapeHtml(item.title)}</a></h2>
          <p>${escapeHtml(excerpt(item.text))}</p>
          ${item.type === 'scientific-session' ? `<div class="dsg-search-result__facts"><span>${escapeHtml(item.metadata?.year || '')}</span><span>${escapeHtml(item.metadata?.target || '')}</span><span>${escapeHtml(item.metadata?.telescope || '')}</span><span>${escapeHtml(item.metadata?.camera || '')}</span><span>${escapeHtml(item.metadata?.filter || '')}</span><span>${escapeHtml(item.metadata?.qualityState || '')}</span></div>` : ''}
          ${rankingExplanation(item)}
          <button type="button" class="dsg-search-center__reset" data-search-detail-index="${index}">Dettagli e navigazione</button>
        </article>`).join('') : '<div class="dsg-search-center__empty">Nessun risultato corrisponde ai criteri selezionati.</div>';
      const serviceStatus = service.getStatus();
      const structuredCount = Object.keys(parsed?.filters || {}).length;
      statsNode.textContent = `${serviceStatus.documentCount} documenti · ${serviceStatus.scientificCount} sessioni scientifiche${structuredCount ? ` · ${structuredCount} filtri nella query` : ''}`;
      root.classList.remove('is-searching');
      if (persist) persistUrlState();
      if (remember) saveHistory();
      events?.emit('search-center-results', { query, parsed, resultCount: results.length, filters: filters(), sort: sortFilter.value });
      return results;
    };

    const exportResults = (format) => {
      const state = currentState();
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      if (format === 'json') downloadText(`dsg-search-${timestamp}.json`, JSON.stringify({ generatedAt: new Date().toISOString(), search: state, results: lastResults }, null, 2), 'application/json');
      else {
        const rows = [['type', 'section', 'title', 'url', 'score', 'target', 'year', 'telescope', 'camera', 'filter', 'quality']];
        lastResults.forEach((item) => rows.push([item.type, item.section, item.title, item.location, item.score, item.metadata?.target, item.metadata?.year, item.metadata?.telescope, item.metadata?.camera, item.metadata?.filter, item.metadata?.qualityState]));
        downloadText(`dsg-search-${timestamp}.csv`, rows.map((row) => row.map(csvCell).join(',')).join('\n'), 'text/csv;charset=utf-8');
      }
      events?.emit('search-center-export', { format, resultCount: lastResults.length });
    };

    const handleError = (error) => {
      console.error(error);
      root.classList.remove('is-loading', 'is-searching', 'is-ready');
      root.classList.add('is-error');
      statusNode.textContent = 'Ricerca non disponibile';
      resultNode.innerHTML = '<div class="dsg-search-center__error">Impossibile caricare gli indici federati.</div>';
      events?.emit('search-center-error', { message: error.message });
    };
    const scheduleRender = () => { window.clearTimeout(timer); timer = window.setTimeout(() => render().catch(handleError), 160); };

    try {
      await service.load();
      const facets = await service.getFacets();
      fillSelect(typeFilter, facets.types); fillSelect(yearFilter, facets.years); fillSelect(targetFilter, facets.targets); fillSelect(qualityFilter, facets.qualities);
      fillSelect(filterFilter, facets.filters || []); fillSelect(telescopeFilter, facets.telescopes || []); fillSelect(cameraFilter, facets.cameras || []);
      const suggestions = [...(facets.targets || []).map((value) => `target:${value}`), ...(facets.years || []).map((value) => `year:${value}`), ...(facets.filters || []).map((value) => `filter:${value}`), ...(facets.qualities || []).map((value) => `quality:${value}`), ...(facets.telescopes || []).map((value) => `telescope:\"${value}\"`), ...(facets.cameras || []).map((value) => `camera:\"${value}\"`)];
      suggestionList.innerHTML = suggestions.map((value) => `<option value="${escapeHtml(value)}"></option>`).join('');
      restoreUrlState(); renderHistory();
      [queryInput, typeFilter, yearFilter, targetFilter, qualityFilter, filterFilter, telescopeFilter, cameraFilter, sortFilter].forEach((control) => control.addEventListener('input', scheduleRender));
      resetButton.addEventListener('click', () => { queryInput.value = ''; [typeFilter, yearFilter, targetFilter, qualityFilter, filterFilter, telescopeFilter, cameraFilter].forEach((control) => { control.value = ''; }); sortFilter.value = 'relevance'; render().catch(handleError); });
      shareButton.addEventListener('click', async () => {
        const url = buildSearchUrl();
        try { await navigator.clipboard.writeText(url.href); shareButton.textContent = 'Link copiato'; window.setTimeout(() => { shareButton.textContent = 'Condividi ricerca'; }, 1600); events?.emit('search-center-share', { url: url.href, method: 'clipboard' }); }
        catch { window.prompt('Copia il link della ricerca:', url.href); events?.emit('search-center-share', { url: url.href, method: 'prompt' }); }
      });
      exportJsonButton.addEventListener('click', () => exportResults('json'));
      exportCsvButton.addEventListener('click', () => exportResults('csv'));
      historyItems.addEventListener('click', (event) => { const button = event.target.closest('[data-search-history-index]'); if (!button) return; const item = loadHistory()[Number(button.dataset.searchHistoryIndex)]; if (!item) return; applyState(item); render().catch(handleError); });
      resultNode.addEventListener('click', (event) => { const button = event.target.closest('[data-search-detail-index]'); if (button) showDetail(Number(button.dataset.searchDetailIndex)); });
      detailPanel.addEventListener('click', (event) => {
        if (event.target.closest('[data-search-detail-close]')) closeDetail();
        else if (event.target.closest('[data-search-detail-previous]')) showDetail(selectedResultIndex - 1);
        else if (event.target.closest('[data-search-detail-next]')) showDetail(selectedResultIndex + 1);
        else {
          const context = event.target.closest('[data-search-context-name]');
          if (!context) return;
          const control = controlsByParameter[context.dataset.searchContextName];
          if (control) { control.value = context.dataset.searchContextValue; render().catch(handleError); }
        }
      });
      window.addEventListener('popstate', () => { restoreUrlState(); render({ persist: false, remember: false }).catch(handleError); });

      const api = Object.freeze({
        version: '1.1.0', search: (query, options = {}) => service.search(query, options),
        getState: () => Object.freeze({ ...currentState(), resultCount: lastResults.length, selectedResultIndex }),
        getResults: () => Object.freeze([...lastResults]), setState: async (state) => { applyState(state || {}); return render(); },
        openResult: (index) => showDetail(Number(index), { focus: false }), closeResult: closeDetail,
        exportJson: () => exportResults('json'), exportCsv: () => exportResults('csv'), clearHistory: () => { localStorage.removeItem(HISTORY_KEY); renderHistory(); }
      });
      window.DSGEnterpriseSearch = api;
      root.classList.remove('is-loading'); root.classList.add('is-ready');
      await render({ persist: false, remember: false });
      queryInput.focus({ preventScroll: true });
      events?.emit('search-center-ready', { ...service.getStatus(), apiVersion: api.version });
    } catch (error) { handleError(error); }
  };

  if (window.DSG?.components) window.DSG.components.register({ name: 'search-center', order: 75, initialize });
  else if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => initialize(), { once: true });
  else initialize();
})();