# BKL-046 · Verificatore della rilettura GitHub

Il manifest di consegna identifica gli 80 contenitori v600 e la capsula di conoscenza v1.171. Il totale esatto è **81 asset e 27.582.310.714 byte**. Questa versione del verificatore controlla l'intero insieme in una release dedicata. Il manifest conserva le impronte degli inventari sorgente e di ogni asset.

Il programma controlla l'ID e la visibilità del repository, l'ID e il tag di una release pubblicata e l'insieme completo degli asset. Rileva nomi mancanti, extra o duplicati, ID riusati e metadati discordanti. Rilegge gli asset tramite i loro ID, verifica dimensione e SHA-256 e controlla nuovamente i metadati al termine. Verifica anche l'unico membro della capsula di conoscenza in streaming. [API GitHub degli asset di release](https://docs.github.com/en/rest/releases/assets)

Il collaudo offline ha respinto 16 casi. Il verificatore ha inoltre riletto la capsula v1.171 locale e confermato il JSON interno da 3.030.957.683 byte con la sua impronta registrata. La ricevuta attesta l'esito locale. Il riscontro remoto richiede gli ID effettivi e il riscaricamento di tutti gli asset, seguito dalla ricostruzione del corpus logico a partire dall'indice v600.

Il manifest conserva destinazione e perimetro come decisioni ancora aperte. La release di destinazione e i diritti di distribuzione restano da confermare. Il lavoro non ha creato release o caricato asset. Nessuna chiusura scientifica.

Per replicare il collaudo, passare a `collaudo.py` la directory del kit e un nuovo risultato. Per una release effettiva, `verifica.py` riceve il percorso del manifest, il suo SHA-256, il repository, l'ID del repository, la visibilità, l'ID della release, il tag e una nuova directory di destinazione. Lo ZIP H/K conserva il manifest e le ricevute. [Inventario locale del corpus](../bkl046-delivery-fresh-local-byte-readback-v1/README.md)
