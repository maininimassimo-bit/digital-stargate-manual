# BKL-046 — Saturazione ricorrente nelle pose lunghe Hubble F658N di Orione

Lo schermo legge i due piani DQ di ciascuna posa individuale da 774 e 822 s. Forma componenti connesse a otto vicini che hanno il bit 256 del full well, escludendo i bit 1, 2, 4 e 8. Per ogni componente trasforma il centro geometrico in coordinate celesti con il WCS del singolo chip. Conserva i soli accoppiamenti univoci entro 0,35 arcsec e mantiene nel rapporto il conteggio delle altre associazioni entro soglia.

| Radice FLC | Componenti DQ 256 | Pixel DQ 256 |
|---|---:|---:|
| jcaz07f5q | 98 | 2145 |
| jcaz07ffq | 111 | 2347 |

Delle 76 coppie geometriche entro soglia, 76 erano univoche. In 3 casi il disco di raggio 3 pixel, centrato sulla posizione media proiettata, aveva SCI finito e DQ zero su entrambe le pose da 150 s e sulla posa da 340 s tenuta fuori dalla stima.

Il censimento copre tutti i piani DQ delle due pose lunghe, comprese le regioni esterne al riquadro iniziale. Il controllo non misura il flusso né prova che corrispondenze astrometriche vicine abbiano la stessa origine fisica. Restano da verificare la registrazione relativa, l'associazione alle sorgenti e la stabilità fra epoche. Le pose di riferimento risalgono al 2003 e al 2005 e le due pose lunghe al 2015. Zero esecuzioni native e chiusure scientifiche.

Gli intervalli FITS letti sono fissati per ETag, lunghezza, SHA-256 e corrispondenza del prefisso con il dossier delle esposizioni. Il replay offline usa i blocchi archiviati, Astropy 7.2.0 e NumPy 2.3.5. Lo script accetta directory del dossier, directory delle dipendenze, directory del dossier delle esposizioni, percorso di output e modo replay.

[Dossier delle esposizioni](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/9a5d19b5f6ae35b9dcd7ca6880295602343b73ab/docs/project/bkl046-orion-acs-f658n-exposure-members-v1) · [Flag DQ ACS](https://hst-docs.stsci.edu/acsdhb/chapter-3-acs-calibration-pipeline/3-4-calacs-processing-steps)