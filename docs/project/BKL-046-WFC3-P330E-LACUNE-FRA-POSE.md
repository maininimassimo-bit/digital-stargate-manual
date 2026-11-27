# BKL-046 · Verifica delle lacune DQ fra pose P330E

Per ogni coppia della stessa visita, banda e sensore, la prova proietta nella seconda posa i centri dei pixel validi del nucleo 7 × 7 della prima, tramite la WCS dei due prodotti FLC. Esclude dal fit i pixel il cui vicino più prossimo nella seconda posa ha DQ diverso da zero. Ripete il procedimento invertendo i ruoli. L’altra posa fornisce la maschera. Le intensità usate per la verifica sono misurate nella posa su cui si esegue il fit. Il vicino più prossimo definisce la selezione dei pixel e non ricampiona l’intensità. La coppia per cui una posa non soddisfa il criterio di identità del picco resta esclusa in entrambe le direzioni.

Il fit usa i rimanenti pixel finiti e con DQ zero in un’apertura di raggio 10 pixel. Stima ampiezza positiva, fondo costante e centro sulla griglia a 1/32 di pixel. Confronta la scelta fra soli piani di indice pari e la loro interpolazione. La metrica è l’RMSE dei pixel esclusi, divisa per il picco osservato del nucleo. La tabella riporta la mediana e il massimo per posa.

| Banda | Pose | Pixel verificati | Mediana, discreto | Mediana, interpolato | Massimo, interpolato |
| --- | ---: | ---: | ---: | ---: | ---: |
| F438W | 8 | 23 | 2,56% | 2,51% | 19,30% |
| F606W | 6 | 19 | 7,33% | 6,28% | 14,15% |
| F814W | 8 | 24 | 2,49% | 2,27% | 15,42% |

Il modello interpolato migliora otto confronti direzionali, ne lascia tredici invariati e ne peggiora uno. Le direzioni della stessa coppia non costituiscono repliche indipendenti. Il test riguarda la previsione di 66 valori misurati in posizioni che approssimano la geometria delle lacune. Dove entrambe le pose sono prive di supporto non esiste un valore di controllo. L’RMSE normalizzato dei singoli pixel non misura il flusso integrato né il colore. Il risultato non cambia l’ammissibilità delle visite. Gli assi FILTER_COLOR/2 e FILTER_COLOR/3 restano aperti.

| Evidenza | SHA-256 |
| --- | --- |
| Protocollo | f9826fce8969046af6a00c0670ed53c3ae1abf224604f743b6a09bee6e7ea03d |
| Programma | cb3b19fa1301894117f337c18edc8e134198199e4aac40529d1220287a2ed64a |
| Verifica | b7ba50934b031a6ce3aa19337931777d1e157cfa73df1342b8fa49b3518f36c6 |
| Ricevuta, riprodotta da H: | fc1fe8c5a3348887dc8b9c67e983abf039c7fb1fc468b9ad47e76b59560993cb |
