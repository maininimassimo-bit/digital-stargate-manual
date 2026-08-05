# ARB-012 C01/C05 — Complete Simulated Execution Evidence

| Campo | Valore |
|---|---|
| Evidence ID | E-ARB012-C01-C05-02 |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Condizioni | ARB-012-C01 / ARB-012-C05 |
| Ambiente | Simulato, non operativo, privo di adattatori hardware |
| Branch di implementazione | `validation/arb-012-c01-c05-completion` |
| Commit verificato | `f99fe91c718071d073cc1776bd1c6c0f3f55c524` |
| Merge commit | `624fb153c9ed0a0651be81e5d7c7a871297ca00d` |
| Test harness | `tests/DigitalStarGate.UnitTests/OperationsCenter/AuthorizationSecurityValidationTests.cs` |
| Workflow | Developer Foundation |
| Workflow run | `30579353794` — run number 179 |
| Job | `quality-gate` — job ID `90995432630` |
| Data verifica | 30/07/2026 |
| Autorità | Digital StarGate Release and Quality Governor |
| Esito | Complete simulated technical coverage; operational closure prohibited |

## 1. Scope e limiti

La prova riguarda esclusivamente fixture, identity store, policy decision, audit sink, dispatcher e break-glass controller simulati. Non sono presenti collegamenti a cupola, montatura, ASCOM, Alpaca, N.I.N.A., rete operativa o dispositivi fisici.

Il risultato non autorizza command path runtime, privilegi reali, break-glass operativo o chiusura organizzativa delle condizioni.

## 2. Copertura ARB-012-C01 verificata

Sono verificati:

- comando autorizzato eseguito una sola volta;
- requester e approver distinti per C3/C4 e diniego dell'auto-approvazione;
- autorizzazione scaduta;
- telemetry stale, unknown e conflicting;
- prevalenza del diniego della Safety Authority;
- idempotenza, retry e riconciliazione dopo timeout simulato;
- revoca tra approval ed execution;
- security event per identità priva di ruolo;
- audit con actor, role, policy version, command class, command ID, correlation ID, reason code, safety decision, approval chain, timestamp, outcome e payload hash.

**Stato C01 nello scope simulato:** `Passed — simulated technical validation`.

**Stato C01 operativo/runtime:** `Blocked by C04 and missing operational integration evidence`.

## 3. Copertura ARB-012-C05 verificata

Sono verificati:

- approvatore distinto dal beneficiario del grant;
- least privilege, scope e durata limitati;
- motivazione obbligatoria;
- notifica di grant, revoca e scadenza;
- revoca automatica alla scadenza;
- security event per riuso dopo revoca;
- post-review obbligatoria e impossibilità di chiusura conforme se assente;
- Security Authority priva di safe-state authority e command authority implicita;
- Auditor read-only e privo di dispatch.

**Stato C05 nello scope simulato:** `Passed — simulated technical validation`.

**Stato C05 operativo/runtime:** `Blocked by C04 and missing operational integration evidence`.

## 4. Evidenza CI

Il workflow `Developer Foundation` run 179 ha completato con conclusione `success` sul final head verificato.

| Gate | Esito |
|---|---|
| Restore | Passed |
| Build | Passed |
| Test | Passed |
| Verify formatting | Passed |
| Setup Python | Passed |
| Install documentation dependencies | Passed |
| Verify MkDocs | Passed |

La CI dimostra compilazione, test e coerenza documentale della copertura simulata. Non dimostra comportamento di dispositivi, integrazioni o identità operative.

## 5. Relazione con C04

Le identità del test harness sono fixture tecniche e non costituiscono nomine. C04 resta `Blocked — bootstrap assignments recorded`; una sola identità organizzativa non soddisfa four-eyes, indipendenza Safety Authority, Auditor indipendente o segregazione dei privilegi.

## 6. Condizioni residue

- C02, C03, C06 e C07 restano `Not Executed`;
- C04 resta `Blocked`;
- nessun adattatore runtime o hardware è validato;
- C3/C4 runtime, break-glass runtime e self-approval restano proibiti;
- gli interlock fisici locali restano indipendenti e autoritativi.

## 7. Disposizione

L'evidenza è accettata come chiusura della **validazione tecnica simulata** di C01 e C05. Non costituisce chiusura operativa delle condizioni né readiness di AP-012.

**Readiness:** `NOT READY FOR RUNTIME ENABLEMENT`.
