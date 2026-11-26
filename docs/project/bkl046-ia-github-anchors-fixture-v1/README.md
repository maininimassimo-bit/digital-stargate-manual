# BKL-046 · Ordine verificato dei due commit di prova IA

Per 32 ticket sintetici ho pubblicato prima il manifesto con i digest delle etichette, vincolati alle richieste e a valori casuali conservati localmente. Dopo la rilettura dal primo commit ho costruito e pubblicato il manifesto delle risposte terminali. I due commit aggiungono un solo file ciascuno. Le etichette aperte, i valori casuali e le risposte in chiaro restano fuori dai commit.

GitHub ha indicato come valide entrambe le firme. Il secondo commit ha come unico genitore il primo e il manifesto delle risposte indica lo stesso commit. I byte di entrambi i manifesti sono stati riscaricati e confrontati con i file locali. Il secondo manifesto registra 30 risposte sintetiche valutabili, una mancante e una malformata. Le chiavi locali hanno aperto tutti i 32 digest. [Commit delle etichette](https://github.com/maininimassimo-bit/digital-stargate-manual/commit/5d034b2ab7c64ba4418ab8412523a6d6f032d7b8) · [Commit delle risposte terminali](https://github.com/maininimassimo-bit/digital-stargate-manual/commit/3841b0e617d202eeb76a4445fb253506f178c0f9)

L'ordine attestato riguarda la sequenza dei due commit e le riletture durante questo collaudo. Il registro non attesta il momento in cui un provider reale avrebbe ricevuto i ticket, né il controllo dell'accesso alle chiavi da parte di identità separate. Gli oggetti di prova restano nella custodia H/K e le unità confermative sono zero.

Per ripetere la verifica locale usare Python 3.12 con `verifica.py verify <protocollo> <fascicolo-vincolo-oracolo> <fascicolo-fixture-evidenze> <directory-di-collaudo>`. La directory di collaudo deve contenere i due manifesti, le due ricevute di rilettura e le aperture sintetiche locali. Il verificatore crea un nuovo riscontro.
