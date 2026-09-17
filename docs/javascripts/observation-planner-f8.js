const root=document.querySelector('[data-observation-planner-f8]');
if(root){
 const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const fmt=s=>new Date(s).toLocaleString('it-IT',{timeZone:'Europe/Rome',day:'2-digit',month:'2-digit',hour:'2-digit',minute:'2-digit'});
 const fail=m=>root.innerHTML=`<section class="dsg-op-panel"><h2>F8 non disponibile</h2><p>${esc(m)}</p><p>Fail-closed: nessun ranking precedente viene presentato come corrente.</p></section>`;
 try{
  const r=await fetch('../data/observation-planner-f8-current-astronomy-suitability.json',{cache:'no-store'}); if(!r.ok)throw new Error(`HTTP ${r.status}`); const d=await r.json();
  if(d.authority!=='NONE'||d.consumerMode!=='READ_ONLY'||d.site?.coordinateDisclosure!=='PROHIBITED'||d.boundaries?.protectedCoordinatesPublished!==false)throw new Error('projection boundary non valida');
  const options=d.setupProfiles.map(s=>`<option value="${esc(s.setupId)}">${esc(s.setupName)}</option>`).join('');
  root.innerHTML=`<section class="dsg-op-panel"><h2>F8 — Planner scientifico della notte</h2><p><strong>Forecast:</strong> reale site-specific F7 · <strong>Geometria:</strong> corrente per la notte · <strong>Modalità:</strong> read-only advisory.</p><label for="dsg-f8-setup"><strong>Setup</strong></label> <select id="dsg-f8-setup">${options}</select><div id="dsg-f8-results"></div><p><small>Nessun risultato costituisce readiness, go/no-go, scheduling, comando o Safety Authority.</small></p></section>`;
  const sel=root.querySelector('#dsg-f8-setup'), out=root.querySelector('#dsg-f8-results');
  const render=()=>{const x=d.rankings.find(q=>q.setupId===sel.value); if(!x)return fail('setup non governato'); out.innerHTML=x.targets.map((t,i)=>`<article class="dsg-op-card"><h3>${i+1}. ${esc(t.targetName)}</h3><p>Suitability setup: <strong>${t.setupSuitabilityScore.toFixed(1)}/100</strong></p>${t.bestWindows.map(w=>`<p>${fmt(w.fromUtc)}–${fmt(w.toUtcExclusive)} · score advisory ${w.advisoryScore.toFixed(1)} · quota media ${w.meanAltitudeDeg.toFixed(1)}° · nuvolosità media ${w.meanCloudCoverPct.toFixed(1)}%</p>`).join('')}</article>`).join('')};
  sel.addEventListener('change',render);render();
 }catch(e){fail(e.message||'errore sconosciuto')}
}
