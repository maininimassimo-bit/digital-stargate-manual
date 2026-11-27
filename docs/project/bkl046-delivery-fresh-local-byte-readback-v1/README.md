# BKL-046 · Rilettura dei contenitori per la consegna GitHub

La verifica ricalcola l'SHA-256 dei contenitori fisici su H: e sul volume della VM ospitato su K:. L'indice v600 fissa 71 lavori, 80 contenitori, 10.180 oggetti distinti e 11.839 alias. Sono stati riletti 27.478.864.996 byte su ciascun volume. Le due liste coincidono e ricoprono, per dimensione e impronta, gli 80 nomi distinti dell'inventario dei potenziali asset.

La capsula v1.171 è stata riletta separatamente sulle due copie. Dalla capsula da 103.445.718 byte è stato ricostruito in streaming lo stesso JSON da 3.030.957.683 byte, con SHA-256 `65511eaafd15af1ea7c7f07cdd90d7947d622b6d6f88b31f022e9ac2399c4c0d`. La verifica non estrae il JSON su disco.

Il repository pubblico del manuale aveva una release senza asset. Il repository privato candidato non aveva release. Il fascicolo è pronto per il trasferimento dei byte verificati quando sarà definito il perimetro autorizzato. La consegna integrale su GitHub richiede un riscaricamento indipendente degli asset effettivamente pubblicati, verifica delle impronte e ricostruzione. La baseline v1.171 resta intermedia. [Indice della conoscenza](../BKL-046-KNOWLEDGE-DELIVERY-v1.171.json)

La replica del kit verifica la riconciliazione fra i due rapporti di lettura, l'indice, l'inventario e la capsula. I contenitori originali sono nelle rispettive copie fisiche. Il rapporto pubblico conserva i riepiloghi e le impronte.
