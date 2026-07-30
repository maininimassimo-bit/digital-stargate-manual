# ARB-012 C01/C05 Authorization and Security Test Plan

| Campo | Valore |
|---|---|
| Identificativo | ARB-012-VAL-C01-C05 |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Condizioni | ARB-012-C01 / ARB-012-C05 |
| Ambiente | Simulato o non operativo |
| Stato | Test plan approved for preparation — execution pending |
| Data | 30/07/2026 |
| Autorità | Digital StarGate Release and Quality Governor |

## 1. Scopo

Definire una campagna riproducibile per verificare command authorization, identity, role scope, four-eyes, safety denial, idempotency, privileged access e break-glass senza collegare il test harness a dispositivi reali, ASCOM, N.I.N.A., cupola, montatura o altri asset fisici.

Questo documento autorizza esclusivamente la preparazione e l'esecuzione in ambiente simulato. Non autorizza command path operativi.

## 2. Dipendenze

- OPSC-CMD-001 — Command Authorization Model;
- OPSC-RACI-001 — Operations Responsibility Matrix;
- ARB-012-C04 Role Assignment Register;
- decisione nominativa dello Sponsor registrata nell'issue #11;
- identity e policy store simulati;
- audit sink simulato append-only;
- Safety Authority stub indipendente;
- command dispatcher fake privo di integrazioni fisiche.

## 3. Componenti del test harness

| Componente | Responsabilità | Vincolo |
|---|---|---|
| Identity Stub | identità, ruolo, sessione, revoca | nessun account operativo |
| Policy Decision Point | permit/deny e reason code | policy versionata |
| Safety Authority Stub | permit/deny/stop | prevale su ogni altra decisione |
| Four-Eyes Coordinator | secondo approvatore per C3/C4 | identità distinta dal requester |
| Fake Command Dispatcher | registra l'intento senza effetto fisico | nessuna integrazione device |
| Idempotency Store | command ID ed execution outcome | duplicati senza doppio effetto |
| Audit Sink | timeline append-only | correlation ID e payload hash |
| Break-Glass Controller | accesso temporaneo e revoca | scope minimo e post-review |

## 4. Dataset minimo

### Identità simulate

- `operator-a` — Operator;
- `operator-b` — Senior Operator / approvatore candidato;
- `maintainer-a` — Maintainer;
- `security-authority-a` — Security Authority;
- `safety-authority-a` — Safety Authority;
- `auditor-a` — Auditor read-only;
- `unknown-user` — nessun ruolo valido.

Le identità sono esclusivamente fixture di test e non costituiscono nomine organizzative.

### Classi di comando

- C1 — osservazione o azione non critica simulata;
- C2 — azione operativa controllata simulata;
- C3 — azione privilegiata simulata con four-eyes;
- C4 — azione safety-relevant simulata con four-eyes e Safety Authority.

## 5. Scenari ARB-012-C01

| ID | Scenario | Risultato atteso |
|---|---|---|
| C01-S01 | C1 con identità, ruolo e scope validi | Permit e singola registrazione nel fake dispatcher |
| C01-S02 | C3 senza secondo approvatore | Deny; nessun dispatch |
| C01-S03 | C3 con requester e approver identici | Deny per violazione four-eyes |
| C01-S04 | autorizzazione scaduta | Deny con reason code `authorization_expired` |
| C01-S05 | telemetry stale/unknown/conflicting | Deny o block secondo policy; mai permit implicito |
| C01-S06 | Safety Authority deny | Deny prevalente e audit completo |
| C01-S07 | command ID duplicato | stesso outcome; nessun secondo effetto |
| C01-S08 | retry dopo timeout | riconciliazione senza doppia esecuzione |
| C01-S09 | privilegio revocato tra approval ed execution | Deny prima del dispatch |
| C01-S10 | utente senza ruolo | Deny e security event |

### Criterio di chiusura C01

Tutti gli scenari devono passare; nessun comando negato deve raggiungere il fake dispatcher; ogni decisione deve riportare actor, role, policy version, command ID, correlation ID, reason code, safety decision, timestamp e outcome.

## 6. Scenari ARB-012-C05

| ID | Scenario | Risultato atteso |
|---|---|---|
| C05-S01 | privileged access approvato e time-bound | accesso entro scope e durata |
| C05-S02 | accesso fuori scope | Deny e audit |
| C05-S03 | break-glass con motivazione valida | accesso minimo, expiry obbligatoria e notifica |
| C05-S04 | break-glass senza motivazione | Deny |
| C05-S05 | scadenza break-glass | revoca automatica |
| C05-S06 | riuso dopo revoca | Deny e security event |
| C05-S07 | Security Authority tenta di dichiarare safe state | Deny per authority boundary |
| C05-S08 | amministratore tenta comando senza ruolo operativo | Deny; admin non implica command authority |
| C05-S09 | post-review mancante | sessione non chiudibile come conforme |
| C05-S10 | Auditor tenta dispatch | Deny; read-only preservato |

### Criterio di chiusura C05

Tutti gli accessi fuori policy devono essere negati. Ogni break-glass deve avere approvatore, motivo, scope, durata, notifica, revoca e post-review. Nessuna autorità security o amministrativa deve acquisire authority safety o command authority implicita.

## 7. Evidence package

L'esecuzione deve produrre:

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
revocation_record
audit_hash
assertion_results
```

Artefatti attesi:

- report JUnit o equivalente;
- log strutturati JSON;
- policy fixture versionata;
- identity e role fixture;
- audit timeline;
- summary con Passed/Failed per scenario;
- approvazione del Release and Quality Governor;
- riesame indipendente per la chiusura delle condizioni.

## 8. Stop conditions

Interrompere immediatamente la prova se:

- il dispatcher risulta collegato a un dispositivo reale;
- viene rilevato un endpoint ASCOM/Alpaca/N.I.N.A. operativo;
- un test modifica configurazioni reali;
- il Safety Authority stub non prevale;
- un comando negato produce un effetto;
- l'audit trail non è disponibile.

## 9. Stato e disposizione

- ARB-012-C01: `Not Executed`;
- ARB-012-C05: `Not Executed`;
- test design: `Prepared`;
- implementation del test harness: `Missing`;
- esecuzione: `Missing`;
- runtime enablement: `Prohibited`.

Il prossimo incremento tecnico deve implementare esclusivamente il test harness simulato e i test automatici descritti, senza adattatori verso hardware o sistemi operativi reali.