/* Owner-approved isolated P6 OAT. Production service and worker are never addressed. */
(() => {
  'use strict';
  const ORIGIN = 'https://dsg-piai-p6-oat-cfjug35c6q-ew.a.run.app';
  const CLIENT = '183451329061-8iedbjrn60u6iau42u1tlsonn6bi6hjd.apps.googleusercontent.com';
  function initialize() {
    const root = document.querySelector('[data-piai-p6-check]');
    if (!root || root.dataset.initialized) return;
    root.dataset.initialized = 'true';
    const q = name => root.querySelector(`[data-p6-${name}]`);
    let credential = null, busy = false, probe = null, recovery = null;
    const opaque = () => Array.from(crypto.getRandomValues(new Uint8Array(16)), x => x.toString(16).padStart(2, '0')).join('');
    const request = () => ({schemaVersion:'1.0',requestId:opaque(),inputRef:opaque(),recipe:'LRGB_LINEAR_PREP_V1',aiMode:'SESSION_ASSISTED'});
    async function call(path, value, auth = true) {
      const controller = new AbortController(), timer = setTimeout(() => controller.abort(), 30000);
      try {
        const headers = auth ? {Authorization:`Bearer ${credential}`} : {};
        if (value !== undefined) headers['Content-Type'] = 'application/json';
        const response = await fetch(ORIGIN + path, {method:value === undefined?'GET':'POST',headers,
          body:value === undefined?undefined:JSON.stringify(value),credentials:'omit',redirect:'error',cache:'no-store',signal:controller.signal});
        if (!response.ok) throw new Error('REQUEST_DENIED');
        return await response.json();
      } finally {clearTimeout(timer);}
    }
    function require(value) {if (!value) throw new Error('EVIDENCE_MISMATCH');}
    async function run(action) {
      if (busy) return;
      busy = true;
      for (const name of ['connect','probe','prepare','status']) q(name).disabled = true;
      try {await action();}
      catch {q('message').textContent = 'Verifica non completata. Conserva la pagina: ripeti la stessa operazione, senza nuove identità.';}
      finally {
        busy = false; q('connect').disabled = Boolean(credential);
        q('probe').disabled = !credential; q('prepare').disabled = !credential;
        q('status').disabled = !credential || !recovery;
      }
    }
    const show = value => {q('result').textContent = JSON.stringify(value,null,2);};
    q('connect').addEventListener('click', () => run(async () => {
      const health = await call('/health',undefined,false);
      require(health.protocol === 'DSG_PIAI_QUEUE_V1' && health.aiMode === 'SESSION_ASSISTED' && health.providerRequests === 0);
      if (!window.google?.accounts?.id) await new Promise((resolve,reject) => {
        const script = document.createElement('script');script.src = 'https://accounts.google.com/gsi/client';
        script.onload = resolve;script.onerror = reject;document.head.append(script);
      });
      google.accounts.id.initialize({client_id:CLIENT,callback:response => {
        credential = response.credential; q('probe').disabled = false;q('prepare').disabled = false;
        q('connect').disabled = true;q('message').textContent = 'Accesso Google ricevuto: puoi verificare l’autorizzazione Owner sul solo servizio di prova.';
      }});
      q('signin').replaceChildren();google.accounts.id.renderButton(q('signin'),{theme:'outline',size:'large'});
      q('message').textContent = 'Accedi con Google per il collaudo isolato.';
    }));
    q('probe').addEventListener('click', () => run(async () => {
      probe ||= request();
      const created = await Promise.all([call('/v1/jobs',probe),call('/v1/jobs',probe)]);
      require(created.every(x => x.jobId === `PIAI_${probe.requestId}` && !('leaseToken' in x)));
      const cancelled = await Promise.all(created.map(x => call(`/v1/jobs/${x.jobId}/cancel`,{})));
      require(cancelled.every(x => x.state === 'CANCELLED' && !('leaseToken' in x)));
      const status = await call(`/v1/jobs/${created[0].jobId}`);
      require(status.job.state === 'CANCELLED' && status.publication === 'NONE' && !('leaseToken' in status.job));
      show({kind:'DSG_PIAI_P6_ISOLATED_OWNER_CONCURRENCY_V1',jobId:created[0].jobId,concurrentClientCreates:2,
        concurrentClientCancels:2,idempotency:'PASS_SAME_JOB',state:'CANCELLED',publication:'NONE',serverInterleavedCasAttested:false});
      q('message').textContent = 'Richieste concorrenti verificate; un solo job di prova, annullato. Nessuna elaborazione avviata.';
    }));
    q('prepare').addEventListener('click', () => run(async () => {
      recovery ||= [request(),request()];
      const jobs = [];
      for (const value of recovery) {
        const job = await call('/v1/jobs',value);
        require(job.jobId === `PIAI_${value.requestId}` && !('leaseToken' in job));jobs.push({jobId:job.jobId,inputRef:value.inputRef,state:job.state});
      }
      show({kind:'DSG_PIAI_P6_ISOLATED_RECOVERY_REQUESTS_V1',jobs,publication:'NONE'});
      q('message').textContent = 'Due job nel solo ambiente di prova. Comunica questi identificativi all’assistente; PixInsight non è stato avviato.';
    }));
    q('status').addEventListener('click', () => run(async () => {
      const statuses = await Promise.all(recovery.map(x => call(`/v1/jobs/PIAI_${x.requestId}`)));
      require(statuses.every(x => x.publication === 'NONE' && !('leaseToken' in x.job) && !x.job.report?.leaseToken));
      show({kind:'DSG_PIAI_P6_ISOLATED_RECOVERY_STATUS_V1',jobs:statuses.map(x => ({jobId:x.job.jobId,state:x.job.state,connection:x.connection})),publication:'NONE'});
      q('message').textContent = 'Stati letti dal servizio di prova; nessuna modifica alle prenotazioni.';
    }));
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded',initialize);else initialize();
  if (typeof document$ !== 'undefined') document$.subscribe(initialize);
})();
