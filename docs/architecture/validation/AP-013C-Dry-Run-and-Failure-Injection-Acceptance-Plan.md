# AP-013C — Dry-Run and Failure-Injection Acceptance Plan

| Campo | Valore |
|---|---|
| Identificativo | `OAT-AP013C-PLAN-001` |
| Package | AP-013C — Verified Transport Cleanup and Convergence Monitoring |
| Stato | Active — real OAT pending |
| Versione | 0.2 |
| Data | 04/09/2026 |
| Modalità iniziale | `DRY_RUN / NO_DELETE` |
| Delete produttivo | Non autorizzato |

## 1. Scopo

Definire i quality gate necessari per dimostrare che AP-013C classifica correttamente convergence e candidacy tecnica senza cancellare alcun file durante la fase iniziale.

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

| Gate | Obiettivo | Evidence minima | Exit |
|---|---|---|---|
| C1 | Architecture baseline | AP-013C package + traceability | review completa |
| C2 | State/evidence contract | READY reuse + ACK schema + reason model | contract stabile |
| C3 | Controlled real OAT | PC/EAGLE/OneDrive reali, no-delete | evidence runtime conservata |
| C4 | Dry-run evaluator | per-asset state + candidate + reason | `Deleted=0` |
| C5 | Failure injection | riproduzione divergenza 445/445 vs 426/426 | no false technical candidate per asset non convergenti |
| C6 | Recovery/reconvergence | PC 445/445 + F verified + ACK converged | candidacy tecnica coerente |
| C7 | Independent ARB | review package/evidence/rollback | disposition ARB |
| C8 | Production promotion | retention + delete semantics + rollback approvati | richiede autorizzazione esplicita |

## 4. Test Matrix

### T01 — Nominal verified asset

Precondizioni:

- XISF + READY validi;
- payload osservato lato PC;
- destinazione F: esistente;
- size/hash destinazione = READY;
- ACK valido e riconvergente su EAGLE.

Atteso in dry-run:

```text
State = TECHNICAL_CANDIDATE_DRY_RUN
TechnicalCandidate = True
CleanupEligible = False
CleanupAuthorized = False
PolicyReasonCode = RETENTION_NOT_APPROVED
Deleted = 0
```

### T02 — READY only / ACK not converged

Atteso:

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

### T04 — Destination hash mismatch

Atteso: ACK non creato oppure evidence `DESTINATION_HASH_MISMATCH`; no-delete.

### T05 — ACK absent

Atteso: `ACK_MISSING`, no-delete.

### T06 — ACK malformed / unsupported schema

Atteso: `ACK_INVALID`, block/no-delete.

### T07 — ACK hash mismatch

Atteso: `DESTINATION_HASH_MISMATCH` o `ACK_READY_HASH_MISMATCH`, no-delete.

### T08 — Restart / retry

Dopo restart di uno dei due host, lo stato deve essere ricostruito da evidence persistente. Nessun asset può diventare technical candidate per default e nessun asset può diventare authorized.

### T09 — Idempotency

Riesecuzioni consecutive con evidence invariata devono produrre la stessa classificazione e non creare ACK semanticamente duplicati.

### T10 — Partial/staging

Un `.dsg-partial` non può produrre READY, ACK, technical candidacy o autorizzazione.

### T11 — Orphan inventory

XISF senza READY e ACK senza READY devono essere visibili nell'inventario metadata-only e classificati fail-closed senza bulk hashing degli XISF.

## 5. Mandatory Incident Reproduction

Scenario derivato dall'incidente 04/09/2026:

```text
EAGLE transport: 445 XISF / 445 READY
PC transport:    426 XISF / 426 READY
Gap:              19 XISF / 19 READY
```

Per i 19 asset non convergenti il dry-run deve dimostrare:

```text
TechnicalCandidate = False
CleanupEligible = False
CleanupAuthorized = False
Deleted = 0
```

È vietato inferire convergence dal solo conteggio EAGLE o da `LastTaskResult = 0`.

## 6. Recovery Phase

Dopo ripristino OneDrive:

1. PC raggiunge la convergenza attesa;
2. ogni payload candidato viene verificato contro READY;
3. la destinazione F: viene verificata per size e SHA-256;
4. viene creato l'ACK di destination verification;
5. l'ACK converge sull'EAGLE;
6. l'evaluator ricalcola lo stato;
7. solo gli asset con evidence completa possono diventare `TechnicalCandidate=True`;
8. `CleanupEligible=False`, `CleanupAuthorized=False` e `Deleted=0` restano invarianti durante l'intera OAT.

## 7. Failure Injection

Devono essere testati in modo non distruttivo, ove applicabili al controlled real OAT o già coperti da synthetic CI:

- OneDrive PC sospeso/offline;
- OneDrive EAGLE sospeso/offline;
- READY ritardato rispetto a XISF;
- XISF ritardato rispetto a READY;
- ACK ritardato;
- ACK corrotto;
- hash mismatch;
- destinazione F: temporaneamente indisponibile;
- restart PC;
- restart EAGLE;
- retry multipli.

Non è richiesto causare perdita dati o cancellazioni reali per validare questi scenari.

## 8. Evidence Bundle

Ogni run deve conservare:

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
- errori e retry;
- eventuale snapshot di configurazione non-secret.

## 9. Promotion Preconditions

C8 non può essere richiesto finché non risultano soddisfatti tutti i seguenti punti:

- C1-C7 completati;
- ARB disposition favorevole dopo re-review;
- retention/grace period formalmente approvata;
- semantica del delete crash-safe e idempotente definita;
- rollback AP-013B verificato;
- nessun unresolved mismatch;
- CI/regression applicabile verde;
- OAT reale con `CleanupAuthorized=False` e `Deleted=0` completata.

## 10. Rollback

Durante dry-run il rollback consiste nel disabilitare evaluator/ACK producer e mantenere AP-013B invariato.

Dopo una futura promotion produttiva, il rollback dovrà almeno:

1. disabilitare cleanup controller;
2. lasciare Export/Import AP-013B in `COPY_ONLY`;
3. preservare READY/ACK/evidence;
4. non ricreare o sovrascrivere automaticamente file mancanti;
5. aprire incident/recovery review se è stato osservato un delete non conforme.

## 11. Disposition corrente

Il piano autorizza controlled real OAT e failure injection non distruttiva.

**Non autorizza cancellazione produttiva.**
