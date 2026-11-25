# BKL-046 · Controllo dello spazio di coordinate della maschera XDRZ

Due mosaici CFA sintetici RGGB formano un controllo di 32 × 28 pixel con traslazione asimmetrica. Lo XDRZ mascherato contiene un solo bit di rigetto nel canale verde, alle coordinate (14, 7). Il pacchetto comprende uno XDRZ senza maschera e uno con lo stesso bit sul canale sbagliato. I campi XML e i tre piani della maschera sono stati riletti e verificati contro la struttura del serializzatore PCL installato.

| Modello per lo stesso bit di rigetto | Verde al punto (13, 8), intensità / peso | Verde al punto (14, 7), intensità / peso |
| --- | ---: | ---: |
| Maschera in coordinate del sensore | 0,25 / 1 | 0,49 / 2 |
| Maschera in coordinate del riferimento | 0,50 / 2 | 0,18 / 1 |
| Maschera assente o sul canale sbagliato | 0,50 / 2 | 0,49 / 2 |

Il comparatore verifica sull'intera immagine le intensità RGB supportate, il supporto e i pesi grezzi. Distingue un unico esito compatibile e, nel percorso di verifica del rigetto, respinge il caso senza effetto e le uscite ambigue. Il collaudo offline ha riconosciuto i quattro casi attesi e respinto due alterazioni. Le due generazioni coincidono su tutti i 17 file. Manifest SHA-256 `d21357169e031363ea3e85943f092594ca470c74988841713df5efdad256dd40`.

PixInsight deve ancora essere verificato con l'esportazione delle intensità lineari e dei pesi grezzi. Solo l'esito nativo può determinare come trasferire i 985 campioni esclusi degli input scientifici. Zero esecuzioni native.
