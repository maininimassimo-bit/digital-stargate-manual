# BKL-046 · Ingressi Gaia XP per tre standard CALSPEC

La query ARI conferma la disponibilità delle rappresentazioni continue e campionate per GD71, GD153 e GRW+70 5824. Il confronto riporta le posizioni e i moti propri Gaia all'epoca J2000 e le confronta con la tabella CALSPEC. Tutti e tre gli accoppiamenti sono entro 0,01 secondi d'arco. Il verificatore controlla anche la distinzione di GD71 dagli altri candidati con moto proprio nella stessa ricerca. [ARI Gaia](https://gaia.ari.uni-heidelberg.de/) · [Tabella CALSPEC](https://www.stsci.edu/hst/instrumentation/reference-data-for-calibration-and-tools/astronomical-catalogs/calspec)

I tre spettri campionati, ciascuno di 343 punti, provengono dai file ufficiali Gaia DR3 sul CDN ESA. Ogni riga attesa è unica e la posizione coincide con la risposta ARI. I file originali e le righe estratte restano nella copia di lavoro e di archivio. Il pacchetto pubblico contiene query, codice e riscontro. [Prodotto XP campionato](https://gaia.aip.de/metadata/gaiadr3/xp_sampled_mean_spectrum/) · [Distribuzione ESA](https://cdn.gea.esac.esa.int/Gaia/gdr3/Spectroscopy/xp_sampled_mean_spectrum/)

I campioni forniscono flussi ed errori marginali. La covarianza richiede la rappresentazione continua e il modello di propagazione. Confronti fotometrici, calibrazione indipendente e chiusure scientifiche restano da verificare.

Per ripetere passare al verificatore la directory con query, risposta ARI, ricevuta CDN e tre gzip originali, poi due percorsi nuovi per riscontro e spettri estratti. Le impronte degli ingressi sono fissate. I dati provengono dalla missione ESA Gaia e sono elaborati dal DPAC.
