# BKL-046 — Replica fotometrica ACS 11677 nelle visite 09 e 11

Il [primo confronto](BKL-046-ACS-11677-FOTOMETRIA.md) usava le visite 01 e 04. Nelle altre quattro visite del censimento iniziale, nessuna delle 103 combinazioni di coppie con durate abbinate condivideva la stessa soluzione Gaia nel chip WFC1. Il replay di questo risultato ha prodotto lo stesso SHA-256.

L'estensione ha verificato 4.998 record MAST in due forme di paginazione, coprendo 48 associazioni nelle 24 visite del catalogo. Ha letto i metadati FITS di 266 esposizioni. Escludendo le visite 01 e 04, il controllo incrocia 4.526 combinazioni di quartetti a durata abbinata entro lo 0,1%, verificando 220 headerlet. Di queste, 3.266 hanno la stessa soluzione Gaia WFC1, 732 hanno almeno un punto utile sullo stesso semichip con una differenza di almeno 550 trasferimenti in entrambi i filtri e 698 rispettano anche la soglia esplorativa di 1.400 s per esposizione. La soglia è stata fissata prima di misurare i nuovi FITS per escludere le pose brevi dal confronto con le precedenti pose da 1.457 s. [Archivio scientifico STScI](https://archive.stsci.edu/prepds/deep47tuc/)

La selezione usa il quartetto con il maggior numero di punti utili fra i 698 casi. Le esposizioni F606W e F814W delle visite 09 e 11 risultano rispettivamente da 1.442 s e 1.443 s. I FITS completi e i log di guida confermano le identità, le durate e lo stato FINE LOCK. Delle 13.643 rilevazioni iniziali, 3.790 ricadono nell'area utile e 235 passano i controlli geometrici dopo il ricentraggio. Tra le rilevazioni ammesse a raggio 3 px nelle due coppie di visite risultano zero corrispondenze entro 0,1 arcsec.

| Coppia di visite | Raggio px | Rilevazioni ammesse | Mediana di valore assoluto Δcolore FLT | FLC | CTE parallela |
| --- | ---: | ---: | ---: | ---: | ---: |
| 01 e 04 | 3 | 7 | 40,15 mmag | 39,57 mmag | 52,83 mmag |
| 09 e 11 | 3 | 49 | 30,50 mmag | 31,42 mmag | 30,56 mmag |
| 09 e 11 | 5 | 2 | 110,26 mmag | 149,69 mmag | 112,82 mmag |

A raggio 3 px la riduzione di valore assoluto per FLC riguarda 28 rilevazioni su 49 nella replica e 7 su 7 nel primo confronto. Nella replica la mediana delle differenze appaiate rispetto a FLT è −1,56 mmag per FLC e +0,30 mmag per la CTE parallela. Questo indicatore calcola prima la differenza per ciascuna sorgente. La tabella riporta invece la mediana di ciascun metodo. Il confronto a raggio 5 px resta limitato a due sorgenti ammesse in entrambi i raggi. Il campionamento per massimi locali e la selezione tramite maschera DQ limitano le conclusioni al sottoinsieme misurato. Restano da verificare la sensibilità alla selezione e la riproducibilità su dati indipendenti dal programma 11677.

| Evidenza | SHA-256 |
| --- | --- |
| Archivio delle quattro visite iniziali | 25c1b010ed9af5aa03b335f87c82f32b795dd36c15691a4ab55d92e3a882f946 |
| Inventario completo dei prodotti | 551efc222ae4b413fe561ae6cd7fe24f559a1f88e0c77c5b0bdb398397b70342 |
| Selezione delle quattro pose lunghe | 57927b43b71798737beab5a91a8f72f5e4a212239e400075f579155d2c96a4cc |
| Riscontro fotometrico con replay identico | fcd5093b4afa0c11f00a88e2d391e6dd3ea99e27c3a85ae3f812440bb019dfa7 |
| Riepilogo comparativo | 2956268e9e08457e11b8196eb059f709cd30c6c53e1eb7ec81ae7bbed1f6a7d6 |
| Archivio dell'estensione su H: | d5a0e323eef5ee533047ff6fd0572a6c4af4bd87a77dcf4cdfcb6803f1b3e1fe |

L'incremento aggiunge una replica offline con gli stessi controlli. Zero chiusure scientifiche e zero avvii nativi in questo incremento.

Il [controllo di sensibilità successivo](BKL-046-ACS-11677-SENSIBILITA.md) identifica 46 sorgenti distinte nelle 49 rilevazioni a 3 px delle visite 09 e 11. Le statistiche di questa pagina si riferiscono alle rilevazioni prima della deduplicazione.
