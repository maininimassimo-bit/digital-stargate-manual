# AP-013C — Verified Transport Cleanup and Convergence Monitoring

| Campo | Valore |
|---|---|
| Identificativo | AP-013C |
| Titolo | Verified Transport Cleanup and Convergence Monitoring |
| Tipo | Architecture Package incrementale di AP-013 |
| Stato | **Accepted — DRY_RUN / NO_DELETE increment closed** |
| Versione | 0.3 |
| Data | 04/09/2026 |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch | `architecture/ap-013c-verified-transport-cleanup` |
| Baseline di partenza | AP-013B `COPY_ONLY` — Passed / Limited Production |
| Backlog | BKL-047 — Done for no-delete scope |
| Review | `ARB-013C-R1` — Approved with Conditions; C01-C06 closed for no-delete scope |
| Runtime evidence | `E-AP013C-OAT-2026-09-04` |
| Safety impact | Nessuna modifica alla Safety Authority |
| Delete produttivo | **Non autorizzato — C8 separate future gate** |

## 1. Purpose

AP-013C governa l'evoluzione del trasporto scientifico raw Digital StarGate affinché lo stato end-to-end del transport OneDrive sia osservabile e fail-closed rispetto alla prova di corretta conservazione del file scientifico nella destinazione autorevole.

Il package nasce dall'incidente OneDrive del 04/09/2026: EAGLE osservava `445 XISF / 445 READY`, mentre il PC principale osservava temporaneamente `426 / 426`. Dopo recovery il PC è riconvergente a 445/445 e i 19 frame mancanti sono stati verificati in `F:\Astrofotografia` senza perdita osservata.

Principio guida:

> Se Digital StarGate non può dimostrare che il dato scientifico è arrivato integro alla destinazione autorevole, il file transport non può essere autorizzato al cleanup.

## 2. Scope accettato

### In scope

- lifecycle end-to-end del raw XISF dal transport EAGLE alla destinazione finale;
- convergence monitoring producer EAGLE / consumer PC;
- riuso READY, size e SHA-256 AP-013B;
- ACK di destination verification emesso solo dopo prova valida della destinazione;
- inventario metadata-only XISF/READY/ACK;
- classificazione fail-closed con reason code;
- separazione esplicita tra `TechnicalCandidate` e autorizzazione produttiva;
- evaluator `DRY_RUN_NO_DELETE`;
- synthetic failure injection e controlled real PC/EAGLE/OneDrive OAT;
- rollback sulla baseline AP-013B `COPY_ONLY`.

### Out of scope / future C8

- cancellazione produttiva di XISF transport;
- retention/grace policy;
- controller capace di eseguire delete;
- execution principal/ACL per cleanup produttivo;
- crash-safe/idempotent delete semantics e partial-failure recovery;
- qualsiasi modifica alla Safety Authority o agli interlock fisici.

Questi elementi richiedono un nuovo change-set governato e non sono autorizzati dalla closure AP-013C v0.3.

## 3. Accepted evidence contract

Il contratto accettato conserva READY AP-013B e ACK schema 1.0. La prova completa può rendere un asset soltanto candidato tecnico nel perimetro corrente:

```text
State = TECHNICAL_CANDIDATE_DRY_RUN
TechnicalCandidate = True
CleanupEligible = False
CleanupAuthorized = False
PolicyReasonCode = RETENTION_NOT_APPROVED
Deleted = 0
```

Evidence incompleta o incoerente resta bloccante. Esempi di reason code accettati includono:

- `READY_MISSING`;
- `READY_INVALID`;
- `TRANSPORT_PAYLOAD_MISSING`;
- `ACK_MISSING`;
- `ACK_INVALID`;
- `DESTINATION_HASH_MISMATCH`;
- `ACK_READY_HASH_MISMATCH`.

## 4. Real OAT closure

Evidence canonica: `docs/architecture/evidence/AP-013C-Real-OAT-2026-09-04.md`.

PC `WIN-QOOF3903TQS` baseline:

```text
445 XISF / 445 READY / 0 ACK / 0 PARTIAL
```

Controlled AP-013C pilot:

```text
AlreadyImportedSkipped = 10
AckCreated = 10
AckFailed = 0
Failed = 0
SourceFilesDeleted = 0
TransportFilesDeleted = 0
OverwritesPerformed = 0
```

Riconvergenza su `EAGLE30154`:

```text
445 XISF / 445 READY / 10 ACK / 0 PARTIAL
```

Evaluator reale EAGLE:

```text
AssetsObserved       = 445
TechnicalCandidates  = 10
Blocked              = 435
ACK_MISSING          = 435
CleanupAuthorized    = 0
CleanupEligible      = 0
Deleted              = 0
```

Il real OAT dimostra che la riconvergenza ACK non viene trasformata in autorizzazione al delete.

## 5. Failure and recovery coverage

AP-013C combina:

- real incident/recovery evidence della foundation AP-013B;
- real ACK generation/reconvergence/evaluator OAT AP-013C;
- synthetic incident-shaped divergence/reconvergence;
- regression tests per missing/orphan/invalid/mismatch states;
- idempotency e fail-closed classification.

Non è stata eseguita né simulata come autorizzata alcuna cancellazione produttiva.

## 6. Architecture boundaries

AP-013B resta la foundation operativa e il rollback:

```text
EAGLE source D:\Images NINA\Target
  -> COPY_ONLY export
  -> OneDrive transport
  -> COPY_ONLY import
  -> F:\Astrofotografia
```

AP-013C aggiunge evidence e classificazione sopra tale foundation. Non acquisisce authority sulla sorgente N.I.N.A., sulla Safety Authority o sugli interlock locali.

GitHub conserva contratti, evidence, script e traceability; non diventa repository dei bulk scientific pixels.

## 7. Observability and audit

Ogni evaluator run produce evidence JSON/CSV con:

- run/timestamp/host;
- inventory XISF/READY/ACK;
- per-asset state;
- technical candidacy;
- cleanup eligibility/authorization;
- reason e policy reason;
- summary counts;
- `Deleted`.

L'inventario resta metadata-only per evitare bulk hydration/hashing degli XISF durante la sola discovery.

## 8. Rollback

Per il package accettato il rollback è semplice e non distruttivo:

1. non eseguire evaluator/ACK producer AP-013C;
2. mantenere AP-013B `COPY_ONLY`;
3. preservare READY/ACK/evidence esistenti;
4. non cancellare o sovrascrivere file scientifici.

## 9. Validation and review

- AP-013C dedicated Pester/Windows CI: green sul runtime baseline OAT;
- Developer Foundation: green;
- documentation validation: green;
- Word generation: green;
- real PC/EAGLE/OneDrive OAT: passed;
- independent ARB re-review `ARB-013C-R1`: **Approved with Conditions**;
- original ARB conditions C01-C06: closed per scope `DRY_RUN/NO_DELETE`.

La CI deve restare verde sul final documentation head prima del merge.

## 10. Closure decision

**AP-013C v0.3 — ACCEPTED / CLOSED FOR DRY_RUN / NO_DELETE.**

BKL-047 può essere chiuso per questo perimetro e la roadmap può riprendere BKL-030 G6 history/persistence.

La closure non autorizza l'obiettivo originario futuro di liberare automaticamente spazio EAGLE mediante cancellazione del transport.

## 11. Future C8 gate

Qualunque proposta di productive cleanup richiede almeno:

1. retention/grace policy approvata;
2. crash-safe e idempotent delete semantics;
3. partial-failure handling e incident recovery;
4. execution principal/ACL e authority boundary;
5. implementazione separata senza modifica della sorgente scientifica RAW;
6. test e OAT applicabili;
7. ARB e release-quality review separate;
8. autorizzazione esplicita prima dell'enablement.

Fino a tale futura decisione:

```text
CleanupEligible = False
CleanupAuthorized = False
Deleted = 0
```

è il contratto obbligatorio.