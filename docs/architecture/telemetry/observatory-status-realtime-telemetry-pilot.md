# Observatory Status Realtime Telemetry Pilot

| Campo | Valore |
|---|---|
| Identificativo | DSG-OBS-RT-001 |
| Versione | 0.2 |
| Stato | Runtime pilot validated; local continuous producer in commissioning |
| Data | 16/08/2026 |
| Target | Observatory Status read-only telemetry pilot |
| Dipendenze | AP-003; AP-004; AP-008; AP-010; AP-012 |

## 1. Scopo

Definire il primo vertical slice read-only per alimentare la pagina **Observatory Status** con telemetria operativa osservata sull'EAGLE, senza introdurre command path, safety authority remota o una tecnologia di transport non ancora validata.

Il pilot implementa il contratto `contracts/telemetry/observatory-status-v1.schema.json` e mantiene il portale come consumer read-only. Stato assente, stale o non verificabile resta `UNKNOWN`/`STALE`.

## 2. Current state verificato

- `docs/status/index.md` espone già una superficie Observatory Status.
- `docs/javascripts/observatory-status.js` consuma la projection `docs/data/realtime/observatory-status.json` e applica freshness lato browser.
- L'EAGLE fisico è il nodo di controllo centrale e ospita Windows, N.I.N.A., CPWI, PHD2 e ASCOM.
- Il runtime AP-014 ha verificato sul nodo `EAGLE30154` la sorgente CloudWatcher `C:\Users\PrimaLuceLab\Documents\CloudWatcher\CloudWatcher.csv`.
- Il CSV CloudWatcher reale contiene `Date`, `Time`, condizioni cloud/rain/brightness, temperatura ambiente, vento, umidità relativa, dew point, pressioni e `Safe Status`.
- Il commissioning DSG-OBS-RT-001 ha verificato lettura concorrente read-only del CSV mentre CloudWatcher lo mantiene aperto e lo aggiorna.
- Il cadence OAT del 16/08/2026 ha osservato 11 cambi in 300 s: media 28 s, P95 30 s, massimo 30 s. La freshness pilot approvata per il weather signal è quindi 60 s.
- La documentazione della cupola richiede sensori OPEN, CLOSED e SAFE, ma polarità, schema elettrico e interfaccia runtime restano `DA VALIDARE`.

## 3. Producer inventory

| Producer / capability | Interfaccia verificata | Stato pilot | Regola |
|---|---|---|---|
| CloudWatcher meteo | CSV locale condiviso su EAGLE | **Runtime verified** | adapter read-only, freshness 60 s |
| Cupola OPEN/CLOSED/SAFE | non verificata | Open issue | nessuna lettura fino a runtime inspection |
| Montatura CGX-L | ASCOM/CPWI capability; runtime contract non verificato | Open issue | no connessione concorrente al driver |
| Camera | status interface non verificata | Open issue | nessun polling diretto |
| Network Starlink/RUT955/VPN/LTE | management telemetry non verificata | Open issue | no credenziali o scraping non governato |
| Power / UPS | source interface non verificata | Open issue | `UNKNOWN` fino a evidence |

## 4. CloudWatcher adapter

`Export-CloudWatcherObservatoryStatus.ps1` apre il CSV con accesso `Read` e `FileShare.ReadWrite`, legge l'header e soltanto la coda recente del file, ignora record finali parziali/non parseabili e seleziona l'ultima osservazione completa. Non modifica CloudWatcher, non apre device connection e non invia comandi.

Campi governati:

- timestamp `Date` + `Time`;
- `Safe Status` -> weather `SAFE`, `UNSAFE` o `UNKNOWN`;
- condizioni raw diagnostiche `Cloud Condition`, `Rain Condition`, `Brightness Condition`, `Wind Condition`, `Switch Status`.

I campi numerici restano non normalizzati finché unità e semantica non sono deliberate da documentazione/evidence.

## 5. Freshness e qualità

Il cadence OAT fisico su `EAGLE30154` ha prodotto:

| Misura | Valore |
|---|---:|
| durata | 300 s |
| polling OAT | 5 s |
| cambi osservati | 11 |
| intervallo medio | 28 s |
| P95 | 30 s |
| massimo | 30 s |
| freshness weather pilot | **60 s** |

Regole:

1. `observed_at_utc` deriva dalla riga CloudWatcher;
2. `fresh_until_utc = observed_at_utc + 60 s` nel profilo pilot;
3. oltre freshness il weather diventa `STALE/UNKNOWN`;
4. payload complessivo resta `DEGRADED` quando il solo meteo è integrato, anche se CURRENT;
5. safety complessiva resta `UNKNOWN` finché la Local Safety Authority non è integrata separatamente;
6. `Safe Status = Safe` non equivale a overall observatory safety.

## 6. Producer continuo locale

`Start-ObservatoryStatusTelemetryProducer.ps1` implementa il primo producer continuo **locale**:

```text
CloudWatcher.csv
    -> shared tail read (15 s)
    -> Observatory Status v1 candidate
    -> validation invariants
    -> atomic replace
    -> C:\DigitalStarGate\TelemetryRuntime\observatory-status.json
```

Il producer usa polling 15 s e freshness 60 s. Scrive inoltre `producer-health.json` e `producer.log`. In caso di errore non sovrascrive la projection valida con un payload incompleto: elimina il candidate temporaneo, registra `DEGRADED` e lascia decadere naturalmente l'ultimo dato tramite freshness.

`DurationSeconds=0` indica esecuzione continua; per commissioning deve essere usata inizialmente una durata finita.

## 7. Transport boundary

Il producer locale **non** esegue `git push`, non contiene token e non pubblica direttamente verso GitHub Pages. Il transport tra `TelemetryRuntime\observatory-status.json` e il portale resta una decisione infrastrutturale separata.

Prima di introdurre un transport permanente devono essere deliberate almeno:

- autenticazione e secret handling;
- reachability EAGLE -> endpoint;
- rate limits e costo operativo;
- buffering/retry e comportamento offline;
- separazione tra repository documentation CI e realtime data plane;
- retention e audit dell'evidence.

## 8. Failure modes

| Scenario | Comportamento |
|---|---|
| CSV assente | producer DEGRADED; nessun falso dato |
| CSV locked da CloudWatcher | lettura condivisa supportata |
| record finale parziale | ignorato; usata ultima riga completa |
| header inatteso | candidate rifiutato |
| dato stale | `STALE/UNKNOWN` |
| `Safe Status` sconosciuto | weather `UNKNOWN` |
| producer arrestato | ultimo dato decade per freshness |
| transport/portale indisponibile | nessun impatto su CloudWatcher o safety locale |

## 9. Acceptance

Completato:

- source reale verificata su EAGLE30154;
- lettura concorrente read-only verificata;
- large-file streaming verificato;
- cadence OAT PASS;
- freshness 60 s derivata da evidence;
- safety/isolation invariants preservate;
- adapter compatibile con record finali parziali.

Da completare:

1. commissioning producer continuo locale per finestra finita;
2. validazione unità campi numerici;
3. runtime inspection OPEN/CLOSED/SAFE cupola;
4. ADR/decisione transport realtime verso il portale;
5. solo dopo questi gate, installazione persistente del producer.

## 10. Traceability

- `contracts/telemetry/observatory-status-v1.schema.json`
- `scripts/telemetry/Export-CloudWatcherObservatoryStatus.ps1`
- `scripts/telemetry/Invoke-CloudWatcherTelemetryPilot.ps1`
- `scripts/telemetry/Measure-CloudWatcherCadence.ps1`
- `scripts/telemetry/Start-ObservatoryStatusTelemetryProducer.ps1`
- `docs/architecture/packages/AP-004-Enterprise-Telemetry-and-Observability-Architecture.md`
- `docs/architecture/packages/AP-012-Enterprise-Operations-Center-Architecture.md`
- `docs/architecture/validation/AP14-W07-EAGLE-M27-OAT-Result.md`
