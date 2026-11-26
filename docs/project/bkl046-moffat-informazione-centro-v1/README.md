# BKL-046 · Informazione sul centro e sul flusso di una PSF Moffat sottocampionata

Calcolo della matrice di Fisher per 72 profili Moffat integrati su 25 × 25 pixel e per due livelli di fondo. Il modello assume conteggi Poisson indipendenti, forma della PSF nota, flusso totale pari a 10.000 elettroni e fondo uniforme. Centro, flusso e livello di fondo sono stimati congiuntamente nel calcolo del limite. [Limiti di Cramér–Rao per astrometria e fotometria](https://arxiv.org/abs/1407.3753)

Le derivate della posizione sono integrali della densità sui bordi opposti. Il confronto con differenze finite perde precisione su tre derivate molto deboli. L'integrale bidimensionale indipendente delle derivate concorda sui quattro pixel più sensibili di ciascuna di queste derivate. Il rapporto conserva entrambi gli esiti.

Nel caso con alfa 0,06 pixel, beta 4,5, rapporto assiale 0,35 e fondo 20 elettroni per pixel, al centro del pixel entrambi gli assi della posizione sono scarsamente informati. Vicino a un solo bordo il limite inferiore della deviazione standard sull'asse meglio informato è 0,00030 pixel. Quello sull'altro asse supera le dimensioni dell'immagine. Vicino all'angolo entrambi gli assi sono informati, con limiti di 0,00010 e 0,00030 pixel. Nei casi citati il limite relativo sul flusso rimane vicino all'1%.

I valori sono limiti locali sotto il modello dichiarato. Un limite superiore alla larghezza del campo indica scarsità d'informazione locale. La precisione di uno stimatore reale, gli effetti di rumore di lettura e gli errori sui parametri di forma restano da misurare. Per riprodurre il calcolo, fornire a `misura.py` il protocollo, il rapporto della quadratura suddivisa, il sorgente dell'integrazione sul contorno, NumPy 2.3.5 e un nuovo percorso di uscita.
