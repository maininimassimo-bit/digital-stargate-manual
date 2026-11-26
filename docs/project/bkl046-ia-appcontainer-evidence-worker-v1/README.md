# BKL-046 — Valutatore IA isolato su ticket sintetici

Un processo Python separato in un AppContainer effimero elabora 32 ticket bilanciati. Il custode controlla token e SID del processo prima di avviarlo, disabilita l'ereditarietà degli handle e assegna zero capability all'AppContainer. Il processo riceve in lettura le richieste e il codice e scrive in un file di risposta predisposto. Il collaudo verifica che il processo riceva accesso negato sia in lettura sia in scrittura sul file delle etichette attese.

Dopo l'uscita, il custode confronta le 128 decisioni con le etichette attese, controlla che richieste ed etichette siano rimaste identiche e rimuove il profilo effimero. Per riprodurre la prova su Windows, eseguire verifica.py con worker.py nella stessa cartella, passando come argomenti la directory della fixture sintetica e un percorso ancora inesistente per la ricevuta. I digest degli input sono fissati nel verificatore.

La prova riguarda l'isolamento degli input nella fixture e l'esattezza del confronto sintetico. Zero unità indipendenti di conferma, chiamate a provider ed esecuzioni native. La raggiungibilità di rete non è stata misurata. Il risultato non chiude alcun criterio scientifico.
