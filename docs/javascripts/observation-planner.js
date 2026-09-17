import { validateObservationPlannerProjection } from './observation-planner-core.mjs';

const host = document.querySelector('[data-observation-planner]');
const forecastHost = document.querySelector('[data-observation-planner-forecast]');
const esc = value => String(value ?? '').replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]);
const formatUtc = value => new Date(value).toLocaleString('it-IT', { dateStyle: 'medium', timeStyle: 'medium', timeZone: 'UTC' }) + ' UTC';

if (host) {
  const labels = {
    targetAltitudeDeg: 'Altitudine target', targetAzimuthDeg: 'Azimut target', meridianTransitUtc: 'Transito al meridiano',
    solarAltitudeDeg: 'Altitudine Sole', moonAltitudeDeg: 'Altitudine Luna', moonAzimuthDeg: 'Azimut Luna',
    moonPhaseAngleDeg: 'Angolo di fase lunare', moonIlluminatedFraction: 'Frazione illuminata', targetMoonSeparationDeg: 'Separazione target–Luna'
  };
  const formatFact = fact => {
    if (fact.unit === 'utc') return formatUtc(fact.instantValue);
    const value = Number(fact.numericValue).toLocaleString('it-IT', { maximumFractionDigits: 4 });
    if (fact.unit === 'fraction') return `${value} (${(Number(fact.numericValue) * 100).toLocaleString('it-IT', { maximumFractionDigits: 1 })}%)`;
    return `${value}°`;
  };
  const fail = message => {
    host.innerHTML = `<section class="dsg-op-panel dsg-op-fail" role="alert"><span>FAIL-CLOSED</span><h2>Projection Observation Planner non disponibile</h2><p>${esc(message)}</p><p>Nessun dato precedente o calcolo alternativo viene sostituito.</p></section>`;
  };
  const render = projection => {
    host.innerHTML = `<section class="dsg-op-summary">
      <article><span>STATO DATI</span><strong>${esc(projection.evidenceAvailabilityState)}</strong></article>
      <article><span>SETUP</span><strong>${esc(projection.setupAvailabilityState)}</strong></article>
      <article><span>RUNTIME S10</span><strong>${esc(projection.boundary.runtimeState)}</strong></article>
      <article><span>FATTI PUBBLICATI</span><strong>${projection.facts.length}</strong></article>
    </section>
    <section class="dsg-op-panel dsg-op-evidence"><div><span>F3-C · BOUNDED SANITIZED PROJECTION</span><h2>Evidence sintetica verificata</h2><p>Adapter <code>${esc(projection.method.adapterId)}@${esc(projection.method.adapterVersion)}</code> · metodo <code>${esc(projection.method.methodId)}</code> · profilo <code>${esc(projection.method.profileRef)}</code>.</p></div><span class="dsg-op-badge">TEST · NONE</span></section>
    <section class="dsg-op-panel"><div class="dsg-op-panel__head"><div><span>FATTI NORMALIZZATI</span><h2>Geometria e contesto lunare</h2></div><small>Istante evidence: ${esc(formatUtc(projection.facts[0].instantUtc))}</small></div><div class="dsg-op-facts">${projection.facts.map(fact => `<article><span>${esc(labels[fact.factType] || fact.factType)}</span><strong>${esc(formatFact(fact))}</strong><small>${esc(fact.factType)}</small></article>`).join('')}</div></section>
    <section class="dsg-op-panel dsg-op-lineage"><span>LINEAGE E VALIDITÀ</span><div><p><strong>Riferimento sito pubblico</strong><br><code>${esc(projection.sitePublicEvidenceRef)}</code></p><p><strong>Validità evidence</strong><br>${esc(formatUtc(projection.validity.fromUtc))} → ${esc(formatUtc(projection.validity.toUtc))}</p><p><strong>Projection digest</strong><br><code>${esc(projection.projectionDigest.slice(0, 20))}…</code></p></div></section>
    <section class="dsg-op-panel dsg-op-boundary"><span>AUTHORITY BOUNDARY</span><h2>Integrazione sintetica, nessuna pianificazione operativa</h2><p>La pagina dimostra adapter e proiezione sanificata su evidence TEST. Non usa il sito protetto, non effettua chiamate esterne e non produce forecast, ranking, readiness o comandi. S10 runtime resta <strong>UNAVAILABLE</strong>; la Safety Authority resta agli interlock fisici locali.</p></section>`;
  };

  fetch('../data/observation-planner-ephemeris-lunar-f3c-projection.json', { cache: 'no-store' })
    .then(response => { if (!response.ok) throw new Error(`Projection repository assente (HTTP ${response.status}).`); return response.json(); })
    .then(async projection => { await validateObservationPlannerProjection(projection); render(projection); })
    .catch(error => fail(error.message));
}

if (forecastHost) {
  const allowedRoot = new Set(['schemaVersion','projectionType','projectionId','environment','authority','publicationState','sourceEvidence','model','validity','variables','excludedInstants','normalizationPolicy','attribution','citations','limitations']);
  const forbidden = new Set(['latitudeDeg','longitudeDeg','elevationM','returnedGrid','rawResponseSha256','artifactId','requestId','requestRef','siteAuthorityRef','forecastInstantsUtc','series','score','rank','ranking','readiness','goNoGo','safe','isSafe','scheduler','command','deviceCommand','safetyAuthority']);
  const inspect = (value, path='projection') => {
    if (!value || typeof value !== 'object') return;
    if (Array.isArray(value)) return value.forEach((child,index)=>inspect(child,`${path}[${index}]`));
    for (const [key,child] of Object.entries(value)) {
      if (forbidden.has(key)) throw new Error(`${path}.${key} non autorizzato nella projection pubblica.`);
      inspect(child,`${path}.${key}`);
    }
  };
  const validate = projection => {
    if (!projection || typeof projection !== 'object' || Array.isArray(projection)) throw new Error('Projection forecast non valida.');
    if (Object.keys(projection).some(key=>!allowedRoot.has(key)) || [...allowedRoot].some(key=>!Object.hasOwn(projection,key))) throw new Error('Projection forecast con proprietà inattese o mancanti.');
    if (projection.schemaVersion !== '1.0' || projection.projectionType !== 'BKL031_F4D_SANITIZED_FORECAST_PROJECTION') throw new Error('Identità F4-D non valida.');
    if (projection.environment !== 'EVALUATION' || projection.authority !== 'NONE' || projection.publicationState !== 'READ_ONLY') throw new Error('Boundary F4-D non valida.');
    if (projection.sourceEvidence.workflowRunId !== 35214129960 || projection.sourceEvidence.evidenceDigest !== '350a7b9ae8b2de308ba55a7105e56bb4de5040572370ab2715c0fa70088af2f5') throw new Error('Lineage F4-C non valida.');
    if (projection.sourceEvidence.acceptedHourlyInstantCount !== 71 || projection.sourceEvidence.excludedHourlyInstantCount !== 1 || projection.sourceEvidence.imputedValueCount !== 0) throw new Error('Riconciliazione F4-C non valida.');
    if (projection.model.modelId !== 'italia_meteo_arpae_icon_2i' || projection.model.runInitialisationUtc !== '2026-09-17T00:00:00Z') throw new Error('Modello o run F4-D non validi.');
    const visibility=projection.variables.find(item=>item.id==='visibility');
    if (!visibility || visibility.availability !== 'UNAVAILABLE') throw new Error('Indisponibilità visibility non preservata.');
    if (projection.excludedInstants.length !== 1 || projection.excludedInstants[0].validAtUtc !== '2026-09-17T00:00:00Z') throw new Error('Istante escluso non preservato.');
    inspect(projection);
    return true;
  };
  const fail = message => { forecastHost.innerHTML = `<section class="dsg-op-panel dsg-op-fail" role="alert"><span>FAIL-CLOSED</span><h2>Contesto forecast non disponibile</h2><p>${esc(message)}</p><p>Nessun dato precedente, provider call o fallback viene utilizzato.</p></section>`; };
  const render = projection => {
    const visibility=projection.variables.find(item=>item.id==='visibility');
    const excluded=projection.excludedInstants[0];
    forecastHost.innerHTML = `<section class="dsg-op-summary">
      <article><span>MODELLO</span><strong>${esc(projection.model.displayName)}</strong></article>
      <article><span>RUN UTC</span><strong>${esc(formatUtc(projection.model.runInitialisationUtc))}</strong></article>
      <article><span>ORE COMPLETE</span><strong>${projection.sourceEvidence.acceptedHourlyInstantCount}/72</strong></article>
      <article><span>VISIBILITY</span><strong>${esc(visibility.availability)}</strong></article>
    </section>
    <section class="dsg-op-panel dsg-op-evidence"><div><span>F4-D · SANITIZED FORECAST PROJECTION</span><h2>Contesto previsionale read-only</h2><p>Evidence riconciliata <code>${esc(projection.sourceEvidence.evidenceId)}</code> · workflow run <code>${projection.sourceEvidence.workflowRunId}</code>.</p></div><span class="dsg-op-badge">EVALUATION · NONE</span></section>
    <section class="dsg-op-panel dsg-op-lineage"><span>RUN E VALIDITÀ</span><div><p><strong>Run inizializzazione</strong><br>${esc(formatUtc(projection.model.runInitialisationUtc))}</p><p><strong>Validità</strong><br>${esc(formatUtc(projection.validity.fromUtc))} → ${esc(formatUtc(projection.validity.toUtcExclusive))} esclusivo</p><p><strong>Normalizzazione</strong><br><code>${esc(projection.normalizationPolicy)}</code></p></div></section>
    <section class="dsg-op-panel"><div class="dsg-op-panel__head"><div><span>COMPLETEZZA</span><h2>71 istanti completi, zero imputazioni</h2></div><small>1 istante escluso</small></div><p>L'istante ${esc(formatUtc(excluded.validAtUtc))} è escluso perché manca <code>${esc(excluded.missingVariables.join(', '))}</code> (${esc(excluded.reasonCode)}). Nessun valore è stato imputato.</p><p><strong>Visibility:</strong> ${esc(visibility.availability)} per ICON-2I; nessun fallback o modello alternativo.</p></section>
    <section class="dsg-op-panel dsg-op-boundary"><span>ATTRIBUZIONE E BOUNDARY</span><h2>Nessuna decisione operativa</h2><p>${esc(projection.attribution)}</p><p>Questa projection pubblica metadata e disponibilità soltanto. Non pubblica coordinate o serie previsionali, non contatta il provider, non produce ranking, readiness, go/no-go, comandi o Safety Authority. S10 runtime resta <strong>UNAVAILABLE</strong>.</p></section>`;
  };
  fetch('../data/observation-planner-forecast-f4d-projection.json', { cache: 'no-store' })
    .then(response=>{ if(!response.ok) throw new Error(`Projection forecast repository assente (HTTP ${response.status}).`); return response.json(); })
    .then(projection=>{ validate(projection); render(projection); })
    .catch(error=>fail(error.message));
}
