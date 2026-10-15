# Copertura temporale della guida — integrazione del 15 ottobre 2026

## Mandato e metodo versionato

Owner autorizza l’integrazione dai log già importati. Questo incremento sostituisce, solo quando misurabile, il sentinel di copertura F4 con `DSG-GUIDING-LIGHT-TEMPORAL-1.0`. Il precedente handover di presentazione resta uno snapshot storico. Il catalogo passa da 1.5 a **1.6**, aggiungendo `guiding.temporalCoverage`; i consumer con verifica esplicita accettano entrambe le versioni. Nessun RAW o report storico viene riscritto.

## Denominatore e numeratore

Denominatore: unione degli intervalli LIGHT identificati da `SequenceItem TakeExposure ImageType LIGHT`, inizio effettivo `CameraVM Capture Starting Exposure`, durata dichiarata e corrispondente fine dell’istruzione. Non include download, plate solving, BIAS, DARK, FLAT, intervalli fra pose o l’intera notte. Un avvio senza fine, più Capture nella stessa istruzione, tempi non validi o conteggio diverso da `lightStarted` rendono indisponibile l’intera misura. Il metodo iniziale è deliberatamente conservativo rispetto a retry e log storici incompleti.

Numeratore: intersezione del denominatore con l’unione dei tratti tra campioni PHD2 consecutivi validi (`Mount`, `ErrorCode=0`, valori numerici finiti), fuori da settling e pause. I campioni sono ancorati a `Guiding Begins at` più `Time` in secondi. Non si collega un segmento al successivo né si estrapolano code. Distanza massima fra campioni: **tre durate configurate della camera di guida**, aggiornate anche dai cambi di parametro. È una convenzione versionata di ricostruzione della continuità, non una soglia di bontà scientifica. Errori, assestamenti e pause interrompono la continuità.

Copertura = secondi coperti / secondi LIGHT. Intervalli sovrapposti o GuideLog duplicati non raddoppiano il tempo. Uno zero è pubblicabile se ci sono intervalli LIGHT e guida validi ma senza sovrapposizione; non significa assenza di dati o prova di mancato funzionamento della guida. In assenza di evidenza resta `UNAVAILABLE`, `coverage:null`, con reason code.

## Orologi e provenienza

La misura usa **lo stesso orologio locale**, senza attribuire falsamente UTC ai log privi di offset. Richiede una connessione N.I.N.A. a PHD2 `127.0.0.1`/`localhost` in ciascun log N.I.N.A. importato; host remoto o non attestato resta indisponibile. Regressioni dei timestamp N.I.N.A., degli anchor PHD2 o del tempo relativo rendono la misura indisponibile, anche nei casi di ritorno dell’ora. Non attesta sincronizzazione NTP o precisione assoluta degli orologi. Date duplicate e cambi di clock restano un limite dei log senza offset: non correggerli per inferenza. Il contratto futuro con timestamp UTC espliciti consentirà eliminare questa ambiguità.

Ogni risultato espone versione, clock basis, massimo gap, secondi totali/coperti e riferimenti ai log con SHA-256 dei byte originali. Un roundtrip UTF-8 non identico rende la misura indisponibile. F4 accetta il valore solo con metodo, clock basis, gap, finitezza, limiti e rapporto numeratore/denominatore coerenti.

## Automazione e consumer

Il generatore canonico del catalogo ricostruisce il risultato direttamente dai RAW ogni volta che gira, incluso il job automatico dopo l’importazione. F4 usa la copertura misurata; mantiene il sentinel interno zero nei casi indisponibili. Il consumer distingue zero misurato e sentinel usando il riferimento esplicito a `guiding/temporalCoverage`, senza confondere gli stati nella stessa cohort. Mostra percentuale, secondi e metodo; le lacune mantengono una spiegazione.

Scoring/profile/pesi e RMS non cambiano. **Confidence e copertura aggregata possono aumentare** perché ora sostenute da copertura temporale misurata. F5 si rigenera sulla cohort intera e resta NOT_READY_FOR_PRODUCTION: nessuna calibrazione produttiva, acceptance scientifica, nuova autorità, Safety o azione dispositivi. Anche i record con assessment fuori profilo possono esporre la misura grezza.

## Audit, validazione e rollback

[Evidenza riproducibile di tutte le sessioni](evidence/guiding-temporal-integration-audit-2026-10-15.json). La presenza dei timestamp rilevata nell’audit preliminare non garantisce che le coppie siano complete, ordinate e sul medesimo clock: per questo la misura finale è disponibile solo dove supera tutti i controlli.

Test sintetici: mezzanotte, intersezione, esclusione errori/settling/pause, gap lungo, orologio remoto/mancante, LIGHT incomplete, conteggio incoerente, regressione clock/DST, zero misurato, deduplicazione e encoding. Test reale: ricalcolo indipendente dal catalogo dei 58 LIGHT del 14–15 ottobre, con identità dei digest sorgente. Regressioni F3/F4/F5 e consumer, generatori, build strict e browser desktop/mobile. Gate finali: exact-head CI, ARB poi RQ, merge atteso e pubblicazione verificata, da attestare nella PR.

Rollback: revert coordinato di generatori, consumer e proiezioni rigenerate, con CI/review. RAW e pacchetti originali immutabili. Nessuna modifica allo schedulatore EAGLE o necessità di ulteriori caricamenti per le sessioni già misurabili.
