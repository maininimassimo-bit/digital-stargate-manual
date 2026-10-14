/* Comparison of sealed diagnostic rows, partial declared covariance only. */
(() => {
  'use strict';
  const exact=(v,keys)=>v!==null&&typeof v==='object'&&!Array.isArray(v)&&Object.keys(v).length===keys.length&&keys.every(k=>Object.hasOwn(v,k));
  const hash=v=>typeof v==='string'&&/^[a-f0-9]{64}$/.test(v),ref=v=>typeof v==='string'&&/^[a-f0-9]{32}$/.test(v);
  const finite=v=>typeof v==='number'&&Number.isFinite(v),maybe=v=>v===null||finite(v);
  const check=ok=>{if(!ok)throw Error('Confronto multi-epoca non compatibile.');};
  const close=(a,b)=>a===null?b===null:b!==null&&Math.abs(a-b)<=1e-10*Math.max(1,Math.abs(a),Math.abs(b));
  const labels=Object.freeze({TRIPLET_TECHNICAL_COVERAGE_INCOMPLETE:'tripletta tecnica incompleta',MEASUREMENTS_UNAVAILABLE_OR_AMBIGUOUS:'misura assente o ambigua',
    APERTURE_PARAMETERS_DIFFER:'aperture o anelli del fondo differenti',BAND_UNKNOWN:'filtro sconosciuto',FILTERS_INCOMPATIBLE:'filtri incompatibili',
    EPOCH_OR_EXPOSURE_UNKNOWN:'epoca o esposizione sconosciuta',SAME_RECORDED_EPOCH:'stessa epoca registrata',SCALE_UNKNOWN_NOT_REPLACED_WITH_ONE:'scala sconosciuta, non posta a uno',
    UNKNOWN_VARIANCE_NOT_ZERO:'varianza sconosciuta, non posta a zero',UNKNOWN_COVARIANCE_NOT_ZERO:'covarianza sconosciuta, non posta a zero',
    MASTER_CALIBRATION:'calibrazione dei master',RESAMPLING_COVARIANCE:'covarianza del ricampionamento',SKY_ESTIMATOR:'stima del fondo',
    CROWDED_PSF:'PSF e sorgenti confuse',SCALE_ESTIMATION:'stima della scala',PASSBAND_RESPONSE:'risposta di banda',UNKNOWN:'componenti non stabilite'});
  function inspect(v,plan){
    globalThis.DSGTestPlanReview.inspect(plan);
    check(exact(v,['schema','planSha256','headSha256','caseRef','sourceRef','referenceFrameRef','budgetSha256','origin','unit',
      'technicalCoverage','attempts','pairs','omittedComponents','propagation','skyIncludesReadNoise','readNoiseAddedSeparately',
      'sourceAssociation','photometricComparability','scienceValidation','fullVariance','significance','variabilityClassification',
      'qualifiedControls','confirmatoryEligible']));
    const c=plan.cases.find(c=>c.caseRef===v.caseRef);
    check(v.schema==='BKL051_MULTI_EPOCH_COMPARISON_V1'&&v.planSha256===plan.planSha256&&v.headSha256===plan.headSha256&&c
      &&ref(v.sourceRef)&&ref(v.referenceFrameRef)&&hash(v.budgetSha256)&&['SYNTHETIC_TEST','PRIVATE_DECLARATIONS'].includes(v.origin)
      &&v.unit==='NORMALIZED_SAMPLE_SUM'&&['TECHNICAL_COVERAGE_COMPLETE','INCOMPLETE'].includes(v.technicalCoverage)
      &&v.propagation==='FIRST_ORDER_DELTA_METHOD_PARTIAL_DECLARATIONS'
      &&v.sourceAssociation==='OPAQUE_REF_NOT_PHYSICAL_CROSS_MATCH_ATTESTATION'
      &&v.photometricComparability==='NOT_VALIDATED'&&v.scienceValidation==='NOT_VALIDATED'
      &&v.fullVariance===null&&v.significance===null&&v.variabilityClassification==='NOT_EVALUATED'
      &&v.qualifiedControls===0&&v.confirmatoryEligible===false
      &&Array.isArray(v.attempts)&&v.attempts.length===c.attempts.length&&Array.isArray(v.pairs)&&v.pairs.length===2);
    check(Array.isArray(v.omittedComponents)&&v.omittedComponents.length>0&&v.omittedComponents.length<=7
      &&new Set(v.omittedComponents).size===v.omittedComponents.length
      &&v.omittedComponents.every(x=>['MASTER_CALIBRATION','RESAMPLING_COVARIANCE','SKY_ESTIMATOR','CROWDED_PSF','SCALE_ESTIMATION','PASSBAND_RESPONSE','UNKNOWN'].includes(x))
      &&[v.skyIncludesReadNoise,v.readNoiseAddedSeparately].every(x=>x===null||typeof x==='boolean')
      &&!(v.skyIncludesReadNoise===true&&v.readNoiseAddedSeparately===true));
    const heads=new Set();
    for(const r of v.attempts){
      check(exact(r,['journalHeadSha256','frameRefs','technicalState','reportSha256','selection','flux','band','dateObs',
        'exposureSeconds','apertureParameters','background','skySampleCount']));
      const old=c.attempts.find(a=>a.journalHeadSha256===r.journalHeadSha256);
      check(old&&!heads.has(r.journalHeadSha256)&&r.technicalState===old.technicalState);heads.add(r.journalHeadSha256);
      check(Array.isArray(r.frameRefs)&&r.frameRefs.length<=1&&r.frameRefs.every(ref)
        &&(r.technicalState==='COMPLETED'?hash(r.reportSha256):r.reportSha256===null)
        &&['UNAVAILABLE','DIAGNOSTIC_ROW','CLIPPED_OR_BACKGROUND_MISSING','SOURCE_MISSING_OR_AMBIGUOUS'].includes(r.selection)
        &&maybe(r.flux)&&maybe(r.background)&&(r.skySampleCount===null||Number.isSafeInteger(r.skySampleCount)&&r.skySampleCount>=0));
      if(r.selection==='DIAGNOSTIC_ROW')check(finite(r.flux)&&finite(r.background)&&r.skySampleCount>0&&r.apertureParameters!==null);
      else check(r.flux===null);
      if(r.apertureParameters!==null){const p=r.apertureParameters;check(exact(p,['coordinateConvention','apertureRadius','annulusInner','annulusOuter'])
        &&p.coordinateConvention==='PI_NATIVE_GEOMETRIC'&&[p.apertureRadius,p.annulusInner,p.annulusOuter].every(x=>finite(x)&&x>0)&&p.annulusOuter>p.annulusInner);}
      if(r.band===null)check(r.dateObs===null&&r.exposureSeconds===null);
      else{check(['Green','Red','Blu','L-Pro'].includes(r.band)&&typeof r.exposureSeconds==='string'&&finite(Number(r.exposureSeconds))&&Number(r.exposureSeconds)>0);
        globalThis.DSGAstrometryContext.timestampSeconds(r.dateObs);}
    }
    const knownFrames=v.attempts.flatMap(r=>r.frameRefs),unique=new Set(knownFrames);
    if(v.technicalCoverage==='TECHNICAL_COVERAGE_COMPLETE')check(v.attempts.length===3&&knownFrames.length===3&&unique.size===3&&v.attempts.every(r=>r.technicalState==='COMPLETED'));
    const reference=v.attempts.find(r=>r.frameRefs[0]===v.referenceFrameRef),pairRefs=new Set();
    for(const p of v.pairs){
      check(exact(p,['frameRef','rightToReferenceScale','variances','covariances','algebraicDifference','conditionalSigma','blockers'])
        &&ref(p.frameRef)&&p.frameRef!==v.referenceFrameRef&&!pairRefs.has(p.frameRef)&&maybe(p.rightToReferenceScale)
        &&(p.rightToReferenceScale===null||p.rightToReferenceScale>0));pairRefs.add(p.frameRef);
      check(Array.isArray(p.variances)&&p.variances.length===3&&p.variances.every(x=>x===null||finite(x)&&x>=0)
        &&Array.isArray(p.covariances)&&p.covariances.length===3&&p.covariances.every(maybe));
      globalThis.DSGCovariance.conditionalCovarianceSigma(p.variances,p.covariances,[0,0,0],()=>check(false));
      const right=v.attempts.find(r=>r.frameRefs[0]===p.frameRef),reasons=[];
      if(v.technicalCoverage!=='TECHNICAL_COVERAGE_COMPLETE')reasons.push('TRIPLET_TECHNICAL_COVERAGE_INCOMPLETE');
      if(!reference||!right||reference.selection!=='DIAGNOSTIC_ROW'||right.selection!=='DIAGNOSTIC_ROW')reasons.push('MEASUREMENTS_UNAVAILABLE_OR_AMBIGUOUS');
      if(reference&&right){
        const paramOrder=x=>x===null?null:[x.coordinateConvention,x.apertureRadius,x.annulusInner,x.annulusOuter];
        if(JSON.stringify(paramOrder(reference.apertureParameters))!==JSON.stringify(paramOrder(right.apertureParameters)))reasons.push('APERTURE_PARAMETERS_DIFFER');
        if(reference.band===null||right.band===null)reasons.push('BAND_UNKNOWN');
        else if(reference.band!==right.band)reasons.push('FILTERS_INCOMPATIBLE');
        if(reference.dateObs===null||right.dateObs===null)reasons.push('EPOCH_OR_EXPOSURE_UNKNOWN');
        else if(DSGAstrometryContext.timestampSeconds(reference.dateObs)===DSGAstrometryContext.timestampSeconds(right.dateObs))reasons.push('SAME_RECORDED_EPOCH');
      }
      if(p.rightToReferenceScale===null)reasons.push('SCALE_UNKNOWN_NOT_REPLACED_WITH_ONE');
      let difference=null,sigma=null;
      if(!reasons.length){difference=reference.flux-p.rightToReferenceScale*right.flux;check(finite(difference));
        sigma=DSGCovariance.conditionalCovarianceSigma(p.variances,p.covariances,[1,-p.rightToReferenceScale,-right.flux],()=>check(false));}
      if(p.variances.includes(null))reasons.push('UNKNOWN_VARIANCE_NOT_ZERO');
      if(p.covariances.includes(null))reasons.push('UNKNOWN_COVARIANCE_NOT_ZERO');
      check(maybe(p.algebraicDifference)&&(p.conditionalSigma===null||finite(p.conditionalSigma)&&p.conditionalSigma>=0)
        &&close(difference,p.algebraicDifference)&&close(sigma,p.conditionalSigma)
        &&Array.isArray(p.blockers)&&p.blockers.length===reasons.length&&new Set(p.blockers).size===reasons.length&&p.blockers.every(x=>reasons.includes(x)));
    }
    if(v.technicalCoverage==='TECHNICAL_COVERAGE_COMPLETE')check([...unique].every(f=>f===v.referenceFrameRef||pairRefs.has(f)));
    return Object.freeze({attempts:heads.size,algebraicPairs:v.pairs.filter(p=>p.algebraicDifference!==null).length,qualified:0,significance:null});
  }
  globalThis.DSGMultiEpoch=Object.freeze({inspect});
  function init(){
    const root=document.querySelector('[data-dsg-multi-epoch]');if(!root||root.dataset.initialized)return;root.dataset.initialized='true';
    const inputs=[root.querySelector('[data-plan]'),root.querySelector('[data-comparison]')],status=root.querySelector('[role="status"]'),output=root.querySelector('[data-result]');let generation=0;
    async function load(){
      const current=++generation;output.replaceChildren();status.textContent='Apri piano e confronto della stessa cronologia.';if(!inputs.every(i=>i.files[0]))return;
      try{
        const files=inputs.map(i=>i.files[0]);check(files.every(f=>f.size<=1048576));const raw=await Promise.all(files.map(f=>f.text()));
        if(current!==generation||!root.isConnected)return;
        const [plan,v]=raw.map(JSON.parse),s=inspect(v,plan),summary=document.createElement('p'),region=document.createElement('div'),table=document.createElement('table');
        summary.textContent=`${v.origin==='SYNTHETIC_TEST'?'Prova sintetica dichiarata':'Dichiarazioni private; origine fisica non attestata'}. Tentativi conservati: ${s.attempts}; differenze algebriche disponibili: ${s.algebraicPairs}. Unità: somma di campioni normalizzati, non flusso calibrato.`;
        region.setAttribute('role','region');region.setAttribute('tabindex','0');region.setAttribute('aria-label','Misure diagnostiche multi-epoca, scorrimento orizzontale');region.style.overflowX='auto';region.style.maxWidth='100%';table.style.minWidth='740px';
        const caption=document.createElement('caption');caption.textContent='Misure dai rapporti tecnici: incertezza completa sconosciuta';table.append(caption);
        const head=document.createElement('thead'),hr=document.createElement('tr');for(const label of ['Tentativo','Epoca registrata','Filtro','Flusso diagnostico','Fondo','Raggio apertura (pixel)','Selezione']){const th=document.createElement('th');th.setAttribute('scope','col');th.textContent=label;hr.append(th);}head.append(hr);table.append(head);
        const body=document.createElement('tbody');for(const [i,r] of v.attempts.entries()){const tr=document.createElement('tr');for(const text of [String(i+1),r.dateObs??'sconosciuta',r.band??'sconosciuto',r.flux===null?'non disponibile':String(r.flux),r.background===null?'non disponibile':String(r.background),r.apertureParameters===null?'non disponibile':String(r.apertureParameters.apertureRadius),r.selection==='DIAGNOSTIC_ROW'?'misura diagnostica':r.selection==='CLIPPED_OR_BACKGROUND_MISSING'?'apertura tagliata o fondo mancante':r.selection==='SOURCE_MISSING_OR_AMBIGUOUS'?'sorgente assente o ambigua':'non disponibile']){const td=document.createElement('td');td.textContent=text;tr.append(td);}body.append(tr);}table.append(body);region.append(table);
        const pairs=document.createElement('ul');for(const p of v.pairs){const li=document.createElement('li');
          li.textContent=`Confronto con ${p.frameRef.slice(0,8)}: scala dichiarata ${p.rightToReferenceScale??'sconosciuta'}; differenza ${p.algebraicDifference??'non disponibile'}; sigma condizionale parziale ${p.conditionalSigma??'non disponibile'}. ${p.blockers.length?'Blocchi: '+p.blockers.map(x=>labels[x]).join('; '):'Nessun blocco aritmetico; confronto scientifico ancora da validare'}.`;pairs.append(li);}
        const limits=document.createElement('p');limits.textContent='Sono calcoli algebrici su misure diagnostiche e budget parziali dichiarati. Stesso identificativo opaco e filtro non attestano associazione fisica, PSF, risposta di banda o calibrazione. La sigma condizionale non è incertezza completa e non viene usata per significatività o classificazione di variabilità. Nessuna immagine differenza generata; nessun controllo qualificato.';
        const omissions=document.createElement('p');omissions.textContent='Componenti omesse dal budget dichiarato: '+v.omittedComponents.map(x=>labels[x]).join('; ')+'. Nessuna componente omessa è assunta nulla. '+([v.skyIncludesReadNoise,v.readNoiseAddedSeparately].includes(null)?'Inclusione del rumore di lettura nel fondo o sua aggiunta separata: non completamente stabilita.':'La dichiarazione non aggiunge due volte il rumore di lettura; resta da verificare scientificamente.');
        output.append(summary,region,pairs,limits,omissions);status.textContent='Ricevute coerenti; calcolo ricontrollato. Confronto scientifico e variabilità non validati.';
      }catch(e){if(current===generation){output.replaceChildren();status.textContent='Ricevute non valide o non corrispondenti: nessun confronto mostrato.';}}
    }
    for(const input of inputs)input.addEventListener('change',load);
  }
  if(typeof document!=='undefined'){if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();if(typeof document$!=='undefined')document$.subscribe(init);}
})();
