# Capitolo 26 – Monitoraggio meteo e sicurezza ambientale

**Codice documento:** DSG-TM-001-26  
**Revisione:** 0.1 Draft

## 26.1 Scopo

Questo capitolo definisce i principi, i segnali e le procedure con cui Digital StarGate valuta la compatibilità delle condizioni ambientali con l'apertura e la prosecuzione di una sessione osservativa.

La funzione meteo deve essere considerata un sistema di sicurezza: in presenza di dati assenti, incoerenti o non affidabili, l'osservatorio deve assumere lo stato più prudente.

## 26.2 Parametri ambientali

I parametri da monitorare comprendono, dove disponibili:

- pioggia o precipitazioni;
- umidità relativa;
- temperatura ambiente;
- punto di rugiada e relativo margine;
- velocità e raffiche di vento;
- copertura nuvolosa;
- luminosità del cielo;
- presenza di condensa;
- qualità o disponibilità del dato meteo.

## 26.3 Classificazione dello stato

| Stato | Significato | Azione |
|---|---|---|
| SAFE | condizioni entro le soglie | apertura e osservazione consentite |
| WARNING | parametro vicino alla soglia | monitoraggio rafforzato |
| UNSAFE | soglia superata | chiusura controllata |
| UNKNOWN | dato assente o incoerente | trattare come UNSAFE, salvo procedura locale controllata |

## 26.4 Principi di sicurezza

1. La pioggia ha priorità massima.
2. Il vento deve essere valutato sia come media sia come raffica.
3. L'umidità deve essere correlata al punto di rugiada.
4. Un singolo sensore non affidabile non deve produrre un falso SAFE.
5. Lo stato meteo deve essere persistente per un intervallo configurato prima di autorizzare la riapertura.
6. La riapertura automatica, se prevista, deve richiedere una finestra stabile e priva di allarmi.

## 26.5 Logica decisionale

```text
DATI DISPONIBILI?
  |-- NO  --> UNKNOWN --> CHIUSURA / BLOCCO APERTURA
  |
  |-- SI
       |
       |-- PIOGGIA? -------- SI --> UNSAFE
       |-- VENTO OLTRE SOGLIA? SI --> UNSAFE
       |-- DEW MARGIN CRITICO?  SI --> WARNING/UNSAFE
       |-- SENSORI COERENTI?    NO --> UNKNOWN
       |-- TUTTO REGOLARE?      SI --> SAFE
```

## 26.6 Procedura DSG-PROC-026-01 – Valutazione pre-apertura

1. Acquisire gli ultimi dati disponibili.
2. Verificare timestamp e freschezza delle misure.
3. Controllare lo stato del sensore pioggia.
4. Verificare vento medio e raffiche.
5. Calcolare o leggere il margine rispetto al punto di rugiada.
6. Verificare la coerenza tra sensori e osservazione AllSky.
7. Classificare lo stato SAFE, WARNING, UNSAFE o UNKNOWN.
8. Consentire l'apertura solo con stato SAFE.
9. Registrare valori e decisione nel log della sessione.

## 26.7 Procedura DSG-PROC-026-02 – Transizione a UNSAFE

1. Sospendere l'avvio di nuove esposizioni.
2. Terminare o annullare l'esposizione in corso secondo la gravità.
3. Arrestare la guida.
4. Parcheggiare la montatura.
5. Chiudere la copertura.
6. Verificare CLOSED.
7. Salvare i dati meteo e i log.
8. Notificare l'operatore.

In caso di pioggia confermata, la procedura deve privilegiare la rapidità della messa in sicurezza.

## 26.8 Isteresi e riapertura

Per evitare cicli ripetuti di apertura e chiusura:

- usare soglie differenziate per passaggio SAFE→UNSAFE e UNSAFE→SAFE;
- richiedere una durata minima di stabilità;
- impedire riaperture dopo pioggia per un intervallo prudenziale;
- richiedere conferma manuale dopo eventi severi o dati incoerenti.

## 26.9 Guasti e anomalie

| Evento | Classificazione | Azione |
|---|---|---|
| dato non aggiornato | UNKNOWN | blocco apertura / chiusura |
| sensore pioggia non disponibile | CRITICAL | trattare come UNSAFE |
| valori impossibili | UNKNOWN | verificare sensore e cablaggio |
| AllSky non raggiungibile | WARNING | usare altri sensori, senza ridurre le protezioni |
| vento oscillante vicino alla soglia | WARNING | applicare isteresi e monitoraggio continuo |

## 26.10 Manutenzione

### Mensile

- verificare timestamp e continuità dei dati;
- controllare log e allarmi;
- pulire sensori esposti secondo le istruzioni del produttore;
- confrontare i dati con una sorgente indipendente.

### Trimestrale

- simulare una transizione a UNSAFE;
- verificare la corretta propagazione dell'allarme;
- collaudare la chiusura automatica.

### Annuale

- verificare taratura e stato fisico dei sensori;
- riesaminare le soglie sulla base degli incidenti e delle condizioni locali.

## 26.11 Checklist meteo

- [ ] dati aggiornati;
- [ ] sensore pioggia operativo;
- [ ] vento entro soglia;
- [ ] margine di rugiada accettabile;
- [ ] stato AllSky disponibile;
- [ ] nessuna incoerenza;
- [ ] stato finale classificato;
- [ ] decisione registrata.

## 26.12 Dati da validare

> **DA VALIDARE:** sensori meteo effettivamente installati e relativo software di integrazione.

> **DA VALIDARE:** soglie operative di vento, umidità e margine di rugiada.

> **DA VALIDARE:** durata minima dello stato SAFE prima di una eventuale riapertura.
