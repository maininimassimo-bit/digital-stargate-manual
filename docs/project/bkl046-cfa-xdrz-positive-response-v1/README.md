# Quota di peso da variazioni positive del segnale CFA

La prova tiene fissi i tre ingressi, la geometria, lo schema CFA e le impostazioni del controllo senza rigetto. Nei due bracci aggiuntivi sostituisce soltanto i valori dei due pixel verdi della posa B con livelli strettamente positivi. Il confronto misura due pendenze rispetto al braccio di base per ciascuna cella. Sono determinazioni sullo stesso campo con la stessa baseline.

| Cella verde nel riferimento | Livelli del pixel in ingresso | Intensità attesa in uscita | Pendenze attese |
| --- | --- | --- | --- |
| (13, 8) | 0,75 · 0,25 · 0,50 | 0,50 · 0,25 · 0,375 | 0,50 · 0,50 |
| (14, 7) | 0,80 · 0,30 · 0,55 | 0,49 · 0,24 · 0,365 | 0,50 · 0,50 |

In una media lineare con pesi fissi, il rapporto tra variazione dell’uscita e variazione dell’ingresso stima la quota del peso della posa B nella cella. Due pendenze coerenti e l’assenza di variazioni altrove sul supporto previsto sono controlli del modello in questi punti. La prova deve mantenere rigetto, pesatura adattiva e normalizzazione disattivati e verificare i parametri nativi effettivi prima di interpretare le pendenze. Il metodo non ricava il peso assoluto o il divisore usato per esportare la mappa. Il collaudo offline respinge una risposta non lineare e una variazione su un pixel estraneo.

Per generare eseguire `risposta.py <kit-originale-a-tre-ingressi> <pacchetti-Python> <nuova-directory>`. Per confrontare le intensità lineari FITS, il terzo argomento diventa il nome di un nuovo JSON e si aggiunge `--exports <directory>` con i file `baseline-rgb.fits`, `first-rgb.fits` e `second-rgb.fits`. La rilettura di esempio usa le mappe previste dal modello. Le misure native richiedono un launcher revisionato e l’ammissione del coordinatore.
