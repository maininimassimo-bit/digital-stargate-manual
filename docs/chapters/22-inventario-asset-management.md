# Capitolo 22 – Inventario tecnico e Asset Management

**Codice documento:** DSG-TM-001-22  
**Revisione:** 0.1 Draft

## 22.1 Scopo

Questo capitolo definisce l'inventario ufficiale dei componenti dell'osservatorio e le regole per la gestione del loro ciclo di vita.

## 22.2 Categorie di asset

- struttura e cupola;
- alimentazione e rete;
- computer e storage;
- montatura;
- ottiche;
- camere;
- filtri e ruote portafiltri;
- fuocheggiatori;
- sensori e accessori;
- software, licenze e firmware.

## 22.3 Codifica asset

Formato:

```text
DSG-<CATEGORIA>-<NUMERO>
```

Esempi:

```text
DSG-NET-001
DSG-PC-001
DSG-MNT-001
DSG-OTA-001
DSG-CAM-001
```

## 22.4 Scheda asset minima

| Campo | Descrizione |
|---|---|
| Asset ID | identificativo univoco |
| Produttore | marca |
| Modello | modello commerciale |
| Numero di serie | seriale |
| Data installazione | data messa in servizio |
| Posizione | ubicazione fisica |
| Firmware | versione |
| Driver | versione |
| Stato | operativo, riserva, guasto, dismesso |
| Ultima manutenzione | data |
| Prossima manutenzione | data |

## 22.5 Inventario iniziale

| Asset ID | Componente | Modello | Stato |
|---|---|---|---|
| DSG-NET-001 | Router primario | Starlink | Operativo |
| DSG-NET-002 | Router failover/VPN | Teltonika RUT955 | Operativo |
| DSG-PC-001 | Computer di controllo | PrimaLuceLab EAGLE3 | Operativo |
| DSG-MNT-001 | Montatura | Celestron CGX-L | Operativo |
| DSG-OTA-001 | Telescopio | Celestron C8 XLT | Operativo |
| DSG-OTA-002 | Telescopio | Sky-Watcher Quattro 200P | Operativo |
| DSG-CAM-001 | Camera mono | QHY695A | Operativo |
| DSG-CAM-002 | Camera OSC | ToupTek 294MC Pro | Operativo |
| DSG-FOC-001 | Fuocheggiatore | Pegasus FocusCube | Operativo |
| DSG-FOC-002 | Fuocheggiatore | ESATTO 2" | Operativo |

## 22.6 Procedura DSG-PROC-022-01 – Inserimento nuovo asset

1. Assegnare Asset ID.
2. Registrare dati tecnici e seriale.
3. Fotografare il componente e l'etichetta.
4. Registrare firmware e driver.
5. Associare manuali e file di configurazione.
6. Pianificare manutenzione.
7. Aggiornare il repository.

## 22.7 Ciclo di vita

Stati previsti:

```text
ACQUISTATO -> IN TEST -> OPERATIVO -> IN MANUTENZIONE -> RISERVA -> DISMESSO
```

## 22.8 Ricambi critici

Devono essere identificati i ricambi con elevato impatto sulla continuità operativa:

- alimentatori 12 V;
- cavi USB e di rete;
- fusibili e protezioni;
- adattatori meccanici;
- supporti di archiviazione;
- SIM di backup;
- sensori di finecorsa.

## 22.9 KPI

| KPI | Descrizione |
|---|---|
| Asset censiti | % sul totale |
| Asset con seriale registrato | % |
| Asset con firmware noto | % |
| Asset oltre manutenzione | Numero |
| Ricambi critici disponibili | % |

## 22.10 Dati da validare

> **DA VALIDARE:** numeri di serie e date di installazione.

> **DA VALIDARE:** disponibilità e posizione dei ricambi critici.
