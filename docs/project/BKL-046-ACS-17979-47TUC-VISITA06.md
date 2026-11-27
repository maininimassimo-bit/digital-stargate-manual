# ACS 17979 · Visita 06 e copertura sullo stesso chip

Per le tre associazioni F606W da 300 secondi della visita 06 è stato acquisito il primo membro con FLT/FLC e RAW associato, prima di esaminare le immagini. I tre JIF, con sei registrazioni registrano `FINE LOCK/GYRO` senza `GSFAIL` riportato e con RMS disponibili. Il calcolo usa i centroidi verificati tramite WCS e conserva il controllo sul puntamento. [ACS Calibration Plans](https://www.stsci.edu/hst/instrumentation/acs/calibration/calibration-plans) · [Guida ai log HST](https://hst-docs.stsci.edu/hstdhb/5-observation-logs/5-2-using-observation-logs)

La geometria è stata verificata separatamente, proiettando una griglia da 32 pixel attraverso i WCS dei due puntamenti per ciascuna coppia di esposizioni e chip. Sono stati valutati 8.001 punti per coppia/chip. La sola sovrapposizione sullo stesso chip presente nella griglia è tra jfln06010 e jfln06020: il massimo spostamento Y è 41,83 pixel sul chip 1 e 31,23 pixel sul chip 2. Le altre coppie non hanno sovrapposizione interna rilevata sullo stesso chip. Nessun punto raggiunge il requisito di 550 trasferimenti.

Il confronto fotometrico esamina 408 candidate. Sette coppie passano i tagli su distanza astrometrica, supporto, isolamento e differenza Y, tutte tra chip diversi. Si confrontano i rate a raggio 3 con PAM e PHOTFLAM prima della correzione, dopo la correzione CALACS a livello pixel, e dopo il modello fotometrico parallelo. L'associazione astrometrica delle coppie ha una separazione massima di 0,061″.

| Metodo, sette coppie tra chip | Mediana del contrasto assoluto | Massimo |
| --- | ---: | ---: |
| FLT | 101,70 mmag | 234,51 mmag |
| FLC | 14,70 mmag | 63,35 mmag |
| FLT con modello parallelo | 25,60 mmag | 55,75 mmag |

Entrambe le correzioni riducono il contrasto assoluto per le sette coppie. Il cambio di chip e l'uso di una sola visita limitano l'interpretazione dei residui. La telemetria FINE LOCK/GYRO lascia possibili errori di rollio. La prova non separa CTE seriale, risposta di chip ed effetto di apertura. Zero avvii nativi e zero chiusure scientifiche.

Replay dei due JSON dagli archivi su H:. SHA-256 del riscontro fotometrico `f0b96d29a4c70c671e1ea484679dfe8a09a676aa9f8f75616070bcc6c67c918f`. SHA-256 della geometria `550876a323bd5452169af8bab926294579357c54c27fb4e940ca1e19a8e6146c`. SHA-256 archivio `2d28a3f9afa7592fdcfa4c872273a6c33bae5b45bb2141865586b0650248ae21`.

[Visita 02 di ACS 17979](BKL-046-ACS-17979-47TUC-CTE.md).
