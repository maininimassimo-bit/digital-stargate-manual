(() => {
  'use strict';

  const VERSION = '2.1.0-rc2';
  const cache = new Map();
  const metrics = {
    requests: 0,
    networkLoads: 0,
    cacheHits: 0,
    failures: 0,
    invalidations: 0,
    indexBuilds: 0,
    indexedLookups: 0
  };

  const now = () => Date.now();
  const eventBus = () => window.DSG?.events || null;
  const emit = (type, detail = {}) => eventBus()?.emit(`science-${type}`, { version: VERSION, ...detail });

  const normalize = (catalog) => Object.freeze({
    ...catalog,
    sessions: Object.freeze([...(catalog.sessions || [])]
      .map((session) => Object.freeze({ ...session }))
      .sort((a, b) => String(b.observationDate).localeCompare(String(a.observationDate))))
  });

  const buildIndexes = (catalog) => {
    const byId = new Map();
    const byTarget = new Map();
    const byYear = new Map();

    catalog.sessions.forEach((session) => {
      byId.set(session.sessionId, session);

      const targetSessions = byTarget.get(session.target) || [];
      targetSessions.push(session);
      byTarget.set(session.target, targetSessions);

      const year = String(session.observationDate).slice(0, 4);
      const yearSessions = byYear.get(year) || [];
      yearSessions.push(session);
      byYear.set(year, yearSessions);
    });

    metrics.indexBuilds += 1;
    return Object.freeze({
      byId,
      byTarget,
      byYear,
      targets: Object.freeze([...byTarget.keys()].sort()),
      years: Object.freeze([...byYear.keys()].sort().reverse())
    });
  };

  const snapshot = (source, entry) => ({
    source,
    state: entry?.state || 'idle',
    loadedAt: entry?.loadedAt || null,
    durationMs: entry?.durationMs ?? null,
    sessionCount: entry?.catalog?.sessions?.length ?? null,
    targetCount: entry?.indexes?.targets?.length ?? null,
    yearCount: entry?.indexes?.years?.length ?? null,
    error: entry?.error?.message || null
  });

  const loadCatalog = async (source, options = {}) => {
    if (!source) throw new Error('Scientific Data Engine: catalog source is required.');

    metrics.requests += 1;
    const { force = false, maxAgeMs = Infinity, signal } = options;
    const existing = cache.get(source);
    const fresh = existing?.state === 'ready'
      && now() - existing.loadedAt <= maxAgeMs;

    if (!force && (fresh || existing?.state === 'loading')) {
      metrics.cacheHits += 1;
      emit('cache-hit', snapshot(source, existing));
      return existing.promise;
    }

    if (force && existing) {
      cache.delete(source);
      metrics.invalidations += 1;
      emit('cache-invalidated', { source, reason: 'forced-reload' });
    }

    const startedAt = now();
    const entry = {
      state: 'loading',
      loadedAt: null,
      durationMs: null,
      catalog: null,
      indexes: null,
      error: null,
      promise: null
    };

    metrics.networkLoads += 1;
    emit('load-start', { source });

    entry.promise = fetch(source, { signal })
      .then((response) => {
        if (!response.ok) throw new Error(`Catalog request failed: ${response.status}`);
        return response.json();
      })
      .then(normalize)
      .then((catalog) => {
        entry.state = 'ready';
        entry.loadedAt = now();
        entry.durationMs = entry.loadedAt - startedAt;
        entry.catalog = catalog;
        entry.indexes = buildIndexes(catalog);
        emit('store-ready', snapshot(source, entry));
        emit('load-ready', snapshot(source, entry));
        return catalog;
      })
      .catch((error) => {
        entry.state = 'error';
        entry.durationMs = now() - startedAt;
        entry.error = error;
        metrics.failures += 1;
        emit('load-error', snapshot(source, entry));
        throw error;
      });

    cache.set(source, entry);
    return entry.promise;
  };

  const ensureEntry = async (source, options) => {
    await loadCatalog(source, options);
    return cache.get(source);
  };

  const preload = (sources, options = {}) => Promise.all(
    [...new Set(Array.isArray(sources) ? sources : [sources])]
      .filter(Boolean)
      .map((source) => loadCatalog(source, options))
  );

  const getSessions = async (source, options) => (await loadCatalog(source, options)).sessions;

  const getSession = async (source, sessionId, options) => {
    const entry = await ensureEntry(source, options);
    metrics.indexedLookups += 1;
    return entry.indexes.byId.get(sessionId) || null;
  };

  const getTargets = async (source, options) => {
    const entry = await ensureEntry(source, options);
    metrics.indexedLookups += 1;
    return [...entry.indexes.targets];
  };

  const getYears = async (source, options) => {
    const entry = await ensureEntry(source, options);
    metrics.indexedLookups += 1;
    return [...entry.indexes.years];
  };

  const getSessionsByTarget = async (source, target, options) => {
    const entry = await ensureEntry(source, options);
    metrics.indexedLookups += 1;
    return [...(entry.indexes.byTarget.get(target) || [])];
  };

  const getSessionsByYear = async (source, year, options) => {
    const entry = await ensureEntry(source, options);
    metrics.indexedLookups += 1;
    return [...(entry.indexes.byYear.get(String(year)) || [])];
  };

  const getKPIs = async (source, options) => {
    const entry = await ensureEntry(source, options);
    const sessions = entry.catalog.sessions;
    return {
      sessionCount: sessions.length,
      targetCount: entry.indexes.targets.length,
      integrationHours: sessions.reduce((sum, session) => sum + Number(session.integrationHours || 0), 0),
      validatedCount: sessions.filter((session) => session.qualityState === 'VALIDATED_ANALYTICS').length
    };
  };

  const filterSessions = (sessions, filters = {}) => {
    const query = String(filters.query || '').trim().toLowerCase();
    return sessions.filter((session) => {
      const haystack = [session.sessionId, session.target, session.telescope, session.camera, session.filter, session.configurationId]
        .join(' ').toLowerCase();
      return (!query || haystack.includes(query))
        && (!filters.year || String(session.observationDate).startsWith(filters.year))
        && (!filters.target || session.target === filters.target)
        && (!filters.quality || session.qualityState === filters.quality);
    });
  };

  const querySessions = async (source, filters = {}, options) => {
    let sessions;
    if (filters.target) sessions = await getSessionsByTarget(source, filters.target, options);
    else if (filters.year) sessions = await getSessionsByYear(source, filters.year, options);
    else sessions = await getSessions(source, options);
    return filterSessions(sessions, filters);
  };

  const getKnowledgeGraph = (session) => ({
    target: { type: 'TARGET', id: session.target, label: session.target },
    session: { type: 'SESSION', id: session.sessionId, label: session.sessionId },
    equipment: [
      { type: 'TELESCOPE', id: session.telescope, label: session.telescope },
      { type: 'CAMERA', id: session.camera, label: session.camera },
      { type: 'FILTER', id: session.filter, label: session.filter }
    ],
    outputs: [
      { type: 'METRICS', state: session.evidenceState, available: true },
      { type: 'MANIFEST', state: session.manifestState, available: false },
      { type: 'TRANSFER', state: session.transferState, available: false }
    ]
  });

  const getLineage = (session) => [
    { label: 'Observation session', state: 'represented', detail: session.sessionId },
    { label: 'Acquisition metrics', state: 'represented', detail: `${session.lightCompleted} completed light frames` },
    { label: 'Scientific assets', state: 'partial', detail: 'paths and binary inventory not exposed in this catalog' },
    { label: 'Manifest', state: 'missing', detail: session.manifestState },
    { label: 'Processing', state: 'missing', detail: 'not represented' },
    { label: 'Publication', state: 'missing', detail: 'not represented' }
  ];

  const clearCache = (source) => {
    const hadEntries = source ? cache.has(source) : cache.size > 0;
    if (source) cache.delete(source);
    else cache.clear();

    if (hadEntries) {
      metrics.invalidations += 1;
      emit('cache-invalidated', { source: source || '*', reason: 'manual' });
    }
    return hadEntries;
  };

  const getStatus = (source) => source
    ? snapshot(source, cache.get(source))
    : [...cache.entries()].map(([key, entry]) => snapshot(key, entry));

  const getMetrics = () => Object.freeze({
    ...metrics,
    cacheEntries: cache.size,
    readyEntries: [...cache.values()].filter((entry) => entry.state === 'ready').length,
    errorEntries: [...cache.values()].filter((entry) => entry.state === 'error').length,
    indexedSessions: [...cache.values()].reduce((sum, entry) => sum + (entry.indexes?.byId?.size || 0), 0)
  });

  window.DSGScientificDataEngine = Object.freeze({
    version: VERSION,
    loadCatalog,
    preload,
    getSessions,
    getSession,
    getTargets,
    getYears,
    getSessionsByTarget,
    getSessionsByYear,
    getKPIs,
    filterSessions,
    querySessions,
    getKnowledgeGraph,
    getLineage,
    clearCache,
    getStatus,
    getMetrics
  });

  emit('engine-ready', { capabilities: ['cache', 'events', 'metrics', 'preload', 'session-store', 'indexes', 'query'] });
})();
