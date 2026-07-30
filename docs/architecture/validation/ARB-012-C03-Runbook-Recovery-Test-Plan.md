# ARB-012-C03 — Runbook Drill and Recovery Test Plan

| Campo | Valore |
|---|---|
| Identificativo | ARB-012-C03-TEST-001 |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Condizione | ARB-012-C03 — Runbook Drill and Recovery |
| Baseline | OPSC-RUN-001 — Operational Runbook Standard |
| Ambiente | Simulato, non operativo, privo di adattatori hardware |
| Stato | Prepared — CI evidence pending |
| Data | 30/07/2026 |
| Autorità | Digital StarGate Release and Quality Governor |

## 1. Obiettivo

Validare in ambiente simulato che il modello di esecuzione runbook rispetti precondizioni, safety checkpoint, stop condition, timeout, riconciliazione, rollback, recovery ordinata, handover ed evidence collection.

La prova non costituisce un drill operativo, non abilita comandi runtime e non sostituisce verifiche fisiche o interlock locali.

## 2. Scope incluso

- arresto quando una precondizione non è verificabile;
- abort prima dell'azione quando il safety checkpoint fallisce;
- timeout trattato come outcome incerto;
- blocco del retry fino alla riconciliazione;
- rollback verso restore point dichiarato;
- verifica congiunta di servizio e stato safety dopo rollback;
- recovery ordinata: containment, diagnosis, technical restore, service verification, safety verification, monitoring, handover e closure with evidence;
- divieto di saltare fasi obbligatorie;
- presenza di execution ID, correlation ID, runbook ID, versione e timestamp nell'evidence record.

## 3. Scope escluso

- cupola, montatura, ASCOM, Alpaca, N.I.N.A. o dispositivi fisici;
- comandi C2-C4 reali;
- soglie temporali operative;
- routing, reperibilità e comunicazioni reali;
- verifica di backup o restore point effettivi;
- four-eyes organizzativo con identità nominate;
- return-to-service operativo.

## 4. Scenari

| ID | Scenario | Esito atteso |
|---|---|---|
| C03-S01 | Precondizione unknown | esecuzione fermata ed evidence prodotta |
| C03-S02 | Safety checkpoint failed | abort prima del dispatch |
| C03-S03 | Timeout durante step | stato reconciliation required e retry bloccato |
| C03-S04 | Rollback con safety non verificata | rollback non completabile |
| C03-S05 | Rollback con servizio e safety validi | stato recovered |
| C03-S06 | Recovery completa in ordine | chiusura con evidence |
| C03-S07 | Recovery con fase saltata | avanzamento negato |
| C03-S08 | Evidence minima correlata | identificativi e timestamp presenti |

## 5. Test harness

`tests/DigitalStarGate.UnitTests/OperationsCenter/RunbookRecoveryValidationTests.cs`

Il test harness usa esclusivamente fixture in memoria. Non contiene adapter, endpoint, credenziali, secret o integrazioni operative.

## 6. Gate di accettazione simulato

La validazione tecnica simulata può essere classificata `Passed` solo se il final head supera:

- restore;
- build;
- test;
- formatting;
- MkDocs strict verification.

Il risultato non chiude lo scope operativo di C03. Lo scope operativo rimane bloccato fino a disponibilità di ambiente autorizzato, ruoli segregati, runbook approvati, restore point reali, drill controllato ed evidenza ARB.

## 7. Safety disposition

- local physical interlocks restano indipendenti e autorevoli;
- nessun timeout implica successo;
- uno stato unknown, stale o conflicting non può essere interpretato come sicuro;
- nessun test può rimuovere maintenance lock o uscire da safe state;
- runtime enablement resta proibito.

## 8. Stato iniziale

`ARB-012-C03: NOT EXECUTED — implementation prepared, CI evidence pending`
