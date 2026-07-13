# Capitolo 1 – Introduzione

**Codice documento:** DSG-TM-001-01  
**Revisione:** 0.2 Draft  
**Classificazione:** Engineering Documentation  
**Stato:** In sviluppo

## 1.1 Scopo

Il presente manuale costituisce il riferimento tecnico e operativo dell’Osservatorio Astronomico Remoto **Digital StarGate**, installato a Manciano (GR) presso l’Agriturismo La Svolta.

Il documento descrive l’architettura generale dell’impianto, i sottosistemi hardware e software, le procedure di conduzione, le modalità di accesso remoto, i controlli di sicurezza, le attività di manutenzione e le procedure di ripristino in caso di anomalia.

Il manuale è concepito come **fonte unica di verità** per la configurazione dell’osservatorio. Le informazioni operative devono pertanto essere mantenute coerenti con lo stato reale dell’impianto e aggiornate dopo ogni modifica significativa.

## 1.2 Obiettivi

Gli obiettivi del manuale sono:

- preservare il know-how tecnico maturato durante la progettazione e l’esercizio dell’osservatorio;
- rendere ripetibili e verificabili le procedure operative;
- ridurre la dipendenza dalla conoscenza individuale del progettista;
- supportare manutenzione preventiva, diagnostica e recovery;
- documentare le dipendenze tra meccanica, alimentazione, rete, controllo e software;
- facilitare l’introduzione di nuovi componenti senza perdita di tracciabilità;
- costituire una base per collaudi, audit tecnici e future evoluzioni.

## 1.3 Campo di applicazione

Il manuale si applica alla configurazione installata presso Digital StarGate e comprende, a titolo principale:

- struttura dell’osservatorio e tetto motorizzato;
- sensori di posizione e sicurezza;
- impianto elettrico e distribuzione delle alimentazioni;
- connettività Starlink e rete Teltonika RUT955;
- accesso remoto tramite VPN;
- computer di controllo PrimaLuceLab EAGLE3;
- montatura Celestron CGX-L;
- sistemi ottici Celestron C8 XLT e Sky-Watcher Quattro 200P;
- camere, filtri, fuocheggiatori e sistemi di guida;
- software N.I.N.A., PHD2, CPWI, ASCOM e strumenti ausiliari;
- automazione delle sessioni e gestione degli incidenti.

Sono escluse dal manuale le operazioni di riparazione interna dei dispositivi commerciali quando richiedono l’intervento del produttore o di un centro autorizzato.

## 1.4 Destinatari

Il documento è destinato a:

- proprietario e responsabile dell’osservatorio;
- operatori remoti autorizzati;
- tecnici incaricati della manutenzione;
- collaboratori coinvolti nell’acquisizione astronomica;
- eventuali futuri gestori dell’impianto.

La consultazione del manuale non sostituisce la formazione pratica, in particolare per le attività che coinvolgono movimentazioni meccaniche, alimentazioni elettriche o interventi locali in condizioni notturne.

## 1.5 Principi di sicurezza

La protezione delle persone e della strumentazione ha priorità rispetto alla continuità della sessione osservativa.

Le regole fondamentali sono:

1. non comandare movimenti quando lo stato meccanico non è noto;
2. non aprire o chiudere il tetto con sensori incoerenti;
3. non riprendere automaticamente una sessione dopo un evento critico senza verifica dello stato;
4. non esporre servizi di controllo direttamente su Internet;
5. non aggiornare software o firmware durante campagne osservative senza una procedura di rollback;
6. non intervenire su circuiti elettrici sotto tensione se non qualificati e autorizzati.

!!! warning "Sicurezza"
    Le procedure riportate nel manuale devono essere adattate allo stato reale dell’impianto. In caso di discordanza tra documentazione e osservazione diretta, prevale la condizione più prudente e l’attività deve essere sospesa.

## 1.6 Struttura documentale

Il manuale è organizzato in capitoli Markdown numerati. Ogni capitolo può includere:

- scopo e campo di applicazione;
- architettura e componenti;
- requisiti e parametri;
- procedure operative;
- verifiche e criteri di accettazione;
- manutenzione;
- troubleshooting;
- dati da validare.

Le principali codifiche sono:

| Elemento | Codifica | Esempio |
|---|---|---|
| Manuale | `DSG-TM-001` | DSG-TM-001 |
| Capitolo | `DSG-TM-001-XX` | DSG-TM-001-05 |
| Procedura | `DSG-PROC-XXX` | DSG-PROC-016 |
| Checklist | `DSG-CHK-XXX` | DSG-CHK-004 |
| Configurazione | `DSG-CONF-XXX` | DSG-CONF-003 |
| Incidente | `DSG-INC-XXX` | DSG-INC-012 |
| Manutenzione | `DSG-MNT-XXX` | DSG-MNT-007 |
| Test | `DSG-TST-XXX` | DSG-TST-005 |

## 1.7 Gestione dei dati non confermati

I valori non ancora verificati direttamente sull’impianto devono essere marcati nel seguente modo:

> **DA VALIDARE:** inserire il dato reale, la fonte e la data di verifica.

Non devono essere inseriti come definitivi indirizzi IP, credenziali, serial number, assorbimenti, limiti meccanici, soglie meteo o versioni software non verificati.

Le informazioni sensibili, come credenziali e chiavi VPN, non devono essere archiviate nel repository. Il manuale deve indicare soltanto dove sono custodite e chi è autorizzato ad accedervi.

## 1.8 Gestione delle revisioni

Ogni modifica sostanziale deve includere:

1. aggiornamento del file interessato;
2. modifica del registro revisioni;
3. commit Git con messaggio descrittivo;
4. eventuale rigenerazione di Word e sito MkDocs;
5. verifica dei collegamenti e della numerazione.

Esempio di commit:

```text
git commit -m "Aggiorna procedura di failover RUT955"
```

## 1.9 Criteri di qualità

Un capitolo è considerato sufficientemente maturo quando:

- non contiene contraddizioni con altri capitoli;
- distingue dati confermati e dati da validare;
- descrive chiaramente prerequisiti, azioni e criteri di accettazione;
- evita istruzioni pericolose o non verificabili;
- utilizza terminologia coerente;
- è leggibile sia nella versione web sia nel documento Word.

## 1.10 Riferimenti interni

- [Capitolo 2 – Architettura generale](02-architettura-generale.md)
- [Capitolo 16 – Avvio dell’osservatorio](16-sop-avvio.md)
- [Capitolo 18 – Emergenze e recovery](18-emergenze-recovery.md)
- [Dati da validare](../appendices/dati-da-validare.md)
- [Registro revisioni](../appendices/registro-revisioni.md)
