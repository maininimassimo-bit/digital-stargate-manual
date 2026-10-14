<link rel="stylesheet" href="../styles/scientific-photo-upload.css">
<link rel="stylesheet" href="../styles/scientific-transients.css">

<div class="dsg-photo-upload dsg-transients" data-dsg-transients>
  <h1>Analisi scientifiche private</h1>
  <p>Consulta lo stato delle analisi e conserva una ricevuta dei riferimenti e dei conteggi comunicati dal PC. Immagini, misure, maschere, History e rapporto completo restano sul tuo computer.</p>
  <p>La funzione è in sviluppo: il servizio dedicato non è ancora attivato. Questa pagina non avvia analisi e non invia segnalazioni. La verifica di possibili sorgenti variabili, nove o asteroidi richiede ancora il collaudo scientifico.</p>
  <p data-dsg-transients-message role="status" aria-live="polite">Accedi con l’account Owner per consultare il servizio privato.</p>
  <button type="button" data-dsg-transients-connect>Accedi con Google</button>
  <button type="button" data-dsg-transients-disconnect disabled>Termina accesso</button>
  <div data-dsg-transients-signin></div>
  <section data-dsg-test-plan aria-label="Piano locale di collaudo">
    <h2>Piano locale di collaudo</h2>
    <p>Apri una bozza minimizzata preparata sul PC per consultare il campione candidato. Il file viene letto nel browser senza essere inviato al servizio o conservato. Usa il formato BKL051_TEST_PLAN_DRAFT_V1, privo di percorsi e metadati personali.</p>
    <label>Bozza del piano <input type="file" accept="application/json,.json"></label>
    <p role="status" aria-live="polite">Nessun piano caricato.</p>
    <p data-dsg-test-plan-result></p>
    <details>
      <summary>Prepara una revisione della bozza caricata</summary>
      <p>Puoi cambiare l’impronta dell’algoritmo o escludere casi dalla copia da salvare. Registra sul PC motivi e regole prima di congelare una nuova versione: nessuna modifica è un collaudo confermativo.</p>
      <label>SHA256 dell’algoritmo (facoltativo nella bozza) <input type="text" data-dsg-plan-algorithm maxlength="64" autocomplete="off" spellcheck="false"></label>
      <label>Identificativi dei casi da escludere, separati da spazi <textarea data-dsg-plan-exclude rows="3" autocomplete="off" spellcheck="false"></textarea></label>
      <button type="button" data-dsg-plan-export disabled>Salva una nuova bozza</button>
    </details>
    <p>Obiettivo del piano: limite dei falsi positivi del 5%, confidenza unilaterale del 95%, almeno 59 controlli indipendenti con zero false segnalazioni. Le sequenze candidate non sono ancora controlli qualificati. Questa consultazione non congela il piano, non avvia prove e non registra un'accettazione.</p>
  </section>
  <section data-dsg-input-lineage aria-label="Provenienza delle copie sperimentali">
    <h2>Provenienza delle copie sperimentali</h2>
    <p>Apri la ricevuta minimizzata BKL051_INPUT_LINEAGE_V1 preparata sul PC per distinguere originale osservativo, copia calibrata sperimentale e derivato con metadati copiati. La verifica dei file non certifica la calibrazione. L’appartenenza al manifest candidato è solo un controllo d’identità: non qualifica un controllo e non collega automaticamente il derivato a un tentativo.</p>
    <label>Ricevuta di provenienza <input type="file" accept="application/json,.json"></label>
    <p role="status" aria-live="polite">Nessuna provenienza caricata.</p>
    <div data-result></div>
    <p>Questa sezione funziona senza autenticazione e legge soltanto in memoria, senza upload o conservazione. Incertezza completa, significatività e autorizzazione all’esecuzione non derivano da questa ricevuta.</p>
    <p>Per i piloti M27 restano documentati il limite temporale dei dark 2024 e i contributi di rumore e covarianza ancora non quantificati. I parametri nominali della camera scelti dall’Owner non costituiscono un’incertezza completa.</p>
  </section>
  <section data-dsg-calibration-context aria-label="Calibrazione e incertezza degli input">
    <h2>Calibrazione e incertezza degli input</h2>
    <p>Apri insieme la provenienza delle copie e il contesto di calibrazione esportati dal PC. Il confronto controlla che gli identificativi degli originali e dei derivati corrispondano. Le mappe mostrate riguardano soltanto il rumore nominale di lettura.</p>
    <label>Ricevuta di provenienza <input data-lineage type="file" accept="application/json,.json"></label>
    <label>Contesto di calibrazione <input data-calibration type="file" accept="application/json,.json"></label>
    <p role="status" aria-live="polite">Nessun contesto di calibrazione caricato.</p>
    <div data-result></div>
    <p>Lettura locale in memoria, senza invio o conservazione. Le componenti mancanti restano sconosciute e non autorizzano un esito scientifico positivo.</p>
  </section>
  <section data-dsg-astrometry-context aria-label="Astrometria candidata e tempi">
    <h2>Astrometria candidata e tempi</h2>
    <p>Confronta il contesto WCS esportato sul PC con la provenienza dello stesso input. Tempi degli header, arrotondamenti e metadati derivati restano distinti. I residui sui riferimenti esclusi dal fit non costituiscono un’incertezza astrometrica completa.</p>
    <label>Ricevuta di provenienza <input data-lineage type="file" accept="application/json,.json"></label>
    <label>Contesto astrometrico <input data-astrometry type="file" accept="application/json,.json"></label>
    <p role="status" aria-live="polite">Nessun contesto astrometrico caricato.</p>
    <div data-result></div>
    <p>Lettura locale in memoria, senza invii o conservazione. Il browser controlla le ricevute; immagini, coordinate private e query dei cataloghi non vengono caricate.</p>
  </section>
  <section data-dsg-multi-epoch aria-label="Confronto preliminare multi-epoca">
    <h2>Confronto preliminare multi-epoca</h2>
    <p>Apri la versione del piano e il confronto esportato dai rapporti tecnici della stessa cronologia. Scala, varianze e covarianze richiedono un budget esplicito: una scala mancante non diventa uno e una covarianza sconosciuta non diventa zero.</p>
    <label>Versione del piano <input data-plan type="file" accept="application/json,.json"></label>
    <label>Confronto multi-epoca <input data-comparison type="file" accept="application/json,.json"></label>
    <p role="status" aria-live="polite">Nessun confronto caricato.</p>
    <div data-result></div>
    <p>Lettura in memoria senza invii, conservazione o lancio. I risultati preliminari non classificano sorgenti variabili e non costituiscono un test confermativo.</p>
  </section>
  <section data-dsg-motion aria-label="Ipotesi di associazione per oggetti mobili">
    <h2>Ipotesi di associazione per oggetti mobili</h2>
    <p>Consulta tutte le combinazioni di un gruppo esplicito di rilevamenti su tre esposizioni. Il modello mostra moto e residui descrittivi senza scegliere automaticamente una sorgente o accettare un tracklet. Un gruppo selezionato con effemeride nota resta un controllo pre-selezionato.</p>
    <label>Ricevuta delle ipotesi <input type="file" accept="application/json,.json"></label>
    <p role="status" aria-live="polite">Nessuna ipotesi di moto caricata.</p>
    <div data-result></div>
    <p>Lettura in memoria, massimo 4 MiB, senza invii o conservazione. Nessun lancio, query, classificazione automatica o autorizzazione alla segnalazione.</p>
  </section>
  <section data-dsg-case-dossier aria-label="Dossier del caso e revisioni interne">
    <h2>Dossier del caso e revisioni interne</h2>
    <p>Apri la ricevuta del dossier congelato sul PC: piano, cronologia, tentativi ed eventuale confronto restano riferiti ai file esatti. Una modifica successiva non trasferisce la revisione a un nuovo contenuto.</p>
    <label>Ricevuta del dossier <input data-view type="file" accept="application/json,.json"></label>
    <p data-view-status role="status" aria-live="polite">Nessun dossier caricato.</p>
    <div data-result></div>
    <details data-review-form>
      <summary>Prepara una revisione interna o una revoca</summary>
      <label>Identificativo locale del revisore <input data-actor type="text" maxlength="32" autocomplete="off" spellcheck="false"></label>
      <button data-new-actor type="button">Crea identificativo locale</button>
      <label>Azione <select data-action><option value="KEEP_FOR_REVIEW">Conserva per revisione</option><option value="REJECT_CANDIDATE">Respingi il candidato</option><option value="FOLLOW_UP">Richiedi approfondimento</option><option value="REVOKE_REVIEW">Revoca una revisione</option></select></label>
      <label>Revisione da revocare <select data-target disabled></select></label>
      <label>Motivazione privata, su una riga <input data-note type="text" maxlength="2048" autocomplete="off"></label>
      <button data-save type="button" disabled>Salva richiesta di revisione sul PC</button>
      <p data-request-status role="status" aria-live="polite">Nessuna richiesta registrata.</p>
      <p>Il file scaricato va applicato al registro locale sulla stessa testa. Il download non registra già una decisione. Una revoca conserva l’evento precedente. Nessuna identità autenticata o autorizzazione all’invio deriva da questo modulo.</p>
    </details>
  </section>
  <section data-dsg-controlled-recovery aria-label="Recupero controllato esplorativo">
    <h2>Recupero controllato esplorativo</h2>
    <p>Consulta l’esperimento con segnali sintetici aggiunti a una copia del fondo reale M27. Verità e parametri sono conservati separatamente dal manifest del rilevatore. Mancanze, ambiguità e mancati recuperi restano visibili; questa prova non qualifica i controlli nulli del piano.</p>
    <label>Ricevuta del recupero controllato <input type="file" accept="application/json,.json"></label>
    <p role="status" aria-live="polite">Nessun risultato di recupero caricato.</p>
    <div data-result></div>
    <p>Lettura locale in memoria, senza upload, salvataggio o lancio. Una prova esplorativa su un solo fondo non misura completezza generale o falsi positivi indipendenti.</p>
  </section>
  <section data-dsg-plan-review aria-label="Versioni ed evidenze del piano locale">
    <h2>Versioni ed evidenze del piano locale</h2>
    <p>Apri la ricevuta minimizzata della versione esportata sul PC, in formato V1 oppure V2 con la prova dei derivati. Mostra separatamente qualificazione documentata, non valutabilità, tentativi tecnici, esiti scientifici dichiarati e revisione Owner. La lettura avviene in memoria, senza invio o conservazione.</p>
    <label>Ricevuta della versione <input type="file" accept="application/json,.json"></label>
    <p role="status" aria-live="polite">Nessuna versione caricata.</p>
    <div data-dsg-plan-review-result></div>
    <details data-dsg-readiness>
      <summary>Verifica i motivi che bloccano il collaudo confermativo</summary>
      <p>Dopo aver caricato la ricevuta della versione, apri il controllo dei prerequisiti esportato sul PC per la stessa cronologia. Il portale verifica che casi e tentativi corrispondano; la rilettura effettiva dei journal avviene soltanto sul PC. Piano preliminare, algoritmo e regole da approvare, indipendenza e riferimento nullo non attestati impediscono il collaudo confermativo.</p>
      <label>Controllo dei prerequisiti <input type="file" accept="application/json,.json"></label>
      <p role="status" aria-live="polite">Nessun controllo dei prerequisiti caricato per questa cronologia.</p>
      <div data-result></div>
    </details>
    <details data-dsg-triplet>
      <summary>Controlla la copertura tecnica delle tre immagini</summary>
      <p>Dopo la ricevuta del piano, carica la verifica BKL051_TRIPLET_TECHNICAL_V1 esportata sul PC. La copertura tecnica richiede un solo tentativo completato e ricontrollato per ognuna delle tre immagini distinte. Tentativi aggiuntivi o falliti restano visibili e non sono scartati per ottenere un risultato favorevole.</p>
      <label>Verifica della tripletta <input type="file" accept="application/json,.json"></label>
      <p role="status" aria-live="polite">Nessuna verifica della tripletta caricata per questa cronologia.</p>
      <div data-result></div>
      <p>Tre completamenti tecnici non validano il confronto fotometrico, la variabilità o il moto. Incertezza completa, significatività, qualificazione del controllo e risultato statistico restano separati e non disponibili in questa ricevuta diagnostica.</p>
    </details>
    <details data-dsg-plan-request>
      <summary>Prepara qualificazione, esito o revisione con evidenze</summary>
      <p>La richiesta viene salvata sul tuo PC e va applicata allo stesso piano con lo strumento locale. Non avvia analisi. Identità e data restano dichiarate; i documenti allegati non sono inviati in rete. Il file scaricato contiene le evidenze e va conservato in privato.</p>
      <label>Caso <select data-case></select></label>
      <label>Decisione dichiarata <select data-action>
        <option value="QUALIFICATION:DOCUMENTED_PENDING_REVIEW">Qualificazione documentata, da revisionare</option>
        <option value="QUALIFICATION:NON_EVALUABLE">Non valutabile</option>
        <option value="OUTCOME_REVIEW:NO_SIGNAL_DECLARED">Assenza di segnale dichiarata</option>
        <option value="OUTCOME_REVIEW:FALSE_ALERT_DECLARED">Falso allarme dichiarato</option>
        <option value="OUTCOME_REVIEW:INCONCLUSIVE">Esito inconcludente</option>
        <option value="OWNER_REVIEW:KEEP_FOR_REVIEW">Owner: conserva per revisione</option>
        <option value="OWNER_REVIEW:REJECT">Owner: respingi</option>
        <option value="OWNER_REVIEW:FOLLOW_UP">Owner: approfondisci</option>
      </select></label>
      <label>Identificativo locale del revisore (32 caratteri esadecimali) <input data-actor type="text" maxlength="32" autocomplete="off" spellcheck="false"></label>
      <label>Tentativo tecnico completato a cui riferire l’esito <select data-attempt></select></label>
      <p>Per documentare un controllo servono riferimento nullo, valutazione dell’indipendenza e motivazione. Per non valutabilità o revisione Owner basta la motivazione; per un esito serve il documento scientifico. Massimo 128 KiB per documento.</p>
      <label>Riferimento nullo <input type="file" data-evidence="NULL_REFERENCE"></label>
      <label>Valutazione dell’indipendenza <input type="file" data-evidence="INDEPENDENCE"></label>
      <label>Motivazione <input type="file" data-evidence="RATIONALE"></label>
      <label>Documento dell’esito scientifico <input type="file" data-evidence="SCIENTIFIC_OUTCOME"></label>
      <button type="button" disabled>Salva richiesta locale con evidenze</button>
      <p role="status" aria-live="polite">Nessuna richiesta registrata.</p>
    </details>
    <p>Il congelamento preliminare sul PC conserva una nuova versione e le impronte di algoritmo e regole senza sovrascrivere le precedenti. Per un derivato associato dal controllo locale, la ricevuta mostra la presenza della prova archiviata: originale e copia usata restano distinti. La calibrazione scientifica resta da attestare. Un’impronta importata non dimostra da sola i byte, l’identità dell’autore o la data di congelamento. Le dichiarazioni documentate restano da revisionare; non sono controlli indipendenti validati. Nessuna ricevuta può assegnare un test superato o un’approvazione scientifica.</p>
  </section>
  <section aria-label="Richiesta di analisi">
    <h2>Gruppo verificato sul PC</h2>
    <p>Scegli solo un gruppo già registrato e verificato sul computer. Il portale non legge le cartelle e non carica le immagini.</p>
    <label>Gruppo <select data-dsg-transients-group disabled></select></label>
    <p data-dsg-transients-group-details></p>
    <label><input type="checkbox" data-dsg-transients-verified disabled> Ho verificato sul PC immagine, riferimento, algoritmo e contratto di questo gruppo.</label>
    <button type="button" data-dsg-transients-create disabled>Richiedi analisi</button>
    <p data-dsg-transients-pending role="status" aria-live="polite"></p>
    <button type="button" data-dsg-transients-retry disabled>Ripeti la stessa richiesta</button>
  </section>
  <section aria-label="Stato delle analisi">
    <h2>Stato ed evidenze</h2>
    <button type="button" data-dsg-transients-refresh disabled>Aggiorna stato</button>
    <p data-dsg-transients-observed></p>
    <div data-dsg-transients-jobs></div>
  </section>
  <p>Per una recovery, verifica sul PC che il processo sia fermo e le evidenze conservate. La chiusura richiede la tua dichiarazione e l’impronta del dossier locale: conserva il tentativo incerto e consente solo un nuovo lavoro distinto.</p>
  <p>Il completamento tecnico non conferma un candidato o una scoperta. Le valutazioni già registrate dall’Owner restano dichiarazioni distinte dalla validazione scientifica. Il download contiene solo la ricevuta dello stato: non verifica i byte del rapporto locale.</p>
  <p><a href="../project/BKL-051-SCIENTIFIC-TRANSIENT-CANDIDATES-2026-10-07/">Stato e piano della funzione</a> · <a href="../pixinsight-pilot/">Elabora con PixInsight e IA</a></p>
  <noscript>La consultazione privata richiede JavaScript e l’accesso Owner.</noscript>
</div>


La [preparazione della concorrenza isolata](../project/BKL-051-S4-ISOLATED-CONCURRENCY-PREPARATION-2026-10-09.md) verifica soltanto due esecutori HTTP locali su storage sintetico. Autenticazione Google, GCS e attivazione dell’ambiente restano gate aperti.

<section data-dsg-case-workspace aria-label="Scheda unificata del caso">
  <h2>Dal piano al dossier</h2>
  <p>Apri una scheda esportata dal PC per consultare insieme piano, tentativi, confronto ed evidenze del dossier. Versioni diverse non vengono mescolate. Nessun file viene caricato in rete.</p>
  <label>Scheda del caso (JSON, massimo 1 MiB) <input type="file" accept="application/json,.json"></label>
  <p role="status" aria-live="polite">Nessuna scheda aperta.</p>
  <div data-result></div>
</section>

Per gli oggetti mobili, l’esportatore locale prepara anche un’anteprima ADES con identificativo assegnato dall’osservatore (`trkSub`), senza inventare un numero ufficiale. L’anteprima resta privata: non dimostra un’associazione valida o una scoperta e non viene inviata. Il controllo del formato è distinto dalle verifiche scientifiche e dal collaudo del servizio MPC. [Formato ADES del MPC](https://docs.minorplanetcenter.net/mpc-ops-docs/observations/ades-format/).
