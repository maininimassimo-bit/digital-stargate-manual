# Incertezza del confronto cromatico Gaia XP per M8–M20

Lo studio ricampiona le 19 stelle già riservate alla verifica, con gli stessi abbinamenti per i due modelli di risposta, le calibrazioni e i centri delle aperture. Gli zeri cromatici restano fissati sulle 20 stelle di stima. Sono stati calcolati 20.000 ricampionamenti per stella e tutte le 256 estrazioni ordinate con reinserimento dalle quattro regioni occupate.

| Modello e calibrazione | Differenza P90 pesato meno unitario (mag) | Percentili spaziali 2,5–97,5% (mag) |
| --- | ---: | ---: |
| Sony QE, A | −0,0073 | [−0,0209, +0,0091] |
| Sony QE, B | −0,0288 | [−0,0371, +0,0043] |
| Siril IMX571, A | +0,0003 | [−0,0209, +0,0091] |
| Siril IMX571, B | −0,0252 | [−0,0326, +0,0043] |

Tutti gli intervalli di ricampionamento attraversano lo zero, sia per stella sia per regione. In B il miglioramento sopravvive alla rimozione di ciascuna regione, ma cambia segno per almeno una rimozione di singola stella in entrambi i modelli. I percentili misurano la sensibilità del risultato al campione osservato. Quattro regioni e gli zeri cromatici fissi limitano l’inferenza. La pesatura resta un comparatore candidato per BKL-046.

Per replicare eseguire `misura.py <protocollo.json> <riscontro-aperture-XP.json> <gaia.json> <pacchetti-Python> <nuovo-riscontro.json>`.
