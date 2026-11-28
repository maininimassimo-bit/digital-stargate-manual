# DSG Voice V1 — verifica della proiezione F9

La [PR #654](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/654) è stata integrata su main il 28 novembre 2026 alle 14:32 Europe/Rome. Il workflow BKL-031 salva il JSON validato come artefatto GitHub Actions per un giorno prima della pubblicazione ordinaria. La review indipendente ha approvato il canale per il collaudo. Alle 14:36 Europe/Rome il primo run schedulato dopo il merge era ancora atteso.

## Verifica del primo run

1. Individuare il primo run schedulato su main che include il merge della PR #654. Registrare il commit del run e l’esito del passaggio di upload.
2. Dalla root del repository, con GitHub CLI autenticata e main aggiornato, eseguire `python integrations/alexa/dsg-voice-v1/scripts/verify-f9-artifact.py RUN_ID`. Usare il validatore F9 della revisione del run per la verifica finale.
3. Registrare identificativo dell’artefatto, hash del JSON, età del run meteo e intervallo notturno. Verificare la copertura richiesta dal consumer e la soglia di 18 ore al momento della consultazione.

Lo ZIP deve contenere solo la proiezione F9. Il validatore del producer controlla il contratto, la freschezza e la protezione delle coordinate. L’artefatto GitHub è un canale di collaudo con download autenticato. Il collegamento automatico alla Lambda richiede un canale approvato e una verifica separata.

## Stato della skill

La skill è privata in Alexa Development e il reader F9 è disabilitato. Restano da qualificare il routing vocale dell’alias di indisponibilità, il test su Echo, le proiezioni per riepilogo, sessioni e avvisi, le verifiche di avviso budget e disattivazione backend e la review finale.
