# BKL-046 · Aperture con DQ reale a confronto con pose integre della stessa visita

Ho riletto i 48 FLC WFC3/UVIS1 di GD153 del programma 11450. Per ogni posa in esame, il centro delle esposizioni integre della stessa visita e banda è proiettato sul suo WCS. La posa in esame è esclusa sia dalla previsione del centro sia dal riferimento fotometrico. Il confronto usa aperture di raggio 10 pixel, la mappa PAM e il fondo mediano fra 16 e 22 pixel. Il programma usa soltanto campioni finiti con DQ zero, registra i pixel mancanti e mantiene il veto sui flag di saturazione.

Delle quattro pose precedentemente respinte per DQ al nucleo, due hanno un confronto integro nella stessa visita e banda entro 0,05 giorni. Ciascuna ha un solo riferimento eleggibile. La tabella riporta la differenza di magnitudine rispetto a quel riferimento. I valori positivi indicano un flusso stimato inferiore a quello del confronto.

| Posa | Banda | Campioni mancanti (r10 / r3) | Somma parziale | Riscalatura per area | Mediana per anello |
| --- | --- | ---: | ---: | ---: | ---: |
| iaah11daq | F606W | 2 / 0 | +3,58 mmag | −3,40 mmag | +2,01 mmag |
| iaah13ewq | F438W | 8 / 1 | +61,36 mmag | +33,15 mmag | +43,82 mmag |

Il veto precedente usava una regione centrale quadrata. Nell'apertura circolare centrata tramite WCS, la posa F606W conserva tutti i campioni entro 3 pixel. Per la posa F438W, la mediana per anello resta da +42,85 a +45,97 mmag ai quattro spostamenti assiali di un quarto di pixel e al centro nominale. Nei dieci confronti fra pose integre, tutti con un solo riferimento, la massima differenza assoluta è 4,42 mmag al centro nominale. Questi confronti integri provengono da altri gruppi visita e banda e forniscono un controllo descrittivo.

La posa F438W mostra una differenza persistente rispetto al riferimento nella stessa visita. La procedura non osserva il flusso che si sarebbe misurato nella stessa posa integra e non attribuisce l'intera differenza ai pixel DQ. Il rapporto conserva anche le pose prive di riferimento, gli esiti ai cinque centri e le 23 misure nelle altre pose rifiutate per supporto. Rimangono aperti la propagazione dell'incertezza, la validazione su altre stelle, l'errore cromatico su terne realmente danneggiate e la verifica nativa. Nessuna chiusura scientifica o esecuzione PixInsight.

Per riprodurre, passare a `misura.py` il protocollo, la directory del kit delle pose del programma 11450, lo ZIP della fotometria indipendente, la directory con NumPy 2.3.5 e Astropy 7.2.0 e un nuovo file di risultato. Tutti i FITS usati, il protocollo d'origine e il rapporto di fotometria sono verificati per SHA-256. [Controllo cromatico a maschere indotte](../bkl046-gd153-geometric-color-coverage-v1/README.md)