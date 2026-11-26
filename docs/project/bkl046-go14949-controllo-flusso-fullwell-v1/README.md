# BKL-046 · Controlli fotometrici non saturi GO14949

La prova rilegge l'apertura da 3 pixel dei tre nuclei con flag di full well e riproduce il rapporto originario. Per il controllo usa le stelle del chip 2 sui tasselli di verifica con guide valide, centro misurato e DQ pulito in entrambe le pose da 400 s. Usa gli stessi centri previsti per le pose lunghe e lo stesso trattamento di fondo e PAM. Su 39 candidate, 37 hanno misure valide anche nella posa B da 40 s.

| Gruppo | Prima posa lunga rispetto a B40 | Seconda posa lunga rispetto a B40 |
| --- | ---: | ---: |
| Controlli non saturi, mediana | +1,02% | +1,20% |
| Controlli non saturi, P05–P95 | −1,73%–+4,85% | −1,91%–+4,72% |
| Tre nuclei full well, minimo–massimo | +0,69%–+1,32% | +0,67%–+1,70% |

I tre nuclei sono tutti più luminosi di qualunque stella di controllo misurata. Il riferimento breve misura 1.252–2.128 elettroni al secondo per i nuclei e 35–789 per i controlli. La somiglianza delle differenze fra pose suggerisce cautela nell'attribuirle al full well. Un confronto a luminosità sovrapposta resta da acquisire.

Questo controllo non modifica la prequalifica geometrica e non dimostra il recupero del flusso saturo. Per il replay passare a `misura.py` il protocollo, la directory della fotometria originale vincolata per impronta e una nuova directory di uscita.
