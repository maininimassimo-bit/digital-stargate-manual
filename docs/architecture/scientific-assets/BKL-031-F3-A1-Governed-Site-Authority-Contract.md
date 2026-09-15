# BKL-031 F3-A1 — Governed Site Authority Contract

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F3-A1-CONTRACT-001 |
| Versione | 1.0 |
| Stato | **PROPOSED REVIEW CANDIDATE — NOT IMPLEMENTED** |
| Data | 15/09/2026 |
| Capability | BKL-031 — Observation Planner intelligente |
| Slice | F3-A1 — Site Authority Contract |
| Source architecture | BKL-031 F3 Solution Architecture |
| Runtime impact | None |

## 1. Scopo

Definire il contratto source-neutral con cui il planner potrà, in un incremento futuro, risolvere il sito osservativo governato. Il contratto non crea record reali, storage, schema eseguibile o adapter e non rende S08 disponibile.

## 2. Invarianti

- il repository/registro approvato è authority; cache e projection non lo sono;
- un sito è current solo se approvato, integro e valido all'istante richiesto;
- assenza, gap, record invalido o conflitto non sono convertiti in dati presunti;
- coordinate e locator sono dati protetti;
- il public reference è indipendente e non correlabile con identificatori o digest interni;
- il Domain non dipende da filesystem, database, framework o API;
- questo contratto non produce readiness, ranking, command o Safety Authority.

## 3. Value object `HalfOpenValidityInterval`

| Campo | Tipo logico | Regola |
|---|---|---|
| `validFromUtc` | RFC 3339 UTC timestamp | obbligatorio, suffisso `Z`, limite incluso |
| `validityEndMode` | `EXCLUSIVE` oppure `UNBOUNDED` | obbligatorio |
| `validToUtc` | RFC 3339 UTC timestamp o null | obbligatorio e > start per `EXCLUSIVE`; null per `UNBOUNDED` |

Per un istante `t`:

- intervallo finito current se `validFromUtc <= t && t < validToUtc`;
- intervallo unbounded current se `validFromUtc <= t`;
- `validToUtc` non è mai incluso;
- non sono ammesse date sentinella per esprimere unbounded;
- tutti i confronti avvengono su istanti UTC normalizzati.

Due revisioni adiacenti `[a,b)` e `[b,c)` sono valide e non si sovrappongono: a `t=b` è candidata solo la seconda. Due revisioni sono in overlap se l'intersezione dei rispettivi intervalli non è vuota; un intervallo unbounded entra in overlap con ogni successivo intervallo della stessa autorità.

Questa sezione costituisce la risoluzione normativa proposta di `ARB-191-MI02`. La condizione può essere chiusa solo dall'ARB e dovrà essere provata da test eseguibili prima della materializzazione.

## 4. Aggregate `GovernedSiteRecord`

### 4.1 Identità e integrità protette

| Campo | Regola |
|---|---|
| `schemaVersion` | versione del futuro schema; non definita materialmente in F3-A1 |
| `siteRecordId` | identificatore interno stabile, non pubblico |
| `observatoryId` | identità interna dell'osservatorio, non pubblica |
| `revision` | intero positivo, monotono per `siteRecordId` |
| `recordDigestInternal` | digest del record canonico protetto; algoritmo/versione da materializzare in F3-B |
| `validity` | `HalfOpenValidityInterval` |

### 4.2 Geodesia e tempo

| Campo | Regola |
|---|---|
| `datum` | esattamente `WGS84` |
| `latitudeDeg` | numero finito, da -90 a +90 |
| `longitudeDeg` | numero finito, da -180 incluso a +180 escluso |
| `elevationM` | numero finito; range operativo da definire nel futuro schema |
| `timezoneIana` | IANA Time Zone ID valido; offset numerico o abbreviazione non sono sufficienti |

Le coordinate sono usate solo da consumer autorizzati. La timezone serve a rendering e policy locali; i calcoli di validità restano UTC.

### 4.3 Authority e lifecycle

| Campo | Regola |
|---|---|
| `authorityRole` | ruolo proprietario della verità del record |
| `ownerRef` | riferimento governato del responsabile |
| `custodianRef` | riferimento governato del custode tecnico |
| `sourceLocator` | locator protetto e auditabile |
| `classification` | almeno `PROTECTED_EXACT_SITE` |
| `approvalState` | `DRAFT`, `APPROVED` o `RETIRED` |
| `approvedByRef` | obbligatorio quando APPROVED |
| `approvedAtUtc` | obbligatorio quando APPROVED, RFC 3339 UTC |
| `retiredAtUtc` | obbligatorio quando RETIRED |

Un record è `eligible` solo se APPROVED, integro, semanticamente valido e interval-valid. DRAFT e RETIRED non diventano current.

## 5. Risoluzione current

Input logico: `observatoryId` e `asOfUtc`.

1. selezionare esclusivamente record eligible della stessa authority;
2. applicare la validità half-open;
3. zero candidati: `UNAVAILABLE` con reason `NO_APPROVED_INTERVAL`;
4. un candidato: `AVAILABLE`;
5. più candidati: `CONFLICTED` con reason `OVERLAPPING_APPROVED_INTERVALS`.

È vietato risolvere il conflitto usando timestamp file, ordine di directory, numero di revisione più alto o “latest wins”. La conflict evidence conserva riferimenti protetti sufficienti per audit, senza esporli nel public read model.

## 6. Boundary interno/pubblico

Il record interno e la projection pubblica appartengono a namespace diversi.

`PublicSiteReference` contiene solo:

- `publicSiteRef`: identificatore opaco assegnato indipendentemente;
- `publicEvidenceDigest`: digest calcolato esclusivamente sul payload pubblico canonico;
- `siteLabelGeneralized`: label non precisa;
- `timezoneDisplay`: valore sanitizzato solo se la policy lo consente;
- `availabilityState` e `reasonCode`;
- `asOfUtc` e provenance pubblicabile.

Non contiene `siteRecordId`, `observatoryId`, `recordDigestInternal`, coordinate esatte, elevation, `sourceLocator`, owner/custodian reference o dettagli di conflict evidence. `publicSiteRef` e `publicEvidenceDigest` non possono essere derivati, hashati o cifrati deterministicamente a partire dai valori interni.

Questa boundary dettaglia `ARB-191-MI01`; la condizione resta aperta fino all'enforcement eseguibile e ai leak test di F3-B/F3-C.

## 7. Application port

`SiteAuthorityPort.resolveSiteAuthority(request) -> SiteAuthorityResolution`

Request:

- `observatoryRef` autorizzato;
- `asOfUtc`;
- `purpose`;
- `callerContext` per policy e audit.

Resolution:

- `state`: `AVAILABLE`, `UNAVAILABLE`, `CONFLICTED` o `INVALID`;
- `reasonCode`;
- `resolvedAtUtc`;
- `site` solo per chiamanti autorizzati e stato AVAILABLE;
- `publicReference` sanitizzato quando previsto;
- `provenance` e `validationSummary`;
- `conflictEvidenceRef` protetto solo per audit autorizzato.

La porta è definita nell'Application layer. Il Domain ospita value object, invarianti e reason codes; Infrastructure implementerà in futuro loader, persistence, digest e policy adapters.

## 8. Failure semantics

| Evento | Esito |
|---|---|
| nessun record approvato valido | `UNAVAILABLE / NO_APPROVED_INTERVAL` |
| gap temporale | `UNAVAILABLE / VALIDITY_GAP` |
| overlap | `CONFLICTED / OVERLAPPING_APPROVED_INTERVALS` |
| timestamp non UTC o intervallo invalido | `INVALID / INVALID_VALIDITY_INTERVAL` |
| coordinate/datum/timezone invalidi | `INVALID / INVALID_SITE_SEMANTICS` |
| digest interno non verificabile | `INVALID / INTEGRITY_FAILURE` |
| accesso non autorizzato | deny + audit, nessun dato sensibile |
| projection pubblica non sanitizzabile | `UNAVAILABLE / PUBLIC_PROJECTION_POLICY` |

Nessun fallimento viene trasformato in coordinate di default, timezone di sistema, ultimo record letto o sito storicamente noto.

## 9. Security, privacy e audit

- least privilege per coordinate e locator;
- encryption at rest/in transit demandata alla futura soluzione;
- log senza coordinate, digest interni o locator;
- eventi audit per approvazione, ritiro, risoluzione conflitto e accesso negato;
- public projection verificata con allowlist;
- nessuna credenziale o dato reale in questo package.

## 10. Observability

Metriche future, senza label sensibili:

- conteggi di AVAILABLE/UNAVAILABLE/CONFLICTED/INVALID;
- failure reason aggregati;
- età della revision authority;
- numero di overlap/gap;
- fallimenti di integrità e policy.

Correlation ID e evidence reference devono essere opachi e non rivelare il sito.

## 11. Migrazione e rollback

La materializzazione futura seguirà: schema/validator -> bounded fixture sintetica -> repository adapter -> contract tests -> authority record approvato -> consumer integration. Ogni passo richiede autorizzazione separata.

Il rollback di F3-A1 è il revert documentale. Nessun dato, dipendenza, secret, runtime o dispositivo è modificato.

## 12. Traceability

| Requisito F3 | Regola F3-A1 |
|---|---|
| S08 source authority | aggregate e Application port |
| current validity | UTC half-open e risoluzione deterministica |
| missingness/conflict | stati fail-closed |
| exact-site privacy | protected record + sanitized public reference |
| MI02 | semantica normativa e adjacency cases |
| MI01 | namespace/digest separation; enforcement futuro |
| safety boundary | nessun readiness, command o authority operativa |

## 13. Open decisions

Restano aperti: formato schema, algoritmo e canonicalizzazione digest, storage, owner registry, policy di generalizzazione geografica, range elevation, retention, key management e adapter. La loro risoluzione non è implicita in questo contratto.

## 14. Governance stop

Questo documento è un review candidate, non un contratto accettato o implementato. Non autorizza record reali, schema, fixture, validator, adapter, provider, F3-A2/A3/B/C, runtime, EAGLE o Safety Authority.

