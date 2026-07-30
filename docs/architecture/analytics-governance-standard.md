# ANA-GOV-001 — Analytics Governance Standard

| Campo | Valore |
|---|---|
| Identificativo | ANA-GOV-001 |
| Package | AP-011 |
| Stato | Proposed for review |
| Data | 30/07/2026 |

## Purpose

Governare ownership, qualità, pubblicazione, accesso, lifecycle e uso responsabile degli analytics Digital StarGate.

## Roles

- **Data Product Owner** — accountable per scopo, qualità, consumer e lifecycle.
- **Data Steward** — definizioni, metadati, qualità e issue remediation.
- **Pipeline Owner** — operatività, failure handling, capacity e recovery.
- **KPI Owner** — formula, interpretazione, soglie e change approval.
- **Model Owner** — performance, drift, limitazioni e retirement.
- **Platform Owner** — servizi DSAP, accesso, patching, backup e observability.
- **ARB** — review delle decisioni architetturali e delle eccezioni.

## Mandatory controls

1. Nessun dataset pubblicato senza owner e schema versionato.
2. Nessun KPI pubblicato senza formula, grain, unità e quality dependency.
3. Nessun modello promosso senza baseline, validation e human review.
4. Ogni breaking change richiede nuova major version e migration plan.
5. Accesso secondo least privilege, classificazione e audit.
6. Retention e deletion devono essere approvate e verificabili.
7. Dati stale, incompleti o `unknown` devono essere visibili al consumer.
8. Eccezioni temporanee hanno owner, motivazione, expiry e compensating control.
9. Dashboard non possono introdurre definizioni KPI locali non registrate.
10. Analytics e AI non sono Safety Authority e non dispongono di command path.

## Lifecycle

`draft -> proposed -> approved -> active -> deprecated -> retired`

La promozione richiede evidence proportionate a criticità, consumer e impatto. Il retirement richiede consumer analysis, export/retention decision e aggiornamento della documentazione.

## Change governance

Ogni modifica registra:

- change ID e owner;
- artefatti impattati;
- schema/KPI/model version;
- compatibility assessment;
- data quality and security impact;
- migration and rollback;
- validation evidence;
- approval and effective date.

## Model governance

I modelli sono classificati come descriptive, diagnostic, predictive o prescriptive-advisory. Il livello prescriptive non implica esecuzione automatica. Sono obbligatori dataset lineage, metriche, bias/coverage assessment dove applicabile, drift monitoring, explainability, fallback e retirement criteria.

## Evidence and review

L'evidence minima comprende contract tests, quality results, lineage, access review, recovery test, performance baseline, KPI validation e, quando presenti, model validation e drift report.

## Exceptions

Le eccezioni non possono derogare ai vincoli safety di AP-010, all'assenza di command path o alla necessità di attribuire ownership e audit.