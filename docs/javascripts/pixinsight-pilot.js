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
      q('fields').disabled = busy || !token || !options || Boolean(frozen);
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
      if(result.context.intent){
        el('p',`Prompt concordato: ${result.context.intent.intake.selection.prompt}`,q('summary'));
        el('p',`Piano confermato: ${result.context.intent.plan.rationale}`,q('summary'));
      }
      el('p',`Workflow: ${result.workflowId}. Originale: ${result.original.width} × ${result.original.height}, non lineare.`,q('summary'));
      el('p',`Sessioni dichiarate: ${result.context.selection.sessionIds.join(', ')}`,q('summary'));
      el('p','Il PC ha verificato l’esecuzione; il servizio conserva il rapporto del worker senza attestazione indipendente. Il workflow descrive la nuova ricetta e la preparazione dei master quando presente; la History precedente resta da verificare.',q('summary'));
      el('p',result.decision?`Valutazione conservata: ${result.decision.decision}. Nessuna pubblicazione.`:'In attesa della tua valutazione scientifica.',q('summary'));
      q('steps').replaceChildren();const list=el('ol','',q('steps'));
      result.steps.forEach(step=>el('li',step.processId,list));lock();
    }
    async function refresh() {

      const {intakes}=await call('/v1/science/intakes');q('plans').replaceChildren();
      if(!intakes.length)el('p','Nessuna cartella e nessun prompt in attesa di verifica.',q('plans'));
      for(const intake of [...intakes].reverse()){
        const card=el('article','',q('plans')), selection=intake.selection;
        el('h3',selection.title,card);
        el('p',`Cartella sul PC: ${selection.masterDirectory}`,card);
        el('p',`Prompt: ${selection.prompt}`,card);
        if(selection.sourceProfile)el('p',`Master: ${selection.sourceProfile.mode} · ${selection.sourceProfile.layout==='PANELS'?'pannelli da unire':'campo singolo'} · oggetto ${intake.target || ''}.`,card);
        if(intake.state==='JOB_CREATED'){el('p','Piano confermato: elaborazione presente nello stato qui sotto.',card);continue;}
        if(intake.sourcePlan){
          el('h4','Selezione dei pannelli',card);
          el('p',intake.sourcePlan.rationale,card);el('p',`Limiti: ${intake.sourcePlan.limitations}`,card);
          for(const panel of intake.sourcePlan.panels){
            el('p',`${panel.panelId} · ${panel.directory} · sessioni ${panel.sessionIds.join(', ')}`,card);
            const files=el('ul','',card);
            for(const [role,master] of Object.entries(panel.masters))el('li',`${role}: ${master.filename} · indice immagine ${master.imageIndex}`,files);
          }
          if(intake.sourceSelectionApproved)el('p','Selezione dei pannelli confermata. Il piano di assemblaggio ed elaborazione resta da verificare; nessun avvio automatico.',card);
          else {
            const confirm=el('button','Conferma selezione dei pannelli',card);confirm.type='button';
            confirm.addEventListener('click',()=>run(async()=>{
              const next=await call(`/v1/science/intakes/${selection.requestId}/approve-sources`,{sourcePlanSha256:intake.sourcePlanSha256});
              if(next.requestId!==selection.requestId || next.nativeStarted!==false)throw new Error('Risposta di conferma non valida. Conserva la selezione.');
              await refresh();message('Selezione confermata. L’assistente può verificare questi master; nessuna elaborazione avviata.');
            }));
          }
        }
        if(intake.preparationPlan){
          const preparation=intake.preparationPlan;
          el('h4','Preparazione dei master',card);
          el('p',preparation.rationale,card);el('p',`Limiti: ${preparation.limitations}`,card);
          const masters=el('ul','',card);
          preparation.masters.forEach(m=>el('li',`${m.panelId} · ${m.role}: ${m.filename} · ${m.width} × ${m.height} · indice ${m.imageIndex}`,masters));
          if(preparation.bayerPattern)el('p',`Demosaicizzazione: pattern ${preparation.bayerPattern}, metodo VNG.`,card);
          if(preparation.canvas)el('p',`Mosaico su griglia comune ${preparation.canvas.width} × ${preparation.canvas.height}; centro ${preparation.canvas.centerRA}, ${preparation.canvas.centerDec}; scala ${preparation.canvas.resolution} gradi/pixel; rotazione ${preparation.canvas.rotation}°.`,card);
          el('p',`${preparation.nativeProcessCount} processi nativi · ${preparation.checkpointCount} file di controllo. L’elaborazione finale richiederà un piano e una conferma separati.`,card);
          if(intake.preparationResult)el('p','Master preparati e verificati dal PC. In attesa della tua conferma del piano di elaborazione finale; risultato ancora lineare.',card);
          else if(intake.preparationApproved)el('p','Preparazione confermata. L’assistente può eseguirla sul PC in PixInsight; nessun avvio automatico dal browser.',card);
          else {
            const confirm=el('button','Conferma preparazione dei master',card);confirm.type='button';
            confirm.addEventListener('click',()=>run(async()=>{
              const next=await call(`/v1/science/intakes/${selection.requestId}/approve-preparation`,{preparationPlanSha256:intake.preparationPlanSha256});
              if(next.requestId!==selection.requestId || next.nativeStarted!==false)throw new Error('Risposta di conferma non valida. Conserva il piano.');
              await refresh();message('Preparazione confermata. L’avvio in PixInsight sul PC resta supervisionato; il piano finale sarà confermato separatamente.');
            }));
          }
        }
        if(!intake.plan){el('p',intake.preparationResult?'L’assistente proporrà il piano di elaborazione finale sui master verificati.':intake.preparationApproved?'L’assistente completerà la verifica dei master preparati e proporrà il piano finale.':'In attesa della verifica e del piano dell’assistente. Nessuna elaborazione avviata.',card);continue;}
        const plan=intake.plan;
        el('p',plan.rationale,card);el('p',`Limiti: ${plan.limitations}`,card);
        el('p',`Master verificati dal PC: ${plan.masters.map(m=>`${m.role} ${m.width} × ${m.height}, indice ${m.imageIndex}`).join('; ')}.`,card);
        el('p',`Fondo: grado ${plan.background.polyDegree}, campione ${plan.background.boxSize}, separazione ${plan.background.boxSeparation}. ${plan.steps.length} processi · ${plan.checkpointCount} checkpoint.`,card);
        const tuning=plan.processing;
        el('p',`Dettaglio L/RGB: ${tuning.sharpenL}/${tuning.sharpenRGB}; riduzione rumore L/RGB: ${tuning.denoiseL}/${tuning.denoiseRGB}; contrasto ampio/fine: ${tuning.contrastLarge}/${tuning.contrastSmall}; fondo dopo stretch: ${tuning.targetBackground}.`,card);
        if(plan.field)el('p',`Campo ${plan.field.target}: fondo verificato [${plan.field.backgroundROI.join(', ')}], maschera ${plan.field.maskLow}–${plan.field.maskHigh}, raggi contrasto ${plan.field.contrastLargeRadius}/${plan.field.contrastSmallRadius}, saturazione ${plan.field.saturation}, stretch stelle ${plan.field.starsStretch}.`,card);
        const steps=el('ol','',card);plan.steps.forEach(process=>el('li',process,steps));
        const button=el('button','Conferma piano e richiedi elaborazione',card);button.type='button';
        button.addEventListener('click',()=>run(async()=>{
          const job=await call(`/v1/science/intakes/${selection.requestId}/approve`,{proposalSha256:intake.proposalSha256});
          if(job.jobId!==`PIAI_${selection.requestId}`)throw new Error('Identità della risposta non valida. Ripeti la conferma dello stesso piano.');
          await refresh();message('Piano confermato e job conservato. L’assistente può preparare le copie sul PC; l’avvio PixInsight resta supervisionato.');
        }));
      }
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
    const targetKey=value=>typeof value==='string'?value.replace(/^(M|NGC|IC) +(?=\d+$)/,'$1'):value;
    function renderSources() {
      const selected=targetKey(q('target').value);
      q('parent').replaceChildren();el('option','Nuova immagine',q('parent')).value='';
      q('parent').value='';
      options.images.forEach((image,index)=>{if(targetKey(image.target)===selected)el('option',`${image.title} · ${image.imageVersionId}`,q('parent')).value=String(index);});
      q('sessions').replaceChildren();
      for(const session of options.sessions.filter(s=>targetKey(s.target)===selected)){const label=el('label','',q('sessions'));label.className='dsg-photo-upload__check';
        const check=document.createElement('input');check.type='checkbox';check.value=session.sessionId;check.dataset.sessionChoice='';label.append(check,document.createTextNode(`${session.target} · ${session.observationDate || ''} · ${session.sessionId}`));}
    }
    async function loadOptions() {
      options=await call('/v1/science/options');q('target').replaceChildren();
      const targets=[...new Set(options.sessions.map(s=>targetKey(s.target)))];
      targets.forEach(target=>{el('option',target,q('target')).value=target;});q('target').value=targets[0] || '';
      renderSources();
      q('date').value=new Date().toLocaleDateString('en-CA');await refresh();
      message('Accesso Owner verificato. Indica cartella, prompt e sessioni. Se hai già un risultato, premi «Apri anteprima e workflow» per riabilitare i download.');
    }
    async function submitFrozen() {
      let job;
      const isIntake=typeof frozen.masterDirectory==='string';
      try {job=await call(isIntake?'/v1/science/intakes':'/v1/science/jobs',frozen);}
      catch(error) {
        if(error.status===400) {
          let absent=false;
          try {await call(isIntake?`/v1/science/intakes/${frozen.requestId}`:`/v1/jobs/PIAI_${frozen.requestId}`);}
          catch(check) {absent=check.status===400 && check.code===(isIntake?'INTAKE_NOT_FOUND':'JOB_NOT_FOUND');}
          if(absent) {
            sessionStorage.removeItem(KEY);frozen=null;await loadOptions();
            message(`Richiesta rifiutata e assenza ${isIntake?'della richiesta di piano':'del job'} verificata. Catalogo e riferimenti aggiornati: seleziona nuovamente i dati e invia.`);
            return;
          }
        }
        throw error;
      }
      if(isIntake?job.requestId!==frozen.requestId:job.jobId!==`PIAI_${frozen.requestId}`)throw new Error('Identità della risposta non valida. Conserva la richiesta.');
      sessionStorage.removeItem(KEY);frozen=null;await refresh();message(isIntake?'Cartella e prompt conservati. L’assistente deve verificare i master e proporre il piano; nessun job PixInsight avviato.':'Richiesta scientifica conservata.');
    }
    q('form').addEventListener('submit',event=>{event.preventDefault();run(async()=>{
      if(!frozen){
        const sessionIds=[...q('sessions').querySelectorAll('input:checked')].map(node=>node.value);
        if(!sessionIds.length || !q('attest').checked)throw new Error('Seleziona le sessioni e conferma l’associazione ai master.');
        if(!q('directory').value.trim() || !q('prompt').value.trim())throw new Error('Indica la cartella completa e il risultato desiderato.');
        const image=q('parent').value===''?null:options.images[Number(q('parent').value)];
        const mode=q('mode').value,layout=q('layout').value;
        const additionalDirectories=layout==='PANELS'?q('additional').value.split(/\r?\n/).map(v=>v.trim()).filter(Boolean):[];
        const bayerPattern=mode==='OSC_CFA'?q('bayer').value:null;
        if(mode==='OSC_CFA' && !bayerPattern)throw new Error('Indica lo schema Bayer verificato; non viene dedotto dal nome del file.');
        frozen={requestId:Array.from(crypto.getRandomValues(new Uint8Array(16)),x=>x.toString(16).padStart(2,'0')).join(''),
          masterDirectory:q('directory').value.trim(),prompt:q('prompt').value,catalogSha256:options.catalogSha256,sessionIds,
          sourceProfile:{mode,layout,bayerPattern,panels:[],additionalDirectories},
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
    q('target').addEventListener('change',()=>{if(options && !frozen)renderSources();});
    q('mode').addEventListener('change',()=>{q('bayer-label').hidden=q('mode').value!=='OSC_CFA';});
    q('layout').addEventListener('change',()=>{q('additional-label').hidden=q('layout').value!=='PANELS';});
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
