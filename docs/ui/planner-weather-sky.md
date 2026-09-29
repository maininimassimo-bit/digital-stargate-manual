# Cielo illustrativo del Planner

Il riquadro della hero di Observation Planner sostituisce il precedente simbolo ◎ con tre immagini realistiche generate per il portale: Via Lattea serena, cielo nuvoloso e pioggia notturna. Rimane accanto alla scena 3D Celestial Atlas ed è visibile anche su mobile.

## Collegamento ai dati

`observation-planner-f9.js` passa la projection già verificata a `planner-weather-sky.mjs`, dopo il rendering del Planner. Nessun fetch aggiuntivo, provider, coordinata o dato sintetico entra nel percorso di produzione. Se il consumer fallisce, anche il riquadro viene azzerato.

La sintesi utilizza tutti e soli i campioni orari della `nightWindow` dichiarata, uguali a quelli del pannello «Previsione completa della notte». Non seleziona solo le ore astronomicamente buie. Richiede una serie ordinata, completa, senza duplicati, a passo orario, nuvolosità numerica 0–100% e precipitazioni numeriche non negative. Campioni mancanti, run oltre 18 ore, notte terminata o finestra non valida producono uno sfondo neutro con stato non disponibile.

La nuvolosità è la media aritmetica dei campioni equidistanti, come nella pagina. Per la sola scelta illustrativa: media ≤20% → sereno; media >20% → nuvoloso. Qualsiasi precipitazione positiva prevale e seleziona pioggia. La didascalia espone media nuvole, totale precipitazioni, numero di campioni con pioggia e intervallo Europe/Rome: l'immagine piovosa non implica precipitazioni per tutta la notte. La convenzione grafica non introduce né modifica soglie operative, ranking, semafori, readiness o Safety Authority.

La Via Lattea, le stelle, le colline e l'intensità della pioggia sono illustrative: non rappresentano una fotografia, coordinate stellari, fasi lunari o visibilità astronomica calcolata. La spiegazione è disponibile nel riquadro stesso.

## Asset e prestazioni

Tre asset locali in `docs/assets/images/planner-sky/`: `clear.webp` (128766 byte), `cloudy.webp` (36264 byte), `rain.webp` (44358 byte), 768×768 pixel. Generati con lo strumento imagegen integrato, poi ridimensionati e compressi per il web. Viene scaricata solo l'immagine selezionata. Nessun canvas aggiuntivo, loop di animazione, CDN o servizio AI al caricamento della pagina. Layout riservato per evitare salti; decodifica asincrona; testo disponibile anche se l'immagine fallisce.

Un timer invalida il riquadro al termine della notte o alla scadenza del run; il controllo viene ripetuto al ritorno alla scheda. Non viene mantenuta una rappresentazione meteo ormai scaduta. Il consumer F9 verifica la projection pubblicata ogni cinque minuti mentre la pagina è visibile e al ritorno alla scheda. Il riquadro viene aggiornato con la stessa projection verificata. Alla scadenza vengono rimossi anche ranking e pannelli correnti, senza prolungare artificialmente la freschezza.

## Verifica e manutenzione

`.github/scripts/test-immersive-planner-sky.cjs` verifica tre condizioni, soglia visiva, priorità pioggia, media e unità, singolo fetch, mobile, campioni mancanti/duplicati/invalidi, fonte indisponibile o stale, immagine assente e scadenza mentre la pagina resta aperta. La suite fa parte di Immersive portal validation; i provider esterni sono bloccati e le fixture non vengono pubblicate.

Per il rollback ripristinare il markup precedente e rimuovere l'import e le chiamate `sky` dal consumer F9. Nessuna migrazione dei dati è necessaria. Le evidenze di CI, revisione e pubblicazione sono registrate nella PR di rilascio.

## Continuità serale

La fonte viene controllata ogni ora al minuto 23 UTC. Stesso modello valido e stessa notte: nessun nuovo download GRIB e nessun timestamp rinnovato. Modello nuovo o notte nuova: normale acquisizione e pubblicazione. Nel Planner sono esposti orario del run e scadenza locale. I filtri selezionati vengono conservati negli aggiornamenti riusciti. Il polling visibile a cinque minuti e il ritorno alla scheda recuperano una nuova pubblicazione senza ricaricamento manuale. La scadenza a 18 ore dal run resta invariata; ritardi del provider o dello scheduler possono ancora produrre indisponibilità esplicita.
