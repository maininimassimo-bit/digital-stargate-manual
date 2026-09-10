# BKL-037 F2 — Canonical Comparison Read Model

| Campo | Valore |
|---|---|
| Identificativo | BKL-037-F2 |
| Stato | Proposed |
| Data | 10/09/2026 |
| Baseline | `4050b232c079170e0270dbc7d733d821f70f8c52` |
| Dipendenza | BKL-037 F1 ACCEPTED |

## Obiettivo

Rendere eseguibili e testabili le semantiche fail-closed definite in F1 mediante due read model puri e read-only: `SESSION_COMPARISON_CANDIDATE` e `SESSION_COMPARISON_SET`.

F2 non persiste benchmark e non introduce un nuovo source of truth. La futura F3 potrà costruire projection multi-sessione esclusivamente attraverso questo contratto.

## Componenti

- `.github/scripts/session-comparison-read-model.mjs` — builder deterministico;
- `.github/scripts/test-session-comparison-read-model.mjs` — test fail-closed.

## Candidate

Il candidate preserva sessione, dimensione, valore, unità, unit semantics, stato di calibrazione angolare, source, timestamp/intervallo, quality, completeness e provenance reference.

Classi ammesse: `COMPARABLE`, `CONTEXT_ONLY`, `PARTIAL`, `UNAVAILABLE`, `INCOMPATIBLE`, `UNKNOWN`.

Il default resta fail-closed. Un valore non diventa `COMPARABLE` solo perché numerico.

## Regole speciali

- FWHM source-native non calibrato o con angular calibration non provata -> `CONTEXT_ONLY`.
- unità assente -> `UNKNOWN`.
- value assente -> `UNAVAILABLE`.
- source/provenance insufficienti -> `UNKNOWN`.
- quality `STALE/UNKNOWN` -> `PARTIAL`.
- background -> `CONTEXT_ONLY` finché non esiste normalizzazione governata.
- final quality -> `CONTEXT_ONLY`; BKL-041 non viene anticipato.
- errors -> descrittivi soltanto.
- PixInsight workflow -> comparabile come storia completa solo con `completeness=COMPLETE`; `PARTIAL/UNAVAILABLE` restano fail-closed.

## Comparison Set

Un set richiede almeno due candidate e dichiara dimension, unit, inclusion/exclusion rules, source refs e timestamp di creazione. Ogni candidate non comparabile o semanticamente incompatibile viene mantenuto nell'elenco `excluded` con reason esplicita.

`comparisonState=COMPARABLE` richiede almeno due candidate incluse; altrimenti `INSUFFICIENT_COMPARABLE_EVIDENCE`.

## Authority

Entrambi i read model espongono:

- `consumerMode=READ_ONLY`;
- `acceptanceAuthority=false`;
- `actionAuthority=NONE`.

Qualsiasi escalation di action/acceptance authority viene rifiutata dal builder.

## Safety

Nessun accesso o comando a EAGLE, cupola, montatura, camera, power, network o Safety Authority. Il componente opera esclusivamente su evidence/read model forniti come input.

## Acceptance criteria

1. test automatici per FWHM calibrato/non calibrato;
2. unità mancanti fail-closed;
3. PixInsight `UNAVAILABLE` non comparabile;
4. background/final quality non promossi a score;
5. mismatch di unità escluso dal ComparisonSet;
6. authority escalation rifiutata;
7. exact-head CI applicabile verde.

## Next

F3 introdurrà una projection multi-sessione deterministica e descrittiva, con aggregazioni soltanto sulla popolazione `COMPARABLE` e con exclusions sempre visibili.
