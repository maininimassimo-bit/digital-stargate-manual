<link rel="stylesheet" href="../styles/observation-planner.css">
<script type="module" src="../javascripts/observation-planner.js"></script>
<script type="module" src="../javascripts/observation-planner-ranking-f5.js"></script>

<div class="dsg-op-center">
<section class="dsg-op-hero">
  <div><span>BKL-031 · OBSERVATION PLANNER INTELLIGENTE</span><h1>Observation Planner</h1><p>Vista read-only di evidence astronomica, contesto forecast e ranking dimostrativo governati. Nessuna projection costituisce readiness, go/no-go, comando o Safety Authority.</p></div>
  <div class="dsg-op-hero__mark" aria-hidden="true">◎</div>
</section>

<section class="dsg-op-notice"><strong>Stato della funzionalità: F4 Accepted/Post-Merge Verified; F5 è un dimostratore EVALUATION/NONE in validazione pre-merge.</strong><p>Il contesto forecast deriva esclusivamente dall’evidence F4-C riconciliata del workflow run <code>35214129960</code>: 71 istanti orari completi, un istante escluso e zero imputazioni. Non vengono effettuate ulteriori chiamate al provider. F4-B accettata resta la baseline dei contratti previsionali; la fixture astronomica sintetica F3-C resta pubblicata separatamente. Il ranking F5 usa identità target governate ma factor values sintetici, esclusivamente per validare metodo e decomposition.</p></section>

<div data-observation-planner-ranking>
  <section class="dsg-op-panel"><h2>Caricamento ranking dimostrativo F5…</h2><p>Il consumer è fail-closed e read-only; nessun risultato precedente o fallback viene sostituito.</p></section>
</div>

<div data-observation-planner-forecast>
  <section class="dsg-op-panel"><h2>Caricamento projection forecast governata…</h2><p>Se la projection non supera la verifica fail-closed, nessun dato precedente o fallback viene sostituito.</p></section>
</div>

<div data-observation-planner>
  <section class="dsg-op-panel"><h2>Caricamento projection astronomica governata…</h2><p>La projection F3-C resta separata e read-only.</p></section>
</div>
</div>
