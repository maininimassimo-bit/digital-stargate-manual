# Capitolo 7 – Montatura equatoriale Celestron CGX-L

**Codice documento:** DSG-TM-001-07  
**Revisione:** 0.3 Draft consolidato  
**Sistema:** Puntamento e inseguimento  
**Installazione:** Permanente su colonna

## 7.1 Scopo

Il capitolo descrive la montatura Celestron CGX-L, la sua integrazione con CPWI, ASCOM, N.I.N.A. e PHD2, le procedure di inizializzazione, parcheggio, puntamento, meridian flip, recovery e manutenzione.

La montatura è un componente critico perché il suo stato condiziona sia l’acquisizione sia la sicurezza della copertura mobile.

## 7.2 Configurazione operativa

| Parametro | Configurazione Digital StarGate |
|---|---|
| Installazione | Permanente su colonna |
| Controllo diretto | CPWI |
| Interfaccia applicativa | ASCOM Telescope |
| Sequencer | N.I.N.A. |
| Guida | PHD2 pulse guiding via ASCOM |
| Plate solving | ASTAP tramite N.I.N.A. |
| Ottiche principali | C8 XLT / Quattro 200P |

> **DA VALIDARE:** numero di serie, firmware motori e hand controller, versione CPWI, posizione Park, limiti software e meccanici.

## 7.3 Architettura di controllo

```text
N.I.N.A. ─────────────┐
                      ├── ASCOM Telescope ── CPWI ── CGX-L
PHD2 pulse guiding ───┘
```

CPWI deve essere l’unico livello che comunica direttamente con la montatura. N.I.N.A. e PHD2 devono utilizzare il driver ASCOM esposto da CPWI.

## 7.4 Stati operativi

| Stato | Descrizione | Comandi ammessi |
|---|---|---|
| OFF | Montatura non alimentata | Nessuno |
| INITIALIZING | Connessione in corso | Diagnostica |
| PARKED | Posizione di sicurezza | Unpark |
| READY | Connessa, non in movimento | Slew, tracking |
| SLEWING | Movimento verso target | Stop controllato |
| TRACKING | Inseguimento attivo | Guida, acquisizione |
| FLIPPING | Meridian flip in corso | Solo supervisione |
| ERROR | Stato incoerente o connessione persa | Recovery |

## 7.5 Requisiti di sicurezza

- posizione Park compatibile con la chiusura della copertura;
- limiti di movimento definiti e verificati;
- cablaggi con sufficiente libertà su entrambi gli assi;
- assenza di collisioni con colonna, ottica, contrappesi e tetto;
- data, ora, coordinate e fuso orario coerenti;
- tracking disattivato durante alcune fasi di manutenzione;
- verifica visiva locale dopo variazioni importanti del setup.

## 7.6 Bilanciamento

Il bilanciamento deve essere verificato per ciascuna configurazione ottica. La sostituzione tra C8 e Quattro modifica massa, baricentro, momento torcente e gestione dei cavi.

### Procedura DSG-PROC-007-01 – Verifica del bilanciamento

1. mettere la montatura in sicurezza;
2. disalimentare o disattivare i motori secondo le indicazioni del costruttore;
3. verificare l’asse RA in più posizioni;
4. regolare i contrappesi senza lasciare elementi allentati;
5. verificare l’asse DEC con il treno ottico completo;
6. controllare che nessun cavo eserciti trazione;
7. serrare e marcare le posizioni di riferimento;
8. eseguire un test di slew a bassa velocità.

## 7.7 Allineamento polare e modello

L’installazione permanente consente di conservare l’allineamento, ma questo deve essere ricontrollato:

- dopo interventi sulla colonna;
- dopo urti o manutenzione meccanica;
- quando la deriva DEC o le prestazioni di guida peggiorano stabilmente;
- almeno con periodicità annuale.

Il plate solving corregge l’errore di puntamento ma non sostituisce un corretto allineamento polare.

## 7.8 Procedura DSG-PROC-007-02 – Avvio e Unpark

1. verificare che la copertura sia chiusa o aperta in uno stato noto e sicuro;
2. verificare che l’ottica non interferisca con la struttura;
3. alimentare la CGX-L;
4. avviare CPWI;
5. selezionare la connessione configurata;
6. verificare data, ora, sito e stato della montatura;
7. eseguire Unpark solo dopo conferma della posizione fisica;
8. effettuare un breve slew di prova;
9. eseguire plate solving e centering prima dell’acquisizione.

## 7.9 Procedura DSG-PROC-007-03 – Park

1. terminare le esposizioni;
2. arrestare la guida PHD2;
3. disabilitare comandi pendenti in N.I.N.A.;
4. comandare Park tramite CPWI/N.I.N.A.;
5. monitorare il movimento fino al completamento;
6. verificare lo stato PARKED restituito da ASCOM;
7. se disponibile, verificare visivamente la posizione;
8. autorizzare la chiusura della copertura solo dopo esito positivo.

> **CRITICO:** lo stato software “Parked” non deve essere considerato sufficiente se la posizione fisica risulta dubbia o la connessione è stata persa durante il movimento.

## 7.10 Meridian flip

### Sequenza standard

1. N.I.N.A. sospende la sequenza;
2. termina l’esposizione corrente;
3. PHD2 interrompe la guida;
4. N.I.N.A. comanda il flip tramite ASCOM/CPWI;
5. CPWI esegue lo slew oltre il meridiano;
6. N.I.N.A. esegue plate solving e centering;
7. viene eseguito l’autofocus se previsto;
8. PHD2 riprende la guida;
9. la sequenza riparte dopo stabilizzazione.

### Criteri di accettazione

- assenza di collisioni o tensione sui cavi;
- target centrato entro la tolleranza;
- guida stabilizzata;
- tracking siderale attivo;
- orientamento e rotazione coerenti con la sequenza.

## 7.11 Pulse guiding

PHD2 invia correzioni RA/DEC attraverso ASCOM e CPWI. Il percorso completo deve restare disponibile:

```text
PHD2 → ASCOM → CPWI → CGX-L
```

L’errore “Pulse Guide Failed” può derivare da perdita della connessione CPWI, blocco del driver ASCOM, sospensione USB, alimentazione instabile o stato non valido della montatura.

## 7.12 Procedura DSG-PROC-007-04 – Recovery dopo perdita di connessione

1. interrompere o mettere in pausa N.I.N.A.;
2. non inviare nuovi slew finché la posizione non è nota;
3. verificare alimentazione e LED della montatura;
4. verificare il cavo USB e la presenza della periferica in Windows;
5. controllare CPWI e riconnettere la montatura;
6. riconnettere il driver ASCOM in N.I.N.A. e PHD2;
7. eseguire un plate solve senza sync aggressivi se lo stato è dubbio;
8. confermare la posizione e la distanza da limiti/collisioni;
9. eseguire Park o riprendere la sequenza solo dopo validazione.

## 7.13 Parametri da registrare

| Parametro | Valore | Note |
|---|---|---|
| Posizione Park | DA VALIDARE | Compatibile con chiusura |
| Limite est/ovest | DA VALIDARE | CPWI/N.I.N.A. |
| Ritardo flip | DA VALIDARE | Minuti dopo meridiano |
| Tracking rate | Siderale | Salvo casi speciali |
| PEC | DA VALIDARE | Stato e data training |
| Backlash DEC | DA VALIDARE | Da PHD2/analisi |
| RMS tipico | DA VALIDARE | Per configurazione |

## 7.14 KPI

| KPI | Obiettivo |
|---|---|
| Slew completati senza errore | ≥ 99% |
| Park completati | 100% |
| Meridian flip completati | ≥ 98% |
| Errori pulse guide | 0 per sessione |
| RMS totale | Compatibile con il campionamento |

## 7.15 Troubleshooting

### Montatura non connessa

- verificare alimentazione;
- verificare USB e porta COM;
- chiudere software concorrenti;
- avviare CPWI prima di N.I.N.A. e PHD2;
- controllare driver e firmware.

### Puntamento impreciso

- verificare ora, sito e fuso;
- controllare posizione iniziale;
- eseguire plate solving;
- verificare modello CPWI;
- controllare allineamento polare.

### Oscillazioni RA/DEC

- verificare seeing e vento;
- controllare bilanciamento e cavi;
- analizzare aggressività PHD2;
- verificare backlash e giochi;
- controllare serraggi e contrappesi.

### Meridian flip fallito

- arrestare la sequenza;
- verificare la posizione fisica;
- controllare limiti CPWI e impostazioni N.I.N.A.;
- parcheggiare se possibile;
- non riprendere senza plate solving e test guida.

## 7.16 FMEA sintetica

| Modo di guasto | Effetto | Gravità | Mitigazione |
|---|---|---:|---|
| Connessione USB persa | Stop guida/controllo | Alta | Cavo stabile, power management off |
| Park errato | Rischio collisione tetto | Critica | Verifica software e fisica |
| Flip fallito | Rischio collisione e perdita sessione | Critica | Limiti e recovery dedicato |
| Bilanciamento errato | Guida scadente e sovraccarico | Media/Alta | Checklist per ogni setup |
| Coordinate/ora errate | Puntamento e limiti errati | Alta | Sincronizzazione automatica |

## 7.17 Manutenzione

### Mensile

- controllo contrappesi, morsetti e cavi;
- test Park/Unpark;
- verifica errori nei log;
- controllo del bilanciamento dopo cambi setup.

### Semestrale

- verifica giochi percepibili;
- controllo connettori e alimentazione;
- analisi periodica PHD2;
- verifica limiti di sicurezza.

### Annuale

- verifica allineamento polare;
- revisione bulloneria della colonna;
- aggiornamento firmware solo dopo backup e test;
- collaudo completo con entrambi i telescopi.

## 7.18 Dati da validare

- numero di serie e versioni firmware;
- configurazione CPWI completa;
- coordinate esatte del sito nel sistema;
- posizione Park e immagini di riferimento;
- limiti meccanici/software;
- stato PEC;
- valori tipici RMS e backlash.
