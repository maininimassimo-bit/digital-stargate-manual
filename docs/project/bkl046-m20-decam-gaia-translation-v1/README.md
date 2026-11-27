# BKL-046 · Controllo Gaia delle coordinate DECam di M20

Ho verificato per ogni posa se una traslazione del WCS può essere confermata da Gaia DR3. Le posizioni Gaia sono propagate all'epoca di osservazione con i moti propri. Il programma cerca scostamenti fino a 140 pixel per asse, stima la traslazione su riquadri alterni e la verifica su riquadri distinti, senza riusare le sorgenti Gaia impiegate nella stima. La soglia fissata richiede almeno cinque associazioni di stima, quattro di verifica e più associazioni di tutti i 24 controlli traslati.

| CCD | Durata | Esito | Associazioni di stima | Associazioni di verifica |
| --- | ---: | --- | ---: | ---: |
| S22 | 30 s | Inconcluso | 1 | 0 |
| N15, prima posa | 50 s | Inconcluso | 2 | 1 |
| N15, seconda posa | 50 s | Inconcluso | 2 | 0 |
| S16, prima posa | 180 s | Inconcluso | 3 | 2 |
| S16, seconda posa | 180 s | Inconcluso | 3 | 3 |

Per le due pose da 180 s, la differenza fra le traslazioni candidate è circa (+11,13, −8,97) pixel. È coerente con lo scostamento relativo misurato nel confronto diretto S16, pari a circa (+11,21, −9,08) pixel. L'accordo non aumenta il numero delle associazioni assolute disponibili e il protocollo rifiuta tutti e cinque i casi. Per le pose brevi, allargare la ricerca a una traslazione costante non ha prodotto corrispondenze sufficienti.

Il test tratta traslazioni e conserva le ipotesi non confermate. Restano aperte le verifiche di orientamento, scala, PSF e trasferimento fotometrico. I FITS sono associati alle rispettive immagini complete e i candidati vengono misurati solo in DATASEC sotto i limiti nominali del relativo amplificatore. Zero avvii PixInsight e zero chiusure scientifiche.

Per riprodurre, eseguire `misura.py` con la directory di questo kit, il kit delle pose brevi, il kit dei ritagli originali, il kit di ripetibilità M20, la directory con NumPy 2.3.5 e Astropy 7.2.0 e un nuovo risultato. La copia del catalogo Gaia a copertura verificata è inclusa nell'archivio locale. [Gaia DR3](https://gea.esac.esa.int/archive/documentation/GDR3/) · [Confronto precedente su S16](../bkl046-m20-decam-science-frame-repeatability-v1/README.md)
