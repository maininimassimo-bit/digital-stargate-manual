# BKL-046 · Finestra originale nel controllo dell'origine XDRZ

Il collaudo usa i moduli CFA v4 per legare PID, ora di creazione, sessione e HWND della finestra originale. Prima della chiusura, il driver rilegge l'impronta della ricevuta del classificatore e la confronta con quella associata allo stesso contesto. La ricevuta è prodotta dal verificatore effettivo su file sintetici.

| Scenario | Esito |
| --- | --- |
| Ricevuta integra e finestra originale | BMP con i pixel del testimone atteso, una chiusura ordinaria ricevuta dalla finestra, scomparsa dell'HWND e uscita zero osservata dall'handle originale. |
| HWND di una seconda finestra con lo stesso titolo | Acquisizione e chiusura respinte. Entrambe le finestre restano vive fino alla pulizia del test. |
| Ricevuta modificata dopo l'acquisizione | Chiusura respinta anche con BMP verificato. |

Nei tre casi il testimone estraneo non riceve WM_CLOSE. Le finestre del collaudo usano SW_SHOWNOACTIVATE. Il rapporto conserva gli esiti riproducibili senza pubblicare le schermate. Nessun accesso al registro canonico, nessuna ammissione e nessun avvio di PixInsight. Restano l'integrazione di questi controlli nello stesso parent R4 con custodia di ingressi e archivio, la revisione e la prova ammessa. [Verifica congiunta dei prodotti](../bkl046-cfa-origin-bound-batch-evidence-v1/README.md)

Il collaudo riceve la sua directory, i moduli esatti inclusi nel kit, il kit del verificatore del batch, le dipendenze e la destinazione del rapporto. Si esegue nella sessione Windows interattiva di DSG-Shared con Python 3.12.