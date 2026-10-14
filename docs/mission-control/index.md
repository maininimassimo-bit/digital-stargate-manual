<link rel="stylesheet" href="../styles/mission-control.css">

<div class="dsg-mission-control" data-mission-control data-session-catalog="../data/scientific-session-catalog.json">

<section class="dsg-mission-hero">
<!-- DSG:IMMERSIVE-SCENE -->
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
    <a href="../bkl042-chat/">AI Observatory Assistant</a>
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
      <div><span>AP-013 PIPELINE</span><h2>Baseline documentata</h2></div>
    </div>
    <p class="dsg-mission-lineage-status" data-mission-pipeline-status>Verifica della baseline documentata…</p>
    <div class="dsg-mission-status" data-mission-pipeline></div>
    <p class="dsg-mission-lineage-status"><a href="../architecture/validation/AP-013-Session-Discovery-Execution-Evidence/">Discovery storica</a> · <a href="../architecture/validation/AP-013-Operational-Acceptance/">Acceptance e vincoli</a></p>
  </article>

  <article class="dsg-mission-panel">
    <div class="dsg-mission-panel__heading">
      <div><span>OBSERVATORY OVERVIEW</span><h2>Boundary operativo</h2></div>
    </div>
    <p class="dsg-mission-lineage-status" data-mission-boundary-status>Verifica dei vincoli documentati…</p>
    <div class="dsg-mission-status" data-mission-boundary></div>
    <p class="dsg-mission-lineage-status"><a href="../architecture/validation/AP-013-Morning-Transfer-Scheduler-Evidence/">Orari e finestra: evidenza storica dello scheduler</a></p>
  </article>

  <article class="dsg-mission-panel dsg-mission-panel--wide">
    <div class="dsg-mission-panel__heading">
      <div><span>KNOWLEDGE &amp; LINEAGE</span><h2>Copertura corrente</h2></div>
      <a href="../scientific-platform-intelligence/">Apri intelligence →</a>
    </div>
    <button type="button" data-mission-refresh>Aggiorna copertura</button>
    <p class="dsg-mission-lineage-status" role="status" data-mission-lineage-status>Caricamento delle fonti correnti…</p>
    <div class="dsg-mission-knowledge" data-mission-knowledge><p>Verifica della copertura in corso…</p></div>
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
<script src="../javascripts/scientific-photo-api.js"></script>
<script src="../javascripts/mission-control-lineage.js"></script>
<script src="../javascripts/mission-control.js"></script>
