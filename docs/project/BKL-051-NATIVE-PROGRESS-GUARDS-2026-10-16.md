# BKL-051 — costo dei controlli durante le letture

Stato: correzione tecnica candidata entro le invarianti V5. Nessuna autorizzazione
di preparazione o esecuzione reale. Milestone aperta, `NOT_VALIDATED`, zero nuovi
controlli reali qualificati.

Una misura di sola lettura ha richiesto 69,79 secondi per verificare gli stessi
77.608.944 byte dell'eseguibile installato. Il callback completo rileggeva i 56
sorgenti a ciascuno dei 1187 controlli, moltiplicando il costo. La costruzione dei
registri ripete la verifica del controllo di avvio: il successo dei test sintetici
non dimostrava quindi la fattibilità del budget originale di 180 secondi.

Il disegno approvato in `ARB-design-native-progress-guards-r1-20261016.json`
classifica la separazione come correzione implementativa entro V5 S3/S4. Non
estende la scadenza, non riduce la chiusura dei sorgenti e non crea autorità.

`_pin`, il controllo di avvio e il relativo snapshot accettano un callback interno
opzionale `progress_guard`. Se omesso, rimane il callback originale a ogni blocco.
Valori non callable, anche falsi, sono rifiutati. Il callback è scelto soltanto dal
codice fidato: nessun campo JSON o comando del driver può disabilitare i controlli.

Tutti i byte restano letti in blocchi di massimo 65536 e inclusi nello stesso hash.
Rimangono dimensioni, limiti, identità dei descrittori originali, percorsi e pin.
Il callback completo è chiamato prima dell'apertura e dopo i controlli di hash e
identità della risorsa. Lo snapshot conserva separatamente entrambi i callback
originali e continua a confrontare l'attestazione viva dei sorgenti prima e dopo
l'intera verifica. Non conserva un risultato positivo in una cache temporale.

Nei registri preavvio il callback di progresso mantiene budget originale,
incertezza in memoria, directory originali, limite dei metadati e tutti i segnali
di cancellazione/incertezza/fase. Omette soltanto la rilettura dei sorgenti, che
resta nel callback completo ai confini. Quest'ultimo ripete i controlli economici
anche dopo la verifica del codice. Non si riusa questo callback preavvio nella
pubblicazione: il suo controllo di tempo e segnali rimane compatibile con la sola
osservazione e conservazione dopo un superamento noto.

I blocchi Windows mantengono gli stessi handle e controlli originali prima e dopo
l'hash. Solo il callback interno della lettura può differire. Il preparatore usa
per i blocchi statici lo stesso `budget.check` originale; mantiene il controllo
completo di sessione prima di ogni risorsa e alla fine della verifica. Le guardie
esterne della preparazione e dell'avvio continuano a richiedere tempo residuo.
Nessun rilascio, nuovo processo o ripristino di tentativi viene aggiunto.

La misura di sviluppo dello stesso eseguibile, con entrambi i controlli completi
e 1185 callback di progresso, è scesa a circa 0,185 secondi. È un confronto della
singola lettura: il callback di progresso del benchmark controlla solo il tempo,
senza directory/segnali della preparazione. Non prova che l'intero percorso,
l'avvio nativo e il checkpoint termineranno entro 180 secondi.

Con le guardie reali dei registri, tre directory e sedici file di metadati
sintetici, la singola lettura richiedeva ancora circa 16,04 secondi. La scansione
dei metadati ora verifica gli antenati prima e dopo ogni directory, evitando di
ripeterli per ciascun file. Ogni elemento resta ispezionato con `lstat`: link,
reparse, file non regolari e hardlink sono rifiutati. Ogni directory viene
confrontata con l'identità originale al termine; anche le directory in coda
mantengono l'identità rilevata nel padre e non possono adottarne una sostitutiva.
Contatori globali di profondità, elementi e byte restano invariati e nessun
risultato è riusato fra chiamate. Il confine rimane privato e quiescente, senza
promessa di snapshot atomica contro modifiche ostili concorrenti.

Questa seconda correzione porta la stessa misura con guardie reali a circa
5,34 secondi, ancora su 56 sorgenti. Il contesto è sintetico e non passa dal
costruttore operativo dei registri; mancano gli snapshot del bootstrap e tutte
le altre fasi. La misura resta distinta dalla fattibilità dell'intera prova.

La selezione di un futuro manifest richiede la chiusura esatta dei moduli di
tutte le fasi, incluse cancellazione, errore, EOF e rilascio. Il profilo di solo
import carica 22 file interi, senza estrarre o modificare funzioni. I soli import
locali tardivi osservati sono in tre funzioni del worker preesistente, estranee
alla catena nativa che ne usa solo gli helper del broker. Questa constatazione
non approva da sola il sottoinsieme: servono audit dei percorsi e prove sintetiche
con loader chiuso, rigetto degli import ulteriori e nuovi manifest esatti rivisti.

Le regressioni coprono default invariato, conteggi per blocco e confine su byte
sintetici, errore del codice al confine finale, scadenza durante lettura, callback
invalidi, inizializzatore vuoto, attestazione mutata, blocchi Windows ancora attivi
e controlli preavvio di budget/segnali senza rilettura dei sorgenti. Restano da
superare i controlli incrociati di pubblicazione e chiusura, la CI dell'exact head
e le revisioni indipendenti del codice finale.

Il piano candidato `45b16527...` e il suo vecchio pacchetto restano conservati in
HOLD. La modifica richiede un nuovo pacchetto sorgenti/bootstrap e un nuovo piano
con hash esatti prima di qualsiasi proposta operativa e consenso umano fresco.

Rollback: revert dei file modificati, conservando prove e piani precedenti. Il
rollback non autorizza avvii, rinnovi, cancellazioni o riuso di vecchi consensi.
