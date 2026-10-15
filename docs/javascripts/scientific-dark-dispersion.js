/* Passive local declarations; no original-byte attestation or execution. */
(() => {
  'use strict';
  const exact=(v,keys)=>v!==null&&typeof v==='object'&&!Array.isArray(v)
    &&Object.keys(v).length===keys.length&&keys.every(k=>Object.hasOwn(v,k));
  const hash=v=>typeof v==='string'&&/^[a-f0-9]{64}$/.test(v);
  const finite=v=>typeof v==='number'&&Number.isFinite(v);
  const check=ok=>{if(!ok)throw new Error('Ricevuta della dispersione non compatibile.');};
  const kinds=['unfiltered-sample-mean','unfiltered-sample-variance','iid-conditional-unfiltered-mean-variance'];
  const titles=['Media dei dark senza rigetto','Dispersione campionaria senza rigetto',
    'Varianza della media: solo con ipotesi di indipendenza'];
  function inspect(v){
    check(exact(v,['schema','scope','nativeReceiptSha256','pixelProofSha256','sourceInventorySha256',
      'sources','exposureSeconds','sourceYear','geometry','maps','actualRejectedMasterVariance','iidAttested',
      'temporal2024to2026Stability','lightAssociationAttested','completeUncertainty','significance',
      'qualifiedControls','executionAuthorized','scienceValidation']));
    check(v.schema==='BKL051_DARK_DISPERSION_CONTEXT_V1'
      &&v.scope==='REFERENCED_LOCAL_DARK_DISPERSION_ONLY_NOT_MASTER_VARIANCE'
      &&hash(v.nativeReceiptSha256)&&hash(v.pixelProofSha256)&&hash(v.sourceInventorySha256)
      &&v.sources===50&&v.exposureSeconds===600&&v.sourceYear===2024
      &&Array.isArray(v.geometry)&&v.geometry.length===3&&v.geometry.every((n,i)=>n===[2752,2160,1][i])
      &&v.actualRejectedMasterVariance===null&&v.iidAttested===false
      &&v.temporal2024to2026Stability==='UNKNOWN'&&v.lightAssociationAttested===false
      &&v.completeUncertainty===null&&v.significance===null&&v.qualifiedControls===0
      &&v.executionAuthorized===false&&v.scienceValidation==='NOT_VALIDATED'
      &&Array.isArray(v.maps)&&v.maps.length===3);
    const hashes=new Set();
    v.maps.forEach((r,i)=>{
      check(exact(r,['kind','sha256','minimum','maximum','mean','pixels','unit','nativeReopenError','independentPixelError'])
        &&r.kind===kinds[i]&&hash(r.sha256)&&!hashes.has(r.sha256)&&r.pixels===5944320
        &&r.unit===(i===0?'NATIVE_NORMALIZED_SAMPLE':'NATIVE_NORMALIZED_SAMPLE_SQUARED')
        &&[r.minimum,r.maximum,r.mean].every(n=>finite(n)&&n>=0)
        &&r.minimum<=r.mean&&r.mean<=r.maximum&&r.nativeReopenError===0
        &&finite(r.independentPixelError)&&r.independentPixelError>=0&&r.independentPixelError<=1e-15);
      hashes.add(r.sha256);
    });
    for(const key of ['minimum','maximum','mean']){
      const expected=v.maps[1][key]/50,actual=v.maps[2][key];
      check(expected===actual||Math.abs(expected-actual)<=Math.max(Math.abs(expected),Math.abs(actual))*1e-12);
    }
    return Object.freeze({sources:50,maps:3,qualified:0});
  }
  globalThis.DSGDarkDispersion=Object.freeze({inspect});
  const mounted=new WeakMap();let activeRoot;
  function init(){
    const root=document.querySelector('[data-dsg-dark-dispersion]');
    if(activeRoot&&activeRoot.root!==root){activeRoot.clear();activeRoot=undefined;}
    if(!root)return;
    if(mounted.has(root)){activeRoot=mounted.get(root);return;}
    if(root.dataset.initialized)return;
    root.dataset.initialized='true';
    const input=root.querySelector('input[type="file"]'),status=root.querySelector('[role="status"]'),output=root.querySelector('[data-result]');
    let generation=0;
    const clear=()=>{generation++;input.value='';output.replaceChildren();status.textContent='Nessuna dispersione caricata.';};
    activeRoot={root,clear};mounted.set(root,activeRoot);
    const el=(tag,text,parent)=>{const node=document.createElement(tag);node.textContent=text;parent.append(node);return node;};
    async function changed(){
      const current=++generation;output.replaceChildren();status.textContent='Nessuna dispersione caricata.';
      const file=input.files[0];if(!file)return;
      const active=()=>current===generation&&root.isConnected&&document.querySelector('[data-dsg-dark-dispersion]')===root;
      try{
        check(Number.isSafeInteger(file.size)&&file.size>0&&file.size<=1048576);
        const text=await file.text();if(!active())return;
        check(typeof text==='string'&&new TextEncoder().encode(text).length<=1048576);
        const value=JSON.parse(text),summary=inspect(value);
        el('p',`Secondo la ricevuta locale: ${summary.sources} dark del 2024, 600 secondi ciascuno; tre mappe conservate. Controlli qualificati: 0.`,output);
        value.maps.forEach((r,i)=>{
          const card=el('article','',output);el('h3',titles[i],card);
          el('p',`Minimo ${r.minimum.toExponential(6)}; massimo ${r.maximum.toExponential(6)}; media ${r.mean.toExponential(6)}.`,card);
          el('p',i===0?'Unità: campione normalizzato nativo.':'Unità: campione normalizzato nativo al quadrato.',card);
          el('p',`Pixel per mappa: ${r.pixels.toLocaleString('it-IT')}. Errore dichiarato di riapertura: 0; ricontrollo indipendente: ${r.independentPixelError.toExponential(3)}.`,card);
        });
        el('p','La varianza del master effettivo con rigetto sigma resta sconosciuta. La divisione per 50 richiede indipendenza e identica distribuzione dei campioni, qui non attestate. Stabilità 2024–2026, covarianze e incertezza completa restano da valutare. Nessuna mappa è associata automaticamente a una LIGHT.',output);
        el('p','Il browser controlla dichiarazioni importate: non rilegge originali o pixel e non autentica l’autore. Nessun avvio, salvataggio, caricamento in rete o accettazione scientifica.',output);
        status.textContent='Ricevuta coerente; dispersione descrittiva e stima condizionale distinte. Incertezza completa sconosciuta.';
      }catch(e){if(active()){output.replaceChildren();status.textContent='Ricevuta mancante o non valida: nessuna dispersione mostrata.';}}
    }
    input.addEventListener('change',changed);
  }
  if(typeof document!=='undefined'){
    if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
    if(typeof document$!=='undefined')document$.subscribe(init);
    if(typeof window!=='undefined')window.addEventListener('pagehide',()=>{if(activeRoot)activeRoot.clear();});
  }
})();
