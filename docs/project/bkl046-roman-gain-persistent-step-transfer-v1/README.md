# BKL-046 · Verifica del rilevatore di salti Roman in una seconda acquisizione

La prova usa la funzione di classificazione congelata in LIN0 senza cambiare soglie. GAIN comprende 20 esposizioni distinte. La stima per ogni esposizione usa le altre 19, contro le altre 29 in LIN0. Le fasce del sensore, gli indici delle letture e le coordinate nei canali sono gli stessi. Si escludono i pixel che raggiungono un limite digitale in una delle letture campionate della rispettiva serie.

| GAIN | Osservazioni pixel × esposizione | Eccessi alla lettura 1 | Eccessi persistenti |
| --- | ---: | ---: | ---: |
| Fascia inferiore | 2.621.280 | 110 | 0 |
| Fascia superiore | 2.621.160 | 114 | 0 |

I due pixel segnalati una volta in LIN0 sul canale 4 erano eleggibili in GAIN. Nessuna delle 20 esposizioni li ha segnalati alla lettura 1. I rispettivi eccessi GAIN alla prima lettura sono da −16 a +30 e da −16 a +24 ADU. Il pixel (30, 8) del canale 15 raggiunge il massimo digitale in tutte le 20 esposizioni già alla lettura 0 e in tutte le letture campionate successive. Il suo andamento resta indeterminato in GAIN.

GAIN e LIN0 hanno livelli di segnale e temporizzazioni diversi. L'assenza di segnalazioni persistenti in GAIN riguarda la parte eleggibile della serie. Il rapporto non stima un tasso di falsi positivi, non identifica la causa fisica e non autorizza una maschera o lo scarto di dati. Il campione delle prove precedenti resta quello registrato.

Per riprodurre usare Python 3.12 con il protocollo, il fascicolo del rilevatore LIN0, la directory della cattura LIN0 con il protocollo delle fasce, il fascicolo della cattura GAIN, il decodificatore LIN0, NumPy 2.3.5 e un nuovo percorso di uscita.
