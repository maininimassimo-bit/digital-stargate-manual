# Capitolo 33 – Roadmap Evolutiva dell’Osservatorio

**Codice documento:** DSG-TM-001-33  
**Revisione:** 0.2 Draft

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
| Breve termine | Immagine dinamica dell’ultima osservazione con Aladin Lite | Alta | In implementazione |
| Breve termine | Contratto dati `latest-observation.json` | Alta | Completata |
| Breve termine | Validazione sensori e procedure safe | Alta | Pianificata |
| Breve termine | Backup configurazioni automatizzato | Alta | Pianificata |
| Medio termine | Parsing automatico RA/DEC da N.I.N.A. e plate solving | Alta | Pianificata |
| Medio termine | Monitoraggio centralizzato KPI | Media | Da valutare |
| Medio termine | Ridondanza alimentazione e rete | Alta | Da valutare |
| Medio termine | Operations Center e Live Observatory | Alta | In roadmap |
| Lungo termine | Evoluzione ottica e camere | Media | Da valutare |

## 33.6 Live Observatory

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

Questa evoluzione sarà sviluppata dopo il consolidamento del contratto dati e dell’EAGLE Agent.

## 33.7 Criteri di successo

- riduzione incidenti;
- aumento sessioni completate;
- riduzione MTTR;
- maggiore autonomia;
- mantenibilità documentata;
- disponibilità di una vista coerente e aggiornata sullo stato dell’osservatorio.
