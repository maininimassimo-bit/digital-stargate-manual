# Capitolo 2 – Architettura generale

**Codice documento:** DSG-TM-001-02  
**Revisione:** 0.2 Draft  
**Classificazione:** Engineering Documentation

## 2.1 Scopo

Il capitolo descrive la struttura logica e funzionale di Digital StarGate, le dipendenze tra i sottosistemi e gli stati operativi utilizzati per governare una sessione remota.

L’architettura è progettata per consentire l’uso locale e remoto dell’osservatorio, mantenendo la protezione della strumentazione come requisito prioritario.

## 2.2 Principi progettuali

### 2.2.1 Modularità

Ogni sottosistema deve poter essere configurato, verificato e sostituito con impatto controllato sugli altri componenti. La modularità riguarda:

- rete e connettività;
- computer di controllo;
- montatura;
- ottica e camere;
- cupola e sensori;
- applicazioni software;
- automazione e procedure.

### 2.2.2 Affidabilità

Le configurazioni stabili e collaudate hanno priorità rispetto agli aggiornamenti non necessari. Gli aggiornamenti devono essere eseguiti solo dopo backup e disponibilità di una procedura di rollback.

### 2.2.3 Fail-safe

Quando lo stato di un componente critico è sconosciuto, il sistema non deve assumere che sia sicuro. Deve interrompere l’azione e richiedere una verifica.

### 2.2.4 Osservabilità

I sottosistemi devono produrre informazioni sufficienti a comprendere lo stato dell’impianto: indicatori, log, sensori, messaggi applicativi e report di sessione.

### 2.2.5 Tracciabilità

Configurazioni, incidenti, manutenzioni e modifiche devono essere registrati e versionati.

## 2.3 Macro-sistemi

| ID | Sottosistema | Funzione principale | Componenti principali |
|---|---|---|---|
| SYS-01 | Struttura e protezione | Protezione fisica e accesso al cielo | struttura, tetto, guide, motore |
| SYS-02 | Sicurezza cupola | Conferma degli stati meccanici | sensori OPEN, CLOSED, SAFE |
| SYS-03 | Alimentazione | Distribuzione dell’energia | quadro, alimentatori, linee 230 V e 12 V |
| SYS-04 | Networking | Accesso remoto e continuità WAN | Starlink, RUT955, SIM, VPN |
| SYS-05 | Controllo | Esecuzione dei software | EAGLE3, Windows, storage |
| SYS-06 | Puntamento | Puntamento e inseguimento | CGX-L, CPWI, ASCOM |
| SYS-07 | Acquisizione | Produzione dei dati astronomici | telescopi, camere, filtri |
| SYS-08 | Guida e fuoco | Correzione inseguimento e messa a fuoco | PHD2, camere guida, FocusCube, ESATTO |
| SYS-09 | Automazione | Orchestrazione della sessione | N.I.N.A., sequenze, recovery |
| SYS-10 | Monitoraggio | Controllo del cielo e registrazione | AllSky, log, report |

## 2.4 Architettura logica

```text
Operatore remoto
      │
      ▼
VPN sul Teltonika RUT955
      │
      ▼
LAN dell'osservatorio
      │
      ├────────► AllSky / apparati di rete
      │
      ▼
PrimaLuceLab EAGLE3
      │
      ├────────► N.I.N.A.
      ├────────► CPWI
      ├────────► PHD2
      ├────────► ASCOM e driver
      │
      ▼
Montatura, camere, fuocheggiatori, filtri e accessori
```

La catena di controllo della montatura deve essere mantenuta coerente:

```text
N.I.N.A. / PHD2 → ASCOM → CPWI → CGX-L
```

CPWI costituisce il punto di controllo diretto della montatura. Le altre applicazioni devono utilizzare l’interfaccia prevista e non aprire connessioni concorrenti incompatibili.

## 2.5 Architettura fisica indicativa

| Area | Apparati | Collegamenti principali |
|---|---|---|
| Esterno | antenna Starlink, struttura di copertura | WAN, alimentazione |
| Locale tecnico | RUT955, alimentatori, protezioni | Ethernet, LTE, 230 V |
| Montatura | EAGLE3, CGX-L, ottica, camere | USB, 12 V, rete |
| Tetto | motore, finecorsa e sensori | alimentazione e segnali |
| Monitoraggio | AllSky e sensori ausiliari | rete e alimentazione |

> **DA VALIDARE:** completare la planimetria fisica con posizione reale di apparati, prese, percorsi dei cavi e punti di sezionamento.

## 2.6 Dipendenze critiche

| Funzione | Dipendenze minime | Conseguenza del guasto |
|---|---|---|
| Accesso remoto | RUT955, WAN disponibile, VPN | perdita della supervisione remota |
| Inizializzazione montatura | alimentazione, USB, CPWI, ASCOM | impossibilità di puntamento |
| Acquisizione | camera, storage, N.I.N.A. | interruzione delle esposizioni |
| Guida | camera guida, PHD2, ASCOM, montatura | stelle mosse e pausa sequenza |
| Chiusura tetto | alimentazione, centralina, sensori coerenti | rischio di mancata protezione |
| Recovery | log, accesso al sistema, stato noto | impossibilità di ripresa sicura |

## 2.7 Stati operativi

Digital StarGate viene rappresentato mediante una macchina a stati.

| Stato | Descrizione | Condizioni tipiche |
|---|---|---|
| OFFLINE | Impianto non disponibile | apparati spenti o manutenzione |
| READY | Impianto acceso e protetto | tetto chiuso, montatura in Park |
| INITIALIZATION | Collegamento e verifica dei dispositivi | avvio CPWI, N.I.N.A. e PHD2 |
| OPENING | Apertura in corso | sensori monitorati |
| OBSERVING | Sessione attiva | tracking, guida e acquisizione |
| RECOVERY | Tentativo controllato di ripristino | errore recuperabile |
| SHUTDOWN | Fine sessione e messa in sicurezza | stop guida, Park e chiusura |
| SAFE MODE | Stato protettivo | sessione interrotta, azioni limitate |
| MAINTENANCE | Interventi tecnici | automazioni inibite |

Transizioni principali:

```text
OFFLINE → READY → INITIALIZATION → OPENING → OBSERVING
OBSERVING → RECOVERY → OBSERVING
OBSERVING → SHUTDOWN → READY
QUALSIASI STATO → SAFE MODE
READY ↔ MAINTENANCE
```

## 2.8 Regole di transizione

Una transizione è autorizzata solo quando i prerequisiti risultano verificati.

Esempi:

- `READY → OPENING`: montatura in posizione sicura, stato sensori coerente e condizioni ambientali accettabili;
- `OPENING → OBSERVING`: conferma del sensore OPEN e assenza di allarmi;
- `OBSERVING → SHUTDOWN`: sequenza terminata o comando dell’operatore;
- `RECOVERY → OBSERVING`: stato ripristinato e verificato;
- `RECOVERY → SAFE MODE`: recovery fallito o stato non determinabile.

## 2.9 Flusso operativo di alto livello

1. verifica della disponibilità dell’alimentazione;
2. verifica della rete primaria o di backup;
3. accesso all’EAGLE3;
4. controllo dei servizi Windows e dello spazio disco;
5. avvio di CPWI e collegamento alla montatura;
6. avvio di N.I.N.A. e collegamento delle periferiche;
7. verifica dei sensori della copertura;
8. apertura controllata;
9. plate solving, autofocus e guida;
10. acquisizione e monitoraggio;
11. eventuale meridian flip;
12. arresto guida e Park;
13. chiusura della copertura;
14. archiviazione di dati e log.

## 2.10 Interfacce tra sottosistemi

| Interfaccia | Tecnologia | Note operative |
|---|---|---|
| WAN primaria | Starlink | disponibilità soggetta a copertura e servizio |
| WAN di backup | LTE SIM1/SIM2 | gestita dal RUT955 |
| Accesso remoto | VPN | obbligatorio per i servizi di gestione |
| LAN | Ethernet/Wi-Fi | indirizzamento documentato e controllato |
| Periferiche astronomiche | USB | cavi corti, stabili e identificati |
| Astrazione hardware | ASCOM | versioni testate e registrate |
| Controllo montatura | CPWI | punto di accesso diretto alla CGX-L |
| Guida | PHD2 | pulse guiding via ASCOM |
| Orchestrazione | N.I.N.A. | profili dedicati alle configurazioni ottiche |

## 2.11 Requisiti non funzionali

### Disponibilità

L’osservatorio deve poter completare una sequenza in autonomia anche in caso di perdita temporanea della supervisione remota, purché tutti i sottosistemi critici restino operativi e le condizioni di sicurezza siano soddisfatte.

### Sicurezza informatica

- accesso amministrativo limitato;
- VPN obbligatoria;
- nessuna credenziale nel repository;
- backup delle configurazioni;
- aggiornamenti pianificati.

### Manutenibilità

Cavi, porte, alimentazioni e profili software devono essere identificabili e documentati.

### Recuperabilità

Devono esistere backup e procedure di ripristino per router, EAGLE3, profili N.I.N.A., PHD2 e configurazioni CPWI.

## 2.12 Criteri di accettazione architetturale

L’architettura è considerata coerente quando:

- ogni dispositivo critico ha un proprietario logico e un percorso di controllo definito;
- non esistono connessioni software concorrenti non documentate;
- le dipendenze per apertura e chiusura sono note;
- la perdita di un servizio non genera comandi meccanici incontrollati;
- sono disponibili procedure di messa in sicurezza;
- il diagramma di rete e l’inventario rispecchiano lo stato reale.

## 2.13 Dati da validare

> **DA VALIDARE:** posizione Park effettiva e margini di sicurezza della CGX-L.

> **DA VALIDARE:** logica reale del segnale SAFE e dipendenze della centralina del tetto.

> **DA VALIDARE:** schema fisico delle connessioni USB e delle alimentazioni dall’EAGLE3.

> **DA VALIDARE:** presenza e caratteristiche di eventuali UPS o sistemi di riavvio remoto.

## 2.14 Riferimenti interni

- [Capitolo 3 – Struttura della cupola](03-struttura-cupola.md)
- [Capitolo 4 – Impianto elettrico](04-impianto-elettrico.md)
- [Capitolo 5 – Infrastruttura di rete](05-infrastruttura-rete.md)
- [Capitolo 15 – Architettura dell’automazione](15-automazione.md)
- [Capitolo 18 – Emergenze e recovery](18-emergenze-recovery.md)
