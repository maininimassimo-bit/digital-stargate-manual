/* Local minimised provenance inspection; no file attestation, network or execution. */
(() => {
  'use strict';
  const exact=(v,keys)=>v!==null&&typeof v==='object'&&!Array.isArray(v)&&Object.keys(v).length===keys.length&&keys.every(k=>Object.hasOwn(v,k));
  const hash=v=>typeof v==='string'&&/^[a-f0-9]{64}$/.test(v);
  const ref=v=>typeof v==='string'&&/^[a-f0-9]{32}$/.test(v);
  const check=ok=>{if(!ok)throw new Error('Provenienza non compatibile.');};
  function inspect(v){
    check(exact(v,['schema','scope','receiptSha256','manifestSha256','terminalSha256','candidateDraftSha256','candidatePlanRef','inputs','calibrationSemantics','scienceValidation','completeUncertainty','significance','qualifiedControls','executionAuthorized']));
    check(v.schema==='BKL051_INPUT_LINEAGE_V1'&&v.scope==='RETAINED_METADATA_COPY_PILOT_ONLY'
      &&['receiptSha256','manifestSha256','terminalSha256','candidateDraftSha256'].every(k=>hash(v[k]))&&ref(v.candidatePlanRef)
      &&v.calibrationSemantics==='NOT_ATTESTED_BY_THIS_IMPORT'&&v.scienceValidation==='NOT_VALIDATED'
      &&v.completeUncertainty===null&&v.significance===null&&v.qualifiedControls===0&&v.executionAuthorized===false
      &&Array.isArray(v.inputs)&&v.inputs.length>0&&v.inputs.length<=64);
    const ids=new Set(),raws=new Set(),outputs=new Set();let included=0;
    for(const row of v.inputs){
      check(exact(row,['inputRef','filter','rawSha256','calibratedSha256','derivedSha256','byteIntegrity','metadataCopy','pixelEquality','sampleMembership']));
      check(ref(row.inputRef)&&!ids.has(row.inputRef)&&['L-Pro','Red','Green','Blu'].includes(row.filter)
        &&['rawSha256','calibratedSha256','derivedSha256'].every(k=>hash(row[k]))
        &&new Set([row.rawSha256,row.calibratedSha256,row.derivedSha256]).size===3
        &&!raws.has(row.rawSha256)&&!outputs.has(row.derivedSha256)
        &&row.byteIntegrity==='RECHECKED_LOCAL_FILES'&&row.metadataCopy==='NATIVE_RECEIPT_REPORTED'
        &&row.pixelEquality==='REPORTED_ZERO_DIFFERENCE_NOT_REMEASURED'
        &&['IN_CANDIDATE_MANIFEST','OUTSIDE_CANDIDATE_MANIFEST'].includes(row.sampleMembership));
      ids.add(row.inputRef);raws.add(row.rawSha256);outputs.add(row.derivedSha256);
      if(row.sampleMembership==='IN_CANDIDATE_MANIFEST')included++;
    }
    return Object.freeze({inputs:ids.size,included,outside:ids.size-included,qualified:0,significance:null});
  }
  globalThis.DSGInputLineage=Object.freeze({inspect});
  function init(){
    const root=document.querySelector('[data-dsg-input-lineage]');if(!root||root.dataset.initialized)return;root.dataset.initialized='true';
    const input=root.querySelector('input'),status=root.querySelector('[role="status"]'),output=root.querySelector('[data-result]');let generation=0;
    input.addEventListener('change',async()=>{
      const current=++generation;output.replaceChildren();status.textContent='Verifica della ricevuta di provenienza…';
      try{
        const file=input.files[0];check(file&&file.size<=1048576);const raw=await file.text();
        if(current!==generation||!root.isConnected)return;
        const v=JSON.parse(raw),s=inspect(v),summary=document.createElement('p'),identity=document.createElement('p'),list=document.createElement('ul');
        summary.textContent=`Copie sperimentali: ${s.inputs}. Originali presenti nel manifest candidato dichiarato: ${s.included}. Fuori dal manifest: ${s.outside}. Controlli qualificati: 0. Incertezza completa e significatività: non disponibili.`;
        identity.textContent=`Impronta del manifest candidato di riferimento: ${v.candidateDraftSha256}. Questa ricevuta non è un collegamento automatico a una versione del piano.`;
        for(const row of v.inputs){
          const item=document.createElement('li');item.textContent=`${row.filter}: tre identità distinte; ${row.sampleMembership==='IN_CANDIDATE_MANIFEST'?'originale presente nel manifest candidato dichiarato':'originale fuori dal manifest candidato dichiarato'}. `;
          const details=document.createElement('details'),title=document.createElement('summary'),p=document.createElement('p');title.textContent='Impronte di originale, calibrata e derivata';
          p.textContent=`Originale: ${row.rawSha256}. Calibrata sperimentale: ${row.calibratedSha256}. Derivata con metadati copiati: ${row.derivedSha256}.`;p.style.overflowWrap='anywhere';
          details.append(title,p);item.append(details);list.append(item);
        }
        output.append(summary,identity,list);status.textContent='Struttura compatibile. Byte ricontrollati sul PC secondo la ricevuta; il browser non li verifica. Uguaglianza dei pixel riportata dalla prova nativa precedente, non rimisurata qui. Calibrazione e provenienza scientifica completa restano da validare.';
      }catch(e){if(current===generation){output.replaceChildren();status.textContent='Ricevuta di provenienza non valida o incompatibile: nessun risultato mostrato.';}}
      finally{if(current===generation)input.value='';}
    });
  }
  if(typeof document!=='undefined'){if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();if(typeof document$!=='undefined')document$.subscribe(init);}
})();
