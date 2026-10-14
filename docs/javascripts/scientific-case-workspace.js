/* Coherent local case workspace; all nested validators remain mandatory. */
(() => {
 'use strict';
 const check=ok=>{if(!ok)throw Error('Scheda del caso non coerente.');};
 const exact=(v,keys)=>v!==null&&typeof v==='object'&&!Array.isArray(v)&&Object.keys(v).length===keys.length&&keys.every(k=>Object.hasOwn(v,k));
 function inspect(v){
  check(exact(v,['schema','caseRef','plan','triplet','dossier','comparison','contextualRecovery','scope','scientificAcceptance','submissionAuthorized','qualifiedControls'])
   &&v.schema==='BKL051_CASE_WORKSPACE_V1'&&v.scope==='LOCAL_VERIFIED_EXPORT_IMPORTED_RECEIPT_NOT_REMOTE_BYTE_ATTESTATION'
   &&v.scientificAcceptance===false&&v.submissionAuthorized===false&&v.qualifiedControls===0);
  globalThis.DSGTestPlanReview.inspect(v.plan);
  const technical=globalThis.DSGTestPlanReview.inspectTriplet(v.triplet,v.plan);
  globalThis.DSGCaseDossier.inspect(v.dossier);
  check(v.caseRef===v.triplet.caseRef&&v.caseRef===v.dossier.caseRef&&v.dossier.planSha256===v.plan.planSha256
   &&v.dossier.planHeadSha256===v.plan.headSha256&&v.dossier.packageStatus==='RETAINED_PACKAGE_VERIFIED'
   &&v.dossier.planStatus==='LIVE_PLAN_MATCHES'&&v.dossier.attempts===technical.attempts
   &&v.dossier.comparisonPresent===(v.comparison!==null));
  if(v.comparison!==null){globalThis.DSGMultiEpoch.inspect(v.comparison,v.plan);check(v.comparison.caseRef===v.caseRef);}
  check((v.dossier.schema==='BKL051_CASE_DOSSIER_REVIEW_V2')===(v.contextualRecovery!==null));
  let context=null;if(v.contextualRecovery!==null)context=globalThis.DSGControlledRecovery.inspect(v.contextualRecovery);
  return Object.freeze({attempts:technical.attempts,technicalComplete:technical.complete,context,qualified:0});
 }
 globalThis.DSGCaseWorkspace=Object.freeze({inspect});
 function init(){
  const root=document.querySelector('[data-dsg-case-workspace]');if(!root||root.dataset.initialized)return;root.dataset.initialized='true';
  const input=root.querySelector('input'),status=root.querySelector('[role="status"]'),out=root.querySelector('[data-result]');let generation=0;
  input.addEventListener('change',async()=>{
   const token=++generation;out.replaceChildren();status.textContent='Verifica dei collegamenti del caso…';
   try{
    const file=input.files[0];check(file&&file.size<=1048576);const raw=await file.text();if(token!==generation||!root.isConnected)return;
    const v=JSON.parse(raw),s=inspect(v),summary=document.createElement('p'),steps=document.createElement('ol'),limits=document.createElement('p');
    summary.textContent=`Caso ${v.caseRef.slice(0,8)}: piano, tentativi e dossier riferiti alla stessa versione. Tentativi conservati: ${s.attempts}. Copertura tecnica: ${s.technicalComplete?'completa':'incompleta'}.`;
    for(const text of ['Piano preliminare congelato: qualificazione scientifica ancora aperta.',
     `Evidenze del dossier: ${v.dossier.evidenceFiles} file; lacune dichiarate: ${v.dossier.evidenceGaps}.`,
     `Confronto multi-epoca allegato: ${v.comparison===null?'no':'sì, preliminare'}.`,
     `Eventi di revisione interna: ${v.dossier.decisions.length}; non sono accettazioni scientifiche o permessi di invio.`]){
     const li=document.createElement('li');li.textContent=text;steps.append(li);
    }
    if(s.context){const li=document.createElement('li');li.textContent=`Esperimento sintetico DI CONTESTO: ${s.context.recovered}/${s.context.injections} recuperi diagnostici. Non dimostra recupero o validazione di questo caso.`;steps.append(li);}
    limits.textContent='Controlli nulli qualificati: 0. Il file importato riporta una verifica locale delle evidenze: questa pagina non rilegge gli originali né autentica l’Owner. Nessun avvio, modifica, caricamento o invio. Validazione scientifica e accettazione finale restano aperte.';
    out.append(summary,steps,limits);status.textContent='Scheda coerente. Le verifiche scientifiche restano aperte.';
   }catch(e){if(token===generation&&root.isConnected){out.replaceChildren();status.textContent='Scheda non valida o con versioni incoerenti: nessun risultato mostrato.';}}
   finally{if(token===generation)input.value='';}
  });
 }
 if(typeof document!=='undefined'){if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();if(typeof document$!=='undefined')document$.subscribe(init);}
})();
