# BKL-051 — collegamento confermativo prima dell'invio

Stato: **implementazione in corso, R09 aperto / NOT_VALIDATED**. Zero controlli
scientifici qualificati. Nessuna attivazione, credenziale, analisi nativa o spesa
autorizzata da questo documento o dal codice.

## Risultato richiesto

Il piano congelato, il riferimento del caso e le tre esposizioni ordinate devono
essere vincolati prima degli invii. Gli intenti devono essere persistiti prima
delle richieste; una risposta persa lascia un tentativo da riconciliare mediante
sole letture, senza reinvio. Un processo incerto o un annullamento soltanto
richiesto impediscono il successivo avvio. `record_execution` conserva il proprio
ruolo di registrazione degli esiti, distinto dall'ammissione all'esecuzione e
dall'accettazione scientifica Owner.

## Prerequisito implementato

`ConfirmatoryCampaigns.dispatch_context` restituisce una fotografia coerente del
registro della campagna: hash del piano e dell'evento FREEZE, revisione congelata
degli input, hash del riferimento e del rapporto degli input, tre frame ordinati,
algoritmo e contratto con identificativi e hash. L'hash del contesto include questi
campi. Il contesto resta stabile quando si registrano altri casi del medesimo
piano; il current head non sostituisce l'identità immutabile del congelamento.

La lettura rifiuta piani non congelati, revocati o bloccati, riferimenti non
selezionati, revisioni degli input diverse da quelle congelate e casi con esito
già registrato. Non cambia il registro e non crea job. Restituisce sempre
`launchAuthorized:false` e `scientificValidation:NOT_VALIDATED`.

Il percorso privato Owner è:

`GET /v1/transient-analysis/campaigns/<planRef>/inputs/<witnessRef>/dispatch-context`

Riusa l'autenticazione Owner esistente. La credenziale Worker non accede a questo
percorso e nessun percorso equivalente Worker è aggiunto. La composizione runtime
delle campagne conserva il valore disabilitato esistente. Non sono aggiunti
percorsi locali, file originali, token o lease alla risposta.

## Disegno ancora da implementare e verificare

L'intento della tripletta e l'ammissione di ogni avvio devono usare il medesimo
registro autorevole della revoca. Le chiamate alla coda devono avvenire fuori dai
callback CAS, che possono essere ripetuti durante la risoluzione dei conflitti.
Gli identificativi deterministici permettono letture esatte dopo una risposta
persa; un GET 404 non autorizza a reinviare una richiesta potenzialmente in volo.

Due CAS separati, o una lettura immediatamente prima di creare il processo,
non costituiscono una transazione tra revoca remota e avvio del sistema operativo.
L'ordine ammissione/revoca deve essere esplicito: un'ammissione già emessa resta
in volo o incerta fino alle evidenze di chiusura, anche dopo revoca. Nessuna
revoca o scadenza prova da sola l'arresto di PixInsight. La lettura del contesto
qui implementata non risolve questo requisito e non consente ancora avvii.

Restano da completare il registro degli intenti e delle ammissioni, la proiezione
dei job che impedisca accessi attraverso i percorsi legacy, il coordinatore locale
sequenziale con intenti durabili, le riconciliazioni, i collegamenti dei rapporti,
la vista Owner e il collaudo integrato. Il flusso diagnostico singolo esistente
resta distinto. Nessun controllo confermativo è stato eseguito.

## Evidenze locali

Le suite `test_confirmatory_dispatch_context`, `test_confirmatory_campaign` e
`test_confirmatory_http` hanno superato 45 prove locali, comprese otto nuove prove
sul contesto e sui confini HTTP. Sono fixture sintetiche e non dimostrano
accettazione scientifica, dispatch completo, CI sull'exact HEAD, rilascio o
accettazione operativa. ARB e RQ esatte restano gate separati.
