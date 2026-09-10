<link rel="stylesheet" href="../styles/roadmap.css">

<div class="dsg-roadmap-app" data-roadmap-source="../data/roadmap.json">
  <header class="dsg-roadmap-hero dsg-roadmap-center-hero">
    <div>
      <span class="dsg-roadmap-kicker">DIGITAL STARGATE · ROADMAP CENTER</span>
      <h1>Programma architetturale e percorso evolutivo</h1>
      <p>
        Stato corrente, milestone, Architecture Package e prossime decisioni,
        derivati dalla projection generata della canonical roadmap source e contestualizzati dalla planning authority AMP-002.
      </p>
      <div class="dsg-roadmap-center-actions">
        <a href="../architecture/">Architecture Center</a>
        <a href="../scientific-platform/">Scientific Platform</a>
        <a href="../documentation/">Documentation Center</a>
        <a href="../architecture/assessments/AMP-002-Architecture-Program-Roadmap-Realignment/">Apri AMP-002</a>
      </div>
    </div>
    <div class="dsg-roadmap-summary" data-roadmap-summary></div>
  </header>

  <section class="dsg-roadmap-current" data-roadmap-current>
    <p>Caricamento del package corrente…</p>
  </section>

  <div class="dsg-roadmap-legend" aria-label="Legenda">
    <span><i class="is-completed"></i> Completato</span>
    <span><i class="is-active"></i> In corso</span>
    <span><i class="is-planned"></i> Pianificato</span>
  </div>

  <section class="dsg-roadmap-overview" aria-labelledby="roadmap-overview-title">
    <div class="dsg-roadmap-section-heading">
      <span class="dsg-roadmap-kicker">AVANZAMENTO COMPLESSIVO</span>
      <h2 id="roadmap-overview-title">Completato e ancora da realizzare</h2>
      <p>Riepilogo globale derivato dalla projection governata della roadmap, includendo tutti gli elementi versionati.</p>
    </div>
    <div class="dsg-roadmap-overview__content" data-roadmap-overview>
      <p>Calcolo dell’avanzamento in corso…</p>
    </div>
  </section>

  <div class="dsg-roadmap-progress" aria-label="Avanzamento complessivo">
    <div class="dsg-roadmap-progress__bar" data-roadmap-progress></div>
  </div>

  <section class="dsg-roadmap-center-section">
    <div class="dsg-roadmap-section-heading">
      <span class="dsg-roadmap-kicker">CAPABILITY WAVES</span>
      <h2>Sequenza degli Architecture Package</h2>
      <p>Ogni wave raggruppa package con responsabilità architetturali correlate.</p>
    </div>
    <main data-roadmap-waves aria-live="polite">
      <p>Caricamento della roadmap in corso…</p>
    </main>
  </section>

  <section class="dsg-roadmap-next">
    <div class="dsg-roadmap-section-heading">
      <span class="dsg-roadmap-kicker">OPEN ROADMAP ITEMS</span>
      <h2>Elementi roadmap non completati</h2>
      <p>Vista sintetica dei primi elementi non completati nel registro; non rappresenta da sola una coda dependency-ordered. Il package corrente e la prossima milestone governata sono indicati esplicitamente nelle card dedicate.</p>
    </div>
    <div class="dsg-roadmap-next__grid" data-roadmap-next>
      <p>Calcolo degli elementi aperti…</p>
    </div>
  </section>

  <section class="dsg-roadmap-milestones">
    <div class="dsg-roadmap-section-heading">
      <span class="dsg-roadmap-kicker">STORICO PUBBLICAZIONI</span>
      <h2>Milestone principali</h2>
      <p>Le milestone rappresentano lo stato registrato e non sostituiscono evidence, review o gate.</p>
    </div>
    <div class="dsg-roadmap-gallery" data-roadmap-gallery></div>
  </section>

  <aside class="dsg-roadmap-source">
    <strong>Authority e projection:</strong>
    lo stato corrente è derivato dalla canonical source <code>.github/roadmap/roadmap-source.json</code> e pubblicato tramite la generated projection <code>docs/data/roadmap.json</code>.
    <a href="../architecture/assessments/AMP-002-Architecture-Program-Roadmap-Realignment/">AMP-002 — Architecture Program Roadmap Realignment</a>
    resta la planning authority dell'architecture program e non sostituisce il live backlog/roadmap status.
  </aside>
</div>

<noscript>Per visualizzare la roadmap dinamica è necessario abilitare JavaScript.</noscript>
