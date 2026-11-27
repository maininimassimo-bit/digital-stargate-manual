# Processo padre candidato per il batch CFA a due depositi

Il padre candidato ottiene il contesto della prenotazione dalla barriera R4, apre gli ingressi custoditi, prepara il batch e rilegge l’entrypoint materializzato. Un handle impedisce la scrittura dell’entrypoint. Il padre mantiene gli handle per tutti i 24 ingressi e per lo script fino all’uscita del figlio originale. Il comando è costruito per il figlio creato dal padre, senza adozione o secondo avvio.

Il collaudo chiama lo stesso componente con un testimone Windows. Nel percorso ordinario e dopo un errore iniettato nella prontezza, tutte le 25 aperture in scrittura sono respinte mentre il figlio vive. Dopo la sua uscita, le aperture riescono. Un ingresso alterato viene respinto prima di costruire il comando.

La prova usa un comando testimone e un contesto isolato. Restano da legare questo padre al launcher gestito, qualificare l’installazione protetta e ottenere revisioni e ammissione. PixInsight non è stato avviato.

Collaudare con `collaudo.py <directory-kit> <directory-batch> <nuovo-riscontro.json>`. Il kit contiene le dipendenze rilette dagli archivi fissati. `materializza-fonti.py` ricopia le dipendenze da tali fonti.
