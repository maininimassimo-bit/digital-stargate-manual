# BKL-031 F1 — Acceptance Record

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F1-ACCEPTANCE-001 |
| Stato | **ACCEPTED / POST-MERGE VERIFIED** |
| Data | 14/09/2026 |
| Capability | BKL-031 — Observation Planner intelligente |
| Incremento accettato | F1 — Source Discovery and Semantic Boundary |
| Pull request | [#183](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/183) |
| Technical head reviewed | `55b502fb4e47ef92975767ceb444078cae36caf8` |
| Review-publication head | `7a4d020b59186c4b05b9741bb12689050e2b7e8d` |
| Merge commit | `b14d9cdd991b5eef74dd9b972958e74c5903a32d` |
| Successore | BKL-031 F2 — Machine-Readable Context/Source Contract and Bounded Fixtures |
| Runtime impact | None |
| PC Principale / EAGLE | Nessuna azione richiesta |

## 1. Decisione

BKL-031 F1 è accettato come baseline architetturale per source discovery, authority, identity, freshness, missingness e separazione semantica dell'Observation Planner. L'accettazione riguarda esclusivamente il contratto documentale integrato tramite PR #183.

F2 è promosso come prossimo incremento governato soltanto a livello di handoff. Questa transizione non autorizza la creazione di schema, fixture, validator, algoritmo, consumer o integrazione runtime.

## 2. Ambito accettato

F1 accetta:

- l'inventario verificato BKL031-S01–S11;
- la distinzione fra `TargetCandidate`, `PlanningContext`, `EvidenceDimension`, `RankingFactor` e `RankingExplanation`;
- la conservazione di Citation, Provenance, authority, identity, freshness, missingness e conflitto;
- la separazione da BKL-032 Session Readiness e dalla Safety Authority fisica/locale;
- l'esecuzione futura dei carichi non banali fuori da EAGLE.

Restano esplicitamente indisponibili sulla baseline accettata:

- BKL031-S07 — stato osservatorio corrente: `UNAVAILABLE_CURRENT_BASELINE`;
- BKL031-S08 — record autorevole del sito: `UNAVAILABLE`;
- BKL031-S09 — assegnazione setup corrente con intervallo di validità: `UNAVAILABLE_CURRENT`;
- BKL031-S10 — sorgente ephemeris/lunar governata: `UNAVAILABLE`;
- BKL031-S11 — sorgente forecast governata: `UNAVAILABLE`.

## 3. Review

| Review | Esito | Qualifica |
|---|---|---|
| ARB BKL-031 F1 | APPROVED WITH CONDITIONS — 99/100 | AI-assisted, owner-authorized; non equivalente ad approvazione umana indipendente |
| Release Quality BKL-031 F1 | CONDITIONALLY READY FOR MERGE | AI-assisted, owner-authorized; non equivalente ad approvazione umana indipendente |

Le condizioni sono trasferite integralmente a F2:

1. le fixture future devono rappresentare S07–S11 come unavailable/unknown e non simulare dati;
2. ogni integrazione site/setup/provider richiede un source contract separatamente governato;
3. F2 non deve contenere pesi numerici, contributi di score, soglie, curve di normalizzazione, ordinamento target o readiness;
4. i 20 casi negativi F1 restano obbligatori per il futuro validator;
5. non sono autorizzati comandi, scheduling automatico, go/no-go o Safety Authority.

## 4. Evidenza CI

### Publication head `7a4d020b59186c4b05b9741bb12689050e2b7e8d`

- Validate documentation — run `34819887824`: SUCCESS;
- Genera manuale Word — run `34819887846`: SUCCESS;
- BKL-041 F4 Governance — run `34819887855`: SUCCESS;
- BKL-046 F4 governance — run `34819887827`: SUCCESS;
- BKL-046 F5 governance — run `34819887828`: SUCCESS;
- Developer Foundation: `NOT_TRIGGERED / NOT_APPLICABLE` per il path set documentation-only.

### Merge commit `b14d9cdd991b5eef74dd9b972958e74c5903a32d`

- Validate documentation — run `34820524743`: SUCCESS;
- Genera manuale Word — run `34820524740`: SUCCESS;
- BKL-041 F4 Governance — run `34820524962`: SUCCESS;
- BKL-046 F4 governance — run `34820524926`: SUCCESS;
- BKL-046 F5 governance — run `34820524942`: SUCCESS;
- Deploy MkDocs artifact to GitHub Pages — run `34820524858`: SUCCESS.

## 5. Rischi, deroghe e limiti

| ID | Stato | Disposizione |
|---|---|---|
| W-BKL031-F1-MERGE-001 | Consumed / Expired | deroga una tantum limitata al merge #183; nessun precedente |
| F1-AI-REVIEW | Disclosed | review AI-assistite non equivalenti a review umane indipendenti |
| BKL031-S07–S11 | Open / carried | mantenere unavailable/unknown finché non esiste un contratto separatamente approvato |
| F2 implementation | **NOT AUTHORIZED** | richiede una nuova azione owner esplicita |

## 6. Handoff

Il successore è definito in:

`docs/architecture/assessments/BKL-031-F2-Machine-Readable-Context-Contract-Handoff-2026-09-14.md`.

Il package deve fermarsi prima di qualsiasi implementazione F2 o review non separatamente autorizzata.
