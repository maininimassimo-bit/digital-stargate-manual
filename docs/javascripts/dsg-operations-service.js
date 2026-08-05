(() => {
  'use strict';

  const VERSION = '1.0.0-rc2';
  const startedAt = Date.now();
  const eventCounts = new Map();
  const recentEvents = [];
  const MAX_RECENT_EVENTS = 50;

  const nowIso = () => new Date().toISOString();
  const eventBus = () => window.DSG?.events || null;

  const recordEvent = (type, detail = {}) => {
    eventCounts.set(type, (eventCounts.get(type) || 0) + 1);
    recentEvents.unshift(Object.freeze({ type, detail, observedAt: nowIso() }));
    if (recentEvents.length > MAX_RECENT_EVENTS) recentEvents.length = MAX_RECENT_EVENTS;
  };

  const trackedEvents = [
    'component-registered',
    'component-ready',
    'component-error',
    'lifecycle-start',
    'lifecycle-ready',
    'science-load-ready',
    'science-load-error',
    'science-cache-hit',
    'science-store-ready',
    'search-load-ready',
    'search-load-error',
    'search-query-complete',
    'theme-change',
    'latest-observation-ready',
    'latest-observation-degraded'
  ];

  const bindTelemetry = () => {
    const events = eventBus();
    if (!events || bindTelemetry.bound) return;
    bindTelemetry.bound = true;

    trackedEvents.forEach((type) => {
      events.on(type, (detail) => recordEvent(type, detail));
    });
  };

  const getComponentHealth = () => {
    const status = window.DSG?.components?.status?.() || [];
    const totals = status.reduce((acc, component) => {
      acc.total += 1;
      acc[component.state] = (acc[component.state] || 0) + 1;
      return acc;
    }, { total: 0, ready: 0, error: 0, registered: 0 });

    return Object.freeze({
      totals: Object.freeze(totals),
      components: Object.freeze(status.map((item) => Object.freeze({ ...item })))
    });
  };

  const getScientificHealth = () => {
    const engine = window.DSGScientificDataEngine;
    if (!engine) return Object.freeze({ available: false, status: [], metrics: null });

    return Object.freeze({
      available: true,
      version: engine.version || null,
      status: Object.freeze([...(engine.getStatus?.() || [])]),
      metrics: engine.getMetrics?.() || null
    });
  };

  const getSearchHealth = () => {
    const service = window.DSGSearchService;
    if (!service) return Object.freeze({ available: false, status: null });

    return Object.freeze({
      available: true,
      version: service.version || null,
      status: service.getStatus?.() || null
    });
  };

  const getThemeHealth = () => {
    const service = window.DSGThemeService;
    if (!service) return Object.freeze({ available: false, state: null });

    return Object.freeze({
      available: true,
      version: service.version || null,
      state: service.getTheme?.() || null
    });
  };

  const getAP013Status = () => Object.freeze({
    package: 'AP-013',
    capability: 'Scheduled COPY_ONLY',
    operatorReportedCompletion: true,
    repositoryEvidenceAvailable: false,
    validationState: 'PENDING_EVIDENCE_REVIEW',
    constraints: Object.freeze({
      mode: 'COPY_ONLY',
      maxFilesPerRun: 1,
      hashAlgorithm: 'SHA-256',
      overwriteExisting: false,
      sourceCleanupAuthorized: false
    })
  });

  const getTelemetry = () => Object.freeze({
    observedEventTypes: eventCounts.size,
    totalEvents: [...eventCounts.values()].reduce((sum, count) => sum + count, 0),
    counts: Object.freeze(Object.fromEntries(eventCounts)),
    recent: Object.freeze([...recentEvents])
  });

  const getSnapshot = () => Object.freeze({
    generatedAt: nowIso(),
    serviceVersion: VERSION,
    uptimeMs: Date.now() - startedAt,
    enterpriseCore: Object.freeze({
      available: Boolean(window.DSG),
      version: window.DSG?.version || null
    }),
    components: getComponentHealth(),
    scientific: getScientificHealth(),
    search: getSearchHealth(),
    theme: getThemeHealth(),
    ap013: getAP013Status(),
    telemetry: getTelemetry()
  });

  const getKPIs = () => {
    const snapshot = getSnapshot();
    const components = snapshot.components.totals;
    const scientificMetrics = snapshot.scientific.metrics || {};
    const searchStatus = snapshot.search.status || {};

    return Object.freeze({
      registeredComponents: components.total,
      readyComponents: components.ready,
      componentErrors: components.error,
      scientificSessionsIndexed: scientificMetrics.indexedSessions || 0,
      scientificFailures: scientificMetrics.failures || 0,
      searchDocuments: searchStatus.documentCount || 0,
      searchScientificEntries: searchStatus.scientificCount || 0,
      observedRuntimeEvents: snapshot.telemetry.totalEvents,
      ap013ValidationState: snapshot.ap013.validationState
    });
  };

  const refresh = () => {
    bindTelemetry();
    const snapshot = getSnapshot();
    eventBus()?.emit('operations-snapshot-ready', snapshot);
    return snapshot;
  };

  window.DSGOperationsService = Object.freeze({
    version: VERSION,
    getSnapshot,
    getKPIs,
    getTelemetry,
    refresh
  });

  const initialize = ({ events } = {}) => {
    bindTelemetry();
    events?.emit('operations-service-ready', {
      version: VERSION,
      capabilities: ['snapshot', 'kpi', 'runtime-events', 'component-health']
    });
  };

  if (window.DSG?.components) {
    window.DSG.components.register({
      name: 'operations-service',
      order: 50,
      initialize
    });
  } else {
    initialize();
  }
})();
