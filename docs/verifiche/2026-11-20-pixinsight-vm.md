# PixInsight nella VM di elaborazione — 20 novembre 2026

Il setup Windows ha completato l’installazione di PixInsight. I campi ProductVersion e FileVersion dell’eseguibile installato riportano entrambi 1.9.6. La distribuzione commerciale identifica il pacchetto come build 1719. La verifica ha utilizzato i metadati del file. Il primo avvio, l’attivazione e le prove di elaborazione restano da verificare.

## Evidenze disponibili per la ripresa

- **BKL-046.** L’osservazione 448 del test NATIVE_STREAM_HASH_WITNESS_001 registra una lettura stabile e la corrispondenza dell’hash. Il verdetto conserva aperte le attestazioni di origine nativa, custodia, memoria e uscita del processo originale. L’osservazione non autorizza un nuovo tentativo o il rilascio del gate comune.
- **BKL-051.** Il rapporto di allineamento del 18 novembre registra il rilascio della sola prenotazione fallita della R3. Per il piano operativo R4 il rilievo ARB-APIOP-R4-001 riguarda l’ordine tra la registrazione dei listener error/close e la validazione del processo figlio. Alla data di quel rapporto servivano modifiche e la revisione RQ non era iniziata.

Questa verifica documenta l’ambiente di elaborazione. Le due milestone restano aperte e l’autorizzazione a una prova nativa deve essere verificata sul registro canonico prima dell’esecuzione.

## Verifica CI di H126

Il 20 novembre 2026 GitHub riportava sette workflow completati con esito positivo sul commit `e47e224353748f6e8da84e05550ba4afd5dc1eca` della [PR #627](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/627). La PR era ancora in bozza. I risultati riguardano la CI del repository. La validazione scientifica e i 456 casi nativi indicati nel rendiconto H126 restano aperti.

## Candidato offline BKL-051

Nel workspace della VM è stato preparato un successore isolato di `probe_common_owner_r2.cjs`. Registra gli eventi `error` e `close` prima di leggere PID, handle e stream. Otto verifiche con EventEmitter coprono i ruoli guardian e parent nei casi ordinario, PID assente, getter che solleva un errore e registrazione parziale dei listener. Nessun processo nativo o lease è stato creato. La verifica è limitata al metodo di acquisizione del figlio. Restano da verificare integrazione con il canale, revisione indipendente e archiviazione su K:. SHA-256 del candidato: `91324731c2e84faf6547c9c83865d65f1e15cfe3a80f2484049247e731f53b75`.

L’esame del chiamante R2 ha individuato una seconda finestra: il callback costruiva il canale prima di restituire il figlio al proprietario. Nel candidato integrato il proprietario registra il figlio, poi passa lo stesso oggetto al costruttore del canale. Un test offline con il canale R2 originale e un errore di registrazione sullo stream conferma la conservazione del primo errore, del successivo errore asincrono e dell’evento di chiusura. Le otto prove precedenti continuano a passare. Il modello sostituisce l’ammissione esterna e non verifica il protocollo nativo. SHA-256 aggiornati: owner `4cd2163e0727443c28f842acbb6768f66fca241826db894b29c4a3d744b49c4c`, root operator `a6d95c70336b9553f87a9daf2d029fc8bb189dff120c725e31aa89b7c2ad41de`.
