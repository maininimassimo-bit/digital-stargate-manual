<link rel="stylesheet" href="../styles/scientific-platform-center.css">
<script src="../javascripts/scientific-platform-status.js" defer></script>

<div class="dsg-scientific-center">

<section class="dsg-scientific-hero">
  <span class="dsg-scientific-hero__eyebrow">DIGITAL STARGATE · SCIENTIFIC PLATFORM</span>
  <h1>Scientific Platform Center</h1>
  <p>
    Centro documentale della piattaforma scientifica Digital StarGate: repository scientifico,
    catalogo osservativo, provenance, knowledge foundations e capability di intelligence.
    Gli stati correnti sono proiettati da evidence governate del repository; i dati di discovery
    AP-013 sono snapshot storici esplicitamente datati e non telemetria runtime.
  </p>
  <div class="dsg-scientific-actions">
    <a href="../architecture/packages/AP-013-Scientific-Image-Repository-Architecture/">AP-013 Architecture</a>
    <a href="../scientific-session-catalog/">Observation Catalog</a>
    <a href="../scientific-platform-intelligence/">Scientific Intelligence</a>
    <a href="../roadmap/">Governed Roadmap</a>
  </div>
</section>

<div data-scientific-platform-status>
  <section class="dsg-scientific-section">
    <span>GOVERNED CURRENT STATE</span>
    <h2>Caricamento stato governato…</h2>
    <p>La pagina non inferisce stati in assenza della projection repository.</p>
  </section>
</div>

<section class="dsg-scientific-section">
  <span>PLATFORM CAPABILITIES</span>
  <h2>Componenti della piattaforma scientifica</h2>
  <div class="dsg-scientific-grid">
    <article class="dsg-scientific-card"><strong>Scientific Binary Storage</strong><p>Conservazione esterna dei RAW, calibration frame, intermedi e prodotti finali. GitHub non è lo storage primario dei binari voluminosi.</p><a href="../architecture/packages/AP-013-Scientific-Image-Repository-Architecture/">Apri AP-013 →</a></article>
    <article class="dsg-scientific-card"><strong>Scientific Asset Registry</strong><p>Identificatori stabili, classificazione, checksum, dimensione, locator e stato di integrità.</p><a href="../architecture/scientific-assets/DSDM-002-Scientific-Data-Manager-Logical-Data-Model/">Logical Data Model →</a></article>
    <article class="dsg-scientific-card"><strong>Observation Catalog</strong><p>Indicizzazione e ricerca read-only delle osservazioni scientifiche, mantenendo AP-013 autorevole per asset, checksum e provenance.</p><a href="../scientific-session-catalog/">Apri Catalogo →</a></article>
    <article class="dsg-scientific-card"><strong>Processing Provenance</strong><p>Workflow, processing run, input, output, ambiente e relazioni di derivazione, con estensioni future governate.</p><a href="../architecture/scientific-assets/DSDM-003-Contract-and-Manifest-Model/">Contract &amp; Manifest →</a></article>
    <article class="dsg-scientific-card"><strong>Session Importer</strong><p>Discovery, parsing deterministico, trasferimento COPY_ONLY, staging verificato e protezione della sorgente.</p><a href="../architecture/scientific-assets/DSDM-004-Session-Importer-Architecture-and-Safe-Transfer-Design/">Importer Architecture →</a></article>
    <article class="dsg-scientific-card"><strong>Scientific Intelligence</strong><p>Knowledge/evidence, Target Knowledge Base, Night Timeline, Anomaly &amp; Trend e provenance come fondazioni read-only governate.</p><a href="../scientific-platform-intelligence/">Scientific Intelligence →</a></article>
  </div>
</section>

<section class="dsg-scientific-section">
  <span>DATA LIFECYCLE</span>
  <h2>Lifecycle governato degli asset</h2>
  <div class="dsg-scientific-flow">identified → ingested → integrity-verified → classified → linked → preserved → processed → derived → quality-reviewed → published | retained</div>
  <p>La cancellazione non è uno stato ordinario. Ogni modifica di stato richiede attore, precondizioni, timestamp, asset interessato, evidence reference e comportamento in errore.</p>
</section>

<section class="dsg-scientific-section">
  <span>DOCUMENTATION MAP</span>
  <h2>Baseline tecnica e evidence</h2>
  <div class="dsg-scientific-docs">
    <a href="../architecture/scientific-assets/AP13-W02-Current-State-Scientific-Asset-Inventory-Specification/"><strong>AP13-W02</strong><span>Current-State Scientific Asset Inventory</span></a>
    <a href="../architecture/scientific-assets/DSDM-001-Scientific-Data-Manager-Conceptual-Model/"><strong>DSDM-001</strong><span>Conceptual Model</span></a>
    <a href="../architecture/scientific-assets/DSDM-002-Scientific-Data-Manager-Logical-Data-Model/"><strong>DSDM-002</strong><span>Logical Data Model</span></a>
    <a href="../architecture/scientific-assets/DSDM-003-Contract-and-Manifest-Model/"><strong>DSDM-003</strong><span>Contract and Manifest Model</span></a>
    <a href="../architecture/scientific-assets/DSDM-004-Session-Importer-Architecture-and-Safe-Transfer-Design/"><strong>DSDM-004</strong><span>Session Importer and Safe Transfer</span></a>
    <a href="../architecture/validation/AP-013-Session-Discovery-Execution-Evidence/"><strong>E-AP013-SD-001</strong><span>Historical Session Discovery Evidence</span></a>
    <a href="../architecture/validation/AP-013-Operational-Acceptance/"><strong>OA-AP013-001</strong><span>Formal Operational Acceptance</span></a>
    <a href="../architecture/validation/AP-013-Morning-Transfer-Scheduler-Evidence/"><strong>Scheduler</strong><span>Morning Transfer Evidence</span></a>
  </div>
</section>

<section class="dsg-scientific-section">
  <span>GOVERNANCE BOUNDARY</span>
  <h2>Authority e proiezioni</h2>
  <p>AP-013 resta autorevole per scientific asset identity, integrity/checksum semantics, storage locator, lifecycle e processing provenance. Catalogo, knowledge, timeline e analytics consumano proiezioni read-only e non possono alterare retroattivamente tali evidenze.</p>
  <div class="dsg-scientific-warning"><strong>Safety:</strong> nessuna capability di questa pagina possiede autorità di comando o di remediation sui dispositivi fisici dell’osservatorio. La Safety Authority e gli interlock fisici locali restano indipendenti.</div>
</section>

</div>
