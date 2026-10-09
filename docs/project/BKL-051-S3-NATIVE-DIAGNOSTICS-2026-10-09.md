# BKL-051 S3 — diagnostica nativa Atami, esiti non validati

Stato: evidenza privata successiva alla preparazione pubblicata con PR #521; riconciliazione candidata ai gate. BKL-051 OPEN. Nessuna misura astronomica accettata e nessuna segnalazione.

## Esiti e conservazione

Tre nuove immagini pubbliche ZTF g e relative maschere, selezionate con effemeride nota: non ricerca cieca. PixInsight 1.9.5 build 1706, StarDetector nativo, posizioni previste non passate al rilevatore. History iniziali/correnti e checkpoint conservati; History a monte NOT_ATTESTED. Lettura del rilevatore e maschera costruita manualmente hanno ricevute e script, non una History di processi integralmente riproducibile.

V1 fallisce prima di aprire gli input per controllo della proprietà errata della versione; V2 apre dati e conserva checkpoint, poi rifiuta la maschera floating perché il rilevatore richiede interi a 8 bit. V3 completa il flusso tecnico con maschera a 8 bit, ma restituisce zero sorgenti: esito INVALIDO della diagnostica, non assenza di stelle o asteroidi.

Il controllo in sola lettura dei tre checkpoint raw-mask XISF contro ogni pixel dei FITS originali prova l'offset +32768 introdotto dall'importazione degli interi FITS signed BITPIX=16 senza BZERO. Interpretare tale offset come bit di qualità escludeva tutti i pixel. Dopo sottrazione dell'offset, zero discrepanze con i FITS e zero bit riservati: 65, 54 e 85 pixel con contaminazioni documentate. Il template 6141 e i bit informativi 2050 restano distinti; non eliminare le sorgenti per i soli bit informativi. Questo è un audit numerico dell'importazione, non una policy di accettazione scientifica.

Il segnale scientifico importato coincide pixel per pixel, alla precisione float32, con (FITS_ADU+1000)/1000000: 856851, 858173 e 868968 campioni, zero nonfiniti/clipping e zero pixel modificati dal rilevatore. Tale normalizzazione non produce automaticamente ADU fisici, magnitudini o varianze calibrate. Gli originali conservano le sei SHA256.

## Tentativo non confermato e ripresa

V4 prepara la correzione dell'offset ma il launcher conserva per errore la radice precedente, a causa di separatori Windows non normalizzati. Prima di possibili scritture è conservata una copia completa del genitore: 49 file verificati identici. Lo script avviato errato è conservato separatamente; destinazione dello script corrente corretta dopo il lancio. Il digest registrato prima dell'avvio non attesta i byte realmente eseguiti: questo tentativo non può entrare nelle evidenze valide.

Entro i 240 secondi di osservazione non arriva una ricevuta di esecuzione. Stato UNCONFIRMED_KEEP_EVIDENCE_NO_REPLAY, processo non attestato fermo; nessuna terminazione dal PID ricostruito e nessun retry automatico. V5 è soltanto preparato in cartella nuova: radice normalizzata esatta e sei SHA originali verificate, launchAllowed=false. Richiede verifica reale di V4, provenienza e fermata prima di un nuovo controller con handle proprio e script pinned.

V1/V2 e tutti i rami falliti conservati; non dichiarare fermi processi non attestati né chiudere PixInsight Owner. V3 è attestato terminato dal proprio controller dopo salvataggi e zero finestre aperte. Il confronto parent/bak di 49 file non significa che l'intero workflow scientifico sia validato o che l'archivio delle dipendenze sia standalone.

## Limiti e prossimi passi

Nessuna attivazione cloud, nuova credenziale, IAM, provider submission o pubblicazione fotografica. Il collaudo cloud sintetico è distinto dalla diagnostica pubblica. Prima la verifica locale del tentativo incerto e l'autorizzazione distinta di attivazione/OAT; poi nuove misure correttamente tracciate. Timing delle effemeridi, WCS/covarianze, calibrazione, PSF/confusione, matching, blind completeness/false positives e policy Owner restano aperti. Un oggetto preselected e tre esposizioni in due notti non costituiscono scoperta o dossier MPC pronto. Non chiudere M3/BKL-051 per questi esiti.
