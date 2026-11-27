# BKL-046 · Verifica congiunta della consegna GitHub

Il comando usa il soggetto di consegna e l’inventario v600 già registrati. Verifica che gli 80 asset del corpus coincidano con un sottoinsieme esatto degli 81 asset previsti nella release. Controlla l’archivio della conoscenza e l’impronta del JSON interno, ricostruisce gli oggetti e gli alias e confronta il rapporto con il ripristino di riferimento.

La modalità `offline` usa i contenitori locali e la capsula v1.171. La modalità `github` richiede la destinazione privata approvata con nome e ID del repository, ID della release e tag. Scarica gli asset per ID. Usa collegamenti NTFS agli stessi file scaricati per il ripristino e controlla nuovamente i metadati della release al termine. Registra un riscontro GitHub solo dopo tutti questi controlli. Il comando effettua letture GitHub e scrive i rapporti nella directory di prova.

Con Python 3.12 avviare `verifica-consegna.py` con la directory che custodisce `piano-completo.json`, `indice.json` e `inventario-trasporto.json` e una nuova directory di output sullo stesso volume NTFS. Aggiungere `offline` seguito dalla directory dei soli 80 asset e dal percorso della capsula, oppure `github` seguito dai quattro parametri della release privata. Il rapporto finale è `esito.json`. I controlli confrontano le impronte degli script e dei metadati prima dell’uso.

Il collaudo locale non attesta un trasferimento remoto. Gli ID e il perimetro della release restano da autorizzare. L’esito esclude la validazione scientifica.

La prova su DSG-Shared ha verificato 81 asset per 27.582.310.714 byte, la capsula della conoscenza, 10.180 oggetti e 11.839 alias. I cinque controlli mirati hanno respinto asset alterato, nome duplicato, inventario diverso, rapporto del solo mirror e impronta alterata degli alias.
