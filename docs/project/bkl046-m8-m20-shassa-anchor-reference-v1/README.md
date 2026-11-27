# BKL-046 · Riferimento Hα indipendente per le celle M8/M20

Il test proietta le sei celle del rivelatore sulle mappe SHASSA di due campi osservati in date diverse, mediante la soluzione astrometrica congelata di M8/M20. Usa le mappe smussate con continuo sottratto. Il protocollo fissa raggi di 2 e 4 arcmin e una copertura minima del 90%. Le mediane sono in Rayleigh. Si mantengono i pixel validi con segno e si escludono i valori FITS `BLANK`. [Atlante SHASSA](https://amundsen.astro.swarthmore.edu/SHASSA/) · [Gaustad et al. 2001](https://arxiv.org/abs/astro-ph/0108518)

| Campo | Data UTC riportata nel FITS | Celle misurate | Intervallo delle mediane a 4 arcmin |
| --- | --- | ---: | ---: |
| 153 | 1998-09-23 | 6/6 | 75,3–800,3 R |
| 119 | 1998-07-01 | 2/6 | 214,8–789,0 R |

Sulle due celle condivise, le differenze 119 meno 153 a 4 arcmin sono +5,9 e −11,3 R. A 2 arcmin sono +17,5 e −88,1 R. Le quattro celle fuori copertura nel campo 119 restano nel rapporto. Il contrasto spaziale osservato mostra che le sei celle possono includere emissione astronomica strutturata. SHASSA misura una banda stretta e le mappe hanno attraversato la riduzione dello stesso atlante. Restano da qualificare un fondo ottico coevo, la risposta di banda della camera e la conversione in ADU. Zero avvii PixInsight e zero chiusure scientifiche. [Campo 153](https://amundsen.astro.swarthmore.edu/SHASSA/ImagePages/153.html) · [Campo 119](https://amundsen.astro.swarthmore.edu/SHASSA/ImagePages/119.html)

Replica con NumPy 2.3.5 e Astropy 7.2.0. Il protocollo identifica cinque ingressi per impronta. L'archivio H/K conserva le mappe originali e i riferimenti congelati per la sola replica. Astropy segnala una scheda PDAY non standard in un FITS. La verifica astrometrica usa la matrice CD e controlla l'inversione della proiezione di partenza.

```text
python -I -B -S misura.py protocollo.json <directory-ingressi> <dipendenze> riscontro-replica.json
```

Dati SHASSA prodotti con il supporto della National Science Foundation.
