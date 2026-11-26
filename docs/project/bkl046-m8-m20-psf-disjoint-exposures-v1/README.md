# BKL-046 · Orientazione PSF M8/M20 su pose disgiunte

Il controllo usa le stesse 19 stelle tenute da parte e 14 mosaici CFA calibrati. Ogni metà contiene sette esposizioni distinte. I centri di riferimento sono proiettati nelle singole pose con le matrici affini archiviate. Si usano i pixel rossi e blu del mosaico senza ricampionamento, con le maschere dei campioni validi. Il fit sceglie forma e larghezza su una metà, poi valuta le forme fissate sull'altra metà. Ampiezza e piano di fondo sono stimati per posa. Il controllo scambia infine i ruoli delle due metà.

| Banda | Valutazioni disponibili su 38 | Stelle con guadagno almeno del 10% in entrambe le direzioni | Stelle con orientazione ripetibile |
| --- | ---: | ---: | ---: |
| Rosso | 38 | 6 | 6 su 19 |
| Blu | 38 | 0 | 0 su 19 |

Le cinque stelle già ripetibili in rosso tra le calibrazioni A e B conservano lo stesso angolo discretizzato anche tra pose disgiunte. Tutte e cinque appartengono alla zona 12. Una sesta stella rossa proviene dalla zona 4. Nessuna stella ha un angolo ammesso in entrambe le bande. I centri non proiettati, usati in un controllo iniziale, lasciavano molti fit privi di ampiezza positiva. Il risultato qui riportato usa la convenzione riferimento-verso-posa del manifest.

Le metà condividono strumento, campo, calibrazione e soluzione astrometrica. Il confronto verifica la stabilità sulle esposizioni disponibili e mantiene aperti l'orientazione fisica, il trasferimento cromatico e la prova PixInsight. Il programma riceve protocollo, ZIP interno dei mosaici, ricevuta delle larghezze, dipendenze e un percorso di rapporto nuovo. [Verifica sui ritagli ricostruiti](../bkl046-m8-m20-psf-orientation-transfer-v1/README.md)