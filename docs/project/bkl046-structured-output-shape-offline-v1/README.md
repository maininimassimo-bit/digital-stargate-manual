# BKL-046 · Forma Structured Outputs e controllo locale delle decisioni

La candidata dello schema locale usa una scelta alla radice e l'operatore not. La guida OpenAI richiede un oggetto alla radice e indica not fra gli operatori non supportati. La nuova forma sperimentale usa un oggetto chiuso con il campo obbligatorio decision e sposta i rami delle azioni all'interno del campo. Il controllo delle prove identiche rimane nel runtime. [Guida Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs?api-mode=responses)

Sulle 1.680 decisioni archiviate la nuova forma consente tutte le 16 decisioni valide. Due prove identiche risultano formalmente ammesse e vengono respinte dal runtime. Il controllo finale coincide con il contratto storico sul campione. I test aggiuntivi respingono un oggetto senza involucro, un campo esterno inatteso e un testo che supera il limite UTF-8.

Il test verifica in locale i vincoli strutturali controllati. Il formato richiederebbe una revisione dell'integrazione perché modifica l'involucro della risposta. Restano da verificare il supporto dello schema sul modello esatto, rifiuti e risposte incomplete da un provider e la qualificazione end-to-end. Nessun deployment, richiesta a provider o avvio PixInsight.

Il programma riceve protocollo, kit dello schema locale, directory delle fonti storiche e un nuovo file di uscita. [Schema locale di partenza](../bkl046-adapter-action-specific-schema-offline-v1/README.md)