# ARB-012 C01/C05 Authorization and Security Test Plan

| Campo | Valore |
|---|---|
| Identificativo | ARB-012-VAL-C01-C05 |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Condizioni | ARB-012-C01 / ARB-012-C05 |
| Ambiente | Simulato o non operativo |
| Stato | Complete simulated scenario implementation — CI evidence pending |
| Data | 30/07/2026 |
| Autorità | Digital StarGate Release and Quality Governor |

## 1. Scopo

Definire una campagna riproducibile per verificare command authorization, identity, role scope, four-eyes, safety denial, idempotency, privileged access e break-glass senza collegare il test harness a dispositivi reali, ASCOM, N.I.N.A., cupola, montatura o altri asset fisici.

Questo documento autorizza esclusivamente preparazione ed esecuzione in ambiente simulato. Non autorizza command path operativi.

## 2. Dipendenze

### 2.1 Dipendenze per l'esecuzione simulata

- OPSC-CMD-001 — Command Authorization Model;
- OPSC-RACI-001 — Operations Responsibility Matrix;
- identity e policy store simulati;
- audit sink simulato append-only;
- Safety Authority stub indipendente;
- command dispatcher fake privo di integrazioni fisiche.

Le identità e i ruoli usati dal test harness sono fixture tecniche. Non costituiscono nomine organizzative.

### 2.2 Dipendenze per la chiusura operativa

- ARB-012-C04 Role Assignment Register completato con identità distinte;
- deleghe, conflict register e access review verificati;
- prova four-eyes con identità realmente autorizzate;
- validazione in ambiente non simulato autorizzata da un futuro gate specifico.

C04 non blocca l'esecuzione tecnica simulata, ma resta obbligatoria prima di qualunque chiusura operativa o runtime di C01/C05.

## 3. Componenti del test harness

| Componente | Responsabilità | Vincolo |
|---|---|---|
| Identity Stub | identità, ruolo, sessione, revoca | nessun account operativo |
| Policy Decision Point | permit/deny e reason code | policy versionata |
| Safety Authority Stub | permit/deny/stop | prevale su ogni altra decisione |
| Four-Eyes Coordinator | secondo approvatore per C3/C4 | identità distinta dal requester |
| Fake Command Dispatcher | registra l'intento senza effetto fisico | nessuna integrazione device |
| Idempotency Store | command ID ed execution outcome | duplicati senza doppio effetto |
| Audit Sink | timeline append-only | correlation ID, payload hash e approval chain |
| Break-Glass Controller | accesso temporaneo, notifica, revoca e post-review | approvatore distinto richiesto |
| Security Event Sink | eventi di abuso o accesso negato | simulato, nessun SIEM operativo |

## 4. Dataset minimo

Le identità simulate includono Operator, Senior Operator, Security Authority, Safety Authority, Auditor e utente senza ruolo. Sono esclusivamente fixture di test.

Le classi simulate sono C1, C2, C3 e C4. C3 richiede four-eyes; C4 richiede four-eyes e decisione prevalente della Safety Authority.

## 5. Scenari ARB-012-C01

| ID | Scenario | Stato implementazione |
|---|---|---|
| C01-S01 | C1 con identità, ruolo e scope validi | Implemented |
| C01-S02 | C3 senza secondo approvatore distinto | Implemented |
| C01-S03 | C3 con requester e approver identici | Implemented |
| C01-S04 | autorizzazione scaduta | Implemented |
| C01-S05 | telemetry stale/unknown/conflicting | Implemented |
| C01-S06 | Safety Authority deny | Implemented |
| C01-S07 | command ID duplicato | Implemented |
| C01-S08 | timeout dopo dispatch e riconciliazione esplicita | Implemented |
| C01-S09 | privilegio revocato tra approval ed execution | Implemented |
| C01-S10 | utente senza ruolo con security event | Implemented |

### Criterio di chiusura simulata C01

Tutti gli scenari devono passare in CI. Ogni decisione deve riportare actor, role, policy version, command class, command ID, correlation ID, reason code, safety decision, timestamp, payload hash, approval chain e outcome.

L'implementazione è completa nel test harness; lo stato resta `Not Executed — implementation complete, CI evidence pending` fino al completamento positivo del workflow sulla branch corrente.

## 6. Scenari ARB-012-C05

| ID | Scenario | Stato implementazione |
|---|---|---|
| C05-S01 | privileged access approvato, con approvatore distinto e time-bound | Implemented |
| C05-S02 | accesso fuori scope | Implemented |
| C05-S03 | break-glass con motivazione, expiry e notifica | Implemented |
| C05-S04 | break-glass senza motivazione | Implemented |
| C05-S05 | scadenza con revoca automatica | Implemented |
| C05-S06 | riuso dopo revoca con security event | Implemented |
| C05-S07 | Security Authority tenta di dichiarare safe state | Implemented |
| C05-S08 | amministratore tenta comando senza ruolo operativo | Implemented |
| C05-S09 | post-review mancante blocca la chiusura | Implemented |
| C05-S10 | Auditor tenta dispatch | Implemented |

### Criterio di chiusura simulata C05

Ogni break-glass deve avere approvatore distinto, motivo, scope, durata, notifica, revoca e post-review. La chiusura deve essere negata finché il post-review non è completato.

L'implementazione è completa nel test harness; lo stato resta `Not Executed — implementation complete, CI evidence pending` fino al completamento positivo del workflow sulla branch corrente.

## 7. Evidence package

L'esecuzione deve produrre o rendere verificabili almeno:

```text
run_id
commit_sha
scenario_id
started_at
completed_at
actor
roles
policy_version
command_class
command_id
correlation_id
decision
reason_code
safety_decision
approval_chain
break_glass_record
notification_record
revocation_record
post_review_record
payload_hash
assertion_results
```

Artefatti richiesti per la chiusura simulata:

- report test del workflow GitHub Actions;
- test harness versionato;
- audit record simulati verificati tramite assertion;
- fixture di identità e ruoli nel test harness;
- summary Passed/Failed per scenario;
- approvazione del Release and Quality Governor;
- riesame indipendente ARB prima di qualunque interpretazione operativa.

## 8. Stop conditions

Interrompere immediatamente la prova se il dispatcher è collegato a dispositivi reali, se viene rilevato un endpoint operativo, se un test modifica configurazioni reali, se il Safety Authority stub non prevale, se un comando negato produce un effetto o se l'audit trail non è disponibile.

## 9. Stato e disposizione

- ARB-012-C01: `Not Executed — implementation complete, CI evidence pending`;
- ARB-012-C05: `Not Executed — implementation complete, CI evidence pending`;
- test design: `Complete for simulated scope`;
- test harness: `Implemented for all listed simulated scenarios`;
- execution evidence: `Pending CI on current head`;
- C04 organizational prerequisite: `Blocked — bootstrap assignments recorded`;
- runtime enablement: `Prohibited`.

Un esito positivo della CI potrà dimostrare esclusivamente la copertura simulata completa. Non chiuderà i requisiti organizzativi, operativi o runtime collegati a C04 e non autorizzerà adattatori verso hardware o sistemi reali.
