# Digital StarGate Enterprise Architecture Context

| Campo | Valore |
|---|---|
| Identificativo | DSG-CTX-001 |
| Versione | 2.1 |
| Stato | Active context baseline |
| Data baseline | 10/09/2026 |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch autorevole | `main` |
| Root bootstrap | `AI_BOOTSTRAP.md` |
| Continuity handover | `docs/project/HANDOVER_2026-09-10.md` |
| Technical baseline | `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-10.md` |
| Current governed package | BKL-046 — AI Post-Processing Assistant for PixInsight |
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
- BKL-037 — Session Comparison & Benchmarking.

BKL-037 rimane read-only/descriptive-only; unità non dimostrate, missing evidence e processing history PixInsight incompleta restano fail-closed.

## 6. Current package — BKL-046

BKL-041 — Scientific Data Quality Score è CLOSED / ACCEPTED / POST-MERGE VERIFIED come capability sperimentale read-only tramite PR #163, merge `e4ccd216b0a0ca4033277ece513f051b052d2b83`. Production readiness resta `NOT_READY_FOR_PRODUCTION`.

BKL-046 F1 è l'incremento corrente per definire:

- use case advisory e confini di approvazione umana;
- input di provenance PixInsight accettati e loro semantic ownership;
- comportamento su evidence missing/stale/unknown;
- explainability, citation e audit trail;
- bias, limiti di comparabilità e gestione delle raccomandazioni;
- authority boundary: nessuna automatic acceptance, remediation non presidiata, device command o Safety Authority;
- divieto di usare lo score sperimentale BKL-041 come ground truth o segnale produttivo.

La promozione a current non approva alcuna implementazione, modello/provider o automazione. F1 deve riusare BKL-044/BKL-045 e separare Recommendation, decisione umana ed execution evidence.

## 7. Roadmap

`... -> BKL-037 CLOSED -> BKL-041 CLOSED -> BKL-046 [CURRENT] -> BKL-031 -> BKL-032 -> BKL-036 -> BKL-033 -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.

AMP-002 resta planning authority per AP-007–AP-015, non live status register.

## 8. Technical debt and decisions

TD-012 resta Accepted e non viene retrofittato. Nessun nuovo debito o ADR è introdotto dalla transizione BKL-041 -> BKL-046.

## 9. Delivery

Ogni incremento richiede exact-head CI, review applicabili, merge protetto e post-merge verification. Nessuna acceptance deriva dalla sola presenza di documentazione.

## 10. Runtime impact

La closure BKL-041 e la promozione BKL-046 sono repository-only. Nessuna azione PC/EAGLE è richiesta.

## 11. Registro revisioni

| Versione | Data | Descrizione |
|---|---|---|
| 1.0 | 04/08/2026 | Prima baseline enterprise |
| 2.0 | 08/09/2026 | Foundation BKL-040 e BKL-038 current |
| 2.1 | 10/09/2026 | Riallineamento a BKL-037 CLOSED/ACCEPTED e BKL-041 current |
| 2.2 | 11/09/2026 | Riallineamento a BKL-041 CLOSED/ACCEPTED e BKL-046 current |
