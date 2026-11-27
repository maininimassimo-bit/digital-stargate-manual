# BKL‑046 · Trasferimento delle maschere dei quadrupoli a GO14949

Il secondo campo usa due esposizioni ACS/WFC F606W da 40 s di GO14949, recuperate da MAST e verificate rispetto alle impronte già registrate. Il protocollo riusa tutti i 677 abbinamenti stellari con centri misurati nelle stesse esposizioni. Le due pose sono proiettate nel piano tangente con il WCS alternativo A in ICRS. [Prova di origine su NGC 5986](BKL-046-NGC5986-DQ-MASCHERA-COMUNE.md)

| Chip | Coppie | Momenti validi con riquadro interamente pulito | Momenti validi con maschera comune | Angoli proiettati disponibili con maschera | Differenza entro 5° |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 294 | 5 | 236 | 152 | 73 |
| 2 | 383 | 6 | 295 | 130 | 45 |
| Totale | 677 | 11 | 531 | 282 | 118 |

Il P90 delle differenze proiettate fra le 282 coppie definite è 17,82°. Le sei coppie con angoli disponibili e riquadro interamente pulito forniscono la base del controllo di sensibilità. Su queste sono applicate le 89 maschere distinte già congelate in NGC 5986. Sono disponibili 530 angoli accoppiati su 534 applicazioni. La deriva della differenza angolare al P90 è 3,786°, oltre il limite congelato di 2°. Il guadagno di copertura si ripete nel secondo campo, mentre il controllo sulla deriva fallisce di nuovo.

Le applicazioni ripetute riusano sei stelle. Il confronto tra campi comprende profondità e origine dei centri diverse. La misura documenta sensibilità della forma osservata, senza verità sull’orientazione intrinseca né esecuzione nativa. L’asse `PSF_PIXEL/2` resta aperto.

SHA‑256 della ricevuta `352a42e6e6cefd79436957d26b8b6aa474702d92f3c2de069a22b45d360c3b42`.
