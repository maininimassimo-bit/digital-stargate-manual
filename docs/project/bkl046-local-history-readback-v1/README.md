# BKL-046 · Rilettura integrale dello storico locale della conoscenza

L'inventario storico include le 181 versioni dalla 0.1 alla 1.171. Questa verifica rilegge integralmente su H: i 45 file ancora da confrontare con i rispettivi SHA-256, pari a 63.599.156.359 byte. Ogni lettura controlla identità, dimensione e data di modifica prima e dopo. Il rapporto aggrega il risultato con le riletture conservate in precedenza.

La mappa di consegna associa ciascuna versione al suo alias, allo SHA-256 dell'oggetto del corpus e all'asset esatto. Le 181 versioni si trovano in 64 contenitori ZIP. La mappa indica il membro esatto per ciascuna versione. Per quattro versioni iniziali la rilettura è corroborata dalla catena dei successori, mentre resta assente una ricevuta diretta separata. Il nome e l'impronta della mappa integrale sono nel riscontro.

Il corpus è predisposto in locale. Rimangono da confermare la destinazione riservata e il perimetro di distribuzione. Gli ID degli asset e il recupero remoto richiedono la verifica della release reale. [Verificatore della consegna GitHub](../bkl046-delivery-integrated-readback-v1/README.md)

Per riprodurre la verifica, `rileggi.py` riceve l'inventario storico congelato, la directory della conoscenza su H: e un percorso nuovo per i risultati. `mappa-versioni.py` riceve le directory dei rapporti storici e dei metadati di consegna, il riscontro appena prodotto e una directory separata per il raccordo. Gli input sono caratterizzati dalle impronte conservate nei due script.
