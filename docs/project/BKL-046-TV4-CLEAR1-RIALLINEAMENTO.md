# BKL-046 — Riallineamento della sfera tra i gruppi TV4

Il registro MRI del 2 marzo 2003 documenta la correzione dell'allineamento della sfera da 24 pollici fra i gruppi CR e CT e le ripetizioni DA e DB. L'associazione per nome immagine, modalità, filtro, ora e durata identifica tutti i 40 fotogrammi del test ABBA. Il catalogo ufficiale dei checksum corrisponde a tutti gli 80 FITS ed etichette usati. Il rapporto di laboratorio descrive la vignettatura osservata prima della correzione. [Registro MRI](https://pds-smallbodies.astro.umd.edu/holdings/dif-cal-hrii_hriv_mri-2-ground-tv4-v1.0/document/imagelog/tv4_mri.asc) · [Rapporto del 2 marzo](https://pds-smallbodies.astro.umd.edu/holdings/dif-cal-hrii_hriv_mri-2-ground-tv4-v1.0/document/reports/report_20030302.asc)

| Durata | Prima del riallineamento | Dopo il riallineamento |
| --- | --- | --- |
| 7.503,5 ms | CR, 10 fotogrammi | DB, 10 fotogrammi |
| 15.003,5 ms | CT, 10 fotogrammi | DA, 10 fotogrammi |

Dopo la sottrazione dell'overscan parallelo e la normalizzazione al centro, la differenza dei profili spaziali prima e dopo il riallineamento si ripete alle due durate. Sui 1.280 blocchi delle cinque regioni, la correlazione delle due mappe di differenza è 0,999994. Nelle due regioni alle righe 64–319 dell'array, la risposta relativa al centro aumenta rispettivamente dell'8,86% e del 5,24% a 7.503,5 ms e dell'8,81% e del 5,21% a 15.003,5 ms. Nelle due regioni alle righe 704–959 la variazione assoluta resta sotto lo 0,16%.

Con due parametri e un gruppo trattenuto per volta, un tasso con salto al riallineamento ha RMS predittivo di 3,01 DN. Il tasso con deriva temporale lineare ha RMS di 25,40 DN. I quattro gruppi provengono dalla stessa sessione di laboratorio. Questo è un confronto predittivo interno del cambiamento documentato.

Il registro contiene sette acquisizioni SRC24 con lo stesso rivelatore, tutte fuori dall'intervallo del test ABBA. Le indicazioni VA nel registro sono impostazioni della sfera. Il log termico contiene sette temperature e i campi orari e documenta un disallineamento fino a circa 30 minuti rispetto all'orologio delle immagini. Le fonti esaminate non forniscono una misura indipendente della dose per i 40 fotogrammi. La sequenza identifica un cambiamento della forma spaziale associato al riallineamento. La risposta assoluta e la causalità quantitativa restano aperte. [Etichetta del log termico](https://pds-smallbodies.astro.umd.edu/holdings/dif-cal-hrii_hriv_mri-2-ground-tv4-v1.0/data/templog/templog_tv4_mri.lbl)

| Evidenza | SHA-256 |
| --- | --- |
| Riscontro e replay identico | de85d311ebaf2ecad7839bf6055ed3b78c49878277bf2f893a826677e3c64c92 |
| Archivio di documenti e verificatore letto su H: | 6e6b141a78f08e5d58e63e17400277f7c8f9a667a4e4ea03c773787fbb8b5f09 |
| Archivio dipendente con i 40 FITS e le etichette | d6d5e0b68f7b5c4f896d8d30a9569ad9afc24020e4f34aeb44cf4a8d92ea9a7a |

Zero chiusure scientifiche e zero esecuzioni native in questo incremento.
