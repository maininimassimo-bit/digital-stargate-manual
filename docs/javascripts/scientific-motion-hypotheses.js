/* Passive, exhaustive association hypotheses inside an explicitly limited pool. */
(() => {
  'use strict';
  const exact=(v,keys)=>v!==null&&typeof v==='object'&&!Array.isArray(v)&&Object.keys(v).length===keys.length&&keys.every(k=>Object.hasOwn(v,k));
  const ref=v=>typeof v==='string'&&/^[a-f0-9]{32}$/.test(v),hash=v=>typeof v==='string'&&/^[a-f0-9]{64}$/.test(v);
  const finite=v=>typeof v==='number'&&Number.isFinite(v),count=v=>Number.isSafeInteger(v)&&v>=0;
  const check=ok=>{if(!ok)throw Error('Ipotesi di moto non compatibili.');};
  const close=(a,b)=>finite(a)&&finite(b)&&Math.abs(a-b)<=1e-8*Math.max(1,Math.abs(a),Math.abs(b));
  function fit(times,positions){
    const hours=times.map(t=>t/3600),mean=hours.reduce((a,b)=>a+b,0)/3,dt=hours.map(t=>t-mean),den=dt.reduce((a,b)=>a+b*b,0);
    check(den>0);const center=[0,1].map(k=>positions.reduce((a,p)=>a+p[k],0)/3);
    const velocity=[0,1].map(k=>positions.reduce((a,p,i)=>a+dt[i]*(p[k]-center[k]),0)/den),intercept=[0,1].map(k=>center[k]-velocity[k]*mean);
    const residuals=positions.map((p,i)=>[0,1].map(k=>p[k]-intercept[k]-velocity[k]*hours[i])),distances=residuals.map(r=>Math.hypot(...r));
    return {velocity,intercept,residuals,rms:Math.hypot(...distances)/Math.sqrt(3),max:Math.max(...distances)};
  }
  function inspect(v){
    check(exact(v,['schema','poolSha256','pool','expectedHypotheses','hypotheses','status','resourceLimit','selectedHypothesis','model',
      'crossEpochCovariance','scienceValidation','trackletAccepted','movingObjectClassification','blindRecovery','qualifiedControls','submissionAuthorized']));
    check(v.schema==='BKL051_MOTION_HYPOTHESES_V1'&&hash(v.poolSha256)&&v.resourceLimit===4096&&v.selectedHypothesis===null
      &&v.model==='UNWEIGHTED_LINEAR_TANGENT_PLANE_DESCRIPTIVE_NOT_ORBIT'&&v.crossEpochCovariance===null
      &&v.scienceValidation==='NOT_VALIDATED'&&v.trackletAccepted===false&&v.movingObjectClassification==='NOT_EVALUATED'
      &&v.blindRecovery===false&&v.qualifiedControls===0&&v.submissionAuthorized===false);
    const p=v.pool;check(exact(p,['schema','origin','selectionBasis','sourceEvidenceSha256','coordinateMeaning','timeMeaning','frames'])
      &&p.schema==='BKL051_MOTION_POOL_V1'&&['SYNTHETIC_TEST','PUBLIC_KNOWN_OBJECT_CONTROL'].includes(p.origin)
      &&['SYNTHETIC_CANDIDATES','RETAINED_EPHEMERIS_NEAREST_THREE_NOT_BLIND'].includes(p.selectionBasis)&&hash(p.sourceEvidenceSha256)
      &&p.coordinateMeaning==='RETAINED_TANGENT_PLANE_ARCSEC_ASTROMETRY_UNVALIDATED'
      &&p.timeMeaning==='NOMINAL_RELATIVE_SECONDS_CLOCK_UNVALIDATED'&&Array.isArray(p.frames)&&p.frames.length===3);
    const ids=new Set(),detections=new Set(),images=new Set();let total=1;
    for(const f of p.frames){
      check(exact(f,['frameRef','imageSha256','catalogSha256','elapsedSeconds','recordedJD','band','retainedCatalogSourceCount','candidates'])
        &&ref(f.frameRef)&&!ids.has(f.frameRef)&&hash(f.imageSha256)&&!images.has(f.imageSha256)&&hash(f.catalogSha256)
        &&finite(f.elapsedSeconds)&&f.elapsedSeconds>=0&&f.elapsedSeconds<=1e9
        &&typeof f.recordedJD==='string'&&/^\d{1,7}(?:\.\d{1,24})?$/.test(f.recordedJD)
        &&['zg','Green','Red','Blu','L-Pro'].includes(f.band)&&count(f.retainedCatalogSourceCount)&&f.retainedCatalogSourceCount<=100000
        &&Array.isArray(f.candidates)&&f.candidates.length<=Math.min(256,f.retainedCatalogSourceCount));
      ids.add(f.frameRef);images.add(f.imageSha256);total*=f.candidates.length;
      for(const d of f.candidates){check(exact(d,['detectionRef','positionArcsec','positionCovariance',...(Object.hasOwn(d,'referenceDistanceArcsec')?['referenceDistanceArcsec']:[])])&&ref(d.detectionRef)&&!detections.has(d.detectionRef)
        &&Array.isArray(d.positionArcsec)&&d.positionArcsec.length===2&&d.positionArcsec.every(x=>finite(x)&&Math.abs(x)<=1e7)&&d.positionCovariance===null);detections.add(d.detectionRef);}
      for(const d of f.candidates)check(!Object.hasOwn(d,'referenceDistanceArcsec')||d.referenceDistanceArcsec===null||finite(d.referenceDistanceArcsec)&&d.referenceDistanceArcsec>=0);
    }
    const times=p.frames.map(f=>f.elapsedSeconds);check(times[0]===0&&times[0]<times[1]&&times[1]<times[2]&&v.expectedHypotheses===total&&Array.isArray(v.hypotheses));
    const jd=v=>{const [whole,fraction='']=v.split('.');return BigInt(whole)*10n**24n+BigInt(fraction.padEnd(24,'0'));};
    const jd0=jd(p.frames[0].recordedJD);
    check(p.frames.every(f=>Math.abs(Number(jd(f.recordedJD)-jd0)/1e24*86400-f.elapsedSeconds)<=1e-6));
    const expectedStatus=total>4096?'RESOURCE_LIMIT_NO_PARTIAL_SELECTION':total===0?'EMPTY_POOL_NOT_NONDETECTION':'ALL_POOL_HYPOTHESES_ENUMERATED';
    check(v.status===expectedStatus&&v.hypotheses.length===(total>0&&total<=4096?total:0));
    const hypotheses=new Set();let i=0;
    if(total>0&&total<=4096)for(const a of p.frames[0].candidates)for(const b of p.frames[1].candidates)for(const c of p.frames[2].candidates){
      const h=v.hypotheses[i++],selection=[a,b,c],r=fit(times,selection.map(d=>d.positionArcsec));
      check(exact(h,['hypothesisRef','detectionRefs','interceptArcsec','velocityArcsecPerHour','residualVectorsArcsec','radialRMSArcsec',
        'maximumResidualArcsec','associationState','velocityCovariance','significance'])&&ref(h.hypothesisRef)&&!hypotheses.has(h.hypothesisRef)
        &&Array.isArray(h.detectionRefs)&&h.detectionRefs.length===3&&selection.every((d,k)=>d.detectionRef===h.detectionRefs[k])
        &&h.associationState==='UNREVIEWED_HYPOTHESIS'&&h.velocityCovariance===null&&h.significance===null);
      hypotheses.add(h.hypothesisRef);
      for(const [actual,expected] of [[h.interceptArcsec,r.intercept],[h.velocityArcsecPerHour,r.velocity]])
        check(Array.isArray(actual)&&actual.length===2&&actual.every((x,k)=>close(x,expected[k])));
      check(Array.isArray(h.residualVectorsArcsec)&&h.residualVectorsArcsec.length===3&&h.residualVectorsArcsec.every((row,j)=>Array.isArray(row)&&row.length===2&&row.every((x,k)=>close(x,r.residuals[j][k])))
        &&h.radialRMSArcsec>=0&&h.maximumResidualArcsec>=0&&close(h.radialRMSArcsec,r.rms)&&close(h.maximumResidualArcsec,r.max));
    }
    return Object.freeze({candidates:detections.size,hypotheses:hypotheses.size,expectedHypotheses:total,qualified:0,selected:null});
  }
  globalThis.DSGMotionHypotheses=Object.freeze({inspect});
  function init(){
    const root=document.querySelector('[data-dsg-motion]');if(!root||root.dataset.initialized)return;root.dataset.initialized='true';
    const input=root.querySelector('input'),status=root.querySelector('[role="status"]'),output=root.querySelector('[data-result]');let generation=0;
    input.addEventListener('change',async()=>{
      const current=++generation;output.replaceChildren();status.textContent='Verifica delle ipotesi di associazione…';
      try{
        const file=input.files[0];check(file&&file.size<=4194304);const raw=await file.text();if(current!==generation||!root.isConnected)return;
        const v=JSON.parse(raw),s=inspect(v),summary=document.createElement('p'),frames=document.createElement('ul'),limits=document.createElement('p');
        summary.textContent=`${v.pool.origin==='SYNTHETIC_TEST'?'Prova sintetica dichiarata':'Controllo pubblico con oggetto noto, pre-selezionato'}. Candidati nel gruppo: ${s.candidates}; combinazioni attese: ${s.expectedHypotheses}; ipotesi calcolate: ${s.hypotheses}. Nessuna ipotesi scelta automaticamente, nessun tracklet accettato.`;
        for(const [i,f] of v.pool.frames.entries()){const li=document.createElement('li');li.textContent=`Esposizione ${i+1}: ${f.candidates.length} candidati nel gruppo su ${f.retainedCatalogSourceCount} sorgenti del catalogo conservato; filtro ${f.band}; tempo relativo nominale ${f.elapsedSeconds} s; JD nominale registrato ${f.recordedJD}.`;
          if(f.candidates.some(c=>Object.hasOwn(c,'referenceDistanceArcsec'))){const p=document.createElement('p');p.textContent='Distanze diagnostiche conservate dalla previsione nota: '+f.candidates.map(c=>c.referenceDistanceArcsec===null||c.referenceDistanceArcsec===undefined?'sconosciuta':String(c.referenceDistanceArcsec)+' arcsec').join('; ')+'. Temporizzazione e associazioni non accettate; nessuna soglia applicata.';li.append(p);}frames.append(li);}
        limits.textContent='Modello lineare descrittivo non pesato sul piano tangente, non soluzione orbitale. Pesi uguali di calcolo non attestano incertezze uguali. Tempi, centroidi, WCS e covarianze non validati; RMS dei residui non è incertezza della velocità o significatività. La selezione con effemeride nota non è recupero cieco; tre esposizioni in notti diverse non attestano un tracklet idoneo alla segnalazione. I file originali non sono letti dal browser.';
        output.append(summary,frames);
        if(v.status!=='ALL_POOL_HYPOTHESES_ENUMERATED'){
          const message=document.createElement('p');message.textContent=v.status==='RESOURCE_LIMIT_NO_PARTIAL_SELECTION'?'Limite di risorse superato: nessun sottoinsieme presentato come ricerca completa.':'Gruppo con esposizione priva di candidati: non significa assenza di oggetti mobili.';output.append(message);
        }else{
          const region=document.createElement('div'),table=document.createElement('table'),caption=document.createElement('caption'),head=document.createElement('thead'),tr=document.createElement('tr');
          region.setAttribute('role','region');region.setAttribute('tabindex','0');region.setAttribute('aria-label','Tutte le ipotesi di associazione, scorrimento orizzontale');region.style.overflowX='auto';region.style.maxWidth='100%';table.style.minWidth='660px';caption.textContent='Tutte le combinazioni del gruppo dichiarato, senza graduatoria di accettazione';table.append(caption);
          for(const label of ['Ipotesi','Rilevamenti opachi','Velocità X (arcsec piano/ora)','Velocità Y (arcsec piano/ora)','RMS descrittivo (arcsec piano)']){const th=document.createElement('th');th.setAttribute('scope','col');th.textContent=label;tr.append(th);}head.append(tr);table.append(head);const body=document.createElement('tbody');
          for(const [i,h] of v.hypotheses.entries()){const row=document.createElement('tr');for(const text of [String(i+1),h.detectionRefs.map(r=>r.slice(0,8)).join(' / '),String(h.velocityArcsecPerHour[0]),String(h.velocityArcsecPerHour[1]),String(h.radialRMSArcsec)]){const td=document.createElement('td');td.textContent=text;row.append(td);}body.append(row);}table.append(body);region.append(table);output.append(region);
        }
        output.append(limits);status.textContent='Struttura e calcoli coerenti. Associazioni fisiche e oggetti mobili non confermati.';
      }catch(e){if(current===generation){output.replaceChildren();status.textContent='Ricevuta non valida o incompatibile: nessuna ipotesi mostrata.';}}
      finally{if(current===generation)input.value='';}
    });
  }
  if(typeof document!=='undefined'){if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();if(typeof document$!=='undefined')document$.subscribe(init);}
})();
