# BKL-046 · Separazione di sorgenti sovrapposte su M8/M20

L'asse FILTER_COLOR/3 resta aperto. La prova confronta apertura, PSF singola e PSF congiunta su immagini lineari rosse e blu ricostruite per interpolazione bilineare per parità. L'esportazione conserva le misure precedenti di apertura e maschera. Stelle di stima 20, stelle di verifica 19. I riferimenti ottici rimangono i due profili Sony con L-Pro già congelati. [Fotometria e gruppi di sorgenti PSF](https://docs.astropy.org/projects/photutils/en/latest/user_guide/grouping.html)

La PSF circolare Moffat è integrata con nove campioni per pixel. La larghezza è stimata sulle sole stelle di stima in calibrazione A, con beta fissato a 2,5. Il modello congiunto usa una larghezza di 2,750 px in rosso e 3,125 px in blu, centro fissato e un unico piano di fondo per il gruppo. Include i vicini Gaia entro 10 pixel e 3 mag in G. Una prova iniziale normalizzava il residuo per il flusso della stessa soluzione e spingeva la stima al limite della griglia. Il risultato qui riportato usa il residuo quadratico in pixel sullo stesso supporto, con minimi interni per le due larghezze condivise.

## Iniezioni su immagini reali

Ho aggiunto un vicino simulato sulle immagini delle stelle tenute da parte. Il vicino ha il 22% del flusso d'apertura rosso e l'11% di quello blu, PSF più larga del 15%, ali più estese e offset subpixel rispetto alla posizione nota al modello. Il confronto della PSF congiunta usa la stessa colonna del vicino prima e dopo l'iniezione. Una prova esatta senza rumore recupera il flusso noto del bersaglio. Le iniezioni misurano la variazione di colore introdotta dal vicino simulato, senza modellare il rumore addizionale del vicino.

| Separazione del vicino | Iniezioni valide | P90 variazione B−R, apertura A/B (mag) | PSF singola A/B (mag) | PSF congiunta A/B (mag) |
| --- | ---: | ---: | ---: | ---: |
| 2,0 px | 57 | 0,091 / 0,092 | 0,082 / 0,083 | 0,047 / 0,046 |
| 3,5 px | 56 | 0,085 / 0,086 | 0,028 / 0,028 | 0,0105 / 0,0104 |
| 5,0 px | 57 | 0,070 / 0,071 | 0,0022 / 0,0021 | 0,0036 / 0,0036 |

## Stelle osservate

A parità di stelle e dopo stima dello zero sulle 20 stelle di calibrazione, l'errore P90 sulle 19 stelle osservate è 0,103–0,126 mag per l'apertura e 0,440–0,449 mag per la PSF congiunta. Il guadagno sulle iniezioni non si trasferisce alle sorgenti osservate. La PSF circolare comune e il piano locale non sono qualificati per il colore di questo campo. La prossima verifica deve distinguere forma della PSF e struttura del fondo usando residui per banda e PSF empiriche con controllo spaziale.

- SHA-256 della ricevuta `1cf6f1b055a9ad2b45ed80d7cfc0b294f957f3621a2592d39d2bb6608058f2d8`.
- Archivio H: `Produzione/2026-10-13/Digital-StarGate-PixInsight/archives/BKL046-M8-PSF-iniezioni-1cf6f1b055a9.zip`.
- Zero avvii nativi e zero chiusure scientifiche.
