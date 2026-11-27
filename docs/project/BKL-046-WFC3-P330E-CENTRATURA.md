# BKL-046 · Effetto della griglia di centratura nel fit WFC3/P330E

Il confronto riprende i medesimi profili sintetici a fuoco intermedio, le 24 maschere P330E e i medesimi campioni di rumore del [test precedente](BKL-046-WFC3-P330E-FUOCO-FIT.md). Per la PSF standard e per la scelta fra i piani di fuoco di indice pari, confronta un centro stimato su griglie a un quarto e a un ottavo di pixel e un centro bloccato alla posizione sintetica vera. I due livelli di segnale sono 20.000 e 200.000 elettroni.

| Banda | Fuoco stimato, P90 con maschera, quarto di pixel | Ottavo di pixel | Centro vero |
| --- | ---: | ---: | ---: |
| F438W | 6,15–6,75% | 3,03–3,42% | 3,03–3,42% |
| F606W | 7,55–8,15% | 4,73–5,07% | 4,73–5,07% |
| F814W | 7,33–7,85% | 5,03–5,29% | 5,03–5,29% |

I 6.656 esiti con griglia a quarti coincidono con la prova precedente, incluso l'errore di flusso. La prova conserva 19.968 esiti totali. La griglia più fine comprende deliberatamente le fasi sintetiche di questo confronto. Il risultato misura l'effetto della discretizzazione della centratura in questi casi. Anche fornendo il centro esatto al fit con fuoco discreto, il P90 resta sopra l'1% in ogni banda e livello di segnale. Il residuo include errore di modello e rumore. Il test non ne stima separatamente le quote e non misura il flusso reale di P330E. Gli assi `FILTER_COLOR/2` e `FILTER_COLOR/3` restano aperti.

| Artefatto | SHA-256 |
| --- | --- |
| Protocollo | `828b289da35648aa943b8b59df0360b65afff1888f20acbb4953d0e67c8b8feb` |
| Programma | `32e7daae039b8a0adb6b8c1cb417ba5515f749a4636422f1aa76600beb398fc9` |
| Verifica appaiata | `64f33b05360c2f3534371c00d40c51ae3b4822bd2d5822baa4c5b4e0af374edc` |
| Ricevuta per caso, riprodotta da archivio H: | `9e4fc698955b2557cd39289bd0a8df435f8a59ee0efcd4ad546ebcffe7293efe` |
