# Repository Knowledge Map

| Campo | Valore |
|---|---|
| Identificativo | DSG-GOV-KM-001 |
| Versione | 2.9 |
| Stato | Active |
| Data | 14/09/2026 |
| Root bootstrap | `AI_BOOTSTRAP.md` |
| Current governed package | BKL-031 F2 — current handoff only; implementation not authorized |

## 1. Scopo

Mappa domini, authority, projection e percorsi di conoscenza. Non sostituisce le fonti canoniche.

## 2. Continuity hierarchy

1. `AI_BOOTSTRAP.md`;
2. current handover e technical baseline 14/09/2026;
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

BKL-015, BKL-044, BKL-035, BKL-040, BKL-038, BKL-039, BKL-045, BKL-037, BKL-041 e BKL-046 sono accepted. AP-013 resta authority degli asset; AP-014 resta catalog/synchronization boundary.

## 5. BKL-037 closed baseline

Session Comparison è read-only/descriptive-only. Confronta esclusivamente dimensioni/unità/provenance compatibili, conserva exclusions e non crea ranking, score, threshold, recommendation o authority.

## 6. BKL-046 closed and BKL-031 current

BKL-046 è CLOSED / ACCEPTED / POST-MERGE VERIFIED come capability deterministica advisory read-only tramite PR #181 e merge `3d680dd3a05c70b2a4654c4187c293e36b0af4a7`. Scientific effectiveness resta `NOT_EVALUABLE_CURRENT_EVIDENCE`, production `NOT_READY_FOR_PRODUCTION`, `aiModelImplemented=false`; nessun apply path o Safety Authority è autorizzato.

BKL-031 F1 è ACCEPTED / POST-MERGE VERIFIED tramite PR #183 e merge `b14d9cdd991b5eef74dd9b972958e74c5903a32d`. F2 è current come handoff soltanto; source/context machine-readable, fixture, validator e ogni implementazione richiedono nuova autorizzazione. S07–S11 restano unavailable/unknown e la separazione da BKL-032/Safety è invariata.

## 7. Roadmap sequence

`... -> BKL-037 CLOSED -> BKL-041 CLOSED -> BKL-046 CLOSED -> BKL-031 [F1 ACCEPTED / F2 CURRENT HANDOFF] -> BKL-032 -> BKL-036 -> BKL-033 -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.

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
