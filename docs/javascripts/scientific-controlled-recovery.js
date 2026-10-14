/* Exploratory recovery counters, never an independent false-positive test. */
(() => {
  'use strict';
  const exact=(v,keys)=>v!==null&&typeof v==='object'&&!Array.isArray(v)&&Object.keys(v).length===keys.length&&keys.every(k=>Object.hasOwn(v,k));
  const hash=v=>typeof v==='string'&&/^[a-f0-9]{64}$/.test(v),ref=v=>typeof v==='string'&&/^[a-f0-9]{32}$/.test(v);
  const count=v=>Number.isSafeInteger(v)&&v>=0,finite=v=>typeof v==='number'&&Number.isFinite(v);
  const check=ok=>{if(!ok)throw Error('Risultato di recupero non compatibile.');};
  function inspect(v){
    check(exact(v,['schema','origin','prelaunchSha256','protocolSha256','sourceSha256','archiveSealSha256','terminalSha256','images',
      'matchingRadiusPixels','gaussianSigmaPixels','sourceShotNoiseAdded','truthSeparation','positionsPassedToDetector','scientificValidation',
      'scientificAcceptance','archiveSealTiming','badPixelQuality','parameterPolicyAccepted','submissionAuthorized','completeDependencyArchive',
      'rows','injectionDenominator','recoveredInjections','evaluatedInjections','ambiguousInjections','missingInjections','baselineProbeDenominator',
      'baselineProbesWithSources','independentTrialCount','qualifiedNullControls','falsePositiveConfidenceBound','measuredFluxBias','measuredFluxErrorRMS','status']));
    check(v.schema==='BKL051_CONTROLLED_RECOVERY_RESULT_V1'&&v.origin==='SYNTHETIC_ADDITION_ON_REAL_M27_BACKGROUND'
      &&['prelaunchSha256','protocolSha256','sourceSha256','archiveSealSha256'].every(k=>hash(v[k]))
      &&exact(v.terminalSha256,['generator','worker'])&&Object.values(v.terminalSha256).every(hash)
      &&v.sourceShotNoiseAdded===false&&v.positionsPassedToDetector===false
      &&v.truthSeparation==='STRUCTURAL_WORKER_PAYLOAD_CHECK_ONLY_NOT_INDEPENDENT_BLIND_ATTESTATION'
      &&v.archiveSealTiming==='POST_RUN_AFTER_INITIAL_SCORE_NOT_PRETRUTH_PROOF'
      &&v.badPixelQuality==='ALL_PIXELS_ADMITTED_NOT_SCIENTIFIC_BAD_PIXEL_VALIDATION'
      &&v.scientificValidation==='NOT_VALIDATED'&&v.scientificAcceptance===false&&v.parameterPolicyAccepted===false
      &&v.submissionAuthorized===false&&v.completeDependencyArchive===false
      &&[v.independentTrialCount,v.falsePositiveConfidenceBound,v.measuredFluxBias,v.measuredFluxErrorRMS].every(x=>x===null)
      &&v.qualifiedNullControls===0&&finite(v.matchingRadiusPixels)&&v.matchingRadiusPixels>0
      &&finite(v.gaussianSigmaPixels)&&v.gaussianSigmaPixels>0);
    check(Array.isArray(v.images)&&v.images.length===2&&new Set(v.images.map(i=>i.imageRef)).size===2);
    for(const i of v.images)check(exact(i,['imageRef','imageSha256','catalogSha256','sources'])&&ref(i.imageRef)&&hash(i.imageSha256)&&hash(i.catalogSha256)&&count(i.sources));
    check(Array.isArray(v.rows)&&v.rows.length>0&&v.rows.length<=10000);const ids=new Set();let recovered=0,evaluated=0,ambiguous=0,missing=0,flagged=0;
    const afterUses=new Map();
    for(const r of v.rows){
      check(r!==null&&typeof r==='object'&&Array.isArray(r.afterMatches));
      for(const index of r.afterMatches)afterUses.set(index,(afterUses.get(index)||0)+1);
    }
    for(const r of v.rows){
      check(exact(r,['targetRef','groupRef','truthAddedFlux','injectionStatus','recovered','baselineMatches','afterMatches','baselineProbeFlag','measuredAddedFlux','fullFluxVariance','significance'])
        &&ref(r.targetRef)&&!ids.has(r.targetRef)&&r.groupRef===v.sourceSha256.slice(0,32)&&finite(r.truthAddedFlux)&&r.truthAddedFlux>0
        &&[r.measuredAddedFlux,r.fullFluxVariance,r.significance].every(x=>x===null));ids.add(r.targetRef);
      for(const matches of [r.baselineMatches,r.afterMatches])check(Array.isArray(matches)&&matches.every(count)&&new Set(matches).size===matches.length);
      if(r.injectionStatus==='MISSING'){check(r.recovered===null&&r.baselineProbeFlag===null&&r.baselineMatches.length===0&&r.afterMatches.length===0);missing++;}
      else{
        const isAmbiguous=r.baselineMatches.length>0||r.afterMatches.length>1||r.afterMatches.some(index=>afterUses.get(index)>1);
        check(r.injectionStatus===(isAmbiguous?'AMBIGUOUS':'EVALUATED')&&r.recovered===(isAmbiguous?null:r.afterMatches.length===1)
          &&r.baselineProbeFlag===(r.baselineMatches.length>0));
        if(isAmbiguous)ambiguous++;else evaluated++;if(r.recovered===true)recovered++;if(r.baselineProbeFlag)flagged++;
      }
    }
    check(v.injectionDenominator===ids.size&&v.baselineProbeDenominator===ids.size&&v.recoveredInjections===recovered
      &&v.evaluatedInjections===evaluated&&v.ambiguousInjections===ambiguous&&v.missingInjections===missing&&v.baselineProbesWithSources===flagged
      &&v.status===(missing===ids.size?'REFERENCE_DETECTOR_UNAVAILABLE_OR_ZERO_REQUIRES_REVIEW':'DIAGNOSTIC_POSITION_SCORING_ONLY'));
    return Object.freeze({injections:ids.size,recovered,ambiguous,missing,qualified:0,independentTrials:null});
  }
  globalThis.DSGControlledRecovery=Object.freeze({inspect});
  function init(){
    const root=document.querySelector('[data-dsg-controlled-recovery]');if(!root||root.dataset.initialized)return;root.dataset.initialized='true';
    const input=root.querySelector('input'),status=root.querySelector('[role="status"]'),output=root.querySelector('[data-result]');let generation=0;
    input.addEventListener('change',async()=>{
      const current=++generation;output.replaceChildren();status.textContent='Verifica del risultato esplorativo…';
      try{
        const file=input.files[0];check(file&&file.size<=1048576);const raw=await file.text();if(current!==generation||!root.isConnected)return;
        const v=JSON.parse(raw),s=inspect(v),summary=document.createElement('p'),details=document.createElement('p'),list=document.createElement('ol'),limits=document.createElement('p');
        summary.textContent=`Inserzioni sintetiche su fondo M27 reale: ${s.injections}; recuperi diagnostici: ${s.recovered}; ambigui: ${s.ambiguous}; mancanti: ${s.missing}. Tutte le inserzioni restano nel denominatore.`;
        details.textContent=`Sigma della gaussiana sintetica: ${v.gaussianSigmaPixels} pixel; raggio di associazione congelato: ${v.matchingRadiusPixels} pixel. Sorgenti del rilevatore nelle due copie: ${v.images.map(i=>i.sources).join(' e ')}; non sono conteggi di falsi positivi. Sonde di posizione sul fondo con sorgenti: ${v.baselineProbesWithSources}/${v.baselineProbeDenominator}, non controlli nulli qualificati.`;
        for(const r of v.rows){const li=document.createElement('li');li.textContent=`${r.targetRef.slice(0,8)}: flusso aggiunto noto ${r.truthAddedFlux} in somma di campioni normalizzati; ${r.injectionStatus==='MISSING'?'valutazione mancante':r.injectionStatus==='AMBIGUOUS'?'associazione ambigua':r.recovered?'recupero diagnostico':'non recuperata nel profilo congelato'}. Flusso aggiunto misurato e varianza completa: non disponibili.`;list.append(li);}
        limits.textContent='Un solo fondo condiviso, nessun numero di prove indipendenti attestato. La PSF è sintetica e non è stato aggiunto rumore Poisson della sorgente. Qualità bad-pixel non validata, parametri esplorativi non accettati come policy. Il worker non riceve la lista delle inserzioni; non è attestazione indipendente di cecità. Il sigillo archivistico è successivo alla prima analisi, non prova pre-verità. Controlli nulli qualificati: 0; limite sui falsi positivi, bias fotometrico e significatività: non disponibili.';
        output.append(summary,details,list,limits);status.textContent='Struttura e contatori coerenti. Risultato esplorativo, non validazione scientifica.';
      }catch(e){if(current===generation){output.replaceChildren();status.textContent='Ricevuta non valida o incompatibile: nessun risultato mostrato.';}}
      finally{if(current===generation)input.value='';}
    });
  }
  if(typeof document!=='undefined'){if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();if(typeof document$!=='undefined')document$.subscribe(init);}
})();
