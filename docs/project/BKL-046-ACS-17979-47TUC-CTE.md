# ACS 17979 · Verifica CTE con stelle osservate a differenti distanze di trasferimento

Il programma 17979 del ciclo 33 è successivo ai dati usati per i coefficienti fotometrici del ciclo 32. Alla visita 02 sono state selezionate le tre associazioni pubbliche F606W da 300 secondi. Per ogni puntamento è stato acquisito il primo membro in ordine lessicografico con coppia FLT/FLC della stessa esposizione e RAW associato in MAST. I file sono a campo intero. Il confronto applica ai FLT l'equazione fotometrica a raggio 3 con i coefficienti del ciclo 32 e usa le controparti FLC per una seconda elaborazione con correzione CALACS. [Piani ACS](https://www.stsci.edu/hst/instrumentation/acs/calibration/calibration-plans) · [Modello parallelo ACS](https://www.stsci.edu/hst/instrumentation/acs/performance/photometric-cte-corrections) · [Correzione pixel ACS](https://www.stsci.edu/hst/instrumentation/acs/performance/pixel-based-cte-corrections)

I tre JIF distinguono jfln02010 e jfln02030 in guida fine da jfln02020 in modalità `GYRO`, con RMS indisponibile. La prima selezione, ancorata alla posizione centrale, ha prodotto zero coppie. L'analisi esplorativa successiva ha escluso il puntamento centrale e ha preselezionato pixel puliti nell'intorno di ciascuna candidata. Il verificatore conserva 312 candidate e tutti i rifiuti. Quattro superano i controlli su associazione nel cielo, DQ di FLT e FLC, isolamento, fondo e separazione Y. La distanza fra i due centroidi sulla sfera è al massimo 0,0103″. Per tutte e quattro le stelle cambia anche il chip.

| Differenza Y, trasferimenti | FLT, mmag | FLC, mmag | FLT con modello parallelo, mmag |
| ---: | ---: | ---: | ---: |
| 1904 | +240,52 | +76,31 | +55,22 |
| 1561 | +282,68 | −117,64 | −63,68 |
| 560 | +13,39 | −30,65 | −43,89 |
| 1188 | +38,19 | −12,14 | −38,44 |

Il contrasto è la magnitudine strumentale ad alto Y meno quella a basso Y in ciascuna coppia. Le misure usano la PAM del rispettivo chip e raggio 3 pixel. In valore assoluto il contrasto diminuisce in tre casi con FLC e in due con il modello fotometrico. La prova non applica un riallineamento dei punti zero dei chip e le quattro stelle condividono la stessa visita. Il segnale comprende dipendenze di chip, risposta dell'apertura e la differenza tra correzione parallela e trattamento CALACS. Per discriminare i metodi occorre un insieme più ampio con coppie sullo stesso chip, o una calibrazione indipendente tra chip. Zero avvii nativi e zero chiusure scientifiche.

Replay della selezione a guida fine e maschera di riferimento più stretta byte per byte dagli archivi su H:. SHA-256 del riscontro `96ddcd8c8db4d7ebe0ee4615bead656b6146e6c77e3cc7372b5f54e3930a97e0`. SHA-256 archivio `fa14d047bfbb48f26cb378542c821184aa8876e377daecba81ee2d5026ce66b3`.

[Confronto FLT/DRZ del programma 17895](BKL-046-ACS-17895-CTE-CALCOLO.md).
