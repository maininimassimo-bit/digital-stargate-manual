# BKL-046 · Evidenza numerica e metadati in Native64

Il controllo rilegge le 64 richieste già fissate e confronta tre regole deterministiche sulle 256 affermazioni. I conteggi per endpoint sono ricostruiti prima della valutazione. Due risposte per ticket derivano da quei conteggi. Le altre due riguardano la validazione della varianza di popolazione e l'ammissione scientifica. I loro valori sono presenti direttamente nei metadati della richiesta.

| Regola | Affermazioni corrette | Negazioni errate | Astensioni | Ticket interamente corretti |
| --- | ---: | ---: | ---: | ---: |
| Rispondere sempre NO | 195/256 | 61 | 0 | 4/64 |
| Usare solo i conteggi e astenersi sulle altre due affermazioni | 128/256 | 0 | 128 | 0/64 |
| Usare i conteggi e copiare i due valori dichiarati | 256/256 | 0 | 0 | 64/64 |

Le modifiche sintetiche ai due valori dichiarati cambiano soltanto le conclusioni di portata. I conteggi numerici rimangono identici. Il punteggio perfetto misura la lettura di un formato tecnico noto. Native64 conserva la sua utilità per le regressioni di parsing e di adjudicazione. Una prova confermativa della capacità di giudicare le evidenze deve distinguere ciò che l'IA ricava dalle misure da ciò che il protocollo le comunica già come verdetto.

I casi sintetici non sono nuovi esiti del workflow. Non sono stati interrogati provider. Le unità indipendenti confermative restano zero.

Per ripetere usare Python 3.12 con il protocollo, il file delle richieste Native64, il rapporto di contabilizzazione esaustiva e un nuovo percorso di uscita.
