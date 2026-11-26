# BKL-046 · Controllo PJSR della primitiva bilineare

Il corpo JavaScript accetta immagini distinte da 64 × 64 pixel e cinque fasi congelate. Imposta la modalità bilineare, legge mediante `Image.interpolate` e scrive il risultato nella regione interna prevista dal fascicolo. Il chiamante possiede le immagini e tutte le operazioni di I/O. Il file contiene soltanto la funzione, senza punto di avvio automatico. Gli script installati citati in `riferimenti-runtime.json` documentano l'uso della primitiva e della proprietà di interpolazione. [Costanti PJSR](https://gitlab.com/pixinsight/PJSR/-/blob/master/include/pjsr/Interpolation.jsh)

Il collaudo Node usa i 17 FITS fissati. Conferma 85 confronti contro il riferimento aritmetico, i tre rifiuti preliminari e la restituzione della modalità iniziale dopo un errore di lettura, scrittura o campione. Se falliscono sia la lettura sia il ripristino della modalità, conserva entrambi gli errori e segnala che il ripristino è fallito. Il chiamante deve scartare qualsiasi uscita parziale in caso di errore.

La simulazione esercita il corpo e i suoi limiti. L'ABI PJSR, i risultati del motore reale e il processo DynamicAlignment restano da verificare. Il controllo della primitiva serve a interpretare un futuro confronto di processo. Nessun avvio, modifica agli script installati o richiesta di ammissione. [Fascicolo numerico](../bkl046-asi2600mc-native-bilinear-reference-v1/README.md)

Replica con `node collaudo.cjs controllo-bilineare.js <directory-ingressi> protocollo.json riscontro-replica.json`. La directory degli ingressi proviene dall'archivio fissato nel protocollo.
