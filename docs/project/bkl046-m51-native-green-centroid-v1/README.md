# Centroidi verdi nativi nelle pose RAW di M51

Il confronto BKL-046 usa tre RAW Canon EOS 6D. Il programma riesegue l’associazione con Gaia DR3 Lite e verifica l’identità byte per byte del rapporto precedente. Per ciascuna coppia conserva le sole stelle Gaia per cui entrambi i fotogrammi forniscono stime valide con tutti i metodi. Le stelle di verifica restano escluse dalla stima delle trasformazioni.

Il protocollo confronta il centro dalla preview a coppie con i centri ricavati dalle parità verdi G1 e G2. Il fit congiunto usa un centro e una forma comuni con ampiezze distinte. Una stella sintetica verifica il recupero del centro a meno di 0,04 pixel anche con ampiezze diverse. Il P90 della distanza fra G1 e G2 nelle tre pose reali vale 0,57, 0,63 e 0,43 pixel nativi.

| Confronto con la prima posa | Stelle di verifica | P90 similarità preview | G1 | G2 | Fit congiunto | Miglior P90 affine |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Centrale | 57 | 0,614 | 0,816 | 0,616 | 0,593 | 0,601 |
| Ultima | 51 | 0,790 | 0,779 | 0,915 | 0,847 | 0,810 |

Tutti i residui sono espressi in pixel nativi. Il fit congiunto migliora la posa centrale di 0,021 pixel e peggiora l’ultima di 0,056 pixel. Tutti i metodi superano la soglia diagnostica di 0,30 pixel. La selezione comune esclude stelle con un fit non valido o un centro fuori tolleranza. Il dato vale per queste tre pose e lascia aperta la verifica degli errori locali e della registrazione nativa. Lo studio si è svolto offline.

Per replicare eseguire `misura.py <protocollo.json> <studio-Gaia-precedente> <acquisizione-RAW> <sorgente-matcher> <rawpy-estratto> <pacchetti-Python> <directory-DLL-VC> <nuovo-riscontro.json>`. Il rapporto registra i pixel nativi, gli identificativi Gaia delle stelle di verifica in comune e le metriche complete di similarità e trasformazione affine.
