# BKL-042 F6-R — Runtime Readiness Gate

| Check | Stato |
|---|---|
| F5 formal owner-witnessed closure | OPEN |
| F6 bounded consumer acceptance | CONDITIONALLY ACCEPTED |
| Provider selected | NO |
| Credentials / bearer token | NOT REQUESTED |
| External traffic | NOT AUTHORIZED |
| Tool / command path | NONE |
| Safety Authority | NONE |
| Runtime production readiness | NOT READY |

## Gate disposition

Il portale può restare sul consumer statico deterministico pubblicato. Non è autorizzata
la trasformazione in chat runtime. Prima di ogni provider decision devono essere
completati privacy/security review, data minimization, budget/consent, audit e fail-closed
tests indicati nel package architetturale.

## Exit criteria futuri

- F5 formalmente accettata;
- adapter provider isolato e dry-run verificabile;
- nessun secret nel client;
- provenance e citazioni obbligatorie nella risposta;
- failure e timeout senza fallback permissivo;
- review ARB/RQ/security/privacy e rollback approvati;
- post-merge CI e Pages verificati.
