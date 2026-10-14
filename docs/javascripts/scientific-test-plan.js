/* Local private plan inspection. No network, persistence, execution or scientific acceptance. */
(() => {
  'use strict';
  const exact=(v,keys)=>v!==null&&typeof v==='object'&&!Array.isArray(v)&&Object.keys(v).length===keys.length&&keys.every(k=>Object.hasOwn(v,k));
  const ref=v=>typeof v==='string'&&/^[a-f0-9]{32}$/.test(v);
  const hash=v=>typeof v==='string'&&/^[a-f0-9]{64}$/.test(v);
  const check=(ok)=>{if(!ok)throw new Error('Piano non valido: nessun conteggio mostrato.');};
  function inspect(v){
    check(exact(v,['schema','planRef','mode','falsePositiveMaximum','confidence','requiredControls','algorithmRef','cases']));
    check(v.schema==='BKL051_TEST_PLAN_DRAFT_V1'&&ref(v.planRef)&&v.mode==='PRELIMINARY_DRAFT'&&v.falsePositiveMaximum===0.05&&v.confidence===0.95&&v.requiredControls===59);
    check((v.algorithmRef===null||hash(v.algorithmRef))&&Array.isArray(v.cases)&&v.cases.length<=500);
    const ids=new Set(),frames=new Set(),hashes=new Set();let clusters=new Set();
    for(const c of v.cases){
      check(exact(c,['caseRef','clusterRef','frames','qualification','truth','execution']));
      check(ref(c.caseRef)&&!ids.has(c.caseRef)&&ref(c.clusterRef));ids.add(c.caseRef);clusters.add(c.clusterRef);
      check(c.qualification==='CANDIDATE'&&c.truth==='UNVERIFIED'&&c.execution==='NOT_RUN');
      check(Array.isArray(c.frames)&&c.frames.length===3);
      for(const f of c.frames){check(exact(f,['frameRef','sha256'])&&ref(f.frameRef)&&hash(f.sha256)&&!frames.has(f.frameRef)&&!hashes.has(f.sha256));frames.add(f.frameRef);hashes.add(f.sha256);}
    }
    return Object.freeze({candidates:ids.size,frames:frames.size,clusters:clusters.size,qualified:0,executed:0,statisticalResult:null});
  }
  function revise(value,algorithmRef,excluded=[]){
    inspect(value);check(algorithmRef===null||hash(algorithmRef));
    check(Array.isArray(excluded)&&new Set(excluded).size===excluded.length
      &&excluded.every(id=>ref(id)&&value.cases.some(c=>c.caseRef===id)));
    const revised=JSON.parse(JSON.stringify(value));revised.algorithmRef=algorithmRef;
    revised.cases=revised.cases.filter(c=>!excluded.includes(c.caseRef));inspect(revised);return revised;
  }
  globalThis.DSGTestPlan=Object.freeze({inspect,revise});
  function init(){
    const root=document.querySelector('[data-dsg-test-plan]');if(!root||root.dataset.initialized)return;root.dataset.initialized='true';
    const input=root.querySelector('input'),message=root.querySelector('[role="status"]'),output=root.querySelector('[data-dsg-test-plan-result]');let version=0,loaded=null;
    const exportButton=root.querySelector('[data-dsg-plan-export]'),algorithm=root.querySelector('[data-dsg-plan-algorithm]'),exclude=root.querySelector('[data-dsg-plan-exclude]');
    if(exportButton&&typeof exportButton.addEventListener==='function')exportButton.addEventListener('click',()=>{
      try{
        check(loaded!==null);const ids=exclude.value.trim()?exclude.value.trim().split(/\s+/):[];
        const value=revise(loaded,algorithm.value.trim()||null,ids);
        const url=URL.createObjectURL(new Blob([JSON.stringify(value,null,2)+'\n'],{type:'application/json'}));
        const link=document.createElement('a');link.href=url;link.download='piano-bozza-revisione.json';link.click();
        setTimeout(()=>URL.revokeObjectURL(url),1000);
        message.textContent='Nuova bozza preparata per il salvataggio. Il piano originale resta invariato. Congelamento e motivi delle esclusioni richiedono una nuova versione sul PC.';
      }catch(e){message.textContent='Revisione non valida: controlla impronta algoritmo ed esclusioni. Nessun file preparato.';}
    });
    input.addEventListener('change',async()=>{
      const current=++version;loaded=null;if(exportButton)exportButton.disabled=true;output.textContent='';message.textContent='Verifica del piano locale…';
      try{const file=input.files[0];check(file&&file.size<=1048576);const text=await file.text();if(current!==version||!root.isConnected)return;const value=JSON.parse(text),s=inspect(value);
        loaded=value;if(exportButton)exportButton.disabled=false;if(algorithm)algorithm.value=value.algorithmRef||'';if(exclude)exclude.value='';
        output.textContent=`Sequenze candidate: ${s.candidates}. Immagini distinte: ${s.frames}. Gruppi di dipendenza dichiarati: ${s.clusters}. Controlli qualificati: 0. Prove eseguite: 0. Risultato statistico: non disponibile.`;
        message.textContent='Bozza locale verificata nella struttura. Provenienza, indipendenza e assenza del fenomeno non sono attestate.';
      }catch(e){if(current===version){output.textContent='';message.textContent='Piano non valido o non compatibile: nessun conteggio mostrato.';}}
      finally{if(current===version)input.value='';}
    });
  }
  if(typeof document!=='undefined'){if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();if(typeof document$!=='undefined')document$.subscribe(init);}
})();
