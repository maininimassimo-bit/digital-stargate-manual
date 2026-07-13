# Capitolo 3 – Struttura della cupola e copertura mobile

**Codice documento:** DSG-TM-001-03  
**Revisione:** 0.2 Draft  
**Classificazione:** Engineering Documentation

## 3.1 Scopo

Il capitolo descrive la struttura di protezione dell’osservatorio, il sistema di movimentazione della copertura e i sensori utilizzati per conoscere gli stati di apertura, chiusura e sicurezza.

La copertura costituisce un sottosistema critico. Un errore di movimentazione può esporre la strumentazione agli agenti atmosferici o causare interferenze meccaniche con montatura, telescopio e cablaggi.

## 3.2 Funzioni principali

Il sistema deve:

- proteggere la strumentazione quando l’osservatorio non è operativo;
- consentire l’apertura e la chiusura locale o remota;
- fornire una conferma indipendente dello stato meccanico;
- interrompere il movimento al raggiungimento dei finecorsa;
- impedire comandi incompatibili o potenzialmente pericolosi;
- consentire una procedura di recovery in caso di blocco.

## 3.3 Componenti

| ID | Componente | Funzione | Criticità |
|---|---|---|---|
| DOME-01 | Struttura portante | Sostegno della copertura e protezione dell’area | Alta |
| DOME-02 | Copertura mobile | Apertura della linea di vista verso il cielo | Critica |
| DOME-03 | Guide di scorrimento | Vincolo e direzione del movimento | Alta |
| DOME-04 | Motorizzazione | Generazione del movimento | Critica |
| DOME-05 | Trasmissione | Trasferimento della forza alle parti mobili | Alta |
| DOME-06 | Sensore OPEN | Conferma apertura completa | Critica |
| DOME-07 | Sensore CLOSED | Conferma chiusura completa | Critica |
| DOME-08 | Segnale SAFE | Consenso alla movimentazione o stato sicuro | Critica |
| DOME-09 | Centralina/relè | Comando e arresto del motore | Critica |
| DOME-10 | Arresto locale | Interruzione manuale del movimento | Critica |

> **DA VALIDARE:** produttore, modello e caratteristiche della motorizzazione e della centralina.

## 3.4 Stati dei sensori

Le combinazioni ammesse devono essere definite in base alla logica elettrica reale.

Matrice concettuale:

| Stato fisico | OPEN | CLOSED | SAFE | Interpretazione |
|---|---:|---:|---:|---|
| Completamente chiuso | 0 | 1 | da validare | protetto |
| In apertura/chiusura | 0 | 0 | da validare | movimento o posizione intermedia |
| Completamente aperto | 1 | 0 | da validare | osservazione possibile |
| Incoerente | 1 | 1 | qualsiasi | anomalia critica |

!!! danger "Stato incoerente"
    La contemporanea attivazione di OPEN e CLOSED deve essere trattata come anomalia. Nessun ulteriore movimento deve essere comandato finché il guasto non è stato diagnosticato.

## 3.5 Interblocco con la montatura

Prima di chiudere la copertura deve essere verificato che la montatura si trovi nella posizione di sicurezza prevista.

La verifica può comprendere:

- stato `Parked` esposto dal driver ASCOM;
- posizione angolare compatibile con il profilo della copertura;
- assenza di movimento della montatura;
- assenza di cavi o accessori fuori sagoma;
- conferma visiva tramite telecamera, quando disponibile.

> **DA VALIDARE:** descrivere la posizione Park reale e le distanze minime tra ottica, montatura e copertura.

## 3.6 Procedura DSG-PROC-003-01 – Apertura controllata

### Prerequisiti

- alimentazione stabile;
- centralina raggiungibile;
- montatura in posizione sicura;
- nessun intervento locale in corso;
- sensori in stato coerente;
- assenza di condizioni ambientali incompatibili;
- operatore o automazione autorizzati.

### Sequenza

1. leggere e registrare lo stato iniziale dei sensori;
2. verificare che `CLOSED` sia attivo e `OPEN` non attivo;
3. verificare il consenso `SAFE` secondo la logica reale;
4. inviare il comando di apertura;
5. monitorare il cambio di stato di `CLOSED`;
6. verificare la progressione del movimento entro il timeout previsto;
7. arrestare il comando al raggiungimento di `OPEN`;
8. verificare che `OPEN` sia stabile e `CLOSED` non attivo;
9. aggiornare lo stato dell’osservatorio a `OPEN`;
10. registrare durata, esito e anomalie.

### Criteri di accettazione

- finecorsa OPEN raggiunto;
- nessun rumore o assorbimento anomalo;
- nessun ostacolo rilevato;
- sensori coerenti;
- movimento completato entro il tempo atteso.

> **DA VALIDARE:** timeout nominale di apertura e tolleranza ammessa.

## 3.7 Procedura DSG-PROC-003-02 – Chiusura controllata

### Prerequisiti

- esposizioni terminate o interrotte;
- guida arrestata;
- montatura parcheggiata;
- posizione meccanica verificata;
- area di scorrimento libera;
- sensori coerenti.

### Sequenza

1. confermare lo stato Park della montatura;
2. verificare l’assenza di elementi fuori sagoma;
3. leggere lo stato dei sensori;
4. inviare il comando di chiusura;
5. monitorare la disattivazione di `OPEN`;
6. verificare la progressione del movimento;
7. arrestare al raggiungimento di `CLOSED`;
8. verificare la stabilità del segnale `CLOSED`;
9. aggiornare lo stato dell’osservatorio a `READY/SAFE`;
10. registrare l’esito.

### Divieti

- non chiudere se la posizione della montatura è sconosciuta;
- non ripetere ciclicamente il comando in presenza di blocco meccanico;
- non bypassare i finecorsa durante l’esercizio ordinario;
- non lasciare la copertura in posizione intermedia senza una valutazione del rischio.

## 3.8 Arresto di emergenza

In caso di rumore anomalo, ostacolo, movimento irregolare o sensori incoerenti:

1. interrompere immediatamente il comando;
2. togliere alimentazione al motore se necessario e sicuro;
3. non invertire automaticamente il movimento;
4. verificare visivamente la struttura;
5. identificare la posizione della montatura;
6. registrare l’incidente;
7. eseguire un test controllato solo dopo la rimozione della causa.

## 3.9 Guasti tipici

### La copertura non si muove

Possibili cause:

- assenza di alimentazione;
- centralina non operativa;
- consenso SAFE assente;
- finecorsa bloccato;
- protezione elettrica intervenuta;
- motore o trasmissione bloccati;
- comando remoto non ricevuto.

### Il motore gira ma la copertura non avanza

Possibili cause:

- trasmissione disaccoppiata;
- elemento meccanico danneggiato;
- slittamento;
- ostacolo sulle guide.

### Movimento lento o irregolare

Possibili cause:

- guide sporche o disallineate;
- attrito anomalo;
- tensione insufficiente;
- usura meccanica;
- carico non uniforme.

### Finecorsa non rilevato

Azioni:

- interrompere il movimento;
- verificare cablaggio e alimentazione del sensore;
- controllare il posizionamento meccanico;
- verificare il segnale alla centralina;
- non riprendere l’automazione fino alla risoluzione.

## 3.10 Manutenzione preventiva

### Prima di una sessione importante

- controllo visivo dell’area di scorrimento;
- verifica dello stato sensori;
- test di un ciclo completo in condizioni controllate;
- verifica della posizione Park.

### Mensile

- pulizia delle guide;
- ispezione dei cablaggi mobili;
- verifica dei fissaggi dei sensori;
- controllo dei tempi di apertura e chiusura;
- verifica di rumori e vibrazioni.

### Semestrale

- controllo della bulloneria;
- verifica dell’allineamento delle guide;
- ispezione della trasmissione;
- controllo della protezione da acqua e polvere;
- prova dell’arresto locale.

### Annuale

- revisione completa della movimentazione;
- verifica delle protezioni elettriche;
- controllo di corrosione e deformazioni;
- aggiornamento della matrice dei rischi.

La lubrificazione deve essere eseguita solo con prodotti compatibili con i materiali e le condizioni ambientali.

## 3.11 Checklist DSG-CHK-003 – Verifica della copertura

- [ ] guide libere;
- [ ] cablaggi integri;
- [ ] sensore OPEN funzionante;
- [ ] sensore CLOSED funzionante;
- [ ] segnale SAFE coerente;
- [ ] montatura in Park;
- [ ] nessun ostacolo;
- [ ] motore senza rumori anomali;
- [ ] tempi di movimento entro la tolleranza;
- [ ] esito registrato.

## 3.12 Dati da validare

> **DA VALIDARE:** schema elettrico della centralina e modalità di comando dei relè.

> **DA VALIDARE:** polarità e logica attiva dei sensori OPEN, CLOSED e SAFE.

> **DA VALIDARE:** tempi nominali di apertura e chiusura.

> **DA VALIDARE:** procedura manuale di sblocco o movimentazione in assenza di alimentazione.

> **DA VALIDARE:** posizione e caratteristiche dell’arresto di emergenza locale.

## 3.13 Riferimenti interni

- [Capitolo 2 – Architettura generale](02-architettura-generale.md)
- [Capitolo 4 – Impianto elettrico](04-impianto-elettrico.md)
- [Capitolo 16 – SOP di avvio](16-sop-avvio.md)
- [Capitolo 18 – Emergenze e recovery](18-emergenze-recovery.md)
