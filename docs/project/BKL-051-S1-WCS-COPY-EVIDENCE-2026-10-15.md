# BKL-051 — evidenza del trasferimento WCS candidato

Stato: correzione candidata del verificatore locale; rilascio da verificare sul
commit esatto. Milestone **OPEN / NOT_VALIDATED**, stima indicativa 37%, zero
controlli scientifici qualificati.

## Problema e correzione

Un precedente script nativo trattava il `Point` restituito da
`imageToCelestial` come un array. Confrontare due proprietà mancanti poteva
produrre un'uguaglianza apparente e serializzare coordinate come oggetti vuoti.
Lo stato terminale di successo e la conservazione dei pixel non dimostrano
l'equivalenza delle coordinate.

Il verificatore locale ora richiede tre confronti conservati: centro e due
angoli opposti nella convenzione geometrica nativa. Ogni confronto deve
contenere coppie numeriche finite, coordinate celesti nell'intervallo previsto
e uguaglianza esatta fra riferimento e copia riaperta. Coordinate mancanti,
oggetti vuoti, booleani, valori non finiti, punti duplicati o errati e
coordinate differenti impediscono l'esportazione del contesto. Il formato
minimizzato del portale resta invariato; le ricevute storiche incomplete
restano conservate e richiedono una nuova prova distinta, senza correzioni
retroattive o riesecuzione automatica.

È una verifica della dichiarazione nativa conservata, non un nuovo calcolo WCS
nel verificatore Python né una prova dell'accuratezza astrometrica sul cielo.

## Evidenza privata reale precedente al candidato

Tre RAW della tripletta diagnostica hanno ricevuto soluzioni candidate usando
esclusivamente una risposta Gaia DR3 già conservata. Tre nuove copie calibrate
sperimentali hanno poi ricevuto il WCS del rispettivo RAW: tutti i 17.832.960
pixel Float64 sono identici ai genitori e nove coppie di coordinate native
finite coincidono dopo la riapertura. Le tre ricevute minimizzate sono state
lette nel portale pubblicato. Revisioni indipendenti ARB e poi RQ approvate nel
solo perimetro tecnico; file, percorsi e coordinate restano privati.

Un primo trasferimento si è fermato al controllo delle coordinate; i successivi
due avvii di quel batch non sono avvenuti. Il fallimento è conservato e la prova
corretta appartiene a un nuovo ramo. Nessun processo isolato di queste prove
resta attivo. Nessun nuovo job cloud, richiesta di catalogo o tentativo nel piano
è derivato da tali copie; i tre tentativi RAW precedenti non sono stati
riassegnati ai derivati.

Queste evidenze non attestano il rilascio della correzione descritta sopra.
Il suo gate richiede regressioni, ripetizione in sola lettura sui file reali,
CI e review indipendenti sul commit esatto.

## Limiti scientifici e operativi

- WCS candidate, residui descrittivi e covarianza completa sconosciuta.
- DATE-AVG dichiarato circa 2,95–2,98 secondi prima del punto medio nominale;
  DATE-OBS delle copie arrotondato a millisecondi. Nessuna correzione di clock
  o shutter dedotta e nessuna accuratezza temporale attestata.
- Calibrazione sperimentale con dark 2024 scelti dall'Owner; stabilità temporale
  e contributi completi del rumore restano da quantificare.
- Nessuna qualificazione indipendente, esito scientifico, acceptance o invio
  astronomico. Tre immagini non equivalgono a 59 controlli indipendenti.
- Le prove cloud precedenti sono concluse e ripristinate; questo package non
  autorizza build cloud, deploy del servizio, IAM, job, spese o query IRSA.

R02/R05 avanzano nell'integrità e nella lettura delle evidenze; non sono chiusi
nel loro perimetro scientifico completo. Restano aperti gli altri requisiti
della [procedura BKL-051](BKL-051-SCIENTIFIC-TRANSIENT-CANDIDATES-2026-10-07.md).
Rollback: revert del verificatore e della relativa documentazione; conservare
sempre originali, tentativi falliti e ricevute, senza promuovere quelle incomplete.
