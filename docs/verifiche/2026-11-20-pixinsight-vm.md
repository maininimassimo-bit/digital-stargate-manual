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


### Esito della verifica della sessione isolata sul PC principale

Secondo il resoconto locale trasmesso dall’Owner, su WIN-QOOF3903TQS la console ID 1 era l’unica sessione interattiva sia all’inizio sia alla fine. Nessuna finestra di prova aperta, nessuna cattura o misura del focus e del cursore. Il collegamento RDP non è stato tentato per il possibile impatto sulla console. Windows Sandbox risulta disabilitata e l’inventario Hyper-V è stato negato. Un eventuale test nella VM Hyper-V riguarderebbe il guest e lascerebbe aperta la verifica di PixInsight installato sull’host fisico. Esito per l’host: isolamento grafico non dimostrato; nessuna elaborazione avviata. I gate e i piani restano invariati.


### Autorizzazione aggiornata per la console del PC principale

L’Owner ha autorizzato l’esecuzione visibile di PixInsight su WIN-QOOF3903TQS e rinviato la verifica della modalità nascosta. La disponibilità di una sessione isolata cessa di essere un prerequisito per questa ripresa. Il pacchetto BKL-051 R6 conserva le approvazioni ARB/RQ sul descrittore `63acf2da99156f8607021d54bfbfbfa48d735c7d0c94f72de2da4c435ef562e2`. Il prossimo controllo operativo va effettuato sul PC principale: disponibilità dei file approvati ai percorsi attesi e stato attuale del coordinatore secondo il piano. Il verbale storico BKL-046 resta in attesa della prova di chiusura originale. Nessuna nuova esecuzione nativa osservata da DSG-Shared.


### Esito del tentativo BKL-051 R6 sul PC principale

Secondo il messaggio conclusivo del tentativo, riportato dall’Owner, il controllo preliminare si è fermato prima della richiesta di prenotazione. In quel momento `active.json` riportava ancora la prenotazione BKL-046 `ea2a08ea-c95c-44d3-b961-52aa8bf1b9d2`; mancava la ricevuta di rilascio e il PID del custode risultava assente. Per questo tentativo BKL-051 R6 non ha ottenuto alcun ID di prenotazione o codice di rifiuto. PixInsight è rimasto chiuso. La ricevuta di acquisizione citata dal PC principale identifica la prenotazione BKL-046. Tra le evidenze consultate non risulta un verbale distinto associato al descrittore R6. Lo stato descritto si riferisce al momento del controllo.


### Verifica della via di recupero BKL-046

Per `ea2a08ea-c95c-44d3-b961-52aa8bf1b9d2`, i file storici su H legano l’operazione `BKL046_NATIVE_STREAM_HASH_WITNESS_001` al custode PID 42296 (creationFiletime 134394750196503804), al parent PID 22484 (134394750206584212) e al processo nativo PID 32732 (134394750300302248). Il runtime-context dichiara esplicitamente di non aver letto lo stato condiviso. Il verbale di prechiusura attende ancora la registrazione della chiusura originale. Il piano di recupero dopo perdita di custodia reperito su K è specifico di BKL-051, prenotazione `298420bd-0d19-4dd3-927a-2ced168678dc`, fallita prima dell’avvio nativo. Per BKL-046 occorre riscontrare sul PC principale le identità complete e le ricevute correnti; se la custodia è perduta, il percorso eccezionale deve essere qualificato per questa prenotazione conservando come sconosciuta l’uscita originale finché priva di prova. Nessun rilascio o nuovo tentativo avviato dalla VM.


### Controllo in sola lettura sul PC principale

Lo script seguente confronta i tre registri prima e dopo il controllo dei tre processi. Due letture uguali documentano soltanto gli estremi dell’intervallo. L’assenza di un PID non dimostra la chiusura normale e nessun esito dello script autorizza automaticamente il rilascio. Sintassi e rifiuto di esecuzione sulla VM verificati; il riscontro operativo deve provenire dal PC principale.

```powershell
# Inventario puntuale. Eseguire nella sessione del PC principale.
$ErrorActionPreference = 'Stop'
if ([Environment]::MachineName -ine 'WIN-QOOF3903TQS') {
    throw 'Verifica riservata al PC principale WIN-QOOF3903TQS.'
}
$stateDir = 'K:\DigitalStarGate\pixinsight-coordination-20261114-r1\state'
$reservation = 'ea2a08ea-c95c-44d3-b961-52aa8bf1b9d2'
function Read-Record([string]$name) {
    $path = Join-Path $stateDir $name
    try {
        $raw = [IO.File]::ReadAllBytes($path)
    } catch [IO.FileNotFoundException] {
        return [ordered]@{ file = $name; state = 'file assente' }
    }
    $sha = [Security.Cryptography.SHA256]::Create()
    try {
        $digest = [BitConverter]::ToString($sha.ComputeHash($raw)).Replace('-', '')
    } finally { $sha.Dispose() }
    $record = [Text.Encoding]::UTF8.GetString($raw).TrimStart([char]0xFEFF) | ConvertFrom-Json
    return [ordered]@{ file = $name; state = 'letto'; sha256 = $digest; reservation = $record.reservation; milestone = $record.milestone; operation = $record.operation }
}
function Read-Records {
    foreach ($name in @('active.json', "$reservation-acquired.json", "$reservation-released.json")) {
        Read-Record $name
    }
}
$before = @(Read-Records)
$identities = foreach ($item in @(
    @{ role = 'custode'; number = 42296; birth = '134394750196503804' }
    @{ role = 'parent'; number = 22484; birth = '134394750206584212' }
    @{ role = 'PixInsight'; number = 32732; birth = '134394750300302248' }
)) {
    $actual = $null
    try {
        $process = [Diagnostics.Process]::GetProcessById($item.number)
        try { $actual = $process.StartTime.ToUniversalTime().ToFileTimeUtc().ToString() }
        finally { $process.Dispose() }
        $status = if ($actual -eq $item.birth) { 'identita coincidente' } else { 'PID riutilizzato' }
    } catch [ArgumentException] { $status = 'PID assente al controllo' }
      catch { $status = 'identita non verificabile: ' + $_.Exception.Message }
    [ordered]@{ role = $item.role; pid = $item.number; expectedBirth = $item.birth; observedBirth = $actual; state = $status }
}
$after = @(Read-Records)
[ordered]@{
    computer = [Environment]::MachineName
    utc = [DateTime]::UtcNow.ToString('o')
    before = $before
    processes = @($identities)
    after = $after
    sameAtBothReads = (ConvertTo-Json $before -Compress) -ceq (ConvertTo-Json $after -Compress)
} | ConvertTo-Json -Depth 6
```


### Passaggio a elaborazione sulla VM DSG-Shared

L’Owner ha designato DSG-Shared per lo sviluppo, la verifica e l’elaborazione PixInsight di entrambe le milestone. Il collaudo della collaborazione precedente è riuscito con il commento `7050080153`; l’incarico `7050086796` chiede al PC principale di disattivare la propria automazione. Il pianificatore sulla VM è stato aggiornato per seguire la migrazione locale.

La VM dispone di PixInsight 1.9.6 Lockhart, 82.432.472 byte, SHA-256 `76d2339130b58be3d112b66cafc578d9f859d80c96842b2ba2dfbbdcdc8b2943`. Il runtime Python 3.12.14 locale ha SHA-256 `5699bdfd4b6924c69d0a1f6b1d75d7760698567ce81b92d4fcc8bb2af4eeba84`. Entrambi differiscono dalle impronte di BKL-051 R6. Per usare questi binari occorre una candidata separata, verificata sul nuovo ambiente e revisionata. La shell gestita ha ricevuto accesso di rete negato su `H:/Codex` e `K:/DigitalStarGate/BKL051/work`. Il registro comune non è leggibile al percorso atteso dalla VM. Il precedente riscontro BKL-046 resta storico e il cambio di host non costituisce rilascio. Nessuna prova di milestone avviata.


### Ripristino delle letture e qualifica offline sulla VM

L’accesso in sola lettura a `DSG-H-Codex$` e `DSG-K-Work$` è stato verificato con una concessione valida per il turno. Il `default_permissions` del profilo utente è stato allineato al profilo gestito `dsg-shared-smb-managed` già presente nei requisiti amministrativi, con rilettura del valore salvato. La prova senza concessione in un nuovo avvio è pendente.

Python 3.12.14 AMD64 è stato eseguito in modalità isolata con una prova SHA-256. Tutti i 62 input R6 sono stati verificati per dimensione e hash; i 25 moduli Python sono stati compilati in memoria. Otto file contengono riferimenti al vecchio host, percorso o binario: quattro moduli Python, due moduli Node e i manifesti bootstrap e preflight. Il pacchetto R6 è conservato; serve un successore separato per qualificare l’elaborazione con PixInsight 1.9.6.

Su H il verbale BKL-046 attende ancora la prova di chiusura originale. Il coordinatore comune non è disponibile alla VM sul percorso atteso. Il piano di recupero reperibile su K riguarda una prenotazione diversa e documenta una procedura legata a identità, ricevute, revisione e lock comune esistente. Nessuna scrittura sul gate o esecuzione nativa.


### Nuovo turno senza concessioni e candidata sorgente BKL-051

Nel nuovo turno, pur con `dsg-shared-smb-managed` salvato nel profilo utente, i quattro UNC rispondono con `0x80070041`. Le letture di H e K senza concessioni restano indisponibili. Creato sulla VM `BKL051-DSG-Shared-candidata-offline-r1.zip`, SHA-256 `50fd939e8b9e4268546958c7238c829670459e0e5f29e41c4656a951b18f7aa4`. Il pacchetto sorgente aggiorna sei moduli per i binari locali. Verificati i 62 input di base, la compilazione dei 25 moduli Python, la sintassi dei due moduli Node aggiornati e otto casi modellati. Restano da ricomporre manifesti e pin transitivi sul percorso operativo, completare le revisioni e qualificare il comportamento nativo tramite il coordinatore. Il nuovo obiettivo dà precedenza alla verifica della pubblicazione BKL-046 v571/v1.146. Nessun publisher avviato o interrotto dalla VM.


### Verifica della pubblicazione v571 / conoscenza v1.146

La ricerca GitHub dei commit con `v571`, `v1.146` o `H146` e delle PR con `v1.146` non ha restituito una corrispondenza. La PR #627 descrive H126 e resta una fonte storica. Da DSG-Shared non è visibile una sessione del publisher né un verbale terminale di v571. La verifica richiede il risultato del publisher originale e la rilettura degli artefatti di conoscenza su H con confronto delle impronte e della destinazione GitHub dichiarata. Stato della pubblicazione indeterminato. Nessun avvio, riavvio o arresto del publisher.


### Rilettura delle pubblicazioni su H

La successiva lettura autorizzata di H ha risolto l’incertezza sulla pubblicazione locale v571. `Ricevuta-terminale-publisher-v571-v1.json` registra uscita 0. Il rapporto indipendente è `PASS_INDEPENDENT_POST_COMMIT_V1146`; SHA-256 ricalcolato di `Conoscenza-PixInsight-v1.146.json`: `7b11789d0616b54cb002c506f0bd2c4e4cfb123a0569f8c409a09da67b2e567e`.

Il deposito contiene anche la pubblicazione successiva v599. Il verbale `publication-v599-g-v1/terminal.json` registra `V599_V1171_PUBLISHED_AND_POSTVERIFIED_NOT_FINAL_MILESTONE`, con rapporto indipendente `PASS_INDEPENDENT_POST_PUBLICATION_V1171_V599`. SHA-256 ricalcolato di `Conoscenza-PixInsight-v1.171.json`: `65511eaafd15af1ea7c7f07cdd90d7947d622b6d6f88b31f022e9ac2399c4c0d`. Entrambe le impronte coincidono con i rispettivi rapporti. Zero chiusure scientifiche e studio incompleto in entrambi gli esiti. La rilettura integrale dei byte da GitHub resta da verificare. Nessuna azione sul publisher. Il coordinamento futuro delle due milestone deve risiedere interamente sulla VM; la prenotazione storica resta soggetta alla procedura di recupero del coordinatore comune.


### Rendiconto analitico v599 dei requisiti BKL-046

La matrice archiviata coincide con SHA-256 `8de48c420407538900cbb4d38cacde84ea55cc2bb5d5437037780c259fb1936c` del rapporto v1.171. Il join per ID tra matrice, registro v45 e successore di lavoro post171 coincide per 4.920 righe univoche e conserva criteri e disposizioni. Il CSV locale `BKL046-rendiconto-requisiti-v599-4920.csv` riporta residuo, criteri, prossima azione e impronta della riga. Rilette 4.920 righe (125 processi, 368 script, 239 oggetti e 4.188 membri PJSR), per 14.521 criteri. Disposizioni: 4.887 con completamento non provato, 26 con evidenze parziali, 6 revisioni circoscritte dei metadati e 1 esclusione motivata di API interna, tutte e sette in attesa delle rispettive attestazioni. Nessuna chiusura scientifica derivata. SHA-256 CSV `9ba878ce5f85827c86d3188c40fcc3bb53b911fc4e1ad8791c84d5c391e22f0a`. La richiesta di scrittura per il solo CSV su H non ha concesso accesso.


### Composizione offline BKL-051 per DSG-Shared

Il successore locale `BKL051-DSG-Shared-composizione-offline-r1.zip` ha SHA-256 `5bc285f2d8a43802866b5760004887529d476c92b59f92e7cb670dabd2725e9d` e descrittore `1df6c9efcb4300e85639ff85c01236259bfa67eacd30fe4d3916a192bf6c71d1`. I binari VM sono legati a preflight, bootstrap e invocazione. Sono state aggiornate le impronte dei moduli Python e i tre riferimenti Node usati dal processo Python. Il piano è stato copiato a byte identici in un percorso successore. Verificati integralmente lo ZIP, i 62 input e i 25 moduli Python. L’ingresso canonico indicato dal preflight ha verificato le dipendenze su dati d’archivio e ha raggiunto il rifiuto atteso in assenza delle revisioni genuine. I percorsi operativi, il coordinatore comune sulla VM, la review indipendente e la qualifica PixInsight nativa restano aperti. Nessuna operazione nativa avviata.


### Componenti da predisporre per le successive prove scientifiche su DSG-Shared

| Prova | Componente e condizione |
| --- | --- |
| BKL-046, calibrazione spettrofotometrica SPCC | Scaricare i cataloghi locali Gaia DR3/SP in formato `.xpsd` da PixInsight Software Distribution e registrarli nelle preferenze del processo Gaia. Il manuale incluso con PixInsight 1.9.6 riporta 4 file e 11,1 GiB per il set piccolo, normalmente adatto a campi ampi o moderati, e 20 file e 63,2 GiB per il set completo, da prevedere quando densità stellare e campo della prova lo richiedono. Sul volume C della VM risultavano circa 47,7 GiB liberi al controllo, quindi il set completo richiede un altro volume con spazio sufficiente. |
| BKL-046 e BKL-051, soluzione astrometrica offline con ImageSolver | Predisporre Gaia DR3 astrometrico in formato XPSD quando il protocollo richiede il plate solving locale. Fissare catalogo, copertura e impronte secondo i campi della prova. ImageSolver e il modulo Gaia sono già presenti. |
| BKL-051, oggetti mobili | CometAlignment, EphemerisGenerator e il file `core-asteroids.xeph` sono già presenti nella VM. Eventuali effemeridi supplementari dipendono dagli oggetti e dagli intervalli temporali del protocollo. |
| BKL-051, prova di compatibilità API | Il piano circoscrive il test a JavaScript e SHA-256. Nessun catalogo aggiuntivo previsto per questa prova. Il piano congelato cita ancora 1.9.5 build 1706. La candidata VM va revisionata per 1.9.6 e ogni esecuzione richiede l’ammissione del coordinatore comune. |

Nelle cartelle ispezionate sulla VM non sono stati individuati file `.xpsd`. La configurazione Gaia effettiva va verificata al momento della prova. Prima di congelare un protocollo, registrare versione, nome, dimensione, SHA-256 e percorso dei file selezionati. La pagina di distribuzione non era consultabile dalla sessione. I requisiti sopra provengono dai manuali ufficiali inclusi nell’installazione. Nessun download o installazione eseguiti. [Manuale SPCC](https://pixinsight.com/doc/docs/SPCC/SPCC.html) · [Manuale ImageSolver](https://pixinsight.com/doc/scripts/ImageSolver/ImageSolver.html) · [Distribuzione PixInsight](https://pixinsight.com/dist/)


### Piano successore BKL-051 VM R2

Lo ZIP locale `BKL051-DSG-Shared-composizione-offline-r2.zip` ha SHA-256 `148c27f9a6663ecc5258587f50d2eecfb8dddce333fdc926e49fa2cf9273e2e5` e descrittore `a4f0e69680bedf6aeaeba35dbc5701ba89a8592cbf34e3307a3fd19880f2c00b`. Il nuovo piano identifica PixInsight 1.9.6 e richiede coordinatore e nativo su DSG-Shared. I percorsi del successore e le impronte del piano e delle dipendenze sono aggiornati. Le regole di ammissione, custodia, chiusura e recupero sono preservate. Lo ZIP e tutti i membri sono stati riletti. L’ingresso canonico, con le letture modellate, supera la verifica delle dipendenze e rifiuta l’ingresso senza rapporti autentici. Sulla R1 sono passati 37 test Node (12 root, 10 rilascio, 1 canale, 8 acquisizione e 6 custodia) e 114 casi Python (94 ammissione e 20 diagnostica), tutti offline. Le revisioni della R2 e i percorsi operativi sono ancora da verificare. La richiesta di scrittura per l’archivio R2 su K non ha concesso accesso.


### Doppia approvazione offline BKL-051 sulla VM e memoria BKL-046

ARB R2 ha riprodotto il rifiuto `EVIDENCE_OUTSIDE_APPROVED_ROOTS` nel lettore del processo padre: ammetteva il file Python del vecchio host. La R3 aggiorna il solo percorso esatto del binario Python e mantiene i controlli del lettore. La lettura effettiva del binario VM ha restituito 107.312 byte. ARB e RQ R3 hanno approvato lo stesso descrittore `b61179d6d702b1358515c60ff3dca82be7886e7b2fe8866f626c47a554985cb2`; rispettivamente 192 e 196 casi offline. SHA-256 del rapporto ARB `cf5afc033cb8aee82f568e70bf1a73d9e4bb026dd7fb50a500472a7eb5a9f212`, del rapporto RQ `cb9f0dd729912bd694bf51d7ce6af3314d67163dc95a9ff0d249858af0825ec2`. Archivio VM `BKL051-DSG-Shared-r3-approvata-offline.zip`, SHA-256 `e1254d52eef2d94487f5e14365e1e6828b7f3ca779a870be22efd301ac3e4584`. `CURRENT.json` e i cinque file comuni risultano ancora WinError 3 sul percorso canonico. Nessuna ammissione o esecuzione nativa.

La VM riportava 5,999 GiB di RAM fisica, 2,566 GiB disponibili, limite di commit 7,874 GiB e commit disponibile 3,264 GiB. Con la configurazione misurata il limite totale è inferiore alla soglia di 12 GiB disponibili riportata in PR #627 per il caso BKL-046. Il caso rimane non avviabile con questa configurazione.


### Inventario per il coordinatore comune su DSG-Shared

Ricalcolate da K le cinque impronte e lunghezze dei file comuni in `calibration-api-probe-integration-20261117-r1/full-runtime-retention-private-r7-test/MODEL-common`. I file `coordinator.py`, `original-parent-adapter.cjs`, `MANIFEST-R4.json`, `ARB-R4.md` e `RQ-R4.md` coincidono con il preflight DSG-Shared R3. La copia di prova non contiene `CURRENT.json`. Il preflight richiede un `CURRENT.json` di 1.426 byte, SHA-256 `6ec823dcd577c7d238b1f37778a90e9825c6ec111f81a88c27086bfbfb32e1bf`. Ricerca mirata nei tre alberi di lavoro relativi al probe, al recupero BKL-051 e alla revisione incrociata senza risultato. Il rapporto `primary2048-suffix196-coordination-recovery-review-h-v1/report.json` riguarda `7f005a11-1d2b-4f1d-a42b-4056ef2f131c`, una prenotazione BKL-046 diversa da `ea2a08ea-c95c-44d3-b961-52aa8bf1b9d2`.

Per l’installazione operativa sulla VM servono la configurazione canonica verificata e la riconciliazione dello stato originale con la prenotazione storica. Un laboratorio con file di modello non fornisce questo stato. Il coordinatore deve avere una sola istanza operativa e un unico stato comune utilizzato da entrambe le milestone. Nessuna inizializzazione o azione di rilascio effettuata.


### Studio documentale CometAlignment per BKL-046

Requisito `process:CometAlignment`, riga v599 `afffe8932bb177bb1307eff2f3b05f16cbd973db6e9ea409847768be72da64c9`. Il manuale installato descrive la precedenza di `Observation:Time:Start` su `DATE-OBS`, l'interpolazione temporale tra fotogrammi fissi, il riferimento e il ruolo dei fotogrammi disabilitati. Il documento locale `BKL046-CometAlignment-contratto-e-protocollo-v1.md` (SHA-256 `8bdb1980b57465fd8a48ce8b688709d6cff4b8747ff6c700e94bb83edfb615bb`) fissa le impronte di modulo e manuale e propone cinque casi discriminanti con coordinate attese. I numeri sono stati verificati analiticamente. La proposta resta in attesa di confronto con le evidenze archiviate, revisione e ammissione alla prova. Stato di chiusura del requisito invariato.


La riconciliazione CometAlignment con la matrice v599 e il registro post171 ha confermato che la scheda anteriore copre parametri, sottrazione e integrazione, con `nativeValidation=NOT_ESTABLISHED` e campo `closureEvidence` vuoto. L’impronta del manuale registrato allora differisce da quella della VM. Il nuovo artefatto `BKL046-CometAlignment-riconciliazione-v1.json` (SHA-256 `8ba84249eb2906b45c0a4f2df78ab11cfefc3c7be6ea8717a8a2ccd41edf8793`) registra entrambe le fonti e i centri analitici esatti, inclusa la distinzione tra la proprietà XISF a 5 s e il keyword FITS a 10 s. Il primo controllo geometrico isola l’interpolazione temporale, con PSF, sottrazione, drizzle e sovrascrittura disattivati. Fixture native, revisione e ammissione restano aperte. Zero chiusure scientifiche.


Per CometAlignment è pronto l’archivio locale `BKL046-CometAlignment-fixture-FITS-v1.zip`, SHA-256 `26f59c261229f8d74d8d9f7d25b4244b3846126fc9bedb4c71440e6068432bac`. Contiene cinque frame sintetici FITS con tempi irregolari, un caso separato con `DATE-OBS` malformato, il generatore e il manifesto. La rilettura ha verificato struttura, timestamp, somma dei pixel, centroidi razionali esatti e byte dell’archivio. L’orientamento delle coordinate in PixInsight resta da verificare prima del confronto nativo. La fixture separata per il conflitto tra proprietà XISF e keyword FITS, la tolleranza di uscita, la revisione e l’ammissione del coordinatore restano aperte.


Per isolare la precedenza temporale di CometAlignment, preparato `BKL046-CometAlignment-fixture-XISF-v1.zip`, SHA-256 `235c438cf904b90f11e4071996f69ad827ef29a474acd0968af4facf0d913374`. I due XISF 64×64 contengono identici valori UInt16, confrontati con il FITS diagnostico. Entrambi contengono DATE-OBS a 10 s. Soltanto quello in conflitto contiene anche la proprietà TimePoint Observation:Time:Start a 5 s. I centri attesi sono rispettivamente (22,5; 20,5) e (25; 21) con le ancore stabilite. Verificati attacco dei campioni, metadati e integrità dello ZIP. Restano la lettura nativa, la convenzione delle coordinate e la tolleranza di confronto dopo revisione e ammissione del coordinatore. Zero chiusure scientifiche.


Il protocollo geometrico candidato `BKL046-CometAlignment-protocollo-geometrico-v2.md` lega modulo e fixture alle impronte ricalcolate sulla VM. SHA-256 del protocollo `296de949302d84f6609db702fc75f99999aed02da0163d4dff31a4f093aa5b99`. La soglia di 0,25 pixel e la risoluzione di lettura di 0,1 pixel valgono per i centri e gli offset prima del ricampionamento, con orientamento verificato sulle ancore. Le due ipotesi di precedenza temporale distano circa 2,55 pixel. Il protocollo resta da revisionare e ammettere sul coordinatore comune della VM. Esito scientifico aperto.


### Requisiti aggiuntivi del coordinatore comune R4 sulla VM

`MANIFEST-R4.json` include anche `COORDINAMENTO.md`, `test_coordinator.py`, `TESTS-R4.txt` e `AGENTS-APPEND.txt`. Trovata la copia archivio di `COORDINAMENTO.md` su K e ricalcolato lo SHA-256 `7f05102ce6160d7cd8181853b09a491949f0ac46290177582fa099c4a574142e`, corrispondente al manifesto. Gli altri tre file e `CURRENT.json` non sono emersi nei tre alberi di lavoro interrogati.

La copia byte-identica di `coordinator.py` è stata caricata per eseguire esclusivamente `scan_pixinsight()` su DSG-Shared. Il comando CIM esatto nella sessione Codex ha restituito codice 1 e «Accesso a una risorsa CIM non disponibile per il client». Questo è un ulteriore prerequisito operativo anche qualora i file canonici diventino disponibili. Il coordinatore deve poter completare l’inventario nel suo contesto di esecuzione sulla VM. Un errore di inventario mantiene il rifiuto di ammissione. Non è stato acquisito alcun lock, né è stato toccato lo stato.


### Regressioni isolate del coordinatore comune sulla VM

Eseguito il codice `coordinator.py` con SHA-256 `a07b2614414c399181f4ffbf07750f870fdfdf159987539f7e1de3d9b3c0c613`, sempre con stato sintetico in cartelle temporanee e scanner modellato. Una prenotazione residua simulata respinge sia BKL-046 sia BKL-051 prima dell’inventario e conserva `active.json` byte per byte. In uno scenario separato, il lock esclusivo Windows impedisce la seconda ammissione mentre la prima è detenuta; un esito nonzero del parent mantiene `active.json` e non produce la ricevuta di rilascio. Sono prove del comportamento di rifiuto sulla VM. L’accesso al coordinatore canonico, l’inventario CIM nel suo contesto operativo e la riconciliazione della prenotazione storica restano prerequisiti per l’operatività. Nessuna scrittura sul coordinatore reale.


### Consegna di lavoro BKL-046 e prerequisiti del trasferimento

La consegna locale `BKL046-ripresa-v599-CometAlignment-v1.zip`, SHA-256 `71e9f97ea58da101b93a91e8b42ef96aea7e351aa43b13e3bce9faa29c961010`, riunisce il rendiconto, il riscontro delle pubblicazioni, la riconciliazione, le fixture e il protocollo geometrico. Tutti i membri corrispondono al manifesto SHA-256 verificato. Deposito su H in attesa di un contesto con scrittura; lettura H autorizzata dall’Owner, ma questa sessione non vede la condivisione.

Il piano del sigillo finale prevede inventario completo dopo chiusura dello studio, verifica indipendente del file consolidato, trasferimento dei byte e recupero remoto. Le prove in tre parti su v1.166 sono ricostruzioni locali già archiviate. Il programma H-v6 ammette destinazioni nuove dentro la radice H e non esegue chiamate GitHub. La documentazione GitHub conferma il limite inferiore a 2 GiB per ciascun asset di Release. Il file v1.171 è di 3.030.957.683 byte. La sessione non ha potuto leggere l’elenco delle Release del repository, quindi la presenza di asset remoti non è verificata. [Documentazione GitHub sulle Release](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)


Il riferimento numerico offline CometAlignment `BKL046-CometAlignment-riferimento-bilineare-v1.json`, SHA-256 `29003bec1ab52f0dcc0b94922eb5054f6834dddfcfc256b2ce0d00638469d42a`, calcola dai campioni FITS effettivi centro, somma e varianza per asse usando aritmetica razionale. A 5 secondi il centro ideale dopo allineamento è (20; 20), con varianza di 0,5 pixel² per asse e somma 1.024. Interpretando gli stessi campioni come esposti a 10 secondi, il centro ideale diventa (17,5; 19,5), con varianza di 0,25 pixel² per asse. È un riferimento del modello bilineare senza bordi. La corrispondenza con ricampionamento e normalizzazione effettivi resta da misurare dopo ammissione. Zero chiusure scientifiche.


Per la sottrazione CometAlignment è stato verificato il controllo analitico `BKL046-CometAlignment-riferimento-sottrazione-v1.json`, SHA-256 `3b04db601ce6179926b1ceabb9691714fab9f7f8cee11cb8c1fec0ca4a6683f6`. Con quattro frame indipendenti di varianza unitaria, sottrarre a ogni frame la media degli stessi frame dà varianza residua 3/4 e covarianza tra residui −1/4. Sottrarre una media comune da un insieme matematicamente indipendente dà 5/4 e +1/4. L’enumerazione esatta verifica 16 e 256 stati rispettivamente. Il secondo caso è un comparatore teorico, separato dai vincoli dell’operando nel manuale. I rami di fit, normalizzazione, reiezione e trasformazione restano da qualificare nativamente. Nessuna chiusura scientifica.


### Chiusura dell’automazione sul PC principale e risorse della VM

L’esecuzione pianificata sul PC principale ha confermato nel commento `7050374281` la rimozione della sua automazione, in risposta all’incarico `7050086796`. Il coordinamento futuro e PixInsight rimangono assegnati a DSG-Shared. La conferma di rimozione riguarda l’automazione e lascia aperto il trasferimento operativo del coordinatore e la riconciliazione della prenotazione BKL-046.

Nuova misura DSG-Shared: 5,999 GiB di RAM totale, 2,496 GiB disponibili, 7,874 GiB di limite commit, 4,591 GiB usati e 3,283 GiB disponibili. Con un carico invariato, la soglia di 12 GiB disponibili richiederebbe almeno 16,591 GiB di limite totale. È un limite inferiore ricavato dalla misura, non il dimensionamento definitivo della VM. La disponibilità di commit e gli altri criteri del piano vanno riletti nel contesto di esecuzione. `CURRENT.json`, coordinatore e stato canonico restano inaccessibili al percorso previsto.


### Riscontro della configurazione SMB effettiva

`codex-cli 0.171.0-alpha.13` supera la soglia 0.138.0 documentata per le allowlist gestite. Il valore `default_permissions` coincide nei due file di configurazione con `dsg-shared-smb-managed`; nei file interrogati non risultano le chiavi legacy `sandbox_mode` e `allowed_sandbox_modes`. Nella sessione effettiva il controllo UNC restituisce ancora `0x80070041`, mentre la precedente concessione puntuale di sola lettura aveva consentito i due accessi. Questo confronto restringe la diagnosi alla proiezione effettiva delle autorizzazioni del runtime della sessione; non identifica quale livello le abbia sostituite. La lettura H resta autorizzata dall’Owner. La verifica successiva va eseguita in una sessione a cui il gestore dell’ambiente abbia applicato esplicitamente il profilo. [Configurazione Codex](https://learn.chatgpt.com/docs/config-file/config-reference)


Per `process:ImageCalibration`, riga v599 `452ef672bb8a4ca3fffe8700c221df0d51041a3fbeacc33fc801c99dd0222877`, è pronto il controllo analitico `BKL046-ImageCalibration-riferimento-flat-dark-v1.json`, SHA-256 `05efb75bbed827b1618f079c59988063996e35986912ddf552b1bb6c9dec9264`. Il manuale installato richiede un confronto diretto con un flat-dark per valutare eventuali sostituti. Nel modello a due livelli e normalizzazione media fissata, un errore proporzionale nei flat si cancella mentre l'errore spazialmente non proporzionale (100, 300) genera scarti esatti 200/27 e −200/41. La coppia discrimina i due casi controllati. Restano aperti la riproduzione nativa, il confronto su acquisizioni fisiche e le relative incertezze. Nessuna modifica ai master o chiusura scientifica.


L’archivio `BKL046-ImageCalibration-fixture-flat-dark-FITS-v1.zip` (SHA-256 `9f2732ed44302733d96592dd3c510556cbdfe6ec4e5b44eef651f3ad0d49dc1d`) contiene sei file sintetici a due regioni, il manifesto e i generatori. Riletti integralmente i campioni. Le sottrazioni e la normalizzazione del modello producono esattamente 1.000 in entrambe le regioni per flat-dark corrispondente e controllo proporzionale, 27200/27 e 40800/41 con la sostituzione bias. Il collaudo nativo richiede impostazioni d’importazione e unità di uscita congelate, revisione e ammissione del coordinatore. Master esistenti e stato scientifico invariati.


Per ImageCalibration è pronto il protocollo per revisione `BKL046-ImageCalibration-protocollo-flat-dark-v1.md`, SHA-256 `37e24317c71372e44e3cea647d11c727aafbf841b62217e4c514821a9be08040`. Le impronte delle fixture, del riferimento numerico e del manuale sono state rilette e confrontate. Il controllo del rapporto mediana sinistra/destra usa 1 per i due controlli e 82/81 per il caso bias sostitutivo, tolleranza assoluta proposta di 0,002 e incertezza massima di lettura 0,0005. Le bande restano disgiunte anche includendo quest’ultima. Il protocollo richiede verifica della scala d’importazione, zero piedistallo, output XISF Float32 e controllo dei livelli assoluti. La revisione, l’ammissione operativa e le misure native restano aperte.


### Supplemento di lavoro alla conoscenza v1.171

Il file locale `BKL046-conoscenza-v1.171-supplemento-VM-v1.json`, SHA-256 `3707a48408c7846a264036875233230c279426316d70a0010944db7c3b07d076`, lega dieci artefatti CometAlignment e ImageCalibration alla baseline v599 e alle due righe di requisito. Sono presenti dimensioni, impronte e ruoli degli artefatti. Sono stati riletti gli ZIP e verificata la corrispondenza di requisiti e criteri al rendiconto di 4.920 righe. I due requisiti conservano le disposizioni v599, con revisione ed esecuzione native pendenti. Il supplemento è separato dalla conoscenza pubblicata e ha zero chiusure scientifiche.


Il verificatore locale `verify-coordinator-r4-snapshot.py`, SHA-256 `5ed2d450915fa95103f5d976c43d91429956300afe0108d7bcb0a15a6a8e6871`, confronta un percorso in sola lettura con il pacchetto VM R3 verificato. Distingue impronta esatta, contenuto diverso, percorso assente e lettura negata. Legge active, acquired e released della prenotazione BKL-046 agli estremi del controllo, senza acquisire il lock. Provato sui due percorsi: sul percorso canonico della VM mancano i sei file e i tre registri, nella copia offline corrispondono i cinque file comuni mentre `CURRENT.json` manca. Il riscontro non attesta ammissione; resta necessario uno snapshot originale con provenienza e stato verificabili.


Il protocollo ImageCalibration v2 `BKL046-ImageCalibration-protocollo-flat-dark-v2.md`, SHA-256 `7cfd4c7c9f13408b4cce14cf7556a5e2b193d4b0e0e75f07ca0ebad548f19060`, rende esplicita la verifica degli hint FITS `signed-is-physical` e `normalize` e della rappresentazione XISF Float32 in uscita con `no-compress-data` e `no-embedded-data`. Il controllo della trasformazione dei campioni precede la comparazione numerica. La v1 resta conservata. Nessuna prova nativa registrata.


La rilettura indipendente ImageCalibration è implementata in `read-imagecalibration-xisf.py`, SHA-256 `e9963347bd71ca25b875596ca9f84513ea64cbf585f4936619954846449e1dda`. Su fixture sintetiche, tre rapporti attesi sono accettati, un caso con regioni scambiate è fuori soglia, e cinque file troncati o con formato o campioni inammissibili vengono respinti. Il lettore calcola impronte, mediane e scarti su XISF Gray Float32 non compresso a 64×64; il responso riguarda solo il rapporto tra regioni. Il controllo della scala in ingresso, dei parametri e dei livelli assoluti resta indipendente. Nessuna misura nativa registrata.


### Doppia soglia di memoria per il subject BKL-046 a 34 sorgenti

La specifica di formato e conoscenza, riletta sul commit `e47e224353748f6e8da84e05550ba4afd5dc1eca` della PR #627, fissa due requisiti simultanei: almeno 8 GiB di memoria fisica disponibile e 12 GiB di commit disponibile. I punti di campionamento sono quattro: prima del custode, dopo l’ammissione prima del claim della sessione, dopo il controllo di sorgenti e input e immediatamente prima della creazione nativa. Rimangono i controlli sull’handle originale e la soglia di 4 GiB di private commit. Il limite totale di RAM della VM misurato è 5,999 GiB, quindi la soglia fisica è attualmente irraggiungibile anche aumentando il solo commit. Con il carico misurato (3,503 GiB di RAM in uso) la soglia fisica richiederebbe almeno 11,503 GiB di RAM totale a parità di carico, oltre al limite di commit già calcolato di 16,591 GiB. I valori sono limiti inferiori basati sul campione, non dimensionamento e non garanzia dei quattro preflight. [Specifica sul commit verificato](https://github.com/maininimassimo-bit/digital-stargate-manual/blob/e47e224353748f6e8da84e05550ba4afd5dc1eca/docs/developer/pixinsight-study-knowledge-format.md)


### Perimetro della campagna e baseline registrata

La specifica della PR #627, letta al commit `e47e224353748f6e8da84e05550ba4afd5dc1eca`, distingue il registro autorevole v600 e la conoscenza v1.171 dai supplementi provvisori. Il rendiconto locale estratto da v599 e le fixture CometAlignment/ImageCalibration devono essere riconciliati con le righe effettivamente pubblicate in v600 prima di qualsiasi proposta di chiusura. La campagna Drizzle conserva i due banchi da 196 e 260 casi nativi aperti. Il corpus storico di 64 casi di sviluppo e i 580 scostamenti relativi restano evidenze con esiti noti e non aggiungono unità all’insieme confermativo. Le sette famiglie, i 25 assi, i 19 criteri Owner, la conferma IA e il trasferimento integrale restano nel perimetro. Sul commit i sette workflow di PR risultano completati con esito positivo; sono controlli del repository. [Specifica BKL-046 sul commit verificato](https://github.com/maininimassimo-bit/digital-stargate-manual/blob/e47e224353748f6e8da84e05550ba4afd5dc1eca/docs/developer/pixinsight-study-knowledge-format.md)


### Perimetro Drizzle e contabilità del piano rumore

La specifica BKL-046 sul commit `e47e224353748f6e8da84e05550ba4afd5dc1eca` distingue il pilota tecnico a 520 casi dai 131.072 campi della campagna prospettica. Nel pilota sono già registrati 64 casi di sviluppo: 196 casi residui del banco 00 più 260 del banco 01 danno 456. È stata verificata la contabilità del modello: 2.912 endpoint (2.632 estimandi supportati e 280 record senza stima) per 64 riquadri tecnici danno 186.368 riferimenti, pari a 168.448 supportati più 17.920 senza stima. Per 131.072 campi sono previsti 381.681.664 stati scalari, che includono gli stati senza stima. Sono conteggi di piano e verifica offline. I campi senza supporto e gli audit falliti vanno conservati; l’unione operativa richiede le ricevute autentiche di chiusura, uscita, analisi e rilascio di entrambi i banchi. Nessun nuovo caso nativo o chiusura scientifica.


### Rilettura del criterio confermativo IA H107

Verificato in aritmetica intera il disegno storico a quota fissata sul commit `e47e224353748f6e8da84e05550ba4afd5dc1eca`. Per 70 confronti, livello per confronto 1/1400 e soglia 1%, le quote minime con 0, 1 e 2 eventi combinati sono rispettivamente 721, 957 e 1.159 unità indipendenti; limiti superiori arrotondati 9.998, 9.993 e 9.993 ppm. Verificato il fallimento dei confini con una unità o un ppm in meno. La ricorrenza esatta riproduce il controesempio per scelta adattiva: probabilità per confronto 0,0015801014 e 10,47878734% per 70 copie indipendenti. Restano da congelare dominio, bracci, unità realmente indipendenti e giudizio in cieco; nessuna quota scelta per una nuova prova, nessuna chiamata API e nessuna nuova unità confermativa. [Specifica H107](https://github.com/maininimassimo-bit/digital-stargate-manual/blob/e47e224353748f6e8da84e05550ba4afd5dc1eca/docs/developer/pixinsight-study-knowledge-format.md#h107-criterio-ia-all1-e-uso-corretto-delle-quote-storiche)


### Diagnosi precisa dell’inventario CIM

Su DSG-Shared la query al namespace `root/cimv2` per il solo processo PixInsight, eseguita con Windows PowerShell non interattivo come nel coordinatore, restituisce `NativeErrorCode=AccessDenied`. Anche la query di controllo `Win32_OperatingSystem` restituisce `AccessDenied`. Il rifiuto si manifesta quindi anche al di fuori della ricerca del processo PixInsight. Dal contesto corrente il servizio `Winmgmt` non è visibile via `Get-Service` e la relativa chiave di registro non è leggibile; questi esiti non attestano che il servizio sia assente o fermo sull’host. Servono l’accesso CIM nel contesto operativo del coordinatore e la configurazione canonica R4. Nessuna modifica a servizi, gate o file di progetto.


Il test R4 tra interpreti Python Windows distinti ha verificato l’esclusione effettiva sulla stessa directory privata. Con il lock sintetico BKL-046 detenuto, il processo BKL-051 riceve `HOST_BUSY_OR_LOCK_UNAVAILABLE` prima dello scanner e `active.json` rimane identico. Dopo il rilascio simulato, un nuovo processo BKL-051 acquisisce e rilascia la prenotazione nella stessa directory; le due ricevute corrispondono alle rispettive milestone. Il codice del coordinatore coincide con l’impronta R4. Stato, scanner ed esiti dei parent sono sintetici, il lock Windows è reale nella sola directory temporanea. Nessuna ammissione operativa o esecuzione PixInsight.


La regressione R4 su stato sintetico ha fatto terminare realmente il primo processo di prova con codice 17, subito dopo il claim e senza rilascio. Il secondo processo ha restituito `UNRESOLVED_PREVIOUS_RESERVATION_NO_AUTOMATIC_RECOVERY` prima dell’inventario. `active.json` e la ricevuta di acquisizione sono rimasti identici byte per byte; nessuna ricevuta di rilascio è comparsa. Il test conferma che la morte del custode non sblocca R4. Il codice coincide con l’impronta R4 e tutte le scritture sono rimaste nella directory di test temporanea. Non attesta la storia o il recupero della prenotazione BKL-046 reale.


### Ricerca dell’originale R4 nel deposito Git K

L’Owner ha autorizzato la lettura di `DSG-K-GitStore$`. Dopo attivazione tecnica della sola lettura per il turno, interrogato il bare Git attraverso l’UNC. In `git cat-file --batch-all-objects` non risulta alcun blob della dimensione attesa per il `CURRENT.json` approvato (1.426 byte). In `git rev-list --all --objects` non risultano percorsi del coordinatore, `CURRENT.json` o della prenotazione storica. Il deposito Git non ha fornito la fonte operativa. Sul percorso canonico di DSG-Shared `CURRENT.json` e lo stato risultano ancora indisponibili; l’inventario CIM eseguito con Windows PowerShell restituisce `AccessDenied`. Nessuna modifica al repository locale, al gate o alla prenotazione. L’accesso al deposito è stato confermato solo per il turno.


Ricerca per impronta circoscritta alle copie locali DSG-Shared: riletti 103 file e 128 membri in 29 ZIP (inclusi ZIP annidati entro 20 MiB). Candidati: JSON fino a 256 KiB e file da 1.426 byte. Nessuna corrispondenza per `CURRENT.json` R4 e per lo SHA-256 storico di active/acquired `c1cb401dada7cf6407767636e6b9e3d8c5a728c67af1e8a70bbb59e8d254c144`. I riferimenti per hash restano separati dai byte originali e dallo stato attuale. Nessuna scrittura sui dati esaminati.
