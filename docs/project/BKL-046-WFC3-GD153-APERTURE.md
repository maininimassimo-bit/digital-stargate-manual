# BKL-046 — Controllo delle aperture GD153 WFC3/UVIS

Ho acquisito e legato ai metadati MAST tutte le 36 pose FLC pubbliche della selezione GD153. Nei programmi 17362 e 17682 la selezione forma sei visite con due pose per banda F438W, F606W e F814W. Tutti gli header riportano `SCAN_TYP=C` ed `EXPFLAG=TDF-DOWN AT EXPSTART`. Il protocollo per fotometria puntata richiede `SCAN_TYP=N` ed `EXPFLAG=NORMAL`, quindi nessuna delle sei visite entra nel confronto a tre bande. [Archivio MAST](https://hst-docs.stsci.edu/hstdhb/1-obtaining-hst-data/1-1-archive-overview) · [Keyword WFC3](https://hst-docs.stsci.edu/wfc3dhb/chapter-2-wfc3-data-structure/2-4-headers-and-keywords)

Come controllo in modalità puntata ho riletto le otto esposizioni F606W UVIS2/C del notebook STScI, distribuite su tre epoche. Ho usato i centri riportati, PAM UVIS2, apertura di 10 pixel, anello di fondo 155–165 pixel e apertura frazionaria campionata su 64 × 64 sottopixel. Il fondo usa i campioni DQ zero con clipping a tre sigma. Ho conservato il veto DQ nel nucleo e nell'apertura, senza sostituzioni. [Notebook di riferimento STScI](https://spacetelescope.github.io/hst_notebooks/notebooks/WFC3/uvis_time_dependent_photometry/uvis_timedep_phot.html)

| Epoca | Pose puntate | Aperture ammissibili |
| --- | ---: | ---: |
| 2009 | 4 | 1 |
| 2013 | 2 | 0 |
| 2017 | 2 | 0 |

Nella posa ammessa la misura è **103.661,72 elettroni/s**, a **4,04 ppm** dal valore del notebook sugli stessi dati, con STmag **13,60305**. Ogni altra posa ha da 1 a 51 pixel DQ diversi da zero nell'apertura. L'accordo sul caso ammesso controlla il calcolo locale su un prodotto reale. La fotometria ripetuta tra epoche e il confronto a tre bande restano non misurati. Il controllo usa dati condivisi con il riferimento e non attesta una nuova calibrazione assoluta né una validazione nativa PixInsight.

| Evidenza | SHA-256 |
| --- | --- |
| Protocollo | `cff6a127ed10ce6fc8cfce2db52229cead541a15b622e811367876abc453d54d` |
| Programma | `1ad0fa88bd3424978cac4c393570f6c4a2adb1afeecfcc04a1784a59d5269e03` |
| Riscontro | `b056310ee0ed0a0620d21b4f50e757cebc84a488deef5b832e79c6c13449833f` |
| Archivio con 44 FLC e replay da H: | `478b092d63578128771eb1c81a89bac64801528b848de9fc67a80829a3f80b82` |
