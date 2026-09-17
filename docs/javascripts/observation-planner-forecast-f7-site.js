const host = document.querySelector('[data-observation-planner-site-forecast]');
const esc = value => String(value ?? '').replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]);
const fmtLocal = value => new Date(value).toLocaleString('it-IT', { timeZone: 'Europe/Rome', day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' });

if (host) {
  const forbidden = new Set(['latitude','longitude','latitudeDeg','longitudeDeg','elevation','elevationM','returnedGrid','returned_grid','siteAuthorityRef','rawResponseSha256','rawSha256','rawRequestUrl','requestUrl','safe','isSafe','readiness','goNoGo','scheduler','deviceCommand']);
  const inspect = (value, path = 'projection') => {
    if (!value || typeof value !== 'object') return;
    if (Array.isArray(value)) return value.forEach((child, index) => inspect(child, `${path}[${index}]`));
    for (const [key, child] of Object.entries(value)) {
      if (forbidden.has(key)) throw new Error(`${path}.${key} non autorizzato nella projection pubblica.`);
      inspect(child, `${path}.${key}`);
    }
  };
  const validate = projection => {
    if (!projection || typeof projection !== 'object' || Array.isArray(projection)) throw new Error('Projection F7 non valida.');
    if (projection.schemaVersion !== '1.0' || projection.projectionType !== 'BKL031_F7_PROTECTED_SITE_SANITIZED_FORECAST_PROJECTION') throw new Error('Identità projection F7 non valida.');
    if (projection.environment !== 'EVALUATION' || projection.authority !== 'NONE' || projection.publicationState !== 'READ_ONLY') throw new Error('Boundary pubblica F7 non valida.');
    if (projection.site?.publicLabel !== 'Manciano (GR), Italia' || projection.site?.coordinateDisclosure !== 'PROHIBITED') throw new Error('Policy sito pubblico F7 non valida.');
    if (projection.sourceEvidence?.workflowRunId !== 35255829165 || projection.sourceEvidence?.workflowHeadSha !== '2c46ca8be59c9ea8245fa03de71e936249c52a1b') throw new Error('Lineage protected-site F7 non valida.');
    if (projection.sourceEvidence?.acceptedHourlyInstantCount !== 71 || projection.sourceEvidence?.excludedHourlyInstantCount !== 1 || projection.sourceEvidence?.imputedValueCount !== 0) throw new Error('Completezza evidence F7 non valida.');
    if (projection.model?.modelId !== 'italia_meteo_arpae_icon_2i' || projection.model?.runInitialisationUtc !== '2026-09-17T12:00Z' || projection.model?.freshnessState !== 'FRESH') throw new Error('Modello/run/freschezza F7 non validi.');
    if (!Array.isArray(projection.forecast?.hourly) || projection.forecast.hourly.length !== 71) throw new Error('Serie forecast F7 incompleta.');
    if (projection.boundaries?.readinessAuthority !== false || projection.boundaries?.schedulingAuthority !== false || projection.boundaries?.automaticTargetSelection !== false || projection.boundaries?.commandAuthority !== 'NONE' || projection.boundaries?.safetyAuthority !== 'LOCAL_PHYSICAL_INTERLOCKS') throw new Error('Authority boundary F7 non valida.');
    const currentRunAgeHours = (Date.now() - Date.parse(projection.model.runInitialisationUtc)) / 3_600_000;
    if (!Number.isFinite(currentRunAgeHours) || currentRunAgeHours < 0 || currentRunAgeHours > projection.model.maxRunAgeHours) throw new Error('Forecast F7 non più fresco: nessun dato storico viene presentato come corrente.');
    inspect(projection);
    return projection;
  };
  const fail = message => {
    host.innerHTML = `<section class="dsg-op-panel dsg-op-fail" role="alert"><span>FAIL-CLOSED</span><h2>Forecast reale del sito non disponibile</h2><p>${esc(message)}</p><p>Nessun dato precedente, localizzazione sintetica o fallback viene mostrato come forecast corrente.</p></section>`;
  };
  const render = projection => {
    const from = Date.parse(projection.nightWindow.fromUtc);
    const to = Date.parse(projection.nightWindow.toUtcExclusive);
    const night = projection.forecast.hourly.filter(row => { const t = Date.parse(row.validAtUtc); return t >= from && t < to; });
    if (!night.length) throw new Error('La projection non contiene la finestra meteo della notte corrente.');
    const rows = night.map(row => `<tr><td>${esc(fmtLocal(row.validAtUtc))}</td><td>${row.temperatureC.toLocaleString('it-IT')} °C</td><td>${row.relativeHumidityPct}%</td><td>${row.dewPointC.toLocaleString('it-IT')} °C</td><td>${row.precipitationMm.toLocaleString('it-IT')} mm</td><td>${row.cloudCoverPct}%</td><td>${row.windSpeedKmh.toLocaleString('it-IT')} km/h</td><td>${row.windGustKmh.toLocaleString('it-IT')} km/h</td></tr>`).join('');
    host.innerHTML = `<section class="dsg-op-summary">
      <article><span>SITO</span><strong>${esc(projection.site.publicLabel)}</strong></article>
      <article><span>FRESCHEZZA</span><strong>${esc(projection.model.freshnessState)}</strong></article>
      <article><span>ORE VALIDE</span><strong>${projection.sourceEvidence.acceptedHourlyInstantCount}/72</strong></article>
      <article><span>STATO DATI</span><strong>${esc(projection.forecast.availabilityState)}</strong></article>
    </section>
    <section class="dsg-op-panel dsg-op-evidence"><div><span>F7 · REAL PROTECTED-SITE FORECAST</span><h2>Forecast meteo reale della notte</h2><p>Dati acquisiti lato server sulle coordinate governate dell'osservatorio; la pagina pubblica espone solo valori sanitizzati e il label generalizzato.</p></div><span class="dsg-op-badge">EVALUATION · NONE</span></section>
    <section class="dsg-op-panel dsg-op-lineage"><span>MODELLO E LINEAGE</span><div><p><strong>Modello</strong><br>${esc(projection.model.displayName)}</p><p><strong>Run</strong><br>${esc(fmtLocal(projection.model.runInitialisationUtc))}</p><p><strong>Recuperato</strong><br>${esc(fmtLocal(projection.model.retrievedAtUtc))}</p></div></section>
    <section class="dsg-op-panel"><div class="dsg-op-panel__head"><div><span>${esc(projection.nightWindow.label)}</span><h2>Dettaglio orario</h2></div><small>Europe/Rome</small></div><div style="overflow-x:auto"><table><thead><tr><th>Ora</th><th>Temp.</th><th>UR</th><th>Dew point</th><th>Pioggia</th><th>Nuvole</th><th>Vento</th><th>Raffiche</th></tr></thead><tbody>${rows}</tbody></table></div></section>
    <section class="dsg-op-panel dsg-op-boundary"><span>ATTRIBUZIONE E BOUNDARY</span><h2>Forecast informativo, nessuna autorità operativa</h2><p>${esc(projection.attribution)}</p><p>Il forecast è reale e riferito al sito governato, ma non costituisce readiness, go/no-go o Safety Authority. Le coordinate protette non sono pubblicate; gli interlock fisici locali restano l'autorità di sicurezza.</p></section>`;
  };
  fetch('../data/observation-planner-forecast-f7-site-projection.json', { cache: 'no-store' })
    .then(response => { if (!response.ok) throw new Error(`Projection forecast F7 assente (HTTP ${response.status}).`); return response.json(); })
    .then(projection => render(validate(projection)))
    .catch(error => fail(error.message));
}
