# Capitolo 35 — Schemi elettrici e cablaggi

**Codice documento:** DSG-TM-001-35  
**Revisione:** 0.1 Draft  
**Classificazione:** Engineering Documentation

## 35.1 Scopo

Il presente capitolo definisce lo standard di rappresentazione, censimento e manutenzione degli schemi elettrici e dei cablaggi dell'Osservatorio Remoto Digital StarGate.

L'obiettivo è garantire che ogni alimentazione, cavo dati, collegamento di rete e interfaccia di sicurezza sia identificabile, tracciabile e verificabile senza dipendere dalla memoria dell'operatore.

## 35.2 Campo di applicazione

Il capitolo si applica a:

- alimentazione 230 V AC;
- distribuzione 12 V DC;
- alimentatori dedicati;
- EAGLE e relative uscite di potenza;
- montatura CGX-L;
- camere astronomiche;
- fuocheggiatori;
- flat panel;
- router, switch e apparati di rete;
- sensori OPEN, CLOSED e SAFE;
- linee USB, seriali, Ethernet e GPIO.

## 35.3 Principi di progettazione

I cablaggi devono rispettare i seguenti principi:

1. separazione tra linee di potenza e linee dati;
2. identificazione univoca di ogni cavo;
3. riduzione delle sollecitazioni meccaniche;
4. prevenzione di loop e impigliamenti durante i movimenti;
5. accessibilità per manutenzione;
6. documentazione aggiornata dopo ogni modifica.

## 35.4 Codifica dei cavi

Ogni cavo deve ricevere un identificativo nel formato:

```text
DSG-CBL-<TIPO>-<NUMERO>
```

Esempi:

| Codice | Descrizione |
|---|---|
| DSG-CBL-PWR-001 | Alimentazione 12 V montatura |
| DSG-CBL-USB-003 | Collegamento USB camera principale |
| DSG-CBL-LAN-002 | Collegamento Ethernet EAGLE–switch |
| DSG-CBL-SEN-001 | Sensore finecorsa CLOSED |

## 35.5 Scheda di censimento

Per ogni cavo devono essere registrati:

| Campo | Descrizione |
|---|---|
| Codice | Identificativo univoco |
| Origine | Dispositivo o morsetto sorgente |
| Destinazione | Dispositivo o morsetto terminale |
| Tipo | Potenza, USB, Ethernet, sensore, seriale |
| Lunghezza | Valore reale o stimato |
| Sezione / categoria | Sezione conduttore o categoria dati |
| Connettori | Tipo alle due estremità |
| Percorso | Canalina, braccio, colonna, parete |
| Stato | Attivo, riserva, dismesso |
| Data installazione | Data di posa |

## 35.6 Architettura elettrica di alto livello

```text
Rete 230 V AC
   |
   +-- Protezione generale
   |
   +-- Alimentatore EAGLE
   +-- Alimentatore CGX-L
   +-- Alimentatore rete / Starlink
   +-- Illuminazione tecnica
   +-- Servizi ausiliari

EAGLE / Distribuzione 12 V DC
   |
   +-- Camera principale
   +-- Camera guida
   +-- Fuocheggiatore
   +-- Ruota filtri
   +-- Flat panel
```

> **DA VALIDARE:** inserire lo schema reale delle protezioni, degli alimentatori e delle uscite utilizzate.

## 35.7 Mappatura USB

La mappatura USB deve essere stabile e documentata.

| Porta | Dispositivo | Driver | Note |
|---|---|---|---|
| USB-01 | Camera principale | Da censire | Preferire USB 3.0 |
| USB-02 | Camera guida | Da censire | Evitare hub non alimentati |
| USB-03 | CGX-L / CPWI | Da censire | Porta critica |
| USB-04 | FocusCube / ESATTO | Da censire | Profilo dipendente |
| USB-05 | Flat panel | Da censire | — |

## 35.8 Regole di posa

- evitare curve strette e schiacciamenti;
- lasciare adeguato gioco nei tratti mobili;
- fissare i cavi senza creare punti di tensione;
- mantenere i cavi di potenza separati dai segnali sensibili;
- utilizzare etichette resistenti e leggibili;
- evitare adattatori non necessari.

## 35.9 Procedura DSG-PROC-035-01 — Aggiornamento della mappa cablaggi

1. identificare il cavo modificato o introdotto;
2. assegnare il codice DSG-CBL;
3. aggiornare la tabella di censimento;
4. aggiornare lo schema logico;
5. eseguire un test funzionale;
6. registrare la modifica nel Change Log;
7. fotografare il collegamento se utile.

## 35.10 Collaudo

Il collaudo deve comprendere:

- continuità elettrica;
- corretta polarità;
- stabilità del collegamento dati;
- assenza di interferenze;
- verifica durante movimenti completi della montatura;
- verifica durante apertura e chiusura della copertura.

## 35.11 Troubleshooting

### Disconnessioni USB intermittenti

Verificare:

- qualità e lunghezza del cavo;
- connettori allentati;
- alimentazione insufficiente;
- sospensione selettiva USB di Windows;
- hub intermedi;
- interferenze elettromagnetiche.

### Caduta di tensione

Verificare:

- sezione del cavo;
- lunghezza;
- assorbimento di picco;
- connettori ossidati;
- alimentatore sottodimensionato.

## 35.12 Manutenzione

### Mensile

- ispezione visiva dei cavi mobili;
- controllo dei connettori;
- verifica dell'assenza di abrasioni.

### Annuale

- verifica completa delle etichette;
- test delle linee critiche;
- aggiornamento delle fotografie e degli schemi.

## 35.13 KPI

| KPI | Descrizione |
|---|---|
| Disconnessioni USB per mese | Numero di eventi |
| Guasti cavo per trimestre | Numero |
| Cablaggi censiti | Percentuale sul totale |
| Schemi aggiornati | Percentuale dopo modifiche |

## 35.14 FMEA sintetica

| Guasto | Effetto | Gravità | Mitigazione |
|---|---|---:|---|
| Cavo USB difettoso | Perdita dispositivo | Alta | Ricambio e test periodico |
| Polarità errata | Danno apparato | Critica | Etichettatura e connettori chiave |
| Cavo impigliato | Rischio meccanico | Critica | Route planning e test movimento |
| Ethernet scollegata | Perdita controllo | Alta | Fissaggio e monitoraggio |

## 35.15 Dati da validare

- schema reale 230 V AC;
- schema reale 12 V DC;
- elenco alimentatori e potenze;
- mappatura USB definitiva;
- codifica completa dei cavi;
- fotografie dei percorsi principali.
