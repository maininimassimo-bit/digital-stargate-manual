# BKL-046 · Sensibilità del colore Bayer all'estinzione atmosferica

L'asse FILTER_COLOR/3 resta aperto. Il test applica ai flussi Gaia XP i coefficienti tabulati ESO di La Silla con trasmissione 10^(−0,4 X kλ). X varia tra 1 e 3 e X=0 costituisce il riferimento senza atmosfera. La curva serve a misurare la sensibilità dei risultati. Le condizioni atmosferiche delle acquisizioni restano sconosciute. [Coefficienti ESO](https://www.eso.org/sci/observing/tools/Extinction.html)

Il controllo legge le 15 intestazioni FITS grezze di M8/M20, distribuite su 46,7 minuti. In nessuna è presente un campo di massa d'aria o una delle chiavi di geometria osservativa verificate. Anche i due FITS elaborati di IC 1805 sono privi di tali campi. L'autore di IC 1805 conferma una modifica per astrofotografia della EOS 40D, senza pubblicare la curva di trasmissione del corpo modificato. [Acquisizione M8/M20](https://siril.org/tutorials/tuto-scripts/index.html) · [Galleria IC 1805](https://amor.cms.hu-berlin.de/~rodrigus/dso_astrophotography.html)

L'analisi riusa i profili ottici e le stelle del rapporto precedente. A ogni massa d'aria lo zero stimato sulle stelle A assorbe lo spostamento comune. Si valuta poi la variazione cromatica tra stelle e il P90 dell'errore sulle stelle di verifica, in calibrazione A e B. Il controllo X=0 riproduce i colori e le metriche precedenti e una trasmissione grigia uniforme lascia invariato il rapporto B/R.

| Campo e profilo | Spostamento comune a X=3 (mag) | P90 variazione tra stelle a X=3 (mag) | Δ P90 dei residui nel reticolo, min / max (mag) |
| --- | ---: | ---: | ---: |
| IC 1805, Canon di serie | +0,232 | 0,004 | −0,00012 / +0,00020 |
| M8/M20, Sony UV/IR + L-Pro | +0,265 | 0,039 | −0,00161 / +0,01170 |
| M8/M20, Sony IMX571 Siril + L-Pro | +0,279 | 0,027 | −0,01171 / +0,00903 |

Su M8/M20, l'estinzione modellata ha un effetto misurabile sulla forma della relazione di colore. Dopo aver adeguato lo zero, la variazione del P90 dei residui rimane entro **0,012 mag** per entrambi i profili e per le masse d'aria considerate. Questo non spiega i residui di circa 0,10–0,17 mag osservati nel test. Una qualifica assoluta richiede documentazione del sito e dei tempi, misure di estinzione o standard osservati, e la risposta delle ottiche effettive. Questo scenario non permette di stimare la massa d'aria realmente osservata.

- SHA-256 della ricevuta `b00a2152ec5481ab1b381121331c2e664b1c14be0b79c275b7a7cb23a6c8e718`.
- Archivio H: `Produzione/2026-10-13/Digital-StarGate-PixInsight/archives/BKL046-Bayer-estinzione-b00a2152ec54-verificato.zip`.
- Il pacchetto conserva la pagina ESO, il codice e la ricevuta. Le impronte identificano le curve, gli archivi FITS, i dati Gaia e il rapporto precedente.
- Zero avvii nativi e zero chiusure scientifiche.
