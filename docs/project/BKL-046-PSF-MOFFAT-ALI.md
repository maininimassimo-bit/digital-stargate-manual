# BKL‑046 · Sensibilità dell’orientazione alla forma delle ali della PSF

La prova mantiene la stessa larghezza a metà altezza, circa 0,608 pixel sull’asse maggiore, e lo stesso rapporto assiale del generatore. Varia il parametro β del profilo Moffat che produce i pixel, lasciando β = 3,5 nel fit. Le quattro fasi subpixel sono registrate esattamente. Le prove con rumore riusano le realizzazioni precedenti a SNR nominale complessivo 100. Le 108 prove con β abbinato riproducono gli esiti precedenti riga per riga. [Prova empirica di riferimento](BKL-046-PSF-DITHER-EMPIRICO.md)

| β del generatore | Angoli entro 5° con rapporto 0,60, con rumore | Angoli entro 5° con rapporto 0,85, con rumore | Angoli spuri nei circolari, con rumore |
| --- | ---: | ---: | ---: |
| 3,5, riferimento | 41/48 | 17/48 | 0/12 |
| 2,5 | 38/48 | 4/48 | 0/12 |
| 5 | 34/48 | 18/48 | 5/12 |

Senza rumore, per rapporto 0,60 gli angoli rientrano in 5° in 24/24 geometrie per entrambi i β diversi da quello del fit. Per rapporto 0,85, rientrano in 3/24 con β 2,5 e in 16/24 con β 5. Nel primo gruppo, 16 esiti sono indeterminati e cinque adattamenti non qualificati. Nessun controllo circolare senza rumore riceve un angolo.

Con rumore e β = 5, tutti e dodici gli adattamenti circolari risultano qualificati numericamente, ma cinque restituiscono un angolo. La coincidenza della larghezza a metà altezza lascia quindi una sensibilità rilevante alla forma delle ali nel regime simulato. I campioni circolari restano piccoli. Il test varia le ali all’interno della famiglia Moffat e lascia aperti i profili strumentali e la misura nativa. L’asse `PSF_PIXEL/2` resta aperto.

SHA‑256 della ricevuta `8d798d4ee11f39941c4d43f2450abf30fe95f31dc46c316b9c8efbbbd4c11eb2`.
