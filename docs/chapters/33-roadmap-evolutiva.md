# Capitolo 33 – Roadmap Evolutiva dell’Osservatorio

**Codice documento:** DSG-TM-001-33  
**Revisione:** 0.4 Draft

## 33.1 Scopo

Definire un processo controllato per pianificare evoluzioni hardware, software e operative senza compromettere la stabilità dell’osservatorio.

## 33.2 Principi

Ogni evoluzione deve:

- rispondere a un’esigenza documentata;
- essere compatibile con l’architettura esistente;
- prevedere test e rollback;
- avere un owner;
- aggiornare inventario e manuale.

## 33.3 Aree di evoluzione

- sensoristica meteo ridondata;
- automazione cupola più resiliente;
- UPS e telecontrollo alimentazioni;
- segmentazione rete e VPN moderna;
- monitoraggio centralizzato;
- storage e backup automatici;
- miglioramento pipeline di acquisizione;
- nuove ottiche o camere;
- visualizzazione dinamica del cielo osservato;
- integrazione progressiva dei dati operativi in tempo reale.

## 33.4 Processo di approvazione

### DSG-PROC-033-01

1. Aprire una Change Request.
2. Descrivere benefici e rischi.
3. Valutare dipendenze e costi.
4. Predisporre piano di test.
5. Eseguire installazione controllata.
6. Validare con sessione pilota.
7. Aggiornare documentazione.
8. Chiudere la modifica.

## 33.5 Roadmap suggerita

| Orizzonte | Iniziativa | Priorità | Stato |
|---|---|---|---|
| Breve termine | Immagine dinamica dell’ultima osservazione con Aladin Lite | Alta | Completata |
| Breve termine | Contratto dati `latest-observation.json` | Alta | Completata |
| Breve termine | Aggiornamento automatico dell’ultima osservazione dalla pipeline Analytics | Alta | Completata |
| Breve termine | Validazione sensori e procedure safe | Alta | Pianificata |
| Breve termine | Capability 002 – Weather Safety Interlock in shadow mode | Alta | Proposta |
| Breve termine | Backup configurazioni automatizzato | Alta | Pianificata |
| Medio termine | Blocco apertura e chiusura automatica tramite Weather Safety Interlock | Alta | Dipendente dalla validazione sensori |
| Medio termine | Miglioramento parsing automatico RA/DEC da N.I.N.A. e plate solving | Alta | Pianificata |
| Medio termine | Monitoraggio centralizzato KPI | Media | Da valutare |
| Medio termine | Ridondanza alimentazione e rete | Alta | Da valutare |
| Medio termine | Operations Center e Live Observatory | Alta | In standby |
| Lungo termine | Evoluzione ottica e camere | Media | Da valutare |

## 33.6 Sequenza Weather Safety Interlock

1. Validare inventario, protocolli, qualità e frequenza dei sensori realmente installati.
2. Definire contratti applicativi e simulatori senza comandare la cupola.
3. Eseguire la capability in shadow mode e confrontare le decisioni con l’operatore.
4. Abilitare il blocco apertura dopo la validazione dell’assenza di falsi `SAFE`.
5. Abilitare la chiusura automatica solo dopo test di idempotenza, conferma `CLOSED` e rollback.
6. Valutare la riapertura automatica come decisione separata dopo evidenze operative sufficienti.

Riferimenti:

- [ADR-005 – Weather Safety Interlock fail-safe](../architecture/ADR-005-Weather-Safety-Interlock.md)
- [Capability 002 – Weather Safety Interlock](../developer/capability-002-weather-safety-interlock.md)
- [Monitoraggio meteo e sicurezza ambientale](26-monitoraggio-meteo-sicurezza-ambientale.md)

## 33.7 Live Observatory

La futura componente **Live Observatory** estenderà il portale con una vista operativa in tempo reale dell’osservatorio remoto.

Sono previsti:

- puntamento corrente del telescopio;
- target attivo e centro dell’inquadratura;
- stato della montatura e del tracking;
- stato della cupola;
- stato del Safety Monitor;
- condizioni CloudWatcher e dati meteorologici;
- immagine AllSky aggiornata;
- stato della sequenza N.I.N.A.;
- RMS di guida, HFR e FWHM;
- avanzamento delle esposizioni;
- cronologia degli eventi operativi.

La componente **Live Observatory è attualmente in standby**. Rimane confermata nella roadmap e sarà ripresa dopo il consolidamento della pubblicazione web, del contratto dati e dell’EAGLE Agent.

## 33.8 Criteri di successo

- riduzione incidenti;
- aumento sessioni completate;
- riduzione MTTR;
- maggiore autonomia;
- mantenibilità documentata;
- disponibilità di una vista coerente e aggiornata sullo stato dell’osservatorio.
