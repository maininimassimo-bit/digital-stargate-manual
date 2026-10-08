/* Dedicated Owner view and explicit queue intents. No worker claim or scientific classification. */
(() => {
  'use strict';
  const ORIGIN = 'https://dsg-pixinsight-pilot-183451329061.europe-west1.run.app';
  const CLIENT = '183451329061-8iedbjrn60u6iau42u1tlsonn6bi6hjd.apps.googleusercontent.com';
  const labels = {QUEUED:'In coda', RESERVED:'Prenotato dal PC', RUNNING:'Operazione in corso',
    COMPLETED:'Completamento tecnico comunicato dal PC', FAILED:'Tentativo non riuscito',
    CANCELLED:'Annullamento confermato', RECOVERY_REQUIRED:'Recupero supervisionato necessario'};
  const decisions = {KEEP_FOR_REVIEW:'Conservare per verifica', REJECT_CANDIDATE:'Scartare il candidato', FOLLOW_UP:'Approfondire'};
  const object = value => value !== null && typeof value === 'object' && !Array.isArray(value);
  const fields = (value, required, optional=[]) => object(value) && required.every(key=>Object.hasOwn(value,key))
    && Object.keys(value).every(key=>required.includes(key)||optional.includes(key));
  const opaque = value => typeof value === 'string' && /^[a-f0-9]{32}$/.test(value);
  const hash = value => typeof value === 'string' && /^[a-f0-9]{64}$/.test(value);
  const instant = value => typeof value === 'string'
    && /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|\+00:00)$/.test(value)
    && Number.isFinite(Date.parse(value)) && new Date(value).toISOString().slice(0,19)===value.slice(0,19);
  const require = value => {if(!value)throw new Error('Ricevuta non valida: nessun risultato mostrato.');};
  const bindingKeys=['bindingRef','inputRef','referenceRef','algorithmRef','contractRef'];
  const canonical=value=>object(value)?Object.fromEntries(Object.keys(value).sort().map(key=>[key,canonical(value[key])])):
    Array.isArray(value)?value.map(canonical):value;
  const same=(a,b)=>JSON.stringify(canonical(a))===JSON.stringify(canonical(b));
  function inspectBinding(value) {
    require(fields(value,bindingKeys)&&Object.values(value).every(opaque));
    return Object.fromEntries(bindingKeys.map(key=>[key,value[key]]));
  }
  function inspectOptions(value) {
    require(fields(value,['bindings'])&&Array.isArray(value.bindings)&&value.bindings.length<=32);
    const bindings=value.bindings.map(inspectBinding);
    require(new Set(bindings.map(b=>b.bindingRef)).size===bindings.length);return bindings;
  }
  const pendingKey='dsg-bkl051-owner-pending-v1';
  function inspectPending(value) {
    require(fields(value,['kind','action','jobId','binding','body'])&&value.kind==='BKL051_OWNER_PENDING_ACTION_V1'
      && typeof value.jobId==='string'&&/^TRN_[a-f0-9]{32}$/.test(value.jobId));
    const binding=inspectBinding(value.binding),body=value.body;
    if(value.action==='CREATE')require(fields(body,['requestId','bindingRef'])&&opaque(body.requestId)
      &&value.jobId==='TRN_'+body.requestId&&body.bindingRef===binding.bindingRef);
    else if(value.action==='CANCEL')require(fields(body,[]));
    else if(value.action==='REVIEW')require(fields(body,['decisionId','reportSha256','decision'])&&opaque(body.decisionId)
      &&hash(body.reportSha256)&&Object.hasOwn(decisions,body.decision));
    else require(false);
    return {...value,binding,body:JSON.parse(JSON.stringify(body))};
  }
  function inspectJobs(value) {
    require(fields(value,['jobs']) && Array.isArray(value.jobs) && value.jobs.length<=32);
    const ids=new Set();
    for(const job of value.jobs) {
      require(fields(job,['jobId','request','binding','state','cancelRequested','sequence','result','reviews',
        'createdAt','updatedAt','executionEvidence','scientificValidation','detailsLocation','publication'],
        ['rootId','attemptId','leaseIssuedAt','leaseExpiresAt']));
      require(fields(job.request,['requestId','bindingRef']) && opaque(job.request.requestId) && opaque(job.request.bindingRef)
        && job.jobId==='TRN_'+job.request.requestId && !ids.has(job.jobId)); ids.add(job.jobId);
      require(fields(job.binding,['bindingRef','inputRef','referenceRef','algorithmRef','contractRef'])
        && Object.values(job.binding).every(opaque) && job.binding.bindingRef===job.request.bindingRef);
      require(Object.hasOwn(labels,job.state) && typeof job.cancelRequested==='boolean'
        && Number.isInteger(job.sequence) && job.sequence>=0 && job.sequence<=128
        && instant(job.createdAt) && instant(job.updatedAt) && Date.parse(job.updatedAt)>=Date.parse(job.createdAt));
      require(job.executionEvidence==='WORKER_REPORTED_NOT_ATTESTED' && job.scientificValidation==='NOT_VALIDATED'
        && job.detailsLocation==='OWNER_PC' && job.publication==='NONE');
      const attempted=Object.hasOwn(job,'attemptId');
      require(attempted ? opaque(job.attemptId) && opaque(job.rootId) && instant(job.leaseIssuedAt)
        && instant(job.leaseExpiresAt) && Date.parse(job.leaseExpiresAt)>=Date.parse(job.leaseIssuedAt)
        : !['rootId','leaseIssuedAt','leaseExpiresAt'].some(key=>Object.hasOwn(job,key)));
      require(!['RESERVED','RUNNING','COMPLETED','FAILED','RECOVERY_REQUIRED'].includes(job.state)||attempted);
      require(job.sequence===0||attempted);
      require(job.state!=='RESERVED'||job.sequence===0);
      require(!['RUNNING','FAILED'].includes(job.state)||job.sequence>=1);
      require(job.state!=='QUEUED'||(!attempted&&job.sequence===0&&!job.cancelRequested));
      require(job.state!=='COMPLETED'||(!job.cancelRequested&&job.sequence>=2));
      if(job.state==='COMPLETED') {
        require(fields(job.result,['reportSha256','bindingRef','qualityCounts']) && hash(job.result.reportSha256)
          && job.result.bindingRef===job.binding.bindingRef
          && fields(job.result.qualityCounts,['measured','excluded','incomplete'])
          && Object.values(job.result.qualityCounts).every(v=>Number.isInteger(v)&&v>=0&&v<=10000000));
      } else require(job.result===null);
      require(Array.isArray(job.reviews)&&job.reviews.length<=32&&(job.state==='COMPLETED'||job.reviews.length===0));
      const reviews=new Set();
      for(const review of job.reviews) {
        require(fields(review,['request','recordedAt','authority']) && fields(review.request,['decisionId','reportSha256','decision'])
          && opaque(review.request.decisionId) && !reviews.has(review.request.decisionId)
          && review.request.reportSha256===job.result.reportSha256 && Object.hasOwn(decisions,review.request.decision)
          && instant(review.recordedAt) && review.authority==='OWNER_DECLARED'); reviews.add(review.request.decisionId);
      }
    }
    // The boundary validates only received structure/correlation, not bytes on the PC or science.
    return JSON.parse(JSON.stringify(value.jobs));
  }
  async function readResponse(response) {
    const length=response.headers.get('Content-Length');
    require(length===null||(/^\d{1,7}$/.test(length)&&Number(length)<=1048576));
    require(response.body&&typeof response.body.getReader==='function');
    const reader=response.body.getReader(),decoder=new TextDecoder('utf-8',{fatal:true});
    let text='',bytes=0;
    try {
      while(true){const part=await reader.read();if(part.done)break;bytes+=part.value.byteLength;
        require(bytes<=1048576);text+=decoder.decode(part.value,{stream:true});}
      return text+decoder.decode();
    } catch(error){try{await reader.cancel();}catch{}throw error;}
    finally {reader.releaseLock();}
  }
  let active;
  function initialize() {
    const root=document.querySelector('[data-dsg-transients]');
    if(active?.root===root)return;
    active?.dispose(); active=null;
    if(!root)return;
    const q=name=>root.querySelector(`[data-dsg-transients-${name}]`);
    let token='', busy=false, controller, disposed=false, epoch=0, url;
    let bindings=[],jobs=[],ready=false,pending=null,storageBlocked=false,retryAllowed=false;
    try {const stored=sessionStorage.getItem(pendingKey);if(stored!==null){require(stored.length<=2048);pending=inspectPending(JSON.parse(stored));}}
    catch {storageBlocked=true;}
    const current=()=>!disposed&&root.isConnected;
    const message=text=>{if(current())q('message').textContent=text;};
    function clear() {ready=false;bindings=[];jobs=[];retryAllowed=false;
      q('group').replaceChildren();q('group-details').textContent='';q('verified').checked=false;q('jobs').replaceChildren();q('observed').textContent='';
      if(url){URL.revokeObjectURL(url);url=null;}}
    function lock() {
      if(!current())return;
      q('connect').disabled=busy;q('refresh').disabled=busy||!token;q('disconnect').disabled=!token;
      for(const button of q('jobs').querySelectorAll('button'))button.disabled=busy||!token;
      const blocked=busy||!token||!ready||storageBlocked||Boolean(pending);
      q('group').disabled=blocked;q('verified').disabled=blocked;
      q('create').disabled=blocked||!q('verified').checked||!bindings.some(b=>b.bindingRef===q('group').value);
      for(const control of q('jobs').querySelectorAll('select'))control.disabled=blocked;
      for(const control of q('jobs').querySelectorAll('input'))control.disabled=blocked;
      for(const button of q('jobs').querySelectorAll('button'))if(button.dataset.mutation)button.disabled=blocked;
      q('retry').disabled=busy||!token||!ready||storageBlocked||!pending||!retryAllowed;
      q('pending').textContent=storageBlocked?'La memoria della richiesta non è verificabile. Nessun nuovo comando è consentito; conserva questa sessione per il recupero supervisionato.':
        pending?(token?'Richiesta conservata: '+pending.action+' · '+pending.jobId+'. Aggiorna lo stato prima di ripetere lo stesso comando.':'Una richiesta è conservata in questa sessione. Accedi per verificarne lo stato.') : '';
    }
    function disconnect() {epoch++;token='';controller?.abort();clear();q('signin').replaceChildren();
      message('Accesso terminato. Le evidenze sul PC e sul servizio sono conservate.');lock();}
    active={root,dispose(){disposed=true;epoch++;token='';controller?.abort();clear();q('signin').replaceChildren();}};
    const el=(tag,text,parent)=>{const node=document.createElement(tag);node.textContent=text;parent.append(node);return node;};
    function download(job) {
      if(!current()||!token||busy)return;
      // Export only the already validated minimized Owner view; never the full local report.
      const receipt={kind:'BKL051_OWNER_STATUS_SNAPSHOT_V1',source:'AUTHENTICATED_SERVICE_VIEW',
        localBytesVerified:false,scientificValidation:'NOT_VALIDATED',publication:'NONE',job};
      if(url)URL.revokeObjectURL(url);
      url=URL.createObjectURL(new Blob([JSON.stringify(receipt,null,2)],{type:'application/json'}));
      const link=document.createElement('a');link.href=url;link.download=job.jobId+'-ricevuta-stato.json';link.click();
    }
    function render(jobs) {
      clear();
      if(!jobs.length)el('p','Nessuna analisi registrata nel servizio.',q('jobs'));
      for(const job of [...jobs].reverse()) {
        const card=el('article','',q('jobs'));el('h3',labels[job.state],card);
        el('p',job.jobId,card);el('p','Ultimo aggiornamento del servizio: '+job.updatedAt,card);
        if(job.cancelRequested&&!['CANCELLED','RECOVERY_REQUIRED'].includes(job.state))
          el('p','Annullamento richiesto: l’arresto del processo non è ancora confermato.',card);
        if(job.state==='RECOVERY_REQUIRED')el('p','Stato incerto. Conserva il tentativo e verifica il PC con l’assistente prima di riprendere.',card);
        const refs=el('details','',card);el('summary','Riferimenti della richiesta',refs);
        const list=el('dl','',refs);
        for(const [key,label] of [['bindingRef','Gruppo registrato'],['inputRef','Immagine'],['referenceRef','Riferimento'],
          ['algorithmRef','Algoritmo'],['contractRef','Contratto']]){el('dt',label,list);el('dd',job.binding[key],list);}
        if(job.result) {
          const counts=job.result.qualityCounts;
          el('p',`Conteggi comunicati dal PC: misurati ${counts.measured}, esclusi ${counts.excluded}, incompleti ${counts.incomplete}. Non sono conteggi di scoperte.`,card);
          el('p','Impronta del rapporto conservato sul PC: '+job.result.reportSha256,card);
        }
        for(const review of job.reviews)el('p',`Valutazione Owner dichiarata: ${decisions[review.request.decision]} · ${review.recordedAt}.`,card);
        el('p','Esecuzione comunicata dal PC, senza attestazione indipendente. Validazione scientifica non completata. Immagini e rapporto completo restano sul PC; nessuna pubblicazione.',card);
        const button=el('button','Scarica ricevuta dello stato',card);button.type='button';button.addEventListener('click',()=>download(job));
        if(!['COMPLETED','FAILED','CANCELLED','RECOVERY_REQUIRED'].includes(job.state)&&!job.cancelRequested) {
          const cancel=el('button','Richiedi annullamento',card);cancel.type='button';cancel.dataset.mutation='true';
          cancel.addEventListener('click',()=>run(()=>start('CANCEL',job,{})));
        }
        if(job.result) {
          const label=el('label','',card),confirmed=el('input','',label);confirmed.type='checkbox';
          el('span',' Ho consultato sul PC il rapporto con questa impronta. La valutazione non conferma una scoperta.',label);
          const choice=el('select','',card);choice.setAttribute('aria-label','Valutazione del rapporto');
          const empty=el('option','Scegli una valutazione',choice);empty.value='';
          for(const [value,text] of Object.entries(decisions)){const option=el('option',text,choice);option.value=value;}
          const review=el('button','Registra valutazione dichiarata',card);review.type='button';review.dataset.mutation='true';
          review.addEventListener('click',()=>{if(confirmed.checked&&Object.hasOwn(decisions,choice.value))
            run(()=>start('REVIEW',job,{decisionId:identifier(),reportSha256:job.result.reportSha256,decision:choice.value}));});
        }
      }
      q('observed').textContent='Consultazione aggiornata ora. Nessun controllo periodico; il PC potrebbe avere uno stato successivo.';
    }
    async function call(path,method='GET',body) {
      require(path==='/options'||path==='/jobs'||/^\/jobs\/TRN_[a-f0-9]{32}\/(?:cancel|review)$/.test(path));
      const session=epoch,credential=token;require(current()&&credential);controller=new AbortController();
      const requestController=controller;
      const timer=setTimeout(()=>requestController.abort(),30000);
      try {
        const response=await fetch(ORIGIN+'/v1/transient-analysis'+path,{method,cache:'no-store',credentials:'omit',
          redirect:'error',signal:requestController.signal,headers:{Authorization:'Bearer '+credential,...(method==='POST'?{'Content-Type':'application/json'}:{})},
          ...(method==='POST'?{body:JSON.stringify(body)}:{})});
        require(current()&&session===epoch);
        if(response.status===404){clear();message('Il servizio di analisi non è attivato. Nessuna nuova analisi è stata avviata dalla pagina; eventuali richieste conservate restano da verificare.');return null;}
        if(response.status===401||response.status===403){disconnect();message('Accesso non autorizzato o scaduto. Accedi di nuovo con l’account Owner.');return null;}
        if(!response.ok)throw new Error('Servizio non disponibile. Premi Aggiorna stato per una nuova consultazione.');
        require((response.headers.get('Content-Type')||'').split(';')[0].trim()==='application/json');
        const text=await readResponse(response);
        require(current()&&session===epoch);return JSON.parse(text);
      } finally {clearTimeout(timer);}
    }
    function reconcile() {
      retryAllowed=false;if(!pending)return '';
      const registered=bindings.find(b=>b.bindingRef===pending.binding.bindingRef);
      require(registered&&same(registered,pending.binding));
      const job=jobs.find(j=>j.jobId===pending.jobId);let confirmed=false,noEffect=false;
      if(job)require(same(inspectBinding(job.binding),pending.binding));
      if(pending.action==='CREATE') {if(job){require(same(job.request,pending.body));confirmed=true;}else retryAllowed=true;}
      else {require(job);
        if(pending.action==='CANCEL') {confirmed=job.cancelRequested;
          noEffect=!confirmed&&['COMPLETED','FAILED','CANCELLED','RECOVERY_REQUIRED'].includes(job.state);retryAllowed=!confirmed&&!noEffect;}
        else {require(job.state==='COMPLETED'&&job.result.reportSha256===pending.body.reportSha256);
          const review=job.reviews.find(r=>r.request.decisionId===pending.body.decisionId);
          if(review){require(same(review.request,pending.body));confirmed=true;}else retryAllowed=true;}
      }
      if(confirmed||noEffect) {
        try{sessionStorage.removeItem(pendingKey);require(sessionStorage.getItem(pendingKey)===null);}
        catch{storageBlocked=true;throw Error('Storage unavailable');}
        const action=pending.action;pending=null;
        return noEffect?'Il lavoro è già terminale: nessun annullamento attribuito a questa richiesta.':
          action==='CANCEL'?'Richiesta di annullamento registrata. Lo stato del PC va verificato separatamente.':
          action==='REVIEW'?'Valutazione Owner dichiarata registrata sul rapporto esatto.':'Richiesta di analisi registrata. Il completamento resta da verificare.';
      }
      return 'Esito del comando ancora da verificare. Puoi ripetere esplicitamente la medesima richiesta.';
    }
    async function refresh() {
      clear();const options=await call('/options');if(options===null)return;
      const checkedBindings=inspectOptions(options),value=await call('/jobs');if(value===null)return;
      const checkedJobs=inspectJobs(value);
      bindings=checkedBindings;jobs=checkedJobs;
      for(const job of jobs){const registered=bindings.find(b=>b.bindingRef===job.binding.bindingRef);require(registered&&same(registered,inspectBinding(job.binding)));}
      const result=storageBlocked?'':reconcile(),canRetry=retryAllowed;
      render(jobs);bindings=checkedBindings;jobs=checkedJobs;ready=true;retryAllowed=canRetry;
      const empty=el('option','Seleziona il gruppo verificato sul PC',q('group'));empty.value='';
      for(const [index,binding] of bindings.entries()){const option=el('option','Gruppo '+(index+1)+' · '+binding.bindingRef,q('group'));option.value=binding.bindingRef;}
      q('group').value='';message(result||'Stato letto dal servizio privato. Il rapporto completo va verificato sul PC.');
    }
    function identifier() {return Array.from(crypto.getRandomValues(new Uint8Array(16)),v=>v.toString(16).padStart(2,'0')).join('');}
    async function start(action,job,body) {
      require(ready&&!pending&&!storageBlocked&&token);
      try {require(sessionStorage.getItem(pendingKey)===null);}catch{storageBlocked=true;throw Error('Storage unavailable');}
      pending=inspectPending({kind:'BKL051_OWNER_PENDING_ACTION_V1',action,jobId:job.jobId,binding:job.binding,body});
      try {const text=JSON.stringify(pending);sessionStorage.setItem(pendingKey,text);require(sessionStorage.getItem(pendingKey)===text);}
      catch{storageBlocked=true;throw Error('Storage unavailable');}
      await send();
    }
    async function send() {
      require(pending&&!storageBlocked&&token&&ready);
      const saved=inspectPending(JSON.parse(sessionStorage.getItem(pendingKey)));require(same(saved,pending));
      retryAllowed=false;ready=false;lock();
      const path=pending.action==='CREATE'?'/jobs':'/jobs/'+pending.jobId+'/'+(pending.action==='CANCEL'?'cancel':'review');
      const value=await call(path,'POST',pending.body);if(value===null)return;
      const acknowledged=inspectJobs({jobs:[value]})[0];require(acknowledged.jobId===pending.jobId&&same(inspectBinding(acknowledged.binding),pending.binding));
      await refresh();
    }
    async function run(action) {
      if(busy||!current())return;busy=true;lock();
      try {await action();}catch {if(current()&&(token||!controller?.signal.aborted)){clear();message(pending?
        'Consultazione non riuscita o ricevuta non valida. Nessun risultato mostrato; richiesta conservata. Aggiorna lo stato prima di riprovare manualmente.':
        'Consultazione non riuscita o ricevuta non valida. Nessun risultato mostrato; riprova manualmente.');}}
      finally {busy=false;lock();}
    }
    q('refresh').addEventListener('click',()=>run(refresh));q('disconnect').addEventListener('click',disconnect);
    q('group').addEventListener('change',()=>{q('verified').checked=false;
      const binding=bindings.find(b=>b.bindingRef===q('group').value);
      q('group-details').textContent=binding?'Immagine: '+binding.inputRef+' · Riferimento: '+binding.referenceRef+
        ' · Algoritmo: '+binding.algorithmRef+' · Contratto: '+binding.contractRef:'';lock();});q('verified').addEventListener('change',lock);
    q('create').addEventListener('click',()=>run(async()=>{require(q('verified').checked);
      const binding=bindings.find(b=>b.bindingRef===q('group').value);require(binding);const requestId=identifier();
      await start('CREATE',{jobId:'TRN_'+requestId,binding},{requestId,bindingRef:binding.bindingRef});}));
    q('retry').addEventListener('click',()=>run(async()=>{require(retryAllowed);await send();}));
    q('connect').addEventListener('click',()=>run(async()=>{
      if(!window.google?.accounts?.id)await new Promise((resolve,reject)=>{
        const script=document.createElement('script');script.src='https://accounts.google.com/gsi/client';
        script.onload=resolve;script.onerror=reject;document.head.append(script);
      });
      if(!current())return;
      const loginEpoch=++epoch;
      google.accounts.id.initialize({client_id:CLIENT,callback:response=>{
        if(!current()||loginEpoch!==epoch||typeof response.credential!=='string'||!response.credential)return;
        run(async()=>{clear();token=response.credential;lock();await refresh();});
      }});
      q('signin').replaceChildren();google.accounts.id.renderButton(q('signin'),{theme:'outline',size:'large'});
      message('Accedi con l’account Owner per leggere lo stato privato.');
    }));
    lock();
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',initialize);else initialize();
  if(typeof document$!=='undefined')document$.subscribe(initialize);
})();
