<link rel="stylesheet" href="../styles/intelligence-centers.css">

<div class="dsg-intelligence-center">

<section class="dsg-intelligence-hero">
  <span class="dsg-intelligence-kicker">DIGITAL STARGATE · SCIENTIFIC PLATFORM INTELLIGENCE</span>
  <h1>Stato pubblicato della piattaforma scientifica</h1>
  <p>
    Vista di sintesi su discovery, inventory, session importer, transfer, manifest,
    provenance e readiness dell’AP-013. I valori mostrati derivano dalla baseline
    versionata e non rappresentano telemetria runtime in tempo reale.
  </p>
  <div class="dsg-intelligence-actions">
    <a href="../scientific-platform/">Scientific Platform</a>
    <a href="../architecture/packages/AP-013-Scientific-Image-Repository-Architecture/">AP-013</a>
    <a href="../architecture/validation/AP-013-Session-Discovery-Execution-Evidence/">Discovery Evidence</a>
    <a href="../architecture/validation/AP-013-Transfer-Readiness-Gate/">Readiness Gate</a>
  </div>
</section>

<div class="dsg-intelligence-kpis">
  <article><span>DISCOVERY</span><strong>203 file</strong><small>11 sessioni osservate</small></article>
  <article><span>PARSING</span><strong>203 / 203</strong><small>0 ambiguous · 0 failed</small></article>
  <article><span>TRANSFER</span><strong>COPY_ONLY</strong><small>SHA-256 obbligatorio</small></article>
  <article><span>PILOT LIMIT</span><strong>1 file/run</strong><small>No overwrite · no cleanup</small></article>
</div>

<section class="dsg-intelligence-section">
  <span>PIPELINE STATUS</span>
  <h2>Capability AP-013</h2>
  <div class="dsg-intelligence-grid">
    <article class="is-green"><strong>Discovery</strong><p>Inventario sintetico completato su 203 file e 11 sessioni.</p><em>Validated</em></article>
    <article class="is-green"><strong>Filename Parsing</strong><p>Parsing deterministico completato senza elementi ambigui o falliti.</p><em>Validated</em></article>
    <article class="is-green"><strong>Transfer Primitives</strong><p>Staging, checksum e protezione della sorgente verificati con test automatici.</p><em>Validated</em></article>
    <article class="is-amber"><strong>Morning Scheduler</strong><p>Launcher protetto e attività giornaliera configurati sul PC Principale.</p><em>Limited pilot</em></article>
    <article class="is-amber"><strong>Unattended Evidence</strong><p>La prima esecuzione unattended resta da consolidare come evidenza formale.</p><em>Open</em></article>
    <article><strong>Catalog &amp; Knowledge Layer</strong><p>Catalogo persistente, lineage e knowledge graph appartengono alla successiva evoluzione M3.3.</p><em>Planned</em></article>
  </div>
</section>

<section class="dsg-intelligence-section">
  <span>SAFE TRANSFER BOUNDARY</span>
  <h2>Condizioni autorizzate</h2>
  <div class="dsg-intelligence-boundary">
    <article><strong>Source</strong><span>Read-only share EAGLE</span></article>
    <article><strong>Destination</strong><span>Root autorizzata e volume verificato</span></article>
    <article><strong>Integrity</strong><span>SHA-256 e manifest di evidenza</span></article>
    <article><strong>Window</strong><span>07:30–08:15</span></article>
  </div>
  <div class="dsg-intelligence-note">
    Bulk transfer, overwrite e source cleanup non sono autorizzati. La dashboard non modifica
    i gate e non abilita operazioni oltre il boundary definito dalla documentazione AP-013.
  </div>
</section>

<section class="dsg-intelligence-section">
  <span>EVIDENCE MAP</span>
  <h2>Documenti autorevoli</h2>
  <div class="dsg-intelligence-assets">
    <a href="../architecture/scientific-assets/AP13-W02-Current-State-Scientific-Asset-Inventory-Specification/"><strong>AP13-W02</strong><span>Current-State Asset Inventory</span></a>
    <a href="../architecture/scientific-assets/DSDM-001-Scientific-Data-Manager-Conceptual-Model/"><strong>DSDM-001</strong><span>Conceptual Model</span></a>
    <a href="../architecture/scientific-assets/DSDM-002-Scientific-Data-Manager-Logical-Data-Model/"><strong>DSDM-002</strong><span>Logical Data Model</span></a>
    <a href="../architecture/scientific-assets/DSDM-003-Contract-and-Manifest-Model/"><strong>DSDM-003</strong><span>Contract and Manifest</span></a>
    <a href="../architecture/scientific-assets/DSDM-004-Session-Importer-Architecture-and-Safe-Transfer-Design/"><strong>DSDM-004</strong><span>Session Importer</span></a>
    <a href="../architecture/validation/AP-013-Transfer-Readiness-Gate/"><strong>Gate</strong><span>Transfer Readiness</span></a>
  </div>
</section>

<section class="dsg-intelligence-section">
  <span>M3.3 DIRECTION</span>
  <h2>Scientific Data Platform</h2>
  <div class="dsg-intelligence-next">
    <article><strong>Session Catalog</strong><p>Identità persistenti, ricerca e vista completa delle sessioni.</p></article>
    <article><strong>Knowledge Graph</strong><p>Relazioni tra target, osservazioni, dataset, processing e pubblicazioni.</p></article>
    <article><strong>Data Lineage</strong><p>Catena completa dai RAW ai prodotti finali e alle evidenze.</p></article>
    <article><strong>Scientific Analytics</strong><p>Qualità, integrazione, strumenti, filtri e crescita del patrimonio.</p></article>
  </div>
</section>

</div>
