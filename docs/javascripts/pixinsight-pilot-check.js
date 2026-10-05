/* P4 Owner OAT only. No image, worker credential, native launch or publication. */
(() => {
  'use strict';
  const CLIENT = '183451329061-8iedbjrn60u6iau42u1tlsonn6bi6hjd.apps.googleusercontent.com';
  const APPROVED_ORIGIN_SHA256 = 'ef4ebd64f0a2cd2e50b7c08781416ac5dbd47722b570135332d56084106ef7d3';
  function initialize() {
    const root = document.querySelector('[data-piai-check]');
    if (!root || root.dataset.initialized) return;
    root.dataset.initialized = 'true';
    const q = name => root.querySelector(`[data-piai-${name}]`);
    let origin = null, credential = null, request = null, busy = false;
    const message = value => { q('message').textContent = value; };
    const opaque = () => Array.from(crypto.getRandomValues(new Uint8Array(16)), x => x.toString(16).padStart(2, '0')).join('');
    async function call(path, value, authenticated = true) {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), 30000);
      try {
        const headers = authenticated ? {Authorization: `Bearer ${credential}`} : {};
        if (value !== undefined) headers['Content-Type'] = 'application/json';
        const response = await fetch(origin + path, {method: value === undefined ? 'GET' : 'POST', headers,
          body: value === undefined ? undefined : JSON.stringify(value), cache: 'no-store', credentials: 'omit', redirect: 'error', signal: controller.signal});
        if (!response.ok) throw new Error('REQUEST_DENIED');
        return await response.json();
      } finally { clearTimeout(timer); }
    }
    async function run(action) {
      if (busy) return;
      busy = true; q('connect').disabled = true; q('probe').disabled = true;
      try { await action(); }
      catch { message('Verifica non completata. Conserva questa pagina e ripeti la stessa operazione.'); }
      finally { busy = false; q('connect').disabled = Boolean(credential); q('probe').disabled = !credential; }
    }
    q('connect').addEventListener('click', () => run(async () => {
      const url = new URL(q('origin').value.trim());
      if (url.protocol !== 'https:' || !/^[a-z0-9-]+(?:\.[a-z0-9-]+)?\.run\.app$/.test(url.hostname) ||
          url.port || url.username || url.password || url.search || url.hash || url.pathname !== '/') throw new Error('ORIGIN');
      if (origin && request && origin !== url.origin) throw new Error('ORIGIN_LOCKED');
      const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(url.origin));
      const hash = Array.from(new Uint8Array(digest), x => x.toString(16).padStart(2, '0')).join('');
      if (hash !== APPROVED_ORIGIN_SHA256) throw new Error('UNAPPROVED_ORIGIN');
      origin = url.origin;
      const health = await call('/health', undefined, false);
      if (health.protocol !== 'DSG_PIAI_QUEUE_V1' || health.aiMode !== 'SESSION_ASSISTED' || health.providerRequests !== 0) throw new Error('HEALTH');
      if (!window.google?.accounts?.id) await new Promise((resolve, reject) => {
        const script = document.createElement('script'); script.src = 'https://accounts.google.com/gsi/client';
        script.onload = resolve; script.onerror = reject; document.head.append(script);
      });
      google.accounts.id.initialize({client_id: CLIENT, callback: response => {
        credential = response.credential; q('origin').disabled = true; q('connect').disabled = true;
        q('probe').disabled = false; message('Accesso Google ricevuto. Verifica ora l’autorizzazione del proprietario sul servizio.');
      }});
      q('signin').replaceChildren();
      google.accounts.id.renderButton(q('signin'), {theme: 'outline', size: 'large'});
      message('Accedi con l’account del proprietario.');
    }));
    q('probe').addEventListener('click', () => run(async () => {
      request ||= {schemaVersion: '1.0', requestId: opaque(), inputRef: opaque(), recipe: 'LRGB_LINEAR_PREP_V1', aiMode: 'SESSION_ASSISTED'};
      const created = await call('/v1/jobs', request);
      if (created.jobId !== `PIAI_${request.requestId}` || 'leaseToken' in created) throw new Error('CREATE');
      const duplicate = await call('/v1/jobs', request);
      if (duplicate.jobId !== created.jobId) throw new Error('IDEMPOTENCY');
      const cancelled = await call(`/v1/jobs/${created.jobId}/cancel`, {});
      const status = await call(`/v1/jobs/${created.jobId}`);
      if (cancelled.state !== 'CANCELLED' || status.job.state !== 'CANCELLED' || status.publication !== 'NONE' ||
          'leaseToken' in status.job || status.job.report?.leaseToken) throw new Error('STATUS');
      q('result').textContent = JSON.stringify({kind: 'DSG_PIAI_OWNER_OAT_V1', jobId: created.jobId,
        ownerAuthentication: 'PASS', idempotentCreate: 'PASS', cancelBeforeNative: 'PASS', state: status.job.state,
        publication: status.publication, executionEvidence: status.executionEvidence}, null, 2);
      message('Accesso del proprietario verificato. Richiesta di prova annullata; nessuna elaborazione avviata.');
    }));
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialize); else initialize();
  if (typeof document$ !== 'undefined') document$.subscribe(initialize);
})();
