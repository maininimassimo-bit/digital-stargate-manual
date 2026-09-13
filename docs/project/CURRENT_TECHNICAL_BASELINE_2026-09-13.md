# Digital StarGate Current Technical Baseline — 13/09/2026

| Campo | Valore |
|---|---|
| Stato | Current technical continuity baseline |
| Data | 13/09/2026 |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Current main baseline | `8ed6085d15f6af9e466a90167f19e970e8c526a7` |
| Current governed package | BKL-046 — AI Post-Processing Assistant for PixInsight |
| Current increment | BKL-046 F5-C — deterministic closure candidate |
| Accepted predecessor | F5-B, PR #179; runtime/Pages evidence completed after PR #180 |

## 1. Current verified state

| Elemento | Valore |
|---|---|
| Canonical sessions | 16 |
| F4 records | 16 |
| F5 catalog snapshot | 16 |
| Evidence session | `2026-09-12_2026-09-13` |
| Analysis run | `34766534178` — SUCCESS |
| Analytics commit | `8ed6085d15f6af9e466a90167f19e970e8c526a7` |
| Pages run | `34766571069` — SUCCESS |
| Live freshness | `FRESHNESS CHAIN VERIFIED` |

## 2. F5-C contract candidate

- schema version `2.0`;
- evaluation state `F5C_CLOSURE_EVALUATED`;
- producer version `2.0.0-f5c`;
- method `BKL046-F5C-CLOSED-EVALUATION-1`;
- registry `BKL046-F5C-CLOSED-REGISTRY-1`;
- evaluation ID prefix `BKL046-F5C-`;
- `F5B_DYNAMIC_UPDATE = PASS`;
- `F5B_CONSUMER = PASS`;
- technical/capability outcome `ACCEPTED_READ_ONLY_WITH_LIMITATIONS`;
- closure recommendation `CLOSE_DETERMINISTIC_CAPABILITY`.

## 3. Retained data outcomes

- provenance eligible: 0;
- Human Decision Receipt: 0;
- execution evidence: 0;
- uncorrelated processing sources: 2;
- target distribution: LDN 1320 = 3, M 27 = 12, UNKNOWN = 1;
- scientific state: `NOT_EVALUABLE_CURRENT_EVIDENCE`;
- human decision state: `NOT_AVAILABLE`;
- production state: `NOT_READY_FOR_PRODUCTION`;
- `aiModelImplemented=false`.

## 4. Validation state

Local candidate validation: generator/check PASS, deterministic verifier PASS, 85/85 test aggregati F2-F5 PASS, inclusi 44/44 test della slice F5 evaluator + consumer; la generazione in memoria contro il catalogo pubblicato a 16 sessioni supera la validazione di freshness. GitHub exact-head CI, ARB/RQ, merge and post-merge verification non sono ancora eseguiti per F5-C.

## 5. Compatibility and rollback

Il contratto `2.0` è una major semantica perché sostituisce identity e stato F5-A con la closure F5-C. Il report, evaluator e consumer devono essere pubblicati atomicamente. Rollback: revert del commit F5-C e nuova pubblicazione Pages; F1-F5-B, catalogo e dati sessione restano intatti.

## 6. Operational limitation

Il rerun manuale duplicato della stessa finestra EAGLE termina correttamente ma come `DEFERRED/PARTIAL`, non come `NOOP/ALREADY_PUBLISHED`. Non è un blocker F5-C, ma richiede un incremento operativo separato.

## 7. Next gate

Exact-head CI sul branch F5-C. Nessuna review AI-assistita o closure acceptance può essere pubblicata senza nuova autorizzazione esplicita.
