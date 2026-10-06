<link rel="stylesheet" href="../styles/scientific-photo-upload.css">

<div class="dsg-photo-upload" data-photo-upload>
  <h1>Aggiungi foto e workflow</h1>
  <p>Aggiungi un’immagine da sessioni già importate oppure da riprese storiche. L’originale e il file del workflow restano privati. Potrai pubblicare l’anteprima dopo averla verificata.</p>
  <p data-photo-status role="status">Verifica del servizio di caricamento…</p>
  <div data-photo-signin></div>
  <form data-photo-form>
    <fieldset disabled data-photo-fields>
      <legend>1. Origine delle riprese</legend>
      <label>Origine<select data-photo-origin><option value="IMPORTED">Sessioni già importate</option><option value="HISTORICAL">Riprese storiche senza sessioni nel portale</option></select></label>
      <div data-photo-imported-fields>
        <label>Oggetto osservato<select data-photo-target required></select></label>
        <p>Se l’immagine combina più notti, seleziona tutte le sessioni di origine.</p>
        <div data-photo-sessions></div>
      </div>
      <div data-photo-historical-fields hidden>
        <label>Oggetto delle riprese storiche<input data-photo-historical-target maxlength="160"></label>
        <label>Provenienza delle riprese<textarea data-photo-provenance maxlength="2000"></textarea></label>
        <p>Descrivi l’origine delle riprese. Questa dichiarazione resta privata. Nella gallery comparirà soltanto che le riprese sono storiche, senza sessioni importate.</p>
        <label class="dsg-photo-upload__check"><input type="checkbox" data-photo-historical-attest>Confermo l’oggetto e la provenienza dichiarati; le sessioni di queste riprese non sono presenti nel portale.</label>
      </div>
      <label>Versione<select data-photo-version><option value="">Nuova immagine</option></select></label>
      <label>Titolo<input data-photo-title required maxlength="160"></label>
      <label>Data di elaborazione<input type="date" data-photo-date required></label>
      <p>La data di elaborazione è distinta dalle date delle riprese.</p>
      <h2>2. File</h2>
      <label>Originale finale privato · XISF o FITS (massimo 1 GiB)<input type="file" data-photo-original accept=".xisf,.fits,.fit" required></label>
      <label>Anteprima · JPEG o PNG (massimo 32 MiB)<input type="file" data-photo-preview accept=".jpg,.jpeg,.png" required></label>
      <label>Workflow PixInsight esportato · JavaScript (massimo 2 MiB)<input type="file" data-photo-workflow accept=".js,.txt" required></label>
      <p>Il workflow viene letto e conservato, senza eseguire i processi. Se il formato non è supportato, il file resta archiviato e i passaggi sono indicati come non disponibili.</p>
      <label class="dsg-photo-upload__check"><input type="checkbox" data-photo-attest required><span data-photo-attest-label>Confermo che l’anteprima deriva dall’originale e che le sessioni selezionate sono quelle di origine.</span></label>
      <button type="submit">Carica e verifica</button>
    </fieldset>
  </form>
  <progress data-photo-progress max="100" value="0" hidden aria-label="Avanzamento del caricamento"></progress>
  <button type="button" data-photo-new hidden>Inizia un nuovo caricamento</button>
  <section data-photo-review hidden aria-label="Revisione prima del salvataggio">
    <h2>3. Verifica e salva</h2>
    <div data-photo-summary></div>
    <img data-photo-review-image alt="Anteprima ripulita dai metadati per la pubblicazione" hidden>
    <p>Il workflow mostra le configurazioni presenti nell’esportazione, in ordine. La storia può essere parziale e non prova l’esecuzione dei processi.</p>
    <p>Per impostazione iniziale vengono pubblicati solo i nomi dei processi. Seleziona singolarmente i parametri che vuoi rendere pubblici.</p>
    <div data-photo-steps></div>
    <div data-photo-public-review></div>
    <label class="dsg-photo-upload__check"><input type="checkbox" data-photo-rights>Confermo di avere il diritto di pubblicare l’anteprima e i campi selezionati.</label>
    <button type="button" data-photo-save>Salva privato</button>
    <button type="button" data-photo-recheck>Ripeti controlli</button>
    <button type="button" data-photo-publish disabled>Salva e pubblica</button>
    <p>La pubblicazione resterà visibile fino al ritiro esplicito. L’originale e il workflow sorgente non vengono pubblicati.</p>
  </section>
  <section aria-label="I tuoi caricamenti"><h2>Archivio privato e versioni</h2><div data-photo-archive>Accedi per consultare il tuo archivio.</div></section>
  <noscript>Il caricamento richiede JavaScript e l’accesso al tuo account Google.</noscript>
</div>
