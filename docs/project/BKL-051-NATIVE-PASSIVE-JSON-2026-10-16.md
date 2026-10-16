# BKL-051: parser passivo per la configurazione nativa

Stato: candidato di supporto all’integrazione nativa, senza avvii o validazione
scientifica. Il parser non legge file e non accetta richieste del portale.

`strict_passive_json.jsh` espone `parseStrictPassiveAsciiJson(bytes, limits)`.
Il chiamante locale fidato fornisce un `Uint8Array` prodotto dalla lettura nativa
limitata e, facoltativamente, `{maxBytes, checkBudget}`. I tre limiti di byte
ammessi sono 1, 8 e 64 MiB, rispettivamente per metadati, rilettura del risultato
e specifica del modello. Il valore predefinito è 1 MiB. Il monitor è `null` o una
funzione del codice locale revisionato: controlla tempo/annullamento e può
interrompere il parser, senza modificare i byte. Non proviene dal JSON.

L’interfaccia binaria è riservata a buffer nativi fidati; non è un sandbox per
oggetti JavaScript ostili o per globali del motore alterati. Rifiuta oggetti
generici, sottoclassi, buffer condivisi e sostituzioni delle proprietà usate del
buffer. I limiti con getter vengono rifiutati senza eseguirli. Il wrapper resta
responsabile di creare i buffer con API native, verificare gli hash e rifiutare
percorsi o oggetti forniti direttamente dal browser.

La sintassi è un sottoinsieme ASCII esplicito di JSON UTF-8. Rifiuta BOM, byte
non ASCII ed escape Unicode fuori ASCII; tutti i campi del protocollo proposto
usano ASCII. Gli escape ASCII vengono decodificati prima di rilevare chiavi
duplicate. `__proto__`, `prototype` e `constructor` sono vietati a ogni livello.
Gli oggetti restituiti hanno prototipo nullo; non vengono usati `eval`, reviver
o codice deserializzato.

| Limite | Massimo |
|---|---:|
| Profondità dei contenitori | 12 |
| Elementi di un array | 16384 |
| Membri di un oggetto | 32 |
| Contenitori complessivi | 65536 |
| Stringhe, incluse le chiavi | 131072 |
| Caratteri di una stringa decodificata | 192 |
| Caratteri decodificati complessivi | 4194304 |
| Membri complessivi | 262144 |
| Valori numerici | 2300000 |

I contatori precedono l’allocazione del relativo elemento. Limiti più restrittivi
possono intervenire prima di quelli aggregati: per esempio ogni membro richiede
anche una chiave stringa. Un input eccessivo viene rifiutato senza troncamenti.

I numeri usano la conversione Float64 del motore: non è aritmetica decimale
esatta. Overflow e una mantissa decimale non nulla che diventa zero sono
rifiutati; `-0` viene conservato. La sicurezza e l’intervallo degli indici sono
controlli dello schema successivo: un coefficiente numerico non viene trattato
automaticamente come indice.

La conversione di un token numerico lungo usa blocchi di 4096 byte. Nel caso
estremo di un singolo token da 64 MiB, frammenti e stringa ricomposta possono
richiedere insieme 256 MiB UTF-16. Con due buffer di input da 64 MiB, 128 MiB
stimati per dati materializzati e 32 MiB di riserva, il conto conservativo del
parser è **544 MiB**, entro il tetto pianificato di 768 MiB. Non è un limite
rigoroso della memoria del motore o del processo; occorre misurarlo nel collaudo
nativo. I buffer di parsing vanno rilasciati prima di allocare le immagini.

Il monitor viene chiamato all’ingresso, durante la scansione almeno ogni 4096
byte, durante la ricomposizione dei token numerici lunghi e alla fine. La
conversione numerica del motore è sincrona: una chiamata può oltrepassare il
tempo cooperativo. Il wrapper e il supervisore devono controllare il termine
anche dopo il ritorno e non accettare un completamento fuori tempo.

Le prove Node usano soltanto byte e numeri inventati. Coprono sintassi, escape,
chiavi duplicate, proprietà attive, limiti singoli e aggregati, underflow e
overflow numerico, interruzione cooperativa e conservazione dell’input. Non
dimostrano compatibilità PJSR, lettura di immagini, provenienza dei fattori,
correttezza del supervisore o accettazione scientifica. Restano necessari gli
schemi esatti del wrapper e i controlli incrociati di tutti i file sigillati.
