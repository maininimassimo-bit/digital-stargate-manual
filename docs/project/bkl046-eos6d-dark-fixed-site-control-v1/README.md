# BKL-046 · Dark EOS 6D e ricorrenza dei codici estremi M51

Ho recuperato tre dei 25 CR2 della cartella dark nello ZIP originale dell'autore. Ho selezionato il primo, il mediano e l'ultimo in ordine lessicografico, verificato la revisione HTTP e il CRC ZIP, e vincolato ogni file per SHA-256. Dai metadati, le pose luce durano 45,3 s e i dark 45,4 s. Tutte sono a ISO 800. I dark hanno durata vicina ma non identica e la temperatura non è stata verificata. [Catalogo originale](https://amor.cms.hu-berlin.de/~rodrigus/datasets.html)

| Fase | Campioni al limite in tutte le pose luce | Presenti anche in tutti i dark al limite |
| --- | ---: | ---: |
| R | 5 | 5 |
| G1 | 9 | 9 |
| G2 | 4 | 4 |
| B | 7 | 7 |

Il limite per canale è 12.507 DN secondo rawpy. Tutti i 25 campioni ricorrenti nelle pose luce superano lo stesso limite alle stesse coordinate e nella stessa fase in tutti i dark. In totale, nei singoli dark compaiono 28–29 campioni al limite. L'accumulo a 14.042–14.043 DN compare anche nei dark. La ricorrenza a coordinate fisse è quindi coerente con una componente del sensore o della catena di lettura presente in assenza della scena. Questo riscontro non identifica il meccanismo fisico, non misura full well e non qualifica una correzione. [Documentazione rawpy](https://letmaik.github.io/rawpy/api/rawpy.RawPy.html)

Per ripetere, eseguire `verifica.py` con questo archivio estratto, la directory estratta dello studio precedente con CR2 luce e wheel, i pacchetti rawpy estratti, le DLL VCLibs e un nuovo percorso di uscita. [Studio delle pose luce](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/1aa418144f7df776547e9dfe0e6101b266078736/docs/project/bkl046-cfa-native-code-limits-v1)
