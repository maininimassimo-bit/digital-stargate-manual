# BKL-031 F3-A1 — Site Authority Contract Validation Plan

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F3-A1-VAL-001 |
| Stato | **ACCEPTED AS PLAN — NOT EXECUTED** |
| Data | 15/09/2026 |
| Contratto | BKL-031-F3-A1-CONTRACT-001 |
| Baseline | `main@b9d08a7cf6b6287825907cab6a846b1ec70f0378` |
| Runtime/OAT | Not Applicable |

## 1. Scopo

Definire l'evidenza richiesta per accettare il contratto F3-A1 e, in futuro, per consentirne la materializzazione. I casi sono specifiche verificabili; nessun test eseguibile, fixture reale o validator è incluso in questa slice.

## 2. Gate

| Gate | Evidenza richiesta ora | Evidenza richiesta prima di F3-B |
|---|---|---|
| MI02 semantica | contratto non ambiguo + review ARB | test eseguibili su boundary, adjacency, overlap e unbounded |
| MI01 privacy | boundary e divieti espliciti | leak tests + digest/canonicalization enforcement |
| Layering | port e responsabilità documentati | dependency tests |
| Runtime | N/A | OAT separato solo dopo implementazione autorizzata |
| Safety | assenza di authority/command | regression assertion |

## 3. Casi positivi

| ID | Scenario | Esito atteso |
|---|---|---|
| A1-P01 | record APPROVED finito, t interno | AVAILABLE |
| A1-P02 | t uguale a `validFromUtc` | AVAILABLE |
| A1-P03 | t appena prima di `validToUtc` | AVAILABLE |
| A1-P04 | intervallo UNBOUNDED, t dopo start | AVAILABLE |
| A1-P05 | `[a,b)` e `[b,c)`, t=b | solo seconda revisione AVAILABLE |
| A1-P06 | WGS84 e coordinate ai limiti ammessi | record semanticamente valido |
| A1-P07 | timezone IANA valida | accettata senza alterare UTC |
| A1-P08 | public projection allowlisted | nessun campo protetto |
| A1-P09 | digest pubblico su payload pubblico | verifica indipendente dal record interno |
| A1-P10 | rollback del package | solo revert documentale |

## 4. Casi negativi — validità temporale

| ID | Scenario | Esito atteso |
|---|---|---|
| A1-N01 | timestamp senza `Z` | INVALID_VALIDITY_INTERVAL |
| A1-N02 | end uguale a start | INVALID_VALIDITY_INTERVAL |
| A1-N03 | end precedente a start | INVALID_VALIDITY_INTERVAL |
| A1-N04 | EXCLUSIVE con end null | INVALID_VALIDITY_INTERVAL |
| A1-N05 | UNBOUNDED con end valorizzato | INVALID_VALIDITY_INTERVAL |
| A1-N06 | data sentinella usata come unbounded | rifiuto |
| A1-N07 | t uguale a end esclusivo senza successore | UNAVAILABLE |
| A1-N08 | gap tra intervalli | VALIDITY_GAP |
| A1-N09 | due record APPROVED in overlap | CONFLICTED |
| A1-N10 | intervallo unbounded seguito da altro APPROVED | CONFLICTED |
| A1-N11 | overlap risolto con revision più alta | comportamento vietato |
| A1-N12 | overlap risolto con mtime/latest file | comportamento vietato |

## 5. Casi negativi — lifecycle, integrità e semantica

| ID | Scenario | Esito atteso |
|---|---|---|
| A1-N13 | solo record DRAFT | UNAVAILABLE |
| A1-N14 | solo record RETIRED | UNAVAILABLE |
| A1-N15 | APPROVED senza approver/timestamp | INVALID |
| A1-N16 | revision zero/negativa | INVALID |
| A1-N17 | digest interno mismatch | INTEGRITY_FAILURE |
| A1-N18 | authority role mancante | INVALID |
| A1-N19 | owner/custodian mancanti | INVALID |
| A1-N20 | datum diverso da WGS84 | INVALID_SITE_SEMANTICS |
| A1-N21 | latitudine fuori range | INVALID_SITE_SEMANTICS |
| A1-N22 | longitudine fuori range | INVALID_SITE_SEMANTICS |
| A1-N23 | NaN/Infinity in coordinate | INVALID_SITE_SEMANTICS |
| A1-N24 | timezone offset-only | INVALID_SITE_SEMANTICS |
| A1-N25 | timezone IANA sconosciuta | INVALID_SITE_SEMANTICS |
| A1-N26 | fallback a coordinate zero | comportamento vietato |
| A1-N27 | fallback a timezone host | comportamento vietato |

## 6. Casi negativi — privacy e authorization

| ID | Scenario | Esito atteso |
|---|---|---|
| A1-N28 | public payload contiene coordinate | leak test fallisce |
| A1-N29 | public payload contiene elevation | leak test fallisce |
| A1-N30 | public payload contiene source locator | leak test fallisce |
| A1-N31 | public payload contiene internal ID/digest | leak test fallisce |
| A1-N32 | public ref derivato dall'internal ID | rifiuto |
| A1-N33 | public digest include campi protetti | rifiuto |
| A1-N34 | log contiene coordinate/locator | redaction failure |
| A1-N35 | caller non autorizzato richiede exact site | deny + audit |
| A1-N36 | conflict evidence esposta pubblicamente | leak test fallisce |
| A1-N37 | projection non sanitizzabile | PUBLIC_PROJECTION_POLICY |

## 7. Casi negativi — boundary e safety

| ID | Scenario | Esito atteso |
|---|---|---|
| A1-N38 | Domain dipende da filesystem/database | architecture test fallisce |
| A1-N39 | contratto seleziona provider ephemeris | scope violation |
| A1-N40 | risultato sito produce readiness/command | boundary test fallisce |
| A1-N41 | workload richiesto su EAGLE | scope violation |

## 8. Esito di review e condizioni

L'ARB AI-assisted della PR #193 ha accettato la risoluzione normativa di `ARB-191-MI02`, mantenendo obbligatori i test eseguibili prima della materializzazione. Restano inoltre open `ARB-193-MI01`, `ARB-193-MI02` e `ARB-191-MI01`.

Il design normativo confermato richiede:

- half-open su ogni intervallo finito;
- start incluso/end escluso;
- unbounded esplicito e senza sentinel;
- adjacency non conflittuale;
- overlap sempre fail-closed;
- nessun tie-break “latest wins”;
- test eseguibili obbligatori prima della materializzazione.

Release Quality della PR #193 ha concluso `CONDITIONALLY READY FOR MERGE`; la verifica post-merge è 9/9 SUCCESS. Le review erano AI-assistite e non equivalgono ad approvazioni umane indipendenti.

## 9. Evidenza non prodotta

Non sono prodotti test runtime, report scientifici, OAT, coordinate reali, fixture, schema, validator, adapter, benchmark o deployment. Tutti i casi restano `NOT EXECUTED` finché una slice di materializzazione non sarà autorizzata.

Il piano è accettato, ma non eseguito, tramite [Acceptance Record F3-A1](../../project/BKL-031-F3-A1-SITE-AUTHORITY-CONTRACT-ACCEPTANCE-2026-09-15.md).

