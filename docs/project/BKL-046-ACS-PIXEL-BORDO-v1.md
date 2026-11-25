# BKL-046 – Sensibilità ACS al contributo dei pixel sul bordo

Il confronto usa le visite indipendenti j8jq03 e j8jq06 dello standard GRW+70D5824, con due esposizioni per visita e per filtro a 3 e 5 pixel. Le misure usano gli stessi centri WCS derivati da CALSPEC, la stessa mappa delle aree dei pixel e la stessa stima del fondo. L'apertura frazionaria pesa la porzione di pixel che interseca il cerchio e verifica la qualità su tutti i pixel intersecati.

Gli scarti indicano la variazione percentuale di ciascun rapporto tra la seconda e la prima visita.

| Raggio | Rapporto | Pixel interi | Area frazionaria |
| --- | --- | ---: | ---: |
| 3 px | F658N/F606W | +1,386% | −0,095% |
| 3 px | F658N/F660N | +1,398% | +0,513% |
| 3 px | F660N/F606W | −0,012% | −0,605% |
| 5 px | F658N/F606W | +0,648% | +0,254% |
| 5 px | F658N/F660N | +0,615% | +0,532% |
| 5 px | F660N/F606W | +0,033% | −0,276% |

Passando da 16×16 a 32×32 suddivisioni per pixel, la variazione massima del flusso per esposizione è 0,0181% a 3 pixel e 0,0045% a 5 pixel. A 10 pixel il supporto DQ esclude la seconda visita. Le visite GD71 restano escluse per centratura non convalidata.

Il cambio di segno di F658N/F606W a 3 pixel rende il risultato inadeguato come controllo di trasferimento tra visite. La stabilità numerica della suddivisione riguarda solo il calcolo dell'area e lascia aperta la qualificazione della correzione d'apertura. Restano zero controlli qualificati e zero chiusure scientifiche.

[Riscontro e impronte dei sorgenti](BKL-046-ACS-PIXEL-BORDO-v1.json) · [Riproduzione delle misure precedenti](BKL-046-RILETTURA-ACS-FONDO-CFA-v1.md)
