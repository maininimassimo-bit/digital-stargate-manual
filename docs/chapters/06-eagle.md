# Capitolo 6 – Computer di controllo PrimaLuceLab EAGLE

**Codice documento:** DSG-TM-001-06  
**Revisione:** 0.3 Draft consolidato  
**Sistema:** Controllo centrale dell’osservatorio  
**Responsabile:** Massimo Mainini

## 6.1 Scopo

Il presente capitolo descrive il computer di controllo PrimaLuceLab EAGLE installato presso Digital StarGate, il suo ruolo nell’architettura generale, le dipendenze software e hardware, le modalità di avvio, backup, ripristino e manutenzione.

L’EAGLE costituisce il nodo centrale del sistema e concentra quattro funzioni principali:

1. esecuzione del software astronomico;
2. collegamento USB delle periferiche;
3. distribuzione e controllo delle alimentazioni a bassa tensione;
4. accesso remoto attraverso la rete dell’osservatorio.

La disponibilità dell’EAGLE è quindi un requisito essenziale per la conduzione remota delle sessioni.

## 6.2 Campo di applicazione

Le indicazioni si applicano all’unità EAGLE utilizzata per:

- controllo della montatura Celestron CGX-L;
- acquisizione con QHY695A e ToupTek 294MC Pro;
- gestione di camera guida, fuocheggiatori e flat panel;
- esecuzione di N.I.N.A., CPWI, PHD2, ASCOM e ASTAP;
- salvataggio temporaneo dei dati osservativi;
- diagnostica e recovery remoto.

## 6.3 Ruolo architetturale

```text
VPN / LAN osservatorio
        │
        ▼
PrimaLuceLab EAGLE
        │
        ├── Windows
        ├── N.I.N.A.
        ├── CPWI
        ├── PHD2
        ├── ASCOM Platform
        ├── ASTAP
        ├── Driver camere e accessori
        ├── Porte USB
        └── Uscite di alimentazione
```

L’EAGLE non deve essere considerato un semplice personal computer, ma un sottosistema critico. Un aggiornamento, una modifica delle porte USB o una variazione delle alimentazioni può influire sull’intero osservatorio.

## 6.4 Inventario logico

| ID | Funzione | Applicazione o interfaccia | Criticità |
|---|---|---|---|
| DSG-PC-001 | Sistema operativo | Windows | Critica |
| DSG-PC-002 | Sequencer | N.I.N.A. | Critica |
| DSG-PC-003 | Controllo montatura | CPWI | Critica |
| DSG-PC-004 | Autoguida | PHD2 | Critica |
| DSG-PC-005 | Middleware | ASCOM Platform | Critica |
| DSG-PC-006 | Plate solving | ASTAP | Alta |
| DSG-PC-007 | Desktop remoto | RDP o strumento approvato | Alta |
| DSG-PC-008 | Archiviazione locale | SSD interno | Alta |

> **DA VALIDARE:** modello esatto dell’EAGLE, numero di serie, CPU, RAM, capacità SSD, versione BIOS e versione di Windows.

## 6.5 Configurazione del sistema operativo

Il sistema operativo deve essere configurato per privilegiare continuità e prevedibilità.

### 6.5.1 Requisiti minimi di configurazione

- nome host univoco e documentato;
- account operativo dedicato;
- password custodita in modo sicuro;
- fuso orario Europe/Rome;
- sincronizzazione automatica dell’orologio;
- sospensione e ibernazione disabilitate;
- riavvio automatico dopo il ritorno dell’alimentazione, se supportato;
- aggiornamenti pianificati fuori dalle finestre osservative;
- esclusione delle cartelle operative da software che possano bloccare i file durante l’acquisizione;
- spazio libero minimo su disco definito e monitorato.

> **SICUREZZA:** non riportare nel repository pubblico password, chiavi VPN, PIN delle SIM o credenziali amministrative.

### 6.5.2 Power management

Devono essere disabilitate le funzioni che possono interrompere periferiche o comunicazioni:

- sospensione selettiva USB;
- spegnimento automatico dei controller USB;
- sospensione del sistema;
- spegnimento del disco durante la sessione;
- risparmio energetico della scheda di rete, se causa disconnessioni.

## 6.6 Mappatura USB

La stabilità delle porte è essenziale. Ogni periferica deve essere collegata sempre alla stessa porta fisica, salvo interventi documentati.

| Porta logica | Dispositivo previsto | Interfaccia | Alimentazione | Stato |
|---|---|---|---|---|
| USB-01 | Camera principale | USB 3 | Separata/EAGLE | DA VALIDARE |
| USB-02 | Camera guida | USB 2/3 | USB | DA VALIDARE |
| USB-03 | Montatura CGX-L/CPWI | USB | Separata | DA VALIDARE |
| USB-04 | Pegasus FocusCube | USB | 12 V | DA VALIDARE |
| USB-05 | ESATTO 2" | USB | 12 V | DA VALIDARE |
| USB-06 | Wanderer Cover V4 | USB | 12 V | DA VALIDARE |
| USB-07 | Ruota portafiltri | USB | USB/12 V | DA VALIDARE |

### Regole operative

- evitare hub USB non alimentati;
- utilizzare cavi corti e di qualità adeguata;
- etichettare entrambe le estremità di ogni cavo;
- non modificare più connessioni contemporaneamente durante il troubleshooting;
- registrare ogni spostamento nel registro configurazioni.

## 6.7 Distribuzione delle alimentazioni

Per ogni uscita devono essere censiti tensione nominale, corrente massima, dispositivo associato e comportamento allo spegnimento.

| Uscita | Dispositivo | Tensione | Assorbimento nominale | Assorbimento di picco | Sequenza |
|---|---|---:|---:|---:|---|
| PWR-01 | Camera principale | 12 V | DA VALIDARE | DA VALIDARE | Prima di N.I.N.A. |
| PWR-02 | Montatura | 12 V | DA VALIDARE | DA VALIDARE | Prima di CPWI |
| PWR-03 | Fuocheggiatore | 12 V | DA VALIDARE | DA VALIDARE | Prima di N.I.N.A. |
| PWR-04 | Flat panel | 12 V | DA VALIDARE | DA VALIDARE | Su richiesta |

Non superare i limiti dichiarati dal costruttore dell’EAGLE e degli alimentatori.

## 6.8 Software e dipendenze

| Software | Funzione | Dipendenze principali | Backup richiesto |
|---|---|---|---|
| N.I.N.A. | Acquisizione e sequenze | ASCOM, driver nativi, ASTAP, PHD2 | Profili, sequenze, plugin |
| CPWI | Controllo CGX-L | Driver Celestron, USB | Configurazione e log |
| PHD2 | Autoguida | Camera guida, ASCOM mount | Profili e calibrazioni |
| ASCOM Platform | Middleware | Driver dispositivi | Elenco versioni |
| ASTAP | Plate solving | Database stellare | Percorsi e impostazioni |

## 6.9 Procedura DSG-PROC-006-01 – Avvio controllato

1. Verificare che l’alimentazione generale sia stabile.
2. Verificare la raggiungibilità della LAN e del router RUT955.
3. Accendere l’EAGLE o verificare che si sia riavviato automaticamente.
4. Attendere il completamento del boot.
5. Collegarsi tramite desktop remoto.
6. Verificare data, ora e fuso orario.
7. Controllare spazio disco, CPU, memoria e stato della rete.
8. Alimentare le periferiche secondo la sequenza definita.
9. Avviare CPWI e connettere la montatura.
10. Avviare N.I.N.A. e connettere i dispositivi.
11. Avviare PHD2 solo dopo la disponibilità della montatura e della camera guida.
12. Eseguire la checklist pre-sessione del Capitolo 16.

**Criterio di accettazione:** nessun errore critico in Gestione dispositivi; dispositivi essenziali connessi; spazio disco sopra la soglia operativa.

## 6.10 Procedura DSG-PROC-006-02 – Riavvio remoto

Il riavvio remoto è ammesso solo dopo aver verificato che:

- non siano in corso esposizioni;
- la montatura sia ferma o parcheggiata;
- la copertura sia in stato sicuro;
- non siano in corso scritture o trasferimenti critici.

Procedura:

1. salvare log e configurazioni aperte;
2. arrestare N.I.N.A., PHD2 e CPWI in quest’ordine;
3. verificare la posizione della montatura;
4. eseguire il riavvio di Windows;
5. attendere almeno il tempo di boot validato;
6. riconnettersi e ripetere DSG-PROC-006-01.

## 6.11 Backup e ripristino

### Contenuti da proteggere

- profili e sequenze N.I.N.A.;
- profili e log PHD2;
- configurazioni CPWI;
- installatori e versioni dei driver stabili;
- database ASTAP e relative impostazioni;
- script, file JSON e plugin;
- documentazione dei mapping USB e power;
- log di Windows relativi agli incidenti;
- immagini non ancora trasferite.

### Politica consigliata

| Tipo | Frequenza | Destinazione | Verifica |
|---|---|---|---|
| Configurazioni | Dopo ogni modifica | Repository/archivio protetto | Diff e apertura file |
| Dati sessione | Dopo ogni notte | Storage esterno | Conteggio e checksum |
| Immagine sistema | Trimestrale o prima di upgrade | Disco esterno | Test di ripristino |

## 6.12 Aggiornamenti e change management

Ogni aggiornamento deve seguire il ciclo:

1. inventario delle versioni correnti;
2. backup;
3. aggiornamento di un solo componente per volta;
4. test funzionale locale o controllato;
5. test di una sequenza breve;
6. registrazione dell’esito;
7. possibilità di rollback.

Non aggiornare Windows, ASCOM, CPWI, N.I.N.A. o i driver immediatamente prima di una campagna osservativa importante.

## 6.13 Monitoraggio e KPI

| KPI | Descrizione | Valore obiettivo |
|---|---|---|
| Tempo medio di avvio | Accensione → sistema operativo disponibile | DA VALIDARE |
| Tempo medio di inizializzazione | Desktop → dispositivi connessi | DA VALIDARE |
| Disconnessioni USB | Numero per sessione | 0 |
| Spazio libero SSD | Percentuale minima | DA VALIDARE |
| Riavvii imprevisti | Numero mensile | 0 |

## 6.14 Troubleshooting

### EAGLE non raggiungibile

1. verificare VPN e RUT955;
2. verificare l’indirizzo IP assegnato;
3. eseguire ping dalla LAN/VPN;
4. controllare alimentazione e LED di stato;
5. tentare un riavvio remoto solo se la montatura è sicura;
6. se non recuperabile, attivare escalation per intervento locale.

### Periferica USB non rilevata

1. verificare alimentazione della periferica;
2. verificare il cavo e la porta prevista;
3. controllare Gestione dispositivi;
4. disconnettere e riconnettere il software, non il cavo, come primo tentativo;
5. riavviare il singolo driver;
6. riavviare l’EAGLE solo dopo messa in sicurezza.

### Disco quasi pieno

1. interrompere nuove acquisizioni se lo spazio è insufficiente;
2. trasferire i dati già completati;
3. rimuovere solo file temporanei conosciuti;
4. non cancellare log dell’incidente prima del backup.

## 6.15 FMEA sintetica

| Modo di guasto | Effetto | Rilevazione | Mitigazione |
|---|---|---|---|
| Blocco Windows | Perdita controllo centrale | RDP e heartbeat assenti | Riavvio controllato, recovery locale |
| Disconnessione USB | Perdita dispositivo | Errori N.I.N.A./PHD2/CPWI | Mappatura stabile, power management disabilitato |
| SSD pieno | Arresto acquisizioni | Monitoraggio spazio | Trasferimento e soglie di allarme |
| Aggiornamento incompatibile | Regressione software | Test fallito | Backup e rollback |
| Alimentazione instabile | Riavvii e perdita sessione | Log e LED | UPS/protezioni da validare |

## 6.16 Manutenzione

### Mensile

- verifica spazio disco e SMART;
- revisione log di sistema;
- verifica mapping USB;
- esportazione configurazioni;
- controllo temperature operative.

### Trimestrale

- immagine di sistema o backup completo;
- test di riavvio e riconnessione;
- verifica del piano di rollback;
- controllo versioni e compatibilità.

### Annuale

- pulizia esterna e ispezione connettori;
- verifica prestazioni SSD;
- revisione account e sicurezza;
- aggiornamento inventario tecnico.

## 6.17 Dati da validare

- modello e generazione esatta dell’EAGLE;
- specifiche CPU, RAM e SSD;
- versione Windows;
- configurazione BIOS/auto power-on;
- mappatura reale USB e alimentazioni;
- soglie di temperatura e spazio disco;
- metodo di backup e percorso di destinazione.
