# ARB-012 C01/C05 — Simulated Execution Evidence

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
| Esito | Passed in simulated scope |

## 1. Scope della prova

La prova valida esclusivamente il comportamento del test harness simulato. Non sono presenti collegamenti a cupola, montatura, ASCOM, Alpaca, N.I.N.A., rete operativa o altri dispositivi fisici.

Il risultato non autorizza l'abilitazione di command path runtime.

## 2. Scenari ARB-012-C01 verificati

- comando autorizzato eseguito una sola volta e auditato;
- four-eyes obbligatorio per comandi privilegiati;
- autorizzazione scaduta negata;
- telemetry stale, unknown o conflicting negata per comandi safety-relevant;
- diniego della Safety Authority prevalente;
- retry e duplicati gestiti senza doppia esecuzione;
- privilegio revocato prima dell'esecuzione negato;
- decisioni registrate nell'audit append-only simulato.

**Decisione C01:** `Passed — simulated scope`.

## 3. Scenari ARB-012-C05 verificati

- privileged access limitato per scope e durata;
- accesso fuori scope negato;
- break-glass con motivazione obbligatoria;
- scadenza e revoca del grant;
- Security Authority priva di authority safety e command authority implicita;
- Auditor privo di capacità di dispatch e con sola lettura audit.

**Decisione C05:** `Passed — simulated scope`.

## 4. Evidenza CI

Il workflow `Developer Foundation` run 170 ha completato con conclusione `success`.

| Gate | Esito |
|---|---|
| Restore | Passed |
| Build | Passed |
| Test | Passed |
| Verify formatting | Passed |
| Setup Python | Passed |
| Install documentation dependencies | Passed |
| Verify MkDocs | Passed |

## 5. Limitazioni e condizioni residue

- C04 resta `Blocked` fino alle nomine nominative e alla verifica delle segregazioni organizzative;
- la prova usa identità e ruoli simulati e non costituisce assegnazione organizzativa;
- non sono validate integrazioni runtime, dispositivi fisici o interlock locali;
- C02, C03, C06 e C07 restano `Not Executed`;
- l'abilitazione runtime di AP-012 resta proibita fino alla re-review finale delle condizioni applicabili.

## 6. Disposizione

Le condizioni C01 e C05 sono chiuse per lo scope simulato definito dalla campagna. Ogni futura implementazione runtime dovrà ripetere le prove sull'implementazione effettiva prima dell'abilitazione operativa.