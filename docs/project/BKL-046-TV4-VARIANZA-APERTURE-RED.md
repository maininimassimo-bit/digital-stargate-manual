# BKL-046 · Varianza in aperture di uguale area nei flat TV4 RED

La prova riusa le differenze di coppia del [test di varianza per pixel](BKL-046-TV4-VARIANZA-FLAT-RED.md). Misura la varianza delle somme su aperture disgiunte da 64 pixel per tre forme, 4 × 16, 16 × 4 e 8 × 8, indicate in ordine righe × colonne. Ogni combinazione usa 1.024 aperture per regione. Le forme condividono le immagini e sono valutate separatamente.

I tre modelli usano esclusivamente i tempi di calibrazione. Il primo moltiplica per 64 la varianza per pixel prevista. Il secondo applica a quel valore un fattore empirico stimato per regione e forma. Il terzo interpola direttamente la varianza misurata sulle aperture nei flat di calibrazione. Le verifiche sono le stesse a 33,5 e 303,5 ms, in cinque regioni.

| Modello | Gamma delle mediane d’errore su tempi e forme | Esiti entro il riferimento del 15% |
| --- | ---: | ---: |
| Pixel indipendenti | 18,08–43,55% | 6/30 |
| Fattore empirico per regione e forma | 8,38–28,70% | 17/30 |
| Interpolazione diretta in apertura | 10,81–22,76% | 12/30 |

Il rapporto fra varianza osservata in apertura e 64 volte la varianza osservata per pixel va da 0,96 a 2,77. A 33,5 ms l’errore mediano del modello a pixel indipendenti è 43,55% sulle aperture orizzontali e 18,08% sulle verticali. Il risultato distingue il comportamento delle somme dalla buona previsione per pixel, riprodotta in tutti i dieci controlli. Il riferimento del 15% è diagnostico. Altre acquisizioni, propagazione attraverso ricampionamento e incertezze fisiche restano da verificare. NOISE_FLUX/2 e NOISE_FLUX/3 restano aperti.

| Evidenza | SHA-256 |
| --- | --- |
| Protocollo | 44d1682cebd5254fe34f52eda5243d2ed9a438dce8e56805ec91a9b2f2d106c0 |
| Programma | 570ede4bd79f46cd8555f0a89997629809aa567d2a0ef11840ee8c40c2c44782 |
| Verifica appaiata | 8780269dddff534ee056a5221cc683375302f5dfd6cb5b9ceae410aae6dc0d04 |
| Riscontro replicato da H: | ff778ec8c42d8d1da726288ab3aa0ff138b0b7aa8a2f67a7ebaed46c15b1bd63 |
