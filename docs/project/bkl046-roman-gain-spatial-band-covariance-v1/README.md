# BKL-046 · Propagazione della varianza in tre fasce del Roman H4RG

Ho fissato due nuove fasce SCI da 64 righe, agli indici 512–575 e 3520–3583, e le ho confrontate con la fascia centrale 1920–1983. I 160 nuovi segmenti HTTP corrispondono alle stesse 20 esposizioni e quattro letture della prova precedente. Ogni richiesta è vincolata all’ETag e alla lunghezza dell’oggetto già registrati, oltre che all’intervallo di byte atteso. [Dati Roman di laboratorio](https://archive.stsci.edu/missions-and-data/roman/wfi-triplet-test-data)

| Lettura | Fascia inferiore, completa / diagonale | Fascia centrale, completa / diagonale | Fascia superiore, completa / diagonale |
| --- | ---: | ---: | ---: |
| 1 | 21,9% / 65,3% | 25,4% / 66,9% | 27,9% / 67,9% |
| 5 | 13,4% / 61,5% | 15,5% / 62,4% | 14,3% / 61,9% |
| 10 | 12,0% / 60,9% | 13,8% / 61,7% | 12,7% / 61,2% |

La tabella riporta l’errore mediano su 320 confronti per fascia e lettura. Tutti i 32 canali in ciascuna fascia hanno una mediana più bassa con la propagazione dei pesi completi. Le maschere escludono i blocchi con campioni al limite di rappresentazione. Nelle nuove fasce restano almeno 951 blocchi su 961 per canale, oltre la soglia fissata di 769. Il rapporto registra inoltre gli scarti rispetto alla fascia centrale sulle stesse coppie e sugli stessi canali.

Le fasce condividono le esposizioni. I risultati riguardano tre zone del rivelatore Roman in laboratorio, a un solo spostamento bilineare. Restano aperte la dose indipendente, la verifica nativa e la risposta ASI2600MC a più dosi. Nessuna chiusura scientifica.

Per riprodurre offline, passare a `misura.py` la directory del kit, le directory estratte degli archivi [rampa GAIN](../bkl046-roman-gain-ramp-covariance-v1/README.md) e [fascia centrale](../bkl046-roman-gain-all-channel-covariance-v1/README.md), la directory con NumPy 2.3.5, il percorso di un nuovo rapporto e l’impronta della cattura `8948884b38d16ed2f8ba1ed092f4151999542a86d5cf4ef483d63ff9108ad9d0`.