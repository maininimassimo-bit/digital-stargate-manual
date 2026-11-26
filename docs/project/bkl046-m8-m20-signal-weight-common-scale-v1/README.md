# Baseline CFA a scala comune per la registrazione pesata di M8–M20

La prova BKL-046 ricostruisce 53 regioni stellari nelle 14 pose Bayer di M8–M20 cambiando solo la geometria. Confronta l’affine a pesi unitari e quello pesato per segnale sullo stesso reticolo a passo nativo. Restano fissi le due calibrazioni, le maschere, le aperture, le due metà di pose alternate e la forma quadrata del deposito. I pesi per segnale agiscono sulla stima della geometria. I contributi dei depositi usano la stessa regola in entrambe le ricostruzioni.

Le 28 matrici convertite riproducono le predizioni del fit stellare. Il rapporto riporta le matrici dirette dal riferimento al rivelatore. Nella struttura ereditata, `binned` contiene l’affine a pesi unitari e `mosaic` quello pesato per segnale. Entrambi usano qui gli stessi centroidi della preview. Per ricostruire si applicano le matrici inverse.

| Canale | P90 variazione assoluta del flusso, deposito da 1,00 px, A / B | Deposito da 0,70 px, A / B |
| --- | ---: | ---: |
| R | 0,384% / 0,360% | 0,494% / 0,389% |
| G1 | 0,169% / 0,201% | 0,215% / 0,180% |
| G2 | 0,148% / 0,188% | 0,188% / 0,208% |
| B | 0,166% / 0,211% | 0,257% / 0,268% |
| G combinato | 0,117% / 0,161% | 0,138% / 0,147% |

Il supporto comune misurato è completo nelle aperture e negli anelli. Il P90 delle differenze di flusso resta sotto l’1% in tutte le combinazioni. La variazione mediana con segno del MAD del fondo fra le due metà va da −0,96% a +1,30%. Il risultato è una baseline offline per il confronto con una futura ricostruzione nativa. La convenzione XDRZ, il significato dei pesi RGB e l’accuratezza fotometrica indipendente restano da qualificare.

Per replicare eseguire `misura.py <protocollo.json> <studio-pesatura> <baseline-globale> <radice-input> <pacchetti-Python> <nuovo-riscontro.json>`.
