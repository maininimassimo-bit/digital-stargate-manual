# BKL-042 F6 — Read-Only Chat Acceptance Package

| Gate | Stato | Evidenza |
|---|---|---|
| Contract | PASS | `schemas/bkl042-f6-read-only-chat.schema.json` |
| Bounded fixture | PASS | `docs/data/bkl042-f6-read-only-chat-fixture.json` |
| Static consumer | PASS | `docs/bkl042-chat/index.md` |
| Fail-closed authority | PASS | `.github/scripts/verify-bkl042-f6-chat.mjs` |
| ARB | Conditional / AI-assisted | `docs/architecture/reviews/ARB-BKL042-F6-READ-ONLY-CHAT-2026-09-23.md` |
| Release Quality | Conditional / AI-assisted | `docs/architecture/reviews/RQ-BKL042-F6-READ-ONLY-CHAT-2026-09-23.md` |
| Runtime AI provider | PASS — BOUNDED OAT | `docs/architecture/validation/BKL-042-F6-PORTAL-OAUTH-OAT-EVIDENCE-2026-09-23.md` |

## Decisione

F6 è accettata come consumer bounded, advisory e read-only con ingresso Google
OAuth e relay provider separato sottoposto a OAT owner-witnessed. Il pacchetto non
abilita una chat AI operativa, retrieval generico, tool, comandi o Safety Authority.

La promozione oltre questo livello richiede gate separati per retrieval, storage,
processing, tool, command path e Safety Authority.
