# ARB-BKL-041-F5 — Independent Architecture Review

| Campo | Valore |
|---|---|
| Review | ARB-BKL-041-F5 |
| Data | 11/09/2026 |
| Proposal | `docs/architecture/scientific-assets/BKL-041-F5-Real-Evidence-Validation-and-Capability-Closure.md` |
| Base | `ed9ffcc92e1a5252b0d8c37634bc652397f3cde1` |
| Reviewed head | `6163af04e21c1f525a54b314a8577e74fa9d4283` |
| PR | #163 |
| Decision | REWORK REQUIRED |
| Score | 84/100 |

## 1. Executive decision

**REWORK REQUIRED — 84/100.**

L'impostazione generale è corretta: F5 valuta l'intera cohort senza outcome filtering, mantiene distinta capability acceptance da production authorization, pubblica la validation nello stesso commit atomico e rende i gap visibili nel consumer. I test e i nove workflow applicabili sul reviewed head sono verdi.

La proposta non è tuttavia approvabile nello stato corrente. Tre soglie quantitative di readiness (`30` sessioni, `3` target, `80%`) non derivano da una decisione o evidence governata e violano il divieto di inventare threshold. Inoltre alcune sezioni dello schema dichiarato chiuso ammettono proprietà arbitrarie, e il ramo futuro in cui tutti i gate passano genera uno stato rifiutato dallo schema e dal browser, con rischio di bloccare una successiva importazione automatica.

## 2. Scorecard

| Dimensione | Score | Evidence-based assessment |
|---|---:|---|
| Scope e semantic integrity | 90 | corretta separazione fra experimental acceptance e production readiness. |
| Cohort integrity | 98 | tutte le 15 sessioni incluse senza selezione per outcome. |
| Scientific integrity e bias | 91 | gap e sbilanciamento espliciti; soglie quantitative prive di evidence governata. |
| Contract integrity | 76 | root chiusa, ma `cohort` e `requirements` consentono drift non dichiarato. |
| Determinism e identity | 99 | report e digest riproducibili; freshness concatenata a catalogo/projection. |
| Dynamic update safety | 78 | atomicità corretta; stato futuro incompatibile può fermare il workflow di import. |
| Explainability e UX | 96 | decisione e limitation chiaramente presentate. |
| Authority e Safety | 100 | nessuna production/acceptance/action/Safety authority. |
| Operability e rollback | 94 | failure e rollback descritti; incompatibilità futura da rimuovere. |
| Traceability e validation | 98 | architettura, closure proposta, roadmap, test e CI coerenti. |

## 3. Findings

### Blocker

Nessuno.

### Major

#### M-01 — Readiness threshold non governati

`minimumImportedSessions=30`, `minimumKnownTargets=3` e i ratio `0.8` non hanno una fonte, un metodo empirico o una decisione architetturale accettata. La loro etichetta come guardrail conservativi non è sufficiente a renderli evidence-based.

**Remediation:** rimuovere i threshold numerici e valutare soltanto stati dimostrabili dal repository, per esempio `REPRESENTATIVENESS_NOT_DEMONSTRATED`, `COVERAGE_ADEQUACY_NOT_DEMONSTRATED`, `GROUND_TRUTH_UNAVAILABLE`, `GUIDING_TEMPORAL_COVERAGE_UNAVAILABLE` e `PROFILE_NOT_CALIBRATED`. In alternativa, introdurre una decisione separata con metodo, fonti, assunzioni e validation evidence; questa seconda strada richiede nuova review scientifica.

**Re-review evidence:** report, schema, test, UX e documentazione non contengono soglie quantitative prive di provenance; i risultati osservati possono restare numerici e descrittivi.

#### M-02 — Stato futuro incompatibile con il contratto di pubblicazione

Il builder emette `READY_FOR_PRODUCTION_REVIEW` se tutti i criteri passano, mentre schema e browser ammettono esclusivamente `NOT_READY_FOR_PRODUCTION`. Una futura importazione che soddisfacesse i gate produrrebbe un file rifiutato dai controlli successivi e potrebbe fermare la pubblicazione automatica.

**Remediation:** mantenere `productionReadiness=NOT_READY_FOR_PRODUCTION` finché non esiste un nuovo profilo approvato e modellare separatamente una eventuale `calibrationInputReadiness`, oppure versionare insieme generator/schema/consumer per entrambi gli stati senza autorizzazione implicita. Nessun passaggio automatico può concedere production use.

**Re-review evidence:** test positivo del futuro stato di input e test che prova `productionUseAuthorized=false` in ogni ramo, senza interrompere il workflow.

### Minor

#### m-01 — Schema/validator parity incompleta

Lo schema usa `additionalProperties: true` per `cohort` e un oggetto generico per `acceptancePolicy.requirements`, nonostante il documento lo descriva come contratto chiuso.

**Remediation:** chiudere e tipizzare tutte le sezioni governate, aggiungere negative tests per proprietà sconosciute e verificare la parity con il validator browser/repository.

### Observations

#### O-01 — Closure con limitation

È architetturalmente legittimo chiudere BKL-041 come capability sperimentale read-only se closure, backlog e roadmap distinguono in modo permanente questo outcome dalla production acceptance. Una futura calibrazione produttiva deve essere una nuova iniziativa/versione, non la riapertura implicita dello stato F5.

#### O-02 — Evidence descrittiva riutilizzabile

I valori verificati — 15 sessioni, 2 target noti, 5/3/7 assessment, SQM 8/15 e guiding coverage 0 — sono evidence descrittiva valida. Possono sostenere la conclusione non produttiva senza essere confrontati con threshold inventati.

## 4. Validation evidence

| Gate | Stato | Evidenza |
|---|---|---|
| Local F5 verifier/idempotency | Passed | 15 sessioni; report deterministico |
| Local F5 tests | Passed | 10/10 |
| Local F2–F4 regression | Passed | 43/43 |
| BKL-041 F5 Governance | Passed | #1, run `34599362943` |
| BKL-041 F4 Governance | Passed | #5, run `34599362897` |
| Developer Foundation | Passed | #1296, run `34599362874` |
| Scientific Platform Governance | Passed | #51, run `34599362867` |
| Validate documentation | Passed | #929, run `34599362940` |
| Genera manuale Word | Passed | #1354, run `34599362805` |
| Analytics consistency | Passed | #33, run `34599362834` |
| Session Comparison | Passed | #17, run `34599362855` |
| BKL-039 regression | Passed | #52, run `34599362847` |
| Architecture findings | Failed | M-01, M-02 e m-01 aperti |

## 5. Re-review criteria

La re-review può iniziare quando:

1. i threshold non governati sono rimossi o supportati da una decisione/evidence separata;
2. il lifecycle futuro non può divergere fra builder, schema e consumer;
3. cohort e policy sono chiuse fail-closed con negative tests;
4. validation report e consumer restano aggiornati automaticamente dopo ogni import;
5. tutti i test e workflow applicabili sono verdi sul nuovo exact head.

Fino alla chiusura dei finding il PR #163 non è pronto per Release Quality o merge.
