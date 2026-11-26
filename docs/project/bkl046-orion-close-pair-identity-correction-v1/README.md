# BKL-046 — Correzione dell'identità e del centro dei riquadri F555W

La risoluzione esatta degli alias in SIMBAD riconduce H97 232 a KZ Ori e H97 345 a V1487 Ori A. I rispettivi identificativi Gaia DR3 vengono verificati nel VOTable custodito. Propagando le posizioni fra J2016.0 e J2000 si riproducono le coordinate SIMBAD, poi le stesse sorgenti vengono proiettate sui quattro FITS F555W alle date di osservazione.

| Sistema | Scarto sul chip rispetto al centro precedente | Riquadri precedenti che contengono la posizione aggiornata | Pixel full well nel nuovo disco di raggio 3 px |
|---|---:|---:|---:|
| H97 232 | 29,12 / 28,86 px | 0 su 2 | 27 / 28 |
| H97 345 | 29,43 / 28,44 px | 0 su 2 | 15 / 23 |
| H97 488 | Alias ambiguo fra due oggetti, Parenago 1867 e 1866 | Da verificare | Non misurati dopo la correzione |

I quattro riquadri precedenti non includevano la posizione aggiornata. Il risultato precedente su H97 345 come controllo insaturo e i fit ottenuti centrandosi sui vecchi massimi non sono attribuibili con affidabilità al sistema indicato. I nuovi massimi sono a 0,06–0,13 arcsec dalla posizione Gaia propagata. Il fit con la stessa libreria empirica STScI riduce il residuo nei quattro confronti H97 232, ma restituisce 3,93–4,00 px, al limite superiore della ricerca e senza conferma della separazione indipendente. Per H97 345 la stima cambia da 2,75 a 4,00 px fra le due pose e le due suddivisioni. La separazione e il rapporto di flusso restano non qualificati. Zero esecuzioni native e chiusure scientifiche.

Il replay ricostruisce il rapporto e i quattro riquadri dai blocchi FITS e dalle risposte catalografiche archiviate. Il fit conserva il codice e la libreria del dossier ePSF precedente, verificati per impronta, con un protocollo che fissa il nuovo rapporto di centraggio.

[SIMBAD di CDS](https://simbad.cfa.harvard.edu/simbad/) · [Gaia DR3, tabella gaia_source](https://doi.org/10.17876/gaia/dr.3/1) · [Confronto ePSF precedente](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/2cf4db3b482abf7501608271603b1f47865bd908/docs/project/bkl046-orion-close-pair-f555w-epsf-v1)
