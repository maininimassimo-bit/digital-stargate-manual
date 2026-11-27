# BKL-046 · Controllo offline delle risposte del backend

Il collaudo usa il formato documentato di Responses, con un modello fittizio a identità fissata. Il consumatore accetta un solo messaggio assistente completato e un solo contenuto strutturato. I contenuti di ragionamento possono accompagnare il messaggio. Rifiuti, risposte incomplete e azioni di strumenti inattese si fermano prima della validazione della decisione. [Riferimento Responses](https://developers.openai.com/api/reference/resources/responses/methods/create)

Le 16 decisioni valide del contratto archiviato passano senza modifiche. Diciassette fixture negative coprono stato incompleto, rifiuto esplicito o misto a testo, identità modello difforme, contenuti ambigui, JSON malformato o non finito e riuso dell'identificativo. Dopo il parsing si applicano ancora i controlli del formato e del runtime. Il legame con uno stato diverso e il superamento del limite UTF-8 vengono respinti a questi livelli.

Il collaudo riguarda corpi di risposta simulati e un registro di riuso in memoria. La provenienza HTTP, la persistenza dei record, l'identità del modello effettivo e la risposta del provider restano da verificare. Non è stato effettuato alcun deployment, invio al provider o avvio PixInsight.

Il programma riceve protocollo, kit della forma di risposta, kit dello schema locale, directory delle fonti storiche e un nuovo file di rapporto. [Forma della risposta e validazione locale](../bkl046-structured-output-shape-offline-v1/README.md)