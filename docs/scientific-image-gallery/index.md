<link rel="stylesheet" href="../styles/bkl-034-image-gallery.css">

<div class="dsg-image-gallery" data-session-photo-gallery>
  <section class="dsg-image-gallery__hero">
<!-- DSG:IMMERSIVE-SCENE -->
    <span class="dsg-image-gallery__kicker">DIGITAL STARGATE · IMMAGINI</span>
    <h1>Scientific Image Gallery</h1>
    <p>Immagini pubblicate con le loro sessioni di origine e i workflow disponibili.</p>
    <a href="../scientific-photo-upload/">Aggiungi foto e workflow · accesso riservato</a>
  </section>

  <section class="dsg-image-gallery__toolbar" aria-label="Filtri gallery">
    <label>Ricerca<input type="search" data-gallery-search placeholder="Titolo, sessione, oggetto…"></label>
    <button type="button" data-gallery-reset>Aggiorna e reimposta</button>
  </section>

  <div class="dsg-image-gallery__resultbar"><span data-gallery-count>Caricamento immagini…</span></div>
  <section class="dsg-image-gallery__grid" data-gallery-grid aria-live="polite"></section>

  <aside class="dsg-image-gallery__governance"><strong>Informazioni disponibili</strong><p>Le sessioni sono quelle dichiarate dall’autore. Un workflow parziale non dimostra l’esecuzione dei processi né certifica la qualità scientifica dell’immagine.</p></aside>
</div>

<section class="dsg-workflows" data-bkl049-workflows aria-labelledby="bkl049-title">
  <h2 id="bkl049-title">Workflow delle immagini</h2>
  <p>Ogni workflow disponibile è collegato a una precisa versione dell’immagine. I passaggi mancanti restano espliciti.</p>
  <button type="button" data-workflow-refresh>Aggiorna workflow</button>
  <p data-workflow-status role="status">Workflow non disponibile senza verifica dei dati.</p>
  <div data-workflow-body></div>
  <noscript>Per verificare e consultare i workflow occorre JavaScript. Nessun workflow è mostrato senza verifica.</noscript>
</section>
