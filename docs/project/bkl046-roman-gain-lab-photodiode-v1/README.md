# BKL-046 · Fotodiodi della sequenza Roman GAIN

Ho riletto l’estensione di telemetria in tutti i 21 FITS GAIN usando intervalli HTTP vincolati agli ETag già registrati. Nei file l’estensione si chiama `LABHK`. Le colonne riportano il monitor MCT in volt, il monitor al silicio in ampere e il tempo in MJD. Le 96 righe contengono 65 istanti distinti. Il segnale MCT va da 0,8002 a 0,8087 V. Il monitor al silicio ha 46 valori negativi e 50 non negativi. [Formato FITS DCL](https://archive.stsci.edu/files/live/sites/mast/files/home/missions-and-data/roman/wfi-triplet-test-data/_documents/Roman_DCL_Triplet_FITS_Metadata_draft_210813e3.pdf)

Ho integrato il segnale MCT interpolato linearmente nelle finestre nominali, solo dove la telemetria copre gli estremi. Ho confrontato la dispersione fra coppie del segnale mediano della fascia centrale diviso per il tempo medio nominale e per l’integrale medio MCT. In due esposizioni `TGROUP` vale 3,17 s. Nelle altre vale 3,08 s. Il calcolo usa il valore di ogni file. [Misure della fascia centrale](../bkl046-roman-gain-all-channel-covariance-v1/README.md)

| Lettura | Coppie con finestra nominale coperta | CV diviso per tempo | CV diviso per integrale MCT |
| --- | ---: | ---: | ---: |
| 1 | 9 | 1,225% | 1,267% |
| 5 | 9 | 0,616% | 0,540% |
| 10 | 9 | 0,520% | 0,450% |

Con la finestra spostata di un gruppo, tutte le dieci coppie sono coperte. Alla lettura 10 il CV passa da 0,631% a 0,506%. Sono confronti descrittivi sulle stesse esposizioni con temporizzazione nominale. Il monitor MCT offre una misura ottica separata dal rivelatore. Restano da verificare l’offset al buio, la conversione in fotoni al sensore e la temporizzazione per pixel. Il risultato attesta un indicatore relativo per questa serie di laboratorio. La dose calibrata e la prova nativa restano aperte.

Per riprodurre, invocare `verifica.py` con la directory estratta del kit, la directory estratta della rampa, `replay`, il kit della fascia centrale, le dipendenze NumPy 2.3.5 e Astropy, un nuovo rapporto e lo SHA-256 della cattura `82e9d6eb221362210cbec719ec73fcc8765e37b82e886c0572b681a07c82e03e`.