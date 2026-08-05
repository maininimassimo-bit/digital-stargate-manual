(() => {
  'use strict';

  const VERSION = '2.1.0-ap14';
  const DEFAULT_LIMIT = 20;
  const SCRIPT_URL = document.currentScript?.src || null;
  const SITE_ROOT = SCRIPT_URL
    ? new URL('../', SCRIPT_URL)
    : new URL('./', document.baseURI);
  const MKDOCS_INDEX_URL = new URL('search/search_index.json', SITE_ROOT);
  const SCIENTIFIC_INDEX_URL = new URL('data/scientific-observation-index.json', SITE_ROOT);

  const state = {
    documents: [],
    scientific: [],
    loaded: false,
    loading: null,
    scientificIndex: null,
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
  const firstFacet = (facets, name) => Array.isArray(facets?.[name]) ? facets[name][0] || null : null;

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

  const mapScientificDocument = (document) => {
    const facets = document.facetValues || {};
    const target = firstFacet(facets, 'target');
    const year = firstFacet(facets, 'year');
    const telescope = firstFacet(facets, 'telescope');
    const camera = firstFacet(facets, 'camera');
    const filter = firstFacet(facets, 'filter');
    const qualityState = firstFacet(facets, 'quality');
    const sessionId = String(document.catalogItemId || '').replace(/^CAT-SESSION-/, '').replace(/-/g, '_');

    return Object.freeze({
      id: `science:${document.searchDocumentId}`,
      type: 'scientific-session',
      title: stripHtml(document.title),
      text: stripHtml(document.summary || document.normalizedText || ''),
      location: new URL(document.sourceUrl, SITE_ROOT).href,
      section: 'Scientific Platform',
      priority: 88,
      keywords: unique([
        ...(document.keywords || []).map(normalizeText),
        ...tokenize(document.normalizedText || ''),
        normalizeText(target),
        normalizeText(telescope),
        normalizeText(camera),
        normalizeText(filter),
        normalizeText(qualityState),
        year
      ]),
      metadata: Object.freeze({
        sessionId,
        target,
        observationDate: year,
        telescope,
        camera,
        filter,
        qualityState,
        catalogItemId: document.catalogItemId,
        indexBuildId: document.indexBuildId,
        sourceDigest: document.sourceDigest,
        rankingSignals: Object.freeze({ ...(document.rankingSignals || {}) })
      })
    });
  };

  const loadMkDocsIndex = async () => {
    const response = await fetch(MKDOCS_INDEX_URL, { cache: 'no-store' });
    if (!response.ok) throw new Error(`Search index request failed: ${response.status}`);
    const payload = await response.json();
    return (payload.docs || []).map(mapDocument);
  };

  const loadScientificIndex = async () => {
    const response = await fetch(SCIENTIFIC_INDEX_URL, { cache: 'no-store' });
    if (!response.ok) throw new Error(`Scientific observation index request failed: ${response.status}`);

    const payload = await response.json();
    if (!Array.isArray(payload.searchDocuments)) {
      throw new Error('Scientific observation index does not contain searchDocuments');
    }

    state.scientificIndex = Object.freeze({
      algorithmVersion: payload.algorithmVersion || null,
      sourceSnapshotDigest: payload.sourceSnapshotDigest || null,
      indexBuildId: payload.indexBuild?.indexBuildId || null,
      outputDigest: payload.indexBuild?.outputDigest || null,
      reconciliationMatched: payload.summary?.reconciliationMatched || 0
    });

    return payload.searchDocuments.map(mapScientificDocument);
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
      if (filters.year && String(meta.observationDate || '') !== String(filters.year)) return false;
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
        const scientificQualityBonus = entry.type === 'scientific-session'
          ? Math.round(Number(entry.metadata?.rankingSignals?.qualityWeight || 0) * 10)
          : 0;
        return {
          ...entry,
          score: relevance + (queryTokens.length ? Math.round(entry.priority / 4) : entry.priority) + scientificQualityBonus
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
      years: Object.freeze(unique(state.scientific.map((entry) => entry.metadata?.observationDate)).sort().reverse()),
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
    scientificIndex: state.scientificIndex,
    metrics: Object.freeze({ ...state.metrics })
  });

  const clear = () => {
    state.documents = [];
    state.scientific = [];
    state.scientificIndex = null;
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
