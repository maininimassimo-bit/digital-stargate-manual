# BKL-046 · Sensibilità delle aperture frazionarie su M8–M20

Il confronto riusa le 2.967 misure Bayer appaiate, i due centri previsti e le due calibrazioni archiviate. Il programma riproduce i flussi originali a supporto discreto. Incrocia poi i pixel delle due aperture con le stime di fondo dei due anelli. Il test usa la stessa maschera di saturazione e pixel caldi. L'apertura frazionaria assegna a ogni fotosito un peso pari alla porzione della sua area coperta dal cerchio, stimata su una griglia 32 × 32. L'anello di fondo mantiene la mediana dei pixel selezionati. Tutte le misure restano nel confronto.

| Parità | P90 variazione del flusso, solo supporto discreto A/B | Solo fondo A/B | Supporto e fondo discreti A/B | Apertura frazionaria e fondo discreto A/B |
| --- | ---: | ---: | ---: | ---: |
| R | 1,139% / 1,118% | 0,611% / 0,563% | 1,520% / 1,380% | 1,372% / 1,224% |
| G1 | 0,844% / 0,831% | 0,516% / 0,521% | 1,131% / 1,128% | 0,935% / 0,948% |
| G2 | 0,822% / 0,800% | 0,444% / 0,445% | 1,065% / 1,067% | 1,050% / 1,013% |
| B | 0,955% / 0,962% | 0,572% / 0,477% | 1,251% / 1,308% | 0,983% / 1,074% |

Le variazioni riportate sono simmetriche e assolute. Il P90 dello spostamento del solo supporto supera quello del solo fondo in tutti gli otto confronti. I quantili dei due effetti si riferiscono a distribuzioni appaiate e la loro somma non rappresenta il quantile dell'effetto congiunto. I pesi frazionari riducono il P90 in tutti gli otto confronti. Tre scendono sotto l'1%. Passando da una griglia 16 × 16 a 32 × 32, il P90 della differenza nella variazione stimata resta entro 0,0174 punti percentuali. Questo verifica la sensibilità alla discretizzazione della griglia. L'accuratezza assoluta del flusso e la comparazione dopo ricostruzione a scala comune restano aperte.

Ricevute identiche in due esecuzioni, SHA-256 `ea9e2f75ee742e7847b9fa0cb7cb9e2f94f50dd02c0858ba94cb64863ab7d66f`. Zero esecuzioni native.
