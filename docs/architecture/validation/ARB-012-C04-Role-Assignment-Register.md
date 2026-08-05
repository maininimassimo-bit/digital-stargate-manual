# ARB-012-C04 — Role Assignment and Four-Eyes Register

| Campo | Valore |
|---|---|
| Evidence ID | E-ARB012-C04-01 |
| Condizione | ARB-012-C04 — Role Assignment and Four-Eyes Enforcement |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Autorità del modello | OPSC-RACI-001 |
| Data | 31/07/2026 |
| Autorità di nomina | Massimo Mainini — Project Owner / Architecture Sponsor |
| Configurazione | Two-person segregated bootstrap |
| Stato | Primary roles redistributed; substitutes, access reviews and independent audit pending |
| Gate status | Blocked |

## 1. Scopo

Il registro governa assegnazioni nominative, deleghe, conflitti e separazione delle responsabilità necessarie per ARB-012-C04. La registrazione non concede privilegi applicativi, infrastrutturali o fisici e non abilita command path runtime.

La configurazione corrente distribuisce le funzioni operative e tecniche a Massimo Mainini e le funzioni approvative e di controllo a Leonardo Di Egidio. La configurazione riduce i conflitti diretti, ma resta transitoria perché non sono disponibili sostituti indipendenti, l'Auditor appartiene ancora allo stesso pool delle autorità di controllo e non esistono ancora evidenze di formazione, access review o test four-eyes.

## 2. Nominative role register

| Ruolo | Titolare | Sostituto | Autorità di nomina | Validità | Formazione verificata | Access review | Stato |
|---|---|---|---|---|---|---|---|
| Project Owner / Architecture Sponsor | Massimo Mainini | Non nominato | Project governance | Dal 31/07/2026 fino a revoca | N/A per gate operativo | N/A | Established |
| Chief Architect | Massimo Mainini | Non nominato | Sponsor | Dal 31/07/2026 fino a revoca | Da verificare | N/A | Bootstrap assignment |
| Architecture Review Board | Independent ARB function | Non nominato | Sponsor / governance | Per review | Da verificare | Read-only | Function established; membership pending |
| Operations Lead | Massimo Mainini | Non nominato | Sponsor | Dal 31/07/2026 fino a revoca | Da verificare | Da eseguire | Assigned — non operational |
| Service Owner | Massimo Mainini | Non nominato | Sponsor | Dal 31/07/2026 fino a revoca | Da verificare | Da eseguire | Assigned — non operational |
| Technical Owner | Massimo Mainini | Non nominato | Sponsor | Dal 31/07/2026 fino a revoca | Da verificare | Da eseguire | Assigned — non operational |
| Operator | Massimo Mainini | Non nominato | Operations Lead | Dal 31/07/2026 fino a revoca | Da verificare | Da eseguire | Assigned — C0–C2 only if separately authorized |
| Senior Operator / C3 Approver | Leonardo Di Egidio | Non nominato | Sponsor | Dal 31/07/2026 fino a revoca | Da verificare | Da eseguire | Independent from Operator; non operational |
| C4 Second Approver | Leonardo Di Egidio | Non nominato | Sponsor | Dal 31/07/2026 fino a revoca | Da verificare | Da eseguire | Recorded; third independent actor still required for positive C4 validation |
| Incident Coordinator | Massimo Mainini | Non nominato | Operations Lead | Dal 31/07/2026 fino a revoca | Da verificare | Da eseguire | Assigned — non operational |
| Maintainer | Massimo Mainini | Non nominato | Technical Owner | Dal 31/07/2026 fino a revoca | Da verificare | Da eseguire | Assigned — no self return-to-service |
| Return-to-Service Approver | Leonardo Di Egidio | Non nominato | Sponsor / Safety governance | Dal 31/07/2026 fino a revoca | Da verificare | Da eseguire | Independent from Maintainer; non operational |
| Safety Authority | Leonardo Di Egidio | Non nominato | Project Owner / local safety governance | Dal 31/07/2026 fino a revoca | Da verificare | Indipendenza organizzativa parziale | Independent from Operations; runtime authority unavailable |
| Security Authority | Leonardo Di Egidio | Non nominato | Project Owner | Dal 31/07/2026 fino a revoca | Da verificare | Da eseguire | Independent from operational beneficiary; non operational |
| Documentation Governor | Massimo Mainini | Non nominato | Chief Architect | Dal 31/07/2026 fino a revoca | Da verificare | N/A | Assigned |
| Auditor | Leonardo Di Egidio | Non nominato | Sponsor | Dal 31/07/2026 fino a revoca | Da verificare | Read-only da implementare | Provisional; not independent from approval authorities |

## 3. Access matrix baseline

Legenda:

- `R`: richiesta consentita entro scope;
- `A`: approvazione richiesta;
- `E`: esecuzione consentita dopo autorizzazione;
- `D`: negato;
- `TBD`: non assegnabile finché identità, policy e controlli non sono implementati.

| Identità / ruolo | C1 | C2 | C3 | C4 | Safety permit/deny | Break-glass |
|---|---|---|---|---|---|---|
| Massimo Mainini — Operator | TBD | TBD | R/E dopo approvazione distinta | R/E solo dopo catena approvativa completa | D | D |
| Massimo Mainini — Operations Lead | TBD | TBD | R; nessuna auto-approvazione | R; nessuna auto-approvazione | D | D |
| Massimo Mainini — Technical Owner / Maintainer | TBD | TBD | R/E entro maintenance window e approvazione distinta | R/E solo dopo catena approvativa completa | D | D |
| Leonardo Di Egidio — C3 Approver | D | D | A per richieste di Massimo | A primaria; non sufficiente da solo per C4 | D | D |
| Leonardo Di Egidio — C4 Second Approver | D | D | D salvo ruolo C3 esplicito | A secondaria solo con altro approvatore indipendente | D | D |
| Leonardo Di Egidio — Return-to-Service Approver | D | D | A limitata al return-to-service | A limitata al return-to-service | C per verifica safety | D |
| Leonardo Di Egidio — Safety Authority | D | D | permit/deny safety | permit/deny/stop | A/R | D |
| Leonardo Di Egidio — Security Authority | D | D | access approval only | access approval only | D | A solo dopo policy e review indipendente |
| Leonardo Di Egidio — Auditor provvisorio | D | D | D | D | D | D |

La matrice è una baseline documentale. Nessun privilegio è implementato o verificato. C3 può essere validato soltanto in ambiente non operativo con Massimo requester/executor e Leonardo approver. C4 resta bloccato perché una sola identità ricopre entrambe le funzioni approvative e manca un terzo attore indipendente.

## 4. Mandatory segregation rules

1. requester e approver devono essere distinti per C3 e C4;
2. per C4 l'esecutore, l'approvatore primario e il secondo approvatore devono essere organizzativamente indipendenti secondo la policy applicabile;
3. Maintainer e return-to-service approver devono essere distinti;
4. Security Authority non può approvare il proprio accesso;
5. Auditor deve avere accesso read-only e non ricoprire ruoli approvativi sullo stesso evidence set;
6. Safety Authority deve essere indipendente dal DSOC per permit, deny, stop e safe state;
7. policy author e policy approver devono essere distinti;
8. la chiusura SEV-1 richiede four-eyes e verifica del safe state.

La configurazione corrente soddisfa parzialmente i punti 1, 3 e 6. Non soddisfa ancora i punti 2 e 5 e non dispone di evidenza tecnica per gli altri controlli.

## 5. Delegation record

| Delegation ID | Delegante | Delegato | Ruolo/scope | Classi comando | Inizio | Scadenza | Approvatore | Revoca | Stato |
|---|---|---|---|---|---|---|---|---|---|
| DEL-C04-001 | Massimo Mainini — Sponsor | Massimo Mainini | Operations, service, technical ownership, operator, incident, maintenance and documentation governance | Nessuna autorizzazione runtime implicita | 31/07/2026 | Fino a revoca | Massimo Mainini — Sponsor | Immediata | Active with restrictions |
| DEL-C04-002 | Massimo Mainini — Sponsor | Leonardo Di Egidio | C3 approval, C4 second approval, return-to-service, safety, security and provisional audit | Nessuna autorizzazione runtime implicita | 31/07/2026 | Fino a revoca | Massimo Mainini — Sponsor | Immediata | Active with restrictions |

Le deleghe non autorizzano C3/C4 runtime, break-glass o accesso privilegiato. L'attivazione contemporanea di ruoli incompatibili resta vietata.

## 6. Conflict register

| Conflict ID | Persona/ruolo | Conflitto | Rischio | Mitigazione | Approvazione | Stato |
|---|---|---|---|---|---|---|
| CR-001 | Massimo Mainini — Sponsor / Operations / Technical / Maintainer | concentrazione delle funzioni operative e tecniche | High | Leonardo approva C3 e return-to-service; auto-approvazione negata | Sponsor | Mitigated for non-operational C3 testing only |
| CR-002 | Leonardo Di Egidio — C3 Approver / C4 Second Approver | stessa identità copre due livelli approvativi C4 | Critical | C4 bloccato; nominare terzo attore indipendente | Sponsor | Open blocker |
| CR-003 | Leonardo Di Egidio — Safety / Security / Auditor | controllo, sicurezza e audit concentrati nella stessa identità | High | audit considerato provvisorio; nominare Auditor indipendente | Sponsor | Open blocker |
| CR-004 | Entrambe le identità | assenza di sostituti per ruoli critici | High | nessuna attivazione runtime; nominare sostituti distinti e time-bound | Sponsor | Open blocker |
| CR-005 | Entrambe le identità | formazione, identity verification e access review non documentate | High | completare C04-W03 prima di qualsiasi test positivo | Sponsor / future Security Authority | Open blocker |

## 7. Four-eyes validation scenarios

| Scenario | Requester / executor | Approver / verifier | Stato di eseguibilità |
|---|---|---|---|
| C3 request and approval | Massimo Mainini | Leonardo Di Egidio | Preparabile in ambiente non operativo |
| Self-approval rejection | Massimo Mainini | Policy enforcement | Preparabile; controllo tecnico non ancora implementato |
| C4 request with two approvals | Massimo Mainini | Leonardo Di Egidio + terzo attore indipendente | Bloccato |
| Approver revocation before execution | Massimo Mainini | Leonardo Di Egidio / Security Authority | Preparabile dopo identity and access implementation |
| Return-to-service | Massimo Mainini — Maintainer | Leonardo Di Egidio | Preparabile in ambiente non operativo |
| SEV-1 closure | Massimo Mainini | Leonardo Di Egidio + independent audit/safety evidence | Bloccato per indipendenza insufficiente |
| Safety suppression rule | Massimo Mainini — author | Leonardo Di Egidio — approver | Preparabile in ambiente non operativo |
| Independent audit | N/A | Auditor indipendente | Bloccato |

## 8. Closure criteria and current gaps

C04 può diventare `Passed` solo quando:

- i ruoli critici dispongono di sostituti approvati;
- C4 dispone di una catena realmente indipendente;
- l'Auditor è separato dalle autorità approvative;
- formazione, identity verification e access review sono documentate;
- revoca e substitute activation sono verificate;
- gli scenari four-eyes sono eseguiti con audit trail completo;
- l'ARB emette una decisione indipendente `Passed`.

## 9. Decisione corrente

**ARB-012-C04: BLOCKED — two-person segregation recorded.**

La redistribuzione consente la preparazione di prove non operative C3, return-to-service e safety author/approver con due identità distinte. Non consente C4, break-glass, audit indipendente o runtime enablement. Gli interlock fisici locali rimangono indipendenti e autorevoli.