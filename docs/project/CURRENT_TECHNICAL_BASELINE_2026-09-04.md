# Digital StarGate — Current Technical Baseline — 2026-09-04

| Campo | Valore |
|---|---|
| Stato | Active technical baseline after BKL-030 closure |
| Scope | Reporting 1.0.8, AP-013 transport baseline, BKL-030 G1-G8, Cloud Run EAGLE Health, operational EAGLE publisher |
| BKL-030 closure merge | `eeba3372d8d788322f52553091f8d63cef5f9e68` |
| Next governed capability | BKL-015 Knowledge Graph machine-readable foundation |
| Does not supersede | ADR, Architecture Package, OAT storiche o decisioni approvate |

## 1. Finalità

Questa baseline registra lo stato tecnico verificato al termine di BKL-030 e costituisce il punto di partenza per BKL-015. Le baseline precedenti restano fotografie storiche valide.

## 2. Runtime scientifico EAGLE

`DigitalStarGate.Reporting 1.0.8` resta la baseline runtime scientifica EAGLE.

Runtime repository operativo:

`C:\DigitalStarGate\digital-stargate-manual-ap14-runtime`

Il runtime deve rimanere sul branch `main`, con working tree pulito. Prima di session import o modifiche operative verificare `HEAD == origin/main`. Worktree feature/OAT devono restare separati.

Questo vincolo è operativo: spostare il runtime principale su un branch feature può compromettere l'importazione automatica della sessione successiva.

## 3. BKL-030 final state

BKL-030 EAGLE Health & Reliability Telemetry è **CLOSED / ACCEPTED**, G1-G8 completati.

Baseline funzionale finale:

- collector host read-only;
- projection corrente atomica;
- history G6 append-only, duplicate-safe, senza retention distruttiva;
- public projection G7 filtrata;
- relay Cloud Run con canale separato `/v1/eagle-health`;
- portal `Observatory Status` consumer read-only;
- publisher EAGLE schedulato ogni minuto;
- G8 Safety Review approvata con boundary invariati.

Non esiste health severity policy approvata: `summary.state=UNKNOWN`, `summary.reason=POLICY_NOT_ACTIVATED`.

## 4. Scheduled Task EAGLE Health

Task operativo:

`DigitalStarGate-EagleHealthTelemetry`

Configurazione verificata:

- account `PrimaLuceLab`;
- S4U / Highest;
- ripetizione 1 minuto;
- `MultipleInstances=IgnoreNew`;
- execution wrapper `scripts/telemetry/Invoke-EagleHealthTelemetryPublish.ps1`;
- runtime repository `C:\DigitalStarGate\digital-stargate-manual-ap14-runtime`;
- DPAPI LocalMachine secret `C:\DigitalStarGate\TelemetryRuntime\secrets\ingest-token.dpapi`.

La projection pubblicata è stata osservata `CURRENT`, host `EAGLE30154`, `signals_published=5`, `automatic_remediation=false`, `safety_authority=OUTSIDE_SCOPE`.

## 5. Cloud Run / portal baseline

Service: `dsg-observatory-status-relay`, region `europe-west1`, project `digital-stargate-telemetry`.

Production revision verificata: `dsg-observatory-status-relay-00005-rof`.

Canali:

- `/v1/observatory-status` — contratto esistente;
- `/v1/eagle-health` — EAGLE Health.

Il browser non contiene ingest credential. L'outage cloud deve produrre evidence unavailable/stale senza influenzare N.I.N.A., Safety Authority o apparati.

## 6. Raw image transport baseline

AP-013B resta la baseline rollback `COPY_ONLY`:

`EAGLE raw -> OneDrive transport XISF + READY -> PC OneDrive -> DSG OneDrive Import -> F:\Astrofotografia`

AP-013C ha introdotto il percorso governato DRY_RUN/NO_DELETE e convergence/eligibility evidence senza autorizzare cancellazione produttiva.

Restano invarianti:

- source cleanup produttivo non autorizzato;
- transport cleanup produttivo non autorizzato salvo decisione separata;
- evidence incompleta/UNKNOWN => no-delete;
- `F:\Astrofotografia` non è cleanup target;
- ACK prova import verificato ma non autorizza da solo la cancellazione source.

## 7. Evidence EAGLE Health

I segnali CPU, memory, storage, uptime e time sync sono evidence. Non devono essere trasformati in severity senza policy approvata.

Storage C: ha mostrato capacità libera molto bassa durante le prove; il dato è operativo ma non equivale a CRITICAL nella baseline corrente.

Windows Time è stato osservato `Stopped`; nessuna remediation automatica è autorizzata.

## 8. Safety / security

- Safety Authority fisica/locale indipendente;
- health e portal non sono Safety Authority;
- nessun command endpoint;
- nessuna automatic remediation;
- token ingest solo server-side/publisher e protetto DPAPI sul runtime EAGLE;
- browser senza token;
- stale/missing/malformed evidence fail-closed;
- Cloud Run non entra nel path di controllo fisico.

## 9. Repository / governance baseline

BKL-030 G7 merge: `a15d85b27ebfbe8a6488330920d10dda8db79a78`.

BKL-030 G8/closure merge: `eeba3372d8d788322f52553091f8d63cef5f9e68`.

La roadmap governance dopo la closure indica BKL-015 come package successivo. Prima dell'avvio BKL-015 devono essere verdi i workflow dell'aggiornamento handover corrente.

## 10. Continuity

Documenti da leggere all'avvio di una nuova sessione:

1. `AI_BOOTSTRAP.md`;
2. `docs/project/HANDOVER_2026-09-04.md`;
3. `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-04.md`;
4. `docs/project/BACKLOG.md`;
5. `.github/roadmap/roadmap-source.json`;
6. review/evidence del package direttamente interessato.

## 11. Next gate — BKL-015

Il prossimo package governato è **BKL-015 Knowledge Graph machine-readable foundation**.

Il design dovrà partire da repository truth e preservare i boundary esistenti: Knowledge Graph e AI sono consumer/derivazioni di evidence governata, non Safety Authority e non command/remediation path. Observation, inference e recommendation devono restare distinguibili e tracciabili.
