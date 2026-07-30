# ARB-012 C01/C05 — Partial Simulated Execution Evidence

| Campo | Valore |
|---|---|
| Evidence ID | E-ARB012-C01-C05-01 |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Condizioni | ARB-012-C01 / ARB-012-C05 |
| Ambiente | Simulato, non operativo, privo di adattatori hardware |
| Branch | `validation/arb-012-conditions` |
| Commit verificato | `88256a3b551c81925f555ed450db9679bfdf8401` |
| Test harness | `tests/DigitalStarGate.UnitTests/OperationsCenter/AuthorizationSecurityValidationTests.cs` |
| Workflow | Developer Foundation |
| Workflow run | `30574735380` — run number 170 |
| Job | `quality-gate` — job ID `90980032234` |
| Data verifica | 30/07/2026 |
| Autorità | Digital StarGate Release and Quality Governor |
| Esito | Partial simulated coverage — gates not closed |

## 1. Scope della prova

La prova valida esclusivamente un sottoinsieme del comportamento del test harness simulato. Non sono presenti collegamenti a cupola, montatura, ASCOM, Alpaca, N.I.N.A., rete operativa o altri dispositivi fisici.

Il risultato non autorizza l'abilitazione di command path runtime e non costituisce chiusura complessiva di C01 o C05.

## 2. Copertura ARB-012-C01

Copertura verificata:

- comando autorizzato eseguito una sola volta e auditato;
- denial four-eyes quando requester e approver coincidono;
- autorizzazione scaduta negata;
- telemetry stale, unknown o conflicting negata per comandi safety-relevant;
- diniego della Safety Authority prevalente;
- replay duplicato gestito senza doppia esecuzione;
- identità revocata negata;
- decisioni registrate nell'audit sink simulato.

Copertura ancora mancante o incompleta:

- timeout e riconciliazione modellati esplicitamente;
- revoca tra approval ed execution come transizione distinta;
- security event dedicato per utente senza ruolo;
- ruolo, correlation ID, safety decision, payload hash e approval chain nell'audit record;
- log JSON, fixture versionate e report scenario-level richiesti dal piano.

**Stato C01:** `Not Executed — partial simulated coverage`.

## 3. Copertura ARB-012-C05

Copertura verificata:

- accesso privilegiato limitato per scope e durata;
- accesso fuori scope negato;
- motivazione break-glass obbligatoria;
- accesso negato dopo expiry o revoca;
- Security Authority priva di authority safety e command authority implicita;
- Auditor privo di capacità di dispatch e con lettura audit.

Copertura ancora mancante o incompleta:

- approvatore del grant;
- notifica del break-glass;
- evento esplicito di revoca automatica alla scadenza;
- security event per riuso dopo revoca;
- post-review obbligatoria e blocco della chiusura conforme se assente;
- catena evidence completa del break-glass.

**Stato C05:** `Not Executed — partial simulated coverage`.

## 4. Evidenza CI dell'esecuzione parziale

Il workflow `Developer Foundation` run 170 ha completato con conclusione `success` sul commit dell'esecuzione.

| Gate | Esito |
|---|---|
| Restore | Passed |
| Build | Passed |
| Test | Passed |
| Verify formatting | Passed |
| Setup Python | Passed |
| Install documentation dependencies | Passed |
| Verify MkDocs | Passed |

Il superamento della CI prova che il sottoinsieme implementato compila e supera i test; non prova il soddisfacimento degli scenari o degli artefatti non implementati.

## 5. Relazione con C04

Le identità e i ruoli del test harness sono fixture simulate e possono essere usati per validazione tecnica non operativa. C04 resta `Blocked` e rimane prerequisito per assegnazioni reali, four-eyes organizzativo, privilegi operativi e chiusura runtime di C01/C05.

## 6. Condizioni residue

- C02, C03, C06 e C07 restano `Not Executed`;
- C04 resta `Blocked` fino alle nomine nominative e alla verifica delle segregazioni organizzative;
- non sono validate integrazioni runtime, dispositivi fisici o interlock locali;
- l'abilitazione runtime di AP-012 resta proibita fino alla re-review finale delle condizioni applicabili.

## 7. Disposizione

L'evidenza viene accettata come prova parziale di avanzamento tecnico in ambiente simulato. Non chiude C01 o C05. Il prossimo incremento deve completare gli scenari e gli artefatti mancanti oppure mantenere esplicitamente i gate non chiusi.
