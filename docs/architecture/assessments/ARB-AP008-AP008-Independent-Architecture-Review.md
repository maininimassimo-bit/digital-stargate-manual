# ARB-AP008 — Independent Architecture Review of AP-008

| Campo | Valore |
|---|---|
| Identificativo | ARB-AP008 |
| Oggetto | AP-008 — Enterprise Integration Architecture |
| Baseline reviewed | main @ 162ae63dd80eb69fd6e99c68e91807dafc8ab386 |
| Data | 22/09/2026 |
| Decisione | Rework Required |

## 1. Scope and evidence

La review verifica AP-008, INT-REF-001, INT-CAT-001, il transport Observatory Status e la traceability corrente. La review non certifica runtime, middleware, command path o Safety Authority.

Evidence verificata:

- AP-008 è marcato Proposed for independent ARB review.
- INT-REF-001 è technology-neutral e separa Domain, Application, EIF, adapter ed External Systems.
- INT-CAT-001 è ancora un candidate catalog non operationally authorized.
- Il transport Observatory Status resta In development.
- L'importazione scientifica Quattro 200P + ToupTek 294MC PRO è prova di una pipeline batch documentale, non di un EIF runtime event.

## 2. Scoring

| Dimensione | Score | Evidenza sintetica |
|---|---:|---|
| Boundary e dependency direction | 88 | Domain isolato; adapter e EIF definiti |
| Contract model | 82 | envelope, command/event/query e versioning definiti; catalogo candidato |
| Reliability | 78 | retry, timeout, inbox/outbox, DLQ e reconciliation descritti; test assenti |
| Security e safety | 84 | trust boundary e local authority preservate; review adapter non eseguita |
| Observability | 80 | correlation, freshness e SLI candidati definiti |
| Operability e rollback | 65 | readiness model presente; runbook e disable evidence mancanti |
| Traceability | 62 | riferimenti presenti; review AP-008 e owner non registrati |
| Validation evidence | 45 | nessun contract, compatibility, replay o failure test AP-008 eseguito |

## 3. Findings

### Blocker

- Nessuna review indipendente AP-008 era registrata.
- Non esiste un contratto approvato e testato per il pilot.
- Non esiste evidence di adapter runtime, autenticazione, replay, reconciliation o rollback.
- Il transport Observatory Status non è un relay deployato e non può essere considerato active integration.

### Major

- Owner di contract registry e adapter non assegnati.
- Protocolli, timeout, retention, rate limit e payload limits non sono deliberati.
- Security review e threat model degli adapter non sono eseguiti.
- Failure e recovery scenarios non sono stati provati.

### Minor / Observation

- I command candidate devono restare esplicitamente non autorizzati.
- La pipeline sessionale pubblicata su GitHub deve essere classificata come document transfer pilot, non come event bus.
- Le condizioni UNKNOWN/STALE e la Safety Authority locale devono restare invariati.

## 4. Decision

AP-008 è coerente come baseline architetturale, ma non è pronto per approvazione. Decisione: Rework Required.

Il primo incremento autorizzabile è INT-SESSION-METADATA-PILOT-001: pilot read-only, non safety-critical, senza comandi e senza scheduler operativo aggiuntivo.

## 5. Re-review criteria

La re-review richiede:

1. owner e lifecycle record per il contratto pilot;
2. schema e compatibility test;
3. duplicate, replay, timeout e failure mapping test;
4. security/trust review dell'adapter;
5. runbook di disable/rollback;
6. evidence di osservabilità e freshness;
7. evidence del pilot e riconciliazione;
8. aggiornamento di traceability e MkDocs.

Fino al superamento dei criteri, AP-008 resta Proposed e nessun command path è autorizzato.