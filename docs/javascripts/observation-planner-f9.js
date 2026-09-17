const root=document.querySelector('[data-observation-planner-f9]');
if(root){
 const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const fmt=s=>new Date(s).toLocaleString('it-IT',{timeZone:'Europe/Rome',day:'2-digit',month:'2-digit',hour:'2-digit',minute:'2-digit'});
 const fail=m=>root.innerHTML=`<section class="dsg-op-panel"><h2>Planner corrente non disponibile</h2><p>${esc(m)}</p><p>Fail-closed: nessun dato storico viene presentato come corrente.</p></section>`;
 try{
  const response=await fetch('../data/observation-planner-f9-current-night.json',{cache:'no-store'});
  if(!response.ok)throw new Error(`projection F9 assente (HTTP ${response.status})`);
  const d=await response.json(), b=d.boundaries||{}, f=d.forecast||{};
  if(d.projectionType!=='BKL031_F9_REPEATABLE_CURRENT_NIGHT'||d.authority!=='NONE'||d.consumerMode!=='READ_ONLY')throw new Error('identity/authority boundary non valida');
  if(f.providerId!=='METEOHUB'||f.upstreamAuthorityId!=='ITALIAMETEO_ARPAE'||f.modelId!=='ICON_2I'||f.freshnessState!=='FRESH')throw new Error('lineage forecast non valida');
  const runMs=Date.parse(f.runInitialisationUtc),retrievedMs=Date.parse(f.retrievedAtUtc),generatedMs=Date.parse(d.generatedAtUtc),runAge=(Date.now()-runMs)/3600000;
  if(!Number.isFinite(runMs)||!Number.isFinite(retrievedMs)||!Number.isFinite(generatedMs)||runAge<0||runAge>18||retrievedMs<runMs||retrievedMs-runMs>18*3600000||generatedMs!==retrievedMs)throw new Error('forecast non corrente o timestamp non valido');
  if(b.recurringTraffic!==true||b.maximumAcquisitionsPerDay!==2||b.monetaryBudgetEur!==0||b.rawGribRetention!=='NONE_EPHEMERAL_ONLY'||b.readinessAuthority!==false||b.automaticTargetSelection!==false||b.schedulingAuthority!==false||b.actionAuthority!=='NONE'||b.commandAuthority!=='NONE'||b.safetyAuthority!=='LOCAL_PHYSICAL_INTERLOCKS'||b.protectedCoordinatesPublished!==false)throw new Error('boundary F9 non valida');
  if(d.method?.ephemerisMode!=='EXPLICIT_MOSEPH_NO_FALLBACK'||d.attribution?.license!=='CC BY 4.0'||d.site?.coordinateDisclosure!=='PROHIBITED')throw new Error('metodo, attribuzione o pubblicazione sito non validi');
  const raw=JSON.stringify(d).toLowerCase();for(const key of ['latitudedeg','longitudedeg','elevationm','gridlatitude','gridlongitude'])if(raw.includes(key))throw new Error('projection contiene coordinate protette');
  const options=d.setupProfiles.map(s=>`<option value="${esc(s.setupId)}">${esc(s.setupName)}</option>`).join('');
  root.innerHTML=`<section class="dsg-op-panel"><h2>Planner della notte corrente</h2><p><strong>Fonte:</strong> MeteoHub · ItaliaMeteo/ARPAE ICON-2I ${esc(f.runInitialisationUtc)} · <strong>aggiornato:</strong> ${fmt(d.generatedAtUtc)}</p><label for="dsg-f9-setup"><strong>Setup</strong></label> <select id="dsg-f9-setup">${options}</select><div id="dsg-f9-results"></div><p><small>Indicazioni scientifiche read-only: non costituiscono readiness, go/no-go, scheduling, comando o Safety Authority.</small></p></section>`;
  const select=root.querySelector('#dsg-f9-setup'),out=root.querySelector('#dsg-f9-results');
  const render=()=>{const ranking=d.rankings.find(x=>x.setupId===select.value);if(!ranking)return fail('setup non governato');out.innerHTML=ranking.targets.map((t,i)=>`<article class="dsg-op-card"><h3>${i+1}. ${esc(t.targetName)}</h3><p>Suitability setup: <strong>${Number(t.setupSuitabilityScore).toFixed(1)}/100</strong></p>${t.bestWindows.length?t.bestWindows.map(w=>`<p>${fmt(w.fromUtc)}–${fmt(w.toUtcExclusive)} · score advisory ${Number(w.advisoryScore).toFixed(1)} · quota media ${Number(w.meanAltitudeDeg).toFixed(1)}° · nuvolosità media ${Number(w.meanCloudCoverPct).toFixed(1)}%</p>`).join(''):'<p>Nessuna finestra astronomicamente eleggibile nella projection corrente.</p>'}</article>`).join('')};
  select.addEventListener('change',render);render();
 }catch(error){fail(error.message||'errore sconosciuto')}
}
