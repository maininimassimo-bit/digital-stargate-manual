# BKL-046 · Fondo differenziale con fasce ai bordi escluse

Sulle coppie di pose IC 1805 e M8/M20 già archiviate, con scala unitaria, si tiene fuori dal fit una fascia contigua larga due celle. Il piano e l'offset sono stimati sulle altre celle. Si misurano mediana e P90 del residuo assoluto solo nella fascia esclusa. Per ogni orientamento si confrontano fasce interne ed esterne di pari larghezza con lo stesso numero di celle di stima e verifica. Il controllo riproduce esattamente tutte le metriche precedenti a scacchiera.

| Campo | Coppie | Passano le due partizioni a scacchiera | Passano tutte le fasce interne | Passano tutte le fasce ai bordi | Passano a scacchiera e falliscono ad almeno un bordo |
| --- | ---: | ---: | ---: | ---: | ---: |
| IC 1805 | 72 | 45 | 29 | 16 | 30 |
| M8/M20 | 27 | 6 | 2 | 1 | 6 |

Il criterio per singola fascia richiede almeno il 10% di riduzione della mediana assoluta e nessun aumento del P90 rispetto al solo offset. I bordi sono quelli della griglia comune analizzata. Un esito favorevole su punti spazialmente alternati lascia aperta l'estrapolazione dove mancano intere fasce di stima. Le 99 coppie riusano pose. La misura riguarda il residuo relativo con questi dati e lascia aperte la calibrazione fotometrica, la verità di fondo, il segnale diffuso preservato e le prove native.

Per replicare si riusano gli script, i dati originali e le ricevute dei test di riferimento. Il programma riceve la directory del protocollo, il campo (IC1805 o M8M20), la directory del test di riferimento, la directory delle pose, il file della registrazione stellare, la directory delle dipendenze, la directory rawpy estratta, la directory del runtime Visual C++ e il file di uscita. Le ultime due dipendenze sono usate per IC 1805. [IC 1805](../bkl046-ic1805-reference-transfer-v1/README.md) · [M8/M20](../bkl046-m8-m20-reference-transfer-v1/README.md)