# BKL-046 · Stato dei percorsi nativi su DSG-Shared

Ho verificato in sola lettura il pacchetto Stream34 v11, il runtime, gli otto ingressi, il registro di studio e le impronte del coordinatore installato. Il registro canonico risultava libero al momento della lettura e l'inventario indicava zero processi PixInsight. La sola misurazione diagnostica riportava 11,46 GiB di memoria fisica disponibile e 12,40 GiB di commit disponibile. Le soglie di lancio sono 8 e 12 GiB nel processo effettivo.

| Percorso | Evidenza riletta | Requisito operativo residuo |
| --- | --- | --- |
| Stream34 v11 | Soggetto esatto e 70 membri verificati, preflight diagnostico riuscito | Verbale ARB autentico sul soggetto, poi RQ vincolato ai byte dell'ARB, attestazioni d'origine, trust autenticato e iscrizione operativa |
| CFA Origine v3 | Fascicolo con 56 file del launcher, piano e controlli | ARB e RQ autentici sul soggetto, posa protetta e iscrizione |
| CFA XDRZ v4 | Soggetto e collaudo con chiavi di prova | ARB e RQ autentici, ingresso gestito protetto e identità registrate |
| Primary2048, build 1719 | Soggetto del dossier e impronta del dispatcher | ARB e RQ riferiti a questa build e binding operativo |
| ImageAnalysis | Indice e impronte del fascicolo tecnico | Integrare osservazione dell'istanza, gestione della chiusura e custodia in un launcher sottoponibile a revisione |

Il soggetto Stream34 v11 è `0b029846da0412875e26595e2ead8361bc35fcef2c882ec2be95303b9582bdd1`. Nel fascicolo non sono stati trovati i cinque file attesi per l'ingresso delle revisioni. La PR #627 era aperta e non riportava richieste o oggetti di review. La ricerca riguarda le collocazioni fissate nei fascicoli e la PR. Il rapporto conserva le impronte dei diversi soggetti e degli archivi letti. [PR #627](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/627) · [Verifica dei verbali Stream34](../bkl046-stream34-v11-review-intake-offline-v1/README.md)

L'ammissione è ancora un passaggio del coordinatore per ogni prova, dopo la catena di autorizzazione e i controlli operativi. Il controllo non ha avviato PixInsight, richiesto ammissione o mutato il registro. La replica verifica lo snapshot archiviato. La disponibilità di memoria e lo stato del registro possono cambiare fra la lettura diagnostica e il lancio.
