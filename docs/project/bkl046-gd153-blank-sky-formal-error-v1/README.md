# BKL-046 · Controllo empirico del rumore di fondo nei FLC di GD153

Ho misurato aperture di cielo su una griglia disgiunta nelle 14 pose WFC3 che compaiono nei confronti GD153. Ogni riquadro usa un'apertura di 10 pixel e il fondo mediano fra 16 e 22 pixel. La griglia evita il bersaglio, applica PAM e rispetta le maschere DQ. Il modello di confronto usa gli ERR dei pixel conservati con aspettativa di fondo costante e rumore gaussiano indipendente. I 512 campioni per riquadro stimano anche la variabilità della mediana dell'anello. [Studio ERR sulle aperture stellari](../bkl046-gd153-formal-flc-error-v1/README.md)

Delle 1.694 posizioni di griglia, 69 cadono nell'esclusione intorno a GD153, 6 hanno supporto insufficiente e 1.619 sono misurabili. Il limite fissato sul massimo residuo di un singolo pixel esclude una sola misura. I residui sono espressi in unità della deviazione standard formale dell'apertura.

| Sintesi sulle 1.618 aperture filtrate | RMS | MAD normalizzata | Valori con modulo sopra 1,96 |
| --- | ---: | ---: | ---: |
| Residui originali | 1,68 | 1,85 | 427 (26,39%) |
| Dopo sottrazione della mediana di ogni posa | 1,27 | 0,84 | 116 (7,17%) |

Nelle due pose F438W della coppia con nucleo danneggiato, le mediane dei residui del cielo sono +1,17 e −0,80 rispettivamente. L'offset fra immagini contribuisce alla dispersione aggregata. Dopo aver rimosso gli offset, RMS e MAD descrivono aspetti differenti della distribuzione. Il rapporto conserva le aperture rifiutate e le sintesi per banda e posa.

Il test caratterizza il fondo misurato lontano dalla stella. La rimozione degli offset è descrittiva. Il test non distingue struttura del fondo e covarianza strumentale, né calibra la covarianza dipendente dal segnale nel nucleo o l'errore dei campioni mancanti. I riquadri condividono pose e calibrazione e non sono bersagli indipendenti. Zero chiusure scientifiche e zero avvii PixInsight.

Per ripetere, passare a `misura.py` il protocollo, la directory delle pose FLC 11450, gli ZIP del confronto nella stessa visita, delle aperture integre e della propagazione formale ERR, la directory con NumPy 2.3.5 e Astropy 7.2.0 e un nuovo file di risultato.