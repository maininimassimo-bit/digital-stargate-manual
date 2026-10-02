(() => {
  'use strict';

  const VERSION = '2.1.2-rc1';
  const engineScript = document.currentScript?.src;
  const workflowSource = engineScript ? new URL('../data/bkl049-public-workflows.json', engineScript).href : null;
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

  const representedState = (value) => {
    const normalized = String(value || '').trim().toUpperCase();
    return Boolean(normalized) && !['UNKNOWN', 'N/A', 'NOT_REPRESENTED', 'MISSING'].includes(normalized);
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
      { type: 'METRICS', state: session.evidenceState, available: representedState(session.evidenceState) },
      { type: 'MANIFEST', state: session.manifestState, available: representedState(session.manifestState) },
      { type: 'TRANSFER', state: session.transferState, available: representedState(session.transferState) }
    ]
  });

  const getLineage = (session) => {
    const manifestAvailable = representedState(session.manifestState);
    const transferAvailable = representedState(session.transferState);
    return [
      { label: 'Observation session', state: 'represented', detail: session.sessionId },
      { label: 'Acquisition metrics', state: representedState(session.evidenceState) ? 'represented' : 'missing', detail: `${session.lightCompleted} completed light frames` },
      { label: 'Scientific assets', state: 'partial', detail: 'paths and binary inventory not exposed in this catalog' },
      { label: 'Manifest', state: manifestAvailable ? 'represented' : 'missing', detail: session.manifestState },
      { label: 'Transfer', state: transferAvailable ? 'represented' : 'missing', detail: session.transferState },
      { label: 'Processing', state: 'missing', detail: 'not represented' },
      { label: 'Publication', state: 'missing', detail: 'not represented' }
    ];
  };

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

  // Separate bounded evidence reader; never normalize workflows as sessions.
  // No cache/fallback: each refresh reads the current published collection.
  const getPublicWorkflowCollection = async ({signal} = {}) => {
    const contract = window.DSGBkl049WorkflowContract;
    if (!contract || !workflowSource || new URL(workflowSource).origin !== location.origin) {
      throw new Error('WORKFLOW_UNAVAILABLE');
    }
    const controller = new AbortController();
    const abort = () => controller.abort();
    signal?.addEventListener('abort', abort, {once: true});
    if (signal?.aborted) abort();
    const timer = setTimeout(abort, 10000);
    let reader;
    try {
      const response = await fetch(workflowSource, {signal: controller.signal, cache: 'no-store',
        redirect: 'error', credentials: 'omit', mode: 'same-origin'});
      if (!response.ok || response.url !== workflowSource || !response.body) throw new Error('WORKFLOW_UNAVAILABLE');
      reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8', {fatal: true});
      let bytes = 0, text = '';
      while (true) {
        const chunk = await reader.read();
        if (chunk.done) break;
        bytes += chunk.value.byteLength;
        if (bytes > contract.MAX_BYTES) throw new Error('WORKFLOW_UNAVAILABLE');
        text += decoder.decode(chunk.value, {stream: true});
      }
      text += decoder.decode();
      if (controller.signal.aborted) throw new Error('WORKFLOW_UNAVAILABLE');
      return contract.parseCollection(text);
    } catch {
      throw new Error('WORKFLOW_UNAVAILABLE');
    } finally {
      clearTimeout(timer);
      signal?.removeEventListener('abort', abort);
      if (reader) { await reader.cancel().catch(() => {}); reader.releaseLock(); }
    }
  };

  const getPhotoUploadContext = async source => {
    const url=new URL(source,location.href);if(url.origin!==location.origin)throw new Error('PHOTO_CATALOG_ORIGIN');
    const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),15000);let reader;
    try{
      const response=await fetch(url.href,{cache:'no-store',redirect:'error',credentials:'omit',signal:controller.signal});
      if(!response.ok || response.url!==url.href || !response.body)throw new Error('PHOTO_CATALOG_UNAVAILABLE');
      reader=response.body.getReader();const chunks=[];let length=0;
      while(true){const item=await reader.read();if(item.done)break;length+=item.value.length;if(length>16*1024*1024)throw new Error('PHOTO_CATALOG_LIMIT');chunks.push(item.value);}
      const bytes=new Uint8Array(length);let offset=0;for(const chunk of chunks){bytes.set(chunk,offset);offset+=chunk.length;}
      const catalog=JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(bytes));
      if(catalog.schemaVersion!=='1.5' || catalog.catalogStatus!=='VERSIONED_ANALYTICS_PROJECTION' || !Array.isArray(catalog.sessions))throw new Error('PHOTO_CATALOG_PROFILE');
      const digest=await crypto.subtle.digest('SHA-256',bytes);
      return {catalogSha256:[...new Uint8Array(digest)].map(x=>x.toString(16).padStart(2,'0')).join(''),sessions:catalog.sessions};
    }finally{clearTimeout(timer);if(reader){await reader.cancel().catch(()=>{});reader.releaseLock();}}
  };

  const getSessionPhotoCollection = async () => {
    const config = await window.DSGPhotoApi.config();
    const url = config.serviceUrl + '/v1/gallery';
    const controller = new AbortController(), timer = setTimeout(() => controller.abort(), 10000);
    let reader;
    try {
      const response = await fetch(url, {signal:controller.signal,cache:'no-store',redirect:'error',credentials:'omit'});
      if(!response.ok || response.url!==url || !response.body) throw new Error('PHOTO_GALLERY_UNAVAILABLE');
      reader=response.body.getReader();const decoder=new TextDecoder('utf-8',{fatal:true});let raw='',bytes=0;
      while(true){const item=await reader.read();if(item.done)break;bytes+=item.value.byteLength;if(bytes>2*1024*1024)throw new Error('PHOTO_GALLERY_LIMIT');raw+=decoder.decode(item.value,{stream:true});}
      raw+=decoder.decode();const collection=JSON.parse(raw);
      const closed=(value,keys)=>value && typeof value==='object' && !Array.isArray(value) && Object.keys(value).sort().join('|')===keys.sort().join('|');
      const text=(value,max)=>typeof value==='string' && value.trim() && value.length<=max;
      if(!closed(collection,['schemaVersion','kind','authority','actionAuthority','records']) || collection.schemaVersion!=='1.0' || collection.kind!=='DSG_SESSION_PHOTO_COLLECTION_V1' || collection.authority!=='projection' || collection.actionAuthority!=='NONE' || !Array.isArray(collection.records) || collection.records.length>64)throw new Error('PHOTO_GALLERY_PROFILE');
      const versions=new Set();
      for(const record of collection.records){
        if(!closed(record,['schemaVersion','kind','imageId','imageVersionId','workflowId','title','target','sessionIds','processingDate','previewUrl','captureCompleteness','executionEvidence','associationEvidence','steps','omittedStepCount','validUntil']) || record.schemaVersion!=='1.0' || record.kind!=='DSG_SESSION_PHOTO_V1' || !/^IMG-[a-f0-9]{32}$/.test(record.imageId) || !/^VER-[a-f0-9]{32}$/.test(record.imageVersionId) || record.workflowId!=='WF-'+record.imageVersionId.slice(4) || versions.has(record.imageVersionId) || !text(record.title,160) || !text(record.target,160) || !/^\d{4}-\d{2}-\d{2}$/.test(record.processingDate) || record.validUntil!==null || record.executionEvidence!=='NOT_ESTABLISHED' || record.associationEvidence!=='OWNER_DECLARED' || !['PARTIAL','UNAVAILABLE'].includes(record.captureCompleteness) || !Array.isArray(record.sessionIds) || record.sessionIds.length<1 || record.sessionIds.length>32 || new Set(record.sessionIds).size!==record.sessionIds.length || !record.sessionIds.every(id=>text(id,160)) || !Array.isArray(record.steps) || record.steps.length>512 || !Number.isInteger(record.omittedStepCount) || record.omittedStepCount<0)throw new Error('PHOTO_RECORD_INVALID');
        const preview=new URL(record.previewUrl);if(preview.origin!==config.serviceUrl || !/^\/v1\/previews\/[a-f0-9]{64}$/.test(preview.pathname) || preview.search || preview.hash || preview.username || preview.password || !preview.pathname.split('/').pop().startsWith(record.imageVersionId.slice(4)))throw new Error('PHOTO_PREVIEW_INVALID');
        versions.add(record.imageVersionId);let previous=0;
        for(const step of record.steps){
          if(!closed(step,['sourceOrdinal','processId','evidenceClass','parameters','omittedParameterCount']) || !Number.isInteger(step.sourceOrdinal) || step.sourceOrdinal<=previous || !/^[A-Za-z_][A-Za-z0-9_]{0,127}$/.test(step.processId) || step.evidenceClass!=='DECLARED' || !Number.isInteger(step.omittedParameterCount) || step.omittedParameterCount<0 || !Array.isArray(step.parameters) || step.parameters.length>128)throw new Error('PHOTO_STEP_INVALID');
          previous=step.sourceOrdinal;const names=new Set();for(const parameter of step.parameters){if(!closed(parameter,['name','lexicalJson']) || !/^[A-Za-z_][A-Za-z0-9_]{0,127}$/.test(parameter.name) || names.has(parameter.name) || !text(parameter.lexicalJson,4096))throw new Error('PHOTO_PARAMETER_INVALID');names.add(parameter.name);}
        }
        if((record.steps.length>0)!==(record.captureCompleteness==='PARTIAL'))throw new Error('PHOTO_COMPLETENESS_INVALID');
      }
      return collection;
    } finally {clearTimeout(timer);if(reader){await reader.cancel().catch(()=>{});reader.releaseLock();}}
  };

  window.DSGScientificDataEngine = Object.freeze({
    version: VERSION,
    getPublicWorkflowCollection,
    getSessionPhotoCollection,
    getPhotoUploadContext,
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
