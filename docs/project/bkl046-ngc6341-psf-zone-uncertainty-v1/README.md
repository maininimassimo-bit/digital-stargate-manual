# BKL-046 · Incertezza per zona del confronto PSF in NGC 6341

Ho trattenuto le 733 stelle misurate in entrambe le direzioni del confronto ACS da 5 e 90 s. I tre casi esclusi restano nel rapporto. Il ricampionamento usa, per CCD, zone intere di 512 pixel. Ogni estrazione riusa la stessa selezione di zone per entrambe le direzioni e per tutte le misure. [Confronto sulle due esposizioni](../bkl046-ngc6341-psf-zone-holdout-v1/README.md)

| CCD e posa di stima | Mediana appaiata, angolo proprio meno angolo di zona | Intervallo descrittivo 2,5–97,5 percentili |
| --- | ---: | ---: |
| 1, 5 s | +2,52 punti percentuali | +0,79–5,00 |
| 1, 90 s | +3,52 punti percentuali | +1,94–5,91 |
| 2, 5 s | +2,36 punti percentuali | +0,22–4,20 |
| 2, 90 s | +3,38 punti percentuali | +1,01–5,16 |

La differenza mediana rimane positiva anche escludendo una zona alla volta. Il confronto con il modello circolare peggiora in tre delle quattro combinazioni per l’angolo proprio in tutto l’intervallo descrittivo. L’unica combinazione con mediana positiva, CCD 1 con stima a 90 s, ha un intervallo da −3,05 a +3,67 punti percentuali.

La procedura esegue 9.999 estrazioni su 27 zone del CCD 1 e 30 del CCD 2. Gli intervalli descrivono la sensibilità alle zone di questo campo e dipendono dai centri, dalla selezione e dalle esposizioni archiviate. Restano aperte la generalizzazione ad altri campi e la verifica nativa.

Per riprodurre, usare Python 3.12 e NumPy 2.3.5. Passare a `misura.py` il protocollo, `riscontro-padre.json`, la directory delle dipendenze e un nuovo rapporto.