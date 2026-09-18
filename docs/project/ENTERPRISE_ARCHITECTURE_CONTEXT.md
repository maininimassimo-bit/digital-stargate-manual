# Digital StarGate Enterprise Architecture Context

| Campo | Valore |
|---|---|
| Identificativo | DSG-CTX-001 |
| Versione | 4.2 |
| Stato | Active context baseline |
| Data baseline | 18/09/2026 |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch autorevole | `main` |
| Root bootstrap | `AI_BOOTSTRAP.md` |
| Continuity handover | `docs/project/HANDOVER_2026-09-17.md` |
| Technical baseline | `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-17.md` |
| Current governed package | BKL-031, BKL-032 and BKL-036 Closed/Accepted/Post-Merge Verified; BKL-033 next; S10 unavailable |
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

## 6. Current package — BKL-033

BKL-031 è **CLOSED / ACCEPTED / POST-MERGE VERIFIED** tramite PR #301 e merge `4a509d574a004fe7fb72bc6c678c9e7f71fe821f`. F3–F9 hanno chiuso il planner repeatable read-only: MeteoHub governato, astronomia della notte, suitability esplicita setup-target, ranking esplicabile e verifica della pagina pubblica di Manciano.

La closure BKL-032 non trasferisce authority: BKL-032 resta responsabile di Session Readiness / Go-No-Go. BKL-036 è chiuso solo per source discovery e semantic contract; score, runtime e source mapping futuro restano separati. Gli interlock fisici locali restano Safety Authority; S10 resta `UNAVAILABLE`. Il Planner non abilita scheduler, selezione automatica, device command o Safety Authority.

## 7. Roadmap

`... -> BKL-037 CLOSED -> BKL-041 CLOSED -> BKL-046 CLOSED -> BKL-031 CLOSED / ACCEPTED -> BKL-032 CLOSED / ACCEPTED -> BKL-036 CLOSED / ACCEPTED -> BKL-033 CURRENT -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.

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

F3-A3 remains a governed validation package. Owner decisions F3-OD04–F3-OD10 and ARB-213-MI01 repository evidence are complete. The bootstrap is applied, its state is remote and ARB-213-MI02 is satisfied by permanent-backend and post-promotion evidence. Exact dependency/IERS artifacts were acquired ephemerally with hash verification; two isolated no-cache builds produced the same unpublished linux/amd64 image config ID, and network-disabled preflight passed. Image push, artifact upload and platform plan/apply remain absent. ADR-010 remains Proposed, the scientific campaign is not executed and S10 remains `UNAVAILABLE`; Safety Authority and EAGLE operations are unchanged.


## 13. F3-A3 decision-preparation boundary

The approved F3-A3 decisions fix the candidate roles, exact local SPK identity, scientific thresholds, privacy boundary, host profile and bounded request values without changing enterprise intent. Implementation and acceptance remain gated by the immutable method profile and authorized scientific evidence. Domain remains provider-neutral; S10 remains `UNAVAILABLE`; Safety Authority and observatory operations are unchanged.


## 14. F3-A3 immutable method-profile boundary

`BKL-031-F3-A3-METHOD-PROFILE-001` is repository evidence for the approved method profile at SHA-256 `e69f60e5ed7f71cd982437f6ca3556b732d6ae9a46718995134aa64a7b7f67ca`. `BKL-031-F3-A3-CONTAINER-MANIFEST-001` fixes the future base, dependencies and IERS identity at static-source level. They are verified fail-closed before future calculation. They do not provide acquired artifacts, a built image, platform plan/apply, scientific evidence, runtime S10 or Safety Authority.

## 15. F3-A3 bootstrap-state boundary

The authorized bootstrap established only the isolated F3-A3 service identities, main-ref WIF trust and protected state/data/evidence buckets. Bootstrap state is remote and versioned. PR #219 promoted the permanent backend and corrected the migration serial acceptance rule after fail-closed incident `ARB-213-MI02-I01`; post-promotion lineage/content, recovery candidate, locking and zero drift were verified. No platform resource, scientific artifact, protected site datum, runtime S10 or Safety Authority is introduced.
