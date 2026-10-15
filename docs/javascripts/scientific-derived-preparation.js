/* Compare local preparation declarations. No bytes attestation or execution authority. */
(() => {
  'use strict';
  const exact=(v,keys)=>v!==null&&typeof v==='object'&&!Array.isArray(v)
    &&Object.keys(v).length===keys.length&&keys.every(k=>Object.hasOwn(v,k));
  const ref=v=>typeof v==='string'&&/^[a-f0-9]{32}$/.test(v);
  const hash=v=>typeof v==='string'&&/^[a-f0-9]{64}$/.test(v);
  const check=ok=>{if(!ok)throw new Error('Preparazione non compatibile.');};
  const matches=Object.freeze({originalInSelectedCase:'Originale nel caso selezionato',
    sameCandidatePlan:'Stessa famiglia del piano',originalInCandidateManifest:'Originale nel manifest candidato',
    derivedMatchesPreparedInput:'Copia associata all’input preparato',algorithmMatchesFrozenPlan:'Algoritmo della versione',
    rulesMatchFrozenPlan:'Regole della versione',currentSignedReadImplementation:'Implementazione corrente del kernel',
    signedReadNativeRegressionPinned:'Regressione nativa conservata'});
  const blockers=Object.freeze(['DERIVED_ATTEMPT_ARCHIVE_LINK_REQUIRED','CALIBRATION_SCIENTIFIC_VALIDATION_MISSING',
    'FULL_UNCERTAINTY_MISSING','CONFIRMATORY_ATTESTATIONS_MISSING']);
  const explanations=['Archivio del nuovo tentativo mancante','Calibrazione scientifica non validata',
    'Incertezza completa mancante','Attestazioni confermative mancanti'];
  function inspect(v,plan,lineage){
    check(globalThis.DSGTestPlanReview&&globalThis.DSGInputLineage);
    DSGTestPlanReview.inspect(plan);DSGInputLineage.inspect(lineage);
    check(exact(v,['schema','scope','status','planRef','versionRef','planSha256','headSha256','caseRef',
      'preflights','selectedJobs','nativeStarts','attempts','executionAuthorized','scienceValidation',
      'qualifiedControls','completeUncertainty','significance']));
    check(v.schema==='BKL051_DERIVED_PREPARATION_V1'&&v.scope==='LOCAL_PREPARATION_ONLY_NO_EXECUTION_PERMISSION'
      &&v.status==='PREPARED_NOT_EXECUTED'&&ref(v.caseRef)&&v.planRef===plan.planRef&&v.versionRef===plan.versionRef
      &&v.planSha256===plan.planSha256&&v.headSha256===plan.headSha256&&lineage.candidatePlanRef===plan.planRef
      &&v.selectedJobs===0&&v.nativeStarts===0&&v.attempts===0&&v.executionAuthorized===false
      &&v.scienceValidation==='NOT_VALIDATED'&&v.qualifiedControls===0&&v.completeUncertainty===null&&v.significance===null
      &&Array.isArray(v.preflights)&&v.preflights.length===3);
    const selected=plan.cases.find(c=>c.caseRef===v.caseRef);
    check(selected&&selected.attempts.length===0);
    const frames=new Set(),raws=new Set(),deriveds=new Set();let signed;
    for(const p of v.preflights){
      check(exact(p,['schema','status','planSha256','headSha256','caseRef','frameRef','rawSha256','derivedSha256',
        'sourceReceiptSha256','candidateDraftSha256','signedReadEvidenceSha256','matches','blockers','scope',
        'executionAuthorized','scienceValidation','qualifiedControls','completeUncertainty','significance']));
      check(p.schema==='BKL051_DERIVED_INPUT_PREFLIGHT_V1'&&p.status==='BLOCKED'
        &&p.planSha256===v.planSha256&&p.headSha256===v.headSha256&&p.caseRef===v.caseRef
        &&p.sourceReceiptSha256===lineage.receiptSha256&&p.candidateDraftSha256===lineage.candidateDraftSha256
        &&ref(p.frameRef)&&hash(p.rawSha256)&&hash(p.derivedSha256)&&hash(p.signedReadEvidenceSha256)
        &&p.rawSha256!==p.derivedSha256&&!frames.has(p.frameRef)&&!raws.has(p.rawSha256)&&!deriveds.has(p.derivedSha256)
        &&p.scope==='LOCAL_ASSOCIATIONS_ONLY_NO_EXECUTION_PERMISSION'&&p.executionAuthorized===false
        &&p.scienceValidation==='NOT_VALIDATED'&&p.qualifiedControls===0&&p.completeUncertainty===null&&p.significance===null
        &&exact(p.matches,Object.keys(matches))&&Object.values(p.matches).every(x=>x===true)
        &&Array.isArray(p.blockers)&&p.blockers.length===blockers.length&&p.blockers.every((x,i)=>x===blockers[i]));
      check(lineage.inputs.some(r=>r.rawSha256===p.rawSha256&&r.derivedSha256===p.derivedSha256
        &&r.sampleMembership==='IN_CANDIDATE_MANIFEST'));
      if(signed===undefined)signed=p.signedReadEvidenceSha256;else check(signed===p.signedReadEvidenceSha256);
      frames.add(p.frameRef);raws.add(p.rawSha256);deriveds.add(p.derivedSha256);
    }
    return Object.freeze({prepared:3,selectedJobs:0,nativeStarts:0,attempts:0,qualified:0});
  }
  globalThis.DSGDerivedPreparation=Object.freeze({inspect});
  const mounted=new WeakMap();let activeRoot;
  function init(){
    const root=document.querySelector('[data-dsg-derived-preparation]');
    if(activeRoot&&activeRoot.root!==root){activeRoot.clear();activeRoot=undefined;}
    if(!root)return;
    if(mounted.has(root)){activeRoot=mounted.get(root);return;}
    if(root.dataset.initialized)return;
    root.dataset.initialized='true';
    const inputs=['plan','lineage','preparation'].map(k=>root.querySelector(`[data-${k}]`));
    const status=root.querySelector('[role="status"]'),output=root.querySelector('[data-result]');let generation=0;
    activeRoot={root,clear(){generation++;output.replaceChildren();for(const input of inputs)input.value='';status.textContent='Nessuna preparazione caricata.';}};
    mounted.set(root,activeRoot);
    const el=(tag,text,parent)=>{const node=document.createElement(tag);node.textContent=text;parent.append(node);return node;};
    async function changed(){
      const current=++generation;output.replaceChildren();
      status.textContent='Scegli versione del piano, provenienza e preparazione riferite agli stessi input.';
      const files=inputs.map(input=>input.files[0]);if(files.some(f=>!f))return;
      status.textContent='Confronto delle tre ricevute locali…';
      const active=()=>current===generation&&root.isConnected&&document.querySelector('[data-dsg-derived-preparation]')===root;
      try{
        check(files.every(f=>Number.isSafeInteger(f.size)&&f.size>0&&f.size<=1048576));
        const texts=await Promise.all(files.map(f=>f.text()));if(!active())return;
        check(texts.every(t=>typeof t==='string'&&new TextEncoder().encode(t).length<=1048576));
        const [plan,lineage,value]=texts.map(t=>JSON.parse(t)),s=inspect(value,plan,lineage);
        el('p',`Secondo la ricevuta locale, copie preparate per questo caso: ${s.prepared}. Job selezionati: 0. Avvii nativi e tentativi: 0. Controlli qualificati: 0.`,output);
        el('p','Il browser confronta dichiarazioni e identificativi: non rilegge i file privati e non attesta calibrazione, sorgenti fisiche, identità o tempi. Incertezza completa e significatività restano sconosciute. Nessun avvio è autorizzato.',output);
        const list=el('ul','',output);for(const text of explanations)el('li',text,list);
        for(const [i,p] of value.preflights.entries()){
          const card=el('article','',output);el('h3',`Copia preparata ${i+1}: otto corrispondenze dichiarate`,card);
          const details=el('details','',card);el('summary','Identificativi e controlli dichiarati',details);
          el('p',`Immagine del piano: ${p.frameRef}. Originale: ${p.rawSha256}. Copia preparata: ${p.derivedSha256}.`,details);
          const checks=el('ul','',details);for(const text of Object.values(matches))el('li',text,checks);
        }
        status.textContent='Ricevute compatibili per versione, caso e provenienza dichiarati. Preparazione locale; quattro blocchi restano presenti. Nessuna esecuzione o validazione scientifica.';
      }catch(e){if(active()){output.replaceChildren();status.textContent='Ricevute mancanti, non valide o incompatibili: nessuna preparazione mostrata.';}}
    }
    for(const input of inputs)input.addEventListener('change',changed);
  }
  if(typeof document!=='undefined'){
    if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
    if(typeof document$!=='undefined')document$.subscribe(init);
    if(typeof window!=='undefined')window.addEventListener('pagehide',()=>{if(activeRoot)activeRoot.clear();});
  }
})();
