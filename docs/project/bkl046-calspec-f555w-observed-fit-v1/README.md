# BKL-046 — Fit a una e due componenti su standard CALSPEC F555W osservati

Il motore e le soglie di ricerca del precedente fit di Orione sono verificati per SHA-256. Il campione è il dossier archivistico dei centri CALSPEC, con 38 FLT pre-SM4 distribuiti in 19 associazioni e quattro stelle. Il fit interpola la libreria ePSF spaziale nel centro del chip salvato dal controllo dei subarray. Applica due partizioni alternate di pixel, con scelta del modello sul sottoinsieme di fit e punteggio sui pixel tenuti fuori.

Fotogrammi con entrambi i fit disponibili: 38/38. Fotogrammi esclusi o con un fit indisponibile: 0.

Per il criterio di concordanza si applicano simultaneamente uno scarto massimo di 20 mas nominali fra separazioni, rapporto minimo/massimo dei rapporti di flusso almeno 0,70 e differenza massima di asse sul rivelatore di 25 gradi modulo 180. La verifica nell'associazione richiede tutti e quattro i risultati delle due partizioni dei due FLT sullo stesso chip.

| Standard | Fotogrammi con due guadagni positivi | Fotogrammi anche concordi | Associazioni con quattro guadagni positivi | Associazioni anche concordi |
|---|---:|---:|---:|---:|
| G191B2B | 3/4 | 0/4 | 1/2 | 0/2 |
| GD153 | 3/6 | 1/6 | 1/3 | 0/3 |
| GD71 | 2/8 | 0/8 | 0/4 | 0/4 |
| GRW+70D5824 | 0/20 | 0/20 | 0/10 | 0/10 |

L'orientamento è misurato sul rivelatore e la separazione usa la scala nominale di 50 mas/pixel. I due FLT di un'associazione condividono sorgente e puntamento. Le acquisizioni ripetute della stessa sorgente non aumentano il numero di unità stellari indipendenti. Il campione fornisce una prova su dati osservati con sorgenti di calibrazione sparse, senza trasferire il risultato al fondo e all'affollamento di Orione. Manca una caratterizzazione indipendente di molteplicità e sensibilità delle quattro stelle. Nessuna etichetta negativa qualificata, nessuna esecuzione nativa, nessuna chiusura scientifica.

La replica usa il dossier CALSPEC H: con SHA-256 1ca87f5e78d19730c0263cf5bd744d540e57f8f6f7f581d0db94618b90e50eab, il motore del dossier positivo di Orione e la libreria vincolata nel protocollo. [Centri dei fotogrammi](https://github.com/maininimassimo-bit/digital-stargate-manual/commit/5be45b7d03a04eb99c65ebafb9b0f1e27dbb05c7) · [Fit di Orione](https://github.com/maininimassimo-bit/digital-stargate-manual/commit/100daf1b1e1d0d4397870483c73f3a5da6b2ba81)
