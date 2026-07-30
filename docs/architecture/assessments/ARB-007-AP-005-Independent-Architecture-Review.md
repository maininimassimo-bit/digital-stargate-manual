# ARB-007 — Independent Architecture Review of AP-005

| Campo | Valore |
|---|---|
| Identificativo | ARB-007 |
| Oggetto | AP-005 — Identity, Access and Remote Operations Security Architecture |
| Tipo | Independent Architecture Review |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch | `main` |
| Data | 30/07/2026 |
| Autorità | Digital StarGate Architecture Review Board |
| Package baseline | `b473e16960c405f3f63826fb086f14d7d40e1f75` |
| Package blob | `3b454bb4ea45d525f57688eff8e7fc5d99756da1` |
| Reference architecture blob | `2ec337f7dc9602961787964dfd68b3bf4e4e5b58` |
| Decisione | Approved with Conditions |
| Punteggio complessivo | 91/100 |

## 1. Mandato e indipendenza

ARB-007 valuta AP-005 e la relativa Enterprise Identity and Trust Reference Architecture rispetto alla baseline verificabile del repository. La review non modifica il package, non promuove capability e non considera la completezza documentale prova di implementazione, hardening, cybersecurity readiness o safety certification.

## 2. Artefatti esaminati

- `docs/architecture/packages/AP-005-Identity-Access-and-Remote-Operations-Security-Architecture.md`;
- `docs/architecture/enterprise-identity-and-trust-reference-architecture.md`;
- `docs/architecture/traceability-register.md`;
- `docs/chapters/05-infrastruttura-rete.md` nei limiti delle evidenze richiamate dal package;
- `docs/chapters/24-sicurezza-informatica-accessi-remoti.md` nei limiti delle evidenze richiamate dal package;
- `docs/chapters/42-ruoli-formazione-handover.md` nei limiti delle evidenze richiamate dal package;
- AP-002, AP-003 e AP-004 e relative review repository-backed;
- `mkdocs.yml`.

## 3. Sintesi esecutiva

AP-005 è coerente, prudente e sufficientemente completo per diventare baseline architetturale di identity, authentication, authorization, privileged access e remote operations security.

Il package separa correttamente autenticazione e autorizzazione, distingue read, operate, configure, administer, override ed emergency, impedisce l'equivalenza VPN = autorizzazione e mantiene ogni comando fisico dietro i boundary applicativi di AP-003. La reference architecture preserva inoltre l'indipendenza di finecorsa, E-stop e interlock locali rispetto a IAM, VPN, sessioni remote, cloud e audit.

Il package non inventa provider, protocolli, account, certificati, soglie o capacità runtime. Le principali lacune sono operative: owner e RACI non deliberati, inventario identità e secret assente, command authorization matrix non pubblicata, policy non machine-readable, pilot non eseguito, break-glass non collaudato e session lifecycle non validato.

## 4. Valutazione dimensionale

| Dimensione | Punteggio | Valutazione |
|---|---:|---|
| Completezza architetturale | 93 | Copre identità umane, service e device, lifecycle, sessioni, privilegi, secret, certificati, break-glass, failure mode, migrazione e rollback. |
| Coerenza con architettura esistente | 95 | Allineato ad AP-002, AP-003 e AP-004; preserva direction e boundary. |
| Governance | 88 | Modello e RACI candidati adeguati, ma authority nominative e frequenze operative non deliberate. |
| Sicurezza | 93 | Least privilege, deny-by-default, segregazione, revoca, secret governance e degraded mode sono ben definiti. |
| Safety | 97 | IAM e accesso remoto non diventano mai autorità safety; nessun ruolo può bypassare interlock locali. |
| Scalabilità | 89 | Il modello supporta human, service e device identity, ma manca uno schema eseguibile e una strategia di federazione/deployment verificata. |
| Manutenibilità | 91 | Contratti candidati, lifecycle e migration incrementale riducono accoppiamento; servono policy versionate e test automatici. |
| Operabilità | 85 | Failure matrix e degraded mode sono solidi, ma pilot, session termination, revocation e break-glass non sono dimostrati. |
| Tracciabilità | 92 | Package, reference architecture e gap sono collegati; release mapping ed evidence locator restano incompleti. |
| Validazione e readiness | 83 | Le validazioni documentali sono chiare, ma non esistono test runtime, inventory, exercise o penetration evidence. |

**Punteggio complessivo ponderato: 91/100.**

## 5. Punti di forza

1. Separazione esplicita tra identity, authentication, authorization, session e physical outcome.
2. Divieto di interpretare VPN o reachability come permesso operativo.
3. Nessun flusso implicito Identity → Device.
4. Privilege separation coerente tra operations, administration, override ed emergency.
5. Command authorization model collegato a use case, assurance, approval, audit, runbook e rollback.
6. Secret metadata separati dal valore del secret.
7. Break-glass temporaneo, attribuibile, revocabile e soggetto a review.
8. Failure e degraded mode non concedono accesso implicito.
9. Migrazione incrementale con pilot non safety-critical.
10. Autorità fisica locale preservata in ogni scenario.

## 6. Finding

### Blocker

Nessun Blocker rilevato per l'approvazione della baseline architetturale.

### Major

#### ARB7-M01 — Ownership e authority operative non formalizzate

**Evidenza:** owner proposto, ruoli candidati e RACI da deliberare.

**Rischio:** approvazione, revoca, access review, break-glass e incident accountability non attribuibili in modo operativo.

**Remediation:** nominare Identity and Security Owner, identity sponsor, system owner, privileged-access approver, break-glass custodian e reviewer indipendente; pubblicare RACI e separation-of-duties matrix.

#### ARB7-M02 — Contratti e matrici non machine-readable

**Evidenza:** command authorization, session e secret metadata contract sono candidati testuali.

**Rischio:** policy drift, interpretazioni divergenti, validazione manuale e assenza di compatibility gate.

**Remediation:** pubblicare schema versionati per Identity, Role, Authorization Policy, Session, Secret Metadata, Access Review e Break-glass Event; aggiungere esempi validi/non validi e test di schema.

#### ARB7-M03 — Inventario e baseline di accesso assenti

**Evidenza:** non risultano verificati utenti, service account, device identity, certificati, token, chiavi, privilegi, owner, scadenze e sistemi autorizzati.

**Rischio:** account dormienti, privilegi eccessivi, secret non ruotabili e revoca incompleta.

**Remediation:** completare Fase 0 con inventory protetto, owner, sponsor, scope, expiry, evidence locator e stato; collegare gli elementi ad AP-006 senza pubblicare valori sensibili.

#### ARB7-M04 — Pilot e controlli runtime non dimostrati

**Evidenza:** nessun test di authentication/authorization, deny, timeout, termination, revocation, loss of VPN, compromise o certificate expiry.

**Rischio:** architettura non trasformabile in readiness operativa verificabile.

**Remediation:** eseguire un pilot read-only o non safety-critical con provisioning, deny test, session timeout, termination, revocation, correlation, audit e recovery da perdita VPN.

#### ARB7-M05 — Break-glass non operativo o collaudato

**Evidenza:** custody, approvazioni, release della credenziale/sessione, revoca, rotation ed exercise non sono verificati.

**Rischio:** lockout durante recovery oppure abuso di privilegi emergency.

**Remediation:** pubblicare procedura, custodia, approvazione, durata, scope, notification, revoca/rotation e post-event review; eseguire tabletop ed esercitazione controllata.

### Minor

#### ARB7-m01 — Timeout, re-authentication e recording non deliberati

Definire valori e criteri per classe di rischio dopo inventory e pilot, senza inventare soglie non misurate.

#### ARB7-m02 — Privacy e retention dei log sensibili incompleti

Collegare attributi personali, session transcript, access log e audit evidence a classificazione, retention, access review e disposal AP-002/AP-004.

#### ARB7-m03 — Release gate incompleto

Ogni release che modifica identity, authorization, remote access o secret lifecycle deve dichiarare policy version, migration, rollback, evidence e open waiver.

#### ARB7-m04 — Build e link validation non eseguite

Eseguire `mkdocs build --strict`, link check e verifica dei diagrammi Mermaid in CI o workspace con checkout.

### Observation

#### ARB7-O01 — Safety boundary particolarmente forte

La separazione tra decisione IAM, use case applicativo, adapter, dispositivo ed esito fisico è uno dei punti più maturi del package.

#### ARB7-O02 — AP-005 e AP-006 sono complementari

AP-005 governa identità e privilegi; AP-006 deve governare inventory e baseline dei relativi CI e locator, senza trasformarsi in secret store.

## 7. Dipendenze e direzione

- AP-005 usa AP-002 per classificazione, retention ed evidence lifecycle.
- AP-005 usa AP-003 per command boundary e application ports.
- AP-005 usa AP-004 per audit, correlation e operations evidence.
- AP-006 può censire identity-related CI e locator, ma non sostituisce authorization o secret governance.
- Dashboard, AI, telemetry e rete non concedono privilegi impliciti.
- Local safety non dipende da IAM, VPN, cloud, repository o audit store.

Non sono stati rilevati conflitti bloccanti o inversioni di dipendenza.

## 8. Decisione

**APPROVED WITH CONDITIONS — 91/100**

AP-005 è approvato come baseline architetturale per Identity, Access and Remote Operations Security.

La decisione non certifica:

- IAM o MFA implementati;
- metodo VPN o device trust;
- privileged-access readiness;
- inventory completo;
- command authorization matrix concreta;
- secret store, PKI o certificate lifecycle runtime;
- break-glass operativo;
- continuous operations o cybersecurity readiness;
- safety certification.

## 9. Condizioni di approvazione

Prima di dichiarare readiness operativa devono essere soddisfatte tutte le seguenti condizioni:

1. owner, authority e RACI formalizzati;
2. inventory di human, service e device identity completato e protetto;
3. command authorization matrix concreta, versionata e approvata;
4. contratti machine-readable con test;
5. session policy deliberata e validata;
6. joiner/mover/leaver, access review e revocation testati;
7. secret/certificate inventory, rotation e expiry evidence disponibili;
8. break-glass procedure ed exercise completati;
9. pilot non safety-critical completato con evidence locator immutabili;
10. loss-of-VPN, compromise, expiry e session-loss testati;
11. release gate e rollback documentati;
12. MkDocs strict build e link check superati;
13. Traceability Register aggiornato;
14. re-review mirata delle condizioni Major prima della promozione operativa.

## 10. Criteri di re-review

La re-review deve ricevere almeno:

- RACI approvato;
- inventory report sanificato;
- policy schema e validation report;
- command authorization matrix;
- session e revocation evidence;
- access review evidence;
- break-glass exercise report;
- pilot report con deny, timeout, termination e recovery;
- audit/correlation evidence;
- release e rollback mapping;
- build e link-check evidence.

## 11. Validazioni eseguite

- repository e branch `main` verificati tramite connettore GitHub;
- AP-005 letto dalla baseline repository;
- Enterprise Identity and Trust Reference Architecture letta dalla baseline repository;
- Traceability Register e MkDocs verificati;
- coerenza documentale con AP-002, AP-003 e AP-004 valutata nei limiti degli artefatti richiamati;
- trust boundary, failure mode, degraded mode, migration e rollback sottoposti a review indipendente.

## 12. Validazioni non eseguite

- inventario reale di utenti, account, token, chiavi e certificati;
- accesso a router, VPN, EAGLE, endpoint o dispositivi;
- test MFA, device trust o conditional access;
- test di timeout, termination, revocation, lockout o compromise;
- break-glass exercise;
- vulnerability assessment o penetration test;
- `mkdocs build --strict` e link check;
- CI/CD e runtime validation;
- test hardware o safety.

## 13. Handoff

Il Program Architect deve registrare ARB-007, mantenere aperte le condizioni ARB7-M01…M05 e coordinare AP-005 con AP-006. Nessuna capability deve essere promossa finché pilot, inventory, policy concrete, break-glass e validation evidence non sono completati.
