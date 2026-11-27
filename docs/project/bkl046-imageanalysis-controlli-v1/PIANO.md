# BKL-046 — Controlli sintetici per ImageAnalysis

Quattro FITS UInt16, 192 × 192 pixel, con 36 stelle gaussiane per file e fondo mediano pari a 1200 ADU. Il generatore ha riprodotto byte per byte tutti e quattro i file. Una seconda implementazione li ha aperti e verificati con Astropy 7.2.0. [Impronte e statistiche del fondo](riscontro.json) · [Rilettura indipendente](rilettura-fits.json)

| Confronto | Controllo | Ipotesi da distinguere |
| --- | --- | --- |
| `compact-shuffled` e `compact-zones` | Identici istogrammi a pieno frame, stessa PSF e stessi pixel stellari. La dispersione delle differenze orizzontali nel fondo passa da 23,635 a 1,744 ADU. | Un estimatore basato solo sull'istogramma restituisce lo stesso valore. Una differenza riproducibile indica sensibilità alla struttura spaziale o alla selezione dei campioni. |
| `compact-shuffled` e `tailed-shuffled` | Stesso campo stellare. Nel fondo la MAD non riscalata scende da 14 a 8 ADU mentre la deviazione standard cresce da 23,635 a 53,630 ADU. | Il verso della risposta distingue i riferimenti MAD e deviazione standard per questi dati. Non identifica da solo la formula o la maschera nativa. |
| `compact-shuffled` e `compact-wide-psf` | Stesso fondo, anche nella disposizione dei pixel. La FWHM gaussiana nominale passa da 3,297 a 4,827 pixel. | Verifica il verso della risposta FWHM. La dispersione a pieno frame cambia con le stelle e va confrontata separatamente da quella del fondo. |

Per la futura prova, fissare versione e impronta del DLL, parametri di misura e ordine dei frame. Usare una cache vuota per ciascuna replica, leggere la tabella nativa senza arrotondamento e conservare `measurementSigma`, `measurementNoise`, `measurementFWHMpx`, `measurementStars` e i descrittori WBPP associati ai singoli percorsi. Ripetere in un ordine diverso per individuare dipendenze dalla sequenza. Un esito mancante o una riga ambigua lascia il confronto inconcludente. Confrontare i valori in scala nativa e in ADU usando un solo fattore documentato per tutta la serie.

I valori sono riferimenti sintetici, con maschera del fondo nota al generatore. La prova nativa resta da ammettere. Il confronto su frame astronomici indipendenti resta da eseguire per la validazione scientifica. [Generatore](genera-controlli.py) · [Verificatore FITS](verifica-fits.py)
