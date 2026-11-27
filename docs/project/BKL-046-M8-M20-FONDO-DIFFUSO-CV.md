# BKL-046 · Scelta del modello di fondo e conservazione del segnale diffuso

Su tre pose reali di M8 e M20 si estraggono nove riquadri per posa nella previsualizzazione dei due verdi CFA. Si iniettano filamenti gaussiani corti e lunghi in quattro direzioni e una componente diffusa larga, a tre ampiezze. Le ampiezze sono multipli della dispersione robusta delle differenze orizzontali, usata come scala locale di contrasto. Il controllo è digitale e la scala include la struttura dell'immagine.

Si stimano piano e quadratica dalle mediane delle celle pari. Il modello adattivo sceglie il grado con minore errore mediano di predizione sulle celle dispari. Il modello viene scelto indipendentemente prima e dopo l'iniezione. Nessun fit riceve la forma o la posizione del segnale iniettato. La differenza fra le immagini corrette viene confrontata col segnale noto nel flusso entro un'apertura centrale e nell'errore relativo L2 su tutto il riquadro. Il controllo recupera un piano noto e riproduce il contrasto nullo.

| Profilo | Iniezioni | Cambi di grado | Errore mediano di flusso sul modello scelto | Mediana errore L2 sul modello scelto |
| --- | ---: | ---: | ---: | ---: |
| Filamento corto | 324 | 73 | −58,9% | 37,9% |
| Filamento lungo | 324 | 107 | −73,7% | 44,1% |
| Diffuso largo | 81 | 28 | −90,6% | 96,3% |

Nessuna delle 729 iniezioni rientra contemporaneamente nel 5% su flusso e forma, neppure mantenendo fisso uno dei due gradi. Il modello adattivo sceglie la quadratica dopo l'iniezione in 453 casi. In 433 di questi il suo errore assoluto di flusso supera quello ottenuto col piano fisso. Il criterio predittivo minimizza l'errore delle celle di fondo e lascia il segnale diffuso esposto a sottrazione perché quelle celle possono contenerlo. I casi riusano le stesse pose e regioni. Il risultato riguarda due modelli offline su riquadri con iniezione centrale e lascia aperte la qualifica di una maschera operativa e le prove native. Zero chiusure scientifiche.

SHA-256 della ricevuta `dd866044eedbd523d5a4dda18fb0eb2527fb65936277b94f56ce7525fa263552`.
