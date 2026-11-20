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


### Perimetro della prossima revisione

L’incarico R4 in `native-api-probe-operation-r4/INCARICO-REVISIONI-INDIPENDENTI.txt` richiede una revisione dell’intera operazione (62 input, 25 moduli). Il descrittore R4 ha SHA-256 `05d29ad31e64725c98c47263c994d94db51a24f93f6403cbdef673a83aeb8c04` e per quella composizione ARB ha richiesto modifiche. Lo ZIP R2 della VM contiene la correzione isolata e i suoi test. Prima della revisione formale occorre integrare la candidata in una composizione separata, verificarne le dipendenze e fissare il nuovo descrittore. La sequenza prevista è ARB sull’intera composizione, poi RQ dopo approvazione ARB.


La VM ha ricostruito in una cartella di lavoro separata tutti i 62 input del descrittore R4, controllandone lunghezza e SHA-256. La composizione candidata di lavoro conserva 60 impronte e sostituisce owner e root operator con i due moduli verificati offline. Il manifesto locale ha SHA-256 `d6c27e7cfbfe197a1a2323cfeff48529fe87cc52318c15f51f278d61eddb92b8`. Il modulo `probe_root_package_r3.cjs` conserva riferimenti R2: resta da allineare il caricamento e verificare la composizione attraverso il suo ingresso prima del congelamento per ARB.


Il nuovo descrittore candidato locale `ROOT-DESCRIPTOR-candidato.json` (SHA-256 `f4c7d448d436ed3743d9778418495176c55b97b93232ff6464454b0fcddf25e5`) associa root e owner ai moduli R3 e include il caricatore aggiornato `probe_root_package_r4.cjs`. Restano 59 input identici alla base R4 su 62. Nella prova offline il costruttore autentico ha verificato la composizione, comprese le dipendenze Python, e ha rifiutato il rapporto di prova PENDING con `API_PROBE_PACKAGE_EXACT_WHOLE_OPERATION_REVIEW`. Il caricamento operativo successivo richiede i due rapporti indipendenti sulla stessa impronta.


L’archivio locale `BKL051-composizione-ARB-20261120-r1.zip` raccoglie il descrittore candidato, i 62 file corrispondenti, il pacchetto test R2, le conoscenze e il manifesto. Controllati CRC e SHA-256 dopo la chiusura dello ZIP. Impronta dell’archivio `b95c579fe3ff72e868d3529fbe0f7323aaf6e20d7cac987e98f29ecd8b11a1a9`. Revisione ARB pendente.


### Campioni di memoria dell’operazione originale BKL-046

Letti su H tutti i 449 file `memory-*.json` dell’operazione `native-stream-hash-witness-001-h-v1`. Tutti riportano `continuousMemoryBoundAttested=false`, 448 dichiarano il riuso dell’handle originale e nessuno elenca motivi in `budgetReasons`. Il massimo valore registrato per `peakWorkingSetBytes` è 948084736 byte. Il verbale `preclose-state.json` indica ancora `AWAIT_FRESH_OWNED_EMPTY_UI_NORMAL_CLOSE_RECORD` e zero chiusure scientifiche. I dati descrivono l’esecuzione archiviata sull’host originario.


### Esito indipendente ARB e host di elaborazione

Il PC principale è l’host designato per l’elaborazione PixInsight. La verifica offline si è svolta su DSG-Shared. La compatibilità dei binari sul PC principale resta da verificare. Per il descrittore `f4c7d448d436ed3743d9778418495176c55b97b93232ff6464454b0fcddf25e5`, ARB ha emesso `CHANGES_REQUIRED`. Il caricamento canonico segue `PREFLIGHT-PINS.json`, seleziona il caricatore R3 e restituisce `API_PROBE_PACKAGE_EXACT_PINNED_MODULE` prima della lettura dei rapporti. Verificati 62 input e 25 moduli. La revisione RQ resta subordinata a una nuova approvazione ARB. Rapporto locale `BKL051-ARB-indipendente.json`, SHA-256 `ee9ce362dd19a7da531c7679dd2dfe0a0bd1e490e1386b2b4b4039d84efbb5f8`.


### Obiettivi di milestone verificati sul checkout di riferimento

BKL-046 riguarda l’assistente IA per il post-processing PixInsight. Il verbale di riapertura del 13 ottobre richiede studio verificabile di processi, script e PJSR installati, conoscenze versionate con provenienza e lacune, validazione scientifica per famiglia di workflow e criteri per integrare le conoscenze nell’IA. BKL-051 riguarda un modulo privato per il confronto di osservazioni, la ricerca di sorgenti variabili, candidati transienti e oggetti mobili, con validazione scientifica, dossier e segnalazioni assistite verso CBAT/TNS/VSX/MPC secondo le condizioni approvate. Fonti del checkout: `docs/project/BACKLOG.md`, `BKL-046-REOPENING-2026-10-13.md` e `BKL-051-SCIENTIFIC-TRANSIENT-CANDIDATES-2026-10-07.md`. La ripresa usa questi obiettivi documentati; il confronto integrale con le due chat originali resta da verificare. L’elaborazione futura è destinata al PC principale in modalità nascosta, subordinata ai gate e alla compatibilità del metodo con le prove richieste.


### Revisioni indipendenti della candidata VM R4

Il descrittore `33ab393c5bc5e13955a670c69096aeca6e2a7754d5bea60c5def9c92ce6cebc8` allinea i riferimenti transitivi anche nel processo Python. ARB APPROVED, rapporto SHA-256 `59726e4308940a15be7a7395f043e5064a8aac69f77d69377b35aa503827945a`. RQ CHANGES_REQUIRED sullo stesso descrittore, rapporto SHA-256 `d12e8760ab3c37e1cefd6c2fc5c34b0586d3d683c31566f7a607e777376154cb`. Dopo la chiusura anomala del custode simulato, la root ha ancora inviato il comando prepare al parent. Entrambi i revisori hanno verificato 62 input e 25 moduli. Il difetto richiede una nuova candidata e revisioni sul suo descrittore. Nessuna ammissione nativa.


### Candidata VM R5

ARB ha confermato che la perdita del custode impedisce nuovi comandi e conserva la possibilità di osservare la richiesta pendente. Sul descrittore `ed877a93c7024cc5d8024cfc4bb95c1fb65e997212cf4a3d5758052bb3506aa5` ha emesso CHANGES_REQUIRED dopo 186 regressioni e tre casi mirati. Un errore del custode durante l’attesa finale può ancora coesistere con la restituzione di `LEASE_RELEASED`. La prima causa e l’eventuale ricevuta vanno conservate distinguendo l’effetto osservato dalla conferma di completamento. Rapporto `BKL051-ARB-indipendente-r5.json`, SHA-256 `609b9848b8b0bb0e7d2a4be45fe966504e1bf920dff9f2c22193aa0e96b4bd3e`. Nessuna RQ su R5.


### Approvazioni indipendenti R6

ARB e RQ hanno entrambe approvato la composizione completa sul descrittore `63acf2da99156f8607021d54bfbfbfa48d735c7d0c94f72de2da4c435ef562e2` (62 input, 25 moduli). RQ ha rieseguito 186 regressioni, sei casi sul custode e quattro prove ulteriori. La causa originale e la ricevuta valida sono conservate e il rilascio resta singolo. SHA-256 dell’archivio `2a050af556f55309cc45e9a85be28b090beec5a5a4dfcdff70f6d1b01390b1fd`; rapporto ARB `c3dc1355e16b538676c81619e8a9a8717e0f6c45afe04b7a7560610c3750c9cf`; rapporto RQ `7f4f60c8ed1ecff32b43986aee8de2990d2ce4e3a8c6e475935492094cc582f8`. Approvazioni tecniche offline. Restano distinte la disponibilità sul PC principale, la compatibilità con l’elaborazione nascosta, l’ammissione operativa e la validazione scientifica.


### Consegna R6 e vincolo sul desktop

Lo ZIP locale `BKL051-ripresa-VM-20261120-r6-approvata.zip` raccoglie la composizione esatta, i due rapporti indipendenti e le conoscenze aggiornate. SHA-256 `71283ba44c91b8c60f85b519f1856d64b325c62cdc4610fa6b31b02d60a08306`. I punti 3–6 del piano richiedono di identificare la finestra originale, acquisire schermate e testo della console, verificare lo stato della finestra e osservarne la chiusura normale. Una sessione grafica separata sul PC principale è una possibilità da qualificare per rispettare il vincolo di non disturbare il desktop di lavoro. Disponibilità e comportamento di tale sessione restano da verificare.


La verifica dei binari R6 sul PC principale resta pendente. La shell collegata identifica DSG-SHARED. La procedura locale `Verifica-binari-PC-principale-R6.ps1` legge versione, lunghezza e SHA-256 di PixInsight e Python ai due percorsi del preflight. Il controllo di funzionamento sulla VM ha distinto PixInsight diverso e percorso Python assente. Nessuna sessione sul PC principale è stata verificata.


### Riscontro dal PC principale WIN-QOOF3903TQS

Il resoconto della verifica locale, trasmesso dall’Owner, identifica PixInsight 1.9.5 (77.608.944 byte) e Python 3.12.14 (107.312 byte). La VM ha confrontato le due impronte riportate con il preflight della composizione approvata da ARB/RQ, descrittore `63acf2da99156f8607021d54bfbfbfa48d735c7d0c94f72de2da4c435ef562e2`. Entrambe coincidono. Per PixInsight la build 1706 deriva dall’identificazione per hash nel piano. Per Python anche il bootstrap della composizione approvata fissa `50f885251e42eb8cd1fbf5d4fbcc01efdbe8b9f4d4379e16664d4d0f3d4a9869`. Il resoconto segnala un valore diverso nel separato manifest storico `K:/DSG051-CAL-R6/bootstrap-manifest.json`.

Al momento della verifica sul PC principale era presente una sola sessione grafica interattiva, console ID 1. PixInsight è rimasto chiuso. Restano da qualificare una sessione isolata e la capacità di osservare finestra, console e uscita originale senza interferire con il desktop di lavoro. Il riscontro non autorizza un avvio nativo o il rilascio del gate.
