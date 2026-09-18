# Repository Knowledge Map

| Campo | Valore |
|---|---|
| Identificativo | DSG-GOV-KM-001 |
| Versione | 6.1 |
| Stato | Active |
| Data | 17/09/2026 |
| Root bootstrap | `AI_BOOTSTRAP.md` |
| Current governed package | BKL-031, BKL-032 and BKL-036 Closed / Accepted / Post-Merge Verified; BKL-033 next; S10 production runtime `UNAVAILABLE` |

## 1. Scopo

Mappa domini, authority, projection e percorsi di conoscenza. Non sostituisce le fonti canoniche.

## 2. Continuity hierarchy

1. `AI_BOOTSTRAP.md`;
2. `docs/project/HANDOVER_2026-09-17.md`;
3. `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-17.md`;
4. `docs/project/ENTERPRISE_ARCHITECTURE_CONTEXT.md`;
5. questo Knowledge Map;
6. `DSG-AEM-001-CONTINUOUS-AUTONOMOUS-EXECUTION-MANDATE-2026-09-15.md`;
7. `BACKLOG.md`;
8. canonical roadmap source;
9. generated roadmap projection;
10. Technical Debt, Decision Log, Development Workflow, Coding Standards e Release Playbook;
11. AMP-002 e package/review/evidence coinvolti.

Handover e baseline precedenti restano snapshot storici e non prevalgono sulla baseline corrente.

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

BKL-031 è **CLOSED / ACCEPTED / POST-MERGE VERIFIED** tramite PR #301 e merge `4a509d574a004fe7fb72bc6c678c9e7f71fe821f`. F1/F2, F3-A1/A2/A3/B/C, F4-A/B/C/D, F5/F6/F7/F8 e F9 sono accettati; F3-C are Accepted / Post-Merge Verified; F4-A and ADR-011 are Accepted / Post-Merge Verified; F8 is Accepted / Post-Merge Verified. F9 ha verificato il refresh repeatable MeteoHub, astronomia della notte corrente, suitability setup/target, ranking esplicabile e pagina pubblica di Manciano. Budget provider storico `2/2_EXHAUSTED`; budget sito protetto `1/1_EXHAUSTED`; Recurring provider traffic is not authorized. Il budget monetario resta €0, con massimo due acquisizioni al giorno, fail-closed e GRIB effimeri senza retention. BKL-032 conserva la readiness/go-no-go authority; local physical interlocks remain Safety Authority; S10 production runtime is `UNAVAILABLE`; il planner resta read-only/advisory senza scheduler, selezione automatica, device command o Safety Authority.

## 7. BKL-032 closed baseline

BKL-032 is closed through PR #304 merge `7e38453b2e499fe577efa0231aeb7bb06329016e`. The accepted capability is a deterministic, read-only evaluator with versioned contracts, owner-approved thresholds and fail-closed missingness. Live source/transport acceptance and public runtime GO remain outside the closure. The governed handoff is **BKL-032 Session Readiness / Go-No-Go Decision Support** → **BKL-036 Observatory Health Score**.

## 8. BKL-036 closure state

BKL-036 is **CLOSED / ACCEPTED / POST-MERGE VERIFIED** for source discovery and semantic contract only through PR #306 merge `b0d3a8b1a10ce71610e4592d5c876e9fd0c8d7c5`. It does not introduce a numeric health score, thresholds, weights, Safety Score, remediation, runtime transport or device commands. BKL-031, BKL-032 and local physical interlocks remain separate authorities. The closure record is `docs/project/BKL-036-CLOSURE-2026-09-18.md`.

## 9. Roadmap sequence

`... -> BKL-037 CLOSED -> BKL-041 CLOSED -> BKL-046 CLOSED -> BKL-031 CLOSED / ACCEPTED -> BKL-032 CLOSED / ACCEPTED -> BKL-036 CLOSED / ACCEPTED -> BKL-033 -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.

## 10. CI/CD e publishing

Workflow e deployment sono evidence solo per l’exact SHA verificato. Generated projection non è authority.

## 11. Safety boundary

Nessun consumer analytics, comparison, scoring, planner o AI può comandare apparati, autorizzare remediation, produrre readiness/go-no-go come authority o sostituire gli interlock fisici. Le coordinate esatte del sito restano protette e non devono essere pubblicate nelle projection.

## 12. Registro revisioni

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
| 5.3 | 17/09/2026 | PR #258 F3-A3 scientific acceptance integrated/post-merge verified; ADR-010 accepted; F3-B authorized repository-only |
| 5.4 | 17/09/2026 | F3-B method/request/evidence schemas, bounded fixture and 34-case validator suite prepared for exact-head acceptance |
| 5.8 | 17/09/2026 | PR #263 F4-A source contract integrated and post-merge verified; ADR-011 accepted; F4-B machine-readable contracts promoted with zero provider traffic |
| 5.9 | 17/09/2026 | F4-B three-schema contract, synthetic TEST/NONE fixture and 24-case fail-closed validator prepared with zero provider traffic |
| 6.0 | 17/09/2026 | PR #265 F4-B integrated and post-merge verified; 26/26 tests and 14/14 workflows; F4-C acquisition-gate preparation promoted |
| 6.1 | 17/09/2026 | F8 Accepted/Post-Merge Verified via PR #279; continuity riallineata a handover/baseline 17/09 e F9 repeatable current-night planner closure promosso come unico successore |

Le sezioni di checkpoint seguenti sono snapshot storici. Eventuali formulazioni come “current” o “next” valgono al momento del relativo checkpoint e non prevalgono sulla baseline corrente definita nelle sezioni 2, 6 e 7.

## F3-A2-D4 acceptance checkpoint — 15/09/2026

PR #207 merged as `e99e6b5ff5ea7247ee447a1c6c62dcaa479dee1b` after 5/5 exact-head workflows and completed 7/7 post-merge workflows. Closed schemas, exact-reference binding, canonical identity, fail-closed resolution, privacy enforcement and 57/57 cases are integrated. No assignment approval, runtime adapter or public protected projection exists. The current mandatory transition is human exact-digest approval or rejection.

## F3-A2-D5 approval checkpoint — 15/09/2026

PR #209 is ACCEPTED / POST-MERGE VERIFIED at merge `bc4307c2042a45985622044e11631421de5b2c3d`. It retains the historical DRAFT, preserves the assignment payload/digest, integrates the protected receipt and resolves `AVAILABLE` only in repository authority for authorized validated input with approved sources. The 65-case suite and all 7 post-merge workflows passed. Runtime S09 remains `UNAVAILABLE_CURRENT`; adapter, EAGLE and Safety Authority are outside scope.

## F3-A3 scientific acceptance gate

F3-A3 owner decisions F3-OD04–F3-OD10, immutable method profile, exact runner, platform and kernel evidence are complete. Main-only run `35189574972` executed the remediated runner once: 8 synthetic vectors, 17/17 metrics, repeatability and transit passed. One create-only private evidence object was verified at raw SHA-256 `483794c9a8a373e8aff2f0dd2ab0f6342826c9bd210beeebcf92e744fad72494`. ADR-010 is Accepted for repository method authority. Further scientific execution, external-reference traffic, protected-site use and runtime remain unauthorized; S10 remains `UNAVAILABLE`.

## F3-A3 decision-preparation package

Authority remains the repository and accepted ADR-010. Official-source observations remain evidence inputs. The accepted profile selects the exact local primary, shared-SPK implementation cross-check, kernel, thresholds and host used by the passed campaign. No external reference, protected-site calculation or runtime is selected. F3-B may now materialize the source-neutral request/evidence contracts and validator.

## F3-B contracts and validator acceptance

F3-B materializes separate method-profile, request and evidence schemas plus one bounded synthetic fixture. The canonical contract digest is `b06932edb860cc4062b45d75b62e7874c3a327a4b4dbfd0b8cb70bdf115cd1f1`; 34 fail-closed and privacy tests passed locally and in governed CI. The fixture is `TEST` / `authority=NONE`, and the public projection omits protected coordinates and internal digests. Exact-head review, expected-head merge and all 11 applicable post-merge workflows passed. F3-C adapter, runtime activation, protected-site calculation and external-reference traffic remain unimplemented and separately gated.
