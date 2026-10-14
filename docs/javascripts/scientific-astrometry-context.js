/* Candidate WCS and timing receipts: passive, exact decimal time arithmetic. */
(() => {
  'use strict';
  const exact=(v,keys)=>v!==null&&typeof v==='object'&&!Array.isArray(v)&&Object.keys(v).length===keys.length&&keys.every(k=>Object.hasOwn(v,k));
  const hash=v=>typeof v==='string'&&/^[a-f0-9]{64}$/.test(v);
  const number=v=>typeof v==='number'&&Number.isFinite(v)&&v>=0;
  const count=v=>Number.isSafeInteger(v)&&v>=0;
  const check=ok=>{if(!ok)throw Error('Contesto astrometrico non compatibile.');};
  const scale=1000000000000n;
  function decimal(v){
    check(typeof v==='string'&&/^-?\d{1,14}(?:\.\d{1,12})?$/.test(v));
    const negative=v.startsWith('-'),[whole,fraction='']=(negative?v.slice(1):v).split('.');
    return (negative?-1n:1n)*(BigInt(whole)*scale+BigInt(fraction.padEnd(12,'0')));
  }
  function timestamp(v){
    check(typeof v==='string'&&/^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d{1,12})?Z?$/.test(v));
    const [date,time]=v.replace(/Z$/,'').split('T'),[h,m,s]=time.split(':'),d=new Date(date+'T00:00:00Z');
    check(Number.isFinite(d.getTime())&&d.toISOString().slice(0,10)===date&&Number(h)<24&&Number(m)<60&&Number(s)<60);
    return BigInt(d.getTime()/1000)*scale+BigInt(h)*3600n*scale+BigInt(m)*60n*scale+decimal(s);
  }
  function inspect(v,lineage){
    globalThis.DSGInputLineage.inspect(lineage);
    check(exact(v,['schema','lineageReceiptSha256','candidateDraftSha256','candidatePlanRef','solverReceiptSha256','wcsReceiptSha256',
      'inputRef','rawSha256','parentDerivedSha256','wcsDerivedSha256','filter','geometry','solutionState','catalog',
      'catalogEpochPropagation','pixelConvention','pixelEquality','holdout','timing','byteIntegrity','scienceValidation',
      'significance','qualifiedControls','executionAuthorized']));
    check(v.schema==='BKL051_ASTROMETRY_CONTEXT_V1'&&['lineageReceiptSha256','candidateDraftSha256','solverReceiptSha256',
      'wcsReceiptSha256','rawSha256','parentDerivedSha256','wcsDerivedSha256'].every(k=>hash(v[k]))
      &&v.lineageReceiptSha256===lineage.receiptSha256&&v.candidateDraftSha256===lineage.candidateDraftSha256
      &&v.candidatePlanRef===lineage.candidatePlanRef&&v.solutionState==='CANDIDATE_NOT_VALIDATED'&&v.catalog==='Gaia DR3'
      &&v.catalogEpochPropagation==='RETAINED_NATIVE_CONDITIONAL_NO_FULL_COVARIANCE'
      &&v.pixelConvention==='PI_NATIVE_GEOMETRIC_RETAINED_CALLER'&&v.pixelEquality==='RETAINED_NATIVE_ZERO_DIFFERENCE_NOT_REMEASURED'
      &&v.byteIntegrity==='RECHECKED_LOCAL_FILES'&&v.scienceValidation==='NOT_VALIDATED'
      &&v.significance===null&&v.qualifiedControls===0&&v.executionAuthorized===false);
    const input=lineage.inputs.find(r=>r.inputRef===v.inputRef);
    check(input&&input.rawSha256===v.rawSha256&&input.derivedSha256===v.parentDerivedSha256&&input.filter===v.filter
      &&new Set([v.rawSha256,v.parentDerivedSha256,v.wcsDerivedSha256]).size===3
      &&Array.isArray(v.geometry)&&v.geometry.length===3&&v.geometry.every(n=>count(n)&&n>0));
    const h=v.holdout;
    check(exact(h,['trainingReferences','heldOutReferences','matched','unmatched','outsideOrUnprojectable','radialRMSPixel',
      'largestResidualPixel','largestSquaredResidualShare','searchGeometry','partition','centroidReuse','unmatchedOutsideRecheck',
      'scope','fullCovariance','independentScientificValidation'])
      &&['trainingReferences','heldOutReferences','matched','unmatched','outsideOrUnprojectable'].every(k=>count(h[k]))
      &&h.trainingReferences>0&&h.heldOutReferences===h.matched+h.unmatched+h.outsideOrUnprojectable&&h.matched>0
      &&number(h.radialRMSPixel)&&number(h.largestResidualPixel)&&h.largestResidualPixel>=h.radialRMSPixel
      &&h.searchGeometry==='SQUARE_PLUS_MINUS_3_PIXELS_DIAGNOSTIC_ONLY'&&h.partition==='DISJOINT_RECHECKED'&&h.centroidReuse===0
      &&h.unmatchedOutsideRecheck==='RETAINED_STATES_NOT_REMATCHED'
      &&h.scope==='DESCRIPTIVE_SCATTER_NOT_WCS_OR_PER_SOURCE_UNCERTAINTY'&&h.fullCovariance===null&&h.independentScientificValidation===false);
    if(h.radialRMSPixel===0)check(h.largestResidualPixel===0&&h.largestSquaredResidualShare===null);
    else check(number(h.largestSquaredResidualShare)&&h.largestSquaredResidualShare>0&&h.largestSquaredResidualShare<=1
      &&Math.abs(h.largestSquaredResidualShare-(h.largestResidualPixel/h.radialRMSPixel)**2/h.matched)<1e-10);
    const t=v.timing;
    check(exact(t,['sourceDateObs','sourceDateAvg','derivedDateObs','derivedDateAvg','exposureSeconds',
      'averageMinusStartHalfExposureSeconds','derivedStartMinusSourceSeconds','averagePreserved','timeScale',
      'clockShutterUncertainty','endTimeOrigin'])&&decimal(t.exposureSeconds)>0n
      &&2n*(timestamp(t.sourceDateAvg)-timestamp(t.sourceDateObs))-decimal(t.exposureSeconds)===2n*decimal(t.averageMinusStartHalfExposureSeconds)
      &&timestamp(t.derivedDateObs)-timestamp(t.sourceDateObs)===decimal(t.derivedStartMinusSourceSeconds)
      &&typeof t.averagePreserved==='boolean'&&t.averagePreserved===(t.sourceDateAvg===t.derivedDateAvg)
      &&t.timeScale==='HEADER_DECLARATION_NOT_CLOCK_ATTESTATION'&&t.clockShutterUncertainty===null
      &&['DERIVED_METADATA_NOT_IN_SOURCE','NOT_ESTABLISHED_BY_THIS_IMPORT'].includes(t.endTimeOrigin));
    timestamp(t.derivedDateAvg);
    return Object.freeze({matched:h.matched,unmatched:h.unmatched,outside:h.outsideOrUnprojectable,qualified:0,covariance:null});
  }
  globalThis.DSGAstrometryContext=Object.freeze({inspect,timestampSeconds:timestamp});
  function init(){
    const root=document.querySelector('[data-dsg-astrometry-context]');if(!root||root.dataset.initialized)return;root.dataset.initialized='true';
    const inputs=[root.querySelector('[data-lineage]'),root.querySelector('[data-astrometry]')],status=root.querySelector('[role="status"]'),output=root.querySelector('[data-result]');let generation=0;
    async function load(){
      const current=++generation;output.replaceChildren();status.textContent='Apri provenienza e contesto astrometrico corrispondenti.';
      if(!inputs.every(i=>i.files[0]))return;
      try{
        const files=inputs.map(i=>i.files[0]);check(files.every(f=>f.size<=1048576));
        const raw=await Promise.all(files.map(f=>f.text()));if(current!==generation||!root.isConnected)return;
        const [lineage,v]=raw.map(JSON.parse),s=inspect(v,lineage),h=v.holdout,t=v.timing;
        const summary=document.createElement('p'),residual=document.createElement('p'),times=document.createElement('ul'),limits=document.createElement('p');
        summary.textContent=`${v.filter}: WCS candidata, catalogo Gaia DR3. Geometria ${v.geometry.join(' × ')}; convenzione geometrica nativa del chiamante PixInsight. Propagazione di epoca condizionale, covarianza completa non disponibile.`;
        residual.textContent=`Riferimenti di addestramento: ${h.trainingReferences}; esclusi dal fit: ${h.heldOutReferences}. Associazioni ricontrollate: ${s.matched}; senza associazione dichiarati: ${s.unmatched}; esterni o non proiettabili dichiarati: ${s.outside}. RMS radiale ${h.radialRMSPixel} pixel, residuo maggiore ${h.largestResidualPixel} pixel (${h.largestSquaredResidualShare===null?'quota quadratica non definita':100*h.largestSquaredResidualShare+'% della somma quadratica'}). È dispersione descrittiva, non incertezza della WCS o della singola sorgente.`;
        for(const text of [`DATE-OBS originale: ${t.sourceDateObs}; copia WCS: ${t.derivedDateObs}. Scarto copia meno originale: ${t.derivedStartMinusSourceSeconds} s.`,
          `DATE-AVG originale: ${t.sourceDateAvg}; copia: ${t.derivedDateAvg}; ${t.averagePreserved?'preservato':'modificato'}.`,
          `Esposizione: ${t.exposureSeconds} s. DATE-AVG meno DATE-OBS meno metà esposizione: ${t.averageMinusStartHalfExposureSeconds} s; aritmetica degli header, nessuna correzione del tempo.`,
          t.endTimeOrigin==='DERIVED_METADATA_NOT_IN_SOURCE'?'Il tempo di fine compare nei metadati derivati ed è assente nell’originale: non è un tempo acquisito attestato.':'Origine del tempo di fine non stabilita da questa importazione.']){
          const item=document.createElement('li');item.textContent=text;times.append(item);}
        limits.textContent='Ricerca diagnostica in un quadrato ±3 pixel, non taglio radiale e non soglia scientifica. Nessun centroide riutilizzato fra le associazioni ricontrollate. I casi senza associazione o esterni non sono stati riassociati. Clock, shutter, sistema temporale fisico e propagazione completa restano da validare. Uguaglianza dei pixel riportata dalla precedente prova nativa, non rimisurata. Nessun controllo indipendente qualificato.';
        output.append(summary,residual,times,limits);status.textContent='Ricevute coerenti: soluzione candidata, nessuna validazione scientifica o autorizzazione al lancio.';
      }catch(e){if(current===generation){output.replaceChildren();status.textContent='Ricevute non valide o non corrispondenti: nessun risultato astrometrico mostrato.';}}
    }
    for(const i of inputs)i.addEventListener('change',load);
  }
  if(typeof document!=='undefined'){if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();if(typeof document$!=='undefined')document$.subscribe(init);}
})();
