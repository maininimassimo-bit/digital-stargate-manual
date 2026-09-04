# Digital StarGate — Current Technical Baseline — 2026-09-04

| Campo | Valore |
|---|---|
| Stato | Active technical delta baseline |
| Scope | Reporting 1.0.8, BKL-030 G1–G5, raw transport AP-013B recovery, AP-013C preparation |
| Supersedes | `CURRENT_TECHNICAL_BASELINE_2026-09-03.md` per lo stato operativo corrente |
| Does not supersede | Principi, boundary, ADR, Architecture Package, OAT storiche o decisioni approvate |

## 1. Finalità

Questa baseline registra lo stato tecnico verificato al 04/09/2026. Le baseline precedenti restano fotografie storiche valide.

## 2. Reporting e scientific session producer

`DigitalStarGate.Reporting 1.0.8` resta la baseline runtime EAGLE. Restano validi il contratto PowerShell 5.1, exact evidence selection NINA/PHD2 e SQM packaging descritti nella baseline del 03/09.

La sessione `2026-09-03_2026-09-04` è stata promossa e le analytics sono state aggiornate su `main`; HEAD verificato prima del package: `ffc2e2cc719336ea6e4134884017a94f811ce08f`.

Il launcher restore-to-main su eccezione resta un hardening separato già tracciato; non è modificato da questo package.

## 3. BKL-030 current state

BKL-030 EAGLE Health & Reliability è `In Progress`, G1–G5 complete. Il G5 Runtime OAT ha verificato collector read-only e projection per FAST, MEDIUM e SLOW_ON_CHANGE. Event Log empty-window è stato corretto e verificato `OBSERVED/CURRENT` con array eventi vuoto.

Evidence operativa rilevante:

- C: osservato a 672,124,928 byte liberi / 0.301% durante G5;
- nessuna severity numerica derivata perché non esiste threshold approvato;
- Windows Time osservato `Stopped`;
- `PendingFileRenameOperations` presente;
- configuration drift `UNKNOWN/BASELINE_NOT_APPROVED`;
- SMART dettagliato non verificato nel contesto non-elevated.

Next BKL-030 gate: G6 history/persistence.

## 4. Raw image transport baseline

La baseline raw transport resta AP-013B in modalità `COPY_ONLY`:

`EAGLE raw -> OneDrive transport XISF + READY -> PC OneDrive -> DSG OneDrive Import -> F:\Astrofotografia`

Nella baseline corrente non è autorizzata la cancellazione automatica di source EAGLE o transport artifacts come effetto dell'import. AP-013B resta il rollback comportamentale durante l'evoluzione successiva.

## 5. OneDrive incident/recovery 04/09

È stato osservato un disallineamento del transport dopo gestione Files On-Demand sul lato EAGLE:

- EAGLE: 445 XISF / 445 READY;
- PC inizialmente: 426 XISF / 426 READY;
- gap: 19 coppie, M 27 `0123–0141`.

L'importer PC non aveva failure: i manifest non ancora convergenti non erano visibili al consumer. Restart semplice del client EAGLE non ha risolto. Dopo reset controllato dello stato OneDrive e verifica dell'account `Business1`, il PC ha raggiunto 445/445 e il probe di sincronizzazione è diventato visibile.

La verifica finale su `F:\Astrofotografia` ha confermato tutti i 19 XISF `0123–0141`. L'evidence importer successiva ha osservato 445 READY, tutti già importati, con zero failure e zero cancellazioni.

## 6. Conseguenza architetturale

La recovery dimostra che `file prodotto su EAGLE`, `file presente nel transport locale`, `file convergente nel cloud/PC` e `file verificato nella destinazione finale` sono stati distinti nella pratica e non devono essere collassati in un singolo stato.

Per questo AP-013C deve introdurre un lifecycle/evidence contract end-to-end prima di autorizzare cleanup automatico.

## 7. AP-013C design baseline

AP-013C è approvato per progettazione, non ancora per cancellazione produttiva.

Obiettivi:

- ridurre crescita del disco C: EAGLE;
- preservare data integrity e recoverability;
- rendere osservabile la convergenza end-to-end;
- rendere la cancellazione fail-closed, idempotente e auditabile.

Stati logici minimi da modellare nella progettazione:

`PRODUCED -> TRANSPORT_READY -> CONVERGED/OBSERVED -> DESTINATION_VERIFIED -> CLEANUP_ELIGIBLE -> CLEANED`

I nomi finali e la macchina a stati devono essere formalizzati nell'Architecture Package; non sono ancora un contratto implementativo approvato.

## 8. Cleanup guardrails

Un file non può essere cancellato dalla source EAGLE per il solo fatto di essere stato esportato nel transport. L'eleggibilità richiede evidence verificabile della destinazione prevista e coerenza con il relativo READY/provenance.

Retention interval, timeout, retry, hash policy, manifest retention, cleanup del transport OneDrive e ordine source-vs-transport sono decisioni ancora aperte da formalizzare in AP-013C.

## 9. Files On-Demand

Files On-Demand resta una funzione di gestione storage del client OneDrive e non costituisce il lifecycle applicativo Digital StarGate. Non usare indiscriminatamente `Always keep on this device` sul transport EAGLE: il capacity risk osservato richiede che la soluzione riduca, non aumenti, la pressione sul disco C:.

## 10. Safety boundary

Invariati:

- local physical Safety Authority indipendente;
- transport, cleanup, telemetry, health e AI non sono Safety Authority;
- nessun cleanup deve interferire con NINA/acquisizione attiva o con file ancora in produzione;
- in caso di evidence incompleta/UNKNOWN il comportamento di cleanup è no-delete.

## 11. Continuity

Documenti correnti:

- `docs/project/HANDOVER_2026-09-04.md`;
- `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-04.md`;
- `docs/project/BACKLOG.md`;
- AP-013B e relativa evidence storica per il contratto COPY_ONLY.

Prossimo lavoro: formalizzazione AP-013C prima dell'implementazione della cancellazione; BKL-030 G6 resta il successivo gate della capability Health & Reliability.
