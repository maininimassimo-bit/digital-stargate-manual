# BKL-030 G5 — EAGLE Runtime OAT — 2026-09-03

| Campo | Valore |
|---|---|
| Identificativo | BKL-030-G5-OAT-2026-09-03 |
| Stato | PASS WITH OPEN OPERATIONAL RISKS |
| Host | EAGLE30154 |
| Repository baseline | `7ad244953f95adae4caecb5d1de60ee01b91f792` |
| Collector | `DSG.EagleHostHealthCollector` |
| Projection | `%LOCALAPPDATA%\DigitalStarGate\telemetry\eagle-health.json` |
| Authority | Read-only telemetry; not Safety Authority |

## 1. Scopo

Registrare l'Operational Acceptance Test runtime del collector host-side BKL-030 su EAGLE30154 dopo G1-G4, senza attivazione permanente di Scheduled Task o servizio e senza remediation automatica.

## 2. Precondizioni verificate

- runtime clone su branch `main`;
- working tree clean;
- `HEAD == origin/main`;
- baseline finale OAT `7ad244953f95adae4caecb5d1de60ee01b91f792`;
- sessione astronomica reale in corso durante il test FAST, con N.I.N.A. e PHD2 attivi;
- collector in modalità `READ_ONLY`;
- `automatic_remediation = false`;
- non-overlap `MUTEX_SKIP`;
- timeout per-probe configurato a 10 secondi.

## 3. G5-A FAST — PASS

Projection prodotta correttamente con:

- `schema_version = 1.0`;
- `component = DSG.EagleHostHealthCollector`;
- `computer = EAGLE30154`;
- `quality = CURRENT`;
- `cadence_class = FAST`.

Segnali `cpu`, `memory`, `processes` e `plugin_heartbeat` sono risultati `OBSERVED/CURRENT`.

Processi osservati durante workload reale:

- N.I.N.A. running;
- PHD2 running;
- AAG CloudWatcher running;
- ASCOM.TS_Shelter running.

Il test conferma che il collector può produrre telemetry FAST durante una sessione reale senza introdurre controllo device o remediation.

## 4. G5-B MEDIUM — PASS

Segnali `storage`, `uptime`, `time_sync`, `usb_com` e `log_sources` sono risultati `OBSERVED/CURRENT`.

### 4.1 Storage capacity

| Volume | Size | Free | Free % |
|---|---:|---:|---:|
| C: `EAGLE3` | 223,397,015,552 B | 672,124,928 B | 0.301% |
| D: `Volume` | 735,304,478,720 B | 355,526,217,728 B | 48.351% |

Il volume C: è quindi un **operational capacity risk candidate**. Non viene assegnata severity HEALTHY/DEGRADED/CRITICAL perché la relativa policy non è ancora governata.

### 4.2 Physical storage

SSD osservato:

- `KINGSTON SA400S37960G`;
- media type `SSD`;
- bus `SATA`;
- `HealthStatus = Healthy`;
- `OperationalStatus = OK`.

I reliability counter dettagliati/SMART non sono disponibili nella baseline non-elevated e restano esplicitamente `UNAVAILABLE_UNLESS_SEPARATELY_VERIFIED`.

### 4.3 Time, USB e uptime

- Windows Time service osservato `Stopped`; nessuna remediation autorizzata;
- uptime correttamente acquisito;
- inventario COM/PnP acquisito con stato `OK` per le porte osservate.

## 5. G5-C SLOW_ON_CHANGE — PASS

Segnali finali:

- `scheduled_tasks = OBSERVED/CURRENT`;
- `pending_reboot = OBSERVED/CURRENT`;
- `windows_update = OBSERVED/CURRENT`;
- `event_log = OBSERVED/CURRENT`;
- `configuration_drift = UNKNOWN/UNKNOWN`, reason `BASELINE_NOT_APPROVED`, come previsto dal contratto.

### 5.1 Event Log runtime defect e remediation software

Il primo OAT SLOW ha mostrato `event_log = UNAVAILABLE/UNKNOWN` quando la query bounded non trovava eventi Level 1/2. La diagnosi diretta su EAGLE ha confermato che non era un problema di accesso: `Get-WinEvent` restituiva `NoMatchingEventsFound` per una finestra valida ma vuota.

Sono stati corretti due aspetti incrementali:

1. empty-window semantic: zero eventi è un'osservazione valida, non un errore;
2. PowerShell runspace error-stream semantic: `NoMatchingEventsFound` rimaneva nello stream del runspace e veniva reinterpretato dal bounded wrapper come failure.

La correzione finale introduce una whitelist esplicita di benign error IDs per il solo probe Event Log; altri errori continuano a degradare il probe.

Merge rilevanti:

- PR #83: empty Event Log window contract;
- PR #84: bounded-probe handling di `NoMatchingEventsFound*`;
- baseline finale: `7ad244953f95adae4caecb5d1de60ee01b91f792`.

Rerun finale su EAGLE:

- `event_log.state = OBSERVED`;
- `event_log.quality = CURRENT`;
- `cadence_class = SLOW_ON_CHANGE`;
- `reason = null`;
- finestra osservata `2026-09-03T21:57:21.928Z` — `2026-09-03T22:57:21.928Z`;
- `event count = 0`.

Questo chiude il finding G5-C.

## 6. Scheduled Tasks / reboot / update evidence

Durante OAT:

- `Digital StarGate - Daily Session Upload` risultava Ready con ultimo `LastTaskResult = 1` dalla precedente esecuzione già investigata;
- `Digital StarGate - OneDrive Export` risultava Ready con `LastTaskResult = 0`;
- CBS reboot pending = false;
- Windows Update reboot required = false;
- `PendingFileRenameOperations` presente;
- `reboot_required` non inferito perché la policy di sintesi non è attiva;
- `wuauserv` osservato `Stopped`.

Nessun servizio è stato avviato/arrestato e nessuna chiave di registro è stata modificata.

## 7. Safety e failure containment

G5 conferma i seguenti invarianti:

- collector host-side separato dal plug-in N.I.N.A.;
- nessun controllo N.I.N.A./PHD2/device/power/network;
- nessuna automatic remediation;
- nessun ruolo di Safety Authority;
- timeout bounded per probe;
- failure isolation per singolo segnale;
- non-overlap via mutex;
- projection atomica e preservazione della precedente projection valida;
- UNKNOWN/UNAVAILABLE resta esplicito quando la source non può essere verificata.

## 8. Esito G5

**G5 Runtime OAT = COMPLETE / PASS WITH OPEN OPERATIONAL RISKS.**

I rischi aperti non invalidano il collector ma devono essere governati separatamente:

1. capacità C: estremamente ridotta (0.301% libero al momento del test);
2. Windows Time service `Stopped`;
3. `PendingFileRenameOperations` presente;
4. detailed SMART/reliability non disponibile non-elevated;
5. configuration drift non attivo finché il baseline manifest non è approvato;
6. severity/health thresholds ancora `POLICY_NOT_ACTIVATED`.

## 9. Prossimo passo

G6: progettare e implementare la persistenza/history della telemetry EAGLE mantenendo separazione tra current projection e storico, senza introdurre severity policy o Safety Authority implicita.
