# SAF-CAT-001 — Safety Hazard and State Catalog

| Campo | Valore |
|---|---|
| Identificativo | SAF-CAT-001 |
| Package | AP-010 |
| Stato | Initial candidate catalog |
| Data | 30/07/2026 |

## 1. Purpose

Catalogo iniziale di hazard, safe state e safety contract candidate. Le classificazioni sono preliminari e richiedono owner, misure ed evidence.

## 2. Risk scale

Severity candidate: `S1 minor`, `S2 moderate`, `S3 major`, `S4 critical`.
Likelihood candidate: `L1 rare`, `L2 unlikely`, `L3 possible`, `L4 likely`.

L'uso della matrice non costituisce certificazione; criteri e soglie devono essere deliberati.

## 3. Initial hazard register

| ID | Hazard | Cause candidate | Consequence | Controls candidate | Status |
|---|---|---|---|---|---|
| HAZ-001 | cupola aperta con pioggia | sensore/automazione/ritardo | danno a ottica ed elettronica | rain interlock, local close, freshness | Candidate |
| HAZ-002 | cupola aperta con vento eccessivo | soglia o sensore inadeguato | danno meccanico | wind policy, inhibitor, close path | Candidate |
| HAZ-003 | collisione montatura-cupola | posizione o sequenza errata | danno meccanico | envelope, park/close sequence, feedback | Candidate |
| HAZ-004 | chiusura non confermata | actuator, sensore o power fault | falsa protezione | independent confirmation, timeout, recovery hold | Candidate |
| HAZ-005 | apertura con meteo stale/unknown | perdita telemetry | esposizione a condizioni unsafe | unknown blocks opening | Candidate |
| HAZ-006 | comando remoto non autorizzato | identity/authorization failure | movimento o esposizione indebita | AP-005, safety veto, audit | Candidate |
| HAZ-007 | perdita WAN durante sessione | provider/router fault | perdita supervisione remota | local autonomy, safe policy | Candidate |
| HAZ-008 | perdita alimentazione | rete elettrica/UPS | movimento incompleto, corruzione dati | UPS, controlled transition, local interlock | Candidate |
| HAZ-009 | riavvio automatico dopo emergenza | state loss o restart policy | ripartenza non sicura | recovery hold, explicit authorization | Candidate |
| HAZ-010 | override manuale persistente | governance insufficiente | protezioni disabilitate | scoped override, expiry, audit | Candidate |
| HAZ-011 | sensori discordanti | guasto/calibrazione | decisione errata | conflict detection, conservative policy | Candidate |
| HAZ-012 | clock non sincronizzato | NTP failure | freshness e sequence errate | clock health, inhibit critical actions | Candidate |

## 4. Safe states

| State | Definition | Entry evidence | Exit rule |
|---|---|---|---|
| SAFE_PROTECTED | osservatorio protetto e stato confermato | closure/protection feedback | autorizzazione e condizioni valide |
| SAFE_MAINTENANCE | energia e movimento sotto procedura manutentiva | maintenance authorization | checklist e recovery hold |
| EMERGENCY_TRANSITION | azione prioritaria verso protezione | hazard trigger | protection confirmation o recovery hold |
| RECOVERY_HOLD | operatività sospesa dopo anomalia/intervento | incident/change record | review e autorizzazione esplicita |
| NORMAL_AUTHORIZED | attività consentita entro limiti | valid conditions and authority | unsafe trigger o stop |
| UNKNOWN | stato non determinabile | missing/stale/conflicting evidence | conferma locale affidabile |

## 5. Safety contract candidates

| ID | Command | Hazards | Required outcome | Status |
|---|---|---|---|---|
| SAF-CON-001 | `DSG.Dome.Command.RequestOpen` | HAZ-001/002/005/006 | open confirmed only under valid conditions | Candidate |
| SAF-CON-002 | `DSG.Dome.Command.RequestClose` | HAZ-003/004/008 | protected state confirmed | Candidate |
| SAF-CON-003 | `DSG.Observatory.Command.AbortSession` | HAZ-001/002/007/008 | acquisition stopped and protection workflow started | Candidate |
| SAF-CON-004 | mount park request | HAZ-003 | park position confirmed | Candidate |
| SAF-CON-005 | manual override request | HAZ-006/010 | scoped, approved, expiring override | Candidate |
| SAF-CON-006 | recovery release | HAZ-009 | transition from hold explicitly authorized | Candidate |

## 6. Evidence register template

| Evidence ID | Hazard/control | Method | Date | Owner | Result | Limitations |
|---|---|---|---|---|---|---|
| TBD | TBD | test/inspection/simulation | TBD | TBD | Not executed | TBD |

## 7. Governance

- Nuovi hazard non vengono cancellati: sono chiusi, accettati, trasferiti o superseded con motivazione.
- Il residual risk richiede owner e approvatore.
- Cambiamenti a sensori, soglie, controller, rete o power attivano impact assessment.
- Incident e near miss possono riaprire hazard chiusi.
- Il catalogo non autorizza runtime finché controlli ed evidence non sono approvati.