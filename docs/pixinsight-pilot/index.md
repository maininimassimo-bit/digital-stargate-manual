<link rel="stylesheet" href="../styles/scientific-photo-upload.css">

<div class="dsg-photo-upload" data-piai-science>
  <h1>Elabora con PixInsight e IA</h1>
  <p>Il pilota usa i master M27 registrati sul tuo PC e l’assistente di questa sessione. L’avvio in PixInsight resta supervisionato. Nessuna nuova chiamata API IA a pagamento.</p>
  <p data-p5-message role="status">Accedi per preparare una richiesta.</p>
  <button type="button" data-p5-connect>Accedi con Google</button>
  <div data-p5-signin></div>
  <form data-p5-form>
    <fieldset disabled data-p5-fields>
      <legend>1. Prepara l’elaborazione</legend>
      <label>Master sul PC<select data-p5-input required></select></label>
      <label>Immagine di riferimento<select data-p5-parent><option value="">Nuova immagine</option></select></label>
      <p>La versione selezionata resta conservata. Il risultato sarà una nuova versione privata.</p>
      <label>Titolo<input data-p5-title required maxlength="160" value="M27 · elaborazione assistita"></label>
      <label>Data di elaborazione<input type="date" data-p5-date required></label>
      <p>Seleziona le sessioni di origine già importate.</p>
      <div data-p5-sessions></div>
      <label><input type="checkbox" data-p5-attest required>Confermo l’associazione dei master alle sessioni selezionate.</label>
      <p>Ricetta M27 LRGB non lineare: 29 operazioni e 15 checkpoint. La ricetta è specifica di questo campo e non certifica colori fotometrici.</p>
      <button type="submit" data-p5-create>Richiedi elaborazione</button>
    </fieldset>
  </form>
  <p data-p5-pending hidden></p>
  <button type="button" data-p5-retry hidden>Ripeti la stessa richiesta</button>
  <section aria-label="Richieste scientifiche"><h2>2. Stato delle elaborazioni</h2>
    <button type="button" data-p5-refresh disabled>Aggiorna stato</button>
    <div data-p5-jobs></div>
  </section>
  <section data-p5-review hidden aria-label="Revisione del risultato">
    <h2>3. Valuta il risultato privato</h2>
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
