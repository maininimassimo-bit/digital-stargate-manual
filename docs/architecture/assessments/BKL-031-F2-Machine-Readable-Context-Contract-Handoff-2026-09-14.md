# BKL-031 F2 — Machine-Readable Context/Source Contract Handoff

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F2-HANDOFF-001 |
| Stato | **OWNER-AUTHORIZED — IMPLEMENTATION CANDIDATE IN PROGRESS** |
| Data | 14/09/2026 |
| Capability | BKL-031 — Observation Planner intelligente |
| Predecessore accettato | BKL-031 F1 |
| Acceptance record | `docs/project/BKL-031-F1-ACCEPTANCE-2026-09-14.md` |
| Accepted merge | `b14d9cdd991b5eef74dd9b972958e74c5903a32d` |
| Repository baseline per l'implementazione | `f6c4b253a56406c930f009af0658b46a12bc088a` |
| Specialist role raccomandato | Solution Architect |
| Runtime impact autorizzato | None |

## 1. Obiettivo del prossimo incremento

Il repository owner ha autorizzato l'implementazione del solo F2. F2 definisce un contratto machine-readable, bounded e fail-closed per rappresentare sorgenti e contesto del futuro Observation Planner. Il contratto codifica, senza calcolo di ranking:

- `TargetCandidate`;
- `PlanningContext`;
- `EvidenceDimension`;
- `RankingFactor`;
- `RankingExplanation`.

L'autorizzazione copre schema, fixture, validator, test, documentazione e quality gate su PR draft. Non copre ARB, Release Quality, merge, provider, ranking, consumer o runtime.

## 2. Input obbligatori

- F1 Source Discovery and Semantic Boundary;
- F1 Source and Semantic Validation Plan;
- F1 Acceptance Record;
- BKL-015 knowledge traceability;
- BKL-035 target identity, Citation e Provenance;
- AP-013/AP-014 asset, session e catalog authority;
- BKL-029 SQM semantics;
- separazione BKL-031/BKL-032/Safety.

## 3. Condizioni trasferite da F1

1. S07–S11 devono restare `UNAVAILABLE`, `UNAVAILABLE_CURRENT` o `UNKNOWN` sulla baseline corrente.
2. Nessuna fixture può inventare sito, setup attivo, ephemeris, Luna, forecast o stato realtime.
3. Le fixture devono avere dimensione e copertura bounded esplicitamente dichiarate.
4. I 20 casi negativi del validation plan F1 sono obbligatori.
5. Nessun peso numerico, score, soglia, normalizzazione, ordinamento o readiness è ammesso.
6. Ogni provider futuro richiede contratto separato su owner, authority, locator, licensing, precision, privacy, validity/freshness e failure behavior.
7. Nessun carico pesante o chiamata esterna viene collocato su EAGLE.
8. Nessun output può diventare comando, scheduler, go/no-go o Safety Authority.

## 4. Output autorizzati dell'incremento

- schema versionato per sorgenti e contesto;
- fixture sintetiche bounded;
- validator fail-closed;
- test positivi e negativi deterministici;
- documentazione di migration/rollback;
- quality gate e review indipendenti o esplicitamente qualificate.

## 5. Acceptance criteria futuri

F2 potrà essere proposto per review solo quando:

- ogni oggetto machine-readable è coerente con la semantica F1;
- ogni fact conserva source locator, Citation, Provenance, authority, validity e quality;
- missing, stale e conflicted restano distinguibili;
- S07–S11 non sono simulati;
- l'identità target BKL-035 non viene ricostruita o fuzzy-matched;
- i 20 casi negativi sono eseguiti e tracciati;
- nessun requisito escluso entra nel changed set;
- tutti i workflow applicabili sono verdi sull'exact head.

## 6. Stop di governance

La presente autorizzazione termina con la pubblicazione della PR draft F2 e la verifica dei quality gate applicabili. ARB, Release Quality, merge, provider selection, ranking, consumer, F3 e qualsiasi runtime richiedono una nuova autorizzazione esplicita del repository owner.
