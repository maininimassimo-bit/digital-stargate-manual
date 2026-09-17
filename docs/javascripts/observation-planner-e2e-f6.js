const host=document.querySelector('[data-observation-planner-f6]');
const F6_TYPE='BKL031_F6_REAL_EVIDENCE_SETUP_AWARE_E2E_PROJECTION';
const F6_METHOD='BKL031-F6-REAL-EVIDENCE-SETUP-AWARE-E2E';
const F4C_DIGEST='350a7b9ae8b2de308ba55a7105e56bb4de5040572370ab2715c0fa70088af2f5';
const esc=value=>String(value??'').replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[char]);

if(host){
  const fail=message=>{host.innerHTML=`<section class="dsg-op-panel dsg-op-fail" role="alert"><span>FAIL-CLOSED</span><h2>F6 E2E non disponibile</h2><p>${esc(message)}</p><p>Nessun fallback, readiness o selezione automatica viene mostrato.</p></section>`;};
  const validate=projection=>{
    const root=['schemaVersion','projectionType','projectionId','environment','authority','consumerMode','method','forecastEvidence','weatherSample','setupScenarios','lineage','limitations','boundary'];
    if(!projection||typeof projection!=='object'||Array.isArray(projection)) throw new Error('Projection F6 non valida.');
    if(Object.keys(projection).some(key=>!root.includes(key))||root.some(key=>!Object.hasOwn(projection,key))) throw new Error('Projection F6 con proprietà inattese o mancanti.');
    if(projection.schemaVersion!=='1.0'||projection.projectionType!==F6_TYPE||projection.projectionId!=='BKL031-F6-E2E-001') throw new Error('Identità F6 non valida.');
    if(projection.environment!=='EVALUATION'||projection.authority!=='NONE'||projection.consumerMode!=='READ_ONLY') throw new Error('Boundary EVALUATION/NONE/READ_ONLY non valida.');
    if(projection.method?.id!==F6_METHOD||projection.method?.version!=='1.0'||projection.method?.rankingAuthority!=='NONE') throw new Error('Metodo F6 non valido.');
    if(projection.forecastEvidence?.evidenceDigest!==F4C_DIGEST||projection.forecastEvidence?.providerRequestBudget!=='2/2_EXHAUSTED'||projection.forecastEvidence?.protectedSiteUsed!==false) throw new Error('Lineage forecast F6 non valida.');
    if(projection.forecastEvidence?.evidenceClass!=='REAL_PROVIDER_BOUNDED_GENERALIZED'||projection.forecastEvidence?.locationClass!=='SYNTHETIC_GENERALIZED') throw new Error('Classificazione forecast F6 non valida.');
    if(!projection.weatherSample||projection.weatherSample.semantics!=='REAL_F4C_VALUE_SAMPLE_FOR_E2E_DATA_PATH_PROOF_NOT_READINESS') throw new Error('Campione meteo F6 non valido.');
    for(const value of [projection.weatherSample.temperatureC,projection.weatherSample.relativeHumidityPct,projection.weatherSample.dewPointC,projection.weatherSample.precipitationMm,projection.weatherSample.cloudCoverPct,projection.weatherSample.windSpeedKmh,projection.weatherSample.windGustKmh]) if(!Number.isFinite(value)) throw new Error('Campione meteo F6 incompleto.');
    if(!Array.isArray(projection.setupScenarios)||projection.setupScenarios.length!==2) throw new Error('Scenari setup F6 non validi.');
    for(const scenario of projection.setupScenarios){
      if(!['WIDEFIELD_OSC','LONG_FOCAL_MONO'].includes(scenario.setupPublicKey)||scenario.compatibilityBasis!=='REGISTERED_SCIENTIFIC_SESSION_EVIDENCE') throw new Error('Setup pubblico F6 non valido.');
      if(!Array.isArray(scenario.eligibleTargets)||scenario.eligibleTargets.length!==1||scenario.eligibleTargets[0].setupCompatibilityState!=='SUPPORTED_BY_HISTORY'||scenario.eligibleTargets[0].f5ScoreClass!=='SYNTHETIC_METHOD_VALIDATION_ONLY') throw new Error('Target eleggibile F6 non valido.');
      if(!Array.isArray(scenario.excludedTargets)||scenario.excludedTargets.length!==1||scenario.excludedTargets[0].setupCompatibilityState!=='UNVERIFIED_FOR_SELECTED_SETUP') throw new Error('Fail-closed setup F6 non valido.');
    }
    const boundary=projection.boundary||{};
    if(boundary.readinessAuthority!==false||boundary.automaticTargetSelection!==false||boundary.schedulingAuthority!==false||boundary.actionAuthority!=='NONE'||boundary.commandAuthority!=='NONE'||boundary.safetyAuthority!=='LOCAL_PHYSICAL_INTERLOCKS'||boundary.runtimeState!=='UNAVAILABLE'||boundary.providerRequestsPerformedByF6!==0) throw new Error('Authority escalation F6.');
    for(const required of ['F4C_LOCATION_SYNTHETIC_GENERALIZED_NOT_PROTECTED_SITE','FORECAST_SAMPLE_IS_REAL_PROVIDER_EVIDENCE_BUT_NOT_CURRENT_RUNTIME_FEED','F5_METHOD_SCORE_REMAINS_SYNTHETIC_GEOMETRY_METHOD_EVIDENCE','SETUP_COMPATIBILITY_IS_HISTORICAL_ACQUISITION_EVIDENCE_NOT_OPTICAL_SUITABILITY_MODEL','NO_ADDITIONAL_PROVIDER_TRAFFIC']) if(!projection.limitations.includes(required)) throw new Error(`Limite F6 mancante: ${required}`);
    const text=JSON.stringify(projection);
    for(const forbidden of ['QUATTRO200_TOUPTEK294_BIN1','C8_QHY695A_BIN1','DSG-CURRENT-SETUP-ASSIGNMENT-001','DSG-SETUP-BASELINE-001','governance/setup-authority/']) if(text.includes(forbidden)) throw new Error('Dettaglio setup protetto rilevato nella projection pubblica.');
  };
  const weather=sample=>`<div class="dsg-op-facts">
    <article><span>Temperatura</span><strong>${esc(sample.temperatureC)} °C</strong><small>${esc(sample.validAtUtc)}</small></article>
    <article><span>Umidità relativa</span><strong>${esc(sample.relativeHumidityPct)}%</strong><small>dew point ${esc(sample.dewPointC)} °C</small></article>
    <article><span>Nuvolosità</span><strong>${esc(sample.cloudCoverPct)}%</strong><small>low ${esc(sample.cloudCoverLowPct)}% · mid ${esc(sample.cloudCoverMidPct)}% · high ${esc(sample.cloudCoverHighPct)}%</small></article>
    <article><span>Precipitazione</span><strong>${esc(sample.precipitationMm)} mm</strong><small>valore F4-C reale</small></article>
    <article><span>Vento</span><strong>${esc(sample.windSpeedKmh)} km/h</strong><small>raffiche ${esc(sample.windGustKmh)} km/h</small></article>
  </div>`;
  const scenarioMarkup=scenario=>{
    const eligible=scenario.eligibleTargets[0];
    const excluded=scenario.excludedTargets[0];
    return `<section class="dsg-op-panel"><div class="dsg-op-panel__head"><div><span>SETUP-AWARE EVIDENCE</span><h2>${esc(scenario.setupLabel)}</h2></div><small>${esc(scenario.setupPublicKey)}</small></div>
      <div class="dsg-op-summary"><article><span>SUPPORTED BY HISTORY</span><strong>${esc(eligible.canonicalName)}</strong><small>${esc(eligible.registeredSessionEvidenceCount)} sessioni REGISTERED · F5 method score ${esc(eligible.f5MethodValidationScore)}</small></article><article><span>UNVERIFIED FOR SETUP</span><strong>${esc(excluded.canonicalName)}</strong><small>${esc(excluded.reasonCode)}</small></article></div>
      <p><strong>Interpretazione:</strong> la compatibilità deriva da evidence storica di acquisizione con il setup selezionato. Non è ancora un modello di idoneità ottica e lo score F5 resta sintetico.</p></section>`;
  };
  const render=projection=>{
    host.innerHTML=`<section class="dsg-op-panel dsg-op-evidence"><div><span>F6 · REAL-EVIDENCE SETUP-AWARE E2E</span><h2>Forecast reale e setup governato nello stesso percorso read-only</h2><p>Il campione meteo proviene dall’evidence F4-C ItaliaMeteo/ARPAE già acquisita e riconciliata. F6 esegue <strong>0</strong> richieste provider aggiuntive e pubblica soltanto una projection sanitizzata.</p></div><span class="dsg-op-badge">EVALUATION · NONE</span></section>
      <section class="dsg-op-panel"><div class="dsg-op-panel__head"><div><span>REAL FORECAST SAMPLE</span><h2>${esc(projection.forecastEvidence.modelId)}</h2></div><small>budget ${esc(projection.forecastEvidence.providerRequestBudget)}</small></div>${weather(projection.weatherSample)}<p>Run ${esc(projection.forecastEvidence.runInitialisationUtc)} · validità ${esc(projection.forecastEvidence.validFromUtc)} → ${esc(projection.forecastEvidence.validToUtcExclusive)} · localizzazione <strong>generalizzata</strong>, non sito protetto.</p></section>
      <section class="dsg-op-panel"><span>SCENARIO SETUP</span><h2>Seleziona il profilo pubblico</h2><p><select data-f6-setup>${projection.setupScenarios.map((item,index)=>`<option value="${index}">${esc(item.setupLabel)}</option>`).join('')}</select></p><div data-f6-scenario></div></section>
      <section class="dsg-op-panel dsg-op-boundary"><span>AUTHORITY BOUNDARY</span><h2>Proof E2E, non raccomandazione operativa</h2><p>Il forecast è evidence reale ma non è ancora un feed runtime fresco del sito. La geometria/score F5 resta evidence sintetica di metodo e la compatibilità setup deriva dallo storico, non da un modello completo di suitability. Nessun readiness/go-no-go, scheduler, selezione automatica, comando o Safety Authority. Gli interlock fisici locali restano autorevoli; S10 resta <strong>UNAVAILABLE</strong>.</p></section>`;
    const select=host.querySelector('[data-f6-setup]');
    const scenarioHost=host.querySelector('[data-f6-scenario]');
    const paint=()=>{scenarioHost.innerHTML=scenarioMarkup(projection.setupScenarios[Number(select.value)]);};
    select.addEventListener('change',paint);
    paint();
  };
  fetch('../data/observation-planner-e2e-f6-projection.json',{cache:'no-store'})
    .then(response=>{if(!response.ok) throw new Error(`Projection F6 repository assente (HTTP ${response.status}).`); return response.json();})
    .then(projection=>{validate(projection);render(projection);})
    .catch(error=>fail(error.message));
}
