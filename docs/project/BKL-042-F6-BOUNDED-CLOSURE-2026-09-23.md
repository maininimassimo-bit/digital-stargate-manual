# BKL-042-F6 — Bounded Read-Only Closure

| Campo | Valore |
|---|---|
| Identificativo | BKL-042-F6 |
| Stato | ACCEPTED / BOUNDED GATE / OWNER-WITNESSED |
| Baseline | `52403dfb` |
| Owner | Massimo Mainini |
| Authority | Advisory/read-only; action/command/execution/safety `NONE` |

## Decisione

BKL-042-F6 è chiusa limitatamente al contratto, fixture, consumer statico e runtime
adapter dry-run bounded. La milestone non include un modello AI, provider, retrieval
runtime o traffico esterno.

## Evidenza accettata

- contratto chat: `schemas/bkl042-f6-read-only-chat.schema.json`;
- fixture citabile: `docs/data/bkl042-f6-read-only-chat-fixture.json`;
- consumer Pages: `docs/bkl042-chat/index.md`;
- dry-run adapter: `docs/data/bkl042-f6-runtime-adapter-dry-run.json`;
- owner-witnessed acceptance: `docs/architecture/validation/BKL-042-F5-F6-OWNER-WITNESSED-ATTESTATION-2026-09-23.md`;
- baseline owner-verified: `52403dfb`.

## Limitazioni mantenute

- evidenza scientifica: `NOT_EVALUABLE_CURRENT_EVIDENCE`;
- runtime provider: `NOT_READY / NOT_AUTHORIZED`;
- provider, secret, external call, upload, tool, PixInsight apply, command,
  remediation, scheduler e Safety Authority: non autorizzati;
- review assistite ARB/RQ: non equivalenti ad approvazioni umane indipendenti.

## Stop condition

Il lavoro si interrompe prima di selezionare provider, creare credenziali o generare
traffico esterno. Per superare questo confine serve una nuova decisione/autorizzazione
esplicita dell’owner e un package runtime separato.

## Addendum post-authorization — 23/09/2026

Con autorizzazione owner separata, il gate portal-ingress Google OAuth e il relay
provider sono stati trattati in package runtime distinti. Il relativo OAT
authenticated live è passato con evidenza owner-witnessed; questa chiusura storica
resta valida per il perimetro statico/dry-run originario e non viene interpretata
come autorizzazione a tool, retrieval generico, upload, processing, command path o
Safety Authority.
