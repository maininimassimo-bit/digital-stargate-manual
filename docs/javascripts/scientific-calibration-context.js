/* Passive pair of local receipts. No upload, persistence or pixel attestation. */
(() => {
  'use strict';
  const exact=(v,keys)=>v!==null&&typeof v==='object'&&!Array.isArray(v)&&Object.keys(v).length===keys.length&&keys.every(k=>Object.hasOwn(v,k));
  const hash=v=>typeof v==='string'&&/^[a-f0-9]{64}$/.test(v);
  const positive=v=>typeof v==='number'&&Number.isFinite(v)&&v>0;
  const check=ok=>{if(!ok)throw Error('Contesto di calibrazione non compatibile.');};
  const components=Object.freeze({LIGHT_PHOTON_READ_DIGITIZATION:['Luce: fotoni, lettura e digitalizzazione','PARTIAL'],
    DARK_FINITE_SAMPLE:['Master dark: campione finito','UNKNOWN'],DARK_TEMPORAL_2024_2026:['Stabilità dark 2024 su LIGHT 2026','UNKNOWN'],
    FLAT_REPEATABILITY:['Ripetibilità flat','CONDITIONAL'],FLAT_SHARED_SPATIAL:['Dark-flat condiviso e covarianza spaziale','PARTIAL'],
    NORMALIZATION_COVARIANCE:['Normalizzazione e covarianza del flat','UNKNOWN'],CROSS_PIXEL_EPOCH_COVARIANCE:['Covarianza fra pixel ed esposizioni','UNKNOWN'],
    FLUX_BACKGROUND_PSF_WCS:['Stimatore del flusso, fondo, PSF e WCS','UNKNOWN']});
  function inspect(v,lineage){
    globalThis.DSGInputLineage.inspect(lineage);
    check(exact(v,['schema','scienceValidation','lineageReceiptSha256','candidateDraftSha256','candidatePlanRef','budgetSha256',
      'cameraChoiceSha256','mapsReceiptSha256','camera','components','maps','inputs','darkTemporalLimitation','byteIntegrity',
      'completeUncertainty','significance','qualifiedControls','executionAuthorized']));
    check(v.schema==='BKL051_CALIBRATION_CONTEXT_V1'&&v.scienceValidation==='NOT_VALIDATED'
      &&['lineageReceiptSha256','candidateDraftSha256','budgetSha256','cameraChoiceSha256','mapsReceiptSha256'].every(k=>hash(v[k]))
      &&v.lineageReceiptSha256===lineage.receiptSha256&&v.candidateDraftSha256===lineage.candidateDraftSha256
      &&v.candidatePlanRef===lineage.candidatePlanRef&&v.byteIntegrity==='RECHECKED_LOCAL_FILES'
      &&v.completeUncertainty===null&&v.significance===null&&v.qualifiedControls===0&&v.executionAuthorized===false
      &&v.darkTemporalLimitation==='2024_DARK_FOR_2026_LIGHT_STABILITY_UNKNOWN');
    const c=v.camera;
    check(exact(c,['sourceCells','gainElectronsPerADU','readNoiseElectrons','parameterStandardUncertainties','readNoiseADUConditional','ADUConvention'])
      &&c.sourceCells==='M5:N5'&&['gainElectronsPerADU','readNoiseElectrons','readNoiseADUConditional'].every(k=>positive(c[k]))
      &&c.parameterStandardUncertainties===null&&c.ADUConvention==='65535_LEVELS_CONDITIONAL_NOT_ATTESTED'
      &&Math.abs(c.readNoiseADUConditional-c.readNoiseElectrons/c.gainElectronsPerADU)<=1e-12*c.readNoiseADUConditional);
    check(Array.isArray(v.components)&&v.components.length===8);
    const terms=new Set();for(const r of v.components){check(exact(r,['component','status'])&&Object.hasOwn(components,r.component)
      &&!terms.has(r.component)&&r.status===components[r.component][1]);terms.add(r.component);}
    check(Array.isArray(v.maps)&&v.maps.length>0&&v.maps.length<=4);
    const filters=new Set();for(const m of v.maps){
      check(exact(m,['filter','mapSha256','varianceMinimum','varianceMaximum','varianceMean','pixels','unit','scope','pixelCheck'])
        &&['L-Pro','Red','Green','Blu'].includes(m.filter)&&!filters.has(m.filter)&&hash(m.mapSha256)
        &&['varianceMinimum','varianceMaximum','varianceMean'].every(k=>positive(m[k]))
        &&m.varianceMinimum<=m.varianceMean&&m.varianceMean<=m.varianceMaximum
        &&Number.isSafeInteger(m.pixels)&&m.pixels>0&&m.unit==='NATIVE_NORMALIZED_SQUARED'
        &&m.scope==='NOMINAL_READ_COMPONENT_ONLY'&&m.pixelCheck==='RETAINED_NATIVE_SAVE_REOPEN_REPORT_NOT_REMEASURED');filters.add(m.filter);
    }
    check(Array.isArray(v.inputs)&&v.inputs.length===lineage.inputs.length);
    const ids=new Set();for(const r of v.inputs){
      check(exact(r,['inputRef','rawSha256','derivedSha256','filter','mapSha256','association']));
      const original=lineage.inputs.find(x=>x.inputRef===r.inputRef),map=v.maps.find(x=>x.filter===r.filter);
      check(original&&map&&!ids.has(r.inputRef)&&['rawSha256','derivedSha256','filter'].every(k=>r[k]===original[k])
        &&r.mapSha256===map.mapSha256&&r.association==='FILTER_ONLY_APPLICATION_NOT_ATTESTED');ids.add(r.inputRef);
    }
    return Object.freeze({inputs:ids.size,maps:v.maps.length,qualified:0,completeUncertainty:null,significance:null});
  }
  globalThis.DSGCalibrationContext=Object.freeze({inspect});
  function init(){
    const root=document.querySelector('[data-dsg-calibration-context]');if(!root||root.dataset.initialized)return;root.dataset.initialized='true';
    const inputs=[root.querySelector('[data-lineage]'),root.querySelector('[data-calibration]')],
      status=root.querySelector('[role="status"]'),output=root.querySelector('[data-result]');let generation=0;
    async function load(){
      const current=++generation;output.replaceChildren();status.textContent='Apri entrambe le ricevute per confrontarle.';
      if(!inputs.every(i=>i.files[0]))return;
      try{
        const files=inputs.map(i=>i.files[0]);check(files.every(f=>f.size<=1048576));
        const raw=await Promise.all(files.map(f=>f.text()));if(current!==generation||!root.isConnected)return;
        const [lineage,v]=raw.map(JSON.parse),s=inspect(v,lineage),summary=document.createElement('p'),camera=document.createElement('p'),list=document.createElement('ul');
        summary.textContent=`Input associati per filtro: ${s.inputs}. Mappe del solo rumore nominale di lettura: ${s.maps}. Incertezza completa e significatività: non disponibili. Controlli qualificati: 0.`;
        camera.textContent=`Camera, celle M5:N5: conversione ${v.camera.gainElectronsPerADU} e⁻/ADU; rumore di lettura ${v.camera.readNoiseElectrons} e⁻, pari a ${v.camera.readNoiseADUConditional} ADU solo nella convenzione dichiarata. Incertezze dei parametri sconosciute.`;
        for(const r of v.components){const item=document.createElement('li');item.textContent=`${components[r.component][0]}: ${{PARTIAL:'componente parziale',CONDITIONAL:'stima condizionale',UNKNOWN:'non quantificato'}[r.status]}.`;list.append(item);}
        const maps=document.createElement('ul');for(const m of v.maps){const item=document.createElement('li');
          item.textContent=`${m.filter}: varianza del solo contributo di lettura, media ${m.varianceMean}, intervallo ${m.varianceMinimum}–${m.varianceMaximum}, unità normalizzate native al quadrato; ${m.pixels} pixel. Non è la varianza di un flusso o di una differenza.`;maps.append(item);}
        const limits=document.createElement('p');limits.textContent='Dark 2024 su LIGHT 2026: stabilità temporale sconosciuta. La corrispondenza del filtro non attesta l’applicazione della mappa a questa immagine. Il controllo dei byte è riferito alla ricevuta del PC; i pixel non sono riletti dal browser. Covarianze mancanti non sono poste a zero.';
        output.append(summary,camera,list,maps,limits);status.textContent='Ricevute coerenti fra loro; calibrazione scientifica ancora da validare.';
      }catch(e){if(current===generation){output.replaceChildren();status.textContent='Ricevute non valide o non corrispondenti: nessun risultato mostrato.';}}
    }
    for(const input of inputs)input.addEventListener('change',load);
  }
  if(typeof document!=='undefined'){if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();if(typeof document$!=='undefined')document$.subscribe(init);}
})();
