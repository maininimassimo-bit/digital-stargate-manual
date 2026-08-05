<link rel="stylesheet" href="../styles/operations-center.css">
<link rel="stylesheet" href="../styles/operations-dashboard.css">

<div class="dsg-operations-center">

<section class="dsg-operations-hero">
  <span class="dsg-operations-hero__eyebrow">DIGITAL STARGATE · OPERATIONS CENTER</span>
  <h1>Osservatorio, automazione e continuità operativa</h1>
  <p>
    Punto di accesso alle procedure operative, alla safety, alla manutenzione,
    al monitoraggio e ai runbook dell’osservatorio. Le dashboard facilitano la consultazione;
    i capitoli tecnici e le evidenze restano le fonti autorevoli.
  </p>
  <div class="dsg-operations-actions">
    <a href="#enterprise-operations-dashboard">Operations Dashboard</a>
    <a href="../status/">Stato osservatorio</a>
    <a href="../chapters/16-sop-avvio/">SOP avvio</a>
    <a href="../chapters/18-emergenze-recovery/">Emergenze e recovery</a>
  </div>
</section>

<div class="dsg-operations-kpis">
  <div class="dsg-operations-kpi"><span>AUTOMAZIONE</span><strong>Governata</strong><small>NINA, CPWI, PHD2 e ASCOM</small></div>
  <div class="dsg-operations-kpi"><span>SAFETY</span><strong>Locale e indipendente</strong><small>Interblocchi non delegati al portale</small></div>
  <div class="dsg-operations-kpi"><span>TRANSFER</span><strong>07:30</strong><small>COPY_ONLY, un file per run</small></div>
  <div class="dsg-operations-kpi"><span>RUNBOOK</span><strong>Versionati</strong><small>Avvio, acquisizione, chiusura e recovery</small></div>
</div>

<section class="dsg-operations-section" id="enterprise-operations-dashboard">
  <span>ENTERPRISE OBSERVABILITY</span>
  <h2>Operations Dashboard</h2>
  <p>Snapshot read-only della piattaforma RC2. I dati provengono esclusivamente dalle API pubbliche dei servizi enterprise e dalla telemetria dell’Event Bus.</p>

  <div class="dsg-operations-dashboard" data-dsg-operations-dashboard>
    <div class="dsg-operations-dashboard__toolbar">
      <div>
        <strong>Platform health snapshot</strong>
        <p data-operations-generated>Preparazione dello snapshot operativo…</p>
      </div>
      <button class="dsg-operations-dashboard__refresh" type="button" data-operations-refresh>Aggiorna snapshot</button>
    </div>

    <section class="dsg-operations-dashboard__kpis" data-operations-kpis aria-label="KPI della piattaforma">
      <div class="dsg-operations-dashboard__empty">Caricamento KPI…</div>
    </section>

    <div class="dsg-operations-dashboard__grid">
      <section class="dsg-operations-dashboard__panel">
        <h3>Component Registry</h3>
        <div class="dsg-operations-dashboard__list" data-operations-components>
          <div class="dsg-operations-dashboard__empty">Caricamento componenti…</div>
        </div>
      </section>

      <section class="dsg-operations-dashboard__panel">
        <h3>Enterprise Services</h3>
        <div class="dsg-operations-dashboard__services" data-operations-services>
          <div class="dsg-operations-dashboard__empty">Caricamento servizi…</div>
        </div>
      </section>

      <section class="dsg-operations-dashboard__panel">
        <h3>Runtime Event Stream</h3>
        <div class="dsg-operations-dashboard__list" data-operations-events>
          <div class="dsg-operations-dashboard__empty">In attesa di eventi runtime…</div>
        </div>
      </section>

      <section class="dsg-operations-dashboard__panel">
        <h3>AP-013 Operational Acceptance</h3>
        <div data-operations-ap013>
          <div class="dsg-operations-dashboard__empty">Caricamento stato AP-013…</div>
        </div>
      </section>
    </div>
  </div>

  <div class="dsg-operations-warning">
    La dashboard non costituisce un sistema di comando e non sostituisce le evidenze versionate. Stati runtime e dati di validazione sono presentati separatamente.
  </div>
</section>

<section class="dsg-operations-section">
  <span>OPERATING MODEL</span>
  <h2>Capability operative</h2>
  <div class="dsg-operations-grid">
    <a href="../chapters/15-automazione/"><strong>Automazione dell’osservatorio</strong><p>Architettura, orchestrazione e responsabilità del controllo automatico.</p><em>Apri →</em></a>
    <a href="../chapters/16-sop-avvio/"><strong>Avvio operativo</strong><p>Sequenza controllata di accensione, connessione, verifica e apertura.</p><em>Apri →</em></a>
    <a href="../chapters/17-acquisizione-automatica/"><strong>Acquisizione automatica</strong><p>Sequenze NINA, guida, autofocus, flip e gestione degli errori.</p><em>Apri →</em></a>
    <a href="../chapters/25-chiusura-osservatorio/"><strong>Chiusura osservatorio</strong><p>Terminazione sessione, chiusura sicura e conservazione dello stato.</p><em>Apri →</em></a>
    <a href="../chapters/26-monitoraggio-meteo-sicurezza-ambientale/"><strong>Meteo e sicurezza ambientale</strong><p>Soglie, osservabilità, safe state e comportamento fail-safe.</p><em>Apri →</em></a>
    <a href="../chapters/18-emergenze-recovery/"><strong>Emergenze e recovery</strong><p>Gestione anomalie, perdita connettività, recovery e ripristino controllato.</p><em>Apri →</em></a>
  </div>
</section>

<section class="dsg-operations-section">
  <span>OPERATIONS LIFECYCLE</span>
  <h2>Sequenza operativa governata</h2>
  <div class="dsg-operations-flow">
    readiness check → power and network → mount and software → weather validation → dome open → acquisition → monitoring → safe close → evidence and reporting
  </div>
</section>

<section class="dsg-operations-section">
  <span>SAFETY &amp; RESILIENCE</span>
  <h2>Principi non negoziabili</h2>
  <div class="dsg-operations-status-grid">
    <article><span>LOCAL SAFETY</span><strong>Independent</strong><small>Gli interblocchi fisici non dipendono dal portale o dal cloud.</small></article>
    <article><span>UNKNOWN STATE</span><strong>Not safe</strong><small>Uno stato stale o sconosciuto non è interpretato come sicuro.</small></article>
    <article><span>REMOTE ACCESS</span><strong>Controlled</strong><small>Accesso remoto separato da safety e comando fisico.</small></article>
    <article><span>RECOVERY</span><strong>Procedure-driven</strong><small>Ripristino solo attraverso runbook e verifiche esplicite.</small></article>
  </div>
</section>

<section class="dsg-operations-section">
  <span>MAINTENANCE &amp; CONTINUITY</span>
  <h2>Supporto operativo</h2>
  <div class="dsg-operations-support">
    <a href="../chapters/19-manutenzione-preventiva/"><strong>Manutenzione preventiva</strong><span>Controlli periodici, pulizia, verifica e calibrazione.</span></a>
    <a href="../chapters/21-backup-disaster-recovery/"><strong>Backup &amp; Disaster Recovery</strong><span>Protezione dati, restore e continuità operativa.</span></a>
    <a href="../chapters/22-inventario-asset-management/"><strong>Asset Management</strong><span>Inventario, ownership, baseline e obsolescenza.</span></a>
    <a href="../chapters/30-metodologia-troubleshooting/"><strong>Troubleshooting</strong><span>Metodo di diagnosi, isolamento e risoluzione.</span></a>
    <a href="../chapters/31-problem-management-post-mortem/"><strong>Problem Management</strong><span>Post-mortem, cause radice e azioni correttive.</span></a>
    <a href="../chapters/29-reportistica-operativa-kpi/"><strong>Reporting &amp; KPI</strong><span>Evidenze, indicatori e governance operativa.</span></a>
  </div>
</section>

<section class="dsg-operations-section">
  <span>CURRENT OPERATIONAL BOUNDARY</span>
  <h2>AP-013 Morning Transfer</h2>
  <div class="dsg-operations-boundary">
    <article><strong>Modalità</strong><span>COPY_ONLY</span></article>
    <article><strong>Finestra</strong><span>07:30–08:15</span></article>
    <article><strong>Integrità</strong><span>SHA-256</span></article>
    <article><strong>Limite</strong><span>1 file per run</span></article>
  </div>
  <div class="dsg-operations-warning">
    Bulk transfer, overwrite e source cleanup restano non autorizzati fino al completamento delle evidenze operative e del readiness review.
  </div>
</section>

</div>

<script src="../javascripts/scientific-data-engine.js"></script>
<script src="../javascripts/dsg-search-service.js"></script>
<script src="../javascripts/dsg-operations-service.js"></script>
<script src="../javascripts/dsg-operations-dashboard.js"></script>
