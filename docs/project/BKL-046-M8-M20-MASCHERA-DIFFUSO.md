# BKL-046 · Mascheramento del segnale diffuso nelle pose M8 e M20

Le 729 iniezioni riprendono gli stessi riquadri, profili e ampiezze della prova sulla scelta del fondo. La maschera operativa esclude le celle con residuo positivo oltre tre scale robuste e si estende di una cella intorno a ciascuna esclusione. Viene ricalcolata prima e dopo l'iniezione usando solo l'immagine corrente. Il controllo con profilo noto esclude invece qualsiasi cella che raggiunga il 2% del picco iniettato e usa la stessa maschera nei due passaggi. Entrambi i procedimenti selezionano piano o quadratica sulle celle di verifica e si astengono se mancano almeno 12 celle in uno dei due gruppi o se il fit è mal condizionato.

| Profilo | Senza maschera, entro 5% su flusso e forma | Maschera dai dati, entro 5% / astenuti | Profilo noto, entro 5% / astenuti |
| --- | ---: | ---: | ---: |
| Filamento corto, 324 | 0 | 15 / 5 | 324 / 0 |
| Filamento lungo, 324 | 0 | 5 / 11 | 324 / 0 |
| Diffuso largo, 81 | 0 | 0 / 0 | 0 / 81 |

Sul diffuso largo la maschera automatica procede in tutti gli 81 casi, con perdita mediana del 91,5% nel flusso centrale. Il controllo con profilo noto si astiene in tutti i casi per mancanza di celle di fondo. Sui filamenti il controllo mostra che la geometria consentirebbe di preservare il segnale se fosse disponibile una maschera affidabile. La maschera automatica ne recupera solo 20 entro soglia. I casi riusano le stesse pose e regioni e il profilo noto è un controllo, non un risultato operativo. Restano da verificare una regola di astensione utilizzabile senza verità in ingresso, un campo indipendente e la prova nativa. Zero chiusure scientifiche.

SHA-256 della ricevuta `219dc1040623a518ede46112be63436942dcda90b6eca3f243bd218a5245a775`.
