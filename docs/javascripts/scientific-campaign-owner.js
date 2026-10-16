/* Owner metadata controls. Transport stays in the existing authenticated session closure. */
(() => {
  'use strict';
  const KEY='dsg-bkl051-campaign-pending-v1',LIMIT=16384;
  const names={CREATE:'Crea il piano',INPUT_REVIEW:'Registra la revisione del controllo',FREEZE:'Congela il piano',
    OUTCOME_REVIEW:'Registra la revisione dell’esito',FINALIZE:'Accetta la sola campagna dichiarata',REVOKE:'Revoca la campagna'};
  const statuses={BLOCKED:'Requisiti ancora incompleti',READY_FOR_OWNER_FINAL_REVIEW:'Pronta per la revisione finale Owner',
    OWNER_ACCEPTED_CAMPAIGN_SCOPE_ONLY:'Campagna dichiarata accettata dall’Owner'};
  const descriptions={CREATE:'Registra un nuovo piano; non avvia il collaudo.',
    INPUT_REVIEW:'Conferma riferimento nullo, indipendenza, modello scientifico e separazione dallo sviluppo per il controllo indicato.',
    FREEZE:'Fissa algoritmo, regole e campione dopo la revisione dell’indipendenza e della separazione dallo sviluppo.',
    OUTCOME_REVIEW:'Accetta l’esito dichiarato sulla precisa evidenza privata indicata nella ricevuta.',
    FINALIZE:'Accetta soltanto la campagna dichiarata, alle condizioni e nei limiti delle prove esaminate.',
    REVOKE:'Conserva le decisioni precedenti e revoca l’idoneità corrente della campagna.'};
  const outcomes={NO_ALERT:'Nessuna segnalazione dichiarata',FALSE_ALERT:'Falsa segnalazione',INCONCLUSIVE:'Inconcludente'};
  const proofs={algorithmSha256:'Impronta dell’algoritmo',contractSha256:'Impronta delle regole',planHeadSha256:'Versione esatta del piano',
    witnessSha256:'Impronta del controllo',nullReferenceSha256:'Riferimento nullo',independenceSha256:'Valutazione dell’indipendenza',
    modelReviewSha256:'Valutazione del modello scientifico',separationEvidenceSha256:'Separazione dallo sviluppo',
    expectedInputReviewSha256:'Revisioni degli input',independenceReviewSha256:'Indipendenza dell’intero campione',
    developmentSeparationReviewSha256:'Separazione dell’intero campione',executionSha256:'Impronta dell’esito',evidenceSha256:'Evidenza della revoca'};
  const blockers={NOT_RESERVED_REAL_CONTROL:'Dato non riservato al collaudo reale',NOT_THREE_SCIENCE_EXPOSURES:'Servono tre esposizioni scientifiche',
    REPEATED_INPUT_OR_EXPOSURE:'Immagini o esposizioni ripetute',BANDPASS_COMPARABILITY_MISSING:'Comparabilità di banda mancante',
    CALIBRATION_OR_FULL_MODEL_UNCERTAINTY_MISSING:'Calibrazione o incertezza del modello incompleta',ACQUISITION_TIME_NOT_VERIFIED:'Tempo di acquisizione non verificato',
    NOT_STRICTLY_CHRONOLOGICAL:'Ordine temporale non verificato',OWNER_INPUT_REVIEW_MISSING:'Revisione Owner degli input mancante',
    INPUT_REVIEW_DIFFERENT_ALGORITHM_OR_RULES:'Revisione riferita ad algoritmo o regole differenti',DEPENDENCY_GROUP_REUSED:'Gruppo di dipendenza ripetuto',
    OBSERVATION_REUSED:'Osservazione riutilizzata',DEVELOPMENT_INPUT_OVERLAP:'Sovrapposizione con dati di sviluppo o sintetici',
    EARLIER_FROZEN_SAMPLE_REUSED:'Campione congelato precedente riutilizzato',PLAN_NOT_FROZEN:'Piano non congelato',PLAN_REVOKED:'Piano revocato',
    COMPLETE_REVIEWED_SAMPLE_MISSING:'Campione completo e revisionato mancante',ZERO_EVENT_CRITERION_FAILED:'Criterio a zero false segnalazioni non soddisfatto'};
  const events={CREATE:'Creazione del piano',FREEZE:'Congelamento',EXECUTION:'Esito comunicato dal PC',OUTCOME_REVIEW:'Revisione dell’esito',
    FINAL_OWNER_ACCEPTANCE:'Accettazione della sola campagna',REVOCATION:'Revoca',DISPATCH_INTENT:'Preparazione tecnica Owner',
    START_ADMISSION:'Ammissione tecnica del frame',FRAME_CLOSURE:'Chiusura tecnica dichiarata',
    UNRESERVED_FENCED_CLOSURE:'Chiusura senza avvio dopo annullamento verificato'};
  const check=ok=>{if(!ok)throw Error('Operazione del collaudo non verificabile.');};
  function mount(root,host){
    const api=globalThis.DSGCampaignContract;check(api);
    const q=name=>root.querySelector(`[data-campaign-${name}]`);
    let authorized=false,busy=false,queueBlocked=true,disposed=false,epoch=0,loadVersion=0;
    let pending=null,storageBlocked=false,retryAllowed=false,loaded=null,view=null,listed=false,selected='',viewVersion=0;
    const current=()=>!disposed&&root.isConnected;
    const el=(tag,text,parent)=>{const n=document.createElement(tag);n.textContent=text;parent.append(n);return n;};
    const say=text=>{if(current())q('status').textContent=text;};
    try{const raw=sessionStorage.getItem(KEY);if(raw!==null){check(raw.length<=LIMIT);pending=api.action(JSON.parse(raw));}}
    catch{storageBlocked=true;}
    function lock(){
      if(!current())return;
      const denied=!authorized||busy,blocked=denied||queueBlocked||storageBlocked;
      q('refresh').disabled=denied;q('select').disabled=denied||Boolean(pending)||!listed;
      q('open').disabled=denied||!selected;
      q('file').disabled=blocked||Boolean(pending);
      q('confirmed').disabled=blocked||!(loaded||pending);
      q('send').disabled=blocked||!listed||!loaded||Boolean(pending)||!q('confirmed').checked;
      q('retry').disabled=blocked||!pending||!retryAllowed||!q('confirmed').checked;
      q('pending').textContent=storageBlocked?'Memoria della richiesta non verificabile: registrazioni bloccate.':
        pending?(authorized?'Richiesta conservata: '+names[pending.action]+'. Aggiorna le campagne per verificarne l’esito.':
          'Una richiesta è conservata. Accedi per riconciliarla.') : '';
    }
    function clearView(){viewVersion++;view=null;q('result').replaceChildren();retryAllowed=false;}
    function preview(value){
      q('preview').replaceChildren();if(!value||!authorized)return;
      el('p',names[value.action],q('preview'));el('p','Piano: '+value.planRef,q('preview'));
      el('p',descriptions[value.action],q('preview'));
      if(value.witnessRef)el('p','Controllo: '+value.witnessRef,q('preview'));
      for(const [key,digest] of Object.entries(value.request))if(key.endsWith('Sha256'))
        el('p',(proofs[key]||'Impronta di verifica')+': '+digest,q('preview'));
    }
    function stored(){
      try{const raw=sessionStorage.getItem(KEY);check(typeof raw==='string'&&raw.length<=LIMIT
        &&JSON.stringify(api.action(JSON.parse(raw)))===JSON.stringify(pending));}
      catch{storageBlocked=true;throw Error('Richiesta conservata alterata.');}
    }
    function forgetConfirmed(){
      stored();try{sessionStorage.removeItem(KEY);check(sessionStorage.getItem(KEY)===null);}
      catch{storageBlocked=true;throw Error('Impossibile confermare la memoria della richiesta.');}
      pending=null;loaded=null;retryAllowed=false;q('confirmed').checked=false;preview(null);
    }
    function render(){
      const out=q('result');out.replaceChildren();if(!view)return;
      const s=view.campaign;
      el('h3',statuses[s.status],out);
      el('p',`Candidati: 59 · Esiti registrati: ${s.executionRecords} · Controlli qualificati nel piano: ${s.qualifiedControls}`,out);
      el('p',`Revisioni degli input: ${s.ownerReviewedInputs}/59 · False segnalazioni: ${s.falseAlertRecords}`,out);
      el('p',s.statisticalResult?`Limite superiore condizionato: ${(100*s.statisticalResult.oneSidedUpperBound).toFixed(5)}%, confidenza 95%.`:
        'Risultato statistico non disponibile: i requisiti del piano non sono tutti soddisfatti.',out);
      el('p','La qualificazione dipende dalle prove private esaminate e dalle regole congelate. Questa ricevuta non verifica i file sul PC e non convalida l’intera milestone.',out);
      const references=el('details','',out);el('summary','Versione e impronte del piano',references);
      for(const [label,value] of [['Piano',s.planSha256],['Ultimo evento',s.headSha256],
        ['Algoritmo',view.plan.algorithmSha256],['Regole',view.plan.contractSha256]])el('p',label+': '+value,references);
      if(s.blockers.length)el('p','Requisiti mancanti: '+s.blockers.map(r=>blockers[r]).join('; '),out);
      const region=el('div','',out);region.setAttribute('role','region');region.setAttribute('aria-label','Tutti i controlli del piano');region.tabIndex=0;
      const table=el('table','',region),head=el('tr','',el('thead','',table));
      for(const title of ['Controllo','Revisione input','Esito','Revisione esito'])el('th',title,head).scope='col';
      const body=el('tbody','',table);
      for(const [i,c] of s.cases.entries()){
        const row=el('tr','',body),cell=el('td',String(i+1)+' · ',row);el('code',c.witnessRef,cell);
        el('td',c.inputReviewedByOwner?'Registrata':'Mancante',row);
        const record=view.executions.find(e=>e.sha256===c.executionSha256);
        const result=el('td',record?outcomes[record.request.outcome]:'Non eseguito',row);
        if(record){
          const proofs=el('details','',result);el('summary','Impronte delle prove sul PC',proofs);
          el('p','Esito esatto: '+record.sha256,proofs);
          el('p','Documento scientifico privato: '+record.request.scienceEvidenceSha256,proofs);
          for(const [j,job] of record.request.jobs.entries())el('p','Rapporto tecnico '+(j+1)+': '+(job.reportSha256||'Non disponibile'),proofs);
        }
        el('td',record?.review?'Registrata':'Mancante',row);
      }
      const details=el('details','',out);el('summary','Cronologia delle registrazioni',details);
      for(const e of view.events)el('p',e.recordedUTC+' · '+events[e.kind]+' · '+e.sha256,details);
    }
    function validEpoch(generation){check(current()&&authorized&&generation===epoch);}
    async function open(planRef,generation){
      clearView();const version=viewVersion,raw=await host.request('/campaigns/'+planRef+'/review-receipt');validEpoch(generation);check(version===viewVersion);
      check(raw!==null);const checked=await api.receipt(raw);validEpoch(generation);check(version===viewVersion);
      check(checked.campaign.planRef===planRef);view=checked;selected=planRef;render();
    }
    async function reconcile(generation){
      if(!pending)return;stored();let result;
      if(pending.action==='CREATE')result=api.reconcileCreate(view,pending.request);
      else if(pending.action==='INPUT_REVIEW'){
        check(view.plan.inputWitnessRefs.includes(pending.witnessRef));
        const raw=await host.request('/campaigns/inputs/'+pending.witnessRef);validEpoch(generation);check(raw!==null);
        const input=await api.input(raw);validEpoch(generation);check(input.request.witnessRef===pending.witnessRef);
        result=api.reconcileInput(input,pending.request);
      }else result=api.reconcile(view,pending.request);
      stored();
      if(result==='CONFIRMED'){forgetConfirmed();say('Registrazione confermata sulla richiesta esatta. Nessuna analisi avviata.');}
      else{retryAllowed=result==='NOT_OBSERVED';say(retryAllowed?
        'Richiesta non osservata nella ricevuta corrente. Resta conservata; puoi ripetere manualmente soltanto la stessa registrazione.':
        'La decisione registrata non coincide: richiesta conservata e nuove registrazioni bloccate.');}
    }
    async function refresh(){
      const generation=epoch;clearView();listed=false;q('confirmed').checked=false;
      const response=await host.request('/campaigns');validEpoch(generation);
      if(response===null){say('Registro del collaudo non disponibile. Le richieste conservate restano da verificare.');return;}
      check(response&&Object.keys(response).length===1&&Array.isArray(response.campaigns)&&response.campaigns.length<=8);
      const summaries=response.campaigns.map(api.summary);check(new Set(summaries.map(s=>s.planRef)).size===summaries.length);
      q('select').replaceChildren();const blank=el('option','Seleziona una campagna',q('select'));blank.value='';
      for(const [i,s] of summaries.entries())el('option',String(i+1)+' · '+s.planRef,q('select')).value=s.planRef;
      listed=true;const target=pending?.planRef||selected;
      if(summaries.some(s=>s.planRef===target)){
        selected=target;q('select').value=target;await open(target,generation);await reconcile(generation);
        if(!pending)say('Ricevuta privata aggiornata. Nessuna analisi avviata.');
      }else{
        selected='';q('select').value='';
        if(pending){stored();retryAllowed=pending.action==='CREATE';say(retryAllowed?
          'Piano non osservato nel registro corrente. La richiesta conservata può essere ripetuta solo manualmente.':
          'Piano della richiesta non disponibile: registrazioni bloccate.');}
        else say(summaries.length?'Seleziona una campagna per consultarne tutti i controlli.':'Nessuna campagna registrata.');
      }
      preview(pending||loaded);
    }
    function checkAction(value){
      if(value.action==='CREATE')return;
      check(view&&view.campaign.planRef===value.planRef);
      const r=value.request;
      if(r.planHeadSha256)check(r.planHeadSha256===view.campaign.headSha256);
      if(value.action==='FREEZE')check(r.expectedInputReviewSha256===view.campaign.inputReviewSnapshotSha256);
      if(value.action==='INPUT_REVIEW')check(view.plan.inputWitnessRefs.includes(value.witnessRef)
        &&r.algorithmSha256===view.plan.algorithmSha256&&r.contractSha256===view.plan.contractSha256);
      if(value.action==='OUTCOME_REVIEW')check(view.executions.some(e=>e.sha256===r.executionSha256));
      if(value.action==='FINALIZE')check(view.campaign.status==='READY_FOR_OWNER_FINAL_REVIEW');
    }
    async function send(){
      check(host.canAct()&&host.canMutate()&&pending&&!storageBlocked&&!queueBlocked);stored();retryAllowed=false;
      const value=pending;let path='/campaigns';
      const suffix={FREEZE:'freeze',OUTCOME_REVIEW:'review-outcome',FINALIZE:'finalize',REVOKE:'revoke'};
      if(value.action==='INPUT_REVIEW')path+='/inputs/'+value.witnessRef+'/review';
      else if(value.action!=='CREATE')path+='/'+value.planRef+'/'+suffix[value.action];
      const response=await host.request(path,'POST',value.request);check(response!==null);
      if(!current()||!authorized)return;
      await refresh();
    }
    function perform(fn){return host.run(async()=>{
      try{check(current()&&authorized&&host.canAct());await fn();}
      catch{if(current()){clearView();say(authorized?'Operazione non verificata. Aggiorna le campagne; ogni richiesta conservata resta da riconciliare.':'Accedi per consultare il collaudo.');}}
      finally{lock();host.changed();}
    });}
    q('refresh').addEventListener('click',()=>perform(refresh));
    q('select').addEventListener('change',()=>{selected=q('select').value;clearView();q('confirmed').checked=false;lock();});
    q('open').addEventListener('click',()=>perform(async()=>{await open(selected,epoch);say('Ricevuta privata verificata.');}));
    q('confirmed').addEventListener('change',lock);
    q('file').addEventListener('change',()=>{
      const version=++loadVersion,generation=epoch;loaded=null;q('confirmed').checked=false;preview(null);
      return perform(async()=>{
        check(!pending&&!storageBlocked&&!queueBlocked);const file=q('file').files?.[0];check(file&&file.size>0&&file.size<=LIMIT);
        const text=await file.text();validEpoch(generation);check(version===loadVersion&&new TextEncoder().encode(text).length<=LIMIT);
        loaded=api.action(JSON.parse(text));preview(loaded);say('Richiesta preparata. Esamina le impronte e conferma prima della registrazione.');
      });
    });
    q('send').addEventListener('click',()=>perform(async()=>{
      check(host.canAct()&&host.canMutate()&&listed&&loaded&&!pending&&!storageBlocked&&!queueBlocked&&q('confirmed').checked);checkAction(loaded);
      try{check(sessionStorage.getItem(KEY)===null);const text=JSON.stringify(loaded);check(text.length<=LIMIT);
        sessionStorage.setItem(KEY,text);check(sessionStorage.getItem(KEY)===text);}
      catch{storageBlocked=true;throw Error('Memoria della richiesta non disponibile.');}
      pending=loaded;loaded=null;host.changed();await send();
    }));
    q('retry').addEventListener('click',()=>perform(async()=>{check(retryAllowed&&q('confirmed').checked);await send();}));
    function reset(){epoch++;loadVersion++;clearView();loaded=null;listed=false;selected='';q('select').replaceChildren();
      q('file').value='';q('confirmed').checked=false;q('preview').replaceChildren();say('Accedi e aggiorna le campagne per consultare il collaudo.');}
    lock();
    return Object.freeze({hasPending(){
      try{if(pending)stored();else check(sessionStorage.getItem(KEY)===null);}catch{storageBlocked=true;}
      return Boolean(pending)||storageBlocked;
    },
      update(state){if(authorized&&!state.authorized)reset();authorized=state.authorized;busy=state.busy;queueBlocked=state.queueBlocked;lock();},
      reset,dispose(){reset();disposed=true;}});
  }
  globalThis.DSGCampaignOwner=Object.freeze({mount});
})();
