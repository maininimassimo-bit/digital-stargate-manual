# BKL-046 · Trasferimento della correzione di apertura fra stelle su UVIS1

Ho confrontato GD153 e GRW+70°5824 sullo stesso chip, con raggi di 5 e 10 pixel, fondo locale mediano e centro iniziale previsto dalle altre due bande via WCS. La ricentratura e i veto sul supporto sono gli stessi per entrambe le stelle. Per GD153 ho aggregato le due terne di ogni visita con la mediana. Per GRW+70°5824 ho usato le due visite UVIS1 complete e già fissate nel censimento. [Controllo GD153](../bkl046-gd153-relative-center-control-v1/README.md) · [Censimento GRW+70°5824](../bkl046-grw70-11907-held-out-color-transfer-v1/README.md)

In ciascuna direzione ho stimato la variazione di colore fra aperture con la mediana di due visite della stella di stima e ho valutato l'errore sulle due visite dell'altra stella. Il termine nominale usa le frazioni di energia racchiusa conservate con la fotometria GD153. La tabella riporta gli errori assoluti mediani in millimagnitudini.

| Stima → verifica | Colore | Senza correzione | Nominale | Altra stella |
| --- | --- | ---: | ---: | ---: |
| GD153 → GRW+70°5824 | F438W − F606W | 3,21 | 4,24 | 3,21 |
| GD153 → GRW+70°5824 | F438W − F814W | 4,77 | 4,77 | 4,77 |
| GD153 → GRW+70°5824 | F606W − F814W | 4,35 | 1,56 | 2,71 |
| GRW+70°5824 → GD153 | F438W − F606W | 1,31 | 4,17 | 0,21 |
| GRW+70°5824 → GD153 | F438W − F814W | 5,74 | 4,37 | 4,37 |
| GRW+70°5824 → GD153 | F606W − F814W | 7,06 | 4,58 | 4,58 |

La correzione stimata dall'altra stella riduce otto errori su dodici rispetto alla stima zero. In due colori nella direzione GD153 → GRW+70°5824, una visita migliora e l'altra peggiora e la mediana resta invariata. Il massimo residuo con correzione è 7,55 mmag. Le differenze fra stelle, visite e posizioni sul chip restano possibili spiegazioni degli scarti.

Le due stelle sono distinte e le pose di stima e verifica sono disgiunte. Le quattro visite condividono filtri, strumento e convenzioni di calibrazione. Il confronto misura la trasferibilità del termine di apertura nei casi ammessi e lascia aperta la validità su altri spettri e geometrie e l'incertezza scientifica. Zero chiusure scientifiche e zero avvii PixInsight.

Per riprodurre, passare a `misura.py` il protocollo, gli ZIP del centro GD153, del censimento GRW+70°5824 e delle aperture GD153 con le frazioni nominali, poi un nuovo percorso di risultato.