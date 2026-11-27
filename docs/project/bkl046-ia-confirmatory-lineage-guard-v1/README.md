# BKL-046 · Controllo della provenienza per le partizioni IA

Il verificatore legge gli inventari fissati di GAIN, LIN0, M8–M20, IC 1805 e M51. Per ciascuna proposta di partizione confronta le impronte dei dati, gli antenati delle analisi derivate e lo stato di esposizione precedente. La modalità di trasferimento tra rivelatori verifica separatamente l'identità del rivelatore. Il controllo respinge anche unità duplicate, antenati ciclici o provenienza mancante.

| Partizione storica proposta | Riscontro |
| --- | --- |
| GAIN per la stima, LIN0 per la verifica | Nessuna impronta coincidente fra i segmenti archiviati. Le due serie sono già state esaminate. |
| GAIN → LIN0 come prova tra rivelatori | Entrambe le serie registrano l'unità Roman 21816. |
| GAIN come stima, rapporto derivato GAIN → LIN0 come verifica | Il rapporto incorpora GAIN. Le impronte dei segmenti ricompaiono risalendo la provenienza. |
| Calibratori M8–M20 per la stima, ricostruzione dello stesso campo per la verifica | La ricostruzione riutilizza i tre archivi di calibrazione. |
| M51 o Native64 come campioni ciechi | Entrambi sono già stati esaminati. Il fascicolo Native64 fornisce zero unità indipendenti. |

Le sei proposte storiche producono zero partizioni confermative ammesse. La prova positiva usa un oggetto sintetico con provenienza distinta. Attesta il comportamento del controllo. L'approvazione di un futuro campione richiede provenienza e separazione effettive, oltre a un protocollo congelato e al controllo dell'accesso alle chiavi.

Per riprodurre usare Python 3.12 con il protocollo, la radice dei fascicoli e un nuovo percorso per il rapporto. Nessun provider, avvio PixInsight o cambiamento nel registro del coordinatore.
