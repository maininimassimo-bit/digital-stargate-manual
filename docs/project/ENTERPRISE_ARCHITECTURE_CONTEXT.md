# Digital StarGate Enterprise Architecture Context

| Campo | Valore |
|---|---|
| Identificativo | DSG-CTX-001 |
| Versione | 2.6 |
| Stato | Active context baseline |
| Data baseline | 12/09/2026 |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch autorevole | `main` |
| Root bootstrap | `AI_BOOTSTRAP.md` |
| Continuity handover | `docs/project/HANDOVER_2026-09-12.md` |
| Technical baseline | `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-12.md` |
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

BKL-041 — Scientific Data Quality Score è CLOSED / ACCEPTED / POST-MERGE VERIFIED come capability sperimentale read-only; production readiness resta `NOT_READY_FOR_PRODUCTION`.

BKL-046 F1-F4 sono CLOSED / ACCEPTED. F4 è stata integrata tramite PR #175 e merge `af48cc2441cf956d88c13c81845fc2a2f7c599f2`, con review ARB/RQ AI-assistite owner-authorized e non equivalenti ad approvazioni umane indipendenti, suite F2/F3/F4 verdi, 6/6 workflow post-merge e Pages live verificate. La deroga `W-BKL046-F4-001` era limitata alla branch protection della PR #175 ed è consumata/scaduta.

F5 è il prossimo incremento soltanto di architettura/design per definire cohort, sufficienza delle evidenze, criteri di valutazione e limitation di una possibile closure read-only. Non introduce model/provider, confidence scientifica, automatic acceptance, PixInsight apply, remediation, device command o Safety Authority.

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
| 2.3 | 11/09/2026 | BKL-046 F1 accepted e F2 current |
| 2.4 | 11/09/2026 | BKL-046 F2 accepted e F3 current |
| 2.5 | 11/09/2026 | BKL-046 F3 accepted e F4 current |
| 2.6 | 12/09/2026 | BKL-046 F4 accepted/post-merge verified e F5 design current |
