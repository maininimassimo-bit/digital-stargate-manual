# BKL-046 — Concordanza del fit attraverso le esposizioni F555W di Orione

Ho trasferito le soglie di concordanza già fissate per gli standard CALSPEC alle cinque coppie pubblicate del dossier Orione. Si richiedono miglioramento del punteggio in tutte e quattro le partizioni di due esposizioni, escursione della separazione entro 20 mas, rapporto minimo/massimo delle stime di flusso almeno 0,70 ed escursione dell'asse entro 25 gradi. L'asse è confrontato modulo 180 gradi per evitare di interpretare uno scambio delle componenti come un disaccordo di orientamento.

Le stime dei centri del fit sono proiettate con la WCS originale e le correzioni di distorsione di ciascuna immagine. Il programma rilegge 63 intervalli FITS verificati per SHA-256 e non riottimizza le componenti. La separazione in cielo è distinta da quella nominale basata su 50 mas/pixel.

| Riga De Furio | Esposizioni misurabili | Concordanza fra esposizioni | Riscontro |
|---|---:|---|---|
| 2 | 2 | Sì | 42,9–46,9 mas. L'asse è entro 19,1 gradi dal riferimento. Una sola esposizione soddisfaceva anche la precedente tolleranza sul flusso pubblicato. |
| 3 | 2 | No | Le separazioni 58,1–61,0 mas e gli assi sono coerenti. Il rapporto minimo/massimo delle stime di flusso è 0,640. |
| 8 | 2 | Sì | 105,9–107,7 mas. L'asse è entro 1,9 gradi dal riferimento. Entrambe le esposizioni soddisfacevano anche le precedenti tolleranze sul flusso e sulla separazione. |
| 10 | 1 | Indisponibile | Due posizioni candidate sono fuori dai chip. |
| 14 | 2 | No | Guadagni, separazioni, assi e rapporti di flusso non soddisfano la concordanza. |

Il criterio di concordanza mantiene due delle quattro coppie con almeno due esposizioni misurabili. Una sola coppia soddisfa anche le precedenti tolleranze sul flusso pubblicato in entrambe le immagini. Le coppie selezionate e il riferimento condividono il programma HST GO10246. Le stime dei cinque casi descrivono la sensibilità di questo confronto, senza fornire una stima indipendente di accuratezza o completezza. Restano necessari casi indipendenti, controlli negativi con limiti di rilevabilità documentati e una procedura nativa approvata. Nessuna esecuzione nativa e nessuna chiusura scientifica.

[Riferimento di catalogo, tabella 1](https://arxiv.org/abs/1910.02092) · [Fit di Orione](https://github.com/maininimassimo-bit/digital-stargate-manual/commit/100daf1b1e1d0d4397870483c73f3a5da6b2ba81) · [Protocollo CALSPEC](https://github.com/maininimassimo-bit/digital-stargate-manual/commit/92d97b1a1198a0969a73037b4472d50bf7270b6b)
