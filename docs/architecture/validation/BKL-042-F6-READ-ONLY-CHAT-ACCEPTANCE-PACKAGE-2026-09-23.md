# BKL-042 F6 — Read-Only Chat Acceptance Package

| Gate | Stato | Evidenza |
|---|---|---|
| Contract | PASS | `schemas/bkl042-f6-read-only-chat.schema.json` |
| Bounded fixture | PASS | `docs/data/bkl042-f6-read-only-chat-fixture.json` |
| Static consumer | PASS | `docs/bkl042-chat/index.md` |
| Fail-closed authority | PASS | `.github/scripts/verify-bkl042-f6-chat.mjs` |
| ARB | Conditional / AI-assisted | `docs/architecture/reviews/ARB-BKL042-F6-READ-ONLY-CHAT-2026-09-23.md` |
| Release Quality | Conditional / AI-assisted | `docs/architecture/reviews/RQ-BKL042-F6-READ-ONLY-CHAT-2026-09-23.md` |
| Runtime AI provider | NOT IMPLEMENTED | Gate futuro separato |

## Decisione

F6 è accettabile esclusivamente come consumer statico deterministico, bounded,
advisory e read-only. Il pacchetto non abilita una chat AI operativa, non abilita
provider o retrieval runtime e non cambia il perimetro di sicurezza.

La promozione oltre questo livello richiede chiusura formale F5, owner-witnessed
acceptance e un nuovo package per provider/runtime.
