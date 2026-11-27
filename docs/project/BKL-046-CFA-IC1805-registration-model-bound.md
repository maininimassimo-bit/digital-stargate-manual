# BKL-046 · Limite della selezione tra campo affine e quadratico su IC 1805

L’analisi riusa i 2.070 residui appaiati già misurati su stelle di regioni escluse dal fit, in 38 pose RAW Bayer di IC 1805. Verifica l’identità del riscontro e ricalcola il P90 pubblicato per entrambe le predizioni a ogni posa. Per stimare il miglior esito ottenibile soltanto con queste due predizioni, prende per ciascuna associazione il minore dei due residui osservati. È un limite ottimistico calcolato a posteriori.

| Predizione | P90 complessivo (pixel nativi) |
| --- | ---: |
| Affine robusta | 0,463 |
| Quadratica robusta | 0,466 |
| Minimo a posteriori per associazione | 0,427 |

Anche usando questo minimo, nessuna posa raggiunge il P90 di 0,30 pixel. La posa migliore resta a 0,307 pixel e 416 associazioni su 2.070 restano sopra soglia. Tra le 66 stelle osservate in almeno 19 pose, 11 mantengono un residuo mediano sopra soglia. Togliendo a turno sei pose consecutive nella sequenza esaminata, la differenza P90 complessiva quadratico meno affine varia da −0,007 a +0,011 pixel. Il confronto resta descrittivo perché le stelle e le pose contribuiscono a misure dipendenti.

Una selezione tra questi due campi, a parità di centroidi e associazioni, non basta per qualificare la registrazione di IC 1805. Per distinguere il contributo dei centroidi da quello del modello geometrico serve una stima indipendente della misura stellare. Restano aperte la validazione CFA alla stessa scala in PixInsight e la chiusura scientifica dell’asse.

Riscontro originale SHA-256 `0b46f893cf58fd7476a57e03911569f9172285aa7d4c1aef1dd26a85304ddf3a`. Due riesecuzioni coincidono con SHA-256 `5bc9ee8a095d486d9f0d52c0ae9575706bc05491cb53756465cb821e0d7d5cef`. Nessun avvio nativo.
