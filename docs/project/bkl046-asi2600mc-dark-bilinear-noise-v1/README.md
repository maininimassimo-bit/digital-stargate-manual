# BKL-046 · Propagazione del rumore dei dark con un ricampionamento bilineare

Il test applica cinque fasi bilineari fisse sulla griglia di ciascuna parità Bayer. Usa i dark da 180 s e i Bias da 3 s della ASI2600MC, con sette coppie disgiunte per gruppo, nove riquadri e quattro parità. Le misure confrontano somme su blocchi 2 × 2, con supporto interno comune. La previsione usa la varianza misurata a monte e assume ingresso omoscedastico indipendente. La propagazione completa include la condivisione dei pixel d'ingresso prodotta dal kernel.

| Gruppo, spostamento di mezzo pixel di parità su entrambi gli assi | Varianza misurata / stima diagonale empirica, mediana | Errore mediano, propagazione completa | Errore mediano, propagazione diagonale | Entro il 10% con propagazione completa |
| --- | ---: | ---: | ---: | ---: |
| Dark 180 s | 2,28 | 5% | 56% | 207/252 |
| Bias 3 s | 2,27 | 4% | 56% | 219/252 |

Per la stessa fase, il rapporto teorico nel modello indipendente è 2,25. La previsione diagonale non rientra nel 10% in alcuno dei 252 confronti in ciascun gruppo. A fase nulla le due previsioni coincidono. Le 252 misure riusano le stesse esposizioni nei diversi riquadri e parità. I campioni di uscita possono avere supporti condivisi. I risultati non costituiscono intervalli di confidenza fra acquisizioni indipendenti.

Il riscontro riguarda `NOISE_FLUX/3`. Il kernel è applicato offline sui FITS e resta da verificare il comportamento degli operatori nativi e dei dati illuminati ricampionati. Zero avvii PixInsight e zero chiusure scientifiche. [Covarianza prima del ricampionamento](../bkl046-asi2600mc-calibrator-covariance-v1/README.md)

Replica con Python 3.12, NumPy 2.3.5 e Astropy 7.2.0. Gli argomenti sono il protocollo, il kit precedente estratto, la directory con i due ZIP originali di calibrazione, le dipendenze e una directory di uscita vuota. I risultati di dettaglio sono nel kit H/K.
