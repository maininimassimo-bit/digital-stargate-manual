# BKL-051 — annullamento e recovery durante le misure

BKL-051 resta OPEN e la scienza NOT_VALIDATED. Questo incremento riconcilia la quinta sessione singola autorizzata; è candidato ai gate del proprio commit. PR #525 precedente rilasciata sul merge `d370b6ff21c4dbf0e41320efd6585926b09e7876`: ARB poi RQ senza finding, 15 workflow post-merge SUCCESS e sette endpoint Pages verificati. Queste ricevute non attestano il presente incremento.

## Due casi nuovi, esplicitamente selezionati

La quarta OAT non aveva dimostrato annullamento durante il nativo né recovery prima del terminale. Entrambi i tentativi precedenti restano conservati. La quinta proposta autorizza soltanto due nuovi job sintetici e due istanze PixInsight, con binding e piani distinti, senza selezione automatica o replay.

Fixture numeriche nuove 2048×2048 Float64, apertura 256 pixel e anello 2–3 volte il raggio. Le 1024 posizioni quasi coincidenti forniscono carico tecnico, non osservazioni indipendenti. Nessuna fotografia, immagine generativa o modifica al kernel di produzione; durata non assunta a priori. Preflight offline verificato prima dell'autorizzazione; lettura ed esecuzione native poi osservate nella sessione.

| Caso | Evidenza osservata | Esito e limite |
|---|---|---|
| OWNER_CANCEL | Prima misura e 118 file di misura osservati senza terminale. Owner richiede personalmente annullamento dal portale mentre il nativo esegue; cloud → supervisore → marker locale → punto sicuro | Terminale nativo e job CANCELLED dopo 292 misure, ACK confermato, checkpoint conservato, handle proprio chiuso. Prova sintetica integrata superata; non una fotografia scientificamente validata |
| NATIVE_RECOVERY | Una sola mancata osservazione locale iniettata dopo la prima misura, con started.json presente e terminale assente | Nativo CANCELLED al punto sicuro dopo 13 misure; supervisore e job RECOVERY_REQUIRED, ACK della recovery confermato. Quiescenza verificata; Owner consulta dossier e registra personalmente dichiarazione sul digest esatto. Non interruzione naturale della rete |

La dichiarazione non resetta il job, non attesta un risultato scientifico e non riavvia il tentativo. Recovery resta RECOVERY_REQUIRED immutabile con chiusura dichiarata. Nessuna seconda POST terminale o rilancio implicito.

## Conservazione e verifica indipendente

Entrambi i processi dedicati sono assenti dopo chiusura del solo handle posseduto. Conservati terminali, tutte le 292/13 righe, parametri, Console, manifest di runtime, journal/outbox, marker e checkpoint dei rami annullati. Verifica delle righe sul contratto nativo e confronto dei blocchi Float64: **4.194.304 campioni bitwise identici per ciascun input/checkpoint**. I dump History iniziale/corrente sono conservati; sulle fixture numeriche nuove risultano vuoti, coerentemente con misure in sola lettura. La traccia operativa e i parametri restano nei journal e nei file del run; nessuna History astronomica a monte attestata.

Il dossier di recovery contiene digest dei file conservati, identità esatta del tentativo e verifica indipendente del PID assente. La dichiarazione cloud coincide con dossier, binding, tentativo e postazione. Queste misure restano somme di campioni normalizzati: full variance e significatività non calcolate, nessuna scoperta o soglia accettata. Archivi genitori e dipendenze PixInsight installate restano esterni; non archivio autonomo completo.

## Limiti, consumo e ripristino

Sessione autorizzata massimo 40 minuti; durata reale **792,91 secondi**. Due job/avvii; **66 richieste worker** entro 300 e **18 operazioni applicative Owner** entro 20, oltre **18 OPTIONS HTTP 204**. Accesso Owner già aperto, letture autenticate osservate; nessuna nuova prova del secondo account. Nessuna build o nuovo account. L'audit HTTP iniziale cercava il percorso recovery sbagliato: errore conservato; versione corretta verifica l'esatto endpoint `close-recovery`, senza cambiare servizio o prove.

Controller concluso. Verifica finale indipendente PASS: P6 al 100%, configurazione transient corrente assente, esatto permesso condizionale temporaneo assente, entrambi i PID dedicati assenti. Job e dichiarazioni conservati; stato modificato legittimamente, non dichiarato invariato. Revisioni storiche restano conservate. Le cinque autorizzazioni OAT sono consumate; nessuna credenziale o sessione riutilizzabile autorizzata.

## Residui obbligatori

| Area | Stato verificato | Residuo |
|---|---|---|
| Cancellazione integrata | Owner/cloud/supervisore/nativo durante misure sintetiche PASS | Regressioni finali e accettazione S5 |
| Recovery integrata | Fault locale prima del terminale, quiescenza e dichiarazione Owner PASS | Limiti dell'iniezione conservati; regressioni finali |
| Persistenza | Probe CAS GCS isolato e prove precedenti conservati | Concorrenza/retry dell'intero servizio e conservazione del backup sotto conflitto |
| Review/export | Valutazione e ricevuta minimizzata della quarta OAT verificati | Rapporto scientifico completo e regressioni/accettazione |
| Scienza | Diagnostica V5/V6 e kernel tecnico in sola lettura | Calibrazione, full variance/covarianze, timing/proper motion, pipeline multi-epoca, campione cieco, completezza/falsi positivi e policy Owner |
| Segnalazioni | Scope CBAT/TNS/VSX/MPC e draft approvati | Adattatori, tracklet, payload immutabile approvato, revoche/duplicati/ricevute e collaudo previsto |

S1/S2 aperte, S3 parziale, S4 incompleta, S5 non accettata. P6 Accepted con limiti del dossier; F4 lifecycle pending, F5 dopo F4, BKL-050 conclusiva. S10/Safety e collegamento C→F invariati. Nessuna fotografia pubblicata o segnalazione inviata. Rollback documentale: revert governato e rigenerazione delle proiezioni, preservando le evidenze private; non resetta job o arresta processi. Gate del presente commit: CI → ARB → RQ → merge sul commit atteso → post-merge e Pages.
