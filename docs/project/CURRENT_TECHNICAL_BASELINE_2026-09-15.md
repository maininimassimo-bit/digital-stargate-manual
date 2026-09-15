# Digital StarGate — Current Technical Baseline 15/09/2026

| Campo | Valore |
|---|---|
| Identificativo | DSG-BASELINE-2026-09-15 |
| Stato | **CURRENT — F3-A2 HANDOFF REVIEWED / MERGE DECISION PENDING / DOCUMENTATION ONLY** |
| Repository baseline | `main@1fd771632239cdca38d7527c55b974d805ffd1b9` |
| Working branch | `docs/bkl-031-f3-a2-handoff` |
| Current package | BKL-031 F3-A2 — Setup Authority Program Assessment and Handoff |
| Runtime delta | None |
| Data/schema delta | None |
| Infrastructure delta | None |

## 1. Baseline integrata

PR #194 è merged nel commit `1fd771632239cdca38d7527c55b974d805ffd1b9` e verificata con 9/9 workflow post-merge. Pages build/deployment e Governed Projection Sync sono SUCCESS. Il waiver una tantum del merge è consumato/scaduto.

## 2. Stato tecnico corrente

F3-A1 è accettato con condizioni, riconciliato e non implementato. F3-A2 è selezionato esclusivamente come handoff documentale per il futuro contratto di `CurrentSetupAssignment`. Sulla PR #195 technical head `047ca2d1f208d8291d88823f4b99c401232ecd6b`, l'ARB AI-assistita ha deciso **APPROVED WITH CONDITIONS — 98/100** e Release Quality **CONDITIONALLY READY FOR MERGE**; le valutazioni non equivalgono ad approvazioni umane indipendenti.

Non esistono assignment reali, classi, schema JSON, fixture, validator, persistence, API, cache, deployment o integrazione EAGLE.

## 3. Dependency readiness

| Elemento | Stato |
|---|---|
| F3 architecture | accepted with conditions |
| F3-A1 contract | accepted with conditions / not implemented |
| AP-006 setup baseline authority | riferimento architetturale disponibile; baseline concreta approvata non attestata |
| F3-A2 detailed contract | not produced / specialist handoff current |
| F3-A3/B/C | not promoted |
| S09 | UNAVAILABLE_CURRENT |

## 4. Condizioni

| ID | Stato corrente |
|---|---|
| `ARB-195-MI01` | open prima dell'approvazione del contratto dettagliato F3-A2 |
| `ARB-193-MI01` | open prima di F3-B |
| `ARB-193-MI02` | open prima di F3-B |
| `ARB-191-MI01` | enforcement/leak tests open prima di F3-B/F3-C |
| `ARB-191-MI02` | normativa accettata; test eseguibili prima della materializzazione |
| AI review independence | review PR #193/#194/#195 dichiarate AI-assisted |
| Safety | authority fisica/locale invariata |

## 5. Verification target

L'exact review-publication head della draft PR #195 deve dimostrare:

- package esclusivamente documentale;
- dependency order coerente;
- roadmap source/projection allineate;
- link e nav validi;
- nessun runtime, schema, dato reale o segreto;
- exact head identificato;
- 7/7 workflow SUCCESS dopo la pubblicazione dei report;
- branch zero behind rispetto a `main`.

## 6. Rollback

Revert documentale del commit F3-A2 handoff. Nessuna migrazione, rotazione credenziali o azione operativa.
