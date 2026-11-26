# BKL-046 — Pose ACS/WFC F658N sovrapposte nella nebulosa di Orione

La ricerca MAST interroga le immagini ACS/WFC con centro catalogato entro RA 83,75–83,89° e Dec −5,46–−5,32°. La risposta completa contiene 326 righe. La ricerca geometrica interpreta i poligoni catalogati e valuta una griglia di 19 × 19 punti con passo 0,005°. Il campione F658N con il maggior numero di durate catalogate è attorno a RA 83,7996° e Dec −5,4097°. Il confronto copre anche il punto di ricerca vicino al Trapezio. La query limita i centri delle osservazioni e può omettere impronte che entrano nel campo da un centro esterno.

| Programma e gruppo | Totale indicato da MAST | Pose individuali verificate negli header FLC | Data UTC |
|---|---:|---|---|
| GO 9898 / j8mf01010 | 300 s | 150 + 150 s | 2003-12-29 |
| GO 10246 / j93k0aofq | 340 s | 340 s | 2005-04-06 |
| GO 13419 / jcaz07010 | 1.596 s | 774 + 822 s | 2015-01-31 |
| GO 9825 / j8oc01010 | 2.036 s | 509 × 4 s | 2004-01-14 |

Ho verificato nove header indipendenti dei prodotti FLC. Tutti riportano ACS/WFC, F658N e guadagno 2 e⁻/ADU. Gli header fissano inoltre il filtro complementare, l'apertura, l'epoca, l'ETag della copia pubblica e lo SHA-256 dei primi 65.536 byte. I membri, i legami con le associazioni e le durate sono nel riscontro.

I poligoni supportano la selezione dei candidati. La copertura effettiva va ancora confermata con WCS per chip e maschere di qualità. Le date differiscono e il confronto richiede controlli per variabilità, orientamento, registrazione, risposta strumentale e saturazione effettiva. Questo caso riguarda una banda astronomica separata. La prova CFA con posa intermedia indipendente resta aperta. Zero esecuzioni native e chiusure scientifiche.

L'archivio H conserva le due risposte MAST usate dai verificatori, le richieste, i prefissi FITS, le ricevute HTTP e i rapporti. Per il replay eseguire verifica.py passando directory del dossier e percorso di output. Lo stesso formato vale per verifica-intestazioni.py, che legge il report geometrico riscontro.json come ingresso con hash fissato.

[Programma ACS di Orione](https://archive.stsci.edu/prepds/orion/) · [API MAST](https://mast.stsci.edu/api/v0/_services.html) · [Archivio pubblico dei FITS HST](https://registry.opendata.aws/mast-hst/)
