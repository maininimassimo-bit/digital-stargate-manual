# BKL-031 F3-A1 — Site Authority Contract Handoff

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F3-A1-HANDOFF-001 |
| Stato | **ACCEPTED WITH CONDITIONS / POST-MERGE VERIFIED — NOT IMPLEMENTED** |
| Data | 15/09/2026 |
| Capability | BKL-031 — Observation Planner intelligente |
| Incremento | F3-A1 — Site Authority Contract |
| Baseline | `main@b9d08a7cf6b6287825907cab6a846b1ec70f0378` |
| Predecessore | BKL-031 F3 Solution Architecture accepted with conditions |
| Impatto runtime | None |
| PC Principale / EAGLE | Nessuna azione richiesta |

## 1. Decisione di handoff

F3-A1 è stato promosso, valutato e integrato come incremento esclusivamente documentale. PR #193 è merged in `b9d08a7cf6b6287825907cab6a846b1ec70f0378` e la verifica post-merge è 9/9 SUCCESS. Il contratto è accettato con condizioni come baseline normativa; non materializza dati, non seleziona storage o provider e non rende disponibile S08.

Le review ARB e Release Quality sulla PR #193 erano AI-assistite e non equivalgono ad approvazioni umane indipendenti. Acceptance non equivale a implementazione.

## 2. Obiettivo

Definire:

- identità, autorità, approvazione, revisione e validità di `GovernedSiteRecord`;
- semantica UTC half-open `[validFromUtc, validToUtc)` e fine unbounded esplicita;
- risoluzione deterministica di current, gap, overlap e conflitto;
- coordinate WGS84, timezone IANA e responsabilità di custodia;
- separazione fra digest interno e riferimento pubblico non correlabile;
- porta Application source-neutral e failure semantics fail-closed;
- criteri di validazione e gate per la futura materializzazione.

## 3. In scope

1. questo handoff;
2. il contratto normativo F3-A1;
3. il validation plan F3-A1;
4. allineamento di bootstrap, continuity, backlog, roadmap, navigation e registri;
5. proposta di risoluzione di `ARB-191-MI02` sottoposta ad ARB.

## 4. Out of scope

- coordinate o identità reali dell'osservatorio;
- schema JSON, fixture, validator, repository adapter o persistence;
- scelta database, secret store, provider ephemeris, libreria o kernel;
- F3-A2 setup, F3-A3 ADR/provider, F3-B materializzazione e F3-C integration;
- forecast, ranking, readiness/go-no-go, automazioni e device command;
- deployment, workload o modifica del PC/EAGLE;
- Safety Authority o bypass degli interlock locali.

## 5. Dipendenze e condizioni

| Elemento | Trattamento F3-A1 |
|---|---|
| F3 Solution Architecture | baseline accettata |
| `ARB-191-MI02` | normativa accettata; executable interval tests restano gate prima della materializzazione |
| `ARB-191-MI01` | boundary interno/pubblico definito; resta gate aperto per enforcement F3-B/F3-C |
| `ARB-193-MI01` | vertical reference, unità e range di `elevationM` open prima di F3-B |
| `ARB-193-MI02` | resolver canonico e authority scope open prima di F3-B |
| Site/setup authority reale | non disponibile e non materializzata |
| Provider ephemeris | non selezionato; irrilevante per F3-A1 |

## 6. Ordine di delivery

1. F3-A1 contract package, review, merge e post-merge verification — completati;
2. Acceptance Reconciliation — corrente;
3. decisione owner separata sul successore;
4. eventuale slice autorizzata per condizioni/materializzazione;
5. review, merge e verifica propri di ogni slice.

Nessuna fase successiva è implicitamente autorizzata.

## 7. Acceptance criteria del package

- semantica temporale non ambigua e testabile;
- overlap fail-closed senza tie-break impliciti;
- adjacency esplicitamente valida;
- end unbounded rappresentata da modalità esplicita, non da sentinel date;
- record approvato e interval-valid come prerequisito di current;
- coordinate e locator classificati e non pubblicati;
- digest pubblico non derivato da identificatori o digest interni;
- porta Application indipendente da storage/framework;
- validation matrix positiva e negativa completa;
- nessuna dichiarazione di runtime, disponibilità S08 o safety authority.

## 8. Rischi

| Rischio | Controllo |
|---|---|
| Selezione “ultimo file” in presenza di overlap | stato `CONFLICTED` e nessun current |
| Correlazione del sito attraverso digest | namespace e materiale di digest separati |
| Coordinate esposte nel portale | projection pubblica sanitizzata senza coordinate/locator |
| Confusione contratto/implementazione | stato NOT IMPLEMENTED e gate espliciti |
| Deriva di timezone | IANA ID obbligatorio, offset numerico non sufficiente |
| Coupling con EAGLE | contratto repository-only e zero workload operativo |

## 9. Acceptance e governance stop

L'esito è registrato in [BKL-031 F3-A1 — Site Authority Contract Acceptance](../../project/BKL-031-F3-A1-SITE-AUTHORITY-CONTRACT-ACCEPTANCE-2026-09-15.md). Le condizioni `ARB-193-MI01`, `ARB-193-MI02`, `ARB-191-MI01` e il gate eseguibile di `ARB-191-MI02` restano carried-forward.

Questa riconciliazione non autorizza materializzazione o slice successive. ARB, Release Quality e merge della riconciliazione, seguiti dalla decisione sul successore, richiedono passaggi separati.

