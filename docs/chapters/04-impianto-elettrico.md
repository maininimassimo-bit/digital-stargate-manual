# Capitolo 4 – Impianto elettrico e distribuzione delle alimentazioni

**Codice documento:** DSG-TM-001-04  
**Revisione:** 0.2 Draft  
**Classificazione:** Engineering Documentation

## 4.1 Scopo

Il capitolo descrive i criteri di distribuzione dell’energia elettrica, le utenze dell’osservatorio, le verifiche operative e le misure di manutenzione necessarie a ridurre il rischio di guasti, surriscaldamenti e interruzioni non controllate.

Le attività sull’impianto a 230 V devono essere eseguite esclusivamente da personale qualificato e nel rispetto delle norme applicabili.

!!! danger "Rischio elettrico"
    Il manuale non autorizza interventi su circuiti in tensione. Prima di aprire quadri o modificare cablaggi è necessario isolare l’alimentazione, verificarne l’assenza e applicare le procedure di sicurezza previste.

## 4.2 Architettura generale

L’impianto comprende indicativamente:

```text
Rete 230 V AC
   │
   ├── Protezioni e sezionamento
   │      ├── Alimentatori 12 V DC
   │      ├── EAGLE3
   │      ├── Montatura CGX-L
   │      ├── Camere e accessori
   │      ├── Motorizzazione copertura
   │      ├── Starlink
   │      ├── Teltonika RUT955
   │      └── Illuminazione tecnica
   │
   └── Eventuale UPS / riavvio remoto
```

> **DA VALIDARE:** presenza, modello, autonomia e utenze protette da UPS.

## 4.3 Principi progettuali

### Selettività

Un guasto su un’utenza non dovrebbe disalimentare indiscriminatamente l’intero osservatorio. Le linee critiche devono essere identificabili e, ove possibile, isolate singolarmente.

### Separazione

Cavi di alimentazione e segnali dati devono seguire percorsi ordinati, evitando accoppiamenti e trazioni sui connettori.

### Identificazione

Ogni cavo, alimentatore, presa e uscita deve riportare un identificativo coerente con l’inventario.

### Margine elettrico

Gli alimentatori non devono essere utilizzati costantemente al limite nominale. L’assorbimento di picco dei dispositivi, in particolare montatura, raffreddamento delle camere e motori, deve essere considerato nel dimensionamento.

### Protezione ambientale

Connessioni e alimentatori devono essere protetti da umidità, condensa, polvere e contatto accidentale.

## 4.4 Inventario delle utenze

| ID | Utenza | Tensione nominale | Alimentatore/linea | Stato documentazione |
|---|---|---:|---|---|
| PWR-01 | PrimaLuceLab EAGLE3 | 12 V DC | da censire | Da validare |
| PWR-02 | Celestron CGX-L | 12 V DC | da censire | Da validare |
| PWR-03 | QHY695A | 12 V DC | EAGLE/alimentatore | Da validare |
| PWR-04 | ToupTek 294MC Pro | 12 V DC | EAGLE/alimentatore | Da validare |
| PWR-05 | Pegasus FocusCube | secondo configurazione | USB/12 V | Da validare |
| PWR-06 | ESATTO 2” | 12 V DC | EAGLE/alimentatore | Da validare |
| PWR-07 | Wanderer Cover V4 | 12 V DC | da censire | Da validare |
| PWR-08 | Starlink | alimentatore dedicato | 230 V AC | Parziale |
| PWR-09 | Teltonika RUT955 | DC dedicata | alimentatore dedicato | Parziale |
| PWR-10 | AllSky | 5/12 V secondo componenti | da censire | Da validare |
| PWR-11 | Motore copertura | da censire | linea dedicata | Da validare |
| PWR-12 | Illuminazione tecnica | 230 V AC | linea dedicata | Da validare |

## 4.5 Mappatura delle alimentazioni EAGLE3

Per ogni uscita dell’EAGLE3 devono essere documentati:

- numero della porta;
- tensione configurata;
- corrente massima ammessa;
- dispositivo collegato;
- assorbimento nominale e di picco;
- comportamento all’avvio;
- stato predefinito dopo un riavvio.

Tabella di censimento:

| Porta EAGLE | Tensione | Dispositivo | Corrente nominale | Corrente di picco | Auto-on | Note |
|---|---:|---|---:|---:|---|---|
| P1 | DA VALIDARE | DA VALIDARE |  |  |  |  |
| P2 | DA VALIDARE | DA VALIDARE |  |  |  |  |
| P3 | DA VALIDARE | DA VALIDARE |  |  |  |  |
| P4 | DA VALIDARE | DA VALIDARE |  |  |  |  |

## 4.6 Sequenza raccomandata di accensione

Una sequenza controllata riduce i picchi di corrente e i problemi di enumerazione USB.

1. apparati di rete e VPN;
2. EAGLE3 e sistema operativo;
3. montatura;
4. camere e sistemi di raffreddamento;
5. fuocheggiatori e ruota filtri;
6. accessori e flat panel;
7. motorizzazione della copertura solo quando necessaria.

La sequenza reale deve essere verificata con la configurazione dell’EAGLE3 e con il comportamento dei singoli dispositivi.

## 4.7 Sequenza raccomandata di spegnimento

1. terminare le esposizioni;
2. arrestare la guida;
3. parcheggiare la montatura;
4. chiudere la copertura;
5. portare gradualmente le camere verso la temperatura ambiente;
6. disconnettere i dispositivi dai software;
7. spegnere le utenze astronomiche;
8. lasciare operativi rete e sistemi necessari alla supervisione secondo la politica definita;
9. arrestare Windows solo se previsto.

!!! warning "Raffreddamento camere"
    Evitare lo spegnimento immediato del raffreddamento a piena potenza. Utilizzare, quando disponibile, una fase di warm-up controllato.

## 4.8 Verifiche prima della sessione

- assenza di odori, rumori o temperature anomale;
- alimentatori correttamente ventilati;
- cavi integri e non in trazione;
- connettori ben inseriti;
- tensioni coerenti;
- assenza di condensa;
- spazio libero intorno ai componenti dissipanti;
- stato delle protezioni;
- capacità di accendere singolarmente le utenze critiche.

## 4.9 Caduta di tensione e instabilità

Sintomi possibili:

- disconnessioni USB durante il raffreddamento;
- reset della montatura durante uno slew;
- camere non rilevate;
- errori casuali dei motori;
- riavvio del router o dell’EAGLE3.

Diagnosi:

1. verificare tensione a vuoto e sotto carico;
2. controllare i connettori e la sezione dei cavi;
3. verificare l’assorbimento simultaneo;
4. isolare una utenza alla volta;
5. controllare i log di Windows e delle applicazioni;
6. sostituire temporaneamente l’alimentatore con uno noto e idoneo, se disponibile.

## 4.10 Blackout

In caso di interruzione di rete:

1. determinare se apparati e copertura sono alimentati da una sorgente di continuità;
2. non assumere che la montatura abbia conservato la posizione logica;
3. al ripristino, verificare fisicamente lo stato della copertura;
4. controllare integrità del filesystem e avvio di Windows;
5. verificare CPWI e la posizione della CGX-L;
6. non comandare la chiusura finché non è nota la posizione della montatura;
7. eseguire la procedura di avvio controllato.

## 4.11 Protezione dalle sovratensioni e messa a terra

La protezione da sovratensioni, fulminazioni indirette e differenze di potenziale deve essere valutata da un tecnico qualificato. Il sito include apparati esterni e cavi di rete/alimentazione che possono aumentare l’esposizione ai disturbi.

> **DA VALIDARE:** presenza e tipologia di SPD, messa a terra, differenziale e protezioni magnetotermiche.

## 4.12 Manutenzione preventiva

### Mensile

- controllo visivo di prese, alimentatori e cavi;
- verifica delle temperature;
- rimozione controllata della polvere;
- verifica delle uscite EAGLE3;
- controllo delle segnalazioni di errore.

### Trimestrale

- verifica dei serraggi accessibili a impianto disalimentato e da personale qualificato;
- test di spegnimento e riavvio controllato;
- verifica dell’eventuale UPS;
- aggiornamento della mappa delle utenze.

### Annuale

- verifica delle protezioni elettriche da parte di tecnico qualificato;
- controllo della messa a terra;
- valutazione dello stato degli alimentatori;
- sostituzione preventiva di componenti degradati;
- test documentato di blackout e ripristino.

## 4.13 Checklist DSG-CHK-004 – Impianto elettrico

- [ ] quadro integro e chiuso;
- [ ] protezioni non intervenute;
- [ ] alimentatori senza surriscaldamenti;
- [ ] cavi identificati;
- [ ] nessuna condensa;
- [ ] tensioni nominali verificate;
- [ ] uscite EAGLE3 correttamente mappate;
- [ ] apparati di rete alimentati;
- [ ] procedura di blackout disponibile;
- [ ] esito registrato.

## 4.14 Dati da validare

> **DA VALIDARE:** schema unifilare reale dell’impianto.

> **DA VALIDARE:** potenza disponibile, protezioni e sezioni dei cavi.

> **DA VALIDARE:** inventario completo degli alimentatori con modello e serial number.

> **DA VALIDARE:** presenza di UPS e autonomia misurata con il carico reale.

> **DA VALIDARE:** mappatura delle uscite di alimentazione dell’EAGLE3.

## 4.15 Riferimenti interni

- [Capitolo 3 – Struttura della cupola](03-struttura-cupola.md)
- [Capitolo 6 – EAGLE](06-eagle.md)
- [Capitolo 18 – Emergenze e recovery](18-emergenze-recovery.md)
- [Capitolo 19 – Manutenzione preventiva](19-manutenzione-preventiva.md)
