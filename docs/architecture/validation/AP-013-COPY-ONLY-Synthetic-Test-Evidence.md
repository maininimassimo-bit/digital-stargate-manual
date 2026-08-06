# AP-013 — COPY_ONLY Synthetic Test Evidence

| Campo | Valore |
|---|---|
| Evidence ID | `E-AP013-COPYONLY-SYNTH-001` |
| Package | AP-013 — Scientific Image Repository Architecture |
| Test scope | Synthetic COPY_ONLY validation |
| Test framework | Pester 5.9.0 |
| Execution host | PC principale |
| Repository path | `C:\DigitalStarGate\digital-stargate-manual-ap013` |
| Execution date | 06/08/2026 |
| Result | Passed |
| Tests | 11 passed, 0 failed, 0 skipped |
| Run ID | `DSG-TRANSFER-RUN-af56a774-cb16-485a-8ee5-32ba27b37c09` |
| Evidence classification | TR-15 synthetic dataset evidence |

## 1. Scopo

Registrare l'esecuzione positiva della suite sintetica AP-013 per la modalità `COPY_ONLY` sul PC principale.

Questa evidenza soddisfa il criterio tecnico TR-15 del Transfer Readiness Gate per quanto riguarda l'esecuzione della suite su dataset sintetico. Non costituisce:

- pilot reale limitato;
- Operational Acceptance Test finale;
- Operational Acceptance formale;
- autorizzazione al source cleanup;
- autorizzazione a promuovere AP-013 allo stato `completed`.

## 2. Comando eseguito

```powershell
Invoke-Pester .\tools\dsdm\session-importer\tests\DSG.SessionTransfer.Tests.ps1 -Output Detailed
```

## 3. Esito sintetico

```text
Pester v5.9.0
Discovery found 11 tests.
Tests completed in 490ms
Tests Passed: 11, Failed: 0, Skipped: 0, Inconclusive: 0, NotRun: 0
```

## 4. Controlli superati

La suite ha verificato con esito positivo:

- accettazione di destinazioni sotto la root autorizzata;
- blocco di path esterni alla root autorizzata;
- classificazione `NEW`;
- classificazione `IDENTICAL`;
- classificazione `CONFLICT`;
- riconoscimento di osservazioni sorgente stabili;
- riconoscimento di osservazioni sorgente instabili;
- copia tramite staging con verifica SHA-256;
- conservazione del file sorgente;
- skip idempotente di una destinazione identica senza riscrittura;
- blocco di una destinazione in conflitto senza overwrite;
- generazione del manifest sintetico in modalità `COPY_ONLY` tramite `WhatIf`.

## 5. Risultato orchestration WhatIf

```text
DSG COPY-ONLY TRANSFER RUN COMPLETED
Run ID: DSG-TRANSFER-RUN-af56a774-cb16-485a-8ee5-32ba27b37c09
Status: COMPLETED
Requested files: 1
Copied and verified: 0
Skipped identical: 0
Deferred unstable: 0
Failed: 0
WhatIf: 1
Source files deleted: 0
```

La voce `Copied and verified: 0` è attesa perché l'orchestrazione è stata eseguita in modalità `WhatIf`.

## 6. Safety assertions confermate

- `Mode = COPY_ONLY`;
- `Status = COMPLETED`;
- `Failed = 0`;
- `SourceFilesDeleted = 0`;
- `SourceCleanupAuthorized = false`;
- `OverwriteExisting = false`;
- nessuna cancellazione sorgente;
- nessun overwrite di destinazioni in conflitto.

## 7. Riferimenti repository

| Evidenza | Percorso |
|---|---|
| Suite Pester | `tools/dsdm/session-importer/tests/DSG.SessionTransfer.Tests.ps1` |
| Transfer orchestrator | `tools/dsdm/session-importer/Invoke-DSGSessionTransfer.ps1` |
| Transfer module | `tools/dsdm/session-importer/DSG.SessionTransfer.psm1` |
| Transfer readiness gate | `docs/architecture/validation/AP-013-Transfer-Readiness-Gate.md` |
| AP-013 evidence manifest | `.github/roadmap/evidence/AP-013.evidence.json` |

## 8. Disposizione

**Synthetic COPY_ONLY test: PASSED.**

**TR-15 technical evidence: SATISFIED by this execution record.**

**Limited real pilot: NOT EXECUTED.**

**Operational Acceptance Test: NOT COMPLETED.**

**Source cleanup: PROHIBITED.**

AP-013 resta `active` finché non saranno completati e accettati gli ulteriori gate previsti, inclusi pilot reale limitato, four-eyes review, OAT e Operational Acceptance formale.
