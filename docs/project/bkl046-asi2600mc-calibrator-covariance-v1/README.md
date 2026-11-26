# BKL-046 · Covarianza nei calibratori ASI2600MC

Il test usa sette coppie cronologiche disgiunte per gruppo, su nove riquadri da 128 × 128 pixel. La quindicesima posa di ogni gruppo resta esclusa. Per ciascuna parità Bayer calcola la differenza delle due pose divisa per la radice di due in blocchi disgiunti 2 × 2 sulla griglia della parità. Tutti i 756 casi coppia-riquadro-parità superano il requisito minimo di supporto. La varianza empirica della somma del blocco coincide con la somma degli elementi della matrice di covarianza.

| Gruppo | Intervallo delle mediane del rapporto fra varianza della somma e stima diagonale | Massimo P95 fra le quattro parità |
| --- | ---: | ---: |
| Bias da 3 s | 1,00–1,01 | 1,08 |
| Dark da 180 s | 1,01–1,02 | 1,08 |
| Flat da 3 s | 1,02–1,04 | 1,34 |

I percentili si riferiscono ai 63 casi riquadro-coppia per parità. I riquadri della stessa coppia condividono le pose. Nei 36 confronti per riquadro e parità, l'eccesso di varianza del flat rispetto al Bias di pari durata, diviso per l'eccesso di segnale, va da 3,88 a 4,12 ADU. Il test comprende una sola durata illuminata. Variazioni di illuminazione e residui temporali entrano nella misura. Il rapporto condizionale non qualifica il guadagno elettronico o la linearità al variare della dose.

Il riscontro riguarda gli assi `NOISE_FLUX/1`, `NOISE_FLUX/2` e `NOISE_FLUX/3`. Le misure sono sui dati Bayer prima del ricampionamento. Restano da verificare la covarianza dopo i processi nativi e un riferimento fisico con più dosi misurate. Zero avvii PixInsight e zero chiusure scientifiche.

Per replicare, usare Python 3.12, NumPy 2.3.5 e Astropy 7.2.0. Passare il protocollo, la directory dei tre ZIP di calibrazione, la ricevuta originale, la directory delle dipendenze e una directory di uscita vuota. I tre ZIP e la ricevuta sono fissati per impronta. Il dettaglio di ogni misura è conservato nel kit H/K.
