# BKL-046 · Distinguibilità di due centri Moffat nel rumore Poisson

Il test confronta 72 traslazioni finite rispetto a sei configurazioni di riferimento. I conteggi simulati sono Poisson indipendenti con 10.000 elettroni di flusso totale e fondo uniforme di 20 elettroni per pixel. La forma, il flusso, il fondo e l'asse ortogonale sono noti. Per ogni ipotesi vengono simulati 4.096 campioni. Il confronto usa il rapporto di verosimiglianza a priori uguali e conserva anche i limiti calcolati dall'affinità di Hellinger. [Distanza di variazione totale e relazione con Hellinger](https://people.lids.mit.edu/yp/homepage/data/itbook-2022.pdf)

| Caso con spostamento positivo di 0,01 px | Accuratezza simulata in x | Accuratezza simulata in y |
| --- | ---: | ---: |
| Moffat stretta al centro | 49,6% | 51,0% |
| Moffat stretta vicino al bordo in x | 100% | 50,8% |
| Moffat stretta vicino all'angolo | 100% | 100% |
| Controllo circolare più largo al centro | 70,2% | 70,1% |

Per la Moffat stretta al centro, il limite inferiore dell'errore ottimale è circa il 50% in entrambi gli assi. Il risultato distingue ipotesi prefissate. Rimangono da provare la stima libera della posizione, la forma incerta, il rumore di lettura e l'applicabilità alle immagini reali.

Il primo protocollo conserva un caso in cui le due quadrature differivano di 9,01 × 10⁻⁶ elettroni per pixel. Il secondo protocollo raffina soltanto la suddivisione dei lati. Le tolleranze, i casi e i semi rimangono quelli originali. Per riprodurre il risultato fornire a `simula-raffinato.py` il protocollo iniziale con il protocollo di raffinamento adiacente, il rapporto di Fisher, il sorgente congelato della quadratura, NumPy 2.3.5 e un nuovo percorso di uscita.
