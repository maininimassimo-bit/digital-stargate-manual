# BKL-046 — Verifica delle esposizioni disponibili nella raccolta M42 di Santiago Rodriguez

La pagina dell'autore indica una Canon EOS 40Da e distribuisce RAW CR2 e prodotti elaborati. La raccolta ZIP ha una lunghezza di 2.400.780.173 byte. Il controllo legge la directory centrale e i primi 16.384 byte compressi a partire dall'intestazione locale di ogni membro CR2, con intervalli HTTP verificati contro lo stesso ETag. Il nome locale deve coincidere con quello della directory centrale. La lettura EXIF restituisce modello, ISO, tempo di posa e timestamp locale. Non sono stati acquisiti i fotogrammi completi.

| Gruppo nel pacchetto | CR2 | Modello EXIF | ISO | Posa EXIF |
|---|---:|---|---:|---:|
| lights | 134 | Canon EOS 40D | 1600 | 30 s |
| darks | 20 | Canon EOS 40D | 1600 | 30 s |
| flats | 17 | Canon EOS 40D | 100 | 2,5 s |
| biases | 4 | Canon EOS 40D | 1600 | 30 s |

La denominazione 40Da proviene dalla descrizione dell'autore. L'EXIF identifica il modello come 40D. I tre file XMP restano esclusi dai conteggi. I quattro CR2 nella cartella biases dichiarano 30 s e richiedono una verifica della funzione di calibrazione prima dell'uso.

Le pose scientifiche coprono una sola durata. La raccolta resta un possibile controllo astronomico a posa costante e viene esclusa dal confronto HDR con una posa intermedia indipendente. I 175 prefissi occupano 2.867.200 byte, oltre ai 262.144 byte della coda del pacchetto. Le impronte dei prefissi sono nel rapporto. Il replay dalla copia H ricostruisce il rapporto leggendo la coda e i prefissi archiviati. Zero esecuzioni native o chiusure scientifiche.

[Datasets di Santiago Rodriguez](https://amor.cms.hu-berlin.de/~rodrigus/datasets.html)
