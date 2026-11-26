# BKL-046 · Sensibilità alle partizioni dei dark M8/M20

Il protocollo riusa le misure congelate di 14 dark da 180 secondi nelle sei celle del rivelatore. Esamina 1.716 partizioni distinte in due gruppi disgiunti di sette, contando ogni coppia di gruppi una sola volta. In 64 partizioni ciascun gruppo riceve una posa per ogni coppia cronologica adiacente. La quindicesima posa rimane esclusa.

| Statistica per cella | Intercalata originale | Prime sette / ultime sette | Mediana delle 1.716 | P95 delle 1.716 | P95 delle 64 appaiate |
| --- | ---: | ---: | ---: | ---: | ---: |
| Media | 0,0997 | 0,1387 | 0,0669 | 0,1186 | 0,1231 |
| Mediana | 0,3571 | 0,2857 | 0,2143 | 0,3214 | 0,3464 |

Valori in ADU per la differenza assoluta massima fra le sei celle. Il caso cronologico con la media supera il P95 descrittivo di tutte le partizioni. Per la mediana è il caso intercalato originale a superarlo. Il rapporto conserva anche il massimo assoluto ai quattro angoli del piano di differenza. I gruppi sono disgiunti all'interno di ogni confronto. Fra confronti si riusano sempre le stesse pose, quindi i percentili descrivono sensibilità alla partizione sul campione fissato.

Il programma riproduce i coefficienti intercalati già pubblicati entro la tolleranza numerica e verifica il calcolo del piano con un controllo a coefficienti noti. Il rapporto completo con tutte le partizioni è nell'archivio H/K. La ricostruzione da H: verifica le impronte del rapporto sintetico e del file completo. Il test contribuisce all'asse `DIFFUSE_BACKGROUND/2` come riscontro strumentale. Restano da misurare il fondo ottico indipendente e l'effetto sulle immagini scientifiche. [Riscontro sorgente](../bkl046-m8-m20-dark-anchor-repeatability-v1/riscontro.json)

```text
python -I -B -S partizioni.py protocollo.json <riscontro-sorgente> riscontro-replica.json tutti-gli-esiti-replica.json
```
