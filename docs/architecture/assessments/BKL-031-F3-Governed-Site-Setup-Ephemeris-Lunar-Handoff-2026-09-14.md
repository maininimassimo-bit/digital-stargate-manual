# BKL-031 F3 — Governed Site/Setup and Ephemeris/Lunar Source Integration Handoff

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-APA-F3-001 |
| Stato | **FULFILLED / SOLUTION ARCHITECTURE ACCEPTED WITH CONDITIONS — NOT IMPLEMENTED** |
| Data | 14/09/2026 |
| Baseline | `main` @ `4d5526c2fa2af10aeddace4f26c33fc95b7eaa57` |
| Capability | BKL-031 — Observation Planner intelligente |
| Incremento | F3 — Governed Site/Setup and Ephemeris/Lunar Source Integration |
| Predecessore | BKL-031 F2 — ACCEPTED / POST-MERGE VERIFIED |
| Specialist role | Solution Architect |
| Runtime / PC Principale / EAGLE | Nessuna modifica autorizzata |

## 1. Program decision

F3 è il successore dipendenza-ordinato definito dal contratto F1. La promozione è limitata alla preparazione del futuro package architetturale per:

- S08 — identità autorevole del sito e timezone;
- S09 — assegnazione setup corrente con intervallo di validità;
- S10 — sorgente/metodo ephemeris e lunar governati.

F3 non include forecast, ranking, portal consumer, readiness o runtime. F4 resta proprietario del forecast; F5 resta proprietario del ranking spiegabile e consumer read-only; BKL-032 resta proprietario della readiness.

## 2. Verified baseline

F1 e F2 sono accepted/post-merge verified. F2 espone un contratto bounded con S08, S09 e S10 unavailable e regole fail-closed già testate.

Repository evidence disponibile:

- BKL-035 target identity e coordinate storiche governate;
- inventario configurazioni/setup storico;
- AP-013/AP-014 session identity e catalog lineage;
- contratto F2 per `PlanningContext`, `EvidenceDimension`, Citation e Provenance.

Gap ancora aperti:

- nessun record canonico materializzato del sito;
- nessuna assegnazione setup corrente con validità;
- nessuna sorgente/metodo ephemeris-lunar approvati;
- nessun contratto per precisione, time scale, coordinate frame, licensing, caching e resource budget.

## 3. Maturity assessment

| Dimensione | Score | Motivazione |
|---|---:|---|
| Semantic contract | 95 | F1/F2 accepted, bounded e fail-closed |
| Target/session lineage | 90 | identity e historical lineage disponibili |
| Site authority | 30 | modello concettuale noto, record canonico assente |
| Current setup authority | 35 | storico disponibile, validità corrente assente |
| Ephemeris/lunar authority | 20 | nessun metodo/provider governato |
| Security/privacy | 75 | boundary definito; provider data-minimization da decidere |
| Safety separation | 100 | BKL-031/BKL-032/Safety separati |
| Runtime readiness | 0 | non autorizzata e non avviata |
| Validation readiness | 80 | negative boundary F2 disponibili; casi F3 da definire |

## 4. Dependency-ordered F3 roadmap

### F3-A — Source discovery and authority decisions

- censire sorgenti candidate per sito/setup/ephemeris/lunare;
- identificare owner/custodian, authority, locator e lifecycle;
- valutare alternative provider/library senza selezionarle implicitamente;
- documentare licensing, privacy, retention e failure modes.

### F3-B — Machine-readable source contracts

- definire record sito con stable identity, coordinate, elevation, timezone e validity;
- definire current setup assignment con stable configuration reference e valid interval;
- definire ephemeris/lunar method contract con version, inputs, time scale, frame/epoch, precision e validity;
- estendere schema/fixture/validator F2 soltanto dopo approvazione architetturale.

### F3-C — Bounded integration and validation

- produrre projection bounded, read-only e fail-closed;
- eseguire calcolo/normalizzazione fuori da EAGLE;
- preservare Citation/Provenance e incomplete/conflicted states;
- integrare test positivi/negativi e CI;
- fermarsi prima di F4/F5.

Le slice sono una proposta di sequenza, non autorizzazione a implementarle.

## 5. Specialist handoff

Il Solution Architect dovrà produrre un Architecture Package contenente:

1. current/target state e component boundaries;
2. source inventory e comparison matrix delle alternative;
3. source ownership/authority contract;
4. schema concettuale e machine-readable contract proposto;
5. porte Application e adapter Infrastructure, senza dipendenze nel Domain;
6. time/coordinate semantics: UTC, timezone IANA, DST, reference frame, epoch e precision/error budget;
7. caching/freshness/validity e deterministic failure behavior;
8. security, privacy, licensing e data-minimization;
9. off-EAGLE resource placement;
10. migration, rollback e observability;
11. validation plan con negative cases;
12. traceability a F1/F2, BKL-035, AP-013/AP-014 e BKL-032.

Un ADR sarà richiesto soltanto quando le alternative provider/library saranno sufficientemente verificate per una scelta consequenziale.

## 6. Architecture rules

- site identity non può essere dedotta da testo libero o coordinate non governate;
- timezone deve essere IANA; offset fisso e timezone display non possono sostituire la timezone del sito;
- setup corrente richiede identificatore stabile, validità temporale e conflict handling;
- configurazioni storiche non possono diventare current per recency o file order;
- ephemeris/lunar facts richiedono metodo e versione, input completi, frame/epoch, time scale, validity e precision dichiarata;
- cache scaduta o input incompleto produce `STALE`/`UNAVAILABLE`, mai last-known-good presentato come current;
- nessuna sorgente F3 può diventare Safety Authority;
- calcolo non banale e chiamate esterne restano fuori da EAGLE;
- nessuna credenziale, host locale o raw operational path entra nel repository o nel browser;
- S07 resta unavailable/current-unknown e S11 resta unavailable fino ai rispettivi incrementi;
- nessun peso, score, ranking, ordering, readiness, scheduler o command field.

## 7. Acceptance criteria for the future F3 architecture package

- source candidate e alternative documentate con evidence e open issues;
- owner, authority, locator, sensitivity, licensing, retention e update semantics espliciti;
- stable site/setup identity e validity/conflict policy;
- time/coordinate/precision contract completo;
- resource placement e failure behavior fail-closed;
- F2 compatibility e migration/rollback definiti;
- almeno i negative cases per missing site, invalid timezone, stale setup, setup conflict, incomplete ephemeris inputs, unknown method version, expired cache, frame/epoch mismatch e prohibited ranking/readiness;
- F4/F5/BKL-032/Safety boundaries invariati;
- MkDocs, links e CI verdi sull'exact head.

## 8. Risks

| ID | Rischio | Trattamento richiesto |
|---|---|---|
| BKL031-F3-R01 | sito/coordinate/timezone errati | authority record, validation e fail-closed |
| BKL031-F3-R02 | DST/time scale/frame/epoch ambiguity | explicit IANA/UTC/frame/epoch contract |
| BKL031-F3-R03 | setup storico promosso a current | validity interval e conflict rules |
| BKL031-F3-R04 | provider/library lock-in o licensing incompatibile | alternative matrix e ADR prima della scelta |
| BKL031-F3-R05 | cache stale presentata come corrente | issue/validity/freshness contract |
| BKL031-F3-R06 | carico o dipendenza di rete su EAGLE | off-EAGLE execution boundary |
| BKL031-F3-R07 | ephemeris trasformata in readiness/Safety | authority NONE, separazione BKL-032/interlock |
| BKL031-F3-R08 | scope creep verso forecast/ranking | F4/F5 ownership e schema prohibition |

## 9. Historical handoff quality gates — satisfied

- repository/source discovery evidence reviewed;
- architecture package completeness;
- schema/contract validation where proposed;
- negative-case traceability;
- security/privacy/licensing review;
- safety and authority review;
- MkDocs strict build and link validation;
- exact-head GitHub Actions;
- independent ARB and Release Quality after separate authorization.

Runtime/OAT is not applicable to the handoff. It becomes applicable only if a later implementation is authorized.

## 10. Historical authorization boundary at handoff publication

At handoff publication, before the later owner authorizations recorded in sections 12–13, this handoff did not authorize:

- detailed solution design or ADR acceptance;
- provider/library selection;
- schema, fixture, validator or adapter changes;
- credentials, network calls or deployment;
- PC Principale/EAGLE activity;
- forecast/F4;
- weights, score, ranking, target ordering or portal consumer/F5;
- readiness, scheduler, go/no-go or BKL-032 implementation;
- device command, remediation or Safety Authority;
- ARB, Release Quality or merge.

## 11. Historical governance stop — consumed by later authorizations

This stop applied after the handoff draft publication. Separate owner authorizations subsequently covered the Solution Architecture package, AI-assisted reviews and PR #190/#191 merges. It never authorized and still does not authorize provider/ADR selection, authority records, implementation or runtime activity.

## 12. Fulfilment record

The handoff was integrated through PR #190 and merge `2ffc77917bcd3fc25a3c5657e8f12e62c9284303` with 9/9 post-merge workflows. After separate owner authorization, it is fulfilled by:

- `docs/architecture/scientific-assets/BKL-031-F3-Governed-Site-Setup-and-Ephemeris-Lunar-Solution-Architecture.md`;
- `docs/architecture/validation/BKL-031-F3-Governed-Site-Setup-and-Ephemeris-Lunar-Validation-Plan.md`.

At initial publication both artifacts were review candidates. PR #191 later completed owner-authorized AI-assisted reviews, merge and post-merge verification. The artifacts select no provider/library, approve no ADR, materialize no real site/setup authority, and implement no schema, fixture, validator, adapter, runtime or portal consumer. Implementation remains separately unauthorized.


## 13. Solution Architecture acceptance

The F3 handoff is fulfilled by the Solution Architecture and validation plan integrated through PR #191 and merge `3a79bb93c9a0925280eba5214d517107804cb13c`. Post-merge workflows completed 9/9 successfully.

The architecture is accepted with conditions and remains non-implementing. `ARB-191-MI01` and `ARB-191-MI02` are carried forward. No F3-A1/A2/A3/B/C slice is promoted or authorized.
