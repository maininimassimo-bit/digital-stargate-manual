# Verifica della fase Bayer nelle due serie RAW

Sono state rilette e verificate le impronte di tutte le 54 pose previste. Nei 39 CR2 di IC 1805, Canon EOS 40D, la mappa dei colori decodificata è RGGB sia nell’intero RAW sia nel ritaglio visibile non ruotato. Il ritaglio inizia sempre alla riga 18 e alla colonna 30, quindi conserva le parità. Il codice di orientamento vale 5 sia nel riscontro EXIF sia nel campo di orientamento del decodificatore. Il controllo conserva i due campi e lavora nelle coordinate del mosaico RAW.

Nei 15 FITS originali di M8–M20, ZWO ASI2600MC Pro, l’intestazione riporta sempre RGGB, binning 1 × 1 e origine del sottoframe (0, 0). I campi XBAYROFF, YBAYROFF e ROWORDER sono assenti in tutti i file. La dichiarazione FITS è verificata, mentre l’orientamento fisico delle righe non è attestato in modo indipendente. Una trasformazione degli assi o un ritaglio con origine dispari richiede una nuova verifica della fase.

I due set forniscono controlli RGGB con due modelli di camera per l’asse CFA_DITHER_DRIZZLE/1. Per completarlo restano da congelare l’orientamento fisico all’acquisizione e la lettura nativa, oltre agli altri schemi Bayer. Questa prova non confronta la risposta scientifica delle camere.

Per replicare eseguire `fase.py <directory-IC1805> <directory-M8-M20> <rawpy-estratto> <pacchetti-Python> <directory-DLL-VC> <nuovo-rapporto.json>`. Lo script verifica gli archivi, le pose, i riscontri di acquisizione e i membri del decoder. Il rapporto registra le impronte delle pose senza esportare pixel grezzi.
