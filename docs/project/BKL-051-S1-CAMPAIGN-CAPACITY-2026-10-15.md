# BKL-051 — capacità esplicita del registro candidato

Stato: candidato locale, non attivato sul servizio. Milestone **OPEN / NOT_VALIDATED**, stima indicativa 37%, zero controlli scientifici qualificati.

## Problema e comportamento

Le 59 triplette candidate richiedono 177 riferimenti di input distinti. La coda storica ammette 32 binding, 32 job e 1 MiB: non può contenere questo campione. Le sequenze candidate non sono 59 controlli nulli indipendenti qualificati.

Il profilo trusted `CANDIDATE_59X3_V1`, selezionato esclusivamente dalla configurazione `DSG_TRANSIENT_CAPACITY_PROFILE`, ammette al massimo 512 binding, 512 job e 8 MiB di stato serializzato. Richiede un riferimento esplicito a un registro isolato. Nessuna richiesta browser sceglie il profilo. Senza profilo la coda conserva i limiti storici; il profilo non attiva un servizio disabilitato.

Il registro esteso contiene un marcatore di profilo. Adozione di registri storici, profili incompatibili e downgrade sono rifiutati senza riscrittura o migrazione. Anche letture e scritture serializzate sono limitate. CAS, backup immutabili, identità worker, riserva monouso, recovery e idempotenza restano applicabili.

Il browser accetta viste minimizzate fino a 512 elementi e 8 MiB, controllando sia dimensione dichiarata sia byte effettivi. Questo limite di lettura vale anche quando il backend mantiene il profilo storico. Non autorizza nuovi job, polling, replay o validazione scientifica.

## Evidenza locale e limiti

La prova backend crea 177 cicli sintetici distinti, li completa, registra una revisione e li rilegge dopo riapertura. Un diverso fixture di 512 righe con 32 revisioni per riga verifica la forma massima sperimentata; non rappresenta 512 esecuzioni. Il modello dimensionale misura circa 1,77 MB di stato per 177 righe con 32 revisioni e 5,12 MB per 512. Non è una dimostrazione universale: i limiti sui byte restano vincolanti.

La verifica browser locale usa markup, CSS e JavaScript del prodotto con identità fittizia e risposte intercettate; CSP impedisce connessioni esterne. Sono state lette 512 e 177 schede, verificati finestra stretta, identificativi lunghi, temi chiaro/scuro e aggiornamento con Invio, con zero POST. Non verifica OAuth reale o servizio cloud. Suite complete, revisione ARB poi RQ e CI sul commit esatto sono gate distinti prima del rilascio; postmerge e pubblicazione richiedono nuove verifiche.

## Attivazione e conservazione

Nessuna build, revisione cloud, modifica IAM, nuova risorsa o spesa è autorizzata da questo incremento. Le precedenti prove sono concluse e ripristinate. Un futuro avvio richiede proposta concreta con immagine, configurazione, stato isolato, permessi, job, richieste, finestra, ripristino e costi approvati. La stima deve includere tutti i backup progressivi e le versioni degli oggetti, non soltanto l'ultimo stato. Nessuna cancellazione o replay è previsto.

Rollback del codice tramite revert, conservando stati e ricevute; un registro esteso non viene aperto automaticamente dalla versione storica. Questo incremento contribuisce a R09, senza chiudere il collaudo operativo e scientifico della milestone.
