# BKL-046 · Catena R4 con finestra testimone per l'origine XDRZ

Il parent legato tramite FD3 riceve l'ID della prenotazione isolata, le impronte dei record R4 e l'impronta del rapporto del classificatore. Il parent usa la custodia v4 per associare la finestra testimone al processo originale, acquisirne il BMP, autorizzare una sola chiusura ordinaria e attendere l'uscita. Il supervisore verifica che il verbale di chiusura rimandi alla stessa prenotazione, allo stesso marcatore, al BMP e al rapporto validati. Gli ingressi rimangono sotto custodia fino all'uscita del parent. Il rilascio avviene durante la custodia dei 16 oggetti su H:, che comprendono anche il BMP e il verbale di chiusura.

| Scenario | Esito |
| --- | --- |
| Finestra originale e rapporto integro | BMP verificato, chiusura ordinaria e uscita zero. R4 emette una sola ricevuta di prova dopo la rilettura dell'archivio su H:. Apertura in scrittura del BMP respinta durante il rilascio. |
| Richiesta rivolta alla finestra omonima estranea | Acquisizione e chiusura respinte. Parent esce con codice 8, prenotazione isolata trattenuta. |
| Rapporto alterato dopo acquisizione | Chiusura respinta. Parent esce con codice 8, prenotazione isolata trattenuta. |

Le finestre e i processi testimone sono reali. I prodotti e inventario PixInsight sono simulati. Il rapporto aggregato omette i BMP, che rimangono nelle directory di prova. Il custode ha operato soltanto sul registro isolato. Il kit permette di revisionare la catena di prova. Restano da collegare il lancio effettivo con i pin del batch, l'attivazione protetta e le approvazioni prima dell'ammissione del coordinatore. [Custodia di ingressi e archivio](../bkl046-cfa-origin-integrated-custody-v1/README.md)

Argomenti del collaudo Node: Python fissato, kit di verifica del batch, fonti del custode degli ingressi, parent_barrier.py CFA v4, dipendenze, directory nuova del registro di prova, radice esistente su H: per l'archivio di prova e nuovo rapporto. I moduli della finestra testimone sono inclusi nel kit.