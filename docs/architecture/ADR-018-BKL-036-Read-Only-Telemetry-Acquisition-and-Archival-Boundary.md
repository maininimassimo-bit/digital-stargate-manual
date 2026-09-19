# ADR-018 — BKL-036 Read-Only Telemetry Acquisition and Repository Archival Boundary

| Campo | Valore |
|---|---|
| ID | ADR-018 |
| Stato | Proposed — BKL-036-F4 implementation candidate |
| Data | 2026-09-19 |
| Decision owner | Repository Owner |
| Scope | Acquisizione controllata e archiviazione di snapshot telemetry |
| Safety Authority | Interlock fisici locali |

## Decisione

BKL-036-F4 introduce un contratto per importare nel repository snapshot di telemetria già prodotti da una sorgente autorizzata. L'importer è read-only rispetto agli apparati: non apre connessioni live, non invia comandi, non abilita scheduling e non esegue remediation.

La pubblicazione di uno snapshot richiede sette domini espliciti: weather, dome, mount, camera, power, network ed eagle_health. Ogni dominio deve riportare fonte, authority, campo, unità, timestamp di osservazione, freshness, stato evidence, compatibilità, qualità e valore.

## Boundary

- source_plane=repository_evidence;
- acquisition_mode=read_only_snapshot_import;
- live_transport_used=false nel contratto F4;
- nessuna credenziale, segreto o dato personale nel payload;
- MISSING, STALE, UNAVAILABLE, PARTIAL e CONFLICTING non possono essere COMPARABLE;
- un archivio incompleto non promuove lo score F3: la proiezione resta UNAVAILABLE;
- gli interlock fisici locali restano l'unica Safety Authority.

## Current e target state

Oggi il repository contiene projection placeholder/unknown e un F3 score statico fail-closed. F4 aggiunge schema, fixture, validator e comando di archiviazione deterministico. L'attivazione di un producer dalla cupola, il trasporto live e una policy di retention operativa richiederanno un gate runtime separato.

## Acceptance criteria

- schema versionato e validator deterministico;
- sette domini obbligatori e nessuna duplicazione;
- rifiuto di live transport, comandi, scheduling e remediation;
- rifiuto di evidence incompleta classificata comparabile;
- fixture corrente accettata ma non promossa a score;
- test positivi e negativi bounded;
- traceability, roadmap, backlog e navigazione aggiornati.

## Conseguenze

F4 rende ingestibile una snapshot governata senza confondere repository evidence e telemetria live. Non rende disponibile automaticamente la telemetria della cupola e non certifica readiness, salute operativa o sicurezza.

## Riferimenti

- ADR-015 — BKL-036-F1 source mapping and evidence compatibility;
- ADR-016 — BKL-036-F2 evidence envelope;
- ADR-017 — BKL-036-F3 archived evidence score;
- BKL-032 — Session Readiness / Go-No-Go Decision Support.
