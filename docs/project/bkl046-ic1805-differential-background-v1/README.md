# BKL-046 · Fondo differenziale di IC 1805

Su cinque coppie reali di pose Bayer, il piano affine riduce almeno del 10% l’errore mediano assoluto sulle celle escluse dalla stima, senza aumentare il P90, in quattro coppie su cinque rispetto a un solo offset. Il modello quadratico soddisfa lo stesso criterio in tre. Le cinque coppie condividono la stessa posa di riferimento.

| Indice della posa | Mediana assoluta offset (ADU) | Mediana assoluta piano (ADU) | P90 offset (ADU) | P90 piano (ADU) |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 0,328 | 0,336 | 0,996 | 0,899 |
| 9 | 0,469 | 0,406 | 1,192 | 0,926 |
| 19 | 0,632 | 0,263 | 1,525 | 0,857 |
| 29 | 0,902 | 0,406 | 2,046 | 0,897 |
| 38 | 1,173 | 0,426 | 2,420 | 1,045 |

Le 30 iniezioni identiche nelle due pose, introdotte dopo il ricampionamento, restano nel risultato entro la precisione numerica. È un controllo della cancellazione nel differenziale. Nelle 30 iniezioni nella sola posa bersaglio si perde dal 50,2% al 90,4% del flusso in apertura. Nessuna soddisfa la tolleranza del 5% congiunta su flusso e forma. Anche l’offset costante sottrae parte del profilo esteso.

Il test usa la media dei due verdi CFA, una registrazione stellare affine già fissata, un fattore fotometrico unitario e celle separate per stima e verifica. Il controllo senza registrazione impiega la stessa maschera comune. I numeri misurano il residuo differenziale rispetto alla posa di riferimento. Restano aperti il fondo assoluto, la separazione del fondo comune, il ruolo della calibrazione e la risposta scientifica dei processi nativi di PixInsight. Nessuna chiusura scientifica in questo incremento.

Per ripetere, usare Python 3.12 con rawpy 0.25.1 (LibRaw 0.21.4), NumPy 2.3.5 e VC Runtime x64. Il programma riceve in ordine la directory del protocollo, la directory contenente `HeartNebula.zip` e la ricevuta del dataset, il percorso della ricevuta stellare, la directory del wheel rawpy estratto, la directory delle dipendenze, la directory DLL di VC Runtime e il percorso del rapporto. Gli hash dei dati e delle ricevute sono nel protocollo. Il kit di custodia include lo ZIP sorgente, le due ricevute e il wheel rawpy. [Catalogo originale](https://amor.cms.hu-berlin.de/~rodrigus/datasets.html)
