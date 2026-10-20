# BKL-051 — conferma Owner e preparazione locale durevole

Stato: **in sviluppo**, R09 aperto, milestone **NOT_VALIDATED**. Nessun controllo reale qualificato da questo incremento.

La preparazione locale e la conferma nel browser costituiscono due passaggi distinti. Il PC verifica il pacchetto dei tre file e le tre ricevute di registrazione, conserva una dichiarazione locale con scrittura esclusiva, flush, fsync e rilettura, quindi esporta la busta minimizzata. La conferma del browser appartiene alla pagina e alla selezione correnti, usa un nonce casuale di 128 bit e non sopravvive a ricaricamento, uscita dall'account o cambio della selezione.

Il blocco locale identifica l'operazione per origine del servizio, piano, azione e controllo/contesto (oppure intento e ordinale della proiezione). Un diverso identificativo di decisione o nonce non crea una seconda operazione. Un errore di scrittura o rilettura conserva il blocco; non esiste recupero mediante nuova cartella alternativa o eliminazione del blocco.

Il browser consuma la conferma prima del primo punto di attesa nell'invio e conserva una registrazione pendente, riletta, prima del POST autenticato. Non dichiara fsync della memoria del browser. Una risposta persa o una pagina ricaricata richiedono riconciliazione: un GET senza risultato non autorizza un nuovo POST. Una risposta arrivata dopo l'uscita dall'account non ripristina lo stato della pagina.

Le impronte e il nonce sono riferimenti di correlazione, non credenziali, permessi o attestazioni di autenticità. La proposta locale deve essere confrontata con la ricevuta autenticata del piano e il contesto congelato del servizio. La busta non include percorsi locali, credenziali Google/Worker, token di lease, immagini o misure scientifiche. Preparazione, proiezione e ammissione tecnica non attestano avvio o arresto nativo né validazione scientifica.

## Evidenza tecnica conservata

- Stager offline: 10 test sintetici PASS; revisioni ARB e RQ sui due file esatti approvate. Le controprove indipendenti verificano concorrenza e fsync fallito.
- Componenti browser e selezione: 32 test PASS, revisioni ARB e RQ approvate sui file esatti. Le prove usano un pacchetto applicativo sintetico e confrontano la chiave semantica JavaScript con quella Python.
- Cronologia completa: 51 test PASS, build rigorosa e revisioni ARB/RQ approvate sul precedente incremento. La ricevuta sintetica di 534 eventi non rappresenta 59 controlli reali.

## Integrazione candidata

La pagina candidata include un pannello per aprire la proposta locale, scegliere preparazione o proiezione di uno dei tre job, verificare la selezione sul piano congelato e scaricare una conferma temporanea. La busta preparata dal PC richiede una conferma esplicita prima dell'unico invio. Il pannello condivide accesso, invalidazione, stato occupato e blocchi con gli altri comandi Owner.

Dopo la registrazione, nuove letture autenticate producono una ricevuta minimizzata. La richiesta resta pendente fino al caricamento della copia salvata e a una nuova verifica esatta. Il recupero non effettua POST. Per i job si verifica identità e namespace attraverso una lettura tecnica dedicata; la ricevuta rimane stabile se il job cambia stato. `projectionObserved:true` indica sola esistenza e `reservationFreshness:NOT_ATTESTED` esclude una nuova prenotazione o un'autorizzazione di avvio.

La lettura Owner dei metadati tecnici usa il namespace Owner e non accetta credenziali Worker. Il namespace Worker conserva la propria autenticazione dedicata. Le risposte omettono lease, tentativi e credenziali; non applicano scadenze o mutazioni della coda. Test e revisioni del componente HTTP sono approvati; non costituiscono un'attivazione remota.

Il flusso candidato e il collegamento al pannello Owner superano 22 test, con pacchetto e cronologia applicativi sintetici. Le buste del test di interfaccia simulano lo scambio locale: la durabilità viene verificata separatamente nei test dello stager. Il disegno separa così prove dell'interfaccia, filesystem e autenticazione; nessuna prova sintetica qualifica un controllo scientifico.

## Gate ancora aperti

Restano build e verifiche del candidato integrato, CI sull'esatto commit aggiornato, revisioni dell'integrazione e collaudo visivo. La conversione delle tre ricevute in un handoff locale verificato e il recupero assistito di processi incerti richiedono ancora lavoro. Il collaudo scientifico e tutti i requisiti R01–R14 restano soggetti alle rispettive prove.

Questo lavoro non attiva il servizio, non avvia PixInsight, non modifica IAM, non usa credenziali reali e non effettua query astronomiche.
