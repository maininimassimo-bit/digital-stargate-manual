# BKL-046 · Effetto della maschera DQ reale su aperture GD153 integre

Ho preso le due pose già respinte per DQ che avevano un confronto nella stessa visita. Ho proiettato la maschera DQ di ciascuna sulle aperture integre della stessa banda, senza usare il flusso della posa danneggiata. Nelle aperture di confronto il flusso e il fondo restano fissi. Conosco quindi l'errore prodotto dalla rimozione dei campioni nell'apertura integra. Il protocollo confronta il pixel più vicino e il supporto di quattro pixel al centro nominale e a quattro scarti assiali di 0,25 pixel.

Per F438W, la mediana per anello produce i seguenti intervalli. Valori positivi indicano una stima di flusso inferiore al riferimento. L'intervallo osservato sulla posa reale è **+42,85–45,97 mmag** rispetto alla posa integra della stessa visita.

| Pose integre su cui è applicata la maschera | Numero di pose | Pixel più vicino | Quattro pixel |
| --- | ---: | ---: | ---: |
| Posa integra della stessa visita | 1 | +1,05–13,54 mmag | +15,06–24,01 mmag |
| Pose di altre visite | 6 | −1,22–35,53 mmag | +10,15–85,10 mmag |

Sulla posa integra della stessa visita, l'errore indotto resta al di sotto della differenza osservata, con uno scarto minimo di 18,84 mmag fra valori allo stesso spostamento per il supporto a quattro pixel. Sulle altre visite, il supporto a quattro pixel produce anche errori vicini a quello osservato. Alla fase nominale della posa integra della stessa visita, la proiezione F438W nasconde 9 campioni di cui 1 nel nucleo con il pixel più vicino, e 20 di cui 3 nel nucleo con quattro pixel. La posa reale aveva 8 campioni mancanti, di cui 1 nel nucleo. Le regole di proiezione incidono sulla copertura e sull'errore.

In F606W, la differenza osservata con la mediana resta fra −0,48 e +2,01 mmag. Nella posa integra della stessa visita, il supporto a quattro pixel dà un errore indotto fra −3,51 e +0,02 mmag. Il rapporto conserva anche somma parziale e riscalatura per area, con 130 combinazioni complessive su una stella. Le fasi ripetono le stesse pose.

Il confronto evidenzia la sensibilità al campionamento delle pose integre. Resta aperta l'attribuzione dell'intera differenza osservata in F438W e resta assente il valore integro della stessa posa danneggiata. Nessuna chiusura scientifica o esecuzione PixInsight. [Confronto sulle pose realmente danneggiate](../bkl046-gd153-natural-dq-sibling-flux-v1/README.md)

Per ripetere, passare a `misura.py` il protocollo, la directory del kit FLC 11450, gli ZIP del confronto nella stessa visita, delle aperture integre, della copertura geometrica e della stima con maschere trattenute, la directory con NumPy 2.3.5 e Astropy 7.2.0 e un nuovo file di risultato. Il programma verifica le impronte dei pacchetti, dei moduli riutilizzati e di ogni FITS prima dell'uso.