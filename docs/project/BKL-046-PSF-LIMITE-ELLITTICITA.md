# BKL‑046 · Ottimi locali al limite di ellitticità

Il controllo riproduce, dallo stato salvato del generatore, le 286 prove con rumore in cui l’adattamento ellittico non aveva soddisfatto la stazionarietà e si era fermato vicino al limite di ellitticità. Ricalcola il centro e l’angolo sul limite esatto. Verifica la stazionarietà nelle direzioni tangenti, la curvatura locale e il segno del gradiente nella direzione radiale. [Protocollo con rumore](BKL-046-PSF-RUMORE-ORIENTAZIONE.md)

| Rapporto segnale-rumore | Casi riesaminati | Minimi locali vincolati verificati | Stazionarietà tangente ancora insufficiente |
| --- | ---: | ---: | ---: |
| 25 | 228 | 213 | 15 |
| 100 | 58 | 57 | 1 |

Tutti i 286 adattamenti al bordo riducono il residuo rispetto all’arresto originario. Solo 270 soddisfano tutti i controlli numerici locali. Di questi, 135 hanno un generatore circolare. Il rapporto assiale al limite è circa 0,493, inferiore a tutti i rapporti assiali veri della prova (0,60, 0,85 e 1). La soluzione numerica al limite segnala un problema di stima della forma anche quando l’ottimo vincolato è verificato.

Le decisioni scientifiche della prova con rumore restano quelle della ricevuta originaria. I 261 arresti lontani dal limite di forma e i 16 casi al limite ancora privi di stazionarietà richiedono verifiche distinte. L’asse `PSF_PIXEL/2` resta aperto.

SHA‑256 della ricevuta `5df254fcd00dca0d4d1788627d4b6f2204d9e437deebe27e9ca1c74dff2e41d7`.
