# BKL-046 · Pose brevi di M20 su CCD scientifici DECam

Tre ritagli in banda r provengono da CCD scientifici e includono il centro di catalogo nella sezione DATASEC. Ogni ritaglio coincide esattamente con la sottoarray dell'immagine completa del CCD. Il conteggio sopra soglia usa il livello nominale dell'amplificatore a cui appartiene ogni campione.

| Esposizione | Data UTC | CCD | Programma | Campioni in DATASEC | Al livello nominale o sopra |
| --- | --- | --- | --- | ---: | ---: |
| 30 s | 13 febbraio 2013 | S22 | 2013A-0351 | 213.520 | 255 |
| 50 s | 6 giugno 2014, 05:23 | N15 | 2014A-0327 | 230.214 | 23 |
| 50 s | 6 giugno 2014, 08:34 | N15 | 2014A-0327 | 227.069 | 20 |

Le due pose di riferimento da 180 s risalgono al 31 luglio 2014, programma 2014A-0191, CCD S16. Si è applicata la stessa ricerca entro ±16 pixel dal WCS usata nel confronto precedente, con stima dell'offset su riquadri alterni e verifica sugli altri. Nei due confronti 30–180 s sono stati esaminati 24 candidati per coppia. Nel confronto fra le due pose da 50 s sono stati esaminati 35 candidati. Nessuna coppia ha raggiunto il numero minimo di corrispondenze in entrambi i gruppi. Il programma ha conservato le misure e i rifiuti senza calcolare rapporti fotometrici.

Le pose brevi acquisite qui non sono coeve con le pose da 180 s. Le immagini sono grezze e i controlli su bias, flat, PSF e livello calibrato di saturazione rimangono aperti. Il risultato verifica la copertura di CCD scientifici e delimita il metodo di registrazione usato. Zero avvii PixInsight e zero chiusure scientifiche.

Per riprodurre il test, eseguire `misura.py` con la directory di questo kit, il kit dei ritagli originali, il kit di ripetibilità M20, il percorso con NumPy 2.3.5 e Astropy 7.2.0 e un nuovo file di risultato. I FITS, gli URL e le impronte sono nel kit. I dati provengono dall'Astro Data Archive di NSF NOIRLab, gestito da AURA tramite accordo di cooperazione con la National Science Foundation. [Archivio NOIRLab](https://astroarchive.noirlab.edu/) · [Confronto precedente](../bkl046-m20-decam-science-frame-repeatability-v1/README.md)
