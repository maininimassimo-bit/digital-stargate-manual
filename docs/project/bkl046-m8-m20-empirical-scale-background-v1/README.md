# BKL-046 · Fondo M8/M20 con scale stimate dalle stelle

Sulle 27 coppie già archiviate si applicano al contrasto della posa bersaglio le 72 stime di scala ricavate dalle stelle della stessa coppia. Si usano otto stime sul campione intero e 64 stime ottenute escludendo a turno un riquadro stellare. Si mantengono invariati il riferimento, il supporto comune, la registrazione, i due modelli e il criterio sulle partizioni spaziali. Il controllo a scala 1 riproduce esattamente i 54 risultati per partizione precedenti. [Stime di scala](../bkl046-m8-m20-stellar-scale-v1/README.md)

| Esito sulle 72 stime applicate | Coppie che passano a scala 1 | Coppie che falliscono a scala 1 | Totale |
| --- | ---: | ---: | ---: |
| Il piano supera sempre il criterio | 4 | 2 | 6 |
| Il piano lo fallisce sempre | 0 | 6 | 6 |
| Esito diverso fra le stime | 2 | 13 | 15 |

Il criterio richiede in entrambe le partizioni una riduzione del 10% della mediana assoluta rispetto al solo offset e nessun aumento del P90. Le 1.944 applicazioni esplorano un insieme finito di stime appaiate. I 15 esiti misti richiedono di sospendere la scelta del piano finché la scala non è meglio determinata. Nei sei casi sempre favorevoli il criterio è stabile sulle stime provate. Le coppie condividono stelle e pose. L'esito favorevole riguarda il residuo relativo e lascia aperta la verifica del fondo assoluto, del segnale diffuso preservato e di una calibrazione spaziale.

Il kit conserva il rapporto completo. Per replicare, il generatore riceve la directory del protocollo, la directory del test di riferimento M8/M20, la directory dati, la ricevuta stellare di registrazione, le dipendenze, la ricevuta delle scale stellari e il percorso del rapporto completo. L'archivio del test di riferimento con dati e registrazione ha SHA-256 f45e5d8080292c7fdfdd486671997f6d8e458ff371adb122a7ad69da3ab7c207. L'archivio delle scale stellari ha SHA-256 d6a8aabaf49794ec90800f6bbae373f1540331d8c0b89c60dedb965e4d17e5ac. [Confronto originario](../bkl046-m8-m20-reference-transfer-v1/README.md)