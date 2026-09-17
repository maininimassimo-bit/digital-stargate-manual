const host=document.querySelector('[data-observation-planner-ranking]');
const esc=value=>String(value??'').replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[char]);

if(host){
  const allowedRoot=new Set(['schemaVersion','projectionType','projectionId','environment','authority','consumerMode','method','lineage','results','limitations','boundary','projectionDigest']);
  const forbidden=new Set(['safe','isSafe','ready','readiness','goNoGo','scheduler','scheduleCommand','deviceCommand','command','automaticSelection','safetyDecision']);
  const scan=(value,path='projection')=>{
    if(Array.isArray(value)) return value.forEach((child,index)=>scan(child,`${path}[${index}]`));
    if(!value||typeof value!=='object') return;
    for(const [key,child] of Object.entries(value)){
      if(forbidden.has(key)) throw new Error(`${path}.${key} non autorizzato nel consumer F5.`);
      scan(child,`${path}.${key}`);
    }
  };
  const validate=projection=>{
    if(!projection||typeof projection!=='object'||Array.isArray(projection)) throw new Error('Projection ranking non valida.');
    if(Object.keys(projection).some(key=>!allowedRoot.has(key))||[...allowedRoot].some(key=>!Object.hasOwn(projection,key))) throw new Error('Projection ranking con proprietà inattese o mancanti.');
    if(projection.schemaVersion!=='1.0'||projection.projectionType!=='BKL031_F5_EXPLAINABLE_RANKING_PROJECTION') throw new Error('Identità F5 non valida.');
    if(projection.environment!=='EVALUATION'||projection.authority!=='NONE'||projection.consumerMode!=='READ_ONLY') throw new Error('Boundary F5 non valida.');
    if(projection.method.id!=='BKL031-F5-EXPLAINABLE-RANKING'||projection.method.version!=='1.0'||projection.method.factorDefinitions.length!==4) throw new Error('Metodo F5 non valido.');
    if(projection.lineage.forecastEvidenceDigest!=='350a7b9ae8b2de308ba55a7105e56bb4de5040572370ab2715c0fa70088af2f5'||projection.lineage.providerRequestBudget!=='2/2_EXHAUSTED') throw new Error('Lineage F5 non valida.');
    if(projection.results.length!==2||projection.results[0].rank!==1||projection.results[1].rank!==2) throw new Error('Ranking F5 non deterministico.');
    if(projection.boundary.readinessAuthority!==false||projection.boundary.automaticTargetSelection!==false||projection.boundary.schedulingAuthority!==false||projection.boundary.commandAuthority!=='NONE'||projection.boundary.actionAuthority!=='NONE'||projection.boundary.safetyAuthority!=='LOCAL_PHYSICAL_INTERLOCKS') throw new Error('Authority escalation F5.');
    if(!projection.limitations.includes('SYNTHETIC_FACTOR_VALUES_FOR_METHOD_VALIDATION_ONLY')) throw new Error('Limite sintetico F5 non preservato.');
    scan(projection); return true;
  };
  const fail=message=>{host.innerHTML=`<section class="dsg-op-panel dsg-op-fail" role="alert"><span>FAIL-CLOSED</span><h2>Ranking dimostrativo non disponibile</h2><p>${esc(message)}</p><p>Nessun risultato precedente o fallback viene mostrato.</p></section>`;};
  const render=projection=>{
    host.innerHTML=`<section class="dsg-op-panel dsg-op-evidence"><div><span>F5 · EXPLAINABLE RANKING</span><h2>Ranking dimostrativo read-only</h2><p>Metodo <code>${esc(projection.method.id)}@${esc(projection.method.version)}</code>. I factor values sono sintetici e servono soltanto a validare metodo, decomposition e ordinamento deterministico.</p></div><span class="dsg-op-badge">EVALUATION · NONE</span></section>
    <section class="dsg-op-summary">${projection.results.map(item=>`<article><span>RANK ${item.rank}</span><strong>${esc(item.canonicalName)}</strong><small>score dimostrativo ${item.score.toLocaleString('it-IT',{maximumFractionDigits:4})}</small></article>`).join('')}</section>
    ${projection.results.map(item=>`<section class="dsg-op-panel"><div class="dsg-op-panel__head"><div><span>DECOMPOSITION · RANK ${item.rank}</span><h2>${esc(item.canonicalName)}</h2></div><small>${esc(item.targetId)}</small></div><div class="dsg-op-facts">${item.factors.map(f=>`<article><span>${esc(f.id)}</span><strong>${Number(f.contribution*100).toLocaleString('it-IT',{maximumFractionDigits:3})}</strong><small>raw ${esc(f.rawValue)} ${esc(f.unit)} · peso ${esc(f.weight)}</small></article>`).join('')}</div></section>`).join('')}
    <section class="dsg-op-panel dsg-op-boundary"><span>AUTHORITY BOUNDARY</span><h2>Dimostratore, non decisione operativa</h2><p>Le identità target sono governate, ma i factor values F5 sono sintetici. F4-D non pubblica forecast values. Il risultato non indica readiness, go/no-go o sicurezza, non pianifica, non seleziona automaticamente target, non invia comandi e non sostituisce gli interlock fisici locali. S10 runtime resta <strong>UNAVAILABLE</strong>.</p></section>`;
  };
  fetch('../data/observation-planner-ranking-f5-projection.json',{cache:'no-store'})
    .then(response=>{if(!response.ok) throw new Error(`Projection F5 repository assente (HTTP ${response.status}).`); return response.json();})
    .then(projection=>{validate(projection);render(projection);})
    .catch(error=>fail(error.message));
}
