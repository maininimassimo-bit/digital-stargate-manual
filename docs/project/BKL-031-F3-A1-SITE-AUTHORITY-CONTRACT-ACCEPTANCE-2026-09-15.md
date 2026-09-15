# BKL-031 F3-A1 — Site Authority Contract Acceptance

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F3-A1-ACCEPTANCE-001 |
| Stato | **ACCEPTED WITH CONDITIONS / POST-MERGE VERIFIED — NOT IMPLEMENTED** |
| Data | 15/09/2026 |
| Capability | BKL-031 — Observation Planner intelligente |
| Incremento | F3-A1 — Site Authority Contract |
| Pull request | #193 |
| Technical head valutato | `8bc4c8ed131bce0580ff95905b130b191605e2e7` |
| Review-publication head | `b81187c58811399b10eb3e1efeadc62491f01918` |
| Merge commit | `b9d08a7cf6b6287825907cab6a846b1ec70f0378` |
| Runtime / dati reali | None |
| PC Principale / EAGLE | Nessuna azione richiesta |
| Successore | Decisione owner separata; nessuna slice promossa automaticamente |

## 1. Decisione

Il Site Authority Contract F3-A1, il relativo handoff e il validation plan sono accettati con condizioni come baseline documentale source-neutral. La decisione riconosce la completezza del contratto normativo e la verifica post-merge della PR #193; non dichiara implementazione, disponibilità del sito, validazione eseguibile o production readiness.

Il contratto resta fail-closed: assenza, gap, conflitto, record invalido o accesso non autorizzato non possono produrre coordinate presunte, timezone host, “latest wins” o readiness operativa.

## 2. Evidenza di integrazione

| Evidenza | Esito |
|---|---|
| PR #193 | merged |
| ARB AI-assisted sul technical head `8bc4c8ed131bce0580ff95905b130b191605e2e7` | APPROVED WITH CONDITIONS — 96/100 |
| Release Quality AI-assisted sul technical head `8bc4c8ed131bce0580ff95905b130b191605e2e7` | CONDITIONALLY READY FOR MERGE |
| Review-publication head | `b81187c58811399b10eb3e1efeadc62491f01918` |
| Merge commit su `main` | `b9d08a7cf6b6287825907cab6a846b1ec70f0378` |
| Workflow post-merge | 9/9 SUCCESS |
| Pages build/integrity e deployment | SUCCESS |
| Governed Projection Sync | SUCCESS |

Le review AI-assistite sono state autorizzate dall'owner e non equivalgono ad approvazioni umane indipendenti.

## 3. Scope accettato

Sono accettati come specifica:

- aggregate logico `GovernedSiteRecord` e lifecycle governato;
- value object `HalfOpenValidityInterval`;
- semantica UTC half-open, end unbounded esplicita, adjacency valida e overlap fail-closed;
- risoluzione deterministica di current, gap, conflitto e invalidità;
- porta Application `SiteAuthorityPort` source-neutral;
- separazione fra record interno protetto e public reference sanitizzato;
- failure semantics, audit boundary e validation matrix documentale;
- ordine di materializzazione futuro, soggetto a decisioni separate.

## 4. Condizioni carried-forward

| ID | Stato | Gate |
|---|---|---|
| `ARB-193-MI01` | OPEN / CARRIED | definire vertical reference, unità e range ammesso di `elevationM` prima di F3-B |
| `ARB-193-MI02` | OPEN / CARRIED | definire identità canonica del resolver e ambito dell'autorità prima di F3-B |
| `ARB-191-MI01` | OPEN / CARRIED | enforcement pubblico/interno e leak tests obbligatori prima di F3-B/F3-C |
| `ARB-191-MI02` | NORMATIVE DESIGN SATISFIED / EXECUTABLE GATE OPEN | test eseguibili su boundary, adjacency, overlap e unbounded obbligatori prima della materializzazione |

Le condizioni non bloccano l'accettazione della specifica documentale. Bloccano qualsiasi claim di implementazione o materializzazione che ne dipenda.

## 5. Verifica post-merge

Sul merge commit `b9d08a7cf6b6287825907cab6a846b1ec70f0378` hanno concluso SUCCESS:

1. Developer Foundation — run 34948679039;
2. Validate documentation — run 34948678997;
3. Generate Word Documentation — run 34948679487;
4. Deploy MkDocs Portal to Pages — run 34948679648;
5. Governed Projection Sync — run 34948679540;
6. Scientific Platform Governance — run 34948679166;
7. BKL-041 F4 Workflow Validation — run 34948679034;
8. BKL-046 F4 Contract Validation — run 34948679011;
9. BKL-046 F5 Contract Validation — run 34948678974.

L'evidenza vale esclusivamente per l'exact SHA indicato.

## 6. Stati e boundary preservati

- S08 resta `UNAVAILABLE`: non esiste un record sito approvato materializzato;
- S09 resta `UNAVAILABLE_CURRENT`;
- S10 resta `UNAVAILABLE`;
- coordinate, elevation, locator e digest interni non sono pubblicati;
- nessun schema, fixture, validator, adapter, persistence, provider o API è stato introdotto;
- nessun forecast, ranking, readiness/go-no-go, device command o automatic remediation è autorizzato;
- PC/EAGLE e Safety Authority fisica/locale non sono modificati.

## 7. Waiver e ruleset

La decisione owner relativa all'assenza del ruleset di `main` per il merge #193 è registrata come waiver una tantum `W-BKL031-F3A1-MERGE-001`. È **CONSUMED / EXPIRED**, non è riutilizzabile e non costituisce precedente automatico.

## 8. Rollback

Il rollback è documentale: revert del merge #193 e, se necessario, di questa riconciliazione. Non sono richieste migrazioni dati, rotazioni di credenziali, rollback runtime o azioni hardware.

## 9. Prossima azione governata

La prossima azione è una decisione owner separata sul successore. Questa acceptance non promuove F3-A2, F3-A3, F3-B o F3-C e non autorizza la materializzazione del Site Authority Contract.

Ogni successore dovrà dichiarare scope, dependency order, condizioni applicabili, exact-head CI, review e boundary di sicurezza.
