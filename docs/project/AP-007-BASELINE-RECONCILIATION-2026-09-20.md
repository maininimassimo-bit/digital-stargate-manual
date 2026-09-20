# AP-007 — Baseline Reconciliation and Ownership Bootstrap

| Campo | Valore |
|---|---|
| Identificativo | AP007-BASELINE-RECON-001 |
| Package | AP-007 — Enterprise Operations and Service Management Architecture |
| Data | 2026-09-20 |
| Stato | Baseline reconciled — review candidate |
| Mandato | DSG-AEM-001 v1.2 |
| Repository baseline | `main@1f67601e0ac16e6e0278244555e1a7e3d34b26e3` |

## 1. Scopo

Questo documento chiude la prima tranche di AP-007: riconciliazione di baseline, dipendenze e vincoli; bootstrap del registro ownership; preparazione alla review ARB. Non certifica operatività, non assegna ruoli non verificati e non introduce un servizio ITSM, runtime, scheduler, comando o Safety Authority.

## 2. Baseline verificata

| Area | Fonte | Esito |
|---|---|---|
| Operating model | AP-007 | presente; pronto per review |
| Reference architecture | OPS-REF-001 | presente; pronto per review |
| Roadmap/dependency order | AMP-002 e roadmap canonica | AP-007 prossimo package attivo |
| Configuration/change | AP-006 | dipendenza esistente |
| Telemetry/observability | AP-004 | dipendenza esistente |
| Identity/privileged access | AP-005 | dipendenza esistente |
| Automation boundary | AP-003 | safety boundary preservato |
| Safety assurance | AP-010 | dipendenza futura; non sostituita da AP-007 |
| Readiness/go-no-go | BKL-032 | autorità separata |
| BKL-036 | closure 2026-09-19 | repository-only; F3 `UNAVAILABLE` |

## 3. Dipendenze e boundary

AP-007 coordina service management, incident, problem, change, release, maintenance, runbook, readiness governance, KPI e degraded mode. Le responsabilità restano separate:

- AP-004 governa telemetry e observability;
- AP-005 governa identity e privileged access;
- AP-006 governa configuration baseline, change tecnico e rollback;
- AP-003/AP-010 governano automation e safety assurance;
- BKL-032 resta autorità per readiness/go-no-go;
- gli interlock fisici/locali restano l’unica Safety Authority.

Il package non autorizza transport live, runtime activation, scheduling, device command, automatic remediation, score promotion, soglie scientifiche o prove fisiche/OAT.

## 4. Ownership bootstrap

| Ruolo | Stato repository | Regola |
|---|---|---|
| Project Owner / Architecture Sponsor | Massimo Mainini | verificato dal package e dal mandato |
| Service Owner | DA VALIDARE | nessuna nomina inventata |
| Technical Owner | DA VALIDARE | nessuna nomina inventata |
| Operator | DA VALIDARE | nessuna nomina inventata |
| Incident Coordinator | DA VALIDARE | nessuna nomina inventata |
| Change Approver | DA VALIDARE | separato dalla Safety Authority |
| Safety Authority | interlock fisici/locali | non trasferibile ad AP-007 |
| Security Authority | DA VALIDARE; boundary AP-005 | nessuna nomina inventata |
| Documentation Governor | DA VALIDARE | nessuna nomina inventata |
| Architecture Review Board | review indipendente richiesta | non sostituibile dall'autore |

La voce `DA VALIDARE` è uno stato governato, non un'approvazione implicita. L'assegnazione dei ruoli operativi richiede evidence o decisione owner esplicita prima di una dichiarazione `READY`.

## 5. Gap classificati

- `missing`: service catalog e owner nominati formalmente;
- `missing`: RACI operativo e sostituti;
- `missing`: support hours, on-call ed escalation verificati;
- `missing`: baseline SLI misurata;
- `missing`: test end-to-end di runbook, recovery e degraded mode;
- `blocked`: qualsiasi claim di disponibilità/SLO numerico senza baseline;
- `blocked`: qualsiasi passaggio a readiness operativa senza review e evidence.

## 6. Acceptance criteria della tranche

- baseline e dipendenze riconciliate contro repository;
- ownership distinta da Safety Authority e marcata `DA VALIDARE` dove manca evidence;
- vincoli BKL-036 e BKL-032 preservati;
- nessuna capability runtime o comando introdotta;
- handover compatto prodotto;
- package pronto per ARB, non ancora approvato.

## 7. Validazioni

Eseguite per ispezione repository:

- AP-007 e OPS-REF-001 recuperati dal default branch;
- AMP-002, traceability register, knowledge graph, roadmap e mandato confrontati;
- dipendenze AP-003…AP-006 e AP-010/BKL-032 ricondotte ai rispettivi boundary;
- assenza di nomine operative non supportate registrata esplicitamente.

Non eseguite:

- `mkdocs build --strict`;
- link checker;
- review ARB indipendente;
- test operativo, recovery, on-call o runbook;
- qualsiasi attività live o OAT.

## 8. Decisione

La baseline AP-007 è reconciled e il package è candidato alla review ARB indipendente. La tranche non promuove AP-007 a `Accepted` o `Operationally Verified`; il prossimo gate è la review ARB con matrice Release Quality.
