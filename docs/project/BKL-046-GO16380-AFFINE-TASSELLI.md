# BKL-046 · Traslazione e modello affine su due pose profonde GO16380

Il confronto su Omega Centauri conserva le correzioni WCS della [prova precedente](BKL-046-GO16380-CORRELAZIONE-WCS.md) per le due guide e per il controllo breve. Per la seconda posa profonda, `jeg055lnq`, la correzione WCS è stimata di nuovo sui soli tasselli pari. Il confronto rifitta entrambi i modelli sui tasselli pari ed esclude 56 pixel dai bordi di tutti i tasselli, sia per la stima sia per la verifica. Le due pose condividono campo e guide e hanno integrazioni del sensore distinte.

| Posa da 400 s | Sensore | Stelle per stima / verifica | P90 traslazione | P90 affine |
| --- | ---: | ---: | ---: | ---: |
| jeg055llq | 1 | 55 / 41 | 0,499718 px | 0,210211 px |
| jeg055llq | 2 | 42 / 41 | 0,464141 px | 0,098425 px |
| jeg055lnq | 1 | 56 / 43 | 0,486438 px | 0,169743 px |
| jeg055lnq | 2 | 42 / 42 | 0,459295 px | 0,102381 px |

Il modello affine riduce l'errore su entrambi i sensori. Il sensore 1 resta sopra 0,1 pixel in entrambe le pose. Il sensore 2 rientra nel limite soltanto nella prima posa. Il risultato sul singolo sensore quindi non si conferma nella replica.

Sugli stessi riferimenti di verifica, le due guide proiettate nella posa lunga differiscono con P90 fra 0,073 e 0,095 pixel. La coppia breve, dopo la traslazione stimata sui tasselli pari, mostra un P90 fra 0,184 e 0,273 pixel nel sistema A40. L'accordo fra guide è una misura relativa e lascia aperta l'accuratezza rispetto alla posa lunga. L'asse `SATURATION_BLEND/4` resta aperto. Nessuna sostituzione di pixel, prova nativa o chiusura scientifica.

| Evidenza conservata | SHA-256 |
| --- | --- |
| Protocollo prima posa | `82ea4c861f22c9759fbf77fe6b37a239cb598684a6bd9414054330d4184282db` |
| Ricevuta prima posa | `eea78884ba50d06402cf791b4103851dffe698cd038ab332f8adfe131a46f1d4` |
| Protocollo replica | `c095b752a91276674fc4f63b02e8f204a2e2987bcbd6d97b417fccbf82e72c6d` |
| Ricevuta replica | `00f1f2830ad73315bdc219e4062f145f02af0c992faec6f6c03c8c563b310dd7` |
