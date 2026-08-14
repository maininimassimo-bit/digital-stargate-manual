<link rel="stylesheet" href="../styles/scientific-session-detail.css">

<div class="dsg-session-detail" data-session-detail data-session-catalog="../data/scientific-session-catalog.json">
  <section class="dsg-session-detail__hero">
    <span>DIGITAL STARGATE · SESSION DETAIL</span>
    <h1 data-detail-title>Caricamento sessione…</h1>
    <p data-detail-subtitle>Recupero dei metadati dal catalogo versionato.</p>
    <div class="dsg-session-detail__actions">
      <a href="../scientific-session-catalog/">← Torna al Catalogo</a>
      <a href="../scientific-platform/">Scientific Platform</a>
      <a href="../scientific-platform-intelligence/">Scientific Intelligence</a>
    </div>
  </section>

  <section class="dsg-session-detail__summary" data-detail-summary></section>

  <section class="dsg-session-detail__section">
    <span>SESSION OVERVIEW</span><h2>Metadati principali</h2><div class="dsg-session-detail__grid" data-detail-metadata></div>
  </section>

  <section class="dsg-session-detail__section">
    <span>WEATHER CONDITIONS</span><h2>Condizioni meteo della sessione</h2>
    <div class="dsg-session-weather" data-detail-weather></div><div class="dsg-session-weather-detail" data-detail-weather-detail></div>
    <div class="dsg-session-weather-chart" data-detail-weather-chart hidden><div class="dsg-session-weather-chart__legend"><span>Temperatura</span><span>Umidità</span><span>Dew point</span></div><svg viewBox="0 0 1000 260" role="img" aria-label="Andamento meteo CloudWatcher della sessione" data-detail-weather-svg></svg></div>
    <p class="dsg-session-detail__note" data-detail-weather-note></p>
  </section>

  <section class="dsg-session-detail__section">
    <span>GUIDING PERFORMANCE</span><h2>Andamento guida della sessione</h2>
    <div class="dsg-session-guiding" data-detail-guiding></div>
    <div class="dsg-session-guiding-chart" data-detail-guiding-chart hidden><div class="dsg-session-guiding-chart__legend"><span>RA</span><span>DEC</span><span>Errore totale</span></div><svg viewBox="0 0 1000 280" role="img" aria-label="Andamento guida PHD2 della sessione" data-detail-guiding-svg></svg></div>
    <p class="dsg-session-detail__note" data-detail-guiding-note></p>
  </section>

  <section class="dsg-session-detail__section">
    <span>KNOWLEDGE GRAPH</span><h2>Relazioni della sessione</h2><div class="dsg-session-graph" data-detail-graph></div>
    <p class="dsg-session-detail__note">Il grafo rappresenta soltanto relazioni presenti nel catalogo attuale. Manifest, transfer, processing e publication restano esplicitamente non rappresentati quando non disponibili.</p>
  </section>

  <section class="dsg-session-detail__section"><span>DATA LINEAGE</span><h2>Catena informativa corrente</h2><div class="dsg-session-lineage" data-detail-lineage></div></section>
  <section class="dsg-session-detail__section"><span>EVIDENCE &amp; SOURCES</span><h2>Collegamenti autorevoli</h2><div class="dsg-session-detail__sources" data-detail-sources></div></section>
  <section class="dsg-session-detail__error" data-detail-error hidden></section>
</div>

<script src="../javascripts/scientific-data-engine.js"></script>
<script src="../javascripts/scientific-session-detail.js"></script>
