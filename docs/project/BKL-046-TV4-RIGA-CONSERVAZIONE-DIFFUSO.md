# BKL-046 — Conservazione del segnale diffuso dopo la sottrazione per riga

Ho iniettato profili noti a picco di 4 DN su 12 differenze dark e quattro differenze CLEAR1 a comando zero. Per ogni riga lo stimatore usa 64 colonne e valuta le altre 64. Il confronto con la stessa differenza senza iniezione isola la variazione di segnale causata dalla sottrazione. Tutte le iniezioni usano una regione centrale confinata a un singolo quadrante. [Controllo dei dark](BKL-046-TV4-CLEAR1-DARK-CONTROLLO.md)

| Profilo iniettato | Flusso recuperato senza maschera | Flusso recuperato con maschera |
| --- | ---: | ---: |
| Gaussiana compatta, σ orizzontale 8 px | 99,97% | 99,97% |
| Gaussiana larga, σ orizzontale 21 px | 88,98% | 98,79% |
| Banda gaussiana che occupa tutta la riga | 0% | Veto per supporto insufficiente |
| Fondo uniforme | 0% | Veto per supporto insufficiente |

La maschera usa la posizione esatta del segnale iniettato e richiede almeno 32 pixel disponibili per riga nella metà usata per stimare l'offset. Una componente uniforme lungo la riga viene assorbita integralmente dall'offset in assenza di una misura separata. La riduzione del rumore osservata nei dark non basta quindi a qualificare la conservazione del segnale diffuso. Il test copre segnali artificiali su differenze reali. Resta aperta la verifica con maschere ottenute da dati indipendenti e confronto nativo.

| Evidenza | SHA-256 |
| --- | --- |
| Riscontro e replay identico | ce12144576cfed8c13372b9429212c2ce8bda30936cd5b907f94aced620aeb65 |
| Archivio riletto su H: | 7408022973528f383fae51910690b8eae2bb7978203e2e5f429d9c405da750b1 |

Zero esecuzioni native e zero chiusure scientifiche in questo incremento.
