# BKL-046 · Ricostruzione CFA esplorativa di IC 1805

Si ricostruiscono 72 sorgenti con 2.021 ritagli estratti dalle 38 pose dopo il riferimento. Si usano solo le associazioni stellari accettate in precedenza, con geometria nominale stimata dalle regioni di addestramento. Il confronto usa la stessa griglia di un pixel nativo e lascia separate le quattro parità. La deposizione diretta da 1,00 e 0,70 px e il bilineare per parità riusano gli operatori già verificati su M8 e M20. Un controllo a segnale costante verifica la conservazione del livello nei pixel coperti.

Si costruiscono due calibrazioni provvisorie in memoria con gruppi alternati e disgiunti da otto dark abbinati e otto flat. Per i flat, l'offset di ogni parità è stimato dalle due strisce sinistre e il flat è normalizzato nel riquadro centrale. Le due metà delle luci alternano le pose. Il flusso usa la stessa apertura al netto della mediana dell'annulus, sui pixel condivisi fra i metodi. La dispersione usa la MAD scalata della differenza tra le due metà. Tutte le 72 stelle sono misurabili per parità, con copertura comune completa nell'annulus delle metà alla geometria nominale.

| Parità | P90 cambio calibrazione, tutti i metodi | P90 flusso bilineare rispetto a 1,00 px, cal. A / B | MAD delle metà, cal. A, 1,00 → 0,70 → bilineare |
| --- | ---: | ---: | ---: |
| R | 0,41–0,52% | 1,76% / 1,70% | 10,23 → 11,65 → 5,14 ADU |
| G1 | 0,32–0,37% | 2,13% / 2,19% | 12,97 → 14,97 → 6,19 ADU |
| G2 | 0,29–0,43% | 2,30% / 2,18% | 12,46 → 14,42 → 6,25 ADU |
| B | 0,30–0,46% | 2,13% / 2,01% | 12,28 → 14,15 → 6,24 ADU |

Il deposito da 0,70 cambia il flusso rispetto a 1,00 di meno dello 0,49% al P90. La MAD per pixel cresce con l'impronta ridotta e scende con il bilineare, come nel primo campo. Lo scarto di flusso del bilineare è più grande in IC 1805. Il confronto è a pari scala geometrica. Il comportamento a pari risposta spaziale e su aperture integrate resta da verificare sul secondo campo. Le due calibrazioni condividono l'approssimazione dell'offset scalare e non misurano l'errore dovuto al dark-flat mancante. La registrazione rimane fuori soglia. Si tratta di una replica esplorativa in ritagli, con zero chiusure scientifiche e zero esecuzioni PixInsight.

SHA-256 della ricevuta `4e5ecceb27ae9ac713b9ce8cf1c09316bd6f15634b08faeadcac22eb7a367844`.
