# BKL-051 — quarta OAT, recovery e ricevuta Owner

BKL-051 resta OPEN. Incremento documentale candidato ai gate; nessuna accettazione scientifica o operativa implicita. PR #524 precedente verificata sul merge `a8c60017cad6e6cb8431b671d24910f2d5e85d8e`: CI exact-head, ARB poi RQ senza finding, 15 workflow post-merge SUCCESS e sette endpoint Pages. Il presente incremento non è attestato da quelle ricevute.

## Sessione autorizzata e risultati reali

Quarta sessione singola autorizzata dall’Owner: massimo 60 minuti, fino a tre nuovi job sintetici e tre avvii PixInsight isolati. Durata reale 930,74 secondi; 79 richieste worker e 26 operazioni applicative Owner entro il limite di 30, più 26 preflight OPTIONS HTTP 204. Stesso servizio, immagine verificata e permesso condizionale sul solo oggetto di controllo; nessuna build o nuovo account. Fixture monocromatiche 64×64 Float64; nessuna fotografia dell’Owner. Parametri, piani, binding, journal/outbox e archivi completi restano privati.

| Caso | Osservazione | Limite |
|---|---|---|
| OWNER_CANCEL | Il job completa prima che la richiesta Owner di annullamento arrivi; UI rifiuta attribuzione della cancellazione a un lavoro terminale | Annullamento durante il nativo NON superato; nessun rilancio |
| NATIVE_RECOVERY | Iniezione locale di mancata osservazione dopo `started.json`; terminale nativo COMPLETED già presente. Supervisore conserva RECOVERY_REQUIRED, chiude solo handle proprio dopo evidenze, processo assente verificato. Owner consulta dossier e registra personalmente dichiarazione legata al digest | Non interruzione naturale della rete né fault durante misure; job resta RECOVERY_REQUIRED, senza reset/replay |
| TERMINAL_LOST_ACK | Una POST COMPLETED reale riceve risposta valida poi scartata localmente prima dell’ACK su disco. Riapertura esplicita e GET autenticata riconciliano identica ricevuta, senza seconda POST o nativo | Iniezione controllata locale dopo successo HTTP; non perdita naturale del socket cloud |

Tre terminali nativi COMPLETED verificati con collector rilasciato; 1024/1024/2 righe, zero pixel modificati, checkpoint/History e manifest conservati. Tutti e tre i processi dedicati fermi. Queste misure normalizzate non hanno full variance/significatività: restano NOT_VALIDATED. Dipendenze installate e archivi genitori esterni: non archivio autonomo completo. Il primo dossier recovery privo di manifest, dovuto a errore dello script di audit, è conservato e superato dalla versione v2 verificata; solo il digest v2 è stato dichiarato dall’Owner.

Owner registra personalmente KEEP_FOR_REVIEW sul terzo rapporto e scarica ricevuta minimizzata. Primo tentativo di download non percepito dall’utente; prova assistita nel browser integrato osserva evento download e file reale, senza ricorrere al browser esterno. Ricevuta aggiornata con revisione confrontata indipendentemente con rapporto locale e stato cloud; corrispondenza verificata. Non è esportazione del rapporto scientifico completo e non conferma una scoperta.

Pagina preesistente caricava controlli precedenti; ricaricamento porta controlli recovery aggiornati, con nuovo login Google personale. Conservare questa osservazione di aggiornamento/caching; non implica collaudo generale cross-browser o regressioni finali.

## Concorrenza GCS isolata

Probe separato sull’archivio esistente: creazione esclusiva di un oggetto diagnostico isolato, poi due scritture concorrenti con stessa generazione attesa. Una riesce; la seconda fallisce con precondizione HTTP 412. Generazione finale e payload coincidono con il vincitore. Oggetto e manifest conservati, nessuna cancellazione. Stato primario dei job invariato durante il probe; nessuna nuova credenziale/IAM o attivazione del servizio. Prova la primitiva CAS reale della storage, non retry concorrente dell’intero servizio o recovery del backup.

## Ripristino e conservazione

Controller concluso. Verifica finale indipendente PASS: P6 traffico 100%, variabili transient assenti nella configurazione corrente, esatto permesso condizionale temporaneo assente; tre handle dedicati fermi. Stato cloud preserva job storici, recovery dichiarata e revisione esatta; ricevuta scaricata coerente. Stato primario cambia legittimamente per nuovi binding/job/revisione, non si dichiara invariato. Revisioni storiche conservate; non si dichiara cancellazione delle loro configurazioni. Credenziale temporanea mantenuta solo in memoria per la sessione. Tutte le quattro autorizzazioni OAT sono consumate.

## Residui obbligatori

| Area | Evidenza acquisita | Residuo |
|---|---|---|
| Accessi | Google Owner e secondo account reale | Regressioni finali e S5 |
| Cancellazione | Prima dell’avvio cloud e punto sicuro nativo locale; rifiuto su lavoro già terminale | Owner → cloud → supervisore → nativo mentre esegue |
| Recovery | Fault locale dopo terminale, quiescenza e dichiarazione Owner reale | Fault e conservazione prima del terminale, nessuna attribuzione automatica |
| ACK | Socket loopback reale; risposta cloud valida scartata localmente e GET senza replay | Limiti delle iniezioni espliciti; eventuali ulteriori prove richieste dal piano |
| Persistenza | Backup verificato, conflitto di generazione GCS isolato | Concorrenza/retry del servizio e conservazione sotto conflitto |
| Review/export | Decisione Owner reale e file scaricato confrontato con cloud/report | Rapporto scientifico completo e regressioni/accettazione |
| Scienza | Diagnostica pubblica V5/V6 e misure native tecniche | Calibrazione, full variance/covarianze, timing/proper motion, fotometria multi-epoca, campione cieco/completezza/falsi positivi, policy approvata |
| Segnalazioni | Scope CBAT/TNS/VSX/MPC approvato e draft locale | Adattatori, tracklet, payload immutabile approvato, revoche/duplicati/ricevute e collaudo previsto |

S1/S2 aperte, S3 parziale, S4 incompleta, S5 non accettata. P6/F4/F5/BKL-050 e S10/Safety/C→F invariati. Nessun invio esterno autorizzato. Rollback documentale: revert governato e rigenerazione projection, conservando evidenze private. Non arresta processi o resetta job. CI → ARB → RQ → merge sul commit atteso → verifica post-merge e Pages.
