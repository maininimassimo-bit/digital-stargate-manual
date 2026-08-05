<link rel="stylesheet" href="../styles/documentation-center.css">
<link rel="stylesheet" href="../styles/search-center.css">

<div class="dsg-documentation-center">

<section class="dsg-documentation-hero">
  <span class="dsg-documentation-hero__eyebrow">DIGITAL STARGATE · DOCUMENTATION CENTER</span>
  <h1>Tutta la documentazione, organizzata per dominio</h1>
  <p>
    Catalogo visuale del patrimonio documentale Digital StarGate. Questa pagina facilita
    l’accesso ai contenuti, mentre i documenti tecnici sottostanti restano le fonti autorevoli.
  </p>
  <div class="dsg-documentation-actions">
    <a href="#enterprise-search-center">⌕ Enterprise Search Center</a>
    <button type="button" data-dsg-doc-search>Ricerca rapida Material</button>
    <a href="../roadmap/">Apri la roadmap</a>
    <a href="../architecture/">Architecture Center</a>
    <a href="../scientific-platform/">Scientific Platform</a>
  </div>
</section>

<div class="dsg-documentation-kpis">
  <div class="dsg-documentation-kpi"><span>DOMINI</span><strong>8</strong><small>Accessi principali del portale</small></div>
  <div class="dsg-documentation-kpi"><span>ARCHITECTURE PACKAGE</span><strong>13</strong><small>AP-001 → AP-013</small></div>
  <div class="dsg-documentation-kpi"><span>MANUALE TECNICO</span><strong>44</strong><small>Capitoli operativi e ingegneristici</small></div>
  <div class="dsg-documentation-kpi"><span>BASELINE ATTIVA</span><strong>AP-013</strong><small>Scientific Image Repository</small></div>
</div>

<section class="dsg-documentation-section" id="enterprise-search-center">
  <span>ENTERPRISE FEDERATED SEARCH</span>
  <h2>Search Center</h2>
  <p>Ricerca contemporaneamente nella documentazione versionata e nel catalogo delle sessioni scientifiche. La ricerca nativa di Material resta disponibile per la consultazione rapida del portale.</p>

  <div class="dsg-search-center" data-dsg-search-center>
    <section class="dsg-search-center__panel" aria-labelledby="dsg-search-title">
      <div>
        <p class="dsg-kicker">Documentation + Scientific Platform</p>
        <h3 id="dsg-search-title">Ricerca unificata della piattaforma</h3>
      </div>

      <label>
        <span class="visually-hidden">Testo da cercare</span>
        <input class="dsg-search-center__query" type="search" data-search-query placeholder="Cerca target, sessione, architettura, procedura o componente…" autocomplete="off">
      </label>

      <div class="dsg-search-center__filters" aria-label="Filtri di ricerca">
        <label>Tipo
          <select data-search-type>
            <option value="">Tutti i tipi</option>
          </select>
        </label>
        <label>Anno
          <select data-search-year>
            <option value="">Tutti gli anni</option>
          </select>
        </label>
        <label>Target
          <select data-search-target>
            <option value="">Tutti i target</option>
          </select>
        </label>
        <label>Qualità
          <select data-search-quality>
            <option value="">Tutti gli stati</option>
          </select>
        </label>
      </div>

      <div class="dsg-search-center__toolbar">
        <div>
          <p data-search-status>Caricamento degli indici federati…</p>
          <p data-search-stats></p>
        </div>
        <button class="dsg-search-center__reset" type="button" data-search-reset>Reimposta filtri</button>
      </div>
    </section>

    <section class="dsg-search-center__results" data-search-results aria-live="polite">
      <div class="dsg-search-center__empty">Preparazione del Search Center…</div>
    </section>
  </div>

  <div class="dsg-documentation-note">
    Il Search Center usa l’indice generato dal plugin Search di MkDocs per la documentazione e lo Scientific Data Engine per le sessioni scientifiche. I dataset JSON restano proiezioni e lo Scientific Data Engine rimane l’unico access layer condiviso per i dati scientifici.
  </div>
</section>

<section class="dsg-documentation-section">
  <span>ESPLORA PER DOMINIO</span>
  <h2>Centri principali</h2>
  <div class="dsg-documentation-grid">
    <a class="dsg-documentation-card" href="../roadmap/">
      <span>PROGRAMMA</span><strong>Roadmap &amp; Milestone</strong><p>Stato del programma, package correnti, milestone e release.</p><em>Apri →</em>
    </a>
    <a class="dsg-documentation-card" href="../architecture/">
      <span>ARCHITETTURA</span><strong>Architecture Center</strong><p>AP, ADR, capability, assessment, validation e governance.</p><em>Apri →</em>
    </a>
    <a class="dsg-documentation-card is-featured" href="../scientific-platform/">
      <span>SCIENTIFIC PLATFORM · ATTIVO</span><strong>AP-013 Scientific Repository</strong><p>Scientific Data Manager, importer, manifest, provenance e readiness.</p><em>Apri →</em>
    </a>
    <a class="dsg-documentation-card" href="../status/">
      <span>OBSERVATORY</span><strong>Stato e sessioni</strong><p>Stato osservatorio, report di sessione e indicatori operativi.</p><em>Apri →</em>
    </a>
    <a class="dsg-documentation-card" href="../chapters/15-automazione/">
      <span>OPERATIONS</span><strong>Procedure e automazione</strong><p>Runbook, SOP, sicurezza, manutenzione e infrastruttura.</p><em>Apri →</em>
    </a>
    <a class="dsg-documentation-card" href="../analytics/">
      <span>ANALYTICS</span><strong>KPI e qualità dati</strong><p>Dashboard, storico, warehouse, configurazioni e quality gate.</p><em>Apri →</em>
    </a>
    <a class="dsg-documentation-card" href="../developer/development-guide/">
      <span>DEVELOPER</span><strong>Sviluppo e contratti</strong><p>Guide, capability, contratti canonici e publication guidelines.</p><em>Apri →</em>
    </a>
    <a class="dsg-documentation-card" href="../chapters/01-introduzione/">
      <span>MANUALE TECNICO</span><strong>Capitoli 1–44</strong><p>Infrastruttura, strumenti, software, operations e governance.</p><em>Apri →</em>
    </a>
  </div>
</section>

<section class="dsg-documentation-section">
  <span>TIPOLOGIE DOCUMENTALI</span>
  <h2>Trova rapidamente il documento corretto</h2>
  <div class="dsg-document-types">
    <a href="../architecture/"><strong>Architecture Package</strong><span>Scope, principi, modelli e boundary.</span></a>
    <a href="../architecture/ADR-001-Session-Layer/"><strong>ADR</strong><span>Decisioni architetturali canoniche.</span></a>
    <a href="../architecture/assessments/ARB-012-AP-012-Independent-Architecture-Review/"><strong>Assessment</strong><span>Review indipendenti e baseline certificate.</span></a>
    <a href="../architecture/validation/"><strong>Validation</strong><span>Campaign, execution evidence e readiness.</span></a>
    <a href="../chapters/16-sop-avvio/"><strong>SOP &amp; Runbook</strong><span>Procedure operative e recovery.</span></a>
    <a href="../developer/platform-contracts/"><strong>Contratti</strong><span>Modelli canonici e integrazione.</span></a>
  </div>
</section>

<section class="dsg-documentation-section">
  <span>PERCORSI CONSIGLIATI</span>
  <h2>Da dove iniziare</h2>
  <div class="dsg-documentation-paths">
    <article><strong>Comprendere il progetto</strong><p>Home → Roadmap → Architecture Center → AP corrente.</p><a href="../roadmap/">Inizia dal programma →</a></article>
    <article><strong>Operare l’osservatorio</strong><p>Stato → Automazione → SOP avvio → Emergenze e recovery.</p><a href="../status/">Apri Observatory →</a></article>
    <article><strong>Lavorare sui dati scientifici</strong><p>Scientific Platform → DSDM → Importer → Readiness Gate.</p><a href="../scientific-platform/">Apri Scientific Platform →</a></article>
    <article><strong>Sviluppare il portale</strong><p>Developer Guide → Contratti → Capability → Publication Guidelines.</p><a href="../developer/development-guide/">Apri Developer →</a></article>
  </div>
</section>

<section class="dsg-documentation-section">
  <span>GOVERNANCE</span>
  <h2>Regole di consultazione</h2>
  <div class="dsg-documentation-note">
    Le dashboard e i centri di dominio sono livelli di accesso. In caso di differenze,
    prevalgono il documento tecnico versionato, il relativo stato, le evidenze e i gate approvati.
  </div>
</section>

</div>

<script src="../javascripts/scientific-data-engine.js"></script>
<script src="../javascripts/dsg-search-service.js"></script>
<script src="../javascripts/dsg-search-center.js"></script>
<script>
document.querySelector('[data-dsg-doc-search]')?.addEventListener('click', () => {
  document.querySelector('label[for="__search"]')?.click();
});
</script>
