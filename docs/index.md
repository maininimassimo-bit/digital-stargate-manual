<link rel="stylesheet" href="./styles/enterprise-home.css">

<div class="dsg-enterprise-home">

<div class="dsg-hero">
  <div class="dsg-hero__overlay"></div>

  <div class="dsg-hero__content">
    <p class="dsg-hero__eyebrow">OSSERVATORIO ASTRONOMICO REMOTO <span>•</span> MANCIANO (GR)</p>
    <h1>Digital StarGate</h1>
    <p class="dsg-hero__tagline">Enterprise Documentation Portal</p>
    <p class="dsg-hero__subtitle">
      La piattaforma documentale ufficiale per l’architettura, le operazioni,
      l’osservatorio e la gestione governata dei dati scientifici.
    </p>

    <div class="dsg-hero__actions">
      <a class="md-button md-button--primary" href="./architecture/">
        Esplora l’architettura <span aria-hidden="true">→</span>
      </a>
      <a class="md-button" href="./roadmap/">
        Apri la roadmap <span aria-hidden="true">→</span>
      </a>
      <a class="md-button" href="./status/">
        Stato osservatorio <span aria-hidden="true">→</span>
      </a>
    </div>

    <div class="dsg-hero__principles">
      <div class="dsg-principle">
        <span class="dsg-principle__icon">◈</span>
        <div><strong>Governance</strong><span>Framework, tracciabilità e conformità enterprise.</span></div>
      </div>
      <div class="dsg-principle">
        <span class="dsg-principle__icon">▤</span>
        <div><strong>Scientific Data</strong><span>Gestione governata del repository scientifico.</span></div>
      </div>
      <div class="dsg-principle">
        <span class="dsg-principle__icon">↗</span>
        <div><strong>Innovation</strong><span>Architettura modulare e sviluppo continuo.</span></div>
      </div>
    </div>
  </div>

  <aside class="dsg-mission-panel">
    <span>LA NOSTRA MISSIONE</span>
    <p>
      Rendere i dati astronomici accessibili, affidabili e utili alla comunità
      scientifica attraverso tecnologia, rigorosa governance e innovazione continua.
    </p>
  </aside>
</div>

<section class="dsg-domain-section">
  <div class="dsg-section-intro">
    <span class="dsg-section-kicker">ESPLORA PER DOMINIO</span>
    <h2>Un portale organizzato per responsabilità e capacità</h2>
  </div>

  <div class="dsg-domain-grid">
    <article class="dsg-domain-card is-executive">
      <span class="dsg-domain-card__icon">▥</span>
      <h3>Executive</h3>
      <p>Visione, programma, governance e pianificazione dell’evoluzione Digital StarGate.</p>
      <a href="./roadmap/">Apri la roadmap →</a>
    </article>

    <article class="dsg-domain-card is-architecture">
      <span class="dsg-domain-card__icon">⌘</span>
      <h3>Architecture</h3>
      <p>Architettura enterprise, metamodel, decisioni, principi e Architecture Package.</p>
      <a href="./architecture/">Esplora l’architettura →</a>
    </article>

    <article class="dsg-domain-card is-scientific">
      <span class="dsg-domain-card__badge">ATTIVO</span>
      <span class="dsg-domain-card__icon">♢</span>
      <h3>Scientific Platform</h3>
      <p>AP-013, Scientific Repository, Session Importer, manifest e dati scientifici.</p>
      <a href="./architecture/packages/AP-013-Scientific-Image-Repository-Architecture/">Apri AP-013 →</a>
    </article>

    <article class="dsg-domain-card is-operations">
      <span class="dsg-domain-card__icon">⚙</span>
      <h3>Operations</h3>
      <p>Procedure operative, automazione, runbook e gestione dell’infrastruttura.</p>
      <a href="./chapters/15-automazione/">Apri Operations →</a>
    </article>

    <article class="dsg-domain-card is-validation">
      <span class="dsg-domain-card__icon">◇</span>
      <h3>Validation &amp; Certification</h3>
      <p>Review indipendenti, assessment, validation campaign, evidenze e readiness gate.</p>
      <a href="./architecture/validation/">Apri Validation →</a>
    </article>

    <article class="dsg-domain-card is-analytics">
      <span class="dsg-domain-card__icon">⌁</span>
      <h3>Analytics</h3>
      <p>KPI, dashboard, qualità dei dati, osservabilità e insight delle sessioni.</p>
      <a href="./analytics/">Apri Analytics →</a>
    </article>

    <article class="dsg-domain-card is-developer">
      <span class="dsg-domain-card__icon">&lt;/&gt;</span>
      <h3>Developer</h3>
      <p>Guide di sviluppo, contratti canonici, capability e standard di pubblicazione.</p>
      <a href="./developer/development-guide/">Apri Developer →</a>
    </article>

    <article class="dsg-domain-card is-observatory">
      <span class="dsg-domain-card__icon">⌂</span>
      <h3>Observatory</h3>
      <p>Strumentazione, acquisizione, stato operativo, ambiente e sessioni osservative.</p>
      <a href="./status/">Apri Observatory →</a>
    </article>
  </div>
</section>

<section class="dsg-program-section">
  <div class="dsg-section-intro">
    <span class="dsg-section-kicker">STATO DEL PROGRAMMA</span>
    <h2>Architettura e avanzamento corrente</h2>
  </div>

  <div class="dsg-program-panel">
    <article>
      <span class="dsg-program-label">ARCHITECTURE PACKAGE</span>
      <span class="dsg-program-value">AP-013 <span class="dsg-status-pill">IN CORSO</span></span>
      <span class="dsg-program-detail">Scientific Image Repository Architecture</span>
      <div class="dsg-progress" aria-label="Avanzamento AP-013: 70 percento"><span></span></div>
    </article>

    <article>
      <span class="dsg-program-label">PROSSIMA MILESTONE</span>
      <span class="dsg-program-value">M3.3</span>
      <span class="dsg-program-detail">Repository scientifico, manifest, catalogo SHA-256 e metadata.</span>
    </article>

    <article>
      <span class="dsg-program-label">BASELINE OPERATIVA</span>
      <span class="dsg-program-value">Limited Pilot</span>
      <span class="dsg-program-detail">Discovery 203 file · 11 sessioni · COPY_ONLY · 1 file per run.</span>
    </article>

    <article>
      <span class="dsg-program-label">SAFETY BOUNDARY</span>
      <span class="dsg-program-value">Protetta</span>
      <span class="dsg-program-detail">Overwrite, bulk transfer e source cleanup non autorizzati.</span>
    </article>
  </div>
</section>

<!-- DSG:AUTO-HOMEPAGE:START -->
<section class="dsg-program-section">
  <div class="dsg-section-intro">
    <span class="dsg-section-kicker">OSSERVATORIO E DATI</span>
    <h2>Indicatori operativi</h2>
  </div>

  <div class="dsg-kpi-grid">
    <div class="dsg-kpi">
      <span class="dsg-kpi__label">Sessioni</span>
      <span class="dsg-kpi__value dsg-counter" data-value="3">0</span>
      <span class="dsg-kpi__detail">storico disponibile</span>
    </div>
    <div class="dsg-kpi">
      <span class="dsg-kpi__label">Integrazione</span>
      <span class="dsg-kpi__value dsg-counter" data-value="31.83" data-decimals="2" data-suffix=" h">0</span>
      <span class="dsg-kpi__detail">totale acquisito</span>
    </div>
    <div class="dsg-kpi">
      <span class="dsg-kpi__label">Immagini</span>
      <span class="dsg-kpi__value dsg-counter" data-value="191">0</span>
      <span class="dsg-kpi__detail">light completati</span>
    </div>
    <div class="dsg-kpi">
      <span class="dsg-kpi__label">Target</span>
      <span class="dsg-kpi__value dsg-counter" data-value="1">0</span>
      <span class="dsg-kpi__detail">oggetti distinti</span>
    </div>
  </div>
</section>
<!-- DSG:AUTO-HOMEPAGE:END -->

<section class="dsg-quick-section">
  <div class="dsg-section-intro">
    <span class="dsg-section-kicker">ACCESSO RAPIDO</span>
    <h2>Documenti e strumenti principali</h2>
  </div>

  <div class="dsg-quick-grid">
    <a class="dsg-quick-card" href="./roadmap/"><strong>Roadmap</strong><span>Stato e pianificazione del programma.</span><em>→</em></a>
    <a class="dsg-quick-card" href="./architecture/packages/AP-013-Scientific-Image-Repository-Architecture/"><strong>Architecture Packages</strong><span>Elenco e stato degli AP attivi.</span><em>→</em></a>
    <a class="dsg-quick-card" href="./architecture/assessments/ARB-012-AP-012-Independent-Architecture-Review/"><strong>Assessment</strong><span>Review e assessment indipendenti.</span><em>→</em></a>
    <a class="dsg-quick-card" href="./chapters/01-introduzione/"><strong>Documentazione tecnica</strong><span>Manuale tecnico e procedure.</span><em>→</em></a>
    <a class="dsg-quick-card" href="https://github.com/maininimassimo-bit/digital-stargate-manual"><strong>Repository</strong><span>Codice sorgente e strumenti.</span><em>→</em></a>
  </div>
</section>

<div class="dsg-enterprise-footer">
  <blockquote class="dsg-enterprise-quote">
    “L’universo non è fatto solo di stelle, ma di dati che raccontano storie.
    Noi costruiamo il ponte per comprenderle.”
  </blockquote>
  <div class="dsg-enterprise-meta">
    <strong>DOCUMENTAZIONE</strong>
    <span>Digital StarGate</span>
    <span>Maintainer: Massimo Mainini</span>
    <span>GitHub Pages · MkDocs Material</span>
    <span>Stato: in continua evoluzione</span>
  </div>
</div>

</div>
