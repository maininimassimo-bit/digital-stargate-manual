(() => {
  'use strict';

  const VERSION = '2.0.0-rc2';
  const DEFAULT_LIMIT = 20;
  const SCRIPT_URL = document.currentScript?.src || null;
  const SITE_ROOT = SCRIPT_URL
    ? new URL('../', SCRIPT_URL)
    : new URL('./', document.baseURI);
  const MKDOCS_INDEX_URL = new URL('search/search_index.json', SITE_ROOT);
  const SCIENTIFIC_CATALOG_URL = new URL('data/scientific-session-catalog.json', SITE_ROOT);

  const state = {
    documents: [],
    scientific: [],
    loaded: false,
    loading: null,
    metrics: {
      loads: 0,
      queries: 0,
      failures: 0,
      documentCount: 0,
      scientificCount: 0
    }
  };

  const eventBus = () => window.DSG?.events || null;
  const emit = (type, detail = {}) => eventBus()?.emit(`search-${type}`, { version: VERSION, ...detail });

  const decodeHtml = (value) => {
    const textarea = document.createElement('textarea');
    textarea.innerHTML = String(value || '');
    return textarea.value;
  };

  const stripHtml = (value) => decodeHtml(String(value || '')
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' '))
    .replace(/\s+/g, ' ')
    .trim();

  const normalizeText = (value) => stripHtml(value)
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase();

  const tokenize = (value) => normalizeText(value)
    .split(/[^a-z0-9]+/)
    .filter((token) => token.length > 1);

  const unique = (values) => [...new Set(values.filter(Boolean))];

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
    if (/^<code>|\.parquet|enum|status$/i.test(String(title || '').trim())) return { section: 'Riferimento tecnico', priority: 20 };
    return { section: 'Documentazione', priority: 50 };
  };

  const scoreText = (queryTokens, fields) => {
    if (!queryTokens.length) return 0;
    const normalized = fields.map((field) => normalizeText(field));
    let score = 0;

    queryTokens.forEach((token) => {
      normalized.forEach((field, index) => {
        if (!field) return;
        if (field === token) score += 30 - index;
        else if (field.startsWith(token)) score += 18 - Math.min(index, 6);
        else if (field.includes(token)) score += 9 - Math.min(index, 4);
      });
    });

    return score;
  };

  const mapDocument = (doc) => {
    const title = stripHtml(doc.title || doc.location);
    const text = stripHtml(doc.text || '');
    const classification = classifyDocument(doc.location, title);

    return Object.freeze({
      id: `doc:${doc.location}`,
      type: 'documentation',
      title: title || doc.location,
      text,
      location: new URL(doc.location, SITE_ROOT).href,
      section: classification.section,
      priority: classification.priority,
      keywords: tokenize(`${title} ${text} ${classification.section}`)
    });
  };

  const mapScientificSession = (session) => Object.freeze({
    id: `science:${session.sessionId}`,
    type: 'scientific-session',
    title: `${session.target} · ${session.sessionId}`,
    text: [
      session.target,
      session.sessionId,
      session.telescope,
      session.camera,
      session.filter,
      session.configurationId,
      session.qualityState,
      session.observationDate
    ].filter(Boolean).join(' '),
    location: new URL(`scientific-session-detail/?sessionId=${encodeURIComponent(session.sessionId)}`, SITE_ROOT).href,
    section: 'Scientific Platform',
    priority: 88,
    keywords: unique([
      ...tokenize(session.target),
      ...tokenize(session.sessionId),
      ...tokenize(session.telescope),
      ...tokenize(session.camera),
      ...tokenize(session.filter),
      String(session.observationDate || '').slice(0, 4),
      normalizeText(session.qualityState)
    ]),
    metadata: Object.freeze({
      sessionId: session.sessionId,
      target: session.target,
      observationDate: session.observationDate,
      telescope: session.telescope,
      camera: session.camera,
      filter: session.filter,
      qualityState: session.qualityState
    })
  });

  const loadMkDocsIndex = async () => {
    const response = await fetch(MKDOCS_INDEX_URL, { cache: 'no-store' });
    if (!response.ok) throw new Error(`Search index request failed: ${response.status}`);
    const payload = await response.json();
    return (payload.docs || []).map(mapDocument);
  };

  const loadScientificIndex = async () => {
    const engine = window.DSGScientificDataEngine;
    if (!engine) return [];

    const candidates = [
      document.querySelector('[data-session-catalog]')?.dataset.sessionCatalog,
      document.querySelector('[data-session-detail]')?.dataset.sessionCatalog,
      SCIENTIFIC_CATALOG_URL.href
    ];

    const source = candidates.find(Boolean);
    if (!source) return [];

    try {
      const sessions = await engine.getSessions(source);
      return sessions.map(mapScientificSession);
    } catch (error) {
      emit('source-degraded', { source: 'scientific', message: error.message });
      return [];
    }
  };

  const load = async (options = {}) => {
    if (state.loaded && !options.force) return getStatus();
    if (state.loading && !options.force) return state.loading;

    state.metrics.loads += 1;
    emit('load-start');

    state.loading = Promise.all([loadMkDocsIndex(), loadScientificIndex()])
      .then(([documents, scientific]) => {
        state.documents = documents;
        state.scientific = scientific;
        state.loaded = true;
        state.metrics.documentCount = documents.length;
        state.metrics.scientificCount = scientific.length;
        emit('load-ready', getStatus());
        return getStatus();
      })
      .catch((error) => {
        state.metrics.failures += 1;
        emit('load-error', { message: error.message });
        throw error;
      })
      .finally(() => {
        state.loading = null;
      });

    return state.loading;
  };

  const matchesFilters = (entry, filters = {}) => {
    if (filters.type && entry.type !== filters.type) return false;
    if (filters.section && entry.section !== filters.section) return false;

    if (entry.type === 'scientific-session') {
      const meta = entry.metadata || {};
      if (filters.year && !String(meta.observationDate || '').startsWith(String(filters.year))) return false;
      if (filters.target && meta.target !== filters.target) return false;
      if (filters.quality && meta.qualityState !== filters.quality) return false;
    }

    return true;
  };

  const search = async (query, options = {}) => {
    await load();
    state.metrics.queries += 1;

    const queryTokens = tokenize(query);
    const limit = Number.isFinite(options.limit) ? options.limit : DEFAULT_LIMIT;
    const corpus = [...state.documents, ...state.scientific];

    const results = corpus
      .filter((entry) => matchesFilters(entry, options.filters))
      .map((entry) => {
        const relevance = scoreText(queryTokens, [entry.title, entry.section, entry.keywords.join(' '), entry.text]);
        return {
          ...entry,
          score: relevance + (queryTokens.length ? Math.round(entry.priority / 4) : entry.priority)
        };
      })
      .filter((entry) => queryTokens.length === 0 || entry.score > Math.round(entry.priority / 4))
      .sort((left, right) => right.score - left.score || left.title.localeCompare(right.title, 'it'))
      .slice(0, limit);

    emit('query-complete', {
      query,
      resultCount: results.length,
      filters: options.filters || {},
      limit
    });

    return results;
  };

  const getFacets = async () => {
    await load();
    return Object.freeze({
      types: Object.freeze(unique([...state.documents, ...state.scientific].map((entry) => entry.type)).sort()),
      sections: Object.freeze(unique([...state.documents, ...state.scientific].map((entry) => entry.section)).sort()),
      targets: Object.freeze(unique(state.scientific.map((entry) => entry.metadata?.target)).sort()),
      years: Object.freeze(unique(state.scientific.map((entry) => String(entry.metadata?.observationDate || '').slice(0, 4))).sort().reverse()),
      qualities: Object.freeze(unique(state.scientific.map((entry) => entry.metadata?.qualityState)).sort())
    });
  };

  const getStatus = () => Object.freeze({
    version: VERSION,
    loaded: state.loaded,
    loading: Boolean(state.loading),
    documentCount: state.metrics.documentCount,
    scientificCount: state.metrics.scientificCount,
    totalCount: state.metrics.documentCount + state.metrics.scientificCount,
    metrics: Object.freeze({ ...state.metrics })
  });

  const clear = () => {
    state.documents = [];
    state.scientific = [];
    state.loaded = false;
    emit('cache-cleared');
  };

  window.DSGSearchService = Object.freeze({
    version: VERSION,
    load,
    search,
    getFacets,
    getStatus,
    clear
  });

  const initialize = ({ events } = {}) => {
    events?.emit('search-service-ready', { version: VERSION });
  };

  if (window.DSG?.components) {
    window.DSG.components.register({
      name: 'search-service',
      order: 45,
      initialize
    });
  } else {
    initialize();
  }
})();
