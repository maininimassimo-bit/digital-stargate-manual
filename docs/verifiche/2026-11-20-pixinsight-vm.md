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

La suite preesistente del chiamante è stata eseguita sul candidato con i riferimenti ai nuovi moduli. Sei casi su dodici superano le verifiche preliminari (cinque invocazioni non valide e un pacchetto respinto prima dell’ammissione). Negli altri sei il modello si ferma alla lettura di `coordinator.py` dal percorso canonico, assente nella VM (`ENOENT`). Il verificatore richiede per questo file 10.650 byte e SHA-256 `a07b2614414c399181f4ffbf07750f870fdfdf159987539f7e1de3d9b3c0c613`. Le asserzioni successive sull’ammissione, l’attesa, la custodia e il rilascio restano da verificare.

## Integrità delle osservazioni BKL-046

La rilettura dalla VM della sequenza da 1 a 448 ha verificato la continuità degli indici. Per tutte le 417 catture dichiarate dai verbali, dimensione e SHA-256 ricalcolati coincidono con i valori registrati. Le altre 31 osservazioni non dichiarano una cattura. Le 417 catture hanno un unico hash (`5e791b5cdad9791bb98d72e0c14ac9c294304a14f179d452abe5c42cbad29bdd`); quella dell’osservazione 448 misura 4.124 byte. Sono letture archiviate ripetute dello stesso contenuto. Origine nativa, limite continuo di memoria, uscita del processo e rilascio del gate richiedono prove distinte.

## Archivi intermedi della ripresa

La VM ha prodotto due ZIP con sorgenti, `conoscenze.json` e manifesto SHA-256. La rilettura integrale ha verificato contenuti e CRC. Il deposito canonico resta in sospeso per entrambi.

| Archivio | SHA-256 |
| --- | --- |
| `BKL046-ripresa-VM-20261120-r1.zip` | `6982bf15086b56002212375c696faf47fb7afac6246a57f9f6b0217958bd2d48` |
| `BKL051-ripresa-VM-20261120-r1.zip` | `abe6fe1b7212746cb3568c3a8ba8956e8237c22dc35328ce7340c87d2ded3278` |


### Memoria disponibile nella VM

Una lettura puntuale di Windows GetPerformanceInfo ha rilevato 5,999 GiB di RAM totale, 2,306 GiB di RAM disponibile e 3,184 GiB di margine di commit. Il gate BKL-046 richiede evidenze continue durante il lavoro nativo. Questa misura a riposo lascia la verifica aperta.


### Dipendenze del coordinatore BKL-051

Nessuno dei cinque percorsi del descrittore `coordinator-trust.json` risulta presente nella VM. Oltre a `coordinator.py` occorrono `original-parent-adapter.cjs`, `MANIFEST-R4.json`, `ARB-R4.md` e `RQ-R4.md`. Nel deposito Git di K: l’unico blob da 10650 byte ha SHA-256 `abc37971d9dfe049709abd934bf3c89468ea3d7df506d14bccf559d29b29ff93`. Il coordinatore richiesto ha SHA-256 `a07b2614414c399181f4ffbf07750f870fdfdf159987539f7e1de3d9b3c0c613`.


### Regressione offline BKL-051 completata

Il percorso `calibration-api-probe-integration-20261117-r1/full-runtime-retention-private-r7-test/MODEL-common` nella condivisione di lavoro K contiene tutti e cinque i file del coordinatore. Lunghezze e SHA-256 coincidono con le cinque righe di `coordinator-trust.json`. Per la sola durata del test in Node, le letture dei cinque percorsi originali hanno restituito in memoria i rispettivi byte verificati. I dodici casi di `check-each-root-case.cjs` sulla candidata locale hanno restituito PASS (uscita 0), con processi e stato modellati. La candidata resta da sottoporre alla revisione prevista. L'esecuzione nativa resta vincolata al gate.


Il pacchetto locale `BKL051-ripresa-VM-20261120-r2.zip` include la candidata, il file di conoscenze aggiornato, gli esiti dei dodici casi e il comando ripetibile `node codice/run-root-model.cjs`. Dopo l’estrazione sulla VM sono state verificate tutte le impronte del manifesto e ripetuti i test con esito positivo. SHA-256 dello ZIP `0d8fa076a5171e7c4f9e54c8b4fe1f0e8fad3529d3a593e44fd08df02897558d`. Destinazione finale K ancora in attesa di scrittura autorizzata.


### Verifica offline del rilascio BKL-051

Dallo ZIP R2 estratto in una cartella temporanea è stata eseguita anche la suite `test_probe_common_owner_release_r3.cjs`. Per ripeterla si può duplicare `codice/run-root-model.cjs` nella stessa cartella e cambiare il solo modulo caricato dall’ultimo `require` in `./test_probe_common_owner_release_r3.cjs`. Il verificatore salva il risultato accanto al codice e richiede un’estrazione nuova. Tutti e dieci i casi riportano PASS. Coprono il rilascio ordinario simulato, il coordinatore occupato, il rifiuto di una ricevuta errata e il controllo delle dipendenze al momento del rilascio. Il modello dichiara zero avvii di processi e zero scritture sullo stato condiviso. La revisione indipendente resta aperta.
