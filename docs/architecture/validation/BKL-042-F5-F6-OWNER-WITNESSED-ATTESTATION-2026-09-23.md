# BKL-042 F5/F6 — Owner-Witnessed Attestation

| Campo | Stato |
|---|---|
| Owner / accountable | Massimo Mainini |
| Attestazione | **ACCEPTED — OWNER-WITNESSED** |
| Baseline tecnica | `33c8217b` |
| Scope | F5 bounded technical closure, F6 static consumer e runtime dry-run |
| Provider / external traffic | None / not authorized |

## Oggetto dell'attestazione

L'owner deve confermare di aver verificato che:

- F5 resta `ACCEPTED_READ_ONLY_WITH_LIMITATIONS` solo sul piano tecnico;
- l'evidenza scientifica resta `NOT_EVALUABLE_CURRENT_EVIDENCE`;
- F6 è limitata a contratto, fixture e consumer statico deterministico;
- il runtime dry-run restituisce `NOT_AUTHORIZED`;
- provider, credenziali, traffico esterno, retrieval runtime, tool, comandi,
  remediation, scheduling e Safety Authority non sono autorizzati;
- review ARB/RQ assistite non sono approvazioni umane indipendenti.

## Decisione owner

Da compilare esclusivamente dall'owner dopo verifica del commit e delle evidenze:

`[ ] ACCETTO il perimetro bounded read-only sopra descritto.`

`[ ] NON ACCETTO / RICHIEDO CORREZIONI.`

| Campo | Valore da compilare dall'owner |
|---|---|
| Nome | Massimo Mainini |
| Data/ora | |
| Commit verificato | `52403dfb` |
| Note / condizioni | F5/F6 bounded read-only accettati; provider e traffico esterno non autorizzati |
| Firma o attestazione | Massimo Mainini — conferma registrata il 23/09/2026 |

La formal acceptance bounded di F5/F6 è registrata. La promozione F6 runtime/provider
resta un gate separato e `NOT_AUTHORIZED`.
