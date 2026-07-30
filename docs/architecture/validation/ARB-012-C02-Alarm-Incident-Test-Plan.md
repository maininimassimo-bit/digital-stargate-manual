# ARB-012-C02 — Alarm and Incident Validation Plan

| Campo | Valore |
|---|---|
| Identificativo | ARB-012-VAL-C02 |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Condizione | ARB-012-C02 — Alarm and Incident Validation |
| Modello autorevole | OPSC-ALM-001 |
| Ambiente | Simulato, non operativo, privo di adattatori hardware |
| Data | 30/07/2026 |
| Stato | Implementation prepared — CI evidence pending |
| Runtime enablement | Prohibited |

## 1. Scopo

Validare in ambiente simulato il lifecycle di alarm e incident, la correlazione, la suppression, l'escalation, l'acknowledgement, la recovery validation e la post-incident review senza collegamenti a cupola, montatura, ASCOM, Alpaca, N.I.N.A. o altri asset operativi.

La prova non autorizza soglie runtime, automazioni, routing reale, comandi, safe-state declaration o integrazioni con sistemi fisici.

## 2. Scenari implementati

| ID | Scenario | Risultato atteso |
|---|---|---|
| C02-S01 | acknowledgement di un alarm | l'alarm passa ad Acknowledged ma non viene chiuso |
| C02-S02 | suppression di alarm safety-relevant | suppression negata e timeline auditata |
| C02-S03 | suppression temporanea scaduta | ritorno automatico a Open con reason code |
| C02-S04 | correlazione di alarm sullo stesso service/CI | gruppo correlato creato senza perdita dei record originari |
| C02-S05 | alarm SEV-1 o safety-relevant | Major Incident con escalation a Safety Authority e Incident Commander |
| C02-S06 | chiusura senza recovery validation | chiusura negata |
| C02-S07 | chiusura dopo recovery e safe-state verification | chiusura consentita |
| C02-S08 | incident chiuso senza post-incident review | completion negata finché la review non è registrata |

## 3. Vincoli di sicurezza

- nessun adapter operativo è presente;
- nessuna soglia numerica viene introdotta;
- gli stati `unknown`, `stale` e `conflicting` non sono trattati come normali o sicuri;
- una suppression non può nascondere condizioni safety-relevant;
- acknowledgement non equivale a resolution;
- cessazione del segnale non equivale a closure;
- la Safety Authority locale e gli interlock fisici restano indipendenti e prevalenti.

## 4. Evidence richiesta

La chiusura dello scope simulato richiede:

- commit finale verificato;
- workflow Developer Foundation completato con successo;
- restore, build, test, formatting e MkDocs passed;
- test report riferibile agli scenari C02;
- conferma che non siano presenti integrazioni hardware o runtime;
- aggiornamento della Validation Campaign.

## 5. Limiti residui

Restano fuori dallo scope simulato corrente:

- routing reale e reperibilità;
- tempi SLA/SLO di acknowledgement ed escalation;
- integrazione ITSM/HMI;
- notification fallback reale;
- retention audit;
- catalogo completo delle correlation rule;
- ownership nominativa e four-eyes organizzativo;
- drill operativo con personale e sistemi reali.

## 6. Disposizione corrente

**ARB-012-C02: NOT EXECUTED — implementation prepared, CI evidence pending**

Anche in caso di CI positiva, l'esito potrà essere classificato esclusivamente come `Passed — simulated technical validation`. La validazione operativa resterà bloccata da C04, dai drill mancanti e dall'assenza di integrazioni runtime autorizzate.
