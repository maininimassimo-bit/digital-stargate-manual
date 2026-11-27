# BKL-046 — Trasferimento della correzione overscan al 27 febbraio TV4

Ho applicato al 27 febbraio 2003 i coefficienti per quadrante calcolati solo sui [dark del 2 marzo](BKL-046-TV4-OVERSCAN-PER-RIGA.md). Il piano comprende otto gruppi FLAT24 MRI in modalità 1 nei due periodi della giornata. Fra le 68 immagini del registro, 67 hanno coppia FITS ed etichetta verificata con i checksum PDS. Un'immagine figura solo nel registro. Escludo dal calcolo altre 27 immagini. Tre sono prive di conferma Hall del filtro e 24 hanno pixel fuori dal supporto di DN già fissato. Le posizioni escluse restano nell'ordine originale e le coppie contigue non vengono ricomposte. [Archivio NASA TV4](https://pds.nasa.gov/ds-view/pds/viewProfile.jsp?dsid=DIF-CAL-HRII%2FHRIV%2FMRI-2-GROUND-TV4-V1.0)

| Gruppo | Tempo comandato | Coppie e quadranti con varianza ridotta | Rapporto mediano della varianza |
| --- | ---: | ---: | ---: |
| AT | 0 ms | 12/12 | 0,58 |
| AZ | 50 ms | 4/4 | 0,79 |
| BB | 500 ms | 6/12 | 1,00 |
| CY | 0 ms | 23/24 | 0,54 |
| DI | 500 ms | 3/16 | 1,02 |

I rapporti confrontano la varianza delle somme 16 × 16 pixel con e senza correzione per singola riga. Nei gruppi BF, DG e DN non resta una coppia entro il dominio fissato. Il beneficio a comando zero si ripete a circa 256 K e 241 K. I due gruppi da 500 ms danno un risultato nullo o sfavorevole. I risultati riportano verifiche per coppia e quadrante e conservano i limiti della sessione. Le varianti con raggruppamenti da 4 o 16 righe non risolvono la perdita di beneficio nei gruppi luminosi. L'offset relativo all'overscan a comando zero è diverso da quello del 2 marzo, quindi i livelli medi tra date richiedono un riferimento dedicato.

Questo riscontro estende l'evidenza a una data tenuta fuori dall'adattamento e a due temperature del CCD. La contaminazione ottica dell'overscan, la conservazione del flusso in un campo reale e la prova nativa restano aperte.

| Evidenza | SHA-256 |
| --- | --- |
| Riscontro e replay identico | d65dd43eee134798d3d583d6da508bc15cd50a9e40981d51374daec3af6746c8 |
| Archivio riletto su H: | 38e89eef065955fcbceb92659940c4802b8aef965511a9fb831054fd5a1c7ac2 |

Zero chiusure scientifiche e zero esecuzioni native in questo incremento.
