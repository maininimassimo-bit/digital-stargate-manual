# BKL-046 — Riferimento alternativo nelle pose da 509 s su Orione F658N

Quattro esposizioni ACS/WFC da 509 s del 14 gennaio 2004 sono state valutate sugli stessi tre candidati del censimento. Sono intercorse 16 giornate di calendario dalle due pose brevi del 29 dicembre 2003. Il test eredita il protocollo fotometrico e la coppia indipendente da 150 s. Per qualificare il riferimento alternativo richiede almeno due esposizioni da 509 s che passino individualmente il controllo primario.

| Candidato | Copertura 509 s | Esito fotometrico |
|---|---:|---|
| 5/5 | 2 su 4 | A raggio 3 px i due flussi disponibili sono il 21,28% e il 20,38% sopra la media delle pose brevi. La separazione massima fra i centroidi è inferiore a 0,027 arcsec. A raggio 5 px il supporto è incompleto. |
| 6/7 | 4 su 4 | A raggio 3 px il supporto o il segnale è insufficiente. Anche a 5 px il supporto è incompleto. |
| 18/22 | 4 su 4 | La coppia breve resta priva di un picco accettato in una delle pose. |

Zero superamenti al raggio primario di 5 pixel sui tre candidati e sulle quattro esposizioni. Nel candidato 5/5 le due pose da 509 s replicano uno scarto importante rispetto alle pose brevi anche con un intervallo temporale ridotto e centroidi concordanti. Il confronto non separa cambiamenti della sorgente, errori di calibrazione, differenze della PSF e fondo strutturato. Conservare il campione come caso negativo di comparabilità. Zero esecuzioni native e chiusure scientifiche.

Il replay usa i nuovi intervalli FITS fissati per origine, ETag e SHA-256. Usa le PAM e le misure delle pose brevi dal dossier fotometrico precedente. Lo script accetta directory di questo dossier, directory runtime, dossier degli header, percorso di output, modo replay, dossier fotometrico e dossier del censimento, in questo ordine.

[Esposizioni F658N](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/9a5d19b5f6ae35b9dcd7ca6880295602343b73ab/docs/project/bkl046-orion-acs-f658n-exposure-members-v1) · [Riferimento precedente da 340 s](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/2de60f08f7d7faf96dce9ef565527da3bb672296/docs/project/bkl046-orion-f658n-heldout-photometry-references-v1)
