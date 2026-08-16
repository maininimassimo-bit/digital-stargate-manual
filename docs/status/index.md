# Observatory Status

> **Modalità read-only.** Questa pagina visualizza osservazioni operative e non costituisce Safety Authority né un canale di comando. Dati assenti o scaduti sono mostrati come `UNKNOWN`; l'ultimo valore noto non viene interpretato come stato corrente.

<div class="dsg-kpi-grid">
<div class="dsg-kpi"><span class="dsg-kpi__label">Qualità telemetria</span><span class="dsg-kpi__value" data-observatory-status="quality">🟡 UNKNOWN</span><span class="dsg-kpi__detail">Rilevazione: <span data-observatory-status="observed-at">—</span> · sorgente: <span data-observatory-status="source">—</span></span></div>
<div class="dsg-kpi"><span class="dsg-kpi__label">Sicurezza meteo osservata</span><span class="dsg-kpi__value" data-observatory-status="weather-state">🟡 UNKNOWN</span><span class="dsg-kpi__detail">Telemetria, non autorità safety</span></div>
<div class="dsg-kpi"><span class="dsg-kpi__label">Cupola osservata</span><span class="dsg-kpi__value" data-observatory-status="dome-state">🟡 UNKNOWN</span><span class="dsg-kpi__detail" data-observatory-status="dome-detail">OPEN: — · CLOSED: — · SAFE: —</span></div>
<div class="dsg-kpi"><span class="dsg-kpi__label">Montatura osservata</span><span class="dsg-kpi__value" data-observatory-status="mount-state">🟡 UNKNOWN</span><span class="dsg-kpi__detail" data-observatory-status="mount-detail">parked: — · tracking: —</span></div>
<div class="dsg-kpi"><span class="dsg-kpi__label">Rete osservata</span><span class="dsg-kpi__value" data-observatory-status="network-state">🟡 UNKNOWN</span><span class="dsg-kpi__detail" data-observatory-status="network-detail">link: — · VPN: — · LTE: —</span></div>
</div>

## Meteo operativo

| Parametro | Valore |
|---|---|
| Temperatura | <span data-observatory-status="weather-temperature">—</span> |
| Umidità | <span data-observatory-status="weather-humidity">—</span> |
| Dew point | <span data-observatory-status="weather-dew-point">—</span> |
| Vento | <span data-observatory-status="weather-wind">—</span> |
| Raffiche | <span data-observatory-status="weather-gust">—</span> |
| Pioggia | <span data-observatory-status="weather-rain">—</span> |
| Pressione | <span data-observatory-status="weather-pressure">—</span> |
| SQM | <span data-observatory-status="weather-sqm">—</span> |
| Temperatura cielo | <span data-observatory-status="weather-sky-temperature">—</span> |
| Stato osservato | <span data-observatory-status="weather-state">🟡 UNKNOWN</span> |

## Stato sistemi osservato

| Sistema | Stato | Dettaglio |
|---|---|---|
| Cupola | <span data-observatory-status="dome-state">🟡 UNKNOWN</span> | <span data-observatory-status="dome-detail">OPEN: — · CLOSED: — · SAFE: —</span> |
| Montatura | <span data-observatory-status="mount-state">🟡 UNKNOWN</span> | <span data-observatory-status="mount-detail">parked: — · tracking: —</span> |
| Camera | <span data-observatory-status="camera-state">🟡 UNKNOWN</span> | <span data-observatory-status="camera-detail">cooling: — · —</span> |
| Alimentazione | <span data-observatory-status="power-state">🟡 UNKNOWN</span> | <span data-observatory-status="power-detail">UPS su batteria: —</span> |
| Rete | <span data-observatory-status="network-state">🟡 UNKNOWN</span> | <span data-observatory-status="network-detail">link: — · VPN: — · LTE: —</span> |

## Contratto e freshness

Il browser aggiorna la projection read-only ogni 15 secondi. Ogni segnale contiene `observed_at_utc`, `fresh_until_utc` e `quality`. Se `fresh_until_utc` è superato, la UI forza lo stato a `UNKNOWN`/`STALE` invece di mostrare l'ultimo valore come corrente.

La projection pubblicata non è una fonte primaria: il producer runtime dovrà essere un adapter governato conforme ad AP-004/AP-008 e dovrà preservare l'autorità degli interlock locali AP-010.

## Ultima sessione scientifica

La telemetria realtime è deliberatamente separata dalla storia scientifica. Per sessioni, target, integrazione, guiding e report utilizzare **Session Reports** e **Scientific Platform**: quei dati sono proiezioni storiche versionate e non descrivono lo stato corrente dell'osservatorio.
