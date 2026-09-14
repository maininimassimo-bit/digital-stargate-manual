# BKL-031 F2 — Acceptance Record

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F2-ACCEPTANCE-001 |
| Stato | **ACCEPTED / POST-MERGE VERIFIED** |
| Data | 14/09/2026 |
| Capability | BKL-031 — Observation Planner intelligente |
| Incremento accettato | F2 — Machine-Readable Context/Source Contract and Bounded Fixtures |
| Pull request | [#188](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/188) |
| Technical head reviewed | `8e46ae3eccdaca5763aee7103063e020f97e2946` |
| Review-publication head | `09b6e2272f40688c7ead0eba964b8eb6f64a0920` |
| Merge commit | `7f861f7399079858c9744e69b6c773664b6b5b54` |
| Successore | BKL-031 F3 — CURRENT HANDOFF ONLY; design/implementation not authorized |
| Runtime impact | None |
| PC Principale / EAGLE | Nessuna azione richiesta |

## 1. Decisione

BKL-031 F2 è accettato come baseline repository-only, bounded e fail-closed dell'Observation Planner. L'acceptance comprende il contratto machine-readable, la fixture source-backed M 27, il validator normativo, la suite deterministica e l'integrazione CI.

BKL-031 resta `In Progress` come capability complessiva. Questa acceptance chiude esclusivamente la milestone F2 e non promuove F3.

## 2. Ambito accettato

- cinque oggetti semantici F1 codificati senza score o ranking;
- inventario BKL031-S01–S11 preservato;
- S07–S11 esplicitamente unavailable/unknown;
- S02 unica authority F2 per RA/Dec/epoch;
- S04 storico risolvibile tramite S03 e non autorizzato ad attestare coordinate;
- Citation e Provenance legate ai valori e agli input/output esatti;
- validator totale e fail-closed;
- 37 test, inclusi N01–N20 e regressioni M-01–M-04/M-R1;
- nessun runtime, provider, consumer operativo o modifica EAGLE.

## 3. Review

| Review | Esito | Qualifica |
|---|---|---|
| ARB PR #188 M-R1 | APPROVED — 99/100 | AI-assisted, owner-authorized; non equivalente ad approvazione umana indipendente |
| Release Quality PR #188 M-R1 | CONDITIONALLY READY | AI-assisted, owner-authorized; non equivalente ad approvazione umana indipendente |

Tutti i finding M-01, M-02, M-03, M-04 e M-R1 sono chiusi. Non resta alcun finding Blocker, Major o Minor.

## 4. Evidenza CI

### Review-publication head `09b6e2272f40688c7ead0eba964b8eb6f64a0920`

Sette workflow su sette: SUCCESS.

### Merge commit `7f861f7399079858c9744e69b6c773664b6b5b54`

| Workflow | Run | Esito |
|---|---:|---|
| Developer Foundation | 1391 | SUCCESS |
| Validate documentation | 1028 | SUCCESS |
| Genera manuale Word | 1454 | SUCCESS |
| Scientific Platform Governance | 91 | SUCCESS |
| Governed Projection Sync | 33 | SUCCESS |
| Deploy MkDocs artifact to GitHub Pages | 794 | SUCCESS |
| BKL-041 F4 Governance | 93 | SUCCESS |
| BKL-046 F4 governance | 67 | SUCCESS |
| BKL-046 F5 governance | 52 | SUCCESS |

## 5. Quality gates

| Gate | Stato | Evidenza |
|---|---|---|
| Architecture | Passed | ARB 99/100 |
| Contract and semantics | Passed | 37/37 tests; all findings closed |
| Documentation and links | Passed | Validate documentation #1028 |
| Build/regression | Passed | Developer Foundation #1391 |
| Governed projections | Passed | Governance workflows and Projection Sync |
| Portal publication | Passed | Pages #794 |
| Security/privacy | Passed | public-safe locator boundary retained |
| Safety | Passed | no action or Safety Authority |
| Runtime/OAT | Not Applicable | repository-only increment |
| Migration | Not Applicable | additive files only |
| Rollback | Passed | repository revert |
| Independent human approval | Not Executed | AI-assisted disclosure retained |

## 6. Risk and waiver register

| ID | Stato | Disposizione |
|---|---|---|
| W-BKL031-F2-MERGE-001 | **Consumed / Expired** | deroga una tantum limitata a PR #188 e exact head `09b6e2272f40688c7ead0eba964b8eb6f64a0920`; nessun precedente |
| F2-AI-REVIEW | Disclosed | non rappresentare le review come approvazioni umane indipendenti |
| BKL031-S07–S11 | Open / carried | mantenere unavailable/unknown fino a source contract separatamente governati |
| Successor / F3 | **NOT AUTHORIZED** | richiede nuova decisione owner e nuovo package |

## 7. Boundaries after closure

Restano fuori scope provider site/setup/ephemeris/lunar/forecast, pesi, score, normalizzazione, ranking, ordinamento target, portal consumer runtime, readiness, scheduling, go/no-go, device command, workload pesante EAGLE e Safety Authority.

## 8. Next governed action

Il successore governato è BKL-031 F3 per sito/setup ed ephemeris/lunare. È autorizzato soltanto l'handoff di programma; design dettagliato, provider selection, implementazione e runtime richiedono nuove autorizzazioni.
