# ARB-012-C04 — Role Assignment and Four-Eyes Register

| Campo | Valore |
|---|---|
| Evidence ID | E-ARB012-C04-01 |
| Condizione | ARB-012-C04 — Role Assignment and Four-Eyes Enforcement |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Data | 22/08/2026 |
| Autorità di nomina | Massimo Mainini — Project Owner / Architecture Sponsor |
| Configurazione | **Two-Person Limited Operations Model** |
| Stato | Target model approved; attributable validation evidence pending |
| Gate status | Blocked pending applicable evidence |

## 1. Modello target

Il modello target usa esclusivamente due persone naturali. Massimo Mainini detiene le responsabilità operative/tecniche e Leonardo Di Egidio le responsabilità approvative, safety e security entro lo scope supportato.

L'assenza di una terza persona non è più un blocker organizzativo. Le capability che richiederebbero una terza identità non vengono simulate o indebolite: sono negate o classificate N/A.

## 2. Registro ruoli

| Ruolo | Titolare | Sostituto | Stato target |
|---|---|---|---|
| Project Owner / Architecture Sponsor | Massimo Mainini | Nessuno | Established |
| Chief Architect / Technical Owner | Massimo Mainini | Nessuno | Established |
| Operations Lead / Service Owner | Massimo Mainini | Nessuno | Established |
| Operator / Requester | Massimo Mainini | Nessuno | C0–C3 entro autorizzazione separata; no self-approval |
| Incident Coordinator | Massimo Mainini | Nessuno | Established |
| Maintainer | Massimo Mainini | Nessuno | Non può approvare il proprio return-to-service |
| C3 Approver | Leonardo Di Egidio | Nessuno | Approver distinto per richieste Massimo |
| Return-to-Service Approver | Leonardo Di Egidio | Nessuno | Distinto dal Maintainer |
| Safety Authority | Leonardo Di Egidio | Nessuno | Permit/deny/stop governance; interlock locali autorevoli |
| Security Authority | Leonardo Di Egidio | Nessuno | Può governare accesso Massimo; self-access approval negata |
| C4 Second Approver | N/A | N/A | Positive C4 denied by governance design |
| Independent internal Auditor | N/A | N/A | Independent audit closure not claimed |

L'assenza di sostituti implica **degraded availability**: se una delle due persone non è disponibile, le operazioni che richiedono entrambe restano sospese. Non è ammessa cross-substitution incompatibile.

## 3. Access matrix target

Legenda: `R` request, `A` approve, `E` execute, `D` denied, `N/A` fuori dal modello.

| Identità / ruolo | C1 | C2 | C3 | C4 | Safety | Break-glass |
|---|---|---|---|---|---|---|
| Massimo — Operator/Requester | R/E secondo policy | R/E secondo policy | R/E solo dopo approvazione Leonardo | D | D | D |
| Massimo — Maintainer | R/E secondo maintenance policy | R/E secondo maintenance policy | R/E solo dopo approvazione distinta | D | D | D |
| Leonardo — C3 Approver | D | D | A per richieste Massimo | D | D | D |
| Leonardo — Return-to-Service | D | D | A limitata al return-to-service | D | verifica safety | D |
| Leonardo — Safety Authority | D | D | permit/deny/stop | D | A/R | D |
| Leonardo — Security Authority | access governance only | access governance only | access governance only | D | D | D |

## 4. Mandatory segregation rules

1. Massimo non può approvare una propria richiesta C3.
2. Leonardo non può essere requester e approver della stessa azione.
3. Massimo Maintainer non può approvare il proprio return-to-service.
4. Leonardo Security Authority non può approvare il proprio accesso.
5. Positive C4 è sempre negato nel modello a due persone.
6. Break-glass è sempre negato.
7. Nessuna cross-substitution può aggirare la separazione.
8. Gli interlock fisici locali non possono essere bypassati e restano autorevoli.
9. L'assenza di independent internal audit non può essere rappresentata come audit indipendente completato.

## 5. Conflict register

| Conflict ID | Conflitto | Mitigazione target | Stato |
|---|---|---|---|
| CR-001 | concentrazione operativa/tecnica in Massimo | C3 e return-to-service richiedono Leonardo; self-approval negata | Accepted with controls |
| CR-002 | impossibilità di una catena C4 a tre attori | positive C4 permanentemente negato | Resolved by prohibition |
| CR-003 | Leonardo concentra approval/safety/security | self-access e self-audit negati; independent audit closure fuori scope | Accepted with scope limitation |
| CR-004 | nessun sostituto | capability two-person sospese in assenza di uno dei titolari | Accepted degraded availability |
| CR-005 | evidence IDV/TRN/access/revocation non completa | completare W03 prima di validazione positiva | Open evidence blocker |

## 6. Four-eyes scenarios target

| Scenario | Attori | Target |
|---|---|---|
| C3 request and approval | Massimo -> Leonardo | Required positive validation |
| Self-approval rejection | Massimo / policy | Required denial validation |
| Approver conflict rejection | Leonardo / policy | Required denial validation |
| Approver/operator revocation | Massimo + Leonardo secondo ruolo | Required validation senza terza persona; conflitti devono produrre deny/suspend |
| Return-to-service | Massimo Maintainer -> Leonardo approver | Required positive validation |
| Safety decision | Massimo Operations -> Leonardo Safety | Required validation |
| Security self-access | Leonardo | Required denial validation |
| C4 positive path | Massimo + Leonardo | Required **denial** validation |
| Break-glass | entrambi | Required **denial** validation |
| Independent internal audit | N/A | Not claimed; repository traceability remains required |

## 7. Closure criteria

C04 può diventare `Passed` nel modello a due persone quando:

- identity/account separation è verificata;
- training e least-privilege review applicabili sono documentati;
- due account non-production distinti sono disponibili per validation;
- revocation e conflict denial sono verificati;
- gli ENV controls applicabili passano;
- i FE scenarios applicabili al modello a due persone sono eseguiti con audit trail completo;
- C4 e break-glass risultano tecnicamente/proceduralmente negati;
- repository CI è verde;
- l'ARB re-review conferma coerenza del **Two-Person Limited Operations Model**.

Non sono exit criteria: terza persona, sostituti indipendenti, positive C4, independent internal audit closure.

## 8. Decisione corrente

**ARB-012-C04: BLOCKED ONLY FOR APPLICABLE TWO-PERSON EVIDENCE.**

Il modello organizzativo target è approvato. Il blocker residuo è evidence-based, non staffing-based. Nessuna autorizzazione runtime è implicata.