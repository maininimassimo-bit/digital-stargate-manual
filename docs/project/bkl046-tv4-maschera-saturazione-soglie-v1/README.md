# BKL-046 · Soglie della maschera di saturazione digitale TV4

La verifica riproduce il rapporto precedente con gli stessi modelli, le due calibrazioni e le dodici pose trattenute. Per la maschera confronta sette soglie di intensità prevista rispetto al limite digitale. Il caso in tabella usa l'overscan parallelo e la calibrazione dopo il riallineamento. La regione centrale delle pose da 30 s contiene 179.248 pixel al limite e 213.968 pixel ancora misurabili.

| Soglia sopra il limite digitale | Pixel misurabili marcati | Pixel saturi non marcati |
| --- | ---: | ---: |
| 0 DN | 81.147 | 0 |
| 128 DN | 52.880 | 222 |
| 256 DN | 27.236 | 5.095 |
| 512 DN | 9.084 | 45.974 |
| 1.024 DN | 4 | 122.280 |

Con una fascia di astensione di ±256 DN, il modello rinvia la decisione su 104.718 pixel misurabili e 5.095 saturi. Fra le decisioni emesse, marca ancora 27.236 pixel misurabili e non classifica alcun saturo come sicuramente misurabile. Questi sono conteggi dello stesso campione di fotogrammi, con dipendenza spaziale.

Il rapporto completo conserva tutti i modelli, i riquadri e le soglie. Nessuna soglia è stata selezionata sulle pose trattenute. Il risultato misura un compromesso di classificazione per la saturazione digitale. Il flusso oltre soglia, la condizione di full well e l'effetto di una ricomposizione effettiva restano aperti.

Eseguire `misura.py` con il protocollo, la directory congelata della verifica precedente con i suoi input e una nuova directory per i risultati.
