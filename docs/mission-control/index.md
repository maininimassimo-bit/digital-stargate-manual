<link rel="stylesheet" href="../styles/mission-control.css">

<div class="dsg-mission-control" data-mission-control data-session-catalog="../data/scientific-session-catalog.json">

<section class="dsg-mission-hero">
  <span class="dsg-mission-kicker">DIGITAL STARGATE · MISSION CONTROL</span>
  <h1>Centro di controllo della piattaforma scientifica</h1>
  <p>
    Vista unificata sul patrimonio osservativo, sulle proiezioni scientifiche pubblicate
    e sui principali servizi documentali. I dati derivano dalle fonti versionate del repository
    e non rappresentano telemetria live dell’osservatorio.
  </p>
  <div class="dsg-mission-actions">
    <a href="../scientific-session-catalog/">Session Explorer</a>
    <a href="../scientific-platform-intelligence/">Scientific Intelligence</a>
    <a href="../operations/">Operations Center</a>
    <a href="../documentation/">Documentation Center</a>
  </div>
</section>

<section class="dsg-mission-kpis" data-mission-kpis aria-live="polite">
  <article><span>SESSIONI</span><strong>—</strong><small>catalogo versionato</small></article>
  <article><span>TARGET</span><strong>—</strong><small>oggetti distinti</small></article>
  <article><span>INTEGRAZIONE</span><strong>—</strong><small>ore complessive</small></article>
  <article><span>QUALITÀ</span><strong>—</strong><small>sessioni validate</small></article>
</section>

<section class="dsg-mission-grid">
  <article class="dsg-mission-panel dsg-mission-panel--wide">
    <div class="dsg-mission-panel__heading">
      <div><span>SCIENTIFIC OPERATIONS</span><h2>Sessioni recenti</h2></div>
      <a href="../scientific-session-catalog/">Apri catalogo →</a>
    </div>
    <div class="dsg-mission-recent" data-mission-recent>
      <p>Caricamento delle sessioni…</p>
    </div>
  </article>

  <article class="dsg-mission-panel">
    <div class="dsg-mission-panel__heading">
      <div><span>AP-013 PIPELINE</span><h2>Stato pubblicato</h2></div>
    </div>
    <div class="dsg-mission-status">
      <div><span>Discovery</span><strong class="is-green">Validated</strong></div>
      <div><span>Filename parsing</span><strong class="is-green">203 / 203</strong></div>
      <div><span>Transfer mode</span><strong class="is-amber">COPY_ONLY</strong></div>
      <div><span>Pilot boundary</span><strong class="is-amber">1 file / run</strong></div>
      <div><span>Overwrite</span><strong>Disabled</strong></div>
      <div><span>Source cleanup</span><strong>Disabled</strong></div>
    </div>
  </article>

  <article class="dsg-mission-panel">
    <div class="dsg-mission-panel__heading">
      <div><span>OBSERVATORY OVERVIEW</span><h2>Boundary operativo</h2></div>
    </div>
    <div class="dsg-mission-status">
      <div><span>Safety</span><strong class="is-green">Local independent</strong></div>
      <div><span>Transfer window</span><strong>07:30–08:15</strong></div>
      <div><span>Integrity</span><strong>SHA-256</strong></div>
      <div><span>Telemetry</span><strong class="is-muted">Not live</strong></div>
    </div>
  </article>

  <article class="dsg-mission-panel dsg-mission-panel--wide">
    <div class="dsg-mission-panel__heading">
      <div><span>KNOWLEDGE &amp; LINEAGE</span><h2>Copertura corrente</h2></div>
      <a href="../scientific-platform-intelligence/">Apri intelligence →</a>
    </div>
    <div class="dsg-mission-knowledge">
      <article><strong>Target</strong><span>Rappresentato</span></article>
      <article><strong>Sessione</strong><span>Rappresentata</span></article>
      <article><strong>Equipment</strong><span>Rappresentato</span></article>
      <article><strong>Metrics</strong><span>Rappresentate</span></article>
      <article class="is-partial"><strong>Scientific assets</strong><span>Parziale</span></article>
      <article class="is-missing"><strong>Manifest</strong><span>Non rappresentato</span></article>
      <article class="is-missing"><strong>Processing</strong><span>Non rappresentato</span></article>
      <article class="is-missing"><strong>Publication</strong><span>Non rappresentata</span></article>
    </div>
  </article>
</section>

<section class="dsg-mission-centers">
  <span class="dsg-mission-kicker">PLATFORM ACCESS</span>
  <h2>Centri e servizi</h2>
  <div>
    <a href="../documentation/"><strong>Documentation Center</strong><span>Patrimonio documentale</span></a>
    <a href="../roadmap/"><strong>Roadmap Center</strong><span>Programma e milestone</span></a>
    <a href="../architecture/"><strong>Architecture Center</strong><span>Package, ADR e governance</span></a>
    <a href="../scientific-platform/"><strong>Scientific Platform</strong><span>AP-013 e DSDM</span></a>
    <a href="../operations/"><strong>Operations Center</strong><span>SOP, safety e recovery</span></a>
    <a href="../repository-analytics/"><strong>Repository Analytics</strong><span>Metriche e maturità</span></a>
  </div>
</section>

<aside class="dsg-mission-note">
  <strong>Interpretazione</strong>
  <p>
    Mission Control aggrega viste e metriche pubblicate. Non abilita comandi remoti e non sostituisce
    safety locale, review, evidence o readiness gate.
  </p>
</aside>

</div>

<script src="../javascripts/scientific-data-engine.js"></script>
<script src="../javascripts/mission-control.js"></script>
