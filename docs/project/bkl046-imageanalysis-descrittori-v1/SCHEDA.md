# BKL-046 — Contratto dei descrittori ImageAnalysis in WBPP 3.2.2

In PixInsight 1.9.6 build 1719, WBPP configura `ImageAnalysis` in modalità Measure, con proseguimento in caso di errore, cache attiva e misure estese disattivate. Associa le righe restituite ai frame usando il percorso. L'esecuzione offline ha chiamato i metodi esatti degli script installati con un sostituto del modulo nativo e dati inventati. [Riscontro riproducibile](riscontro.json)

| Aspetto | Comportamento osservato nel wrapper | Conseguenza per la base di conoscenza |
| --- | --- | --- |
| Dispersione e rumore | Il campo `mad` del descrittore contiene `measurementSigma`. Il rumore viene copiato da `measurementNoise` e non rientra nel controllo di finitezza del descrittore. Nel collaudo un valore `NaN` per il solo rumore passa il controllo. | Conservare il nome originale della colonna. Validare separatamente la finitezza del rumore se lo si usa. |
| Cache | La chiave include `CACHE_VERSION` e `ImageAnalysis.toSource()`. A pari configurazione e percorso, WBPP confronta solo la data di ultima modifica. Nella simulazione i dati cambiati con data invariata lasciano in uso il descrittore in cache. | Registrare anche digest e dimensioni del frame quando si congela una misura riproducibile. Una cache del wrapper non prova l'identità dei byte. |
| Conteggi | Con successo globale e nessuna riga per un frame, il frame viene marcato come fallito mentre `nFailed` può restare zero. Righe sintetiche duplicate per lo stesso percorso incrementano `nMeasured` più volte pur producendo un singolo descrittore finale. | Riconciliare uno per uno i frame richiesti, le righe restituite e gli esiti scritti. Usare i contatori del wrapper come diagnostica. |

La prova identifica il contratto di integrazione. Restano aperte la definizione nativa di `measurementSigma`, la provenienza del valore di rumore e la verifica su frame reali. L'impronta del DLL identifica il modulo installato. Nel collaudo il DLL è stato letto per il calcolo dell'impronta e il processo PixInsight è rimasto chiuso.

Riferimenti locali, con impronte registrate nel riscontro. `BPP-SubframeAnalyzer.js`, righe 395–620, e `BPP-ExecutionCache.js`, righe 76–86 e 213–243. [Verificatore offline](verifica-descrittori.cjs)
