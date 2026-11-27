# BKL-046 · Integrazione dei pixel Moffat mediante il contorno

Il protocollo storico conserva 36 profili Moffat, otto fallimenti del primo raffinamento Simpson e un successivo controllo indipendente su 108 pixel selezionati. Questa prova rilegge gli array congelati e confronta tutti i 22.500 pixel senza modificare i casi né le tolleranze.

Il metodo trasforma ciascun pixel in un parallelogramma nelle coordinate normalizzate della PSF. Il teorema della divergenza sostituisce l'integrale bidimensionale della densità con il flusso di un campo vettoriale radiale lungo il contorno. Ogni lato è integrato separatamente. Per sei profili circolari con beta 1,5 è disponibile anche il confronto con l'angolo solido esatto del rettangolo.

| Confronto | Scarto massimo per pixel | Scarto massimo sulla somma del campo |
| --- | ---: | ---: |
| Contorno ordine 64 e 128 | 2,91 × 10⁻¹¹ elettroni | 5,46 × 10⁻¹² elettroni |
| Contorno ordine 128 e Gauss 2D archiviato | 9,28 × 10⁻¹¹ elettroni | 1,18 × 10⁻¹⁰ elettroni |

Nei sei controlli circolari, lo scarto massimo per pixel rispetto alla formula dell'angolo solido è 6,37 × 10⁻¹² elettroni. La prova verifica l'accordo numerico nel dominio congelato. Rimangono aperti il limite d'errore certificato, la rappresentatività delle PSF strumentali e la calibrazione scientifica.

Per riprodurre il confronto fornire a `integra-bordi.py` l'archivio storico dell'integrazione Moffat, la ricevuta del raffinamento Simpson, la directory dei pacchetti con NumPy 2.3.5 e un nuovo percorso per il rapporto.
