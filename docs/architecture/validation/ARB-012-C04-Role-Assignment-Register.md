# ARB-012-C04 — Role Assignment and Four-Eyes Register

| Campo | Valore |
|---|---|
| Evidence ID | E-ARB012-C04-01 |
| Condizione | ARB-012-C04 — Role Assignment and Four-Eyes Enforcement |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Autorità del modello | OPSC-RACI-001 |
| Data | 30/07/2026 |
| Stato | Draft register — assignments incomplete |
| Gate status | Blocked |

## 1. Scopo

Il registro governa le assegnazioni nominative, le sostituzioni, le deleghe, i conflitti di interesse e la separazione delle responsabilità necessarie per rendere operativa la matrice OPSC-RACI-001.

La presenza del registro non abilita privilegi, comandi o ruoli operativi. Ogni assegnazione deve essere approvata, avere validità esplicita ed essere collegata a evidenze di access review e formazione.

## 2. Nominative role register

| Ruolo | Titolare | Sostituto | Autorità di nomina | Validità | Formazione verificata | Access review | Stato |
|---|---|---|---|---|---|---|---|
| Project Owner / Architecture Sponsor | Massimo Mainini | Da nominare | Project governance | Da formalizzare | N/A per gate operativo | N/A | Established sponsor; delegation pending |
| Chief Architect | Da nominare formalmente | Da nominare | Sponsor | Da definire | Da verificare | N/A | Pending |
| Architecture Review Board | Independent ARB function | Da definire | Sponsor / governance | Per review | Da verificare | Read-only | Function established; membership pending |
| Operations Lead | Da nominare | Da nominare | Sponsor | Da definire | Da verificare | Da eseguire | Blocked |
| Service Owner | Da nominare | Da nominare | Sponsor / Operations Lead | Da definire | Da verificare | Da eseguire | Blocked |
| Technical Owner | Da nominare | Da nominare | Service Owner | Da definire | Da verificare | Da eseguire | Blocked |
| Operator | Da nominare | Da nominare | Operations Lead | Da definire | Da verificare | Da eseguire | Blocked |
| Senior Operator | Da nominare | Da nominare | Operations Lead | Da definire | Da verificare | Da eseguire | Blocked |
| Incident Coordinator | Da nominare | Da nominare | Operations Lead | Da definire | Da verificare | Da eseguire | Blocked |
| Maintainer | Da nominare | Da nominare | Technical Owner | Da definire | Da verificare | Da eseguire | Blocked |
| Change Approver | Da nominare | Da nominare | Operations Lead / governance | Da definire | Da verificare | Da eseguire | Blocked |
| Safety Authority | Da nominare formalmente | Da nominare | Project Owner / local safety governance | Da definire | Da verificare | Separata dal DSOC | Blocked |
| Security Authority | Da nominare | Da nominare | Project Owner | Da definire | Da verificare | Da eseguire | Blocked |
| Documentation Governor | Da nominare formalmente | Da nominare | Chief Architect | Da definire | Da verificare | N/A | Pending |
| Auditor | Da nominare | Da nominare | Sponsor | Da definire | Da verificare | Read-only | Blocked |

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
| Senior Operator | TBD | TBD | A/E entro delega | A/E entro delega | D | R entro policy |
| Operations Lead | TBD | TBD | A entro delega | A entro delega | D | A operativo, non security |
| Technical Owner | TBD | TBD | R/E entro scope | R/E entro scope | D | R tecnico |
| Maintainer | TBD | TBD | R/E entro maintenance window | R/E entro maintenance window | D | R tecnico |
| Safety Authority | D salvo ruolo separato | D salvo ruolo separato | permit/deny safety | permit/deny/stop | A/R | D |
| Security Authority | D salvo ruolo separato | D salvo ruolo separato | access approval only | access approval only | D | A |
| Auditor | D | D | D | D | D | D |

La matrice resta non operativa finché policy e identità non sono implementate e testate tramite C01 e C05.

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

## 5. Delegation record template

| Delegation ID | Delegante | Delegato | Ruolo/scope | Classi comando | Inizio | Scadenza | Approvatore | Revoca | Stato |
|---|---|---|---|---|---|---|---|---|---|
| Da assegnare | — | — | — | — | — | — | — | — | Missing |

Sono vietate deleghe permanenti generiche per Safety Authority, Security Authority e classi C3/C4.

## 6. Conflict register

| Conflict ID | Persona/ruolo | Conflitto | Rischio | Mitigazione | Approvazione | Stato |
|---|---|---|---|---|---|---|
| CR-001 | Ruoli operativi non ancora assegnati | impossibile verificare segregazione | High | completare nomine e access review | Sponsor | Open |
| CR-002 | Possibile cumulo Maintainer / return-to-service approver | self-certification | High | nominare approvatore distinto o formalizzare compensating control | Safety Authority / Operations Lead | Open |
| CR-003 | Possibile cumulo Operator / approver C3-C4 | bypass four-eyes | Critical | enforcement tecnico e policy deny | Security Authority / Operations Lead | Open |
| CR-004 | Possibile cumulo amministratore / Security Authority | privilege self-approval | Critical | approvatore indipendente e audit | Sponsor | Open |

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

**ARB-012-C04: BLOCKED**

Il modello e i template sono pronti, ma le assegnazioni nominative, le deleghe, l'access review e le prove four-eyes non sono ancora disponibili. Nessun ruolo operativo o privilegio deve essere considerato attivo sulla base di questo documento.
