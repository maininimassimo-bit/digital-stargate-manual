# Riepilogo homepage: coerenza e aggiornamento — 16 ottobre 2026

> Rettifica18 ottobre2026: conteggi, ultima sessione e misure citati qui descrivono lo stato storico precedente alla [riconciliazione per finestra manifest](HANDOVER_2026-10-18-CATALOG-NIGHT-RECONCILIATION.md). Il RAW è preservato; usare i derivati riconciliati per lo stato corrente.

## Diagnosi e significato dei dati

Il badge «Roadmap 13/10/2026 · dati scientifici 16/10/2026» accostava due date diverse senza chiarire che la seconda era la generazione della projection, non la notte acquisita. Roadmap aggiornata il 13 ottobre, package BKL-051 e avanzamento 90% sono coerenti con roadmap-source.json. L’ultima acquisizione scientifica è NGC281 del 14–15 ottobre; latest-observation.json è stato rigenerato il 16 ottobre. Non si cambia alcuna di queste date per far apparire nuove le sorgenti.

Il catalogo verificato contiene 25 registrazioni, 22 con LIGHT avviate o completate. Tre hanno entrambi i contatori a zero: 10–11 agosto, 26–27 agosto, 15–16 ottobre. Restano nel catalogo come evidenza storica. Il conteggio dei target esclude UNKNOWN e gli altri segnaposto: tre target identificati (M27, NGC281, LDN1320). Totali pubblicati invariati: 153,33 ore e 920 LIGHT completate.

## Contratto di presentazione

La scheda distingue «sessioni con LIGHT», registrazioni complessive e registrazioni senza LIGHT. Basta un contatore positivo (avviate oppure completate) per includere un’acquisizione: una posa fallita non scompare. Contatori mancanti non diventano zero: la classificazione è non determinabile; i totali con valori mancanti sono esplicitamente parziali. Booleani, stringhe, negativi e contatori frazionari non sono conteggi validi. Le registrazioni senza LIGHT non vengono cancellate o riscritte.

La data roadmap è separata dalla data/notte di acquisizione e dall’aggiornamento dei dati. La notte deriva dall’identità della sessione; l’istante generated_at è visualizzato nel fuso Europe/Rome. Date mancanti non diventano 1970. Il collegamento alla sessione richiede un’identità latest presente nel catalogo; incoerenze o errori rimuovono i valori presentati come correnti e riportano il collegamento al catalogo.

Il consumer homepage-effects.js rilegge le tre projection con cache no-store ogni 60 secondi a pagina visibile, al ritorno sulla pagina e con «Aggiorna riepilogo». Una richiesta in corso impedisce sovrapposizioni; timeout condiviso 12 secondi, protezione dei nodi rimossi dalla navigazione e inizializzazione idempotente. Gli aggiornamenti avvengono solo con le tre sorgenti ricevute. Il polling della homepage non modifica repository, schedulatore EAGLE, workflow scientifici o dati di acquisizione. La pubblicazione delle projection continua a dipendere dai workflow di generazione e deploy esistenti; non è telemetria live dell’osservatorio.

## Verifiche, rilascio e rollback

Test browser isolato test-home-snapshot.cjs: conteggi scientifici/tecnici/incerti, posa fallita, target segnaposto, date distinte e mancanti, refresh automatico/manuale/visibilità, totali parziali, errore HTTP, recupero e contatori invalidi. Integrato nel workflow Immersive portal validation. Test del contratto di rigenerazione homepage aggiornato con i nuovi marker. Build MkDocs strict e suite browser desktop/mobile verificano la presentazione reale; ARB indipendente, poi Release Quality sull’exact HEAD, CI e postmerge/Pages attestati nella PR.

Authority e baseline roadmap non cambiano. RAW, report, history e projection JSON restano byte invariati. Rollback: revert coordinato del consumer, markup, stile, marker del generatore e test; nessuna migrazione dati necessaria.
