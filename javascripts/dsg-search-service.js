(() => {
  'use strict';

  const VERSION = '2.2.0-ap14-w04';
  const DEFAULT_LIMIT = 20;
  const QUERY_FIELDS = new Set(['target', 'year', 'filter', 'quality', 'type', 'section', 'telescope', 'camera', 'sort']);
  const SCRIPT_URL = document.currentScript?.src || null;
  const SITE_ROOT = SCRIPT_URL ? new URL('../', SCRIPT_URL) : new URL('./', document.baseURI);
  const MKDOCS_INDEX_URL = new URL('search/search_index.json', SITE_ROOT);
  const SCIENTIFIC_INDEX_URL = new URL('data/scientific-observation-index.json', SITE_ROOT);

  const state = {
    documents: [], scientific: [], loaded: false, loading: null, scientificIndex: null,
    metrics: { loads: 0, queries: 0, failures: 0, documentCount: 0, scientificCount: 0 }
  };

  const emit = (type, detail = {}) => window.DSG?.events?.emit(`search-${type}`, { version: VERSION, ...detail });
  const decodeHtml = (value) => { const node = document.createElement('textarea'); node.innerHTML = String(value || ''); return node.value; };
  const stripHtml = (value) => decodeHtml(String(value || '').replace(/<script[\s\S]*?<\/script>/gi, ' ').replace(/<style[\s\S]*?<\/style>/gi, ' ').replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim();
  const normalizeText = (value) => stripHtml(value).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const tokenize = (value) => normalizeText(value).split(/[^a-z0-9]+/).filter((token) => token.length > 1);
  const unique = (values) => [...new Set(values.filter(Boolean))];
  const firstFacet = (facets, name) => Array.isArray(facets?.[name]) ? facets[name][0] || null : null;

  const parseQuery = (query) => {
    const filters = {};
    const freeTerms = [];
    const tokens = String(query || '').match(/(?:[^\s"]+|"[^"]*")+/g) || [];

    for (const token of tokens) {
      const separator = token.indexOf(':');
      if (separator > 0) {
        const field = token.slice(0, separator).toLowerCase();
        const value = token.slice(separator + 1).replace(/^"|"$/g, '').trim();
        if (QUERY_FIELDS.has(field) && value) {
          filters[field] = value;
          continue;
        }
      }
      freeTerms.push(token.replace(/^"|"$/g, ''));
    }

    return Object.freeze({ raw: String(query || ''), text: freeTerms.join(' ').trim(), filters: Object.freeze(filters) });
  };

  const classifyDocument = (location, title) => {
    const path = String(location || '').toLowerCase();
    const label = normalizeText(title);
    if (path.includes('roadmap')) return { section: 'Roadmap', priority: 100 };
    if (path.includes('/architecture/packages/') || /\bap-\d+/.test(label)) return { section: 'Architecture Package', priority: 95 };
    if (path.includes('/architecture/adr-') || /\badr-\d+/.test(label)) return { section: 'ADR', priority: 90 };
    if (path.includes('/architecture/assessments/') || /\barb-\d+/.test(label)) return { section: 'Assessment', priority: 86 };
    if (path.includes('/architecture/validation/')) return { section: 'Validation', priority: 84 };
    if (path.includes('/scientific-platform') || path.includes('/scientific-session')) return { section: 'Scientific Platform', priority: 82 };
    if (path.includes('/chapters/16-') || path.includes('sop')) return { section: 'SOP', priority: 80 };
    if (path.includes('/operations/')) return { section: 'Operations', priority: 78 };
    if (path.includes('/developer/')) return { section: 'Developer', priority: 68 };
    if (path.includes('/chapters/')) return { section: 'Manuale tecnico', priority: 64 };
    if (path.includes('/appendices/') || path.includes('/assets/')) return { section: 'Allegato tecnico', priority: 34 };
    return { section: 'Documentazione', priority: 50 };
  };

  const scoreText = (queryTokens, fields) => {
    if (!queryTokens.length) return { score: 0, matchedTerms: [] };
    const normalized = fields.map((field) => normalizeText(field));
    let score = 0;
    const matchedTerms = [];

    for (const token of queryTokens) {
      let tokenMatched = false;
      normalized.forEach((field, index) => {
        if (!field) return;
        if (field === token) { score += 30 - index; tokenMatched = true; }
        else if (field.startsWith(token)) { score += 18 - Math.min(index, 6); tokenMatched = true; }
        else if (field.includes(token)) { score += 9 - Math.min(index, 4); tokenMatched = true; }
      });
      if (tokenMatched) matchedTerms.push(token);
    }
    return { score, matchedTerms };
  };

  const mapDocument = (doc) => {
    const title = stripHtml(doc.title || doc.location);
    const text = stripHtml(doc.text || '');
    const classification = classifyDocument(doc.location, title);
    return Object.freeze({ id: `doc:${doc.location}`, type: 'documentation', title: title || doc.location, text,
      location: new URL(doc.location, SITE_ROOT).href, section: classification.section,
      priority: classification.priority, keywords: tokenize(`${title} ${text} ${classification.section}`), metadata: Object.freeze({}) });
  };

  const mapScientificDocument = (document) => {
    const facets = document.facetValues || {};
    const metadata = Object.freeze({
      target: firstFacet(facets, 'target'), year: firstFacet(facets, 'year'),
      telescope: firstFacet(facets, 'telescope'), camera: firstFacet(facets, 'camera'),
      filter: firstFacet(facets, 'filter'), qualityState: firstFacet(facets, 'quality'),
      catalogItemId: document.catalogItemId, indexBuildId: document.indexBuildId,
      sourceDigest: document.sourceDigest, rankingSignals: Object.freeze({ ...(document.rankingSignals || {}) })
    });
    return Object.freeze({ id: `science:${document.searchDocumentId}`, type: 'scientific-session',
      title: stripHtml(document.title), text: stripHtml(document.summary || document.normalizedText || ''),
      location: new URL(document.sourceUrl, SITE_ROOT).href, section: 'Scientific Platform', priority: 88,
      keywords: unique([...(document.keywords || []).map(normalizeText), ...tokenize(document.normalizedText || ''),
        normalizeText(metadata.target), normalizeText(metadata.telescope), normalizeText(metadata.camera),
        normalizeText(metadata.filter), normalizeText(metadata.qualityState), metadata.year]), metadata });
  };

  const loadJson = async (url, label) => {
    const response = await fetch(url, { cache: 'no-store' });
    if (!response.ok) throw new Error(`${label} request failed: ${response.status}`);
    return response.json();
  };

  const loadMkDocsIndex = async () => (await loadJson(MKDOCS_INDEX_URL, 'Search index')).docs?.map(mapDocument) || [];
  const loadScientificIndex = async () => {
    const payload = await loadJson(SCIENTIFIC_INDEX_URL, 'Scientific observation index');
    if (!Array.isArray(payload.searchDocuments)) throw new Error('Scientific observation index does not contain searchDocuments');
    state.scientificIndex = Object.freeze({ algorithmVersion: payload.algorithmVersion || null,
      sourceSnapshotDigest: payload.sourceSnapshotDigest || null, indexBuildId: payload.indexBuild?.indexBuildId || null,
      outputDigest: payload.indexBuild?.outputDigest || null, reconciliationMatched: payload.summary?.reconciliationMatched || 0 });
    return payload.searchDocuments.map(mapScientificDocument);
  };

  const load = async (options = {}) => {
    if (state.loaded && !options.force) return getStatus();
    if (state.loading && !options.force) return state.loading;
    state.metrics.loads += 1;
    emit('load-start');
    state.loading = Promise.all([loadMkDocsIndex(), loadScientificIndex()]).then(([documents, scientific]) => {
      state.documents = documents; state.scientific = scientific; state.loaded = true;
      state.metrics.documentCount = documents.length; state.metrics.scientificCount = scientific.length;
      emit('load-ready', getStatus()); return getStatus();
    }).catch((error) => { state.metrics.failures += 1; emit('load-error', { message: error.message }); throw error; })
      .finally(() => { state.loading = null; });
    return state.loading;
  };

  const matchesFilters = (entry, filters = {}) => {
    const meta = entry.metadata || {};
    if (filters.type && normalizeText(entry.type) !== normalizeText(filters.type)) return false;
    if (filters.section && normalizeText(entry.section) !== normalizeText(filters.section)) return false;
    if (filters.target && normalizeText(meta.target) !== normalizeText(filters.target)) return false;
    if (filters.year && String(meta.year || '') !== String(filters.year)) return false;
    if (filters.filter && normalizeText(meta.filter) !== normalizeText(filters.filter)) return false;
    if (filters.quality && normalizeText(meta.qualityState) !== normalizeText(filters.quality)) return false;
    if (filters.telescope && !normalizeText(meta.telescope).includes(normalizeText(filters.telescope))) return false;
    if (filters.camera && !normalizeText(meta.camera).includes(normalizeText(filters.camera))) return false;
    return true;
  };

  const sortResults = (results, sort) => {
    if (sort === 'title') return results.sort((a, b) => a.title.localeCompare(b.title, 'it'));
    if (sort === 'year-desc') return results.sort((a, b) => String(b.metadata?.year || '').localeCompare(String(a.metadata?.year || '')) || b.score - a.score);
    if (sort === 'quality') return results.sort((a, b) => Number(b.metadata?.rankingSignals?.qualityWeight || 0) - Number(a.metadata?.rankingSignals?.qualityWeight || 0) || b.score - a.score);
    return results.sort((a, b) => b.score - a.score || a.title.localeCompare(b.title, 'it'));
  };

  const search = async (query, options = {}) => {
    await load();
    state.metrics.queries += 1;
    const parsed = parseQuery(query);
    const filters = { ...(options.filters || {}), ...parsed.filters };
    const sort = filters.sort || options.sort || 'relevance';
    delete filters.sort;
    const queryTokens = tokenize(parsed.text);
    const limit = Number.isFinite(options.limit) ? options.limit : DEFAULT_LIMIT;

    const ranked = [...state.documents, ...state.scientific].filter((entry) => matchesFilters(entry, filters)).map((entry) => {
      const textScore = scoreText(queryTokens, [entry.title, entry.section, entry.keywords.join(' '), entry.text]);
      const authorityScore = queryTokens.length ? Math.round(entry.priority / 4) : entry.priority;
      const qualityScore = entry.type === 'scientific-session' ? Math.round(Number(entry.metadata?.rankingSignals?.qualityWeight || 0) * 10) : 0;
      return { ...entry, score: textScore.score + authorityScore + qualityScore,
        scoreExplanation: Object.freeze({ text: textScore.score, authority: authorityScore, quality: qualityScore,
          matchedTerms: Object.freeze(textScore.matchedTerms), structuredFilters: Object.freeze({ ...filters }) }) };
    }).filter((entry) => queryTokens.length === 0 || entry.scoreExplanation.text > 0);

    const results = sortResults(ranked, sort).slice(0, limit);
    emit('query-complete', { query, parsed, resultCount: results.length, filters, sort, limit });
    return results;
  };

  const getFacets = async () => {
    await load();
    const corpus = [...state.documents, ...state.scientific];
    return Object.freeze({
      types: Object.freeze(unique(corpus.map((entry) => entry.type)).sort()),
      sections: Object.freeze(unique(corpus.map((entry) => entry.section)).sort()),
      targets: Object.freeze(unique(state.scientific.map((entry) => entry.metadata.target)).sort()),
      years: Object.freeze(unique(state.scientific.map((entry) => entry.metadata.year)).sort().reverse()),
      filters: Object.freeze(unique(state.scientific.map((entry) => entry.metadata.filter)).sort()),
      telescopes: Object.freeze(unique(state.scientific.map((entry) => entry.metadata.telescope)).sort()),
      cameras: Object.freeze(unique(state.scientific.map((entry) => entry.metadata.camera)).sort()),
      qualities: Object.freeze(unique(state.scientific.map((entry) => entry.metadata.qualityState)).sort())
    });
  };

  const getStatus = () => Object.freeze({ version: VERSION, loaded: state.loaded, loading: Boolean(state.loading),
    documentCount: state.metrics.documentCount, scientificCount: state.metrics.scientificCount,
    totalCount: state.metrics.documentCount + state.metrics.scientificCount, scientificIndex: state.scientificIndex,
    supportedQueryFields: Object.freeze([...QUERY_FIELDS]), metrics: Object.freeze({ ...state.metrics }) });

  const clear = () => { state.documents = []; state.scientific = []; state.scientificIndex = null; state.loaded = false; emit('cache-cleared'); };

  window.DSGSearchService = Object.freeze({ version: VERSION, load, search, parseQuery, getFacets, getStatus, clear });
  const initialize = ({ events } = {}) => events?.emit('search-service-ready', { version: VERSION, queryFields: [...QUERY_FIELDS] });
  if (window.DSG?.components) window.DSG.components.register({ name: 'search-service', order: 45, initialize });
  else initialize();
})();
