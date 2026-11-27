# Batch candidato per i due depositi CFA XDRZ

Il componente BKL-046 deriva dal batch v6. Esegue ciascuno dei cinque controlli a traslazioni intere e il controllo frazionario ai depositi da 0,70 e 1,00 pixel. Ogni caso conserva le impronte dei tre descrittori e indica il gruppo di ingressi. Il batch esporta i parametri prima dell’esecuzione e verifica di nuovo la larghezza prima di scrivere i FITS RGB e dei pesi. Conserva anche la console e l’ordine delle esportazioni.

Nel test con un sostituto del processo, il batch registra 12 casi, 24 eventi e 24 chiusure delle finestre di risultato. Respinge 11 anomalie, compreso il cambio della larghezza dopo l’esecuzione. Il controllo frazionario deve ancora essere collegato alla verifica numerica dei FITS nativi. Un valore riletto dal processo, da solo, non dimostra la larghezza applicata.

Il componente resta fuori dal launcher operativo. Per l’avvio servono un preflight che verifichi e custodisca questi ingressi, il legame con il coordinatore, il confronto dei prodotti e le revisioni sul soggetto integrato. Il v6 congelato resta a 0,70 pixel.

Generare con `prepara.py <soggetto-v6> <kit-intero> <studio-due-depositi> <studio-frazionario> <directory-output>`. Verificare con `node collaudo.cjs batch-cfa.js piano.json contratto.json <nuovo-riscontro.json>`.
