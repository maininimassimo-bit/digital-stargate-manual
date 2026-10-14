/* Local internal dossier history and explicit review requests, never submission. */
(() => {
  'use strict';
  const exact=(v,keys)=>v!==null&&typeof v==='object'&&!Array.isArray(v)&&Object.keys(v).length===keys.length&&keys.every(k=>Object.hasOwn(v,k));
  const hash=v=>typeof v==='string'&&/^[a-f0-9]{64}$/.test(v),ref=v=>typeof v==='string'&&/^[a-f0-9]{32}$/.test(v);
  const count=v=>Number.isSafeInteger(v)&&v>=0;
  const check=ok=>{if(!ok)throw Error('Revisione del dossier non compatibile.');};
  const labels=Object.freeze({KEEP_FOR_REVIEW:'Conserva per revisione',REJECT_CANDIDATE:'Respingi il candidato',FOLLOW_UP:'Richiedi approfondimento',REVOKE_REVIEW:'Revoca una revisione'});
  function utc(v){check(typeof v==='string'&&/^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d{1,6})?Z$/.test(v));return globalThis.DSGAstrometryContext.timestampSeconds(v);}
  function inspect(v){
    const contextual=v?.schema==='BKL051_CASE_DOSSIER_REVIEW_V2';
    check(exact(v,['schema','dossierRef','caseRef','planSha256','planHeadSha256','packageSha256','ledgerAnchorSha256','ledgerHeadSha256',
      'originDeclared','packageStatus','planStatus','attempts','evidenceFiles','evidenceGaps','comparisonPresent','decisions',
      'actorIdentityAttested','scientificAcceptance','submissionAuthorized','externalSubmission',...(contextual?['contextualRecoveryRelationship']:[])]));
    check((v.schema==='BKL051_CASE_DOSSIER_REVIEW_V1'||contextual)
      &&(!contextual||v.contextualRecoveryRelationship==='CONTEXT_ONLY_NOT_CASE_RECOVERY_OR_VALIDATION')&&ref(v.dossierRef)&&ref(v.caseRef)
      &&['planSha256','planHeadSha256','packageSha256','ledgerAnchorSha256','ledgerHeadSha256'].every(k=>hash(v[k]))
      &&['SYNTHETIC_TEST','NOT_ATTESTED'].includes(v.originDeclared)
      &&['RETAINED_PACKAGE_VERIFIED','RETAINED_PACKAGE_UNAVAILABLE_OR_CHANGED'].includes(v.packageStatus)
      &&['LIVE_PLAN_NOT_RECHECKED','LIVE_PLAN_MATCHES','HISTORICAL_PLAN_REVISION','LIVE_PLAN_UNAVAILABLE_OR_CHANGED'].includes(v.planStatus)
      &&count(v.attempts)&&v.attempts<=500&&count(v.evidenceFiles)&&v.evidenceFiles>0&&count(v.evidenceGaps)
      &&typeof v.comparisonPresent==='boolean'&&Array.isArray(v.decisions)&&v.decisions.length<=128
      &&v.actorIdentityAttested===false&&v.scientificAcceptance===false&&v.submissionAuthorized===false&&v.externalSubmission==='NONE');
    const seen=new Map(),revoked=new Set();let previous=null;
    for(const d of v.decisions){
      check(exact(d,['eventRef','action','actorRef','recordedUTC','targetEventRef','revoked'])&&ref(d.eventRef)&&!seen.has(d.eventRef)
        &&ref(d.actorRef)&&Object.hasOwn(labels,d.action)&&typeof d.revoked==='boolean');
      const time=utc(d.recordedUTC);check(previous===null||time>=previous);previous=time;
      if(d.action==='REVOKE_REVIEW'){
        const target=seen.get(d.targetEventRef);check(target&&target.action!=='REVOKE_REVIEW'&&!revoked.has(d.targetEventRef));revoked.add(d.targetEventRef);
      }else check(d.targetEventRef===null);
      seen.set(d.eventRef,d);
    }
    for(const d of v.decisions)check(d.revoked===revoked.has(d.eventRef));
    if(!v.decisions.length)check(v.ledgerHeadSha256===v.ledgerAnchorSha256);
    else check(v.ledgerHeadSha256!==v.ledgerAnchorSha256);
    return Object.freeze({decisions:seen.size,revoked:revoked.size,livePackage:v.packageStatus==='RETAINED_PACKAGE_VERIFIED',submissionAuthorized:false});
  }
  function request(v,decision){
    inspect(v);check(exact(decision,['eventRef','actorRef','recordedUTC','action','targetEventRef','note'])
      &&ref(decision.eventRef)&&!v.decisions.some(d=>d.eventRef===decision.eventRef)&&ref(decision.actorRef)
      &&Object.hasOwn(labels,decision.action)&&typeof decision.note==='string'&&decision.note.length>0&&decision.note.length<=2048
      &&decision.note===decision.note.trim()&&!/[\p{C}\u2028\u2029]/u.test(decision.note));
    const time=utc(decision.recordedUTC);if(v.decisions.length)check(time>=utc(v.decisions.at(-1).recordedUTC));
    if(decision.action==='REVOKE_REVIEW')check(v.decisions.some(d=>d.eventRef===decision.targetEventRef&&d.action!=='REVOKE_REVIEW'&&!d.revoked));
    else check(decision.targetEventRef===null&&v.packageStatus==='RETAINED_PACKAGE_VERIFIED');
    return {schema:'BKL051_DOSSIER_REVIEW_REQUEST_V1',packageSha256:v.packageSha256,ledgerAnchorSha256:v.ledgerAnchorSha256,
      expectedHeadSha256:v.ledgerHeadSha256,decision:{...decision}};
  }
  globalThis.DSGCaseDossier=Object.freeze({inspect,request});
  function init(){
    const root=document.querySelector('[data-dsg-case-dossier]');if(!root||root.dataset.initialized)return;root.dataset.initialized='true';
    const input=root.querySelector('[data-view]'),status=root.querySelector('[data-view-status]'),output=root.querySelector('[data-result]');
    const form=root.querySelector('[data-review-form]');let loaded=null,generation=0;
    const controls=form?Object.fromEntries(['actor','action','target','note','save','new-actor','request-status'].map(k=>[k,form.querySelector('[data-'+k+']')])):null;
    if(controls){
      controls.save.disabled=true;
      controls.action.addEventListener('change',()=>{controls.target.disabled=controls.action.value!=='REVOKE_REVIEW';});
      controls['new-actor'].addEventListener('click',()=>{try{controls.actor.value=crypto.randomUUID().replaceAll('-','');controls['request-status'].textContent='Identificativo locale creato: non autentica l’identità del revisore.';}catch(e){controls['request-status'].textContent='Identificativo non creato: nessuna richiesta registrata.';}});
      controls.save.addEventListener('click',()=>{
        try{
          check(loaded&&root.isConnected);
          const value=request(loaded,{eventRef:crypto.randomUUID().replaceAll('-',''),actorRef:controls.actor.value.trim().toLowerCase(),
            recordedUTC:new Date().toISOString(),action:controls.action.value,targetEventRef:controls.action.value==='REVOKE_REVIEW'?controls.target.value:null,note:controls.note.value.trim()});
          const url=URL.createObjectURL(new Blob([JSON.stringify(value,null,2)+'\n'],{type:'application/json'})),link=document.createElement('a');
          link.href=url;link.download='richiesta-revisione-dossier.json';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
          controls['request-status'].textContent='Richiesta salvata sul PC, da applicare al registro locale sulla stessa testa. Nessuna revisione già registrata e nessun invio esterno.';
        }catch(e){controls['request-status'].textContent='Richiesta non preparata: controlla identificativo, motivazione, azione e revisione da revocare. Nessun file registrato.';}
      });
    }
    input.addEventListener('change',async()=>{
      const current=++generation;loaded=null;output.replaceChildren();if(controls){controls.save.disabled=true;controls.target.replaceChildren();controls.action.value='KEEP_FOR_REVIEW';controls.target.disabled=true;controls.note.value='';controls['request-status'].textContent='Nessuna richiesta registrata.';}status.textContent='Verifica della ricevuta del dossier…';
      try{
        const file=input.files[0];check(file&&file.size<=1048576);const raw=await file.text();if(current!==generation||!root.isConnected)return;
        const v=JSON.parse(raw),s=inspect(v),summary=document.createElement('p'),state=document.createElement('p'),history=document.createElement('ol'),limits=document.createElement('p');
        summary.textContent=`${v.originDeclared==='SYNTHETIC_TEST'?'Origine sintetica dichiarata':'Origine dei dati non attestata'}. Dossier ${v.dossierRef.slice(0,8)}; tentativi: ${v.attempts}; file referenziati: ${v.evidenceFiles}; lacune: ${v.evidenceGaps}; confronto allegato: ${v.comparisonPresent?'sì':'no'}.`+(v.schema==='BKL051_CASE_DOSSIER_REVIEW_V2'?' Esperimento sintetico allegato come contesto: non dimostra recupero o validazione di questo caso e non aggiunge controlli qualificati.':'');
        state.textContent=(s.livePackage?'Il pacchetto conservato è stato ricontrollato sul PC.':'Pacchetto conservato indisponibile o modificato: nuove revisioni bloccate; resta possibile revocare una decisione precedente.')+' '+({LIVE_PLAN_MATCHES:'La cronologia del piano corrente corrisponde alla versione congelata.',LIVE_PLAN_NOT_RECHECKED:'Il piano corrente non è stato ricontrollato.',HISTORICAL_PLAN_REVISION:'Il piano è cambiato: questa revisione riguarda una versione storica.',LIVE_PLAN_UNAVAILABLE_OR_CHANGED:'Piano corrente indisponibile o modificato.'}[v.planStatus]);
        for(const d of v.decisions){const li=document.createElement('li');li.textContent=`${labels[d.action]}; data dichiarata ${d.recordedUTC}; revisore locale ${d.actorRef.slice(0,8)}; ${d.revoked?'decisione revocata':'decisione conservata'}.`;history.append(li);}
        limits.textContent='La revisione riguarda soltanto il dossier congelato e le sue impronte. Identità e data sono dichiarate, non autenticate. Non è accettazione scientifica o autorizzazione alla segnalazione; le lacune non sono colmate dalla decisione. Motivazioni complete e file scientifici restano nell’archivio privato. Il browser non rilegge i file originali.';
        const identities=document.createElement('details'),title=document.createElement('summary'),hashes=document.createElement('p');title.textContent='Impronte del contenuto e del registro';hashes.style.overflowWrap='anywhere';
        hashes.textContent=`Pacchetto: ${v.packageSha256}. Piano: ${v.planSha256}; testa congelata: ${v.planHeadSha256}. Ancora del registro: ${v.ledgerAnchorSha256}; testa: ${v.ledgerHeadSha256}.`;identities.append(title,hashes);
        output.append(summary,state,history,limits,identities);loaded=v;
        if(controls){for(const d of v.decisions.filter(d=>d.action!=='REVOKE_REVIEW'&&!d.revoked)){const option=document.createElement('option');option.value=d.eventRef;option.textContent=labels[d.action]+' — '+d.eventRef.slice(0,8);controls.target.append(option);}controls.target.disabled=controls.action.value!=='REVOKE_REVIEW';controls.save.disabled=false;}
        status.textContent='Ricevuta coerente. Revisione interna distinta da approvazione scientifica e invio.';
      }catch(e){if(current===generation){output.replaceChildren();status.textContent='Ricevuta non valida o incompatibile: nessun dossier mostrato.';}}
      finally{if(current===generation)input.value='';}
    });
  }
  if(typeof document!=='undefined'){if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();if(typeof document$!=='undefined')document$.subscribe(init);}
})();
