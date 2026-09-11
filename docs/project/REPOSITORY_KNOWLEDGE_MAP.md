# Repository Knowledge Map

| Campo | Valore |
|---|---|
| Identificativo | DSG-GOV-KM-001 |
| Versione | 2.6 |
| Stato | Active |
| Data | 11/09/2026 |
| Root bootstrap | `AI_BOOTSTRAP.md` |
| Current governed package | BKL-046 — AI Post-Processing Assistant for PixInsight |

## 1. Scopo

Mappa domini, authority, projection e percorsi di conoscenza. Non sostituisce le fonti canoniche.

## 2. Continuity hierarchy

1. `AI_BOOTSTRAP.md`;
2. current handover e technical baseline 10/09/2026;
3. Enterprise Architecture Context;
4. questo Knowledge Map;
5. `BACKLOG.md`;
6. canonical roadmap source;
7. generated roadmap projection;
8. Technical Debt, Decision Log, Development Workflow, Coding Standards e Release Playbook;
9. AMP-002 e package/review/evidence coinvolti.

## 3. Authority / projection map

Authority: repository, Architecture Package/ADR, backlog, canonical roadmap, registri, closure/review/workflow/evidence.

Projection: roadmap JSON, cataloghi/read model scientifici, Observatory Status, Timeline/Replay, Equipment Performance, Session Comparison e Analytics Center.

Ogni consumer preserva source locator, semantic type, lifecycle, Citation, Provenance, quality e completeness dove previsti.

## 4. Accepted foundation

BKL-015, BKL-044, BKL-035, BKL-040, BKL-038, BKL-039, BKL-045 e BKL-037 sono accepted. AP-013 resta authority degli asset; AP-014 resta catalog/synchronization boundary.

## 5. BKL-037 closed baseline

Session Comparison è read-only/descriptive-only. Confronta esclusivamente dimensioni/unità/provenance compatibili, conserva exclusions e non crea ranking, score, threshold, recommendation o authority.

## 6. BKL-041 closed and BKL-046 current

BKL-041 è CLOSED / ACCEPTED / POST-MERGE VERIFIED come capability sperimentale read-only; production readiness resta `NOT_READY_FOR_PRODUCTION`. BKL-046 F1-F3 sono CLOSED / ACCEPTED; F3 è stato integrato tramite PR #169, merge `8339aecf0b6b7fa19396561b20253c0411fd7ee7`, con review ARB/RQ AI-assistite owner-authorized e non indipendenti. F4 è current per un consumer session/provenance-driven read-only, collegato automaticamente al post-import con projection atomica e gate freshness/digest fail-closed, mantenendo execution evidence separata e senza selezionare model/provider o apply path.

## 7. Roadmap sequence

`... -> BKL-037 CLOSED -> BKL-041 CLOSED -> BKL-046 [CURRENT] -> BKL-031 -> BKL-032 -> BKL-036 -> BKL-033 -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.

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
