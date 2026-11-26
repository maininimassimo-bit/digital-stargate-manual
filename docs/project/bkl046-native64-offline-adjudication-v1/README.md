# BKL-046 · Adjudicazione offline delle risposte al corpus tecnico Native64

La prova usa i 64 pacchetti storici di sviluppo e le chiavi di valutazione separate. Verifica la corrispondenza per impronta, ricalcola i totali dai conteggi per endpoint e confronta le quattro risposte attese con i conteggi e i metadati di portata. Un'affermazione positiva significa che i dati forniti sostengono la conclusione. Un'astensione lascia l'esito irrisolto. L'identificativo della risposta è legato a una prenotazione del collaudo e ai byte esatti del pacchetto.

| Controllo simulato | Esito |
| --- | --- |
| Risposte coerenti con le chiavi | 64 accettate e valutate senza errori |
| Quattro affermazioni positive | Almeno una falsa affermazione in 64 casi, 195 affermazioni errate in totale |
| Quattro risposte negative | 61 false negazioni a livello di singola affermazione |
| Astensione su tutte le domande | 64 irrisolti, zero false affermazioni |
| Risposta assente, campi mancanti, tipi o legami alterati | Assenze classificate separatamente. Risposte malformate respinte |
| Riutilizzo | 64 risposte respinte dopo la prima valutazione |

Gli 11 scenari per pacchetto sono fixture deterministiche. L'archivio conserva i 704 esiti e rilegge il corpus fissato su H:. La prova qualifica un controllo offline di valutazione. Le risposte non provengono da un modello o da un provider. Il corpus riusa sorgenti con risultati già noti e fornisce zero unità indipendenti. Restano da congelare una popolazione indipendente, l'isolamento operativo delle chiavi, il backend e le configurazioni del confronto, e da applicare il criterio Owner nel disegno confermativo.

Il programma riceve protocollo, directory del corpus con sottodirectory packets e oracle, e una directory nuova per i rapporti. La copia GitHub contiene codice e riepilogo. Nessun avvio PixInsight, chiamata a provider o nuova chiusura scientifica.