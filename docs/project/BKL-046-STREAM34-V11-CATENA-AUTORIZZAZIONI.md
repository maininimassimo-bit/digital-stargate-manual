# BKL-046 · Passaggio dai verbali alla sessione Stream34 v11

La verifica offline su DSG-Shared lega il fascicolo del launcher v11 all’autorità di sessione inclusa nel pacchetto. Il soggetto è `0b029846da0412875e26595e2ead8361bc35fcef2c882ec2be95303b9582bdd1`. Il test passa al verificatore d’ingresso i verbali ARB e RQ firmati da due chiavi effimere distinte. Verifica poi che il modulo di autorità della stessa candidata accetti le identità di test dell’operatore e del supervisore interattivo per la medesima iscrizione.

Sono stati respinti 13 casi. Comprendono impronte errate, firma d’iscrizione di un altro ruolo, scadenza, directory o provider diversi, soggetto diverso, verbale diverso, chiavi locali scambiate, due ruoli contemporanei e riuso della stessa chiave pubblica. L’esecuzione ripetuta a partire dallo ZIP e dal verificatore d’ingresso conservati su H: ha prodotto la stessa ricevuta.

Il collaudo usa esclusivamente chiavi di prova. Lo stato operativo resta in attesa dei verbali reali ARB e RQ per il soggetto v11, dell’impronta di fiducia dal canale autorizzato e delle attestazioni successive di deployment e iscrizione. La richiesta di ammissione resta da presentare al coordinatore.

| Evidenza | SHA-256 |
| --- | --- |
| Modulo di autorità v11 | 5c9bebd706ae1d58c29bc0d74b052228a701788b332433f3a1ddb153e1e82ab1 |
| Programma di test | aad9ea77b1e117315f2c0ea19fe0b6a637b6f4609842a037c7f27999eb2b4e49 |
| Ricevuta riprodotta da H: | 4670648e0fc32bf271786eceb7d6e3b870aa62761c25ea02efcd54b0e4515513 |
