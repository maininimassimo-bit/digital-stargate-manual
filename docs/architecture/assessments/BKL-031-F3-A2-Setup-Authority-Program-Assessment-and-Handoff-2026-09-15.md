# BKL-031 F3-A2 — Setup Authority Program Assessment and Handoff

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F3-A2-PROGRAM-001 |
| Stato | **AUTHORIZED HANDOFF / REVIEW CANDIDATE — NOT IMPLEMENTED** |
| Data | 15/09/2026 |
| Capability | BKL-031 — Observation Planner intelligente |
| Incremento selezionato | F3-A2 — Setup Authority Contract |
| Baseline | `main@1fd771632239cdca38d7527c55b974d805ffd1b9` |
| Predecessore | F3-A1 accepted with conditions / post-merge verified |
| Specialist role | Digital StarGate Solution Architect |
| Runtime / dati reali | None |
| PC Principale / EAGLE | Nessuna azione richiesta |

## 1. Decisione di programma

F3-A2 — Setup Authority Contract è selezionato come successore dependency-ready di F3-A1. La promozione è limitata alla preparazione di un package documentale revisionabile da parte del Solution Architect.

F3-A2 deve definire come il planner risolverà in futuro l'assegnazione governata del setup corrente per un sito, collegandola a una baseline AP-006 stabile e riutilizzando la semantica temporale half-open accettata in F3-A1.

La decisione non materializza `CurrentSetupAssignment`, non crea schema, fixture, validator, adapter, persistence o API e non rende S09 disponibile.

## 2. Baseline verificata

- PR #193 ha integrato F3-A1 in `b9d08a7cf6b6287825907cab6a846b1ec70f0378`;
- PR #194 ha riconciliato l'accettazione F3-A1 in `1fd771632239cdca38d7527c55b974d805ffd1b9`;
- PR #194 ARB AI-assisted: `APPROVED WITH CONDITIONS — 99/100`;
- PR #194 Release Quality AI-assisted: `CONDITIONALLY READY FOR MERGE`;
- PR #194 post-merge: 9/9 workflow SUCCESS, inclusi Pages e Governed Projection Sync;
- waiver `W-BKL031-F3A1-ACCEPTANCE-MERGE-001`: CONSUMED / EXPIRED;
- F3-A1 resta documentale e non implementato;
- F3-A2/A3/B/C non erano promossi prima di questa decisione.

Le review AI-assistite non equivalgono ad approvazioni umane indipendenti.

## 3. Maturity assessment

| Area | Maturità | Motivazione |
|---|---:|---|
| F3 source-neutral architecture | 90/100 | accepted with conditions e post-merge verified |
| F3-A1 site authority contract | 85/100 | normative contract accepted; implementation/tests absent |
| F3-A2 setup authority | 35/100 | aggregate e dependency intent defined; detailed contract absent |
| F3-A3 method/provider ADR | 25/100 | alternatives known; provider, license, error budget and evidence open |
| F3-B machine-readable contracts | 20/100 | future sequence defined; schema/fixture/validator not authorized |
| F3-C bounded integration | 10/100 | boundary defined; adapter/projection/OAT absent |
| Runtime/operational readiness | 0/100 | not authorized and no runtime evidence |

I punteggi descrivono maturità documentale/implementativa, non efficacia scientifica.

## 4. Dependency-ordered roadmap

1. F3-A1 — Site Authority Contract: accepted with conditions, not implemented;
2. **F3-A2 — Setup Authority Contract: handoff documentale corrente**;
3. F3-A3 — Method ADR and validation spike: non promosso;
4. F3-B — machine-readable schema/fixture/validator: non promosso;
5. F3-C — bounded adapter/projection/integration: non promosso;
6. F4 — forecast: non promosso;
7. F5 — ranking/consumer read-only: non promosso;
8. F6 — closure: futura.

F3-A3 non precede F3-A2 perché il metodo ephemeris deve ricevere autorità sito e setup con semantiche già definite. F3-B richiede i contratti A1/A2/A3 accettati; F3-C richiede le relative materializzazioni e validazioni.

## 5. Prioritized package backlog

| Priorità | Package | Stato | Gate |
|---|---|---|---|
| 1 | F3-A2 Setup Authority Contract | Current handoff | package documentale + CI + review |
| 2 | F3-A2 Acceptance Reconciliation | Not authorized | solo dopo eventuale merge/review |
| 3 | F3-A3 Method ADR/validation spike | Not promoted | decisione owner separata |
| 4 | F3-B Contracts and Validator | Blocked | A1/A2/A3 accettati e condizioni soddisfatte |
| 5 | F3-C Bounded Integration | Blocked | F3-B accettato e runtime authorization |

## 6. Specialist handoff brief

Il Solution Architect dovrà produrre:

1. un `CurrentSetupAssignment` contract source-neutral;
2. lifecycle, revision, approval, validity e retirement rules;
3. collegamento stabile a un setup/configuration baseline AP-006;
4. regola di current deterministica su intervalli UTC half-open;
5. failure semantics per assenza, gap, overlap, invalidità e reference non risolvibile;
6. Application port separata da storage/framework;
7. boundary protetto/pubblico e policy di sanitizzazione;
8. validation plan positivo/negativo;
9. migration/rollback sequence;
10. traceability verso S09, F3 architecture, F3-A1 e condizioni ARB.

Il package dovrà essere esclusivamente documentale. Nomi di classi o tipi sono logici, non codice approvato.

## 7. Acceptance criteria del futuro package F3-A2

- identity e revision dell'assignment non ambigue;
- site authority reference e configuration reference con ownership dichiarata;
- setup baseline immutable o version-pinned;
- lifecycle `DRAFT/APPROVED/RETIRED` o equivalente esplicitamente governato;
- solo record approved, integro e interval-valid può essere current;
- intervalli UTC `[validFromUtc, validToUtc)` coerenti con F3-A1;
- adjacency valida; gap fail-closed; overlap `CONFLICTED`;
- nessun fallback a latest file, mtime, setup storico o configurazione host;
- public projection allowlisted, senza credenziali, seriali protetti o locator interni;
- S09 resta `UNAVAILABLE_CURRENT` finché non esiste una materializzazione approvata;
- nessun ranking, readiness, scheduler, command o Safety Authority;
- validation cases documentati ma non dichiarati eseguiti.

## 8. Condizioni e dipendenze carried-forward

| ID | Trattamento F3-A2 |
|---|---|
| `ARB-191-MI02` | normativa half-open riutilizzata; test eseguibili ancora obbligatori prima della materializzazione |
| `ARB-191-MI01` | boundary pubblico/interno preservata; enforcement resta gate F3-B/F3-C |
| `ARB-193-MI01` | elevation semantics resta gate del Site Authority prima di F3-B; non risolta da F3-A2 |
| `ARB-193-MI02` | resolver identity/scope resta gate del Site Authority prima di F3-B; F3-A2 deve referenziarlo senza duplicarlo |
| AP-006 | source authority della configuration baseline; non copiare o ridefinire asset identity |
| S09 | `UNAVAILABLE_CURRENT` fino a materializzazione separatamente autorizzata |

## 9. Rischi e controlli

| Rischio | Controllo richiesto |
|---|---|
| setup “latest wins” | current interval-valid e conflict fail-closed |
| mutazione silenziosa della configurazione | reference version-pinned e revision governata |
| duplicazione dell'asset authority AP-006 | reference, non copia, della baseline autorevole |
| assignment incrociato al sito errato | site authority ref protetto e validation negativa |
| esposizione di seriali/locator | public allowlist e redaction |
| fallback alla configurazione EAGLE | comportamento esplicitamente vietato |
| confusione con readiness | nessun score, go/no-go o command |
| falsa implementazione | status NOT IMPLEMENTED e test NOT EXECUTED |

## 10. Quality gates

Prima dell'integrazione del futuro package F3-A2:

- exact-head CI;
- review ARB e Release Quality autorizzate separatamente;
- traceability bootstrap/handover/backlog/roadmap/nav;
- nessun runtime/data/schema delta;
- nessun dato sensibile o credenziale;
- rollback documentale;
- merge/ruleset decision separata.

Prima della materializzazione:

- nuova autorizzazione owner;
- condizioni applicabili soddisfatte;
- schema/fixture/validator review;
- executable boundary/conflict/privacy tests;
- runtime/OAT solo se e quando applicabili.

## 11. Decision and risk summary

**Decisione:** promuovere F3-A2 esclusivamente come handoff documentale al Solution Architect.

**Rischio residuo:** medio-basso per il package documentale; alto se l'assignment venisse materializzato senza identity, interval, AP-006 reference e privacy enforcement.

**Safety:** nessuna variazione. Gli interlock fisici/locali restano indipendenti e autorevoli.

## 12. Governance stop

La corrente autorizzazione termina con la draft PR di questo Program Assessment/Handoff e la verifica CI dell'exact head. Non include:

- progettazione dettagliata del contratto F3-A2;
- ARB o Release Quality;
- merge o nuova deroga ruleset;
- real setup assignment;
- schema, fixture, validator, adapter, persistence o API;
- F3-A3/B/C, F4/F5/F6;
- runtime, PC/EAGLE, command o Safety Authority.
