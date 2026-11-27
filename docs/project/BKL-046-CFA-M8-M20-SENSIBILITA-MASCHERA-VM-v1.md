# BKL-046 · Effetto della maschera CFA sui flussi M8–M20

Il confronto ha ricostruito la baseline affine dai 1.484 FITS calibrati di 53 stelle in 14 pose. La lettura ha verificato SHA-256, checksum FITS, fase RGGB, maschere e matrici. La ricostruzione con esclusione ha riprodotto i flussi archiviati entro 7,89 × 10⁻⁸ ADU di differenza assoluta. I tre bracci usano le stesse aperture e lo stesso supporto della baseline: esclusione, inclusione dei valori scartati e azzeramento dei valori con peso conservato. Sono stati identificati 985 campioni scartati in 506 ritagli.

| Canale | Peggior errore assoluto senza maschera | Peggior errore assoluto con valori azzerati e peso conservato |
| --- | ---: | ---: |
| R | 12,851% | 21,088% |
| G1 | 0,348% | 0,233% |
| G2 | 0,373% | 2,476% |
| B | 0,180% | 0,244% |
| G combinato | 0,232% | 1,178% |

I massimi coprono entrambe le calibrazioni, le due registrazioni e le due larghezze del deposito. Tre sorgenti rosse hanno superato l'1% in entrambi i bracci alternativi, sebbene il P90 rosso rimanga sotto lo 0,171%. Il test per la futura configurazione nativa deve quindi verificare che i campioni rifiutati contribuiscano zero anche al peso e riportare gli scostamenti per sorgente. Le due esecuzioni offline coincidono. Il comportamento in PixInsight e l'accuratezza assoluta restano da verificare. Esecuzioni native e chiusure scientifiche a zero.
SHA-256 archivio H: 1eb5f6a2126ac8a7e74b7158733c2200a9e5b41702eda6ff902480717b4dc822.
