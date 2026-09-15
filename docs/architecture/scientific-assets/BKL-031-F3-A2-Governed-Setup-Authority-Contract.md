# BKL-031 F3-A2 — Governed Setup Authority Contract

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F3-A2-CONTRACT-001 |
| Stato | **ACCEPTED WITH CONDITIONS / POST-MERGE VERIFIED — NOT IMPLEMENTED** |
| Versione | 1.1 |
| Data | 15/09/2026 |
| Baseline | `main@357a5edfbd39346b10a1a2d751018ff6d1dd208f` |
| Parent handoff | `BKL-031-F3-A2-PROGRAM-001` |
| Parent acceptance | `BKL-031-F3-A2-HANDOFF-ACCEPTANCE-001` |
| Governing architecture | BKL-031 F3 Solution Architecture; AP-006 governance concepts |
| Review disposition | `ARB-195-MI01` closed normatively; `ARB-197-MI01` carried before materialization |
| Runtime / data / schema impact | None |
| PC Principale / EAGLE | Nessuna attività richiesta |

## 1. Scopo e boundary

Questo contratto definisce, a livello logico e source-neutral, come il planner potrà risolvere una configurazione corrente governata per un osservatorio e un istante UTC.

Il contratto definisce identità, authority reference, approval, revision, validità, risoluzione, failure semantics, boundary pubblico/protetto, porte applicative, migrazione e validazione.

Non:

- materializza un `CurrentSetupAssignment`;
- attesta l'esistenza di una baseline setup approvata;
- crea schema, fixture, validator, persistence, adapter o API runtime;
- seleziona CMDB, repository, provider o formato di storage;
- legge configurazioni da EAGLE, N.I.N.A. o altri host;
- rende S09 disponibile;
- introduce ranking, readiness, scheduler, command path o Safety Authority.

## 2. Risoluzione di ARB-195-MI01

Il contratto distingue quattro concetti che non sono intercambiabili:

| Concetto | Authority | Significato | Non prova |
|---|---|---|---|
| AP-006 architecture authority | package/review AP-006 | regole per CI, desired/observed state, baseline, approval e drift | esistenza di una baseline concreta |
| concrete approved baseline instance | futura source authority AP-006-compatible | snapshot immutabile/versionato con owner, custodian, approver, evidence e validità | assegnazione corrente a un sito |
| `CurrentSetupAssignment` | futura Setup Assignment Authority | relazione approvata tra sito e baseline per un intervallo | configurazione osservata realmente sull'host |
| observed/historical configuration evidence | session evidence, export o telemetry | stato osservato o storico e drift evidence | desired authority o current assignment |

AP-006 è quindi una **governance authority**, non un registro materializzato implicitamente. Una baseline concreta è utilizzabile soltanto se una futura `ConfigurationBaselineAuthorityPort` ne risolve identità, versione, digest, ownership, approval evidence e validità.

L'assenza o l'ambiguità della baseline concreta non viene colmata da valori storici, host configuration, file recenti o conoscenza dell'operatore: la risoluzione fallisce in modo esplicito e S09 resta `UNAVAILABLE_CURRENT`.

## 3. Authority model

### 3.1 Ruoli logici obbligatori

| Ruolo | Responsabilità |
|---|---|
| `ConfigurationBaselineOwner` | accountable per contenuto e lifecycle della baseline concreta |
| `ConfigurationBaselineCustodian` | custodia tecnica della source autorevole |
| `BaselineApprovalAuthority` | approva versione, validità ed evidence della baseline |
| `SetupAssignmentOwner` | accountable per la relazione sito-baseline |
| `SetupAssignmentCustodian` | mantiene revisioni e locator dell'assignment |
| `SetupAssignmentApprovalAuthority` | approva attivazione, validità e ritiro dell'assignment |

Il contratto richiede riferimenti governati a questi ruoli, non assegna persone o sistemi reali. La mancata risoluzione di un ruolo rende il record non eligible.

### 3.2 Separation of duties

La baseline e l'assignment richiedono approval evidence separate. L'approvazione della baseline non attiva automaticamente un assignment; l'approvazione dell'assignment non rende valida una baseline assente, non approvata o fuori validità.

Un singolo soggetto può ricoprire più ruoli soltanto se una futura policy autorizzata lo consente. Questo contratto non assume tale policy.

## 4. Value object riutilizzato

F3-A2 riutilizza senza ridefinirlo `HalfOpenValidityInterval` di F3-A1:

- `validFromUtc`: RFC 3339 UTC con suffisso `Z`, limite incluso;
- `validityEndMode`: `EXCLUSIVE` o `UNBOUNDED`;
- `validToUtc`: maggiore dello start per `EXCLUSIVE`, null per `UNBOUNDED`;
- intervallo finito: `validFromUtc <= t && t < validToUtc`;
- intervallo unbounded: `validFromUtc <= t`;
- nessuna data sentinella;
- adiacenza `[a,b)` / `[b,c)` valida;
- overlap fail-closed.

## 5. Reference contract della baseline concreta

`ApprovedSetupBaselineReference` è un envelope protetto verso una baseline esterna. Non copia la baseline e non ne diventa authority.

| Campo logico | Regola |
|---|---|
| `baselineId` | identità stabile assegnata dalla source authority |
| `baselineVersion` | versione immutabile o revision pin esplicito |
| `configurationId` | identità esatta della configurazione desired |
| `baselineDigest` | digest protetto della baseline canonica |
| `baselineOwnerRef` | riferimento risolvibile a `ConfigurationBaselineOwner` |
| `baselineCustodianRef` | riferimento risolvibile a `ConfigurationBaselineCustodian` |
| `baselineApprovalAuthorityRef` | riferimento risolvibile a `BaselineApprovalAuthority` |
| `baselineApprovalEvidenceRef` | evidence immutabile dell'approvazione |
| `baselineApprovedAtUtc` | timestamp UTC dell'approvazione |
| `baselineValidity` | validità effettiva dichiarata dalla source authority |
| `baselineSourceLocator` | locator protetto, mai pubblico |
| `classification` | classificazione governata della baseline/reference |

La porta autorevole deve confermare che tutti i campi si riferiscano alla stessa versione e che, per `asOfUtc`, la baseline sia approvata, effettiva, integra e non ritirata. Un ID presente nel documento architetturale, in un inventario candidato o in una sessione storica non soddisfa il contratto.

## 6. Aggregate `CurrentSetupAssignment`

### 6.1 Identità e integrità

| Campo logico | Regola |
|---|---|
| `schemaVersion` | versione del futuro schema; non materializzata in F3-A2 |
| `assignmentId` | identificatore interno stabile |
| `revision` | intero positivo, monotono per assignment |
| `observatoryId` | identità interna coerente con F3-A1 |
| `siteRecordRef` | riferimento protetto all'exact site authority revision |
| `siteRecordDigest` | digest protetto della revision sito |
| `setupBaselineRef` | `ApprovedSetupBaselineReference` version-pinned |
| `assignmentDigestInternal` | digest del payload canonico protetto; algoritmo futuro |
| `validity` | `HalfOpenValidityInterval` |
| `sourceLocator` | locator protetto e auditabile |
| `classification` | classificazione almeno interna/protetta |

### 6.2 Ownership, approval e lifecycle

| Campo logico | Regola |
|---|---|
| `assignmentOwnerRef` | riferimento governato al responsabile |
| `assignmentCustodianRef` | riferimento governato al custode |
| `assignmentApprovalAuthorityRef` | riferimento governato all'approvatore |
| `approvalState` | `DRAFT`, `APPROVED` o `RETIRED` |
| `approvedByRef` | obbligatorio e coerente con l'authority quando APPROVED |
| `approvedAtUtc` | obbligatorio quando APPROVED |
| `approvalEvidenceRef` | evidence immutabile quando APPROVED |
| `retiredAtUtc` / `retirementEvidenceRef` | obbligatori quando RETIRED |

Le revisioni sono append-only. Una correzione o variazione produce una nuova revision; non sovrascrive silenziosamente quella approvata. DRAFT e RETIRED non sono eligible.

## 7. Eligibility invariants

Un assignment è eligible soltanto se tutte le condizioni sono vere:

1. `approvalState=APPROVED`;
2. identity, revision e digest sono validi;
3. owner, custodian e approval authority sono risolvibili;
4. approval evidence dell'assignment è integra;
5. site authority revision/digest è risolta e coerente con `observatoryId`;
6. `asOfUtc` appartiene all'intervallo half-open dell'assignment;
7. la baseline reference è completa e version-pinned;
8. la source authority risolve esattamente una baseline concreta;
9. la baseline è approvata, integra, effettiva e non ritirata a `asOfUtc`;
10. `configurationId`, `baselineId`, versione e digest coincidono con la source authority.

Observed configuration e drift evidence non rendono eligible un assignment e non possono sostituire la baseline desired.

## 8. Risoluzione deterministica current

Input logico: `observatoryRef`, `asOfUtc`, `purpose`, `callerContext`.

1. autorizzare il caller senza esporre dati in caso di deny;
2. risolvere F3-A1 Site Authority per `observatoryRef/asOfUtc`;
3. se il sito non è AVAILABLE, restituire uno stato fail-closed coerente;
4. caricare tutti gli assignment APPROVED della stessa authority il cui intervallo contiene `asOfUtc`;
5. zero candidati: `UNAVAILABLE_CURRENT`;
6. più candidati: `CONFLICTED`, senza filtrarli mediante revision, timestamp o ordine;
7. per l'unico candidato, verificare integrità, ruoli, approval evidence, site binding e baseline reference;
8. risolvere la concrete baseline tramite la porta AP-006-compatible;
9. restituire `AVAILABLE` soltanto se tutte le invarianti sono soddisfatte.

È vietato usare:

- “latest wins”;
- revision più alta come tie-break;
- mtime, nome file o ordine directory;
- ultima configurazione di sessione;
- `configuration-summary.csv`;
- configurazione host/EAGLE/N.I.N.A.;
- default o memoria dell'operatore.

## 9. Application e outbound ports

### 9.1 Inbound port

`SetupAuthorityPort.resolveCurrentSetup(request) -> SetupAuthorityResolution`

Request:

- `observatoryRef`;
- `asOfUtc`;
- `purpose`;
- `callerContext`;
- `correlationId`.

Resolution:

- `state`: `AVAILABLE`, `UNAVAILABLE_CURRENT`, `CONFLICTED` o `INVALID`;
- `reasonCode`;
- `resolvedAtUtc`;
- `assignment` protetto solo quando autorizzato e AVAILABLE;
- `publicReference` sanitizzato quando ammesso;
- `provenance` e `validationSummary`;
- `conflictEvidenceRef` protetto solo per audit autorizzato.

### 9.2 Outbound ports

| Porta | Responsabilità |
|---|---|
| `SiteAuthorityPort` | risolve la site authority F3-A1 senza duplicarla |
| `SetupAssignmentRepositoryPort` | restituisce tutti i candidati per authority e intervallo |
| `ConfigurationBaselineAuthorityPort` | risolve la concrete approved baseline e la sua evidence |
| `SetupPublicProjectionPolicyPort` | applica allowlist e classificazione |
| `SetupAuthorityAuditPort` | registra decisione, reason e correlation senza payload sensibile |

Storage, framework, protocollo e vendor appartengono a futuri adapter Infrastructure.

## 10. Component boundaries

| Layer | Responsabilità | Esclusioni |
|---|---|---|
| Domain | identity, lifecycle, eligibility, interval e reason codes | I/O, storage, HTTP, file system |
| Application | orchestrazione dei resolver e policy, risultato fail-closed | parsing vendor, UI, device access |
| Infrastructure | futuri repository/baseline/audit adapters | decisioni di authority |
| Portal projection | futuro read model pubblico sanitizzato | baseline/assignment protetti, command path |

La sequenza logica è: consumer autorizzato → Setup Authority → Site Authority → assignment repository → baseline authority → policy pubblica/audit → resolution. La baseline authority viene interrogata solo nel ramo con un singolo candidato. Ogni errore produce un risultato esplicito, non un fallback.

## 11. Failure semantics

| Evento | Esito |
|---|---|
| site authority unavailable | `UNAVAILABLE_CURRENT / SITE_AUTHORITY_UNAVAILABLE` |
| site authority conflicted/invalid | `CONFLICTED` o `INVALID / SITE_AUTHORITY_FAILURE` |
| nessun assignment approvato | `UNAVAILABLE_CURRENT / NO_APPROVED_ASSIGNMENT` |
| gap temporale | `UNAVAILABLE_CURRENT / VALIDITY_GAP` |
| più assignment interval-valid | `CONFLICTED / OVERLAPPING_APPROVED_ASSIGNMENTS` |
| intervallo/timestamp invalido | `INVALID / INVALID_VALIDITY_INTERVAL` |
| assignment DRAFT o RETIRED | non eligible; mai current |
| identity/revision/digest assignment invalido | `INVALID / ASSIGNMENT_INTEGRITY_FAILURE` |
| ownership/approval assignment incompleta | `INVALID / ASSIGNMENT_AUTHORITY_INCOMPLETE` |
| site binding incoerente | `INVALID / SITE_ASSIGNMENT_MISMATCH` |
| baseline reference mancante | `UNAVAILABLE_CURRENT / BASELINE_REFERENCE_MISSING` |
| baseline non trovata | `UNAVAILABLE_CURRENT / BASELINE_NOT_RESOLVABLE` |
| più baseline per la stessa reference | `CONFLICTED / AMBIGUOUS_BASELINE_REFERENCE` |
| baseline non approvata/non effettiva/ritirata | `INVALID / BASELINE_NOT_APPROVED_EFFECTIVE` |
| owner/custodian/approver baseline non risolvibile | `INVALID / BASELINE_AUTHORITY_INCOMPLETE` |
| digest/version mismatch | `INVALID / BASELINE_INTEGRITY_FAILURE` |
| configuration mismatch | `INVALID / CONFIGURATION_BASELINE_MISMATCH` |
| caller non autorizzato | deny + audit; nessun payload |
| projection pubblica non sanitizzabile | `UNAVAILABLE_CURRENT / PUBLIC_PROJECTION_POLICY` |

## 12. Boundary protetto/pubblico

`PublicSetupReference` è un namespace separato e contiene soltanto:

- `publicSetupRef`: ID opaco assegnato indipendentemente;
- `publicEvidenceDigest`: digest del solo payload pubblico canonico;
- `availabilityState` e `publicReasonCode`, scelto da una enum pubblica generalizzata e separata dai reason code interni;
- `asOfUtc`;
- `configurationPublicRef`, label e validità solo quando ciascun campo è classificato pubblico;
- provenance pubblicabile senza locator protetti.

Non contiene assignment ID/revision/digest, observatory ID, site record reference, baseline ID/version/digest, owner/custodian/approver reference, approval evidence, source locator, seriali, licenze, credential reference, conflict evidence o reason code interno. I dettagli interni sono mappati solo a categorie pubbliche allowlisted; in assenza di una mappatura autorizzata viene pubblicato esclusivamente lo stato generalizzato.

`publicSetupRef` e `publicEvidenceDigest` non possono essere derivati, hashati o cifrati deterministicamente dai valori interni. L'allowlist è deny-by-default. `ARB-191-MI01` resta aperta fino all'enforcement e ai leak test eseguibili di F3-B/F3-C.

## 13. Security, audit e observability

- least privilege su record, locator ed evidence;
- secret e credential assenti dal contratto e dai log;
- correlation ID opaco;
- audit per creazione revision, approvazione, ritiro, deny, conflict e integrity failure;
- metriche aggregate per stato/reason senza label sensibili;
- conteggio overlap, gap, baseline unresolved e policy failure;
- freshness non trasforma un record storico in current;
- observed drift può generare evidence, non remediation automatica;
- nessun log pubblico contiene digest o reference protetti.

## 14. Migration e rollback

Sequenza futura, ciascuna soggetta ai gate applicabili:

1. accettare questo contratto documentale;
2. completare F3-A3 method ADR/validation spike come package separato;
3. in F3-B definire schema, synthetic fixtures, validator, canonicalizzazione digest e leak test;
4. implementare adapter per assignment e baseline authority solo dopo source/owner approval;
5. materializzare una concrete baseline e un assignment solo con evidence reale e autorizzazione applicabile;
6. attivare il consumer S09 soltanto dopo contract tests e OAT;
7. pubblicare esclusivamente il read model sanitizzato.

Rollback futuro:

- disabilitare activation pointer/read model;
- ritirare l'assignment senza cancellarne audit/evidence;
- lasciare la baseline esterna invariata;
- riportare S09 a `UNAVAILABLE_CURRENT`;
- non selezionare configurazioni storiche o host come fallback.

Il rollback corrente è il revert documentale.

## 15. Traceability

| Requisito | Copertura |
|---|---|
| F3 S09 source authority | aggregate, ports e resolver |
| F3-A2 handoff | identity, lifecycle, validity, failure, public boundary |
| AP-006 desired/baseline concepts | reference envelope e authority port, senza copia |
| `ARB-195-MI01` | separazione architecture/baseline/assignment/observed + role/evidence/failure |
| `ARB-191-MI02` | riuso normativo half-open |
| `ARB-191-MI01` | namespace/allowlist; enforcement futuro |
| F3-A1 | site authority reference e failure propagation |
| S09 missingness | `UNAVAILABLE_CURRENT` finché non esiste materializzazione valida |
| Safety | nessun command, readiness o authority operativa |

## 16. Open implementation decisions

Restano futuri e non impliciti:

- formato/versione dello schema;
- canonicalizzazione e algoritmo digest;
- concrete owner/custodian/approval authority;
- source locator e adapter della baseline authority;
- storage/retention/encryption/key management;
- public classification di configuration reference/label/validity;
- policy di separation of duties;
- migration data e OAT;
- provider/method F3-A3.

Questi elementi non impediscono la review del contratto logico, ma impediscono materializzazione e disponibilità S09 finché non sono deliberati e provati.

## 17. Acceptance gate

Il contratto può essere accettato come specifica documentale soltanto dopo:

- exact-head CI;
- ARB e Release Quality AI-assistite secondo `DSG-AEM-001`;
- conferma della chiusura normativa di `ARB-195-MI01`;
- nessuna claim di baseline, assignment o test eseguibile esistente;
- allineamento bootstrap, handover, baseline, backlog, roadmap e nav;
- merge e post-merge evidence con `W-DSG-AEM-RULESET-001` se applicabile.

Schema, fixture, validator, adapter, materializzazione, runtime ed EAGLE restano fuori scope.
