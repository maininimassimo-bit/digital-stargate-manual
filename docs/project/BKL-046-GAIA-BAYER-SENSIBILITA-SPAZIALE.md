# BKL-046 · Sensibilità spaziale del trasferimento e disponibilità di spettri Gaia XP

L'asse FILTER_COLOR/3 resta aperto. Il controllo riparte dal confronto congelato IC 1805 → M8/M20. La mediana e il modello lineare sono ricostruiti dalle 18 stelle sorgente e verificati rispetto alle previsioni del rapporto precedente sulle 42 stelle di destinazione. La prova riguarda la differenza di colore Bayer tra aperture da 3 e 6 pixel.

## Sensibilità del risultato

Ho escluso a turno ciascuna delle otto zone sul campo di destinazione, mantenendo fisso il modello. In un controllo separato ho escluso a turno ciascuna delle otto zone del campo sorgente, ristimando sia il modello sia la mediana. Le omissioni misurano sensibilità a questi campioni. I risultati fra omissioni non sono repliche indipendenti né intervalli di confidenza.

| Metodo | Omissioni zona M8/M20 con P90 migliore, A / B | Omissioni zona IC 1805 con P90 migliore, A / B | Omissioni zona IC 1805 con bias assoluto peggiore, A / B |
| --- | ---: | ---: | ---: |
| drop 1,0 | 7/8 / 7/8 | 6/8 / 8/8 | 8/8 / 8/8 |
| drop 0,7 | 7/8 / 7/8 | 6/8 / 7/8 | 8/8 / 8/8 |
| Bilineare per parità CFA | 5/8 / 8/8 | 2/8 / 6/8 | 8/8 / 8/8 |

Limitando il confronto alle 37 stelle entro il supporto BP−RP di IC 1805, il P90 scende per tutti i metodi di 0,004–0,014 mag, mentre il bias mediano assoluto aumenta di 0,010–0,018 mag. Il compromesso fra coda e bias persiste anche entro il supporto cromatico. La correzione non è qualificata come trasferibile. [Motivazione del controllo per blocchi spaziali](https://doi.org/10.1111/ecog.02881)

## Spettri Gaia per il prossimo confronto

La query ESA ha restituito esattamente gli 81 identificativi richiesti. Tutti hanno rappresentazioni XP continue e campionate. Escludendo i duplicati Gaia e le sorgenti segnalate come variabili, rimangono 22/39 stelle di IC 1805 e 39/42 di M8/M20. L'assenza del flag di variabilità non implica una stabilità fotometrica dimostrata. Le richieste DataLink campionate di prova hanno risposto HTTP 503, quindi qui è verificata la disponibilità a catalogo. [Campi Gaia DR3](https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_main_source_catalogue/ssec_dm_gaia_source.html)

Il confronto assoluto richiede flussi Bayer lineari, stima di apertura e fondo con incertezza, e risposte spettrali complessive dei due sistemi. Il catalogo di IC 1805 indica EOS 40Da, mentre l'EXIF identifica EOS 40D. Il manuale ZWO documenta la camera M8/M20. La corrispondenza delle risposte ottiche effettive alle due acquisizioni va verificata prima di sintetizzare un colore strumentale di riferimento. [Dati IC 1805](https://amor.cms.hu-berlin.de/~rodrigus/datasets.html) · [Manuale ZWO ASI2600](https://i.zwoastro.com/zwo-website/manuals/ZWO_ASI2600_Manual_EN.pdf) · [Fotometria sintetica Gaia DR3](https://iris.cnr.it/bitstream/20.500.14243/515854/1/aa43709-22.pdf)

## Riproducibilità

- Archivio H: `Produzione/2026-10-13/Digital-StarGate-PixInsight/archives/BKL046-Bayer-Gaia-sensibilita-030d1288d38d.zip`.
- Sensibilità: SHA-256 `030d1288d38d63c3dc90cb1b65ef97ed665dc413b06e49c735bf1a201db2eb6b`.
- Censimento XP: SHA-256 `3a0672169b9981b3104c67ab8f64f7211c9b68d727e7374e059c534a23cc05cd`.
- Zero avvii nativi e zero chiusure scientifiche.
