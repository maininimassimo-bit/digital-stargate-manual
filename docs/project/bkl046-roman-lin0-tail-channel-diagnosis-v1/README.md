# BKL-046 · Canali responsabili della sensibilità della coda Roman

Il controllo esplorativo conserva il campione completo e verifica che le somme pesate dei blocchi RAW riproducano tutte le 960 varianze di riferimento accettate alla lettura 1. Calcola inoltre la frazione della somma dei quadrati centrati concentrata nelle finestre maggiori. L'analisi usa le stesse maschere della previsione e riporta tutte le 32 esclusioni singole di canale e tutte le 15 esclusioni singole di coppia per fascia.

| Fascia superiore, previsione empirica | P95 GAIN | P95 LIN0 | Differenza in punti |
| --- | ---: | ---: | ---: |
| Campione completo | 13,13% | 12,80% | +0,33 |
| Escluso il canale 15 | 11,43% | 11,91% | −0,48 |
| Escluso il canale 4 | 13,11% | 12,75% | +0,36 |
| Esclusa la coppia che inizia all'esposizione 19 | 13,10% | 12,81% | +0,29 |

Il canale 15 compare 13 volte fra i 24 casi con maggiore errore GAIN nella fascia superiore. Il confronto più estremo appartiene invece al canale 4, coppia che inizia all'esposizione 19. L'errore supera il 91% con entrambe le previsioni e le cinque finestre maggiori spiegano il 90,95% della somma dei quadrati centrati di quel caso. I cinque termini si riferiscono a finestre ricampionate che possono condividere pixel.

Il risultato separa la ricorrenza su un canale dall'evento locale estremo. L'esclusione del canale 15 è descrittiva. Il campione completo resta il riferimento. Il controllo non attribuisce l'origine fisica delle finestre estreme, non qualifica una regola di scarto e non implica un vantaggio generalizzabile. Il confronto tra sessioni, la dose calibrata e la prova nativa restano aperti.

Per ripetere usare Python 3.12 con il protocollo, le directory delle analisi di previsione e incertezza, il decodificatore LIN0 e il kernel dei canali, le due catture con i segmenti FITS, NumPy 2.3.5 e una nuova directory di uscita.
