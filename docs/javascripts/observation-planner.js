import { validateObservationPlannerProjection } from './observation-planner-core.mjs';

const host = document.querySelector('[data-observation-planner]');

if (host) {
  const esc = value => String(value ?? '').replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]);
  const labels = {
    targetAltitudeDeg: 'Altitudine target', targetAzimuthDeg: 'Azimut target', meridianTransitUtc: 'Transito al meridiano',
    solarAltitudeDeg: 'Altitudine Sole', moonAltitudeDeg: 'Altitudine Luna', moonAzimuthDeg: 'Azimut Luna',
    moonPhaseAngleDeg: 'Angolo di fase lunare', moonIlluminatedFraction: 'Frazione illuminata', targetMoonSeparationDeg: 'Separazione target–Luna'
  };
  const formatUtc = value => new Date(value).toLocaleString('it-IT', { dateStyle: 'medium', timeStyle: 'medium', timeZone: 'UTC' }) + ' UTC';
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
