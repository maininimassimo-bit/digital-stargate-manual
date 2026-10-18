# Catalogo: vista scientifica e pacchetti tecnici — 18 ottobre 2026

## Richiesta e contratto

L’Owner approva la separazione nella vista pubblica tra sessioni scientifiche e pacchetti tecnici. La riconciliazione precedente aveva identificato correttamente cinque pacchetti senza LIGHT, ma li mostrava insieme alle acquisizioni. Questo documento aggiorna esclusivamente il contratto di presentazione del precedente handover di riconciliazione.

La vista iniziale include soltanto record con `lightStarted > 0` oppure `lightCompleted > 0`. Una LIGHT avviata e fallita resta visibile anche con zero completamenti: la selezione non dipende dalla qualità, dal target identificato o dall’esito Analytics. Il checkbox accessibile **Mostra pacchetti tecnici**, inizialmente disattivato, aggiunge i pacchetti senza acquisizioni alla stessa ricerca. Anno, target e qualità continuano a combinarsi con la selezione; cercare un pacchetto tecnico richiede l’attivazione esplicita del checkbox. Reimposta azzera tutti i filtri e disattiva il checkbox. Refresh manuale, timer e ritorno della visibilità conservano la selezione corrente.

I KPI sono riferiti sempre all’intera popolazione delle acquisizioni scientifiche: sessioni con LIGHT, target identificati distinti, integrazione e validate/totale. Non cambiano con i filtri di ricerca né con l’inclusione dei pacchetti tecnici. Una nota indica quanti pacchetti senza acquisizioni sono consultabili con il filtro. La barra dei risultati distingue sessioni scientifiche da registrazioni comprensive dei pacchetti tecnici.

Alla baseline riconciliata: 22 sessioni con LIGHT, 5 pacchetti senza acquisizioni, 3 target identificati, 116,17 ore; 5/22 sessioni validate Analytics. L’ultima acquisizione resta il 16–17 ottobre. Questi numeri descrivono la baseline, non sono valori fissati nel consumer.

## Conservazione e confini

Nessuna cancellazione o modifica a RAW, manifest, ricevute, storico, report, proiezioni JSON o link di dettaglio. Il dataset completo mantiene 27 registrazioni; la selezione riguarda soltanto il catalogo pubblico. Il guard d’importazione esistente resta invariato: nessuna nuova LIGHT nella finestra manifest significa no-op per tutte le pubblicazioni scientifiche. Il pacchetto tecnico può restare come ricevuta di trasferimento. Nessuna modifica a EAGLE, Safety, authority o criteri di qualità. Le ricevute INVALID storiche restano esplicite.

## Verifica e rollback

Test browser sul markup effettivo: esclusione iniziale, inclusione esplicita, KPI scientifici invarianti, combinazione con qualità/ricerca, reset, acquisizione fallita visibile, refresh e recupero da errore. Verificare layout desktop/mobile, build strict, ARB indipendente poi Release Quality, CI sull’head finale e postmerge/Pages. Esiti e SHA nella PR di rilascio.

Rollback: revert unitario di consumer, controllo HTML, stile e documentazione di questo package. Nessun rollback dati necessario. Il contratto precedente resta recuperabile nella storia Git.
