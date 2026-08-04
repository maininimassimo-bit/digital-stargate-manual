<link rel="stylesheet" href="../styles/scientific-session-explorer.css">

<div class="dsg-session-explorer" data-session-catalog="../data/scientific-session-catalog.json">

<section class="dsg-session-hero">
  <span class="dsg-session-kicker">DIGITAL STARGATE · SCIENTIFIC SESSION CATALOG</span>
  <h1>Esplora le sessioni scientifiche</h1>
  <p>
    Catalogo navigabile costruito sui dataset versionati del repository. Le schede presentano
    una vista sintetica; metriche sorgente, documentazione ed evidenze restano autorevoli.
  </p>
  <div class="dsg-session-hero__actions">
    <a href="../scientific-platform/">Scientific Platform</a>
    <a href="../scientific-platform-intelligence/">Scientific Intelligence</a>
    <a href="../architecture/validation/AP-013-Session-Discovery-Execution-Evidence/">Discovery Evidence</a>
  </div>
</section>

<section class="dsg-session-kpis" data-session-kpis aria-live="polite">
  <article><span>SESSIONI</span><strong>—</strong><small>nel catalogo versionato</small></article>
  <article><span>TARGET</span><strong>—</strong><small>oggetti distinti</small></article>
  <article><span>INTEGRAZIONE</span><strong>—</strong><small>ore complessive</small></article>
  <article><span>QUALITÀ</span><strong>—</strong><small>sessioni validate</small></article>
</section>

<section class="dsg-session-toolbar" aria-label="Filtri catalogo">
  <label>
    <span>Ricerca</span>
    <input type="search" placeholder="Sessione, target, telescopio, camera…" data-session-search>
  </label>
  <label>
    <span>Anno</span>
    <select data-session-year><option value="">Tutti</option></select>
  </label>
  <label>
    <span>Target</span>
    <select data-session-target><option value="">Tutti</option></select>
  </label>
  <label>
    <span>Qualità</span>
    <select data-session-quality>
      <option value="">Tutte</option>
      <option value="VALIDATED_ANALYTICS">Validated</option>
      <option value="ATTENTION_REQUIRED">Attention required</option>
    </select>
  </label>
  <button type="button" data-session-reset>Reimposta</button>
</section>

<div class="dsg-session-resultbar">
  <span data-session-count>Caricamento catalogo…</span>
  <span>Fonte: dataset versionati · stato non real-time</span>
</div>

<section class="dsg-session-grid" data-session-grid aria-live="polite">
  <article class="dsg-session-empty">Caricamento delle sessioni in corso…</article>
</section>

<aside class="dsg-session-governance">
  <strong>Regola di governance</strong>
  <p>
    Il Catalogo non certifica automaticamente manifest, transfer o publication state.
    Quando tali stati non sono rappresentati nei dataset sorgente vengono mostrati come non disponibili.
  </p>
</aside>

</div>

<script src="../javascripts/scientific-session-explorer.js"></script>
