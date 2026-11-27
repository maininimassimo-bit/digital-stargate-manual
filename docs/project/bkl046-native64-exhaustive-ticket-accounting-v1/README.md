# BKL-046 · Contabilità delle affermazioni IA sul corpus Native64

Il programma prova tutte le 81 combinazioni di quattro risposte YES, NO o ABSTAIN su ciascuno dei 64 pacchetti tecnici noti. Ricalcola le conclusioni dai conteggi e dai limiti di portata della richiesta, verifica la corrispondenza con gli esiti storici, quindi usa la funzione di adjudicazione congelata. La verifica conserva insieme le affermazioni positive infondate, le negazioni errate e le astensioni sullo stesso ticket.

| Caso nella griglia deterministica | Numero |
| --- | ---: |
| Vettori di risposta validi | 5.184 |
| Vettori interamente corretti | 64 |
| Vettori con almeno un'affermazione positiva infondata | 3.668 |
| Fra questi, vettori che contengono anche un'astensione | 2.770 |
| Vettori senza alcuna affermazione positiva ma con almeno una negazione errata | 484 |
| Ticket di prova con risposta assente o malformata | 128 |

Filtrare le risposte con astensione prima di contare le affermazioni infondate perderebbe 2.770 casi della griglia. Escludere le risposte assenti o malformate dalla contabilità farebbe sparire 128 ticket assegnati. Il verificatore registra questi ticket come irrisolti e verifica che il medesimo identificativo non possa essere riutilizzato nel collaudo.

Il conteggio descrive il contratto sul corpus tecnico noto. I vettori sono generati, le unità indipendenti confermative sono zero e nessun provider è stato interrogato. Restano da qualificare la popolazione, l'isolamento delle chiavi, il backend effettivo e il piano inferenziale Owner.

Per riprodurre usare Python 3.12 con protocollo, directory di adjudicazione Native64, directory di proiezione delle richieste e un nuovo percorso del rapporto. La pubblicazione contiene solo codice e contatori aggregati.
