# BKL-046 · Emissione Hα e geometria dei riferimenti M8/M20

Il campo SHASSA 153 copre tutte le 192 celle geometriche M8/M20 ai due raggi fissati. Il programma rilegge le sei celle del test precedente, riproducendone coordinate, supporto e mediane. Confronta la disposizione originale con i sei valori Hα più bassi e con sei celle a emissione minima distribuite in altrettanti settori prefissati. [Misura precedente](../bkl046-m8-m20-shassa-anchor-reference-v1/README.md) · [Campo SHASSA 153](https://amundsen.astro.swarthmore.edu/SHASSA/ImagePages/153.html)

| Disposizione, raggio 4 arcmin | Mediana Hα, R | Massimo Hα, R | Fattore massimo di propagazione | Dopo rimozione di una cella, caso peggiore |
| --- | ---: | ---: | ---: | ---: |
| Originale | 179,10 | 800,3 | 0,873 | 1,371 |
| Sei celle a emissione più bassa | 60,55 | 60,7 | 3,164 | 5,166 |
| Una cella a emissione minima per settore | 68,55 | 126,0 | 1,069 | 1,608 |

Il fattore è il massimo, sui 192 centri, del rapporto fra deviazione standard del valore predetto dal piano e deviazione standard di una misura di riferimento, assumendo errori indipendenti e di pari varianza. Il massimo è circa 3,6 volte quello originale scegliendo le sei celle globalmente più deboli, e circa 1,2 volte scegliendone una per settore. A 2 arcmin la preferenza geometrica resta la stessa, mentre cambiano alcuni identificativi. Il rapporto conserva tutte le rimozioni singole e il file completo conserva le misure per cella.

Le aperture vicine possono sovrapporsi. Il rapporto non misura la covarianza della mappa né l'errore reale di un piano in ADU. La selezione è una candidata da verificare con misure ottiche coeve e indipendenti. La prova riguarda gli assi `DIFFUSE_BACKGROUND/2` e `DIFFUSE_BACKGROUND/3`. Zero avvii PixInsight e zero chiusure scientifiche.

Per replicare, estrarre l'archivio sorgente fissato da `protocollo.json` e usare NumPy 2.3.5 e Astropy 7.2.0.

```text
python -I -B -S confronta.py protocollo.json <archivio-estratto> <dipendenze> riscontro-replica.json esiti-replica.json
```

Dati SHASSA prodotti con il supporto della National Science Foundation. [Gaustad et al. 2001](https://arxiv.org/abs/astro-ph/0108518)
