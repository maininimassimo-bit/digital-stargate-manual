# BKL-046 — Runner dei controlli ImageAnalysis

Il runner prepara due misure dello stesso insieme di quattro FITS, in ordine diretto e inverso, con un'istanza ImageAnalysis distinta per ordine. Usa la stessa struttura a quattro colonne che genera `BPP-helper.js` di WBPP 3.2.2. Disattiva la cache per la prova e mantiene le misure estese disattivate. Verifica byte e impronta di ogni FITS prima e dopo ogni esecuzione. [Codice candidato](ImageAnalysis-controls.jsh)

Le righe native sono ricondotte al percorso esatto del frame. Una riga mancante, duplicata, estranea o con misure non numeriche invalida la prova. La tabella finale conserva le misure per entrambi gli ordini e le differenze per campo, senza arrotondamento preventivo.

Il collaudo offline ha letto e verificato i quattro FITS effettivi. Ha usato un sostituto di ImageAnalysis per provocare otto errori e una variazione d'ordine di 0,5 pixel. Resta da integrare l'adattatore PJSR con la custodia dell'operazione e far revisionare il pacchetto prima di chiedere l'ammissione. [Riscontro](riscontro.json) · [Verificatore](verifica-runner.cjs)
