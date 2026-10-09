// Token stays in the calling browser's memory. No storage, console or token export.
export function validateDescriptor(value, now = Date.now() / 1000) {
  if (!value || Object.keys(value).sort().join() !==
      ['baseUrl', 'deadline', 'jobs', 'sessionRef', 'sourceRevision'].sort().join()) throw Error('Descrittore incompleto');
  const url = new URL(value.baseUrl);
  if (url.protocol !== 'https:' || !/^dsg-s4-lab-[a-f0-9]{12}-183451329061\.europe-west1\.run\.app$/.test(url.hostname)
      || url.port || url.pathname !== '/' || url.search || url.hash || url.username || url.password) throw Error('Servizio isolato richiesto');
  if (!/^[a-f0-9]{32}$/.test(value.sessionRef) || !url.hostname.startsWith('dsg-s4-lab-' + value.sessionRef.slice(0, 12) + '-')
      || !/^[a-f0-9]{40}$/.test(value.sourceRevision) || !Number.isFinite(value.deadline)
      || !(now < value.deadline && value.deadline <= now + 1800)) throw Error('Sessione o revisione non valida');
  if (!Array.isArray(value.jobs) || value.jobs.length !== 2 || value.jobs.some(job =>
      !job || Object.keys(job).sort().join() !== 'bindingRef,requestId' ||
      !/^[a-f0-9]{32}$/.test(job.bindingRef) || !/^[a-f0-9]{32}$/.test(job.requestId))
      || value.jobs[0].requestId === value.jobs[1].requestId || value.jobs[0].bindingRef === value.jobs[1].bindingRef) throw Error('Coppia sintetica richiesta');
  return structuredClone(value);
}

export class OwnerSession {
  constructor(descriptor, token, transport = (input, options) => globalThis.fetch(input, options), clock = () => Date.now() / 1000) {
    this.descriptor = validateDescriptor(descriptor, clock());
    if (typeof token !== 'string' || !token || token.length > 8192) throw Error('Accesso Owner richiesto');
    this.token = token; this.transport = transport; this.clock = clock; this.used = false; this.uncertain = false;
  }
  forget() { this.token = ''; }
  async request(path, body, authenticated = true) {
    if (this.clock() >= this.descriptor.deadline) throw Error('Sessione scaduta');
    const headers = {};
    if (authenticated) headers.Authorization = 'Bearer ' + this.token;
    if (body !== undefined) headers['Content-Type'] = 'application/json';
    const response = await this.transport(new URL(path, this.descriptor.baseUrl), {
      method: body === undefined ? 'GET' : 'POST', headers,
      body: body === undefined ? undefined : JSON.stringify(body),
      cache: 'no-store', credentials: 'omit', redirect: 'error', signal: AbortSignal.timeout(30000)
    });
    if (response.status !== 200) throw Error('Risposta non confermata: interrompere senza ripetere');
    return response.json();
  }
  async createPair() {
    if (this.used) throw Error('Sessione già utilizzata; nessuna ripetizione automatica');
    this.used = true;
    const d = this.descriptor;
    try {
      const health = await this.request('/health', undefined, false);
      if (health.protocol !== 'DSG_S4_LAB_V1' || health.sessionRef !== d.sessionRef
          || health.sourceRevision !== d.sourceRevision || health.storageMode !== 'GCS_ADC') throw Error('Servizio o sorgenti non corrispondenti');
      const before = await this.request('/lab/audit');
      if (before.sessionRef !== d.sessionRef || before.sourceRevision !== d.sourceRevision
          || before.phase !== 'CREATE' || before.finishedPhases.join() !== 'REGISTER'
          || before.bindings.length !== 2 || before.jobs.length !== 0
          || d.jobs.some(job => !before.bindings.some(binding => binding.bindingRef === job.bindingRef))) throw Error('Registrazione della coppia non confermata');
      const paths = ['A', 'B'].map(name => '/e/' + name + '/v1/transient-analysis/jobs');
      const replies = await Promise.allSettled(paths.map((path, i) => this.request(path, d.jobs[i])));
      if (replies.some(row => row.status !== 'fulfilled')) throw Error('Coppia incerta: fermarsi e riconciliare in lettura');
      await this.request('/lab/finish', {sessionRef: d.sessionRef});
      const committed = await this.request('/lab/audit');
      // Repeat only after BOTH success receipts and successful phase confirmation.
      for (let i = 0; i < 2; i++) {
        const repeated = await this.request(paths[i], d.jobs[i]);
        if (JSON.stringify(repeated) !== JSON.stringify(replies[i].value)) throw Error('Ricevuta ripetuta diversa');
      }
      const audit = await this.request('/lab/audit');
      if (audit.sessionRef !== d.sessionRef || audit.sourceRevision !== d.sourceRevision
          || audit.storageMode !== 'GCS_ADC' || audit.finishedPhases.join() !== 'REGISTER,CREATE'
          || audit.jobs.length !== 2 || audit.jobs.some(job => job.state !== 'QUEUED')
          || d.jobs.some(request => !audit.jobs.some(job => job.request.requestId === request.requestId
            && job.request.bindingRef === request.bindingRef))
          || audit.generation !== committed.generation || audit.sha256 !== committed.sha256
          || audit.attempts.length !== 6 || audit.attempts.filter(row => row.committed === true).length !== 4
          || ['REGISTER', 'CREATE'].some(phase => {
            const reads = audit.reads.filter(row => row.phase === phase);
            return reads.length !== 2 || new Set(reads.map(row => row.executor)).size !== 2
              || reads[0].generation !== reads[1].generation;
          })
          || audit.observedUpload412 !== 2 || audit.copies.length !== 6
          || audit.copies.some(copy => copy.verified !== true)) throw Error('Evidenza incompleta: non accettare S4');
      return {protocol: 'DSG_S4_OWNER_BROWSER_RECEIPT_V1', sessionRef: d.sessionRef,
        sourceRevision: d.sourceRevision, authentication: 'BROWSER_REPORTED_GOOGLE_OWNER',
        receipts: replies.map(row => row.value), audit, milestoneClosed: false};
    } catch (error) { this.uncertain = true; throw error; }
    finally { this.forget(); }
  }
}
