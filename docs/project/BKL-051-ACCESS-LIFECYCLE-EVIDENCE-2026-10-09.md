# BKL-051 — accessi Google e ciclo nativo, 9 ottobre 2026

BKL-051 resta OPEN. Incremento candidato ai gate; nessuna accettazione operativa o scientifica implicita. La precedente PR #523 è stata unita sul merge `4f8d3e913edd773d4a0344e151f72b1ca1ee127d`: 13 controlli applicabili exact-head, ARB poi RQ APPROVED senza finding, 14 workflow post-merge SUCCESS e sette endpoint pubblicati verificati. Queste ricevute non provano il rilascio del presente incremento.

## Accessi reali Google

Terza sessione singola autorizzata e conclusa in 443,54 secondi. Dopo rinnovo personale del login, Owner: GET options/jobs HTTP 200 e lettura delle schede private. Secondo account scelto personalmente dall’utente: GET options HTTP 403, messaggio di rifiuto, zero schede private e richiesta disabilitata. Identità del secondo account confermata dall’utente; nessun token decodificato o credenziale Google estratta. La risposta iniziale 403 della sessione Owner scaduta resta separata dal risultato non-Owner.

Cinque GET e cinque OPTIONS osservate, nessun POST applicativo, nuovo job o avvio nativo. Verifica indipendente finale PASS: traffico P6 100%, variabili transient assenti nella configurazione corrente, permesso condizionale temporaneo assente e generazione dello stato invariata. Le revisioni storiche sono conservate. Immagini, identità, percorsi e ricevute complete restano privati.

## Cancellazione durante esecuzione PixInsight

Nuova prova locale su copia della fixture sintetica monocromatica 64×64 Float64; 1024 posizioni di misura, senza fotografie dell’Owner. Codice nativo rilasciato invariato. Dopo osservazione della prima misura e handle proprio ancora attivo, marker di cancellazione esatto. PixInsight ha prodotto terminale CANCELLED dopo dieci misure, checkpoint e History iniziale/corrente conservati prima della chiusura dell’handle.

Verifica indipendente: tutti i 4096 campioni del checkpoint sono identici bit per bit all’input; input genitore invariato. Ricevute, script, parametri, log e manifest SHA256 conservati; dipendenze installate e archivio genitore esterni, non archivio autonomo completo. Il processo isolato è fermo. Nessuna chiusura di altre istanze PixInsight. La prova verifica il punto sicuro nativo; non verifica pulsante Owner, trasporto cloud o supervisore completo con cancellazione remota.

## Perdita effettiva della risposta su socket locale

Due nuove prove della suite receipt coordinator usano il vero adapter HTTP e il trasporto dedicato su loopback, con storage MemoryStore e journal sintetici. Il server interrompe effettivamente la connessione TCP, anziché simulare soltanto un’eccezione nel client.

- Dopo commit: una sola POST report, risposta perduta, nessun ACK locale iniziale. Riapertura esplicita dell’outbox e GET autenticata confermano identica ricevuta; ACK conservato senza seconda POST. Envelope originale invariato.
- Prima del commit: una sola POST report consumata senza scrittura, risposta perduta; GET trova sequence zero e nessuna ricevuta. Riapertura congela in RECONCILIATION_REQUIRED, conserva envelope e recovery, senza ACK, seconda POST o nuova operazione.

Suite locale: 21/21 PASS. Si tratta di regressioni tecniche con socket reale e storage sintetico; non costituiscono lost-ACK del servizio cloud, CAS GCS, autenticazione Google o misura scientifica. Il comportamento produttivo e il contratto non cambiano.

## Diagnostica pubblica V6

Nuovo ramo rispetto a V5: sola sensitivity StarDetector da 0,5 a 0,8, resto invariato; parametri diagnostici, non soglia operativa. Tre esposizioni pubbliche ZTF del controllo Atami: 1033/439/1354 sorgenti; audit indipendente dei pixel e delle maschere senza discrepanze, originali invariati. Convenzione StarDetector SAMPLE_INDEX_ZERO coerente con contratto S2 già rilasciato; conversione Astropy origin zero senza offset.

Distanze delle sorgenti più vicine alle posizioni note: 0,136835 / 15,000433 / 0,167632 arcsec. Prima e terza recuperate diagnosticamente; seconda non recuperata. Le distanze non sono associazioni accettate: timing, covarianze, completezza, falsi positivi e politica di selezione restano da validare. Campione preselezionato e non cieco; nessun tracklet MPC pronto.

## Matrice residua di chiusura

| Area | Evidenza acquisita | Gate ancora aperto |
|---|---|---|
| Accessi | Google Owner e secondo account reale | Regressioni finali e accettazione S5 |
| Cancellazione | Prima dell’avvio cloud; punto sicuro nativo locale | Percorso Owner → cloud → supervisore → nativo durante il job |
| ACK | ACK storico cloud; perdita socket locale prima/dopo commit | Perdita controllata reale nel percorso cloud e riconciliazione |
| Persistenza | Backup cloud verificato uguale ai byte primari | Conflitto CAS GCS realmente osservato e conservazione |
| Recovery/report | Funzionalità rilasciate e prove sintetiche | Quiescenza reale, dichiarazione Owner e revisione/esportazione effettive |
| Scienza | Diagnostici V5/V6 e cataloghi pubblici | Fotometria multi-epoca compatibile, calibrazione, covarianze/timing, validazione cieca e policy approvata |
| Segnalazioni | Piano CBAT/TNS/VSX/MPC e draft locale | Adattatori, oggetti mobili, payload/revoche/duplicati/ricevute e collaudo previsto |

S1/S2 aperte, S3 parziale, S4 incompleta, S5 non accettata. Nessuna esclusione di requisiti per inferenza. Ulteriori attivazioni cloud richiedono proposta concreta distinta per credenziale temporanea e servizi; le tre precedenti sessioni sono consumate. Invii esterni non autorizzati. P6, F4/F5, BKL-050, S10/Safety e collegamento C→F invariati.

Rollback del presente incremento: revert governato dei test/documenti e rigenerazione delle projection; conservare tutti gli archivi privati. Il revert non arresta processi né cancella evidenze. CI → ARB → RQ → merge sul commit atteso → post-merge e Pages.
