# BKL-031 F3-A2 — Setup Authority Contract Validation Plan

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F3-A2-VAL-001 |
| Stato | **ACCEPTED / REPOSITORY VALIDATOR AND 57 CASES IMPLEMENTED** |
| Data | 15/09/2026 |
| Contract | `BKL-031-F3-A2-CONTRACT-001` accepted with conditions / not implemented |
| Review | PR #197 — ARB 97/100; Release Quality conditionally ready; post-merge 9/9 |
| Baseline | `main@357a5edfbd39346b10a1a2d751018ff6d1dd208f` |
| Test data | Synthetic fixtures plus protected exact-reference binding on repository records |
| Runtime / OAT | Not executed / not authorized |

## 1. Scopo

Definire la matrice di validazione del contratto logico F3-A2. I casi sono acceptance criteria futuri; questa pubblicazione non dichiara schema, fixture, validator o test eseguiti.

## 2. Preconditions future

Prima dell'esecuzione dovranno esistere:

- schema versionato e validator autorizzati;
- synthetic fixtures senza dati reali/protetti;
- stub deterministici di Site Authority e Configuration Baseline Authority;
- canonicalizzazione e digest profile approvati;
- public allowlist e deny-list eseguibili;
- test clock UTC controllato;
- log/audit sink privo di payload sensibili.

## 3. Positive cases

| ID | Scenario | Expected |
|---|---|---|
| P01 | un assignment APPROVED, site ref valido, baseline concreta approved/effective | `AVAILABLE` |
| P02 | `asOfUtc=validFromUtc` | limite iniziale incluso |
| P03 | `asOfUtc<validToUtc` | assignment disponibile |
| P04 | adiacenza `[a,b)` e `[b,c)` a `t=b` | solo il secondo candidato |
| P05 | intervallo `UNBOUNDED` con start passato | candidato valido |
| P06 | baseline ID/version/configuration/digest coincidono | baseline reference valida |
| P07 | owner, custodian e approval authority risolvibili | eligibility preservata |
| P08 | assignment e baseline approval evidence separate | entrambe verificate |
| P09 | revision precedente RETIRED e nuova APPROVED non overlapping | nuova revision disponibile |
| P10 | public fields tutti classificati e allowlisted | `PublicSetupReference` minima |
| P11 | observed state differisce dal desired | `AVAILABLE` + drift evidence; desired invariata |
| P12 | stesso input/source snapshot ripetuto | stesso esito e provenance riproducibile |

## 4. Negative and fail-closed cases

| ID | Scenario | Expected |
|---|---|---|
| N01 | nessun assignment | `UNAVAILABLE_CURRENT / NO_APPROVED_ASSIGNMENT` |
| N02 | gap tra intervalli | `UNAVAILABLE_CURRENT / VALIDITY_GAP` |
| N03 | due assignment interval-valid | `CONFLICTED / OVERLAPPING_APPROVED_ASSIGNMENTS` |
| N04 | unico assignment DRAFT | non current |
| N05 | unico assignment RETIRED | non current |
| N06 | end uguale/minore di start | `INVALID / INVALID_VALIDITY_INTERVAL` |
| N07 | timestamp senza `Z` o offset non normalizzato | `INVALID / INVALID_VALIDITY_INTERVAL` |
| N08 | end null senza `UNBOUNDED` o sentinel date | invalid |
| N09 | assignment digest non verificabile | `INVALID / ASSIGNMENT_INTEGRITY_FAILURE` |
| N10 | assignment owner/custodian/approver mancante | `INVALID / ASSIGNMENT_AUTHORITY_INCOMPLETE` |
| N11 | approval evidence assignment assente | invalid |
| N12 | site authority unavailable | `UNAVAILABLE_CURRENT / SITE_AUTHORITY_UNAVAILABLE` |
| N13 | site record/digest/observatory mismatch | `INVALID / SITE_ASSIGNMENT_MISMATCH` |
| N14 | baseline reference mancante | `UNAVAILABLE_CURRENT / BASELINE_REFERENCE_MISSING` |
| N15 | baseline ID non risolvibile | `UNAVAILABLE_CURRENT / BASELINE_NOT_RESOLVABLE` |
| N16 | due baseline risolte per la stessa exact reference | `CONFLICTED / AMBIGUOUS_BASELINE_REFERENCE` |
| N17 | baseline DRAFT, non approvata, fuori validità o ritirata | `INVALID / BASELINE_NOT_APPROVED_EFFECTIVE` |
| N18 | baseline owner/custodian/approver non risolvibile | `INVALID / BASELINE_AUTHORITY_INCOMPLETE` |
| N19 | baseline version o digest mismatch | `INVALID / BASELINE_INTEGRITY_FAILURE` |
| N20 | `configurationId` mismatch | `INVALID / CONFIGURATION_BASELINE_MISMATCH` |
| N21 | solo concetto/candidate baseline AP-006, nessuna instance | fail-closed; nessuna existence claim |
| N22 | tentativo “latest session wins” | rifiutato |
| N23 | tentativo di usare configuration summary | rifiutato |
| N24 | tentativo di usare mtime, filename, directory order o revision tie-break | rifiutato |
| N25 | tentativo fallback EAGLE/N.I.N.A./host | rifiutato |
| N26 | observed/drift evidence tenta di sostituire desired | rifiutato; evidence preservata |
| N27 | caller non autorizzato | deny + audit, nessun payload |
| N28 | public payload contiene ID/digest/locator/approval protetti | leak test fallisce |
| N29 | public ref/digest derivato deterministicamente dall'interno | leak test fallisce |
| N30 | campo configuration/label/validity non classificato pubblico | omesso o projection unavailable |
| N31 | conflict evidence esposta al portale | leak test fallisce |
| N32 | errore adapter/baseline authority | fail-closed; nessun fallback |
| N33 | reason code interno copiato nella projection pubblica | leak test fallisce; usare publicReasonCode generalizzato |

## 5. Property and determinism tests

- per ogni `t`, non più di un assignment può produrre AVAILABLE;
- intervalli adiacenti non sono overlap;
- un intervallo unbounded entra in overlap con ogni successivo della stessa authority;
- permutation dell'ordine di input non modifica il risultato;
- revision/mtime/file order non sono tie-break;
- stessa exact authority snapshot produce stessa decisione;
- public canonical payload non contiene token della deny-list;
- reason code interno non è mai pubblicato senza una mappatura allowlisted;
- la rimozione di un approval/authority reference non può aumentare availability;
- un observed fact non può mutare desired assignment;
- un failure non può produrre command, readiness o Safety Authority.

## 6. Security and privacy validation

Verificare:

- allowlist pubblica deny-by-default;
- namespace pubblico distinto;
- public ID/digest non derivabili dagli interni;
- log senza assignment ID, observatory ID, baseline ID/digest, locator, seriali o licenze;
- deny senza payload;
- correlation ID opaco;
- audit evidence accessibile solo al ruolo autorizzato;
- nessun secret/credential in schema, fixture, output o artifact.

## 7. Migration and rollback validation

Future test sequence:

1. validator rejects invalid legacy/candidate inputs;
2. synthetic baseline stub and assignment fixture produce expected state;
3. activation disabled returns S09 to `UNAVAILABLE_CURRENT`;
4. retirement preserves audit and removes current eligibility;
5. adapter failure does not select history/host fallback;
6. rollback restores prior missingness without deleting external baseline evidence;
7. public projection disappears or becomes unavailable without leaking protected reason detail.

## 8. Traceability matrix

| Finding/requisito | Casi |
|---|---|
| `ARB-195-MI01` | P06-P08, N14-N21 |
| `ARB-191-MI02` | P02-P05, N02-N08, property tests |
| `ARB-191-MI01` | P10, N27-N31, security tests |
| F3-A1 site binding | P01, N12-N13 |
| deterministic current | P01-P05, N01-N05, N22-N26 |
| fail-closed S09 | N01-N33 |
| rollback | migration/rollback cases |
| Safety boundary | property test command/readiness prohibition |

## 9. Execution status

| Area | Stato |
|---|---|
| Document consistency | da verificare con CI della PR |
| Schema/fixture/validator | IMPLEMENTED IN F3-A2-D4 |
| Positive/negative tests | EXECUTED — 45/45 PASS on implementation head |
| Leak tests | EXECUTED — PASS on implementation head |
| Property tests | EXECUTED — 6/6 PASS on implementation head |
| Runtime/OAT | NOT EXECUTED / NOT AUTHORIZED |
| PC/EAGLE activity | NONE |

Nessun caso è dichiarato passed finché non esisteranno implementation evidence ed exact-head test output.

## 10. F3-A2-D4 execution evidence

The repository implementation adds the 45 planned A2 cases, six protected D4 binding/schema/privacy cases and six property/boundary cases: 57/57 passed on implementation head `96386395ff0d81d0d93e14666215296ade643a83` in workflow run `35011741820`.

The protected repository DRAFT validates, binds to the two already approved authority records and remains `UNAVAILABLE_CURRENT`. Runtime/OAT remains `NOT APPLICABLE` for this repository-only increment.
