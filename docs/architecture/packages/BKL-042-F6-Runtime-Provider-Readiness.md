# BKL-042 F6-R — Runtime Provider Readiness Package

| Campo | Valore |
|---|---|
| Stato | Readiness design only / provider not selected |
| Parent | BKL-042-F6 bounded read-only chat |
| Owner / accountable | Massimo Mainini |
| Runtime traffic | NOT AUTHORIZED |
| Authority | action/command/execution/safety `NONE` |

## Scopo

Definire i gate necessari prima di collegare un provider AI reale alla chat del portale.
Questo package non seleziona un provider, non invia dati, non crea credenziali e non
introduce un endpoint runtime.

## Prerequisiti obbligatori

1. Chiusura formale BKL-042-F5 con owner-witnessed acceptance.
2. Acceptance F6 bounded consumer post-merge verificata.
3. Data minimization e classificazione delle fonti/projection.
4. Threat model per prompt injection, data exfiltration, citation spoofing e stale data.
5. Identity, consent, secret handling, budget e rate-limit decision.
6. Audit schema per correlation ID, method/provider version, source digest e limitation.
7. Fail-closed contract per unavailable, conflict, stale, uncited o provider error.
8. ARB, Release Quality, security/privacy review e rollback plan.

## Limiti non negoziabili

- nessun tool calling o function calling nella prima integrazione;
- nessun upload automatico di immagini, sidecar o file locali;
- nessun PixInsight apply o modifica di parametri;
- nessun comando a osservatorio, mount, camera, power o network;
- nessuna remediation, scheduling, target selection o Safety Authority;
- nessuna esposizione di bearer token o credenziali nel browser.

## Decisione di gate

Il provider runtime resta `NOT_READY / NOT_AUTHORIZED`. Il prossimo lavoro autorizzabile
è solo la review del package e la definizione di un adapter dry-run senza traffico,
subordinata ai prerequisiti sopra elencati.
