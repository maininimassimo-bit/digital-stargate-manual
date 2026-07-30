# ARB-012 Validation Campaign

| Campo | Valore |
|---|---|
| Identificativo | ARB-012-VAL-001 |
| Titolo | Validation Campaign for ARB-012 Conditions C01–C08 |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch | `validation/arb-012-conditions` |
| Data | 30/07/2026 |
| Autorità | Digital StarGate Release and Quality Governor |
| Stato | Active validation campaign — partial simulated evidence available |
| Readiness | Not Ready for runtime enablement |

## 1. Scopo

Questa campagna governa la produzione, verifica e registrazione delle evidenze richieste dalle condizioni `ARB-012-C01…C08`. Distingue in modo esplicito:

- validazione documentale e CI;
- validazione tecnica in ambiente simulato o non operativo;
- validazione organizzativa;
- validazione runtime, security e safety sull'implementazione effettiva.

Una condizione può essere dichiarata `Passed` solo quando tutti i criteri di chiusura applicabili allo scope dichiarato sono soddisfatti con evidenza riproducibile. Una copertura parziale non costituisce chiusura.

## 2. Regole di classificazione

Ogni gate usa esclusivamente uno dei seguenti stati:

- `Passed`: criteri soddisfatti con evidenza verificata;
- `Failed`: prova eseguita con esito negativo;
- `Not Executed`: prova definita ma non ancora eseguita;
- `Blocked`: prova non eseguibile per dipendenza, ambiente, ruolo o capability assente;
- `Not Applicable`: gate non pertinente, con motivazione approvata.

Quando alcuni scenari sono stati eseguiti ma il gate non è chiuso, lo stato rimane `Not Executed` e la copertura viene registrata come evidenza parziale.

## 3. Quality-gate matrix

| Condizione | Ambito | Stato corrente | Gate di chiusura | Evidenza minima |
|---|---|---|---|---|
| ARB-012-C01 | Command Authorization Validation | Not Executed — partial simulated coverage | policy, ruoli, freshness, safety denial, expiry, idempotency e audit completo verificati | report scenario completo, log correlati e decision record |
| ARB-012-C02 | Alarm and Incident Validation | Not Executed | lifecycle, correlation, suppression, escalation, acknowledgement e closure verificati | scenario report con timeline, alarm/incident records e audit trail |
| ARB-012-C03 | Runbook Drill and Recovery | Not Executed | precondizioni, checkpoint, stop condition, rollback, recovery ed evidence collection verificati | drill report con esito, tempi, deviazioni e rollback evidence |
| ARB-012-C04 | Role Assignment and Four-Eyes Enforcement | Blocked | ruoli nominativi, deleghe, conflitti, approver distinti e access review attivi | role assignment register, delegation records e prova four-eyes |
| ARB-012-C05 | Security and Break-Glass Validation | Not Executed — partial simulated coverage | least privilege, privileged access, break-glass, notifica, revoca e post-review verificati | access logs, approval record, notification, revocation evidence e post-review |
| ARB-012-C06 | Degraded Mode and Dependency Failure | Not Executed | failure di telemetry, notification, audit sink, correlation e identity gestiti senza bypass safety | fault-injection report e degraded-mode evidence |
| ARB-012-C07 | Audit, Retention and Time Integrity | Not Executed | append-only trail, timestamp, correlation, payload hash, retention e time integrity verificati | audit integrity report, retention configuration e clock evidence |
| ARB-012-C08 | Publication and CI Validation | Passed | restore, build, test, format e `mkdocs build --strict` completati sul final head verificato | GitHub Actions run, job, commit SHA e documento evidence |

## 4. Dipendenze e sequenziamento

### 4.1 Simulazione tecnica C01/C05

La preparazione e l'esecuzione tecnica in ambiente simulato possono usare identità, ruoli, policy e autorità come fixture non operative. Per tale scope C04 non è un prerequisito bloccante, purché:

- le identità siano chiaramente marcate come simulate;
- nessuna fixture costituisca nomina organizzativa;
- nessun adapter sia collegato a hardware o runtime operativo;
- il risultato non venga interpretato come readiness operativa.

### 4.2 Chiusura organizzativa e operativa

C04 resta prerequisito obbligatorio per:

- assegnazione di ruoli e privilegi reali;
- validazione four-eyes con soggetti nominati;
- abilitazione di command path C3/C4;
- qualunque chiusura operativa o runtime di C01 e C05.

## 5. Validation scenarios

Restano autorevoli gli scenari definiti nei documenti di test e nelle sezioni originarie della campagna. Per C01 e C05 l'esecuzione corrente copre solo un sottoinsieme simulato; gli scenari mancanti e gli artefatti non prodotti devono essere completati prima del passaggio a `Passed`.

## 6. Evidence register

| Evidence ID | Condizione | Descrizione | Stato | Riferimento |
|---|---|---|---|---|
| E-ARB012-C01-01 | C01 | Command authorization simulated execution | Partial | `ARB-012-C01-C05-Execution-Evidence.md` |
| E-ARB012-C02-01 | C02 | Alarm and incident scenario report | Missing | da produrre |
| E-ARB012-C03-01 | C03 | Runbook drill and recovery report | Missing | da produrre |
| E-ARB012-C04-01 | C04 | Role assignment and four-eyes evidence | Blocked | `ARB-012-C04-Role-Assignment-Register.md`; issue #11 |
| E-ARB012-C05-01 | C05 | Security and break-glass simulated execution | Partial | `ARB-012-C01-C05-Execution-Evidence.md` |
| E-ARB012-C06-01 | C06 | Degraded-mode fault-injection report | Missing | da produrre |
| E-ARB012-C07-01 | C07 | Audit, retention and time-integrity report | Missing | da produrre |
| E-ARB012-C08-01 | C08 | CI and publication run | Passed | `ARB-012-C08-CI-Publication-Evidence.md`; run #172; commit `21d68b1caa40f1de84705cb8ec30b148053aef83` |

## 7. Risk and waiver register

| ID | Rischio | Severità | Trattamento | Waiver |
|---|---|---|---|---|
| R-ARB012-01 | command path abilitato prima della chiusura applicabile di C01 | Critical | mantenere runtime disabilitato | non ammesso |
| R-ARB012-02 | safety state dedotto da telemetry assente o incoerente | Critical | fail-safe e blocco azioni dipendenti | non ammesso |
| R-ARB012-03 | ruoli critici non nominati | High | completare C04 prima dell'operatività | non ammesso per C3/C4 |
| R-ARB012-04 | break-glass persistente o non auditato | Critical | scope minimo, expiry, notifica e post-review | non ammesso |
| R-ARB012-05 | audit trail incompleto | High | chiudere C07 prima della readiness | solo ambienti non operativi |
| R-ARB012-06 | stato documentale incoerente | High | mantenere matrice, evidence register e PR sincronizzati | non ammesso |

## 8. Ordine di esecuzione aggiornato

1. mantenere C08 verificato sul final head;
2. completare C04 tramite nomine, deleghe, conflict register e access review;
3. completare gli scenari e gli artefatti mancanti di C01 e C05;
4. validare C07;
5. validare C02;
6. eseguire C03;
7. validare C06;
8. eseguire re-review finale C01–C08.

C01–C07 devono essere eseguite inizialmente in ambiente simulato o non operativo. Nessuna prova può disabilitare interlock locali o mettere a rischio persone, cupola, montatura o altri asset fisici.

## 9. Readiness recommendation

**NOT READY FOR RUNTIME ENABLEMENT**

C08 è chiusa per il commit verificato. C01 e C05 dispongono di evidenza tecnica parziale in scope simulato ma restano `Not Executed` come gate complessivi. C02, C03, C06 e C07 non sono eseguite; C04 è bloccata. Rimane vietata l'attivazione di command path operativi fino alla chiusura verificata delle condizioni applicabili e alla decisione finale di re-review.
