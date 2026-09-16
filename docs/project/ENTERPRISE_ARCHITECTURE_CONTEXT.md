# Digital StarGate Enterprise Architecture Context

| Campo | Valore |
|---|---|
| Identificativo | DSG-CTX-001 |
| Versione | 3.9 |
| Stato | Active context baseline |
| Data baseline | 15/09/2026 |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch autorevole | `main` |
| Root bootstrap | `AI_BOOTSTRAP.md` |
| Continuity handover | `docs/project/HANDOVER_2026-09-15.md` |
| Technical baseline | `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-15.md` |
| Current governed package | BKL-031 F3-A3 decision-preparation review candidate; ADR-010 proposed; owner decision pending |
| Owner | Massimo Mainini |

## 1. Scopo e gerarchia

Questo documento fornisce il contesto enterprise corrente. Il repository GitHub è source of truth; bootstrap, current handover, current baseline, Knowledge Map, backlog e canonical roadmap prevalgono sugli snapshot storici.

## 2. Authority e projection

- `BACKLOG.md`: stato, priorità e dipendenze;
- `.github/roadmap/roadmap-source.json`: roadmap funzionale canonica;
- `docs/data/roadmap.json`: projection generata;
- Architecture Package/ADR: decisioni e boundary;
- closure/review/workflow/evidence: supporto delle acceptance claim;
- portal dataset/read model: projection ricostruibili.

Nessuna projection può promuoversi a authority.

## 3. Boundary enterprise

Presentation, Application, Domain, Infrastructure, Persistence, Messaging ed External Systems restano distinti. Domain non dipende da framework, persistence o infrastructure. Citation, Provenance, source authority, semantic type, lifecycle e confidence devono attraversare i consumer governati.

## 4. Safety Authority

La Safety Authority fisica/locale e gli interlock restano indipendenti. Portale, telemetry, replay, analytics, comparison, quality score e AI non possono comandare apparati, autorizzare remediation o inferire uno stato Safety corrente da evidence storica.

## 5. Accepted intelligence and scientific foundation

Sono accettati, fra gli altri:

- BKL-015 — Knowledge Graph machine-readable foundation;
- BKL-044 — Knowledge Graph / AI Evidence Contract;
- BKL-035 — Target Knowledge Base;
- BKL-040 — Night Timeline / Observatory Replay;
- BKL-038 — Anomaly & Trend Center;
- BKL-039 — Equipment Performance Registry;
- BKL-045 — PixInsight Workflow Provenance Plugin;
- BKL-037 — Session Comparison & Benchmarking;
- BKL-041 — Scientific Data Quality Score;
- BKL-046 — AI Post-Processing Assistant, deterministic read-only closure.

BKL-037 rimane read-only/descriptive-only; unità non dimostrate, missing evidence e processing history PixInsight incompleta restano fail-closed.

## 6. Current package — BKL-031

BKL-041 — Scientific Data Quality Score è CLOSED / ACCEPTED / POST-MERGE VERIFIED come capability sperimentale read-only; production readiness resta `NOT_READY_FOR_PRODUCTION`.

BKL-046 F1-F5 sono CLOSED / ACCEPTED / POST-MERGE VERIFIED come capability deterministica advisory read-only tramite PR #181 e merge `3d680dd3a05c70b2a4654c4187c293e36b0af4a7`. Scientific effectiveness resta `NOT_EVALUABLE_CURRENT_EVIDENCE`, production `NOT_READY_FOR_PRODUCTION` e `aiModelImplemented=false`.

BKL-031 F1/F2, F3 Solution Architecture, F3-A1 Site Authority and F3-A2 setup-authority contract are accepted/post-merge verified with their recorded conditions. The protected setup baseline and Site Authority are separately APPROVED. PR #207 integrated the protected assignment DRAFT; PR #209 then integrated the separate approval receipt and unchanged `APPROVED` envelope as merge `bc4307c2042a45985622044e11631421de5b2c3d`. The suite passes 65/65 and all 7 post-merge workflows succeeded. Repository authority resolves `AVAILABLE` only for authorized validated input. S08 remains `UNAVAILABLE`; runtime S09 remains `UNAVAILABLE_CURRENT` because no adapter exists. `ARB-204-MI02` is mandatory before any runtime adapter. F3-A3/B/C, F4 forecast, F5 ranking/consumer, BKL-032 readiness, EAGLE operations and Safety Authority remain separate.

## 7. Roadmap

`... -> BKL-037 CLOSED -> BKL-041 CLOSED -> BKL-046 CLOSED -> BKL-031 [F1/F2 ACCEPTED / F3 SA ACCEPTED / F3-A1+A2 REPOSITORY AUTHORITIES ACCEPTED / F3-A3 EXACT SPK DECISION CURRENT / ADR-010 PROPOSED / S10 UNAVAILABLE] -> BKL-032 -> BKL-036 -> BKL-033 -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.

AMP-002 resta planning authority per AP-007–AP-015, non live status register.

## 8. Technical debt and decisions

TD-012 resta Accepted e non viene retrofittato. Le deroghe una tantum storiche restano consumate/scadute; `W-DSG-AEM-RULESET-001` governa i merge sostitutivi correnti. ADR-009 è Accepted. Nessun runtime provider o adapter è accettato; `ARB-204-MI02` resta un gate obbligatorio.

## 9. Delivery

Ogni incremento richiede exact-head CI, review applicabili, merge protetto e post-merge verification. Nessuna acceptance deriva dalla sola presenza di documentazione.

## 10. Runtime impact

La repository authority F3-A2-D5 è APPROVED/AVAILABLE per caller autorizzati, ma il runtime S09 resta `UNAVAILABLE_CURRENT`. Nessuna azione PC/EAGLE è richiesta e nessun command, readiness/go-no-go o Safety Authority è introdotto.

## 11. Registro revisioni

| Versione | Data | Descrizione |
|---|---|---|
| 1.0 | 04/08/2026 | Prima baseline enterprise |
| 2.0 | 08/09/2026 | Foundation BKL-040 e BKL-038 current |
| 2.1 | 10/09/2026 | Riallineamento a BKL-037 CLOSED/ACCEPTED e BKL-041 current |
| 2.2 | 11/09/2026 | Riallineamento a BKL-041 CLOSED/ACCEPTED e BKL-046 current |
| 2.3 | 11/09/2026 | BKL-046 F1 accepted e F2 current |
| 2.4 | 11/09/2026 | BKL-046 F2 accepted e F3 current |
| 2.5 | 11/09/2026 | BKL-046 F3 accepted e F4 current |
| 2.6 | 12/09/2026 | BKL-046 F4 accepted/post-merge verified e F5 design current |
| 2.7 | 13/09/2026 | BKL-046 closed/accepted/post-merge verified e BKL-031 F1 current |
| 2.8 | 14/09/2026 | BKL-031 F1 accepted/post-merge verified; F2 current handoff only |

| 2.9 | 14/09/2026 | BKL-031 F2 accepted/post-merge verified; successor decision pending |

| 3.0 | 14/09/2026 | BKL-031 F3 promoted as current handoff only |

| 3.1 | 14/09/2026 | BKL-031 F3 Solution Architecture review candidate |


| 3.2 | 14/09/2026 | BKL-031 F3 Solution Architecture AI-assisted ARB/RQ complete; merge decision pending |


| 3.3 | 14/09/2026 | BKL-031 F3 Solution Architecture accepted with conditions; implementation decision pending |
| 3.4 | 15/09/2026 | PR #192 closure integrated; F3-A1 Site Authority Contract review candidate current |
| 3.5 | 15/09/2026 | PR #193 F3-A1 merged/post-merge verified; Acceptance Reconciliation current |
| 3.6 | 15/09/2026 | PR #194 F3-A1 reconciliation merged/post-merge verified; F3-A2 handoff current |

| 3.7 | 15/09/2026 | PR #209 D5 accepted/post-merge verified; repository authority AVAILABLE, runtime S09 unavailable; successor selection current |

| 3.8 | 15/09/2026 | PR #210 D5 reconciliation accepted; F3-A3 Method ADR and validation-spike handoff current; no provider/runtime selection |
| 3.9 | 15/09/2026 | PR #211 handoff integrated; F3-A3 Solution Architecture, proposed ADR-010 and validation-spike plan review candidate |

## 12. F3-A3 enterprise boundary

F3-A3 remains a repository-governance package. Owner decisions F3-OD04–F3-OD10 are complete, including the exact `de442s.bsp` identity for F3-OD05, but ADR-010 remains Proposed and the scientific campaign is not executed. ARB-213-MI01/MI02 remain open. S10 remains `UNAVAILABLE`; Safety Authority and EAGLE operations are unchanged.


## 13. F3-A3 decision-preparation boundary

The approved F3-A3 decisions fix the candidate roles, exact local SPK identity, scientific thresholds, privacy boundary, host profile and bounded request values without changing enterprise intent. Implementation and acceptance remain gated by the immutable method profile and authorized scientific evidence. Domain remains provider-neutral; S10 remains `UNAVAILABLE`; Safety Authority and observatory operations are unchanged.
