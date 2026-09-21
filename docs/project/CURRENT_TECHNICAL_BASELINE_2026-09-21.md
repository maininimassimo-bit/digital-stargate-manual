# Digital StarGate — Current Technical Baseline 21/09/2026

| Campo | Valore |
|---|---|
| Identificativo | DSG-BASELINE-2026-09-21 |
| Stato | Current governed continuity baseline |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch autorevole | `main` |
| Baseline verificata | `main@6288bd1a3129ebf519cd1a66868cbe7b77514de9` |
| Work package corrente | AP-007 — Enterprise Operations and Service Management Architecture |
| Stato package | Baseline reconciled — review candidate |
| Mandato | DSG-AEM-001 v1.2 ACTIVE / OWNER-AUTHORIZED |

## 1. Scopo e autorità

Questa baseline riconcilia gli artefatti di continuità con il default branch alla data indicata. GitHub e il commit di baseline restano la fonte di verità; le projection e gli snapshot precedenti non prevalgono sul repository corrente.

AP-007 resta candidato alla review ARB indipendente: non è promosso a `Operationally Verified`, non assegna ruoli non verificati e non abilita un servizio ITSM, transport live, scheduler, comando, remediation automatica o Safety Authority.

## 2. Stato riconciliato

- BKL-031 e BKL-032 restano Closed / Accepted / Post-Merge Verified entro i rispettivi boundary.
- BKL-036 è chiuso come capability repository-only bounded; F3 Health Score resta `UNAVAILABLE`.
- AP-007 ha baseline e ownership bootstrap riconciliati in `AP007-BASELINE-RECON-001`; i ruoli non supportati da evidence restano `DA VALIDARE`.
- Il prossimo gate è ARB indipendente AP-007, seguito dalla matrice Release Quality; qualsiasi evidence operativa rimane separatamente richiesta.

## 3. Authority e boundary invariati

- gli interlock fisici/locali restano l’unica Safety Authority;
- BKL-032 conserva l’autorità decision-support di readiness/go-no-go read-only;
- BKL-031 resta advisory/read-only;
- AP-007 coordina il modello operativo ma non sostituisce AP-003/AP-004/AP-005/AP-006/AP-010;
- missing, stale, conflict o assenza di evidence non possono essere promossi a stato operativo.

## 4. Catena di tracciabilità

| Elemento | Record autorevole |
|---|---|
| Bootstrap | `AI_BOOTSTRAP.md` |
| Handover corrente | `docs/project/HANDOVER_2026-09-21-AP-007.md` |
| Baseline AP-007 | `docs/project/AP-007-BASELINE-RECONCILIATION-2026-09-20.md` |
| Package | `docs/architecture/packages/AP-007-Enterprise-Operations-and-Service-Management-Architecture.md` |
| Reference architecture | `docs/architecture/enterprise-operations-and-service-management-reference-architecture.md` |
| Traceability | `docs/architecture/traceability-register.md` |
| Mandato | `docs/project/DSG-AEM-001-CONTINUOUS-AUTONOMOUS-EXECUTION-MANDATE-2026-09-15.md` |

## 5. Validazione

Eseguita: confronto degli artefatti sopra indicati contro `main@6288bd1a3129ebf519cd1a66868cbe7b77514de9` e verifica per ispezione dei boundary.

Non eseguita: review ARB indipendente, matrice Release Quality, `mkdocs build --strict`, test runtime/OAT, test di runbook/recovery/on-call e qualsiasi attività live.

## 6. Prossimo passo

Completare ARB AP-007 e Release Quality sullo stesso exact head. L’eventuale implementazione operativa richiederà evidence, owner/ruoli validati e un gate separato.
