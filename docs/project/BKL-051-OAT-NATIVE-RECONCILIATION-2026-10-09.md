# BKL-051 — riconciliazione OAT e diagnostica nativa

Stato: incremento documentale candidato ai gate. BKL-051 OPEN; nessuna accettazione scientifica o operativa finale.

## Evidenze reali successive alla PR #522

Due sessioni cloud limitate, autorizzate separatamente dall'Owner, hanno utilizzato la stessa immagine verificata dalla seconda build. La prima ha verificato un nuovo job sintetico Owner attraverso portale, servizio privato e PixInsight: completamento tecnico, rapporto locale conservato, originali invariati. Un secondo job distinto è stato annullato prima della prenotazione e dell'avvio nativo. Il rapporto conserva zero misure complete, zero esclusioni e due budget incompleti: varianza completa e significatività restano sconosciute. Non è una prova astronomica valida.

La prima attivazione non aveva instradato il traffico alla revisione nuova: errore conservato, rollback e correzione esplicita entro il limite autorizzato; nessuna esecuzione nativa attribuita a quel tentativo. Il completamento riguarda soltanto la sessione corretta.

La seconda sessione ha verificato cinque richieste GET respinte con HTTP 403 / ACCESS_DENIED: bearer worker errato, credenziale transient sul worker legacy, credenziale worker sul canale Owner con e senza origine, origine browser sul canale worker. Nessuna credenziale legacy estratta. Una GET autenticata ha riconciliato il tentativo già completato e già ACKNOWLEDGED con rapporto locale verificato e ricevuta coincidente, senza replay o riacquisizione della proprietà del processo. Non è una simulazione di risposta persa.

La lettura Owner reale dal portale mostra il completamento e l'annullamento con il medesimo digest e conteggi. Nessuna valutazione Owner dedotta dalla visualizzazione. Backup e stato primario verificati byte-identici; generazione primaria immutata nella seconda sessione. Non è un'iniezione di conflitto CAS.

Entrambe le sessioni sono terminate con rollback verificato indipendentemente: traffico P6 al 100%, variabili transient rimosse dalla configurazione corrente e rimosso il solo binding condizionale temporaneo. Revisioni storiche e prove conservate; non si dichiara cancellazione delle revisioni. Nessuna nuova build o servizio transient permanentemente attivo.

## Diagnostica nativa V5

V4 è stato osservato nella UI reale: errore di protezione dalla sovrascrittura prima di aprire gli input. L'istanza osservata è stata chiusa e l'assenza del processo verificata. Resta non attestato il contenuto realmente caricato dopo la modifica dello script avvenuta successivamente al lancio: questa limitazione storica non viene rimossa.

V5 è un nuovo ramo con script e applicazione verificati mediante digest prima dell'avvio, radice normalizzata e sei SHA256 degli originali verificate prima e dopo. Controller con handle proprio, osservazione limitata e arresto soltanto dopo ricevuta conclusiva e zero finestre aperte. Nessun arresto ricostruito da PID. I rami precedenti, History iniziali/correnti, maschere, checkpoint e archivio genitore sono conservati.

StarDetector nativo restituisce 639, 206 e 1075 sorgenti. Audit indipendente completo: zero discrepanze tra maschere raw corrette e FITS originali, zero discrepanze nelle maschere binarie a 8 bit, zero discrepanze nel segnale normalizzato float32 e zero pixel scientifici alterati. Nessuna trasformazione automatica in magnitudini o varianze calibrate. History a monte NOT_ATTESTED; rilevatore in lettura e maschera manuale tracciati tramite script e ricevute, senza dichiarare una History di processi integralmente riproducibile o un archivio standalone delle dipendenze.

Il primo confronto diagnostico con l'effemeride, usando la conversione proposta meno mezzo pixel, trova distanze minime circa 11,42, 14,80 e 0,88 secondi d'arco. Non costituisce associazione accettata: timing, covarianza astrometrica, PSF/confusione e policy quantitativa non sono validati. Non dichiarare Atami recuperato in tutte le epoche. Campo selezionato con effemeride nota, non ricerca cieca.

## Controllo indipendente con cataloghi PSF pubblici

Tre richieste pubbliche circoscritte hanno acquisito i cataloghi PSF delle medesime esposizioni, con ricevute HTTP 200 e digest conservati. Nessuna immagine Owner trasmessa e nessun rilancio PixInsight. IRSA documenta il prodotto `psfcat.fits` e la derivazione del suo percorso dalla metadata: [ZTF Metadata/API](https://irsa.ipac.caltech.edu/docs/program_interface/ztf_metadata.html).

I cataloghi riportano sorgenti a circa 0,15/0,19/0,20 secondi d'arco dalle posizioni previste. Sono misure del provider, non nostre associazioni accettate o fotometria calibrata. I valori del catalogo non sostituiscono un modello completo di incertezza; le magnitudini strumentali non vanno presentate come magnitudini calibrate. Le due prime sorgenti vicine all'effemeride non sono recuperate dal rilevatore V5, mentre la terza lo è soltanto come confronto diagnostico. Il controllo del footprint nelle zone previste non trova pixel esclusi o saturi; non autorizza abbassamenti automatici di soglia.

Sulla stessa popolazione di tutte le sorgenti native finite, senza selezione per distanza o flusso, il confronto con il vicino di catalogo più prossimo è stato ripetuto per tre offset prestabiliti: -0,5, 0 e +0,5 pixel. L'offset nullo dà mediane circa 0,082/0,084/0,054 secondi d'arco; la sottrazione di mezzo pixel dà circa 0,705/0,719/0,703. Questo evidenzia una convenzione del rilevatore da verificare separatamente rispetto alle coordinate geometriche delle aperture. Il contratto generale non è cambiato e le analisi storiche sono conservate. Vicini più prossimi e mediane non costituiscono identità validate, calibrazione astrometrica assoluta o prova cieca di completezza. Ripresa scientifica: verificare la convenzione specifica di StarDetector e la sensibilità/PSF prima di nuove associazioni.

## Matrice dei requisiti residui

| Perimetro | Evidenza disponibile | Requisito ancora aperto |
|---|---|---|
| S1/S2 | Input conservati, contratti, astrometria diagnostica | Calibrazione, covarianze, timing, matching con moto proprio, policy quantitativa validata |
| S3/S3-M | Controlli pubblici e rilevatore nativo corretto | Pipeline fotometrica completa, associazioni reali, tracklet, completeness e falsi positivi con prove cieche |
| S4 | Owner create/read, completamento sintetico e cancel prima dell'avvio; GET negative e ACK storico | Non-Owner Google reale, cancel durante il nativo, risposta persa, conflitto CAS reale, recovery dopo quiescenza, revisione/export Owner |
| S1-R/S4-R/S5-R | Ricerca procedure e dossier locale DRAFT | Adattatori/formati verificati, ricevute e gestione duplicati/errori; prove sandbox dove disponibili e decisioni sui requisiti esterni |
| S5 | Prove tecniche e rollback tracciati | Regressioni/accessibilità finali, limiti e soglie validati, accettazione operativa Owner |

Ordine di ripresa: verificare l'associazione e la qualità dei dati pubblici prima di adottare soglie; implementare i budget scientifici mancanti con controlli indipendenti; completare i casi lifecycle non eseguiti; validare gli adattatori e preparare l'accettazione finale. Nuove sessioni cloud richiedono una proposta concreta e la relativa autorizzazione: le due sessioni precedenti sono esaurite. Nessun invio reale, pubblicazione fotografica o nuova elaborazione P6. F4/F5, BKL-050, Safety e collegamento C→F invariati.

Ricevute complete, script pinned, screenshot Owner e manifest SHA256 conservati nell'archivio privato. Identificativi di job/worker, percorsi Owner, credenziali e dati integrali non sono pubblicati. Questo documento non chiude alcun requisito non eseguito e richiede CI e review sul proprio commit prima del rilascio.
