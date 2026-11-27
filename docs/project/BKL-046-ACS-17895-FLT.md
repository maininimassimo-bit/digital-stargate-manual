# ACS 17895 · Verifica nei 24 FLT originali

L'audit riprende tutti i 24 membri FLT delle 12 associazioni del programma 17895. Per ciascun file sono stati verificati SHA-256, identità, associazione, bersaglio, filtro, amplificatore B e subarray WFC1B-1K. Tutte le pose riportano `PCTECORR=OMIT`. Le posizioni indipendenti provengono dai due record Gaia DR3 identificati in CALSPEC e propagati all'epoca della posa. [Identità Gaia in CALSPEC](https://www.stsci.edu/hst/instrumentation/reference-data-for-calibration-and-tools/astronomical-catalogs/calspec)

La ricerca diagnostica esamina una finestra di ±35 pixel dalla proiezione Gaia. Cerca un massimo su una mediana mobile 3×3 con DQ zero, richiede un contrasto di almeno 20 volte la dispersione robusta locale e mantiene una soglia di quattro pixel per la corrispondenza di posizione.

| Visita | Esito sui sei FLT |
| --- | --- |
| jfjv02 · WDFS0122-30 | Nessuna sorgente supera la soglia nella finestra |
| jfjv03 · WDFS0458-56 | Sei rilevamenti coerenti, spostati di +0,513″ a est e +0,049″ a nord da Gaia. Scostamento massimo dalla mediana 0,0095″ |
| jfjv15 · WDFS0458-56 | Sei rilevamenti entro soglia Gaia |
| jfjv17 · WDFS0122-30 | Sei rilevamenti entro soglia Gaia |

Il segnale di jfjv03 è un candidato coerente tra tre bande, da confermare con registrazione o riscontri di puntamento indipendenti. Le finestre a raggio 3 e 5 hanno pixel DQ non nulli in tutti e sei i rilevamenti. Per jfjv02 il risultato si limita alla finestra riprodotta.

I 12 rapporti di telemetria JIF sono stati legati per identificativo alle 24 esposizioni. Tutti e sei i membri di jfjv02 registrano `GUIDEACT=GYRO` e `GSFAIL=NOLOCK`. I sei di jfjv03 registrano `FINE LOCK/GYRO` e `TLMGAP`. Tutti e dodici quelli di jfjv15 e jfjv17 riportano `FINE LOCK` e nessun codice di errore nella stessa voce. Il mancato aggancio è un riscontro diretto per jfjv02. Il vuoto di telemetria di jfjv03 impedisce una diagnosi causale completa dello scarto. [Guida STScI alle anomalie ACS](https://www.stsci.edu/hst/instrumentation/acs/proposing/exception-report-instructions)

Nei 12 FLT di jfjv15 e jfjv17, tutte le aperture a raggio 3 hanno DQ zero e nessun pixel con flag di saturazione nell'apertura. A raggio 5 tutte contengono uno o due pixel non utilizzabili. A raggio 3 sono stati misurati **30.327–34.034 elettroni per singola posa**, con un fondo di **2,05–14,07 elettroni/pixel** e **514,87–515,10 trasferimenti paralleli** dalla geometria WFC1. Questi numeri consentono una successiva verifica del modello CTE con parametri per esposizione. La guida web prescrive DRZ, mentre la documentazione ACSTOOLS descrive l'API anche per la fotometria FLT. Le due modalità vanno confrontate esplicitamente. Nessuna correzione è stata applicata, zero avvii nativi e zero chiusure scientifiche. [Calcolatore ACS](https://acsphotometriccte.stsci.edu/) · [Documentazione ACSTOOLS](https://acstools.readthedocs.io/en/latest/acsphotcte.html)

Replay dagli archivi su H: con JSON identico byte per byte. SHA-256 riscontro `23bccbd31a7abaa4b393d456447675c2bf987bc83b6ea31f2b6d58d8a56da121`. SHA-256 archivio `67d3776c513eb7b638ad932a72c512cbb4054cb5d950d251440feff86a842ca6`.

Anche l'audit JIF è stato ripetuto byte per byte. SHA-256 riscontro `662132e414df86d7962a5eb3310167effe2ad79c4e84406a00e7a8bdc54d1838`. SHA-256 archivio `d5b652922f94a83459e3d613f57a0068230408e5d9055fa8be7a8f8dd5001f5c`.

[Provenienza e misure DRZ](BKL-046-ACS-17895-CTE-DRZ.md).
