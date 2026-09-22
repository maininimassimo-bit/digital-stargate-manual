# INT-SESSION-METADATA-PILOT-001 — Read-only Session Metadata Integration Pilot

| Campo | Valore |
|---|---|
| Identificativo | INT-SESSION-METADATA-PILOT-001 |
| Package | AP-008 |
| Stato | Proposed — not operationally authorized |
| Safety class | non_safety |
| Direzione | N.I.N.A. session metadata -> repository/portal projection |
| Baseline | main @ 162ae63dd80eb69fd6e99c68e91807dafc8ab386 |

## Scopo

Definire il primo slice AP-008 per metadata di sessione scientifica. Il pilot non invia comandi e non controlla dome, mount, camera, relay, PLC, CPWI, ASCOM, N.I.N.A. o PHD2.

Il pilot riusa il trasferimento governato di manifest, log e report già verificato dalla pipeline AP-014, ma non lo promuove automaticamente a event transport attivo.

## Contract candidate

- Contract ID: DSG.Observation.Event.SessionCompleted
- Version: 1.0.0 candidate
- Producer candidate: N.I.N.A. session adapter
- Consumer candidate: repository/analytics/portal projection
- Classification: internal
- Freshness: current, stale o unknown dichiarata nella projection
- Safety Authority: nessuna
- Command authority: NONE

Envelope minimo richiesto: contract_id, contract_version, message_id, occurred_at, published_at, correlation_id, producer, subject, schema_uri, classification, freshness, payload.

Il payload deve riferire session_id, manifest, checksum e provenance. Non deve contenere credenziali o comandi.

## Boundary

1. L'adapter legge metadata e file già disponibili.
2. La validazione rifiuta schema, checksum o session identity non validi.
3. La pubblicazione è idempotente per session_id e manifest digest.
4. Un duplicato produce no-op/reconciliation, mai una seconda sessione.
5. Un errore o un outcome non verificabile produce failure/unknown e non promuove dati a current.
6. Il consumer aggiorna solo proiezioni read-only.

## Acceptance tests

- schema validation positiva e negativa;
- session identity mismatch;
- checksum mismatch;
- duplicate delivery/idempotency;
- retry bounded su errore transient;
- no retry su authentication/authorization/schema reject;
- repository/portal projection reconciliation;
- disable path con nessuna perdita della Safety Authority locale;
- stale/missing evidence visualizzata come UNKNOWN o non disponibile.

## Exclusions

- nessun broker o provider selezionato;
- nessun relay live deployato;
- nessun scheduler aggiuntivo;
- nessun command contract attivato;
- nessuna promozione di N.I.N.A. a Safety Authority;
- nessuna modifica agli interlock locali.

## Exit criteria

Il pilot può passare a review solo quando owner, schema, compatibility evidence, security review, runbook, rollback/disable evidence e reconciliation report sono registrati. Prima di allora resta Proposed.

## Shadow evidence from real session

The real session `2026-09-21_2026-09-22` produced a shadow-only `DSG.Observation.Event.SessionCompleted` artifact and fail-closed diagnostic test:

- evidence: `docs/architecture/validation/INT-SESSION-METADATA-PILOT-001-Shadow-Diagnostic-2026-09-22.md`;
- shadow event: `docs/data/integration/session-completed-shadow-event-2026-09-21_2026-09-22.json`;
- test: `.github/scripts/test-session-completed-shadow-event.mjs`;
- runtime publication remains disabled;
- the diagnostic outcome is `YELLOW`, with three unmatched/interrupted LIGHT poses and one PHD2 settling failure preserved as diagnostic evidence.

This evidence does not authorize a live adapter, broker, scheduler change, command path or Safety Authority promotion.
