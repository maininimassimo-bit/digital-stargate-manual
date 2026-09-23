<link rel="stylesheet" href="../styles/bkl-034-image-gallery.css">

<div class="dsg-image-gallery" data-bkl034-gallery data-source="../data/bkl034-scientific-image-gallery-fixture.json">
  <section class="dsg-image-gallery__hero">
    <span class="dsg-image-gallery__kicker">DIGITAL STARGATE · BKL-034</span>
    <h1>Scientific Image Gallery</h1>
    <p>Projection bounded e read-only delle immagini scientifiche collegate a sessione, target e processing provenance.</p>
    <div class="dsg-image-gallery__badges"><span>AUTHORITY · PROJECTION</span><span>COMMAND · NONE</span><span>SAFETY · NONE</span></div>
  </section>

  <section class="dsg-image-gallery__toolbar" aria-label="Filtri gallery">
    <label>Ricerca<input type="search" data-gallery-search placeholder="ID, sessione, target, provenance…"></label>
    <label>Stato<select data-gallery-state><option value="">Tutti gli stati</option><option value="observed">Observed</option><option value="stale">Stale</option><option value="unknown">Unknown</option><option value="unavailable">Unavailable</option></select></label>
    <button type="button" data-gallery-reset>Reimposta</button>
  </section>

  <div class="dsg-image-gallery__resultbar"><span data-gallery-count>Caricamento projection…</span><span>Fonte: fixture governata · read-only</span></div>
  <section class="dsg-image-gallery__grid" data-gallery-grid aria-live="polite"><article class="dsg-image-gallery__empty">Caricamento della gallery…</article></section>

  <aside class="dsg-image-gallery__governance"><strong>Limite di interpretazione</strong><p>Le card mostrano solo metadati e riferimenti della projection. Stati stale/unknown restano espliciti e non vengono trasformati in qualità, readiness, ranking o raccomandazioni.</p></aside>
</div>

<script src="../javascripts/bkl-034-image-gallery.js"></script>
