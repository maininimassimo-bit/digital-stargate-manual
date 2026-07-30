# ARB-012 C01/C05 Authorization and Security Test Plan

| Campo | Valore |
|---|---|
| Identificativo | ARB-012-VAL-C01-C05 |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Condizioni | ARB-012-C01 / ARB-012-C05 |
| Ambiente | Simulato o non operativo |
| Stato | Partial simulated execution completed — closure criteria pending |
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

- ARB-012-C04 Role Assignment Register completato;
- decisione nominativa dello Sponsor registrata nell'issue #11;
- deleghe, conflict register e access review verificati;
- prova four-eyes con identità realmente autorizzate.

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
| Audit Sink | timeline append-only | correlation ID e payload hash richiesti per la chiusura |
| Break-Glass Controller | accesso temporaneo e revoca | approvazione, notifica e post-review richiesti per la chiusura |

## 4. Dataset minimo

Le identità simulate includono Operator, Senior Operator, Maintainer, Security Authority, Safety Authority, Auditor e utente senza ruolo. Sono esclusivamente fixture di test.

Le classi simulate sono C1, C2, C3 e C4. C3 richiede four-eyes; C4 richiede four-eyes e decisione prevalente della Safety Authority.

## 5. Scenari ARB-012-C01

| ID | Scenario | Stato corrente |
|---|---|---|
| C01-S01 | C1 con identità, ruolo e scope validi | Executed |
| C01-S02 | C3 senza secondo approvatore | Executed tramite approvatore non distinto |
| C01-S03 | C3 con requester e approver identici | Executed |
| C01-S04 | autorizzazione scaduta | Executed |
| C01-S05 | telemetry stale/unknown/conflicting | Executed |
| C01-S06 | Safety Authority deny | Executed |
| C01-S07 | command ID duplicato | Executed |
| C01-S08 | retry dopo timeout con riconciliazione esplicita | Partial — replay idempotente verificato, timeout non modellato |
| C01-S09 | privilegio revocato tra approval ed execution | Partial — revoca prima della chiamata verificata |
| C01-S10 | utente senza ruolo con security event | Partial — deny verificato, security event dedicato non prodotto |

### Criterio di chiusura C01

Tutti gli scenari devono passare e ogni decisione deve riportare actor, role, policy version, command ID, correlation ID, reason code, safety decision, timestamp e outcome. L'implementazione corrente non produce ancora tutti questi campi e artefatti; pertanto C01 resta `Not Executed — partial simulated coverage`.

## 6. Scenari ARB-012-C05

| ID | Scenario | Stato corrente |
|---|---|---|
| C05-S01 | privileged access approvato e time-bound | Partial — durata e scope verificati, approvatore non modellato |
| C05-S02 | accesso fuori scope | Executed |
| C05-S03 | break-glass con motivazione valida, expiry e notifica | Partial — motivazione ed expiry verificate, notifica assente |
| C05-S04 | break-glass senza motivazione | Executed |
| C05-S05 | scadenza break-glass | Executed come denial dopo expiry; evento di revoca automatica non prodotto |
| C05-S06 | riuso dopo revoca con security event | Partial — deny verificato, security event dedicato assente |
| C05-S07 | Security Authority tenta di dichiarare safe state | Executed |
| C05-S08 | amministratore tenta comando senza ruolo operativo | Executed |
| C05-S09 | post-review mancante | Not Executed |
| C05-S10 | Auditor tenta dispatch | Executed |

### Criterio di chiusura C05

Ogni break-glass deve avere approvatore, motivo, scope, durata, notifica, revoca e post-review. Poiché approvatore, notifica, post-review e catena completa di evidenza non sono ancora implementati, C05 resta `Not Executed — partial simulated coverage`.

## 7. Evidence package richiesto

L'esecuzione completa deve produrre almeno:

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
audit_hash
assertion_results
```

Artefatti obbligatori per la chiusura:

- report JUnit o equivalente;
- log strutturati JSON;
- policy fixture versionata;
- identity e role fixture;
- audit timeline;
- summary Passed/Failed per scenario;
- approvazione del Release and Quality Governor;
- riesame indipendente ARB.

## 8. Stop conditions

Interrompere immediatamente la prova se il dispatcher è collegato a dispositivi reali, se viene rilevato un endpoint operativo, se un test modifica configurazioni reali, se il Safety Authority stub non prevale, se un comando negato produce un effetto o se l'audit trail non è disponibile.

## 9. Stato e disposizione

- ARB-012-C01: `Not Executed — partial simulated coverage`;
- ARB-012-C05: `Not Executed — partial simulated coverage`;
- test design: `Prepared`;
- test harness: `Partially implemented`;
- execution: `Partial`;
- C04 organizational prerequisite: `Blocked`;
- runtime enablement: `Prohibited`.

Il prossimo incremento tecnico deve completare esclusivamente gli scenari e gli artefatti mancanti in ambiente simulato, senza adattatori verso hardware o sistemi operativi reali.
