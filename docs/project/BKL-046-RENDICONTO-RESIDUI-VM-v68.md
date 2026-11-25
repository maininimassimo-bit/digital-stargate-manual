# BKL-046 — Rendiconto residui DSG-Shared v68

Ho esteso il [rendiconto v67](BKL-046-RENDICONTO-RESIDUI-VM-v67.md) con sette note TV4, rilette al commit `2d557a7275eb58ba3113dd13b76fafe6704bb26d`. Le impronte Git dei testi coincidono con il confronto di otto commit. Su H: ho riletto 220.680.721 byte in sette archivi e verificato 16 membri JSON. La verifica dalla copia su K: ha prodotto lo stesso rendiconto.

L'asse `DIFFUSE_BACKGROUND/2` ora comprende il riallineamento della sfera TV4 documentato a metà della sequenza, il controllo di rumore a sette livelli, il confronto con 24 dark e i test di conservazione del flusso. La sottrazione per riga riduce il rumore correlato nel controllo ma rimuove i segnali iniettati che occupano tutta la riga. Una maschera ricavata da fotogrammi disgiunti perde ancora circa l'11% del flusso della gaussiana larga e non rileva i segnali costanti lungo la riga. Restano aperti il riferimento ottico indipendente, il trasferimento a immagini scientifiche e il confronto nativo. [Riallineamento della sfera](BKL-046-TV4-CLEAR1-RIALLINEAMENTO.md) · [Maschera su frame disgiunti](BKL-046-TV4-RIGA-MASCHERA-DISGIUNTA.md)

Il perimetro resta di 4.920 requisiti e 14.521 criteri, con sette famiglie, 25 assi e 19 criteri Owner aperti, zero nuove chiusure scientifiche e zero avvii nativi. La capsula v1.171 resta una baseline intermedia recuperabile localmente. Il puntatore di rendiconto avanza preservando i byte e lo stato di consegna della capsula. [Indice della conoscenza](BKL-046-KNOWLEDGE-DELIVERY-v1.171.json)

| Evidenza | SHA-256 |
| --- | --- |
| Rendiconto v67 | b25e78878bd689f4fb2a142c0b9677e948195394e1ae3d18ded4d08feb11609b |
| Rendiconto v68 | d8ff40bdbbff037d2368f798c457faf82e00e1ab8a816cfb5faa7c3514b8fd7a |
| Archivio v68 riletto su H: | 5c06b9637fb95f4dbcdff6265fa0c815ae47874f5b9f7581ee14b18eedfa3be3 |
