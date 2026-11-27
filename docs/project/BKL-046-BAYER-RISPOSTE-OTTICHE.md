# BKL-046 · Risposte ottiche documentate e confronto Bayer a pendenza unitaria

Il tutorial originale identifica per M8/M20 la camera ZWO ASI2600MC e il filtro **Optolong L-Pro**. Il FITS di riferimento conferma la ASI2600MC Pro e la focale di 388 mm. Per IC 1805, l'autore indica Canon EOS 40Da e Skywatcher 72ED senza spianatore. L'EXIF riporta EOS 40D e non consente di ricostruire la trasmissione della modifica. [Acquisizione M8/M20](https://siril.org/tutorials/tuto-scripts/index.html) · [Acquisizione IC 1805](https://amor.cms.hu-berlin.de/~rodrigus/datasets.html)

## Confronto su stelle tenute da parte

Il modello usa gli spettri GAVO già verificati e gli stessi flussi lineari a raggio 6 pixel. Si adegua soltanto lo zero cromatico sulle stelle di stima della calibrazione A. La pendenza rimane unitaria. Si valuta sulle stesse 9 stelle di IC 1805 e 19 di M8/M20 in A e B.

Per IC 1805 si usa la curva Canon EOS 40D di serie di Jiang et al. La misura è per unità di radianza. Le forme B e R sono normalizzate separatamente e lo zero viene stimato, quindi il calcolo non determina il guadagno assoluto. La curva di serie è un riferimento provvisorio per il corpo indicato come 40Da. [Misure Jiang et al.](https://www.gujinwei.org/research/camspec/db.html)

Per M8/M20 si confrontano due approssimazioni su 410–690 nm. La prima usa i canali Sony UV/IR della libreria PixInsight installata. La seconda usa il profilo Sony IMX571 di Siril, derivato dal grafico di una camera Player One con lo stesso sensore. Entrambe sono moltiplicate per la stessa curva tabulata del L-Pro. Il calcolo per conteggi di fotoni include il fattore λ. La QE già inclusa nei profili OSC non viene moltiplicata una seconda volta. Ho ordinato le coppie lunghezza d'onda–risposta del profilo Siril: il canale rosso conteneva una coppia fuori ordine. [Profilo Siril fissato per revisione](https://gitlab.com/free-astro/siril-spcc-database/-/raw/3426f0939d53d4d3a1b4c8e620a6faf8212bda32/osc_sensors/Sony_IMX571.json) · [Filtro Optolong L-Pro](https://www.optolong.com/cms/document/detail/id/13.html)

| Campo e profilo | drop 1,0 P90 A/B (mag) | drop 0,7 P90 A/B (mag) | Bilineare per parità P90 A/B (mag) |
| --- | ---: | ---: | ---: |
| IC 1805, Canon di serie 400–720 nm | 0,071 / 0,071 | 0,069 / 0,069 | 0,074 / 0,074 |
| M8/M20, Sony UV/IR + L-Pro | 0,152 / 0,146 | 0,157 / 0,156 | 0,126 / 0,122 |
| M8/M20, IMX571 Siril + L-Pro | 0,124 / 0,118 | 0,127 / 0,126 | 0,103 / 0,111 |

Su M8/M20 includere L-Pro cambia il colore sintetico, dopo riallineamento dello zero, di **0,027–0,030 mag al P90**. I due profili con L-Pro differiscono di **0,067 mag al P90**. Estendere il solo profilo PixInsight fino a 700 nm cambia il colore di 0,005 mag al P90. Questi scarti misurano la sensibilità al modello ottico. Restano da reperire la risposta della camera modificata di IC 1805 e quella del sistema ASI2600MC effettivamente usato, inclusi finestra, filtro e ottica, prima di qualificare il colore assoluto. L'asse FILTER_COLOR/3 resta aperto.

## Riproducibilità

- SHA-256 ricevuta `829812223d0e6076ec419f77c425574ae54436fd4cb76440162845ac15699ab9`.
- Archivio H: `Produzione/2026-10-13/Digital-StarGate-PixInsight/archives/BKL046-Bayer-passband-829812223d0e.zip`.
- Il pacchetto conserva codice, risposta Siril e ricevuta. La libreria PixInsight è letta in sola lettura e fissata per SHA-256 `f74d3f6dbfe4e23a6a0dc6211a91b2e0e2de1733b3a6f4bde764fe571795d372`. Gli spettri e le misure di ingresso restano nell'archivio GAVO precedente.
- Zero avvii nativi e zero chiusure scientifiche.
