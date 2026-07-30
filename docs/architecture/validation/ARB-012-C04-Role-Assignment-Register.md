# ARB-012-C04 — Role Assignment and Four-Eyes Register

| Campo | Valore |
|---|---|
| Evidence ID | E-ARB012-C04-01 |
| Condizione | ARB-012-C04 — Role Assignment and Four-Eyes Enforcement |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Autorità del modello | OPSC-RACI-001 |
| Data | 30/07/2026 |
| Autorità di nomina | Massimo Mainini — Project Owner / Architecture Sponsor |
| Configurazione | Single-person governance — bootstrap phase |
| Stato | Bootstrap assignments recorded; independent roles and substitutes pending |
| Gate status | Blocked |

## 1. Scopo

Il registro governa le assegnazioni nominative, le sostituzioni, le deleghe, i conflitti di interesse e la separazione delle responsabilità necessarie per rendere operativa la matrice OPSC-RACI-001.

La presenza del registro non abilita privilegi, comandi o ruoli operativi. Ogni assegnazione deve essere approvata, avere validità esplicita ed essere collegata a evidenze di access review e formazione.

La configurazione corrente è una configurazione organizzativa transitoria di bootstrap. Massimo Mainini ricopre provvisoriamente tutti i ruoli nominativi per consentire la formalizzazione della responsabilità durante la fase pre-operativa. Tale cumulo non soddisfa i requisiti di indipendenza, segregation of duties o four-eyes e non autorizza command path runtime.

## 2. Nominative role register

| Ruolo | Titolare | Sostituto | Autorità di nomina | Validità | Formazione verificata | Access review | Stato |
|---|---|---|---|---|---|---|---|
| Project Owner / Architecture Sponsor | Massimo Mainini | Non nominato | Project governance | Dal 30/07/2026 fino a revoca | N/A per gate operativo | N/A | Established |
| Chief Architect | Massimo Mainini | Non nominato | Sponsor | Dal 30/07/2026 fino a revoca | Da verificare | N/A | Bootstrap assignment |
| Architecture Review Board | Independent ARB function | Non nominato | Sponsor / governance | Per review | Da verificare | Read-only | Function established; membership pending |
| Operations Lead | Massimo Mainini | Non nominato | Sponsor | Dal 30/07/2026 fino a revoca | Da verificare | Da eseguire | Bootstrap assignment |
| Service Owner | Massimo Mainini | Non nominato | Sponsor / Operations Lead | Dal 30/07/2026 fino a revoca | Da verificare | Da eseguire | Bootstrap assignment |
| Technical Owner | Massimo Mainini | Non nominato | Service Owner | Dal 30/07/2026 fino a revoca | Da verificare | Da eseguire | Bootstrap assignment |
| Operator | Massimo Mainini | Non nominato | Operations Lead | Dal 30/07/2026 fino a revoca | Da verificare | Da eseguire | Bootstrap assignment — non operational |
| Senior Operator | Massimo Mainini | Non nominato | Operations Lead | Dal 30/07/2026 fino a revoca | Da verificare | Da eseguire | Bootstrap assignment — no independent approval |
| Incident Coordinator | Massimo Mainini | Non nominato | Operations Lead | Dal 30/07/2026 fino a revoca | Da verificare | Da eseguire | Bootstrap assignment |
| Maintainer | Massimo Mainini | Non nominato | Technical Owner | Dal 30/07/2026 fino a revoca | Da verificare | Da eseguire | Bootstrap assignment — no self return-to-service |
| Change Approver | Massimo Mainini | Non nominato | Operations Lead / governance | Dal 30/07/2026 fino a revoca | Da verificare | Da eseguire | Bootstrap assignment — C3/C4 approval prohibited |
| Safety Authority | Massimo Mainini | Non nominato | Project Owner / local safety governance | Dal 30/07/2026 fino a revoca | Da verificare | Indipendenza non soddisfatta | Bootstrap assignment — runtime authority unavailable |
| Security Authority | Massimo Mainini | Non nominato | Project Owner | Dal 30/07/2026 fino a revoca | Da verificare | Da eseguire | Bootstrap assignment — privileged self-approval prohibited |
| Documentation Governor | Massimo Mainini | Non nominato | Chief Architect | Dal 30/07/2026 fino a revoca | Da verificare | N/A | Bootstrap assignment |
| Auditor | Massimo Mainini | Non nominato | Sponsor | Dal 30/07/2026 fino a revoca | Da verificare | Read-only non indipendente | Bootstrap assignment — independent audit unavailable |

## 3. Access matrix baseline

Legenda:

- `R` richiesta consentita entro scope;
- `A` approvazione richiesta;
- `E` esecuzione consentita dopo autorizzazione;
- `D` negato per ruolo;
- `TBD` non assegnabile finché identità, ruolo e policy non sono implementati.

| Ruolo | C1 | C2 | C3 | C4 | Safety permit/deny | Break-glass |
|---|---|---|---|---|---|---|
| Operator | TBD | TBD | R, no self-approval | R, no self-approval | D | D |
| Senior Operator | TBD | TBD | A/E solo con identità distinta | A/E solo con identità distinta | D | R entro policy |
| Operations Lead | TBD | TBD | A solo con requester distinto | A solo con requester distinto | D | A operativo, non security |
| Technical Owner | TBD | TBD | R/E entro scope e approvazione distinta | R/E entro scope e approvazione distinta | D | R tecnico |
| Maintainer | TBD | TBD | R/E entro maintenance window e approvazione distinta | R/E entro maintenance window e approvazione distinta | D | R tecnico |
| Safety Authority | D salvo ruolo separato | D salvo ruolo separato | permit/deny safety | permit/deny/stop | A/R | D |
| Security Authority | D salvo ruolo separato | D salvo ruolo separato | access approval only | access approval only | D | A |
| Auditor | D | D | D | D | D | D |

Poiché tutte le funzioni nominative bootstrap sono assegnate alla stessa identità, nessuna combinazione C3/C4 che richieda approvazione indipendente è eseguibile. La matrice resta non operativa finché policy, identità distinte e controlli non sono implementati e testati tramite C01, C04 e C05.

## 4. Mandatory segregation rules

Le seguenti separazioni sono obbligatorie:

1. requester e approver distinti per C3 e C4;
2. esecutore e secondo approvatore distinti per C4;
3. Maintainer distinto dal return-to-service approver per interventi safety-relevant;
4. Security Authority distinta dal beneficiario del privileged access;
5. Auditor privo di command execution;
6. Safety Authority indipendente dal DSOC per permit, deny, stop e safe state;
7. policy author distinto dal policy approver;
8. chiusura SEV-1 soggetta a four-eyes e verifica del safe state.

La configurazione bootstrap non soddisfa queste separazioni. La mitigazione vigente è il divieto di auto-approvazione, il blocco delle classi C3/C4, l'assenza di privilegi runtime e il mantenimento degli interlock fisici locali indipendenti dall'applicazione.

## 5. Delegation record

| Delegation ID | Delegante | Delegato | Ruolo/scope | Classi comando | Inizio | Scadenza | Approvatore | Revoca | Stato |
|---|---|---|---|---|---|---|---|---|---|
| DEL-C04-BOOT-001 | Massimo Mainini — Sponsor | Massimo Mainini | Ruoli nominativi bootstrap, solo governance e ambiente non operativo | Nessuna autorizzazione C3/C4 runtime | 30/07/2026 | Fino a revoca o nomina di soggetti distinti | Massimo Mainini — Sponsor | Revocabile immediatamente | Active with restrictions |

La registrazione bootstrap non costituisce delega di privilegi reali. Sono vietate deleghe permanenti generiche per Safety Authority, Security Authority e classi C3/C4.

## 6. Conflict register

| Conflict ID | Persona/ruolo | Conflitto | Rischio | Mitigazione | Approvazione | Stato |
|---|---|---|---|---|---|---|
| CR-001 | Massimo Mainini — tutti i ruoli nominativi bootstrap | assenza di sostituti e concentrazione delle responsabilità | High | fase pre-operativa; nominare sostituti e responsabili distinti prima del runtime | Sponsor | Open |
| CR-002 | Massimo Mainini — Maintainer / return-to-service approver | self-certification | High | return-to-service vietato finché non è nominato un approvatore distinto | Sponsor; futura Safety Authority indipendente | Open |
| CR-003 | Massimo Mainini — Operator / Senior Operator / Change Approver | bypass four-eyes | Critical | C3/C4 bloccati; auto-approvazione negata; introdurre seconda identità | Sponsor | Open |
| CR-004 | Massimo Mainini — amministratore / Security Authority | privilege self-approval | Critical | privileged access e break-glass operativo vietati; approvatore indipendente richiesto | Sponsor | Open |
| CR-005 | Massimo Mainini — Operations Lead / Safety Authority | Safety Authority non indipendente dal DSOC | Critical | nessun permit/deny/stop applicativo considerato valido per runtime; nominare Safety Authority indipendente | Sponsor | Open |
| CR-006 | Massimo Mainini — ruoli operativi / Auditor | audit non indipendente | High | audit corrente solo self-assessment; nominare auditor read-only indipendente | Sponsor | Open |

## 7. Four-eyes validation scenarios

La chiusura C04 richiede almeno:

1. richiesta C3 da parte di un Operator e approvazione da identità distinta;
2. rifiuto dell'auto-approvazione;
3. richiesta C4 con due identità distinte e verifica dei conflitti;
4. revoca di uno degli approvatori prima dell'esecuzione;
5. return-to-service approvato da attore diverso dal Maintainer;
6. chiusura SEV-1 con doppia approvazione e verifica Safety Authority;
7. modifica di suppression rule safety-relevant con author e approver distinti;
8. audit trail completo di requester, approver, policy, timestamp e decisione.

Con una sola identità nominata, gli scenari positivi four-eyes non sono eseguibili. Possono essere preparati o simulati con fixture, ma non costituiscono evidenza organizzativa o operativa.

## 8. Closure criteria

C04 può diventare `Passed` solo quando:

- tutti i ruoli critici hanno titolare e sostituto approvati;
- validità, formazione e deleghe sono documentate;
- access review è completata;
- conflict register è approvato e mitigato;
- gli scenari four-eyes sono eseguiti con evidenza;
- nessuna identità può auto-approvare C3/C4 o privileged access;
- Safety Authority e Security Authority restano separate dalle responsabilità incompatibili.

## 9. Decisione corrente

**ARB-012-C04: BLOCKED — bootstrap assignments recorded**

La decisione dello Sponsor ha formalizzato Massimo Mainini come titolare provvisorio di tutti i ruoli nominativi durante la fase bootstrap, con validità dal 30/07/2026 fino a revoca. Non sono nominati sostituti o soggetti indipendenti.

Il registro non abilita ruoli operativi, privilegi, break-glass o command path runtime. C04 resta bloccata fino alla nomina di identità distinte, al completamento di formazione e access review, alla mitigazione dei conflitti e all'esecuzione verificata degli scenari four-eyes. I command path C3/C4 restano proibiti e gli interlock fisici locali rimangono indipendenti e autorevoli.
