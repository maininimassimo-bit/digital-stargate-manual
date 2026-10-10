<link rel="stylesheet" href="../styles/scientific-photo-upload.css">

<div class="dsg-photo-upload" data-piai-science>
  <h1>Elabora con PixInsight e IA</h1>
  <p>Indica l’oggetto, le cartelle dei master e il risultato desiderato. Puoi richiedere un piano OpenAI direttamente da questa pagina quando il servizio è attivo, oppure usare l’assistenza della chat. Confermi sempre il piano prima di creare l’elaborazione. L’avvio in PixInsight sul PC resta supervisionato.</p>
  <p data-p5-message role="status">Accedi per preparare una richiesta.</p>
  <button type="button" data-p5-connect>Accedi con Google</button>
  <div data-p5-signin></div>
  <form data-p5-form>
    <fieldset disabled data-p5-fields>
      <legend>1. Prepara l’elaborazione</legend>
      <label>Pianificazione<select data-p5-planning-mode><option value="SESSION_ASSISTED">Con l’assistente della chat</option><option value="OPENAI_API" data-p5-openai-option disabled>OpenAI dalla pagina · disponibilità da verificare</option></select></label>
      <div data-p5-openai-consent-label hidden>
        <label><input type="checkbox" data-p5-openai-consent>Autorizzo l’invio a OpenAI del testo della richiesta, dell’oggetto e dei metadati minimi dei master per generare un piano.</label>
        <p>La richiesta API può avere un costo. Immagini, percorsi e hash dei singoli file non vengono inviati a OpenAI. Non inserire password, chiavi, percorsi o dati personali nel testo. Il servizio effettua al massimo una chiamata per richiesta, con un limite giornaliero configurato.</p>
      </div>
      <label>Origine dei master<select data-p5-origin><option value="CATALOG">Sessioni già importate</option><option value="HISTORICAL">Riprese storiche senza sessioni nel portale</option></select></label>
      <label data-p5-catalog-label>Oggetto delle sessioni importate<select data-p5-target required></select></label>
      <div data-p5-historical-fields hidden>
        <label>Oggetto dei master storici<input data-p5-historical-target maxlength="160" placeholder="M31"></label>
        <label>Provenienza delle riprese storiche<textarea data-p5-provenance rows="3" maxlength="2000" placeholder="Descrivi l’origine dei master e ciò che conosci delle riprese. Non occorre inventare date o sessioni."></textarea></label>
        <label><input type="checkbox" data-p5-historical-attest>Confermo la provenienza dichiarata; le sessioni non sono importate nel portale.</label>
        <p>Nome e provenienza restano dichiarazioni private. Non vengono create sessioni, associazioni al catalogo o immagini pubblicate.</p>
      </div>
      <label>Tipo di master<select data-p5-mode><option value="LRGB">LRGB · L, R, G e B monocromatici</option><option value="OSC">OSC · master RGB già debayerizzato</option><option value="OSC_CFA">OSC · master CFA da debayerizzare</option><option value="SHO">Banda stretta SHO · SII, Hα e OIII</option><option value="HOO">Banda stretta HOO · Hα e OIII</option></select></label>
      <label data-p5-bayer-label hidden>Schema Bayer dichiarato<select data-p5-bayer><option value="">Seleziona lo schema verificato</option><option>RGGB</option><option>BGGR</option><option>GBRG</option><option>GRBG</option></select></label>
      <label>Composizione<select data-p5-layout><option value="SINGLE">Campo singolo</option><option value="PANELS">Mosaico · pannelli da unire</option></select></label>
      <label>Cartella dei master sul PC<input data-p5-directory required maxlength="500" placeholder="F:\Astrofotografia\M27\Master" autocomplete="off"></label>
      <p>Inserisci il percorso completo della cartella contenente i master XISF. I pannelli del mosaico possono trovarsi anche nella stessa cartella. Il browser non apre le cartelle: l’assistente le verifica sul PC. Percorsi e prompt sono conservati nel servizio privato Owner; i master restano sul PC.</p>
      <label data-p5-additional-label hidden>Altre cartelle dei pannelli, se presenti<textarea data-p5-additional rows="3" maxlength="8000" placeholder="Un percorso completo per riga. Lascia vuoto se tutti i pannelli sono nella cartella indicata sopra."></textarea></label>
      <label data-p5-parent-label>Immagine di riferimento<select data-p5-parent><option value="">Nuova immagine</option></select></label>
      <p>La versione selezionata resta conservata. Il risultato sarà una nuova versione privata.</p>
      <label>Titolo<input data-p5-title required maxlength="160" placeholder="Oggetto · elaborazione assistita"></label>
      <label>Data di elaborazione<input type="date" data-p5-date required></label>
      <div data-p5-session-fields>
      <p>Seleziona le sessioni di origine già importate.</p>
      <div data-p5-sessions></div>
      <label><input type="checkbox" data-p5-attest required>Confermo l’associazione dei master alle sessioni selezionate.</label>
      </div>
      <label>Come vuoi elaborare i master?<textarea data-p5-prompt required maxlength="4000" rows="5" placeholder="Vorrei un risultato non lineare con dettaglio fine, colori equilibrati, stelle contenute e fondo naturale. Per un mosaico indica anche le preferenze sui filtri e sui pannelli."></textarea></label>
      <p>Descrivi il risultato desiderato. L’assistente verifica i master e propone il piano adatto al campo. Per i mosaici confermi prima la selezione dei pannelli; per mosaici e master CFA confermi poi la preparazione. L’elaborazione finale richiede una conferma separata del suo piano. Il risultato resta privato fino alla tua decisione.</p>
      <button type="submit" data-p5-create>Invia cartella e prompt</button>
    </fieldset>
  </form>
  <p data-p5-pending hidden></p>
  <button type="button" data-p5-retry hidden>Ripeti la stessa richiesta</button>
  <section aria-label="Piani di elaborazione"><h2>2. Verifica e conferma il piano</h2>
    <p>Con OpenAI dalla pagina, il collegamento di pianificazione attivo sul PC verifica i master nei campi già configurati e il servizio propone il piano. Premi «Aggiorna stato» per consultarlo. Per un nuovo campo occorre prima verificare la regione di fondo e la configurazione locale; per CFA e mosaici occorre completare la preparazione approvata. Con la modalità chat, comunica all’assistente che hai inviato la richiesta. Bias, dark, mappe di rigetto e varianti drizzle non vengono scelti tacitamente.</p>
    <div data-p5-plans></div>
  </section>
  <section aria-label="Richieste scientifiche"><h2>3. Stato delle elaborazioni</h2>
    <button type="button" data-p5-refresh disabled>Aggiorna stato</button>
    <div data-p5-jobs></div>
  </section>
  <section data-p5-review hidden aria-label="Revisione del risultato">
    <h2>4. Valuta il risultato privato</h2>
    <div data-p5-summary></div>
    <img data-p5-preview alt="Anteprima privata del risultato PixInsight" style="max-width:100%">
    <div data-p5-steps></div>
    <button type="button" data-p5-workflow>Scarica workflow</button>
    <button type="button" data-p5-correlations>Scarica correlazioni runtime</button>
    <button type="button" data-p5-receipt>Scarica collegamenti e ricevuta</button>
    <button type="button" data-p5-accept>Accetta come risultato privato</button>
    <button type="button" data-p5-reject>Richiedi una nuova elaborazione</button>
    <p>L’originale XISF resta sul tuo PC. L’accettazione conserva il risultato privato; la pubblicazione richiede la procedura separata di verifica foto e workflow.</p>
    <a href="../scientific-photo-upload/">Apri caricamento foto e workflow</a>
  </section>
  <noscript>La procedura richiede JavaScript e l’accesso Owner.</noscript>
</div>
