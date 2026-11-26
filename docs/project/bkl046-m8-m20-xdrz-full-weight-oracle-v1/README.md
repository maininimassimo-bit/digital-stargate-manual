# Oracolo offline dei pesi XDRZ su 48 × 48 pixel

Il calcolo BKL-046 estende all’intera mappa la regione diagnostica 14-1-0. Usa i 28 ritagli FITS calibrati, la validità di ciascun campione e le matrici unitarie e pesate della baseline M8–M20. Calcola pesi, intensità e supporto RGB per i depositi da 1,00 e 0,70 pixel, inclusi i controlli senza rigetto e con valori azzerati a peso conservato.

Ritagliando l’uscita a 29 × 29, il supporto coincide esattamente con l’oracolo precedente. Gli scarti massimi sono 3,56 × 10⁻¹⁵ nei pesi e 1,12 × 10⁻¹⁶ nelle intensità codificate. Con il rigetto applicato, tutti i 12 massimi per canale, geometria e deposito sono maggiori nella mappa completa che nel ritaglio. La differenza massima è 0,00947 nelle unità dei pesi offline.

L’oracolo rende confrontabili tre ipotesi offline: pesi grezzi, normalizzazione al massimo globale e normalizzazione separata per canale. Le ultime due producono mappe attese che differiscono di almeno 0,387 al loro punto di massima differenza in ogni combinazione di geometria e deposito. I denominatori derivano dalle mappe attese, senza adattarli ai FITS osservati. La modalità usata da PixInsight resta da misurare sul controllo nativo.

Per replicare eseguire `misura.py <protocollo.json> <riscontro-scala-comune.json> <codice-baseline.py> <zip-calibrati> <oracolo-29.zip> <pacchetti-Python> <directory-output-vuota>`.
