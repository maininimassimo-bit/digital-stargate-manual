---
name: pixinsight-scientific
description: Elabora e confronta immagini astronomiche con PixInsight nativo, preservando master, History, maschere, checkpoint e provenienza scientifica. Usare per workflow LRGB, OSC/CFA, SHO/HOO, mosaici, drizzle e confronti di deconvoluzione o denoise, anche nel progetto Digital StarGate.
---

# PixInsight scientifico

Realizzare elaborazioni native riproducibili, distinguendo resa estetica, integrità tecnica e validazione scientifica. Conservare il segnale acquisito e dichiarare i limiti dei processi basati su modelli. Non creare strutture astronomiche con generatori di immagini, inpainting o pixel prelevati da fotografie di riferimento.

## Prima di elaborare

- Nel progetto Digital StarGate leggere [il contesto e gli handover](references/digital-stargate.md). Verificare milestone aperte e pianificate prima di affermarne la chiusura.
- Leggere [il protocollo nativo](references/native-workflow.md) prima di avviare processi o costruire confronti.
- Per SHO/HOO e SPCC narrowband leggere [calibrazione, presentazione e lezioni SHO](references/narrowband-spcc.md): separare il checkpoint calibrato dalla resa finale e verificare le caratteristiche dei filtri.
- Individuare la versione scelta dall'utente e il checkpoint corretto. Una revisione è un ramo nuovo: non sovrascrivere il risultato approvato.
- Verificare file, SHA256, geometria reale, canali, formato, linearità, filtri, allineamento, eventuali immagini ausiliarie e Bayer. Il nome della cartella non prova che un file sia ancora CFA. Chiedere soltanto i dati mancanti indispensabili.
- Accertare disponibilità e versione di PixInsight, moduli e modelli effettivamente caricati. Per novità o parametri incerti consultare documentazione ufficiale aggiornata; non dedurre la versione del modello da quella del modulo.

## Elaborazione e controllo

Usare PixInsight/PJSR e processi nativi disponibili. Preferire gli script già validati nel progetto, dopo aver letto impostazioni e dipendenze; non eseguire alla cieca script storici che possono consegnare risultati al portale. Parametri di una nebulosa non sono una ricetta universale.

Provare modifiche costose o aggressive su ritagli rappresentativi, poi applicare la ricetta scelta all'intero campo e ricontrollarlo. Separare stelle e nebulosità quando utile, conservando entrambi i rami; proteggere fondo, stelle e nuclei con maschere verificabili. Evitare saturazione dei nuclei, aloni, ringing, neri chiusi e grana amplificata. Non eliminare come gradiente una nebulosità debole senza verificarla sui canali/master.

Per BlurXTerminator ripartire da dati lineari appropriati, prima di denoise e separazione stelle; non sovrapporre deconvoluzioni a una versione già trattata senza una motivazione verificata. Comparare MLDenoise e NoiseXTerminator sul medesimo checkpoint, dichiarando i trattamenti già presenti. La scelta deve conservare filamenti deboli e morfologia stellare, non soltanto abbassare una misura di rumore.

## History e consegna

- Registrare i processi realmente eseguiti, versioni/modelli, parametri, input/output, maschere, ordine e ramificazioni, con ricevute di completamento. Esportare History iniziale/corrente dei checkpoint prima di chiudere le immagini.
- Collegare ogni ramo al suo genitore esatto. Una History esportata dopo un'apertura/clone non contiene necessariamente tutta la provenienza; integrare manifest, script e archivio del genitore senza inventare passaggi mancanti.
- Conservare anche tentativi falliti e prove scartate, etichettati come tali. Il numero di operazioni di tutti i rami non è il numero di passaggi sequenziali del risultato finale.
- Verificare geometria, pixel finiti, clipping, integrità degli originali e apertura dei prodotti. Esportare XISF scientifico e anteprime; TIFF/JPG secondo richiesta, dichiarando profondità e trasformazioni.
- Archiviare History, configurazione, dipendenze e SHA256. Se gli XISF intermedi o l'archivio genitore restano separati, indicare esattamente dove: non chiamare autonomamente riproducibile uno ZIP che dipende da file esterni.
- Consegnare confronto prima/dopo e riferimento al 100%, distinguendo migliorie visibili e limiti. Un JPEG non sostituisce l'originale scientifico. Accettazione privata, pubblicazione e chiusura di un collaudo sono eventi distinti.
- Quando l'Owner accetta, registrare un evento riferito ai file esatti e ai loro SHA256, conservando i documenti precedenti come evidenza storica. L'accettazione non elimina limiti tecnici né autorizza implicitamente pubblicazione o chiusura della milestone.

Non chiudere processi PixInsight dell'utente per comodità. Terminare soltanto istanze isolate di proprietà del lavoro, dopo salvataggio e ricevuta terminale. Per controllare l'interfaccia leggere la skill computer-use disponibile; non introdurre un sistema alternativo di automazione del desktop.
