# BKL-051: preparazione privata del tentativo lineare

Stato: sorgente candidata, senza driver o CLI. Nessuna preparazione reale,
autorizzazione nativa o cloud deriva da questo documento. Milestone aperta,
`NOT_VALIDATED`, zero nuovi controlli reali qualificati.

`LinearAttemptPreparation` crea il budget originale a 180 secondi nel costruttore,
prima di qualsiasi IO del piano. Il chiamante deve aver ottenuto consenso umano
fresco sul piano, sulla proposta e sul codice esatti prima di creare il tentativo.
`prepare()` consuma l'unico tentativo prima del primo IO e restituisce un
`LinearNativeSupervisor` originale non avviato. Non chiama Popen, non lancia
PixInsight, non accede a cloud/provider e non offre recupero da file o PID.
Il consumo è fissato anche sulla sessione bootstrap originale: un nuovo oggetto
non può ripetere una preparazione fallita prima di creare directory o registri.
Un nuovo interprete non autentica un nuovo consenso: il driver/operatore non
deve riusare la decisione dopo perdita del genitore o fallimento.

Il piano `DSG_NATIVE_LINEAR_PREPARATION_V1` contiene root privata canonica,
parametri V2, descrittori dei sette input obbligatori e delle eventuali carte
fino a 71 file forniti, e otto risorse parent fisse. `parameters.json` è prodotto
dal piano approvato, portando la chiusura sigillata a un massimo di 72 record.
Percorsi, hash, dimensioni e schemi sono chiusi e verificati. I parametri
descrivono geometria, formato e hash dell'header; il preparatore non decodifica
pixel FITS, maschere o fattori e non valuta il kernel. Il wrapper nativo deve
ancora verificare formati, geometria effettiva e modello, senza dedurre validità
fisica dalle sole dichiarazioni. Una preparazione riuscita non prova un modello
eseguibile o scientificamente valido.

La decisione `DSG_NATIVE_LINEAR_HUMAN_SCOPE_V1` è fornita separatamente con hash
atteso e riferimento al piano/proposta: evita un ciclo fra hash del piano e
hash della decisione. Deve corrispondere all'operazione, a un avvio/180 secondi,
al permesso di preparazione e cleanup posseduto e a nessun cloud. Deve coprire
l'intera scadenza originale. Il record JSON non autentica il consenso; il futuro
driver/operatore deve collegarlo a una vera decisione umana. I record sintetici
dei test non sono autorizzazioni reali e non possono essere usati per esecuzioni.

La preparazione verifica risorse e attestazione viva del bootstrap, poi crea tre
directory operative esclusive. Copia soltanto byte opachi dichiarati con creazione
esclusiva, letture limitate, hash in streaming, fsync, rilettura e identità del
descrittore sorgente. Conserva copie esatte del piano e della decisione, verifica
metadati di lineage e carte dichiarative, produce seal, e controlla almeno 1 GiB
libero e il limite aggregato di 200 MiB con riserva canonica Owner/ready e 1 MiB
cancel prima del grant. Non elimina o ripara copie parziali. Directory già
presenti impediscono un nuovo tentativo anche se il precedente fallì prima
dell'avvio. `grantAttemptConsumed` e `grantCommitted` distinguono una scrittura
tentata dal suo completamento verificato.

L'entry usa CRLF, quattro include in ordine fisso, template launcher privato e
una sola chiamata letterale con identificativi/hash/tempo validati. Percorsi
nativi con quote, traversal o Unicode non ammesso vengono respinti; nessun testo
arbitrario diventa codice. Il controllo collega entry, risorse, sorgenti parent
attestate, bootstrap, seal/grant e decisione; parent-intent collega il controllo.
La copia del piano viene aggiunta ai pin originali S7. I gruppi statici sono
acquisiti prima di restituire il supervisore e restano riferimenti forti sul
preparatore anche se una fase successiva fallisce. Solo il driver autorizzato
potrà chiamare esplicitamente `start()` una volta.

Il renderer è verificato con percorsi Windows sintetici. Le prove portabili di
composizione sostituiscono renderer, bootstrap e blocchi: non dimostrano include
PJSR o sharing Windows reale. Un percorso completo sintetico conserva il
fallimento prima delle immagini e la ricevuta di uscita con processo fittizio,
senza trasformarlo in successo tecnico o scientifico. I kernel di queste fixture
sono intenzionalmente opachi e non vengono eseguiti.

Restano driver isolato con protocollo esplicito di comandi e gestione di EOF,
packaging/manifest e consenso fresco sul pacchetto finale, mantenimento dei
riferimenti e rilascio esplicito dopo uscita, revisioni, preflight PJSR reale e
collaudo integrato del portale. R01–R14, modello fisico completo e 59 controlli
nulli realmente indipendenti non sono chiusi da questo componente. Rollback con
revert del codice/test/documento, preservando tentativi e registri incerti.
