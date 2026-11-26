# BKL-046 · Ripetibilità dei dark per le celle selezionate con SHASSA

Il protocollo confronta tre disposizioni fissate prima della nuova misura. Sono state rilette 14 pose dark da 180 secondi nelle 15 celle distinte richieste dalle tre disposizioni. La quindicesima posa resta esclusa. Il programma riproduce esattamente le misure già pubblicate nelle sei celle originali e riproduce gli esiti della partizione intercalata entro la tolleranza numerica. Applica alle differenze fra metà lo stesso fit planare e gli stessi profili digitali da 2 ADU. [Disposizioni SHASSA](../bkl046-m8-m20-shassa-anchor-geometry-v1/README.md) · [Misura su dark di riferimento](../bkl046-m8-m20-dark-anchor-repeatability-v1/README.md)

| Disposizione, media per cella | P95 errore relativo di forma sul profilo diffuso | Partizioni entro il 5% su flusso e forma |
| --- | ---: | ---: |
| Originale | 7,42% | 1.324/1.716 |
| Sei celle con Hα minima | 11,76% | 854/1.716 |
| Una cella con Hα minima per settore | 7,60% | 1.184/1.716 |

La disposizione per settore conserva un P95 vicino all'originale per il profilo diffuso. La quota entro soglia scende dal 77,2% al 69,0%. Anche i due filamenti superano la soglia nella maggior parte delle partizioni. Il rapporto contiene i dati sulla mediana per cella e i confronti intercalato e cronologico. Ogni confronto usa due metà disgiunte della stessa acquisizione. Le 1.716 partizioni riusano le pose e i percentili descrivono la sensibilità alla partizione.

Resta da misurare il fondo ottico coevo e da qualificare la relazione Hα–ADU. Il risultato riguarda gli assi `DIFFUSE_BACKGROUND/2` e `DIFFUSE_BACKGROUND/3`. Zero avvii PixInsight e zero chiusure scientifiche.

Per replicare, usare Python 3.12, NumPy 2.3.5 e Astropy 7.2.0. Gli argomenti in ordine sono il protocollo, il rapporto di selezione SHASSA, il precedente rapporto dark, lo ZIP dei dark, la ricevuta dei FITS dark, la directory del protocollo di iniezione, la directory estratta del fondo di riferimento, il rapporto completo scala e bordi, la directory dipendenze e il rapporto da creare. Le fonti archiviate sono fissate per impronta.
