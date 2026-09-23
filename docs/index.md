---
title: Digital StarGate
description: Portale operativo, scientifico e documentale dell'osservatorio astronomico remoto di Manciano.
hide:
  - toc
---

<link rel="stylesheet" href="./styles/enterprise-home.css?v=d6f2d481">

<main class="dsg-enterprise-home">

<section class="dsg-hero dsg-hero--home" aria-labelledby="dsg-home-title">
  <div class="dsg-hero__overlay"></div>
  <div class="dsg-hero__content">
    <p class="dsg-hero__eyebrow">OSSERVATORIO ASTRONOMICO REMOTO · MANCIANO</p>
    <h1 id="dsg-home-title">Dal cielo al dato,<br>in un’unica vista.</h1>
    <p class="dsg-hero__subtitle">
      Stato dell’osservatorio, sessioni scientifiche, analisi e documentazione tecnica:
      ogni informazione mantiene origine, aggiornamento e livello di affidabilità visibili.
    </p>
    <div class="dsg-hero__actions">
      <a class="md-button md-button--primary" href="./mission-control/">Apri Mission Control</a>
      <a class="md-button" href="./scientific-session-catalog/">Esplora le sessioni</a>
    </div>
  </div>
  <div class="dsg-hero__trust" aria-label="Garanzie del portale">
    <span><strong>Read-only first</strong> Nessun comando agli apparati</span>
    <span><strong>Repository governed</strong> Fonti e proiezioni versionate</span>
    <span><strong>Auto-updated</strong> Refresh dopo ogni sessione importata</span>
  </div>
</section>

<!-- DSG:AUTO-HOMEPAGE:START -->
<section class="dsg-live-board" aria-labelledby="dsg-live-title" data-dsg-home-snapshot aria-live="polite">
  <div class="dsg-live-board__heading">
    <div><span class="dsg-section-kicker">SNAPSHOT GOVERNATO</span><h2 id="dsg-live-title">Il progetto e l’ultima notte</h2></div>
    <span class="dsg-data-freshness" data-home-freshness>Caricamento projection…</span>
  </div>
  <div class="dsg-live-board__grid">
    <article class="dsg-live-card dsg-live-card--primary">
      <span>Package corrente</span>
      <strong data-home-current-package>—</strong>
      <p data-home-current-detail>Stato roadmap non ancora disponibile</p>
      <a href="./roadmap/">Apri roadmap</a>
    </article>
    <article class="dsg-live-card">
      <span>Ultima sessione</span>
      <strong data-home-latest-session>—</strong>
      <p data-home-latest-detail>Projection scientifica non ancora disponibile</p>
      <a href="./scientific-session-catalog/" data-home-latest-link>Apri dettaglio sessione</a>
    </article>
    <article class="dsg-live-card">
      <span>Patrimonio pubblicato</span>
      <strong data-home-session-count>—</strong>
      <p data-home-session-totals>Conteggi non ancora disponibili</p>
      <a href="./scientific-session-catalog/">Apri catalogo</a>
    </article>
  </div>
</section>
<!-- DSG:AUTO-HOMEPAGE:END -->

<section class="dsg-domain-section" aria-labelledby="dsg-domains-title">
  <div class="dsg-section-intro">
    <span class="dsg-section-kicker">ESPLORA</span>
    <h2 id="dsg-domains-title">Scegli ciò che devi capire o fare</h2>
    <p>Sei percorsi chiari separano stato corrente, storia scientifica, operatività e fonti autorevoli.</p>
  </div>

  <div class="dsg-domain-grid">
    <a class="dsg-domain-card is-observatory" href="./status/">
      <span class="dsg-domain-card__meta">LIVE E FRESHNESS</span><h3>Osservatorio</h3>
      <p>Meteo, cupola, EAGLE e stato dei sistemi con evidenza di qualità e scadenza.</p><em>Apri stato osservatorio</em>
    </a>
    <a class="dsg-domain-card is-scientific" href="./scientific-session-catalog/">
      <span class="dsg-domain-card__meta">STORICO VERSIONATO</span><h3>Sessioni scientifiche</h3>
      <p>Cerca una sessione, apri il dettaglio e risali a report, sorgenti e provenance.</p><em>Esplora il catalogo</em>
    </a>
    <a class="dsg-domain-card is-analytics" href="./analytics/">
      <span class="dsg-domain-card__meta">ANALISI DESCRITTIVA</span><h3>Analytics</h3>
      <p>Confronti, trend e prestazioni delle configurazioni senza ranking impliciti.</p><em>Apri Analytics Center</em>
    </a>
    <a class="dsg-domain-card is-operations" href="./operations/">
      <span class="dsg-domain-card__meta">PROCEDURE E RUNBOOK</span><h3>Operations</h3>
      <p>Procedure operative, automazione, recovery e confini di sicurezza.</p><em>Apri Operations Center</em>
    </a>
    <a class="dsg-domain-card is-architecture" href="./architecture/">
      <span class="dsg-domain-card__meta">DECISIONI E CONTRATTI</span><h3>Architettura</h3>
      <p>Architecture Package, ADR, modelli, review ed evidence verificabili.</p><em>Apri Architecture Center</em>
    </a>
    <a class="dsg-domain-card is-governance" href="./documentation/">
      <span class="dsg-domain-card__meta">RICERCA E GOVERNANCE</span><h3>Documentazione</h3>
      <p>Trova rapidamente manuali, standard, roadmap e documenti di progetto.</p><em>Apri Documentation Center</em>
    </a>
  </div>
</section>

<section class="dsg-context-section" aria-labelledby="dsg-context-title">
  <div class="dsg-context-section__copy">
    <span class="dsg-section-kicker">COME LEGGERE IL PORTALE</span>
    <h2 id="dsg-context-title">Realtime e storico non sono la stessa cosa</h2>
    <p>Lo stato osservatorio usa segnali con freshness esplicita. Le sessioni e le analisi sono proiezioni storiche versionate. Uno stato assente o scaduto resta <strong>UNKNOWN/STALE</strong> e non viene trasformato in uno stato sicuro.</p>
  </div>
  <div class="dsg-context-section__actions">
    <a href="./status/"><strong>Stato corrente</strong><span>Telemetria read-only e freshness</span></a>
    <a href="./scientific-platform/"><strong>Patrimonio scientifico</strong><span>Contratti, cataloghi e lineage</span></a>
  </div>
</section>

<section class="dsg-quick-section" aria-labelledby="dsg-quick-title">
  <div class="dsg-section-intro"><span class="dsg-section-kicker">ACCESSO RAPIDO</span><h2 id="dsg-quick-title">I punti di ingresso principali</h2></div>
  <div class="dsg-quick-grid">
    <a class="dsg-quick-card" href="./mission-control/"><strong>Mission Control</strong><span>Vista sintetica della piattaforma.</span><em>Apri</em></a>
    <a class="dsg-quick-card" href="./roadmap/"><strong>Roadmap</strong><span>Avanzamento e prossima milestone.</span><em>Apri</em></a>
    <a class="dsg-quick-card" href="./session-reports/"><strong>Report sessioni</strong><span>Report Markdown e PDF pubblicati.</span><em>Apri</em></a>
    <a class="dsg-quick-card" href="./chapters/01-introduzione/"><strong>Manuale tecnico</strong><span>Impianto, strumenti, software e procedure.</span><em>Apri</em></a>
  </div>
</section>

<footer class="dsg-enterprise-footer">
  <p>Digital StarGate · Osservatorio astronomico remoto di Manciano</p>
  <p>Fonti versionate su GitHub · Presentation boundary read-only</p>
</footer>

</main>
