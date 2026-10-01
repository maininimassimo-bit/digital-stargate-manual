/* Read-only gallery workflow panel; only the Scientific Data Engine fetches. */
(() => {
  'use strict';
  const base = new URL('../', document.currentScript.src);
  let enginePromise;
  const ensureEngine = () => {
    if (window.DSGScientificDataEngine?.getPublicWorkflowCollection) return Promise.resolve();
    if (!enginePromise) enginePromise = new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = new URL('javascripts/scientific-data-engine.js', base).href;
      script.onload = () => window.DSGScientificDataEngine?.getPublicWorkflowCollection ? resolve() : reject();
      script.onerror = reject;
      document.head.append(script);
    }).catch(() => { enginePromise = null; throw new Error('WORKFLOW_UNAVAILABLE'); });
    return enginePromise;
  };
  const element = (tag, text, parent) => {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = text;
    parent?.append(node);
    return node;
  };
  const labels = {
    PARTIAL_HISTORY: 'La storia disponibile è parziale.',
    EXECUTION_NOT_OBSERVED: 'L’esecuzione dei processi non è stata osservata direttamente.',
    UPSTREAM_RELATIONS_UNRESOLVED: 'Collegamenti intermedi, input e maschere non sono tutti risolti.',
    PROCESS_VERSIONS_UNAVAILABLE: 'Le versioni storiche dei processi non sono disponibili.',
    PUBLIC_FIELDS_OMITTED: 'Sono mostrati soltanto i campi approvati per la pubblicazione.'
  };
  const initialize = () => {
    const host = document.querySelector('[data-bkl049-workflows]');
    if (!host) return;
    const body = host.querySelector('[data-workflow-body]'), status = host.querySelector('[data-workflow-status]');
    const refresh = host.querySelector('[data-workflow-refresh]');
    let alive = true, controller, expiry, sequence = 0;
    const unavailable = () => {
      body.replaceChildren();
      status.textContent = 'Workflow non disponibile. Nessun collegamento viene dedotto dal nome dell’immagine.';
    };
    const render = collection => {
      const query = new URL(location.href).searchParams;
      const keys = ['image', 'version', 'workflow'];
      const selected = keys.some(key => query.has(key));
      let records = collection.records;
      if (selected) {
        if (!keys.every(key => query.getAll(key).length === 1)) throw new Error('WORKFLOW_UNAVAILABLE');
        const match = window.DSGBkl049WorkflowContract.resolve(collection, ...keys.map(key => query.get(key)));
        if (!match) throw new Error('WORKFLOW_UNAVAILABLE');
        records = [match];
      }
      if (!records.length) { unavailable(); return; }
      status.textContent = 'Workflow dichiarati, con lacune esplicite. Ordine esportato; non è una cronologia osservata.';
      for (const record of records) {
        const article = element('article', undefined, body);
        article.className = 'dsg-workflow-card';
        element('h3', `Immagine ${record.imageId} · versione ${record.imageVersionId}`, article);
        const url = new URL('scientific-image-gallery/', base);
        url.searchParams.set('image', record.imageId); url.searchParams.set('version', record.imageVersionId);
        url.searchParams.set('workflow', record.workflowId);
        const link = element('a', `Collegamento esatto al workflow ${record.workflowId}`, article);
        link.href = url.href;
        element('p', record.captureCompleteness === 'PARTIAL' ? 'Workflow parziale · DECLARED / PARTIAL' : 'Passaggi non disponibili · UNAVAILABLE', article);
        const gaps = element('ul', undefined, article);
        record.gaps.forEach(gap => element('li', labels[gap], gaps));
        element('p', `Passaggi non mostrati: ${record.omittedStepCount}.`, article);
        const details = element('details', undefined, article);
        element('summary', 'Mostra i passaggi disponibili', details);
        for (const step of record.steps) {
          element('h4', `${step.sourceOrdinal}. ${step.processId} · DECLARED`, details);
          element('p', `Parametri non mostrati: ${step.omittedParameterCount}.`, details);
          for (const parameter of step.parameters) {
            element('strong', parameter.name, details);
            element('pre', parameter.lexicalJson, details);
          }
        }
        const method = element('a', 'Come leggere queste evidenze', article);
        method.href = new URL(record.methodCitation, base).href;
      }
      expiry = setTimeout(unavailable, Math.max(0, Date.parse(collection.validUntil) - Date.now()));
    };
    const load = async () => {
      const request = ++sequence;
      controller?.abort(); clearTimeout(expiry);
      controller = new AbortController();
      unavailable(); status.textContent = 'Verifica dei workflow disponibili…';
      refresh.disabled = true;
      try {
        await ensureEngine();
        if (!alive || request !== sequence) return;
        const collection = await window.DSGScientificDataEngine.getPublicWorkflowCollection({signal: controller.signal});
        if (!alive || request !== sequence || !host.isConnected) return;
        render(collection);
      } catch { if (alive && request === sequence) unavailable(); }
      finally { if (alive && request === sequence) refresh.disabled = false; }
    };
    const visibility = () => { if (!document.hidden) load(); };
    refresh.addEventListener('click', load);
    document.addEventListener('visibilitychange', visibility);
    window.addEventListener('popstate', load);
    load();
    return () => {
      alive = false; ++sequence; controller?.abort(); clearTimeout(expiry);
      refresh.removeEventListener('click', load); document.removeEventListener('visibilitychange', visibility);
      window.removeEventListener('popstate', load); body.replaceChildren();
    };
  };
  if (window.DSG?.components) window.DSG.components.register({name: 'bkl049-gallery-workflows', order: 90, initialize});
  else {
    let cleanup;
    const remount = () => { cleanup?.(); cleanup = initialize(); };
    if (window.document$?.subscribe) window.document$.subscribe(remount);
    else if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', remount, {once: true});
    else remount();
  }
})();
