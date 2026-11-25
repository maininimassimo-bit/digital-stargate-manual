# BKL-046 · Accordo tra le due parità verdi nella registrazione di IC 1805

Sulle associazioni stellari di verifica congelate di IC 1805, il programma stima separatamente i centroidi dai due reticoli verdi del mosaico Bayer. Per ogni associazione calcola la differenza tra lo spostamento misurato con G1 e quello misurato con G2, sempre rispetto alla stessa posa di riferimento. In questa differenza si cancella un eventuale spostamento geometrico comune. Il controllo con due sorgenti sintetiche recupera sia l'accordo sia uno scarto imposto di 0,40 pixel entro 0,03 pixel.

Su 2.070 associazioni precedenti, 2.003 consentono entrambe le misure. Sono distribuite su 38 pose e 77 stelle. Il P90 della differenza fra gli spostamenti è 0,842 pixel nativi.

| Insieme | Associazioni | P90 del residuo affine congiunto (pixel nativi) |
| --- | ---: | ---: |
| Tutte le associazioni con misura congiunta | 2.070 | 0,462645 |
| Associazioni con entrambe le misure separate | 2.003 | 0,426303 |
| Disaccordo tra G1 e G2 al massimo 0,30 pixel | 1.075 | 0,299885 |
| Disaccordo tra G1 e G2 sopra 0,30 pixel | 928 | 0,546830 |

L'accordo tra parità è un indicatore diagnostico di qualità su questo campo. Il gruppo a basso disaccordo comprende il 52% delle associazioni originarie e il suo P90 sfiora la soglia. Selezione e valutazione condividono i pixel delle stesse stelle. Restano possibili errori comuni ai due centroidi e dipendenze dovute alla posa di riferimento. Il risultato motiva un controllo su pose o fonti astrometriche indipendenti, con copertura dichiarata. L'asse CFA resta aperto e PixInsight non è stato avviato.

I due rapporti ottenuti rileggendo le 39 pose hanno SHA-256 `5aa721557e500f9fcb3ee03cfcb4f8a12c84a90797e9cdd425169cd8481f2588`. Il protocollo fissa le impronte dei dati e le versioni del decodificatore.
