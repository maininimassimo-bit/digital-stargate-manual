# Capitolo 25 – Chiusura controllata dell'osservatorio

**Codice documento:** DSG-TM-001-25  
**Revisione:** 0.1 Draft

## 25.1 Scopo

Il presente capitolo definisce la procedura standard per terminare una sessione osservativa, mettere in sicurezza la strumentazione e chiudere la copertura mobile dell'Osservatorio Remoto Digital StarGate.

La chiusura controllata deve lasciare l'impianto in uno stato noto, verificabile e riproducibile, riducendo il rischio di collisioni, infiltrazioni, perdita di dati o riavvii non governati.

## 25.2 Campo di applicazione

La procedura si applica a:

- termine ordinario di una sequenza N.I.N.A.;
- chiusura anticipata richiesta dall'operatore;
- chiusura per peggioramento delle condizioni ambientali;
- arresto dopo un recovery parziale;
- messa fuori servizio per manutenzione.

Le emergenze con rischio immediato sono gestite dal Capitolo 18.

## 25.3 Condizioni preliminari

Prima di comandare la chiusura devono essere verificate almeno le seguenti condizioni:

| Controllo | Stato richiesto |
|---|---|
| Esposizione | terminata o interrotta in modo controllato |
| Guida PHD2 | arrestata |
| Montatura | in Park verificato |
| Tracking | disattivato |
| Treno ottico | entro l'inviluppo sicuro |
| Cavi | liberi da trazione e interferenze |
| Sensore OPEN | coerente con copertura aperta |
| Sensore SAFE | TRUE, se previsto dalla logica di impianto |
| Percorso di chiusura | libero |

> **ATTENZIONE:** la chiusura non deve essere avviata se la posizione della montatura è sconosciuta o se i sensori della copertura risultano incoerenti.

## 25.4 Stati di chiusura

| Stato | Descrizione |
|---|---|
| PRE-CLOSE | verifica dei prerequisiti |
| PARKING | montatura in movimento verso Park |
| READY-TO-CLOSE | montatura sicura e sensori coerenti |
| CLOSING | copertura in movimento |
| CLOSED | finecorsa CLOSED attivo |
| SECURED | servizi, dati e alimentazioni verificati |
| CLOSE-FAULT | anomalia rilevata durante la procedura |

## 25.5 Procedura DSG-PROC-025-01 – Chiusura ordinaria

1. Terminare la sequenza N.I.N.A. senza avviare nuove esposizioni.
2. Arrestare la guida in PHD2.
3. Salvare le immagini ancora in memoria e verificare la chiusura dei file FITS.
4. Comandare il Park tramite N.I.N.A. o CPWI.
5. Verificare in CPWI il raggiungimento della posizione di Park.
6. Confermare che il tracking sia disattivato.
7. Verificare la coerenza dei sensori OPEN, CLOSED e SAFE.
8. Comandare la chiusura della copertura.
9. Monitorare il movimento fino all'attivazione del finecorsa CLOSED.
10. Verificare che il motore si arresti correttamente.
11. Controllare che OPEN sia FALSE e CLOSED sia TRUE.
12. Archiviare log e report della sessione.
13. Avviare il warm-up controllato delle camere raffreddate.
14. Disconnettere i dispositivi dai software nell'ordine previsto.
15. Applicare la politica di spegnimento o standby dell'EAGLE.
16. Registrare l'esito nel Registro Operativo.

## 25.6 Procedura DSG-PROC-025-02 – Chiusura anticipata

La chiusura anticipata può essere richiesta per nuvolosità persistente, vento, problemi di guida, errore software o decisione dell'operatore.

1. Mettere in pausa la sequenza.
2. Terminare o annullare l'esposizione in corso.
3. Arrestare la guida.
4. Eseguire Park.
5. Verificare l'inviluppo di sicurezza.
6. Chiudere la copertura.
7. Salvare log, motivazione e timestamp dell'interruzione.
8. Classificare l'evento come operativo o incidentale.

## 25.7 Gestione di un errore di Park

Se il Park non viene completato:

1. non comandare la chiusura;
2. verificare alimentazione e connessione della CGX-L;
3. controllare CPWI e il driver ASCOM;
4. verificare visivamente la posizione tramite telecamera disponibile;
5. tentare un solo recovery controllato;
6. se lo stato resta incerto, passare a SAFE MODE e richiedere intervento locale.

## 25.8 Gestione di un errore di chiusura

| Sintomo | Azione iniziale |
|---|---|
| motore non parte | verificare alimentazione, centralina e interlock |
| movimento interrotto | interrompere i comandi, verificare ostacoli e protezioni |
| CLOSED non si attiva | non considerare la struttura sicura; verificare finecorsa |
| OPEN resta attivo | verificare sensore o posizione meccanica |
| rumore anomalo | arresto immediato e ispezione locale |

## 25.9 Criteri di accettazione

La chiusura è completata solo quando:

- la montatura è Parked;
- la copertura è fisicamente chiusa;
- CLOSED è TRUE;
- OPEN è FALSE;
- non sono presenti allarmi;
- i dati della sessione sono salvati;
- le camere sono in fase di warm-up o spente correttamente;
- l'evento è registrato.

## 25.10 Checklist di fine sessione

- [ ] esposizioni terminate;
- [ ] PHD2 arrestato;
- [ ] montatura in Park;
- [ ] tracking disattivato;
- [ ] percorso della copertura libero;
- [ ] copertura chiusa;
- [ ] CLOSED attivo;
- [ ] OPEN disattivo;
- [ ] dati e log salvati;
- [ ] camere riportate a temperatura sicura;
- [ ] report di sessione generato;
- [ ] anomalia eventualmente registrata.

## 25.11 KPI

| KPI | Descrizione |
|---|---|
| tempo medio di chiusura | da fine sequenza a stato SECURED |
| chiusure completate al primo tentativo | percentuale mensile |
| errori di Park | numero per trimestre |
| errori sensori copertura | numero e durata |
| interventi locali per chiusura | numero annuale |

## 25.12 Dati da validare

> **DA VALIDARE:** posizione geometrica esatta di Park compatibile con la chiusura.

> **DA VALIDARE:** timeout massimo ammesso per il movimento della copertura.

> **DA VALIDARE:** comportamento previsto dell'alimentazione EAGLE dopo la chiusura.
