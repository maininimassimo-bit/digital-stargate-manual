# BKL-046 · Verifica del campione IA a quota fissata

Il collaudo usa un elenco sintetico di 957 unità, con un ticket per unità e impronte fissate prima della valutazione. Il programma controlla che tutti i ticket assegnati abbiano un esito terminale. Mantiene i mancanti e i malformati nel denominatore, registra separatamente le negazioni errate e conserva l'eventuale compresenza di affermazioni infondate e astensioni.

| Caso di verifica | Eventi infondati accertati | Eventi nel limite prudenziale | Calcolo alla soglia dell'1% |
| --- | ---: | ---: | --- |
| Una sola unità con affermazione infondata e astensione | 1 | 1 | Entrambi i calcoli sotto il limite di decisione |
| Una unità con affermazione infondata e una diversa senza risposta | 1 | 2 | Passa il conteggio accertato, fallisce quello prudenziale |
| Una risposta assente e una malformata, senza eventi accertati | 0 | 2 | Passa il conteggio accertato, fallisce quello prudenziale |
| Solo negazioni errate | 0 | 0 | Passa la sola metrica delle affermazioni infondate, con 957 negazioni errate registrate |

Il limite prudenziale conta come potenzialmente problematico ogni ticket irrisolto. L'unione evita di contare due volte il medesimo ticket. È un'analisi di sensibilità del disegno, non un nuovo criterio Owner. Il test respinge campioni incompleti, doppie risposte, unità duplicate, impronte alterate, legami difformi, ticket ancora assegnati e flag incompatibili. Il confronto usa la coda binomiale esatta con errore unilaterale 1/1.400 del caso illustrativo precedente.

Le 957 unità sono fixture di test. Nessun campione reale, backend o accesso indipendente alle chiavi è stato qualificato. Le unità confermative accertate restano zero.

Per ripetere usare Python 3.12 con il protocollo, i riscontri fissati di potenza e persistenza e un nuovo percorso di uscita.
