# BKL-051 — riletture dei sorgenti con concorrenza limitata

## Problema e modifica

La prova locale `7944807ee340461ba7769db803334946` ha superato il budget originale durante l'avvio e ha registrato un errore di sintassi PJSR. La correzione della sintassi è separata da questo incremento. Le misure dei controlli Python hanno inoltre identificato il costo delle numerose riletture integrali dei sorgenti; nessuna misura di questo documento dimostra che un nuovo avvio nativo terminerà entro 180 secondi.

`VerifiedSources.assert_intact` rilegge ora sorgenti diversi con un executor locale di massimo quattro thread. Costruzione del loader, importazione e compilazione restano sequenziali. Il corpo di `_read` rimane invariato: per ogni file conserva tutti gli `lstat` ordinati sul file e sui suoi antenati, rifiuto degli alias, apertura, due `fstat`, lettura limitata, controllo del percorso corrente, identità originale, confronto integrale dei byte e SHA-256. Non vengono sostituiti controlli con API Windows, cache o campionamenti.

Prima della scansione sono verificati finder e moduli caricati; vengono acquisiti i riferimenti originali e le righe immutabili delle mappe dei sorgenti, delle identità e dei moduli. Dopo il completamento di tutti i worker vengono ricontrollati riferimenti, contenuti e identità dei moduli prima di restituire successo. Il worker usa esclusivamente la riga acquisita prima delle letture.

## Errori, memoria e durata

Ogni invocazione crea e chiude il proprio executor. Nessun executor, future o risultato viene memorizzato nel loader. Il context manager attende i worker avviati anche quando falliscono sottomissione o recupero dei risultati. Una lettura bloccata può quindi ritardare l'uscita: non è un timeout rigido. I controlli esterni del budget originale restano necessari dopo il ritorno; non vengono introdotti rinnovi, nuovi avvii o chiusure di processi.

Gli errori delle letture vengono ridotti nel worker a descrittori immutabili limitati, senza traceback o nuovi buffer. Il chiamante ricostruisce `VerificationError`, la famiglia `OSError` con errno pertinente e le interruzioni previste. In presenza di più errori viene propagato il primo nell'ordine del manifest, dopo la conclusione di tutti i worker. Testi diagnostici oltre 1024 caratteri vengono omessi; non partecipano all'autorità di verifica. Gli errori inattesi rifiutano il controllo.

Oltre ai buffer originali conservati, limitati complessivamente a 16 MiB, possono esistere al massimo quattro letture attive di `MAX_SOURCE + 1` byte: 4 MiB più quattro byte di rilevamento dell'eccesso, esclusi gli overhead ordinari di Python e hashing. Al massimo 128 job condividono riferimenti ai buffer originali; gli esiti non contengono buffer appena letti. La rimozione dei traceback evita che i future completati trattengano un ulteriore buffer per ogni errore.

## Confine di validità

L'ordine temporale delle osservazioni tra file diversi cambia. Non si dichiara equivalenza per ogni modifica concorrente coordinata nel tempo: né la versione sequenziale né questa versione costituiscono uno snapshot atomico di tutti i file. Restano necessari il confine privato e quiescente e le verifiche originali di ogni singolo file. Le cinque snapshot del bootstrap e il numero dei controlli ai confini delle risorse non vengono ridotti.

La classificazione del design indipendente è `APPROVED_DIRECTION_WITH_REQUIRED_IMPLEMENTATION_PROOFS`, non approvazione del codice né autorizzazione operativa. Il codice richiede CI sull'exact HEAD, poi ARB e Release Quality indipendenti, in quest'ordine.

## Verifica

Le prove dedicate usano esclusivamente sorgenti inventati in directory temporanee: 22 e 128 sorgenti riletti, limite di quattro worker, osservazioni ordinate sugli antenati, errori deterministici, cambiamenti delle mappe e dei moduli durante le letture, interruzione della sottomissione, assenza di thread superstiti e mancata conservazione dei buffer dei worker falliti. Le regressioni del loader e del bootstrap verificano inoltre importazioni, sostituzioni, byte originari e rifiuto degli accessi non dichiarati.

La tornata locale dedicata esegue 51 test con esito positivo. Include un'interruzione durante il recupero dei risultati, una lettura corta con stream chiuso e il vero `LiveNativeBudget` caricato insieme ai suoi moduli interi: se l'ultima lettura porta il clock sintetico al termine originale, il controllo successivo rifiuta l'operazione senza spostare origine o scadenza.

Cinque misure locali del bootstrap intero, con le cinque snapshot e creazione/chiusura dei thread incluse, hanno prodotto 19–21 ms con il nuovo loader. Una nuova tornata della versione sequenziale ha prodotto 33–36 ms. Percorsi dei fixture, dimensione del loader, carico del sistema e cache possono influenzare il confronto: non è un benchmark controllato dell'intero tentativo. I 22 moduli di produzione e il modulo diagnostico sono conservati interi; nessun metodo è estratto o sostituito nella misura del bootstrap.

Il profilo completo dei 22 moduli di produzione viene eseguito separatamente con test sintetici della supervisione. Non usa un consenso operativo e non prepara né avvia PixInsight. Queste prove non qualificano controlli nulli reali, non validano il modello fisico dell'incertezza e non completano R01–R14. La milestone resta `OPEN / NOT_VALIDATED`, con zero nuovi controlli scientifici qualificati.

Rollback: ripristinare il solo incremento dei sorgenti con un commit ordinario, conservando prove e registri. Nessuna cancellazione o modifica cloud è necessaria.
