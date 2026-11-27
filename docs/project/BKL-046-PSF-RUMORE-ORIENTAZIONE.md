# BKL‑046 · Orientazione PSF con rumore gaussiano

Il protocollo confronta la soglia dell’adattamento senza rumore con una soglia fissata prima della prova. La nuova regola richiede ellitticità almeno 0,04 e un miglioramento della somma dei quadrati di almeno 9,21 volte la varianza del rumore. Si usano 864 realizzazioni di rumore gaussiano su 54 geometrie Moffat. Il livello di rumore è noto, la scala è fissata e il centro iniziale è spostato di 0,05 pixel. [Controllo numerico senza rumore](BKL-046-PSF-CENTRO-LIBERO.md)

| Rapporto segnale-rumore | Profilo | Prove | Non qualificate | Angolo indeterminato | Angolo utile entro 5° | Angolo fuori tolleranza o spurio |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 25 | Circolare | 240 | 218 | 22 | — | 0 |
| 25 | Rapporto assiale 0,60 | 96 | 84 | 12 | 0 | 0 |
| 25 | Rapporto assiale 0,85 | 96 | 87 | 9 | 0 | 0 |
| 100 | Circolare | 240 | 100 | 139 | — | 1 |
| 100 | Rapporto assiale 0,60 | 96 | 37 | 1 | 25 | 33 |
| 100 | Rapporto assiale 0,85 | 96 | 21 | 36 | 14 | 25 |

La soglia precedente assegnava 22 e 79 angoli spuri ai controlli circolari rispettivamente ai due livelli. La nuova soglia li riduce a 0 e 1. Fra gli adattamenti circolari qualificati le frazioni corrispondenti sono 0 su 22 e 1 su 140. Le prove non qualificate restano nel denominatore del controllo di disponibilità.

Nessun gruppo supera congiuntamente i criteri congelati di disponibilità e orientazione. Tutti i 547 casi non qualificati falliscono il controllo di stazionarietà ellittico, con un caso che fallisce anche il controllo circolare. In 286 casi il fit ellittico non stazionario è entro 0,00001 dal limite superiore di ellitticità. Il test distingue un limite dell’ottimizzazione da un angolo indeterminato. Resta da verificare l’ottimo vincolato anziché accettare ogni arresto al bordo. Incertezze, profili fuori famiglia e riproduzione nativa restano aperti.

SHA‑256 della ricevuta `7267bbf8d6700576c7582e19c91f11df59c7e778165e68f0996dcc13b194b9a5`.
