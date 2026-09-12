# BKL-046 F5-A — Validation Remediation Evidence

| Campo | Valore |
|---|---|
| Evidence ID | BKL-046-F5A-REMEDIATION-EVIDENCE-001 |
| Data | 12/09/2026 |
| Stato | Technical remediation exact-head CI green; ARB/RQ re-review pending |
| Pull request | #178 |
| Remediation head | `df1fd85ea2bf2e058bcbca17ca5ace704acbab8a` |
| Parent review-publication head | `d83675a3307d6bb8275acfbcc2b5b617cc8b404d` |
| Governing review | `ARB-BKL-046-F5A-AI-ASSISTED-R1` — `REWORK REQUIRED` |
| Scope | Remediation `ARB-F5A-M01`, `ARB-F5A-M02` e `ARB-F5A-C01` |
| Explicitly excluded | F5-A acceptance, F5-B/F5-C, merge, AI model, scientific effectiveness, production/apply authority |

## 1. Outcome

Il remediation head chiude tecnicamente i due finding Major e il finding Minor della prima review F5-A. Gli stessi probe che erano accettati dal technical head precedente ora falliscono chiuso. Questa evidence supporta una re-review, ma non sostituisce ARB/RQ e non promuove F5-A ad Accepted.

## 2. Finding disposition

| Finding | Remediation | Evidence | Candidate disposition |
|---|---|---|---|
| `ARB-F5A-M01` | F5 riusa `validateHumanDecisionReceipt()` e `validateStableId()` del contratto F2; il validator F2 applica stable ID, item shape e bound di edit/rationale | F5A-UT-024; F2 regression 17/17; schema-binding verifier | Resolved pending re-review |
| `ARB-F5A-M02` | `validateSourceSet()` richiede equality esatta di directory e regex canoniche | F5A-UT-025 e probe con digest ricalcolato | Resolved pending re-review |
| `ARB-F5A-C01` | F5 invoca `validateAdvisoryProjection()` canonico prima dei controlli catalog-specific | F5A-UT-023 con internal drift e digest ricalcolato | Resolved pending re-review |

## 3. Contract changes

Il contratto runtime F2 espone limiti machine-readable riusabili:

- stable ID: lunghezza 2..128 e pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$`;
- Human Decision edits: massimo 32;
- edit parameter ID: massimo 256;
- edit unit: massimo 64;
- edit reason: massimo 2.048;
- decision rationale: massimo 4.096.

Il verifier F5 confronta questi limiti con `ai-post-processing-assistant-f2.schema.json` e verifica che lo schema raw F5 referenzi direttamente `$defs/humanDecisionReceipt` di F2. La CI esegue i negative test di conformance oltre al parse dei due schema.

## 4. Reproduced review probes

| Probe | Previous head | Remediation head |
|---|---|---|
| F2-invalid receipt con ID non stabile, actor corto, edit arbitrario e rationale oltre bound | accepted | `FAIL_CLOSED` — stableId pattern rejection |
| source-set con directory errata, wildcard pattern e digest ricalcolato | accepted | `FAIL_CLOSED` — canonical directory rejection |
| F4 internal decision-state drift con record/projection digest ricalcolati | non coperto direttamente | `FAIL_CLOSED` — canonical F4 validator rejection |

## 5. Exact-head CI evidence

| Workflow | Run | Result |
|---|---:|---|
| BKL-046 F5 governance | `34682668900` | SUCCESS |
| BKL-046 F2 Governance | `34682668926` | SUCCESS |
| BKL-046 F3 Governance | `34682668936` | SUCCESS |
| BKL-046 F4 governance | `34682668937` | SUCCESS |
| BKL-041 F4 Governance | `34682668968` | SUCCESS |
| Validate documentation | `34682668950` | SUCCESS |
| Developer Foundation | `34682668898` | SUCCESS |
| Genera manuale Word | `34682668903` | SUCCESS |

Il job F5 registra:

- F5-A: 25 test, 25 PASS, 0 FAIL;
- F2 regression: 17 test, 17 PASS, 0 FAIL;
- persisted evaluation `--check`: PASS;
- registry, source contract e deterministic reconstruction verifier: PASS;
- regressioni F3, F4 projection e F4 consumer: PASS.

## 6. Known answer retained

La remediation non modifica gli input o il report persistito. Restano invariati:

| Field | Value |
|---|---|
| Evaluation ID | `BKL046-F5A-F4FEB5E207DD3F7D3E4F6C87` |
| Evaluation digest | `174f8d75a27160b476c65d2670c50e4089811834dd1e5867418c77dfbac41f70` |
| Canonical sessions | 15 |
| Exact provenance eligible | 0 |
| Human Decision receipts / execution evidence | 0 / 0 |
| Scientific state | `NOT_EVALUABLE_CURRENT_EVIDENCE` |
| Production state | `NOT_READY_FOR_PRODUCTION` |
| Closure recommendation | `KEEP_OPEN` |
| AI model implemented | `false` |

## 7. Remaining gates

1. pubblicare una nuova ARB/RQ re-review sul remediation head o sul solo evidence-publication descendant;
2. non riusare `W-BKL046-F5A-REVIEW-001`, già consumata;
3. ottenere un esito favorevole e CI verde sul relativo publication head;
4. richiedere separatamente autorizzazione al merge e disposizione per l'assenza di branch protection;
5. mantenere F5-B/F5-C `NOT_EXECUTED` fino all'acceptance F5-A.

## 8. Traceability

- [F5-A ARB R1](../reviews/ARB-BKL-046-F5A-AI-Assisted-Implementation-Review-2026-09-12.md)
- [F5-A RQ R1](../reviews/RQ-BKL-046-F5A-AI-Assisted-Release-Quality-Review-2026-09-12.md)
- [F5 validation plan](BKL-046-F5-Real-Evidence-Evaluation-Plan.md)
- [F5 architecture](../scientific-assets/BKL-046-F5-Real-Evidence-Evaluation-and-Capability-Closure.md)
- [PR #178](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/178)
