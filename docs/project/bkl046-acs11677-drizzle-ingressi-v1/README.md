# Ingressi per la replica AstroDrizzle di ACS GO-11677

Per l'associazione `jb6v01010` in F606W, i sei FLC del manifest corrispondono in ordine alle 12 schede degli ingressi SCI del DRC ufficiale. Dimensioni e identita FITS sono confrontate con il censimento MAST. Tre SHA-256 erano gia registrati e sono stati verificati. Gli altri tre sono stati calcolati dopo l'acquisizione da MAST.

Il pacchetto conserva il trailer MAST, i prefissi delle testate DRC e DRZ e la MDRIZTAB CRDS usata nel trailer. Conserva anche la wheel ufficiale DrizzlePac 3.11.0 per Linux x86-64 e CPython 3.12, verificata contro la distribuzione PyPI. DSG-Shared non ha WSL installato e la release PyPI non include una wheel Windows. La wheel non contiene le dipendenze da fissare separatamente.

Per il prossimo collaudo restano da qualificare ambiente e dipendenze, verificare le referenze geometriche effettive dei FLC e costruire le due esecuzioni controllate con e senza il ricalcolo del bit 4096. Il confronto con MAST deve partire da copie di lavoro e conservare individualmente le mappe DQ dei due chip. I prodotti archiviati e i master sono ingressi immutabili. La preparazione documentata qui non ha eseguito AstroDrizzle ne PixInsight e non chiude requisiti scientifici.

[Archivio MAST dell'associazione](https://mast.stsci.edu/portal/Mashup/Clients/Mast/Portal.html) | [Distribuzione AstroDrizzle 3.11.0](https://pypi.org/project/drizzlepac/3.11.0/)
