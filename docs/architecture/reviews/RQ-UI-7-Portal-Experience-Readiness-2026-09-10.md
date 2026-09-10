# Release Quality Review — UI 7.0 Portal Experience

| Campo | Valore |
|---|---|
| Review | RQ-UI-7 |
| Data | 10/09/2026 |
| Release candidate | UI 7.0 |
| Exact head valutato | `0594abb3f6cfefcb8a13398b1a48efcfe30ee22b` |
| PR | #155 |
| ARB | ARB-UI-7 — APPROVED |
| Raccomandazione | **READY FOR MERGE** |

## 1. Decisione

UI 7.0 soddisfa i quality gate richiesti per il merge. Scope, tracciabilità, compatibilità, rollback e boundary sono documentati; i workflow CI obbligatori risultano verdi sull'exact head valutato.

Il gate post-merge resta aperto fino alla verifica del deploy GitHub Pages e delle superfici pubbliche principali.

## 2. Scope integrity

| Controllo | Esito |
|---|---|
| Homepage, navigation e design system inclusi | PASS |
| Information architecture MkDocs aggiornata | PASS |
| Audit stale/legacy disponibile | PASS |
| Dynamic projection contract documentato | PASS |
| URL pubblici e schema dati preservati | PASS |
| Nessun workflow privilegiato modificato | PASS |
| Nessun impatto EAGLE/device/Safety Authority | PASS |

## 3. Definition of Done

| Evidenza | Stato |
|---|---|
| Solution architecture DSGP-SOL-001 | Accepted |
| Design System DSG-UI-001 v2.0 | Accepted |
| Publication Guidelines DSG-DEV-001 v2.0 | Active |
| Freshness audit DSG-UI-AUD-001 | Completed |
| ARB-UI-7 | Approved |
| JavaScript/YAML/CSS checks | Pass |
| MkDocs/documentation CI | Success |
| Scientific Platform Governance | Success |
| Word generation | Success |
| Rollback | UI-only, documentato |

## 4. Exact-head evidence

| Workflow | Run | Esito |
|---|---:|---|
| Scientific Platform Governance | 34535321361 | SUCCESS |
| Validate documentation (no deploy) | 34535321363 | SUCCESS |
| Genera manuale Word | 34535321347 | SUCCESS |

## 5. Release risks

| Rischio | Livello | Gate |
|---|---|---|
| Differenze di rendering sul sito Pages | Basso | verifica post-merge obbligatoria |
| Projection temporaneamente non disponibile | Basso | fallback UNKNOWN/UNAVAILABLE già implementato |
| Cache browser di dataset precedenti | Basso | fetch `cache: no-store` |
| Regressione deep link | Basso | URL preservati e MkDocs CI verde |

## 6. Rollback recommendation

In caso di regressione visuale o funzionale, revert del merge UI 7.0 e nuovo deploy Pages. Non modificare dataset, workflow di import, evidence o runtime osservatorio.

## 7. Change control dopo la review

È consentito soltanto l'aggiornamento editoriale dello stato release e del riferimento a questa review. Qualunque modifica funzionale richiede una nuova valutazione. L'head finale deve rieseguire con successo i workflow obbligatori.

## 8. Final recommendation

**READY FOR MERGE**, con verifica GitHub Pages post-merge obbligatoria prima di dichiarare UI 7.0 Released.
