<link rel="stylesheet" href="../styles/scientific-platform-center.css">

<div class="dsg-scientific-center">

<section class="dsg-scientific-hero">
  <span class="dsg-scientific-hero__eyebrow">DIGITAL STARGATE · SCIENTIFIC PLATFORM</span>
  <h1>Scientific Platform Center</h1>
  <p>
    Dashboard documentale dell’AP-013 per repository scientifico, asset registry,
    session importer, metadati, checksum, provenance e trasferimento protetto.
    I dati mostrati rappresentano l’ultima baseline pubblicata, non telemetria runtime.
  </p>
  <div class="dsg-scientific-actions">
    <a href="../architecture/packages/AP-013-Scientific-Image-Repository-Architecture/">AP-013 Architecture</a>
    <a href="../architecture/scientific-assets/DSDM-004-Session-Importer-Architecture-and-Safe-Transfer-Design/">Session Importer</a>
    <a href="../architecture/validation/AP-013-Transfer-Readiness-Gate/">Readiness Gate</a>
    <a href="../architecture/validation/AP-013-Session-Discovery-Execution-Evidence/">Discovery Evidence</a>
  </div>
</section>

<div class="dsg-scientific-kpis">
  <div class="dsg-scientific-kpi"><span>DISCOVERY</span><strong>203 file</strong><small>11 sessioni rilevate</small></div>
  <div class="dsg-scientific-kpi"><span>PARSE QUALITY</span><strong>100%</strong><small>203 parsed · 0 ambiguous · 0 failed</small></div>
  <div class="dsg-scientific-kpi"><span>TRANSFER MODE</span><strong>COPY_ONLY</strong><small>SHA-256 obbligatorio</small></div>
  <div class="dsg-scientific-kpi"><span>PILOT LIMIT</span><strong>1 file/run</strong><small>No overwrite · no cleanup</small></div>
</div>

<section class="dsg-scientific-section">
  <span>PLATFORM CAPABILITIES</span>
  <h2>Componenti della piattaforma scientifica</h2>
  <div class="dsg-scientific-grid">
    <article class="dsg-scientific-card">
      <strong>Scientific Binary Storage</strong>
      <p>Conservazione esterna dei RAW, calibration frame, intermedi e prodotti finali. GitHub non è lo storage primario dei binari voluminosi.</p>
      <a href="../architecture/packages/AP-013-Scientific-Image-Repository-Architecture/">Apri AP-013 →</a>
    </article>
    <article class="dsg-scientific-card">
      <strong>Scientific Asset Registry</strong>
      <p>Identificatori stabili, classificazione, checksum, dimensione, locator e stato di integrità.</p>
      <a href="../architecture/scientific-assets/DSDM-002-Scientific-Data-Manager-Logical-Data-Model/">Logical Data Model →</a>
    </article>
    <article class="dsg-scientific-card">
      <strong>Observation Context</strong>
      <p>Collegamento tra target, sessione, strumenti, configurazione e condizioni osservative.</p>
      <a href="../architecture/scientific-assets/DSDM-001-Scientific-Data-Manager-Conceptual-Model/">Conceptual Model →</a>
    </article>
    <article class="dsg-scientific-card">
      <strong>Processing Provenance</strong>
      <p>Workflow, processing run, input, output, ambiente e relazioni di derivazione.</p>
      <a href="../architecture/scientific-assets/DSDM-003-Contract-and-Manifest-Model/">Contract &amp; Manifest →</a>
    </article>
    <article class="dsg-scientific-card">
      <strong>Session Importer</strong>
      <p>Discovery, parsing deterministico, piano di trasferimento e copy staging verificato.</p>
      <a href="../architecture/scientific-assets/DSDM-004-Session-Importer-Architecture-and-Safe-Transfer-Design/">Importer Architecture →</a>
    </article>
    <article class="dsg-scientific-card">
      <strong>Integrity &amp; Preservation</strong>
      <p>SHA-256, immutabilità RAW, retention, backup, restore e media migration governata.</p>
      <a href="../architecture/validation/AP-013-Transfer-Readiness-Gate/">Readiness Gate →</a>
    </article>
  </div>
</section>

<section class="dsg-scientific-section">
  <span>DATA LIFECYCLE</span>
  <h2>Lifecycle governato degli asset</h2>
  <div class="dsg-scientific-flow">
    identified → ingested → integrity-verified → classified → linked → preserved → processed → derived → quality-reviewed → published | retained
  </div>
  <p>
    La cancellazione non è uno stato ordinario. Ogni modifica di stato richiede attore,
    precondizioni, timestamp, asset interessato, evidence reference e comportamento in errore.
  </p>
</section>

<section class="dsg-scientific-section">
  <span>SAFE TRANSFER</span>
  <h2>Boundary operativo del limited pilot</h2>
  <div class="dsg-scientific-status-grid">
    <article><span>SORGENTE</span><strong>EAGLE NINA Images</strong><small>Accesso read-only tramite credenziale protetta</small></article>
    <article><span>DESTINAZIONE</span><strong>Scientific Archive</strong><small>Root autorizzata e volume verificato</small></article>
    <article><span>INTEGRITÀ</span><strong>SHA-256</strong><small>Staging, verifica e manifest di evidenza</small></article>
    <article><span>SCHEDULER</span><strong>07:30</strong><small>Finestra mattutina e launcher protetto</small></article>
  </div>
  <div class="dsg-scientific-warning">
    <strong>Safety boundary:</strong> overwrite, bulk transfer, modifica dei RAW e cancellazione della sorgente non sono autorizzati.
  </div>
</section>

<section class="dsg-scientific-section">
  <span>DOCUMENTATION MAP</span>
  <h2>Baseline tecnica pubblicata</h2>
  <div class="dsg-scientific-docs">
    <a href="../architecture/scientific-assets/AP13-W02-Current-State-Scientific-Asset-Inventory-Specification/"><strong>AP13-W02</strong><span>Current-State Scientific Asset Inventory</span></a>
    <a href="../architecture/scientific-assets/DSDM-001-Scientific-Data-Manager-Conceptual-Model/"><strong>DSDM-001</strong><span>Conceptual Model</span></a>
    <a href="../architecture/scientific-assets/DSDM-002-Scientific-Data-Manager-Logical-Data-Model/"><strong>DSDM-002</strong><span>Logical Data Model</span></a>
    <a href="../architecture/scientific-assets/DSDM-003-Contract-and-Manifest-Model/"><strong>DSDM-003</strong><span>Contract and Manifest Model</span></a>
    <a href="../architecture/scientific-assets/DSDM-004-Session-Importer-Architecture-and-Safe-Transfer-Design/"><strong>DSDM-004</strong><span>Session Importer and Safe Transfer</span></a>
    <a href="../architecture/scientific-assets/evidence/AP13-W02/E-AP13-W02-01-Source-Authorization-and-Scope-Record/"><strong>E-AP13-W02-01</strong><span>Source Authorization and Scope</span></a>
    <a href="../architecture/validation/AP-013-Session-Discovery-Execution-Evidence/"><strong>Evidence</strong><span>Session Discovery Execution</span></a>
    <a href="../architecture/validation/AP-013-Transfer-Readiness-Gate/"><strong>Gate</strong><span>Transfer Readiness</span></a>
  </div>
</section>

<section class="dsg-scientific-section">
  <span>NEXT EVOLUTION</span>
  <h2>Verso M3.3 e AP-014</h2>
  <div class="dsg-scientific-next">
    <article><strong>Persistent Asset Identity</strong><p>Identificatori indipendenti dal path fisico e catalogo degli asset.</p></article>
    <article><strong>Manifest &amp; Metadata</strong><p>Contratti machine-readable, checksum e metadata governati.</p></article>
    <article><strong>Observation Catalog</strong><p>Boundary verso AP-014 per indicizzazione, ricerca e discovery.</p></article>
    <article><strong>Repository Intelligence</strong><p>Crescita, integrità, capacity e qualità del patrimonio scientifico.</p></article>
  </div>
</section>

</div>
