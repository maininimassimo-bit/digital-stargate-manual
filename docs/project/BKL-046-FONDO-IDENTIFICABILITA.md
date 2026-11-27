# BKL-046 · Separabilità tra fondo additivo e segnale diffuso

Si usa la geometria affine misurata nelle 15 pose M8/M20 e nelle 39 pose IC 1805 per simulare il campionamento dello stesso cielo su una griglia comune. Il test proietta sei modi polinomiali del cielo fuori dallo spazio dei fondi ammessi. La SVD è calcolata dopo ortonormalizzazione dei modi del cielo. Il valore singolare residuo misura la frazione di norma disponibile lungo una direzione, nell'ipotesi di pesi uniformi. I controlli con geometria identità e sola traslazione verificano le degenerazioni attese.

| Fondo ammesso | M8/M20, modi sopra l'1% su 6 | IC 1805, modi sopra l'1% su 6 |
| --- | ---: | ---: |
| Offset libero per posa | 5 | 5 |
| Quadratica comune sul rivelatore e offset libero per posa | 0 | 3 |
| Quadratica libera per posa | 0 | 0 |

Con una quadratica libera per posa, tutti e sei i modi del cielo sono nel sottospazio di fondo. Anche una geometria affine diversa per posa lascia tale ambiguità esatta. Con una quadratica comune e offset liberi, il maggior valore singolare residuo è 0,00322 in M8/M20 e 0,364 in IC 1805. In IC 1805, tre direzioni superano il livello diagnostico dell'1%, mentre le due pendenze del cielo mantengono meno dello 0,05% della propria norma. Per il modello comune, il profilo gaussiano largo mantiene il 9,66% o 14,89% della norma, il filamento lungo l'85,16% o 85,84%.

La stessa immagine può ammettere diverse separazioni fra cielo e fondo quando i relativi spazi coincidono. In quel caso il confronto predittivo tra modelli o le sole maschere della scena non possono identificare il flusso assorbito. Il test sostiene una regola di astensione per i modi degeneri. Il livello dell'1% è un indicatore strutturale, senza modello di rumore, maschere reali o intervalli di confidenza. I valori di norma non sono percentuali di flusso fotometrico recuperato. Restano da misurare fondi indipendenti e incertezze e da verificare il processo nativo. Zero chiusure scientifiche.

SHA-256 della ricevuta `3e802109cb197c89470ee7f7ed2577a17a9a543abe559eec3c0906ca6d085804`.
