# BKL-046 · Trasferimento della correzione cromatica fra visite di GD153

La prova usa il rapporto WFC3 archiviato e verificato, con il limite di 0,05 giorni fra le tre bande. Dei 48 FLC di GD153 restano quattro terne con fotometria valida a entrambi i raggi, 5 e 10 pixel. Le terne provengono da due visite. Lasciandone fuori una, rimane soltanto una visita di confronto. Il requisito di due visite di stima lascia **zero predizioni empiriche verificabili**, sia aggregando i dither sia a dither uguale.

Una copia di lavoro precedente conteneva cinque terne su tre visite. Nell'archivio pubblicato, la quinta terna ha un intervallo di circa 0,05539 giorni ed è esclusa dal limite già adottato. L'identità di ogni ingresso è fissata nel protocollo. [Verifica numerica da cui provengono i dati](../BKL-046-WFC3-GD153-APERTURE-INDIPENDENTI.md)

Sulle quattro terne valide, con la mediana dell'anello 75–125 pixel, il cambio di raggio produce le seguenti variazioni mediane assolute.

| Colore ST | Senza correzione | Dopo correzione nominale | Unità |
| --- | ---: | ---: | --- |
| F438W − F606W | 1,50 | 2,13 | millimagnitudini |
| F438W − F814W | 6,96 | 2,00 | millimagnitudini |
| F606W − F814W | 6,23 | 1,65 | millimagnitudini |

La correzione nominale riduce l'escursione fra aperture nei due colori che includono F814W e la aumenta per F438W − F606W. La direzione dell'effetto mediano si conserva anche con la stima della moda nell'anello ampio e con la mediana nell'anello locale. I tre calcoli riusano le stesse pose e riguardano la stessa stella. Restano aperti il trasferimento fra visite, la variazione spaziale e cromatica della PSF e la validità su stelle e condizioni indipendenti.

Per replicare, passare a `misura.py` il protocollo, lo ZIP della verifica numerica archiviata e un nuovo file di risultato. Il programma verifica lo ZIP e il membro per SHA-256, poi ricalcola le differenze cromatiche dai flussi prima di confrontarle con i valori conservati. Zero avvii PixInsight e zero chiusure scientifiche.
