# BKL-051 — preparazione locale dei derivati nel portale

Stato: incremento candidato di sola lettura. BKL-051 **OPEN / NOT_VALIDATED**, 37% indicativo, zero controlli scientifici qualificati.

## Dal piano alla preparazione

Il piano diagnostico RAW precedente conserva i propri tentativi. Le copie calibrate sperimentali richiedono regole compatibili e una nuova versione preliminare: non si trasferiscono tacitamente i completamenti RAW. Il produttore `tools/scientific_transients/derived_preparation.py` esporta una ricevuta minimizzata `BKL051_DERIVED_PREPARATION_V1` per un solo caso con tre frame distinti.

Il produttore riusa il piano congelato, gli operatori preparati, il registro locale e il preflight dei derivati. Richiede un head atteso, tre associazioni esplicite, operatori senza job selezionato, run non avviati e otto corrispondenze locali valide per ciascun input. Rilegge le evidenze e l'head prima dell'esportazione; input alterati, parziali, duplicati, avviati, selezionati o riferiti a regole diverse impediscono una ricevuta di preparazione riuscita. Non offre trasporto, credenziali, avvio o discovery delle cartelle.

La ricevuta contiene tre preflight esistenti, senza percorsi privati, identità worker, segreti o immagini. I conteggi zero riguardano la preparazione e il caso selezionato della versione esatta: non affermano che non esistano altri tentativi o job nella cronologia del progetto. I file restano modificabili sul PC: il ricontrollo puntuale non è una garanzia di immutabilità futura.

## Consultazione nel portale

La sezione «Preparazione locale delle copie calibrate» confronta tre JSON: versione del piano, provenienza delle copie e ricevuta di preparazione. Ogni file è limitato a 1 MiB, letto soltanto in memoria, senza invio o conservazione. Ogni sostituzione o errore invalida il risultato combinato precedente; letture tardive o pagine rimosse non ripristinano risultati obsoleti.

I validatori esistenti del piano e della provenienza vengono riutilizzati. Sono richiesti stessa versione, cronologia, caso, famiglia del piano e impronte delle ricevute; originali e derivati devono coincidere con le coppie dichiarate nella provenienza. Schemi, tipi, tre identità distinte, otto flag letterali e quattro blocchi sono controllati rigorosamente; campi aggiuntivi e promozioni di autorità vengono rifiutati.

Il produttore verifica i record dei frame nel piano privato. La vista minimizzata del piano non include quei record: il browser confronta le dichiarazioni importate e non rilegge operatori, immagini o prove native. La frase «secondo la ricevuta locale» distingue questa consultazione da un'attestazione di byte, autore, tempi o verità scientifica.

## Preparato non significa eseguito

La vista mostra tre copie preparate secondo la ricevuta e zero job selezionati, avvii nativi, tentativi e controlli qualificati per quel caso. Gli otto controlli non rimuovono i quattro blocchi: archivio del nuovo tentativo mancante, calibrazione scientifica non validata, incertezza completa mancante e attestazioni confermative mancanti. Il preflight resta `BLOCKED`; nessun pulsante avvia, registra, ritenta o invia analisi.

Il punto geometrico diagnostico non è un'associazione fisica di sorgente. Restano aperti dark 2024 e stabilità temporale, camera nominale, covarianze, tempi, astrometria completa, riferimenti nulli e indipendenza. Incertezza completa e significatività restano sconosciute. Tre completamenti tecnici futuri non qualificheranno da soli un controllo.

## Prove e rilascio

Le prove sintetiche usano le API locali effettive con file fittizi, engine e catalogo fittizi, senza eseguire PixInsight. Il consumatore JavaScript riceve la fixture generata dal produttore Python, così i due contratti vengono provati insieme. Controprove includono frame/regole/versioni/provenienze incompatibili, sorgenti diventate obsolete durante l'esportazione, job già selezionati, run avviati, flag falsi, autorità improprie, limiti, invalidazione asincrona e navigazione istantanea.

L'interoperabilità dei tre input reali è verificata separatamente in privato; nessun relativo file viene pubblicato come fixture. Suite complete, rendering reale, ARB poi RQ, CI sul commit esatto, merge, controlli postmerge, Pages e identità degli asset sono gate distinti. Questo documento descrive il contratto candidato, non sostituisce le ricevute finali del rilascio.

Rollback tramite revert del package, conservando ogni versione, preparazione, tentativo e ricevuta. Nessuna cancellazione, migrazione o replay. Nessuna build o attivazione cloud, modifica IAM, risorsa, spesa, query IRSA, pubblicazione di fotografie o invio astronomico è autorizzato. Le precedenti prove cloud restano concluse e ripristinate; un nuovo perimetro esecutivo richiede proposta e consenso separati.
