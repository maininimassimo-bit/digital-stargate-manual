# BKL-046 · Errore cromatico dovuto alle lacune DQ in GD153

Ho propagato al colore gli errori di flusso della prova con campioni oscurati. Il confronto usa quattro terne WFC3 valide nelle tre bande entro 0,05 giorni, da due visite di GD153. Per ogni terna ho unito gli esiti delle tre bande della stessa visita maschera e dello stesso chip. Il colore di riferimento è quello della terna integra.

Il 90° percentile dell'errore assoluto di colore nei casi con almeno una lacuna nel nucleo è riportato in millimagnitudini. Ci sono cinque casi con la regola del pixel più vicino e dodici con la regola dei quattro pixel circostanti.

| Copertura | Colore | Somma parziale | Riscalatura per area | Mediana per anello |
| --- | --- | ---: | ---: | ---: |
| Pixel più vicino | F438W − F606W | 26,54 | 21,00 | 4,90 |
| Pixel più vicino | F438W − F814W | 28,60 | 22,64 | 20,76 |
| Pixel più vicino | F606W − F814W | 11,93 | 9,15 | 23,31 |
| Quattro pixel | F438W − F606W | 47,12 | 43,78 | 34,61 |
| Quattro pixel | F438W − F814W | 52,14 | 42,52 | 59,16 |
| Quattro pixel | F606W − F814W | 47,34 | 48,51 | 35,86 |

La mediana per anello aveva ridotto l'errore assoluto sul singolo flusso. Sul colore, il risultato dipende anche dalla correlazione fra gli errori nelle due bande. Con quattro pixel di supporto, la mediana per anello riduce il P90 in due colori e lo peggiora per F438W − F814W rispetto a entrambi i confronti. Il rapporto conserva anche i risultati per visita di riferimento e le aperture senza lacune.

Le combinazioni riusano pose e maschere. I percentili descrivono i casi del controllo e non una probabilità di errore su nuove stelle. Restano aperti i colori su esposizioni effettivamente danneggiate, la variabilità fra stelle, l'incertezza e la verifica nativa. Zero avvii PixInsight e zero chiusure scientifiche.

Per ripetere, passare a `misura.py` il protocollo, lo ZIP delle aperture integre, lo ZIP della prova con maschere e un nuovo percorso di risultato. [Misura sul singolo flusso](../bkl046-gd153-heldout-dq-flux-stress-v1/README.md) · [Terne fotometriche di riferimento](../BKL-046-WFC3-GD153-APERTURE-INDIPENDENTI.md)
