(() => {
  const cache = new Map();

  const normalize = (catalog) => ({
    ...catalog,
    sessions: [...(catalog.sessions || [])]
      .map((session) => ({ ...session }))
      .sort((a, b) => String(b.observationDate).localeCompare(String(a.observationDate)))
  });

  const loadCatalog = async (source) => {
    if (!source) throw new Error('Scientific Data Engine: catalog source is required.');
    if (!cache.has(source)) {
      cache.set(source, fetch(source).then((response) => {
        if (!response.ok) throw new Error(`Catalog request failed: ${response.status}`);
        return response.json();
      }).then(normalize));
    }
    return cache.get(source);
  };

  const getSessions = async (source) => (await loadCatalog(source)).sessions;
  const getSession = async (source, sessionId) => {
    const sessions = await getSessions(source);
    return sessions.find((session) => session.sessionId === sessionId) || null;
  };

  const getTargets = async (source) => [...new Set((await getSessions(source)).map((session) => session.target))].sort();
  const getYears = async (source) => [...new Set((await getSessions(source)).map((session) => String(session.observationDate).slice(0, 4)))].sort().reverse();

  const getKPIs = async (source) => {
    const sessions = await getSessions(source);
    return {
      sessionCount: sessions.length,
      targetCount: new Set(sessions.map((session) => session.target)).size,
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

  const clearCache = (source) => source ? cache.delete(source) : cache.clear();

  window.DSGScientificDataEngine = Object.freeze({
    loadCatalog,
    getSessions,
    getSession,
    getTargets,
    getYears,
    getKPIs,
    filterSessions,
    getKnowledgeGraph,
    getLineage,
    clearCache
  });
})();
