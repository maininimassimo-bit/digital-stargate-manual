# BKL-046 — Sensibilità alla griglia di rilevazione ACS 11677

Le aperture e i controlli astrometrici e di qualità sono rimasti gli stessi. Per ciascuna coppia di visite ho spostato la griglia di rilevazione di 12 px orizzontalmente, verticalmente e su entrambi gli assi. Ho confrontato ogni fase separatamente. Per ciascun raggio ho raggruppato le rilevazioni collegate entro 0,1 arcsec e conservato quella col residuo di ricentraggio minore. Nel confronto tra fasi sono state contate solo le corrispondenze univoche.

| Visite | Offset px | Rilevazioni a 3 px | Sorgenti a 3 px | Sorgenti a 5 px | Riduzioni FLC a 3 px | Mediana appaiata FLC |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 01 e 04 | 0, 0 | 7 | 7 | 0 | 7 | −5,13 mmag |
| 01 e 04 | 12, 0 | 7 | 6 | 0 | 6 | −3,96 mmag |
| 01 e 04 | 0, 12 | 6 | 6 | 0 | 6 | −9,21 mmag |
| 01 e 04 | 12, 12 | 7 | 6 | 0 | 6 | −3,96 mmag |
| 09 e 11 | 0, 0 | 49 | 46 | 2 | 27 | −1,84 mmag |
| 09 e 11 | 12, 0 | 57 | 48 | 2 | 29 | −2,29 mmag |
| 09 e 11 | 0, 12 | 46 | 43 | 2 | 26 | −2,13 mmag |
| 09 e 11 | 12, 12 | 51 | 45 | 2 | 28 | −2,44 mmag |

La mediana appaiata usa la differenza FLC meno FLT del valore assoluto del Δcolore della singola sorgente. Il segno negativo ricorre in tutte le fasi e l'effetto mediano resta modesto nelle visite 09 e 11. Fra 42 e 45 sorgenti delle fasi traslate di 09 e 11 corrispondono univocamente al campione iniziale. La mediana appaiata della correzione CTE parallela varia da +0,24 a +0,29 mmag nella seconda coppia. Restano solo due sorgenti per il confronto fra raggi, quindi quel confronto resta aperto.

Il catalogo esterno ha individuato 36 visite con entrambi i filtri nel programma ACS/WFC 10424 su NGC 6397, una nel 9444 e due nel 10101. Questa pagina riporta un riscontro di catalogo e sei perturbazioni offline su 11677. L'ammissione scientifica del campione esterno richiede ancora i controlli sui prodotti individuali. [Riduzione del programma 10424](https://doi.org/10.1088/0004-6256/135/6/2114) · [Dati ACS di 9444 e 10101](https://doi.org/10.1051/0004-6361/200912757)

| Evidenza | SHA-256 |
| --- | --- |
| Tabella e riscontro di sensibilità | fdfb4ce320c7351f7f1f76af6e7d391f7d7f754e4a280485f529a1cb43098f1d |
| Riscontro di catalogo esterno | aacd7ec18b9500bbb3237062a5c583c6a95bd09f694ba8b6bff923e09fa0d2c0 |
| Archivio verificato su H: | 356375eab80bf259434216492f11d02e3d1cacbf47bb3c0d0ccddc3973ac957b |

Il ricalcolo della tabella e quello della fase 12, 0 per le visite 09 e 11 hanno riprodotto byte identici. Zero chiusure scientifiche e zero avvii nativi in questo incremento.
