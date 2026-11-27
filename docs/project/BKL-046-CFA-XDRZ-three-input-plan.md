# BKL-046 · Piano candidato per il controllo XDRZ a tre ingressi

Il codice WBPP installato applica un minimo di tre immagini nel suo flusso di DrizzleIntegration. Il piano candidato adotta lo stesso minimo per evitare che un eventuale rifiuto per numero di immagini renda inconcludente il controllo. Questo non attribuisce la stessa regola a ogni modalità di esecuzione del modulo.

Le cinque esecuzioni candidate includono tre casi con traslazioni intere e due con shear e origini serializzate diverse. Ogni caso dispone di tre mosaici sorgenti distinti. Il terzo ingresso dei casi interi mantiene discriminanti i valori e i pesi attesi dei due verdi di controllo. Il piano fissa scala 1, deposito quadrato 0,70 e CFA RGGB letto dagli XDRZ. Registra il rigetto come attivo solo nei due controlli di maschera. Richiede intensità RGB lineari, pesi grezzi e una rilettura dei parametri effettivi.

Il verificatore del piano ha controllato gli ingressi e tre impronte dell'installazione. Ha respinto i casi con due ingressi, un ingresso duplicato e il rigetto attivo senza maschera. Il comparatore FITS ha riconosciuto sei risultati previsti e respinto quattro alterazioni. Due generazioni hanno riprodotto 34 file identici, incluso il manifest. SHA-256 del piano `377aea9a4decbf470a95c92f7f85852bc59f5e056b76a8c7ae110e842fcfd6e7`.

Il piano riguarda solo i controlli sintetici. Le impostazioni effettive, l'origine e la semantica della maschera restano da verificare in PixInsight dopo revisione e ammissione del coordinatore. Zero esecuzioni native.
