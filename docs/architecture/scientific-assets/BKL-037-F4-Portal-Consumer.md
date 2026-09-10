# BKL-037 F4 — Portal / Consumer Read-Only

| Campo | Valore |
|---|---|
| Identificativo | BKL-037-F4 |
| Stato | Accepted |
| Accepted merge | `2e58d440b78e2c5c6d2f2c5978ccdf738c8674c3` |
| Data | 10/09/2026 |
| Baseline | `6c51f66ad74f3bcbc773c09b6e12f0b6a301ebc9` |
| Dipendenza | BKL-037 F3 ACCEPTED |
| Authority | Consumer read-only |

## Obiettivo

Esporre `SESSION_COMPARISON_PROJECTION` F3 nel portale senza trasformare il browser in source of truth o analytical engine.

Il consumer visualizza soltanto dati già presenti nella projection governata: dimensione, unità, sessioni incluse, exclusions, provenance, completeness, limitations e summary descrittivo.

## Fail-closed

Il browser rifiuta la projection quando:

- `projectionType` non è `SESSION_COMPARISON_PROJECTION`;
- `consumerMode` non è `READ_ONLY`;
- `acceptanceAuthority` non è `false`;
- `actionAuthority` non è `NONE`;
- mancano included sessions, exclusions o limitations;
- mancano le limitations `NO_RANKING_OR_QUALITY_SCORE` o `NO_SAFETY_OR_ACTION_AUTHORITY`.

Se `docs/data/session-comparison-projection.json` non è disponibile, il portale mostra esplicitamente uno stato di indisponibilità e non inventa un confronto.

## Consumer semantics

Il portale può mostrare:

- summary numerico già prodotto da F3;
- valori delle sessioni incluse con unità e provenance;
- quality/completeness originali;
- exclusions con reason e comparability class;
- source refs e limitations.

Il portale non calcola media, ranking, score, threshold, recommendation o acceptance decision. Non riclassifica exclusions.

## Authority e safety

La vista non scrive AP-013/AP-014, non modifica asset/sessioni, non esegue PixInsight e non dispone di device command/remediation. La Safety Authority locale resta indipendente.

BKL-041 resta separato per qualunque futuro Scientific Data Quality Score.

## Acceptance criteria F4

1. consumer browser read-only e fail-closed;
2. nessun calcolo analitico aggiuntivo nel browser;
3. provenance, completeness, exclusions e limitations visibili;
4. authority escalation rifiutata;
5. assenza della projection gestita come UNAVAILABLE, senza inference;
6. navigazione/documentazione repository coerente;
7. exact-head CI applicabile verde.

## F5

F5 eseguirà acceptance finale su evidence repository reale, includendo una projection persistita prodotta dalla pipeline F2/F3, verifica del rendering consumer, ARB, Release Quality, merge protetto e post-merge verification. L'evidence F5 non potrà colmare artificialmente unità o provenance mancanti.
