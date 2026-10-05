/* P5 private Owner requests and review; no script execution or publication. */
(() => {
  'use strict';
  const ORIGIN = 'https://dsg-pixinsight-pilot-183451329061.europe-west1.run.app';
  const CLIENT = '183451329061-8iedbjrn60u6iau42u1tlsonn6bi6hjd.apps.googleusercontent.com';
  const KEY = 'dsg-piai-scientific-request-v1';
  const labels = {QUEUED:'In coda',RESERVED:'Preso in carico dal PC',PREPARING:'Preparazione delle copie',
    PREPARED:'Copie pronte',AWAITING_NATIVE:'Avvia lo script preparato in PixInsight con l’assistente',
    RUNNING:'Elaborazione in corso',COMPLETED:'Elaborazione tecnica completata',FAILED:'Elaborazione non riuscita',
    CANCELLED:'Annullato',RECOVERY_REQUIRED:'Recupero supervisionato necessario'};
  function initialize() {
    const root = document.querySelector('[data-piai-science]');
    if (!root || root.dataset.initialized) return;
    root.dataset.initialized = 'true';
    const q = name => root.querySelector(`[data-p5-${name}]`);
    let token = '', busy = false, options, result, previewUrl, frozen;
    try { frozen = JSON.parse(sessionStorage.getItem(KEY)); } catch {}
    const message = text => { if (root.isConnected) q('message').textContent = text; };
    const el = (tag,text,parent) => {const node=document.createElement(tag);node.textContent=text;parent.append(node);return node;};
    function lock() {
      q('fields').disabled = busy || !token || !options?.inputs.length || Boolean(frozen);
      q('refresh').disabled = busy || !token;
      q('connect').disabled = busy;
      q('retry').hidden = !frozen; q('retry').disabled = busy || !token;
      q('pending').hidden = !frozen;
      q('pending').textContent = frozen ? `Richiesta conservata ${frozen.requestId}: ${frozen.title} · ${frozen.processingDate} · sessioni ${frozen.sessionIds?.join(', ')} · riferimento ${frozen.parent?.imageVersionId || 'nuova immagine'}. La ripetizione mantiene questi dati.` : '';
      for(const name of ['accept','reject','workflow','correlations','receipt'])q(name).disabled=busy || !token || !result ||
        (['accept','reject'].includes(name) && Boolean(result.decision));
    }
    async function call(path,value,binary=false) {
      if (!token) throw new Error('Accedi con l’account Owner.');
      const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),60000);
      try {
        const response=await fetch(ORIGIN+path,{method:value===undefined?'GET':'POST',cache:'no-store',credentials:'omit',
          redirect:'error',signal:controller.signal,headers:{Authorization:`Bearer ${token}`,...(value===undefined?{}:{'Content-Type':'application/json'})},
          body:value===undefined?undefined:JSON.stringify(value)});
        if(!response.ok) {
          if(response.status===403){token='';throw new Error('Accedi di nuovo. La richiesta conservata resta disponibile.');}
          const code=(await response.json()).error;
          if(code==='RESULT_PENDING')throw new Error('Il PC non ha ancora consegnato anteprima e workflow.');
          const error=new Error('Operazione non completata. Ripeti la stessa richiesta; non avviare un secondo job.');
          error.status=response.status;error.code=code;throw error;
        }
        return binary?response.blob():response.json();
      } finally {clearTimeout(timer);}
    }
    async function run(action) {
      if(busy)return;busy=true;lock();
      try{await action();}catch(error){message(error.message);}finally{busy=false;lock();}
    }
    function save(blob,name) {
      const url=URL.createObjectURL(blob),anchor=el('a','',root);anchor.href=url;anchor.download=name;anchor.click();anchor.remove();
      setTimeout(()=>URL.revokeObjectURL(url),1000);
    }
    async function showResult(jobId) {
      const next=await call(`/v1/science/${jobId}/result`);
      const image=await call(`/v1/science/${jobId}/preview`,undefined,true);
      if(previewUrl)URL.revokeObjectURL(previewUrl);
      result=next;previewUrl=URL.createObjectURL(image);q('preview').src=previewUrl;q('review').hidden=false;
      q('summary').replaceChildren();
      el('p',`${result.context.selection.title} · versione privata del pilota · ${result.imageId} · ${result.imageVersionId}`,q('summary'));
      el('p',`Workflow: ${result.workflowId}. Originale: ${result.original.width} × ${result.original.height}, non lineare.`,q('summary'));
      el('p',`Sessioni dichiarate: ${result.context.selection.sessionIds.join(', ')}`,q('summary'));
      el('p','Il PC ha verificato l’esecuzione; il servizio conserva il rapporto del worker senza attestazione indipendente. Il workflow descrive la ricetta eseguita, non tutta la History precedente.',q('summary'));
      el('p',result.decision?`Valutazione conservata: ${result.decision.decision}. Nessuna pubblicazione.`:'In attesa della tua valutazione scientifica.',q('summary'));
      q('steps').replaceChildren();const list=el('ol','',q('steps'));
      result.steps.forEach(step=>el('li',step.processId,list));lock();
    }
    async function refresh() {
      const {jobs}=await call('/v1/science/jobs');q('jobs').replaceChildren();
      if(!jobs.length)el('p','Nessuna richiesta scientifica.',q('jobs'));
      for(const job of [...jobs].reverse()) {
        const card=el('article','',q('jobs'));el('strong',job.jobId,card);
        const status=await call(`/v1/jobs/${job.jobId}`);
        el('p',`${labels[job.state] || job.state} · ${status.connection==='OFFLINE'?'PC senza contatto recente: prenotazione conservata':status.connection==='RECENT_CONTACT'?'Contatto recente con il PC':'Contatto PC non confermato'}`,card);
        if(job.report)el('p',`${job.report.processCount} operazioni · ${job.report.outputCount} checkpoint`,card);
        if(job.state==='COMPLETED'){
          const button=el('button','Apri anteprima e workflow',card);button.type='button';button.addEventListener('click',()=>run(()=>showResult(job.jobId)));
        } else if(!['FAILED','CANCELLED','RECOVERY_REQUIRED'].includes(job.state)){
          const button=el('button','Annulla richiesta',card);button.type='button';button.addEventListener('click',()=>run(async()=>{
            await call(`/v1/jobs/${job.jobId}/cancel`,{});message('Annullamento richiesto. Un processo già in corso può terminare prima dell’arresto.');await refresh();}));
        }
      }
    }
    async function loadOptions() {
      options=await call('/v1/science/options');q('input').replaceChildren();
      options.inputs.forEach((input,index)=>{const option=el('option',`${input.target} · master LRGB registrati ${index+1}`,q('input'));option.value=input.inputRef;});
      q('parent').replaceChildren();el('option','Nuova immagine',q('parent')).value='';
      options.images.forEach((image,index)=>{el('option',`${image.title} · ${image.imageVersionId}`,q('parent')).value=String(index);});
      q('sessions').replaceChildren();
      for(const session of options.sessions){const label=el('label','',q('sessions'));label.className='dsg-photo-upload__check';
        const check=document.createElement('input');check.type='checkbox';check.value=session.sessionId;check.dataset.sessionChoice='';label.append(check,document.createTextNode(`${session.observationDate || ''} · ${session.sessionId}`));}
      q('date').value=new Date().toLocaleDateString('en-CA');await refresh();
      message(options.inputs.length?'Accesso Owner verificato. Seleziona le sessioni e prepara la richiesta.':'Accesso Owner verificato. L’assistente deve registrare i master verificati sul PC.');
    }
    async function submitFrozen() {
      let job;
      try {job=await call('/v1/science/jobs',frozen);}
      catch(error) {
        if(error.status===400) {
          let absent=false;
          try {await call(`/v1/jobs/PIAI_${frozen.requestId}`);}
          catch(check) {absent=check.status===400 && check.code==='JOB_NOT_FOUND';}
          if(absent) {
            sessionStorage.removeItem(KEY);frozen=null;await loadOptions();
            message('Richiesta rifiutata e assenza del job verificata. Catalogo e riferimenti aggiornati: seleziona nuovamente i dati e invia.');
            return;
          }
        }
        throw error;
      }
      if(job.jobId!==`PIAI_${frozen.requestId}`)throw new Error('Identità della risposta non valida. Conserva la richiesta.');
      sessionStorage.removeItem(KEY);frozen=null;await refresh();message('Richiesta scientifica conservata. L’assistente può prepararla sul PC e avviare PixInsight sotto supervisione.');
    }
    q('form').addEventListener('submit',event=>{event.preventDefault();run(async()=>{
      if(!frozen){
        const sessionIds=[...q('sessions').querySelectorAll('input:checked')].map(node=>node.value);
        if(!sessionIds.length || !q('attest').checked)throw new Error('Seleziona le sessioni e conferma l’associazione ai master.');
        const image=q('parent').value===''?null:options.images[Number(q('parent').value)];
        frozen={requestId:Array.from(crypto.getRandomValues(new Uint8Array(16)),x=>x.toString(16).padStart(2,'0')).join(''),
          inputRef:q('input').value,catalogSha256:options.catalogSha256,sessionIds,
          parent:image?{imageId:image.imageId,imageVersionId:image.imageVersionId,workflowId:image.workflowId}:null,
          title:q('title').value,processingDate:q('date').value,associationConfirmed:true};
        sessionStorage.setItem(KEY,JSON.stringify(frozen));
      }
      await submitFrozen();
    });});
    q('retry').addEventListener('click',()=>run(submitFrozen));
    q('refresh').addEventListener('click',()=>run(refresh));
    for(const [name,decision] of [['accept','ACCEPT_PRIVATE'],['reject','REJECT']])q(name).addEventListener('click',()=>run(async()=>{
      await call(`/v1/science/${result.jobId}/decision`,{reviewSha256:result.reviewSha256,decision});await showResult(result.jobId);
      message(decision==='ACCEPT_PRIVATE'?'Risultato accettato privatamente. Nessuna pubblicazione eseguita.':'Valutazione conservata. Puoi preparare una nuova richiesta; nessun nuovo job avviato automaticamente.');
    }));
    q('workflow').addEventListener('click',()=>run(async()=>save(await call(`/v1/science/${result.jobId}/workflow`,undefined,true),`${result.workflowId}.js`)));
    q('correlations').addEventListener('click',()=>run(async()=>save(await call(`/v1/science/${result.jobId}/correlations`,undefined,true),`${result.workflowId}-correlazioni.json`)));
    q('receipt').addEventListener('click',()=>save(new Blob([JSON.stringify(result,null,2)],{type:'application/json'}),`${result.jobId}-collegamenti.json`));
    q('connect').addEventListener('click',()=>run(async()=>{
      if(!window.google?.accounts?.id)await new Promise((resolve,reject)=>{const script=document.createElement('script');script.src='https://accounts.google.com/gsi/client';script.onload=resolve;script.onerror=reject;document.head.append(script);});
      google.accounts.id.initialize({client_id:CLIENT,callback:response=>run(async()=>{token=response.credential;try{await loadOptions();}catch(error){token='';throw error;}})});
      q('signin').replaceChildren();google.accounts.id.renderButton(q('signin'),{theme:'outline',size:'large'});message('Accedi con l’account Owner.');
    }));
    lock();
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',initialize);else initialize();
  if(typeof document$!=='undefined')document$.subscribe(initialize);
})();
