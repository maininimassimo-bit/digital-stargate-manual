# BKL-051: errore di inclusione PJSR e correzione candidata

Stato: correzione sorgente candidata; milestone **OPEN / NOT_VALIDATED**,
zero nuovi controlli reali qualificati. Nessuna accettazione scientifica.

## Evidenza nativa e limiti delle prove precedenti

Il candidato `f113b2c853c470d11025ee8d5cce59697e581773` aveva CI 24/24 e
revisioni indipendenti approvate nel loro perimetro tecnico. La successiva
prova locale, autorizzata separatamente su soli sei valori inventati, ha
consumato una preparazione e un avvio. Non ha completato il preflight.

Il supervisore originale ha raggiunto il budget originale di 180 secondi
con errore `NATIVE_BUDGET_EXPIRED`, senza Owner-ready o ritorno nativo
causale, senza pubblicazione e senza ricevuta di chiusura posseduta.
Il registro reale di PixInsight 1.9.5 build 1706, letto tramite Computer Use,
ha inoltre mostrato `SyntaxError: illegal character` nella riga 8 di
`native_linear_measurement.jsh`, durante l'inclusione dell'entry e prima
di qualsiasi calcolo del wrapper.

La finestra mostrava Ready, Pause/Abort disabilitato e nessuna vista
disponibile. Queste osservazioni non sono state trasformate in un ritorno
nativo causale. Con un nuovo consenso, limitato alla riconciliazione, è
stato impartito un solo comando di chiusura normale alla finestra originale.
L'handle originale ha poi provato l'uscita con codice 0; soltanto dopo il
driver ha rilasciato i file ed è uscito. Nessuna terminazione forzata,
ripetizione, cancellazione di file o convalida della prova fallita.

## Correzione del sorgente

Le tre verifiche della radice Windows, in wrapper, ownership e launcher,
usavano una slash escapata immediatamente seguita dal delimitatore finale
di una regex. La sequenza conteneva due slash adiacenti. Il testo
dell'errore nativo è compatibile con un taglio del preprocessore a quel
punto, mentre il solo parser JavaScript dei test accettava il sorgente.

La correzione usa l'escape esadecimale `\x2f` per la stessa slash nelle
regex di prefisso e suffisso. Restano invariati drive alfabetico, slash
iniziale obbligatoria, rifiuto del separatore finale, caratteri vietati,
limite di lunghezza e controlli di ogni componente. Nessuna modifica a
budget, grant, nonce, handle, processo, ricevute o criteri scientifici.

## Prove e prossimi gate

La nuova regressione dimostra che il parser JavaScript ordinario accetta
il controesempio e che una trasformazione conservativa che tronca le
code di commento lo rende invalido. Lo stesso controllo fallisce sui
sorgenti precedenti e passa dopo la correzione. Questa trasformazione è
soltanto una regressione del rischio osservato: **non è un preprocessore
PJSR e non dimostra la compatibilità nativa**.

La suite completa del wrapper/launcher, con soli mock e pixel inventati,
passa da 51 PASS e 1 FAIL prima della correzione a 52/52 PASS dopo, in
29,914 secondi. Include drive maiuscoli/minuscoli, risultati condizionali
invariati e percorsi relativi, UNC, backslash, componenti vuote, punto,
parent, caratteri vietati e non ASCII rifiutati prima di letture o viste.

Restano da completare CI e revisioni sul nuovo commit esatto. Resta inoltre
aperta la fattibilità dell'intera catena entro i 180 secondi: la precedente
misura di una singola lettura opaca non includeva tutti i controlli del
bootstrap e le verifiche ripetute dell'operazione. La correzione sintattica
non risolve né dimostra questo requisito temporale. Nessun limite viene
esteso e nessuna prova nativa viene ripetuta con il consenso consumato.

Le prove locali, la console e la riconciliazione sono conservate
separatamente negli artefatti privati `Esito-prova-native-f113-7944807e-r1-20261016.json`,
`Console-nativa-prova-f113-7944807e-r1-20261016.txt` e
`Riconciliazione-uscita-normale-native-7944807e-r2-20261016.json`.
L'assenza di History/checkpoint da questo tentativo è esplicita: il
wrapper non è stato eseguito, e non vengono fabbricati prodotti mancanti.
Rimangono integralmente R01–R14, il modello fisico congiunto e i 59
controlli nulli reali indipendenti richiesti per il collaudo.
