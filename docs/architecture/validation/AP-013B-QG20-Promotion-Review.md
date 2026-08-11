# AP-013B — QG-20 Promotion Review

| Campo | Valore |
|---|---|
| Identificativo | `QG20-AP013B-001` |
| Incremento | AP-013B — OneDrive-mediated COPY_ONLY Transport |
| Data review | 11/08/2026 |
| Baseline review | `0fa5cfb6a3778f7529083418c2c3e5fba62064a6` |
| Decisione | **Approved for limited production** |
| QG-20 | **Passed** |
| Limite operativo | `MaxFilesPerRun <= 30` |

## 1. Scope della promotion

La promotion riguarda esclusivamente l'incremento AP-013B che sostituisce il data path SMB/VPN diretto con un transport OneDrive mantenendo il motore AP-013 in modalità `COPY_ONLY`.

La decisione non dichiara completato l'intero package AP-013. Il package AP-013 resta governato dal proprio evidence manifest e dai relativi artefatti di architecture review e operational acceptance.

## 2. Release impact report

### Impatto autorizzato

- EAGLE esporta da `D:\Images NINA\Target` verso il transport OneDrive dedicato;
- il PC principale importa dal transport OneDrive verso `F:\Astrofotografia`;
- gli scheduler AP-013B restano attivi e hidden;
- la task legacy SMB `Digital StarGate - Morning Transfer` resta disabilitata e disponibile esclusivamente come rollback esplicito;
- `COPY_ONLY`, SHA-256, manifest `READY`, no overwrite e no delete restano invarianti obbligatorie.

### Impatto non autorizzato

La promotion non autorizza:

- `MaxFilesPerRun > 30`;
- cleanup automatico di source o transport;
- overwrite;
- bypass della verifica SHA-256;
- modifica della semantica READY/staging;
- riattivazione permanente del percorso SMB/VPN;
- dichiarazione di capacità scale-out a 1000 file.

## 3. Quality-gate review

| Area | Stato | Evidenza |
|---|---|---|
| Architecture boundary | Passed | OneDrive è transport, `F:` resta repository finale |
| Source immutability | Passed | `SourceFilesDeleted = 0` nei run verificati |
| No overwrite | Passed | `OverwritesPerformed = 0` |
| End-to-end integrity | Passed | SHA-256 manifest = transport = destination |
| READY protocol | Passed | Import solo dopo payload localmente disponibile e verificato |
| Unit/regression | Passed | suite OneDrive 9/9; SessionImporter/SessionTransfer senza failure |
| Batch 10 | Passed | OAT-RUN-010 |
| Batch 100 cumulative | Passed | progression verificata oltre 100 asset |
| Batch 1000 | Not Executed | non bloccante con batch massimo 30 |
| Sync interruption | Passed | QG-11 fail-safe e recovery end-to-end |
| Restart recovery | Passed | QG-12A PC + QG-12B EAGLE |
| Tamper/conflict | Passed synthetic | mismatch hash e conflitti bloccano l'import |
| Idempotency | Passed | retry sicuri e `SKIP_IDENTICAL` |
| Evidence | Passed | CSV/JSON per run |
| Scheduler | Passed | hidden, `IgnoreNew`, `LastTaskResult = 0` osservato |
| Security/ACL | Passed | ACL e principal verificati sui due host; nessun secret negli argomenti |
| Operations/runbook | Passed | runbook AP-013B e rollback disponibili |
| CI candidate baseline | Passed | `deploy`, `quality-gate`, `build-word` su `0fa5cfb6...` tutti `completed/success` |

## 4. Risk and waiver register

| Rischio | Disposition |
|---|---|
| OneDrive delay/throttling | Accepted with mitigation: batch 30, READY protocol, idempotent retry |
| Cloud interruption | Mitigated and tested by QG-11 |
| Host reboot | Mitigated and tested by QG-12A/B |
| Files On-Demand / local availability | Mitigated: nessun import senza payload locale verificato |
| Backlog growth | Mitigated at current scale; progression verificata con batch 30 |
| Duplicate temporary storage | Accepted; automatic cleanup remains prohibited |
| Local path dependency | Technical debt; controlled by runbook change control |
| QG-10 not executed | Waiver limited to batch <=30; scale-out claims prohibited |
| `main` branch unprotected | Governance observation; non-blocking for AP-013B runtime promotion, remediation recommended separately |
| Commit unsigned | Governance observation; non-blocking under current repository policy |

Nessun waiver autorizza delete, overwrite, hash bypass o ampliamento del batch oltre 30.

## 5. CI and repository truth

Al momento della review:

- `main` punta a `0fa5cfb6a3778f7529083418c2c3e5fba62064a6`;
- check run `deploy`: `completed/success`;
- check run `quality-gate`: `completed/success`;
- check run `build-word`: `completed/success`.

## 6. Governance boundary AP-013B vs AP-013

Il manifest `.github/roadmap/evidence/AP-013.evidence.json` continua a richiedere, per completare l'intero AP-013:

- `docs/architecture/reviews/ARB-013-Scientific-Image-Repository-Architecture-Review.md`;
- `docs/architecture/validation/AP-013-OAT-001.md`;
- `docs/architecture/validation/AP-013-Operational-Acceptance.md`.

Questi artefatti non sono sostituiti dalla presente promotion review. Di conseguenza:

- **AP-013B operational increment: Approved for limited production**;
- **AP-013 package: remains Active until its evidence contract is fully satisfied**.

## 7. Promotion decision

**QG-20: PASSED — APPROVED FOR LIMITED PRODUCTION.**

Condizioni vincolanti:

1. mantenere `MaxFilesPerRun <= 30`;
2. mantenere `COPY_ONLY`;
3. mantenere SHA-256 e protocollo READY;
4. nessuna cancellazione automatica di source o transport;
5. nessun overwrite;
6. task legacy SMB disabilitata salvo rollback esplicito;
7. qualsiasi modifica a path, principal, batch, cleanup, hashing o staging richiede nuova validazione;
8. QG-10 deve essere eseguito prima di dichiarare capacità operativa equivalente a 1000 file o di aumentare il batch oltre 30.

## 8. Readiness recommendation

**READY — Limited Production.**

La promotion AP-013B è autorizzata nella baseline e nei limiti sopra descritti. Non viene concessa alcuna autorizzazione implicita per chiudere AP-013 nel roadmap/evidence model finché il relativo evidence contract non è completo.
