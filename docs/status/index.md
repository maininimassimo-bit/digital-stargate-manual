# Observatory Status

> **Modalità read-only.** Questa pagina visualizza osservazioni operative e non costituisce Safety Authority né un canale di comando. Dati assenti o scaduti sono mostrati come `UNKNOWN`; l'ultimo valore noto non viene interpretato come stato corrente.

> **Hosted telemetry pilot.** Il browser tenta prima il relay HTTPS governato su Google Cloud Run e non contiene credenziali di ingest. Se il relay non è raggiungibile, usa la projection statica del portale solo come fallback; freshness e stato `UNKNOWN` continuano a essere applicati lato browser.

<div class="dsg-kpi-grid">
<div class="dsg-kpi"><span class="dsg-kpi__label">Qualità telemetria</span><span class="dsg-kpi__value" data-observatory-status="quality">🟡 UNKNOWN</span><span class="dsg-kpi__detail">Rilevazione: <span data-observatory-status="observed-at">—</span> · sorgente: <span data-observatory-status="source">—</span> · trasporto: <span data-observatory-status="transport">—</span></span></div>
<div class="dsg-kpi"><span class="dsg-kpi__label">Safety osservata</span><span class="dsg-kpi__value" data-observatory-status="safety-state">🟡 UNKNOWN</span><span class="dsg-kpi__detail" data-observatory-status="safety-detail">Telemetria N.I.N.A., non autorità safety</span></div>
<div class="dsg-kpi"><span class="dsg-kpi__label">Meteo disponibile</span><span class="dsg-kpi__value" data-observatory-status="weather-state">🟡 UNKNOWN</span><span class="dsg-kpi__detail">Disponibilità della telemetria meteo N.I.N.A.</span></div>
<div class="dsg-kpi"><span class="dsg-kpi__label">Cupola osservata</span><span class="dsg-kpi__value" data-observatory-status="dome-state">🟡 UNKNOWN</span><span class="dsg-kpi__detail" data-observatory-status="dome-detail">Shutter: —</span></div>
<div class="dsg-kpi"><span class="dsg-kpi__label">Montatura osservata</span><span class="dsg-kpi__value" data-observatory-status="mount-state">🟡 UNKNOWN</span><span class="dsg-kpi__detail" data-observatory-status="mount-detail">parked: — · tracking: —</span></div>
<div class="dsg-kpi"><span class="dsg-kpi__label">Camera osservata</span><span class="dsg-kpi__value" data-observatory-status="camera-state">🟡 UNKNOWN</span><span class="dsg-kpi__detail" data-observatory-status="camera-detail">cooler: — · temperatura: —</span></div>
</div>

## Meteo operativo

| Parametro | Valore |
|---|---|
| Disponibilità | <span data-observatory-status="weather-state">🟡 UNKNOWN</span> |
| Temperatura | <span data-observatory-status="weather-temperature">—</span> |
| Umidità | <span data-observatory-status="weather-humidity">—</span> |
| Dew point | <span data-observatory-status="weather-dew-point">—</span> |
| Vento | <span data-observatory-status="weather-wind">—</span> |
| Raffiche | <span data-observatory-status="weather-gust">—</span> |
| Pioggia | <span data-observatory-status="weather-rain">—</span> |
| Pressione | <span data-observatory-status="weather-pressure">—</span> |
| Nuvolosità | <span data-observatory-status="weather-cloud-cover">—</span> |
| SQM | <span data-observatory-status="weather-sqm">—</span> |
| Temperatura cielo | <span data-observatory-status="weather-sky-temperature">—</span> |

## Stato sistemi osservato

| Sistema | Stato | Dettaglio |
|---|---|---|
| Safety Monitor | <span data-observatory-status="safety-state">🟡 UNKNOWN</span> | <span data-observatory-status="safety-detail">Telemetria N.I.N.A., non autorità safety</span> |
| Cupola | <span data-observatory-status="dome-state">🟡 UNKNOWN</span> | <span data-observatory-status="dome-detail">Shutter: —</span> |
| Montatura | <span data-observatory-status="mount-state">🟡 UNKNOWN</span> | <span data-observatory-status="mount-detail">parked: — · tracking: —</span> |
| Camera | <span data-observatory-status="camera-state">🟡 UNKNOWN</span> | <span data-observatory-status="camera-detail">cooler: — · temperatura: —</span> |
| Alimentazione | <span data-observatory-status="power-state">🟡 UNKNOWN</span> | <span data-observatory-status="power-detail">Sorgente verificata non ancora integrata</span> |
| Rete | <span data-observatory-status="network-state">🟡 UNKNOWN</span> | <span data-observatory-status="network-detail">Sorgente verificata non ancora integrata</span> |

## Contratto e freshness

Il browser aggiorna la projection read-only ogni 15 secondi. Ogni segnale contiene `observed_at_utc`, `fresh_until_utc` e `quality`. Se `fresh_until_utc` è superato, la UI forza lo stato a `UNKNOWN`/`STALE` invece di mostrare l'ultimo valore come corrente.

`weather.state` descrive la disponibilità della telemetria meteo (`AVAILABLE` quando corrente); non deve essere interpretato come verdetto di sicurezza. L'osservazione Safety è esposta separatamente tramite `safety.observed_state` e `safety.authority`. Anche tale osservazione resta informativa: gli interlock fisici locali mantengono l'autorità.

Il relay hosted espone soltanto lettura pubblica della projection e ingest autenticato separato. Il token di ingest resta fuori dal browser. Il filesystem locale del container Cloud Run è considerato storage transitorio per il pilot: la persistenza durevole e il comportamento di recovery dopo sostituzione istanza devono essere chiusi prima del cutover production-grade.

La projection pubblicata non è una fonte primaria: il producer runtime è un adapter governato e deve preservare l'autorità degli interlock locali; il portale non eleva mai la telemetria a Safety Authority.

## Ultima sessione scientifica

La telemetria realtime è deliberatamente separata dalla storia scientifica. Per sessioni, target, integrazione, guiding e report utilizzare **Session Reports** e **Scientific Platform**: quei dati sono proiezioni storiche versionate e non descrivono lo stato corrente dell'osservatorio.
