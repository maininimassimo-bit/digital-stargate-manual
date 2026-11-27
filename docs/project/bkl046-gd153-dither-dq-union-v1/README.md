# BKL-046 · Copertura congiunta delle maschere DQ nelle visite di GD153

Ho riletto 48 FLC da otto visite. Le sei pose di id2406 restano escluse per il flag di esposizione. Sulle 21 coppie rimanenti, ho proiettato una griglia centrata sulla posizione Gaia prevista e ho contato quali punti possono essere serviti da almeno una delle due pose usando solo pixel finiti con DQ zero.

Con il pixel più vicino, una visita su sette, **icrw07**, copre l'intera apertura di raggio 10 in tutte le bande e in tutte e quattro le fasi. Con il supporto di quattro pixel attorno alla posizione proiettata, **nessuna visita** copre l'intera apertura, anche alla fase nominale. Tre visite mantengono il nucleo di raggio 3 completo con quattro pixel in tutte le bande e fasi. Con la finestra 4×4, il nucleo resta completo soltanto in icrw06.

| Visita | Peggior lacuna r10, pixel più vicino | Peggior lacuna r10, 2×2 | Peggior lacuna r10, 4×4 |
| --- | ---: | ---: | ---: |
| icrw06 | 1 | 7 | 62 |
| icrw07 | 0 | 6 | 67 |
| id2407 | 2 | 8 | 59 |
| iddn05 | 1 | 7 | 89 |
| iddn06 | 1 | 11 | 116 |
| idor02 | 3 | 15 | 120 |
| idor03 | 3 | 19 | 104 |

La tabella prende il massimo dei punti scoperti su bande e fasi. L'unione usa il WCS dei prodotti e la posizione Gaia già fissata. La copertura verifica un prerequisito geometrico. Non ricostruisce il flusso, non convalida l'associazione con il picco e non modifica i FITS. Un'apertura incompleta richiede un metodo validato sui campioni mancanti o ulteriori pose con copertura. Zero avvii PixInsight e zero chiusure scientifiche.

Per riprodurre, eseguire `misura.py` con il protocollo, i due kit GD153 precedenti estratti nell'ordine indicato nel protocollo, le dipendenze NumPy 2.3.5 e Astropy 7.2.0 e un nuovo risultato. [Visite 12334 e 14021](../bkl046-gd153-external-stare-visit-screen-v1/README.md) · [Visite 14384, 14883 e 14992](../bkl046-gd153-calibration-visits-core-dq-v2/README.md)
