# BKL-031 F3-A3 — Ephemeris/Lunar Method ADR and Validation Spike Program Assessment and Handoff

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F3-A3-PROGRAM-001 |
| Stato | **AUTHORIZED HANDOFF / REVIEW CANDIDATE — NO PROVIDER SELECTED / NOT IMPLEMENTED** |
| Data | 15/09/2026 |
| Capability | BKL-031 — Observation Planner intelligente |
| Incremento selezionato | F3-A3 — Method ADR and validation spike |
| Baseline | `main@a1d2d84f9f787c247516bc825cb83d2bc15a43f5` |
| Predecessori | F3-A1/F3-A2 repository authorities accepted and post-merge verified |
| Specialist role | Digital StarGate Solution Architect |
| Runtime / dati reali | None |
| PC Principale / EAGLE | Nessuna azione richiesta |

## 1. Decisione di programma

F3-A3 — Method ADR and validation spike è selezionato come successore dependency-ready di F3-A2.

La promozione è limitata a un package documentale decision-ready: il Solution Architect dovrà definire il confronto riproducibile tra i metodi candidati, il piano di validazione scientifica e la struttura dell'ADR futuro. Questa decisione non seleziona provider, libreria, kernel, servizio remoto, host o soglia numerica e non rende S10 disponibile.

F3-B resta bloccato finché F3-A3 non avrà un ADR accettato e condizioni verificabili. F3-C e qualsiasi adapter/runtime restano separati.

## 2. Baseline verificata

- PR #210 ha riconciliato F3-A2-D5 e ha integrato la baseline corrente come `a1d2d84f9f787c247516bc825cb83d2bc15a43f5`;
- F3-A1 Site Authority è APPROVED nella repository authority;
- F3-A2 CurrentSetupAssignment è APPROVED e risolve `AVAILABLE` soltanto per input autorizzati e validati;
- S08 resta `UNAVAILABLE` per il runtime;
- S09 resta `UNAVAILABLE_CURRENT` per il runtime;
- S10 resta `UNAVAILABLE`;
- nessun adapter, provider, libreria scientifica, kernel o cache operativo è approvato;
- `ARB-204-MI02` resta gate obbligatorio prima di ogni runtime adapter.

Le review AI-assistite precedenti sono process-separated ma non equivalgono ad approvazioni umane indipendenti.

## 3. Maturity assessment

| Area | Maturità | Motivazione |
|---|---:|---|
| F3 source-neutral architecture | 90/100 | accepted with conditions/post-merge verified |
| F3-A1 site authority | 90/100 | repository authority approved; runtime adapter absent |
| F3-A2 setup authority | 90/100 | repository authority approved/available; runtime S09 unavailable |
| F3-A3 method decision | 30/100 | candidate set and blockers known; ADR, pins and evidence absent |
| F3-B machine-readable contracts | 20/100 | blocked by accepted F3-A3 decision |
| F3-C bounded integration | 10/100 | adapter/projection/OAT absent and not authorized |
| Runtime/operational readiness | 0/100 | no provider, host, adapter or runtime evidence |

I punteggi descrivono maturità documentale/implementativa, non accuratezza o efficacia scientifica.

## 4. Dependency-ordered roadmap

1. F3-A1 — Site Authority: repository authority accepted; runtime separate;
2. F3-A2 — Setup Authority: repository authority accepted/available; runtime separate;
3. **F3-A3 — Method ADR and validation spike: handoff documentale corrente**;
4. F3-B — machine-readable schema/fixture/validator: blocked;
5. F3-C — bounded adapter/projection/integration: blocked;
6. F4 — forecast: non promosso;
7. F5 — ranking/consumer: non promosso;
8. F6 — closure: futura.

F3-A3 è dependency-ready perché le autorità repository di sito e setup sono state completate. Non è runtime-ready: la selezione metodologica e le condizioni scientifiche, legali, privacy e operative restano aperte.

## 5. Candidate set vincolante per il confronto

Il futuro package deve confrontare senza preselezione:

| Candidato | Modalità da valutare | Evidenza minima richiesta |
|---|---|---|
| Astropy Coordinates + JPL ephemeris pinned | locale/offline dopo acquisizione governata | pin libreria/dati, frame e refraction policy, IERS/EOP, coverage, license/provenance |
| Skyfield + JPL BSP pinned | locale/offline dopo acquisizione governata | pin libreria/kernel, timescale/topos, coverage/checksum, phase/almanac conventions, license/provenance |
| JPL Horizons observer API | servizio remoto best-effort | service/version drift, request/output contract, availability, deterministic cache, terms e privacy exact-site |

Nessun candidato è preferito da questo handoff. Le fonti ufficiali e i termini devono essere verificati nuovamente nel futuro package alla data di esecuzione.

## 6. Owner decision gates

| ID | Decisione obbligatoria | Stato |
|---|---|---|
| F3-OD04 | provider/library, versione e ruoli primary/secondary | OPEN — owner/ADR |
| F3-OD05 | kernel/data package, coverage e checksum policy | OPEN — owner/ADR |
| F3-OD06 | error budget scientifico numerico e reference indipendente | OPEN — owner/ADR |
| F3-OD07 | IERS/EOP/leap-second acquisition e freshness | OPEN — owner/ADR |
| F3-OD08 | cache/retention, privacy external-service e licensing | OPEN — owner/ADR |
| F3-OD09 | execution host e resource/performance budget misurabile | OPEN — owner/ADR |
| F3-OD10 | bounded evaluation grid e maximum request size | OPEN — owner/ADR |

Il Solution Architect deve preparare opzioni, trade-off, evidence plan e raccomandazione condizionata. Non può chiudere autonomamente questi gate quando implicano provider/terms, trasmissione di dati protetti, soglie scientifiche o host operativo.

## 7. Specialist handoff brief

Il Solution Architect dovrà produrre:

1. decision context, scope e non-goals per l'ADR F3-A3;
2. comparison matrix source-neutral dei tre candidati;
3. dependency/data/kernel pinning e supply-chain evidence plan;
4. independent reference-vector strategy senza usare coordinate reali protette;
5. metriche, unità e metodo per misurare accuracy, repeatability, coverage e failure behavior;
6. proposta di error-budget envelope da sottoporre all'owner, non dichiarata accettata;
7. IERS/EOP/leap-second and freshness policy options;
8. privacy/threat model per cache e servizi esterni;
9. licensing/redistribution/notice checklist;
10. bounded resource/performance spike plan su host sintetico o espressamente autorizzato;
11. positive, negative, boundary e regression cases;
12. migration, rollback e rejection path che lasciano S10 `UNAVAILABLE`;
13. traceability verso F3 architecture, F3-A1/A2, F2 contract e condizioni ARB;
14. owner decision record template per F3-OD04–F3-OD10.

## 8. Acceptance criteria del futuro package F3-A3

- nessun provider preselezionato senza decisione tracciata;
- librerie, provider, dati e kernel identificati con versione/pin proposti;
- reference indipendente e protocollo di confronto riproducibili;
- error budget proposto con unità e razionale, ma non marcato accepted prima della decisione owner;
- synthetic/generalized site inputs only finché la privacy decision non autorizza altro;
- nessuna chiamata esterna con coordinate protette durante il package documentale;
- coverage, out-of-range, stale-data, unavailable-provider e conflicting-result behavior fail-closed;
- deterministic evidence include request, method, adapter, data/kernel e configuration identity;
- nessun silent fallback tra metodi;
- S10 resta `UNAVAILABLE` fino ad ADR, evidence e future materialization autorizzata;
- nessun forecast, ranking, readiness/go-no-go, command o Safety Authority;
- test/spike `NOT EXECUTED` finché non esiste un incremento successivo esplicitamente autorizzato.

## 9. Rischi e controlli

| Rischio | Controllo richiesto |
|---|---|
| scelta implicita del provider | ADR e gate owner separati |
| accuratezza non misurabile | error budget e reference indipendente espliciti |
| dipendenza non riproducibile | versioni, kernel e checksum pinned |
| drift temporale/IERS | freshness e missingness fail-closed |
| esposizione exact-site | synthetic/generalized inputs e privacy gate |
| dipendenza da servizio remoto | availability, deterministic cache e rejection path |
| licenza/redistribuzione incompatibile | terms review prima della selezione |
| consumo risorse non limitato | bounded grid/request size e host budget |
| falsa implementazione | stato NOT IMPLEMENTED / spike NOT EXECUTED |

## 10. Quality gates

Prima dell'integrazione di questo handoff:

- exact-head CI;
- Documentation, ARB e Release Quality review process-separated;
- coerenza bootstrap/handover/baseline/backlog/roadmap/nav;
- nessun runtime, dependency, kernel, data o infrastructure delta;
- nessun dato protetto, credenziale o locator interno;
- merge con expected-head control e post-merge verification.

Prima di un futuro ADR/spike eseguibile:

- refresh delle fonti ufficiali e dei termini;
- decisioni owner applicabili;
- ambiente e input autorizzati;
- dipendenze e dati pinned;
- protocollo, metriche e reference vectors approvati;
- privacy, licensing e rollback verificati.

## 11. Decision and risk summary

**Decisione:** promuovere F3-A3 esclusivamente come handoff documentale al Solution Architect per preparare ADR e validation-spike plan.

**Rischio residuo:** basso per questo handoff; alto se un metodo venisse selezionato o provato con dati reali senza i gate F3-OD04–F3-OD10.

**Safety:** nessuna variazione. Gli interlock fisici/locali restano indipendenti e autorevoli.

## 12. Governance stop

La corrente autorizzazione termina con integrazione e verifica post-merge di questo Program Assessment/Handoff. Non include:

- scelta o approvazione di provider/library/kernel;
- installazione di dipendenze o download di dati scientifici;
- chiamate a servizi esterni;
- uso o trasmissione di coordinate protette;
- definizione finale di error budget o soglie scientifiche;
- selezione dell'host o attività PC/EAGLE;
- schema, fixture, validator, adapter, cache, persistence, API o runtime;
- F3-B/C, F4/F5/F6, readiness, command o Safety Authority.
