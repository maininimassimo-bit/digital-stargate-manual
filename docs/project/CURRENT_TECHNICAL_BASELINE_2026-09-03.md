# Digital StarGate — Current Technical Baseline — 2026-09-03

| Campo | Valore |
|---|---|
| Stato | Active technical delta baseline |
| Scope | Scientific session producer, exact evidence selection, SQM packaging, PowerShell 5.1 publish contract |
| Supersedes | `CURRENT_TECHNICAL_BASELINE_2026-09-02.md` per lo stato operativo corrente |
| Does not supersede | Principi, boundary, ADR, Architecture Package, OAT storiche o decisioni approvate |

## 1. Finalità

Questo documento registra il delta tecnico verificato il 03/09/2026 dopo l'incidente del producer automatico, la release Reporting 1.0.8 e la recovery della sessione `2026-09-02_2026-09-03`. Le baseline precedenti restano fotografie storiche valide.

## 2. Runtime Reporting corrente

La baseline runtime corrente su EAGLE30154 è `DigitalStarGate.Reporting 1.0.8`, merge `0f9bffb5a9e6192dbf0302b563b10ec7e451bd8b` del repository `maininimassimo-bit/DigitalStarGate.Reporting`.

Installazione verificata in un nuovo Windows PowerShell `-NoProfile -NonInteractive -ExecutionPolicy Bypass`:

- `DigitalStarGate.Reporting 1.0.8`;
- ModuleBase `C:\Users\PrimaLuceLab\Documents\WindowsPowerShell\Modules\DigitalStarGate.Reporting\1.0.8`;
- `Import-DSGSession` 1.0.8;
- `Publish-DSGSession` 1.0.8.

## 3. Session producer contract

Catena produttiva invariata:

`Scheduled Task -> Invoke-DSGSessionPreflight.ps1 -> Invoke-DSGAutomaticSession.ps1 -> DigitalStarGate.Reporting`.

Il preflight continua a richiedere runtime clone valido, clean, su `main`, fetch/pull fast-forward riusciti e `HEAD == origin/main` prima dell'import.

Il launcher restore-to-main su eccezione resta un hardening aperto e non deve essere confuso con il fix Reporting 1.0.8.

## 4. Evidence selection contract

Reporting 1.0.8 elimina la divergenza tra discovery e packaging NINA/PHD2: il package usa i file già selezionati dalla discovery nella finestra reale della sessione.

La precedente copia con tolleranza legacy ±12 ore non è più la baseline. Questo impedisce l'inclusione di PHD2 adiacenti terminati fuori finestra, pur preservando un log NINA iniziato precedentemente quando la sua attività/LastWriteTime ricade nella finestra corrente.

## 5. SQM evidence packaging

Resta valido il contratto introdotto dalla 1.0.7:

- source default `%LOCALAPPDATA%\DigitalStarGate\telemetry\sqm-history.ndjson`;
- `raw/sqm/sqm-history.ndjson`;
- `raw/sqm/sqm-summary.json`;
- manifest generato dopo l'export SQM.

Per `2026-09-02_2026-09-03` sono stati verificati `1295` campioni, quality `AVAILABLE`, coverage `0.9803`, min `8.91`, mean `18.1931`, max `20.84`, median `19.14` mag/arcsec².

SQM resta scientific telemetry/history, mai Safety Authority.

## 6. PowerShell 5.1 publish contract

Reporting 1.0.8 rende il wrapper Git compatibile con il comportamento Windows PowerShell 5.1 osservato sull'EAGLE: il normale stderr di Git non deve interrompere il flusso quando il comando ha exit code zero.

La recovery reale ha verificato:

```text
SessionId = 2026-09-02_2026-09-03
Committed = True
Pushed = True
Count = 1
```

Commit session branch: `0023553bf300a1536663a6ee01f7d6a5c3745514`.

## 7. Sessione e projection correnti

La sessione `2026-09-02_2026-09-03` è stata promossa automaticamente. Le projection correnti riportano M 27, `C8_QHY695A_BIN1`, completion `98.72%`, RMS total `0.244 arcsec`, SQM `AVAILABLE` con 1295 campioni/coverage `0.9803`, e severity `YELLOW`.

Il refresh analytics è presente su `main` al commit `d4feb68e89e39977d7b34b15acce69a0065dedb0`.

## 8. Stato runtime EAGLE

Dopo la recovery il clone `C:\DigitalStarGate\digital-stargate-manual-ap14-runtime` è stato verificato:

- branch `main`;
- working tree clean;
- `HEAD...origin/main = 0 0`.

Questo è lo steady state richiesto prima del prossimo run automatico.

## 9. OAT storica AP-014

Le evidence AP-014 eseguite con Reporting 1.0.6 restano storiche e valide per ciò che hanno realmente testato. I documenti del 02/09 descrivono correttamente la remediation 1.0.7 allora vigente. La baseline operativa corrente è ora 1.0.8.

## 10. Debito tecnico residuo

Restano separati:

1. restore-to-main garantito nel launcher in `finally` o meccanismo equivalente, preservando evidence e senza reset distruttivi;
2. confronto/ripristino completo della copertura quality gate Reporting storica oltre ai regression test 1.0.8.

Il drift discovery/copy ±12 ore e il bug Git stderr PowerShell 5.1 sono invece corretti nella baseline 1.0.8.

## 11. Safety e authority boundary

Invariati:

- local physical Safety Authority indipendente;
- telemetry, SQM, health, analytics e AI non sono Safety Authority;
- nessun controllo diretto portale/AI sui device nella baseline corrente;
- evidence scientifica e health non sostituiscono gli interlock locali;
- UNKNOWN/STALE non devono essere rappresentati come current.

## 12. Evoluzione successiva

La capability successiva resta **BKL-030 EAGLE Health & Reliability**. Il primo incremento è D1/D2 source discovery read-only su `EAGLE30154` tramite `scripts/telemetry/Inspect-EagleHealthSources.ps1`. Nessuna soglia o remediation automatica è autorizzata prima della classificazione delle source/evidence.
