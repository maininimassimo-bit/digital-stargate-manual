# Repository Knowledge Map

| Campo | Valore |
|---|---|
| Identificativo | DSG-GOV-KM-001 |
| Versione | 5.2 |
| Stato | Active |
| Data | 15/09/2026 |
| Root bootstrap | `AI_BOOTSTRAP.md` |
| Current governed package | F3-A3 decision-preparation: Solution Architecture, proposed ADR-010 and not-executed validation-spike plan |

## 1. Scopo

Mappa domini, authority, projection e percorsi di conoscenza. Non sostituisce le fonti canoniche.

## 2. Continuity hierarchy

1. `AI_BOOTSTRAP.md`;
2. current handover e technical baseline 15/09/2026;
3. Enterprise Architecture Context;
4. questo Knowledge Map;
5. `DSG-AEM-001-CONTINUOUS-AUTONOMOUS-EXECUTION-MANDATE-2026-09-15.md`;
6. `BACKLOG.md`;
7. canonical roadmap source;
8. generated roadmap projection;
9. Technical Debt, Decision Log, Development Workflow, Coding Standards e Release Playbook;
10. AMP-002 e package/review/evidence coinvolti.

## 3. Authority / projection map

Authority: repository, Architecture Package/ADR, backlog, canonical roadmap, registri, closure/review/workflow/evidence.

Projection: roadmap JSON, cataloghi/read model scientifici, Observatory Status, Timeline/Replay, Equipment Performance, Session Comparison e Analytics Center.

Ogni consumer preserva source locator, semantic type, lifecycle, Citation, Provenance, quality e completeness dove previsti.

## 4. Accepted foundation

BKL-015, BKL-044, BKL-035, BKL-040, BKL-038, BKL-039, BKL-045, BKL-037, BKL-041 e BKL-046 sono accepted. AP-013 resta authority degli asset; AP-014 resta catalog/synchronization boundary.

## 5. BKL-037 closed baseline

Session Comparison è read-only/descriptive-only. Confronta esclusivamente dimensioni/unità/provenance compatibili, conserva exclusions e non crea ranking, score, threshold, recommendation o authority.

## 6. BKL-046 closed and BKL-031 current

BKL-046 è CLOSED / ACCEPTED / POST-MERGE VERIFIED come capability deterministica advisory read-only tramite PR #181 e merge `3d680dd3a05c70b2a4654c4187c293e36b0af4a7`. Scientific effectiveness resta `NOT_EVALUABLE_CURRENT_EVIDENCE`, production `NOT_READY_FOR_PRODUCTION`, `aiModelImplemented=false`; nessun apply path o Safety Authority è autorizzato.

BKL-031 F1/F2 e l'handoff F3 sono ACCEPTED / POST-MERGE VERIFIED. F3-A1 è integrato tramite PR #193 e riconciliato tramite PR #194. F3-A2 handoff e detailed contract sono accepted with conditions/post-merge verified via PR #195 e #197; AP-006 governance, concrete baseline evidence, current assignment e observed drift restano separati. ADR-009 governa i registri protetti. The first setup baseline and Site Authority are independently approved. PR #204 integrated the Site Authority lifecycle; PR #205 reconciled acceptance as `d5f403bbe6a39731213c372cb22296324d10b03d` with 9/9 post-merge workflows. F3-A2-D3 source, roles, separation and validity decisions are complete and stored as protected evidence. PR #207 integrated the F3-A2-D4 protected `CurrentSetupAssignment` DRAFT, closed schemas, validator and 57/57 tests. The Repository Owner subsequently approved its exact protected digest; PR #209 integrated the receipt and unchanged `APPROVED` envelope as `bc4307c2042a45985622044e11631421de5b2c3d`, with 65/65 tests and 7/7 post-merge workflows. Repository authority is `AVAILABLE` for authorized validated input. No runtime adapter exists: S08 is `UNAVAILABLE`, S09 is `UNAVAILABLE_CURRENT`. `ARB-204-MI01` and `ARB-204-MI02` remain preconditions for later revisions/adapters. S07/S11, F3-A3/B/C, F4 forecast, F5 ranking/consumer, BKL-032 readiness and Safety remain separate.

## 7. Roadmap sequence

`... -> BKL-037 CLOSED -> BKL-041 CLOSED -> BKL-046 CLOSED -> BKL-031 [F1/F2 ACCEPTED / F3 SA ACCEPTED / F3-A1+A2 REPOSITORY AUTHORITIES ACCEPTED / F3-A3 DECISION PREPARATION CURRENT / ADR-010 PROPOSED / S10 UNAVAILABLE] -> BKL-032 -> BKL-036 -> BKL-033 -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.

## 8. CI/CD e publishing

Workflow e deployment sono evidence solo per l’exact SHA verificato. Generated projection non è authority.

## 9. Safety boundary

Nessun consumer analytics, comparison, scoring o AI può comandare apparati, autorizzare remediation o sostituire gli interlock fisici.

## 10. Registro revisioni

| Versione | Data | Descrizione |
|---|---|---|
| 1.0 | 04/08/2026 | Prima repository knowledge map |
| 2.0 | 08/09/2026 | Continuity e knowledge foundation |
| 2.1 | 10/09/2026 | BKL-037 current |
| 2.2 | 10/09/2026 | BKL-037 closed/accepted e BKL-041 current |
| 2.3 | 11/09/2026 | BKL-041 closed/accepted e BKL-046 F1 current |
| 2.4 | 11/09/2026 | BKL-046 F1 accepted e F2 current |
| 2.5 | 11/09/2026 | BKL-046 F2 accepted e F3 current |
| 2.6 | 11/09/2026 | BKL-046 F3 accepted e F4 current |
| 2.7 | 12/09/2026 | BKL-046 F4 accepted/post-merge verified e F5 design current |
| 2.8 | 13/09/2026 | BKL-046 closed/accepted/post-merge verified e BKL-031 F1 current |
| 2.9 | 14/09/2026 | BKL-031 F1 accepted/post-merge verified; F2 current handoff only |

| 3.0 | 14/09/2026 | BKL-031 F2 accepted/post-merge verified; successor decision pending |

| 3.1 | 14/09/2026 | BKL-031 F3 promoted as current handoff only |

| 3.2 | 14/09/2026 | BKL-031 F3 Solution Architecture review candidate |


| 3.3 | 14/09/2026 | BKL-031 F3 Solution Architecture AI-assisted ARB/RQ complete; merge decision pending |


| 3.4 | 14/09/2026 | BKL-031 F3 Solution Architecture accepted with conditions; implementation decision pending |
| 3.5 | 15/09/2026 | PR #192 closure integrated; F3-A1 Site Authority Contract review candidate current |
| 3.6 | 15/09/2026 | PR #193 F3-A1 merged/post-merge verified; Acceptance Reconciliation current |
| 3.7 | 15/09/2026 | PR #194 F3-A1 reconciliation merged/post-merge verified; F3-A2 handoff current |
| 3.8 | 15/09/2026 | PR #195 F3-A2 handoff post-merge verified; DSG-AEM-001 active; detailed contract next |
| 3.9 | 15/09/2026 | PR #196 mandate post-merge verified; F3-A2 detailed contract and validation plan current |
| 4.0 | 15/09/2026 | PR #197 F3-A2 contract accepted/post-merge verified; concrete authority decision gate current |

| 4.1 | 15/09/2026 | ADR-009 authority model owner-authorized; first protected baseline payload remains DRAFT pending exact-digest approval |

| 4.2 | 15/09/2026 | PR #199 authority/DRAFT integrated and post-merge verified; exact-digest owner gate current |

| 4.3 | 15/09/2026 | Exact-digest owner approval recorded; PR #201 receipt and `APPROVED` lifecycle envelope under review |


| 4.4 | 15/09/2026 | PR #201 merged/post-merge verified; F3-A1-M1 Site Authority owner decision gate current |
| 4.5 | 15/09/2026 | PR #202 baseline verified; F3-A1-M1 decisions complete; F3-A1-M2 protected DRAFT review candidate and exact-digest approval next |
| 4.6 | 15/09/2026 | PR #204 Site Authority approval accepted/post-merge verified; F3-A2-D3 CurrentSetupAssignment owner decision gate current |
| 4.7 | 15/09/2026 | PR #205 reconciliation verified; F3-A2-D3 owner decisions complete and F3-A2-D4 DRAFT handoff next |
| 4.8 | 15/09/2026 | PR #207 D4 protected DRAFT accepted/post-merge verified; mandatory human exact-digest approval next |
| 4.9 | 15/09/2026 | Exact-digest assignment approval received; PR #209 receipt/promotion review candidate with 65/65 implementation tests |
| 5.0 | 15/09/2026 | PR #209 D5 accepted/post-merge verified; repository authority AVAILABLE; runtime adapter absent; successor selection current |
| 5.1 | 15/09/2026 | PR #210 D5 reconciliation accepted/post-merge verified; F3-A3 documentation-only handoff current; no provider selected |
| 5.2 | 15/09/2026 | PR #211 handoff integrated/post-merge verified; F3-A3 Solution/ADR/validation decision-preparation review candidate |

## F3-A2-D4 acceptance checkpoint — 15/09/2026

PR #207 merged as `e99e6b5ff5ea7247ee447a1c6c62dcaa479dee1b` after 5/5 exact-head workflows and completed 7/7 post-merge workflows. Closed schemas, exact-reference binding, canonical identity, fail-closed resolution, privacy enforcement and 57/57 cases are integrated. No assignment approval, runtime adapter or public protected projection exists. The current mandatory transition is human exact-digest approval or rejection.


## F3-A2-D5 approval checkpoint — 15/09/2026

PR #209 is ACCEPTED / POST-MERGE VERIFIED at merge `bc4307c2042a45985622044e11631421de5b2c3d`. It retains the historical DRAFT, preserves the assignment payload/digest, integrates the protected receipt and resolves `AVAILABLE` only in repository authority for authorized validated input with approved sources. The 65-case suite and all 7 post-merge workflows passed. Runtime S09 remains `UNAVAILABLE_CURRENT`; adapter, EAGLE and Safety Authority are outside scope.

## F3-A3 current handoff

The Program Architect selected F3-A3 after repository-authority completion for F3-A1/A2. The Solution Architect must prepare the method ADR and validation-spike plan for F3-OD04–F3-OD10. This mapping does not authorize dependencies, kernels, external calls, protected-site use, thresholds or runtime; S10 remains `UNAVAILABLE`.


## F3-A3 decision-preparation package

Authority remains the repository and future accepted ADR-010. Official-source observations and candidate versions are evidence inputs, not authority or approved pins. BKL-031-F3-A3-SOLUTION-001 defines the source-neutral boundary; ADR-010 exposes F3-OD04–F3-OD10; BKL-031-F3-A3-VAL-001 defines a synthetic, bounded campaign that is NOT EXECUTED. No provider, kernel, threshold, host, external call or runtime is selected.
