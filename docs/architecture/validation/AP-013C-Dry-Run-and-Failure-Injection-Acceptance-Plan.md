# AP-013C — Dry-Run and Failure-Injection Acceptance Plan

| Campo | Valore |
|---|---|
| Identificativo | `OAT-AP013C-PLAN-001` |
| Package | AP-013C — Verified Transport Cleanup and Convergence Monitoring |
| Stato | **Passed — DRY_RUN / NO_DELETE** |
| Versione | 0.3 |
| Data | 04/09/2026 |
| Modalità accettata | `DRY_RUN / NO_DELETE` |
| Evidence runtime | `E-AP013C-OAT-2026-09-04` |
| ARB re-review | `ARB-013C-R1` — Approved with Conditions |
| Delete produttivo | **Non autorizzato** |

## 1. Scopo

Definire e registrare i quality gate necessari per dimostrare che AP-013C classifica correttamente convergence e candidacy tecnica senza cancellare alcun file durante l'incremento accettato.

La remediation ARB separa esplicitamente la prova tecnica dalla policy di autorizzazione:

```text
TechnicalCandidate = True|False
CleanupEligible = False
CleanupAuthorized = False
Deleted = 0
```

`TechnicalCandidate=True` non autorizza alcun delete.

## 2. Invarianti di test

Per tutti i test prima di una futura promotion C8:

```text
CleanupEligible = False
CleanupAuthorized = False
Deleted = 0
SourceFilesDeleted = 0
TransportFilesDeleted = 0
OverwritesPerformed = 0
```

Qualunque violazione rende l'esito `FAILED` e blocca la promotion.

## 3. Gate

| Gate | Obiettivo | Evidence minima | Stato finale |
|---|---|---|---|
| C1 | Architecture baseline | AP-013C package + traceability | **Passed** |
| C2 | State/evidence contract | READY reuse + ACK schema + reason model | **Passed** |
| C3 | Controlled real OAT | PC/EAGLE/OneDrive reali, no-delete | **Passed — `E-AP013C-OAT-2026-09-04`** |
| C4 | Dry-run evaluator | per-asset state + candidate + reason | **Passed — `Deleted=0`** |
| C5 | Failure injection | riproduzione divergenza 445/445 vs 426/426 | **Passed** |
| C6 | Recovery/reconvergence | PC/F verified + ACK converged | **Passed per scope no-delete** |
| C7 | Independent ARB | review package/evidence/rollback | **Passed — `ARB-013C-R1`** |
| C8 | Production promotion | retention + delete semantics + rollback approvati | **Not Authorized / separate future gate** |

## 4. Test Matrix

### T01 — Nominal verified asset

Precondizioni:

- XISF + READY validi;
- payload osservato lato PC;
- destinazione F: esistente;
- size/hash destinazione = READY;
- ACK valido e riconvergente su EAGLE.

Atteso e verificato nel real OAT:

```text
State = TECHNICAL_CANDIDATE_DRY_RUN
TechnicalCandidate = True
CleanupEligible = False
CleanupAuthorized = False
PolicyReasonCode = RETENTION_NOT_APPROVED
Deleted = 0
```

### T02 — READY only / ACK not converged

Atteso e verificato nella classificazione live:

```text
TechnicalCandidate = False
CleanupEligible = False
CleanupAuthorized = False
ReasonCode = ACK_MISSING
Deleted = 0
```

### T03 — Payload transport mancante

Atteso:

```text
TechnicalCandidate = False
ReasonCode = TRANSPORT_PAYLOAD_MISSING
Deleted = 0
```

Coperto da regression test metadata-only; non è stato introdotto artificialmente sul transport reale.

### T04 — Destination hash mismatch

Atteso: ACK non creato oppure evidence `DESTINATION_HASH_MISMATCH`; no-delete. Coperto synthetic/regression.

### T05 — ACK absent

Atteso: `ACK_MISSING`, no-delete. Verificato anche nel real OAT per 435 asset.

### T06 — ACK malformed / unsupported schema

Atteso: `ACK_INVALID`, block/no-delete. Coperto synthetic/regression.

### T07 — ACK hash mismatch

Atteso: `DESTINATION_HASH_MISMATCH` o `ACK_READY_HASH_MISMATCH`, no-delete. Coperto synthetic/regression.

### T08 — Restart / retry

Lo stato deve essere ricostruito da evidence persistente. Nessun asset può diventare technical candidate per default e nessun asset può diventare authorized. La foundation AP-013B dispone già di real restart/recovery evidence; AP-013C aggiunge synthetic/regression coverage senza modificare il path COPY_ONLY sottostante.

### T09 — Idempotency

Riesecuzioni consecutive con evidence invariata devono produrre la stessa classificazione e non creare ACK semanticamente duplicati. Coperto da regression test AP-013C e dalla baseline AP-013B per il transport.

### T10 — Partial/staging

Un `.dsg-partial` non può produrre READY, ACK, technical candidacy o autorizzazione. Il real OAT ha osservato `PARTIAL=0` su PC ed EAGLE.

### T11 — Orphan inventory

XISF senza READY e ACK senza READY devono essere visibili nell'inventario metadata-only e classificati fail-closed senza bulk hashing degli XISF. Coperto da remediation C01 e regression test.

## 5. Mandatory Incident Reproduction

Scenario derivato dall'incidente 04/09/2026:

```text
EAGLE transport: 445 XISF / 445 READY
PC transport:    426 XISF / 426 READY
Gap:              19 XISF / 19 READY
```

La failure injection AP-013C ha dimostrato per i 19 asset non convergenti:

```text
TechnicalCandidate = False
CleanupEligible = False
CleanupAuthorized = False
Deleted = 0
```

È vietato inferire convergence dal solo conteggio EAGLE o da `LastTaskResult = 0`.

## 6. Real Recovery / Reconvergence Evidence

Il controlled real OAT del 04/09/2026 ha verificato:

1. baseline PC `445 XISF / 445 READY / 0 ACK / 0 PARTIAL`;
2. verifica di 10 destinazioni già presenti su `F:\Astrofotografia`;
3. creazione `AckCreated=10`, `AckFailed=0`;
4. riconvergenza OneDrive su EAGLE a `445 XISF / 445 READY / 10 ACK / 0 PARTIAL`;
5. evaluator EAGLE con `TechnicalCandidates=10` e `Blocked=435`;
6. `CleanupEligible=0`, `CleanupAuthorized=0`, `Deleted=0`.

Evidence canonica: `docs/architecture/evidence/AP-013C-Real-OAT-2026-09-04.md`.

## 7. Failure Injection Coverage

La validazione non distruttiva comprende, tramite real AP-013B foundation evidence e/o AP-013C synthetic/regression tests:

- OneDrive PC sospeso/offline;
- OneDrive EAGLE/restart recovery della foundation transport;
- READY/XISF non convergenti;
- ACK ritardato/mancante;
- ACK corrotto;
- hash mismatch;
- restart PC;
- restart EAGLE;
- retry multipli.

Non è stata provocata perdita dati o una cancellazione reale. Una futura modalità produttiva richiederà una nuova campagna specifica e una nuova autorizzazione.

## 8. Evidence Bundle

L'evidence accettata conserva o riferisce:

- run ID e correlation ID;
- timestamp UTC;
- host;
- versione evaluator/contract;
- inventory XISF/READY/ACK;
- per-asset state;
- `TechnicalCandidate`;
- `CleanupEligible`;
- `CleanupAuthorized`;
- reason code e policy reason code;
- size/hash rilevanti lato PC/destination;
- summary count;
- `Deleted`;
- errori/retry applicabili;
- configurazione non-secret rilevante.

## 9. Future C8 Preconditions

C8 productive cleanup non è parte della presente acceptance e non può essere richiesto finché non risultano soddisfatti tutti i seguenti punti:

- retention/grace period formalmente approvata;
- semantica del delete crash-safe e idempotente definita;
- partial-failure handling definito;
- authority boundary, principal/ACL e rollback produttivo definiti;
- implementazione produttiva separata e test applicabili;
- nessun unresolved mismatch;
- CI/regression applicabile verde;
- nuova disposition ARB e release-quality favorevole;
- autorizzazione esplicita prima dell'enablement.

## 10. Rollback

Per l'incremento accettato il rollback consiste nel disabilitare evaluator/ACK producer e mantenere AP-013B invariato in `COPY_ONLY`.

Dopo una futura promotion produttiva, un nuovo design dovrà almeno:

1. disabilitare cleanup controller;
2. lasciare Export/Import AP-013B in `COPY_ONLY`;
3. preservare READY/ACK/evidence;
4. non ricreare o sovrascrivere automaticamente file mancanti;
5. aprire incident/recovery review se è stato osservato un delete non conforme.

## 11. Disposition finale

**PASSED — AP-013C DRY_RUN / NO_DELETE.**

C1-C7 sono completati per il perimetro no-delete. `E-AP013C-OAT-2026-09-04` e `ARB-013C-R1` costituiscono la closure evidence del runtime e della review indipendente.

**C8 PRODUCTIVE CLEANUP: NOT AUTHORIZED / NO-GO.**
