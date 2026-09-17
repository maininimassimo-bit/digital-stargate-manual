<link rel="stylesheet" href="../styles/observation-planner.css">
<script type="module" src="../javascripts/observation-planner.js"></script>
<script type="module" src="../javascripts/observation-planner-forecast-f7-site.js"></script>
<script type="module" src="../javascripts/observation-planner-e2e-f6.js"></script>
<script type="module" src="../javascripts/observation-planner-ranking-f5.js"></script>
<script type="module" src="../javascripts/observation-planner-f8.js"></script>

<div class="dsg-op-center">
<section class="dsg-op-hero">
  <div><span>BKL-031 · OBSERVATION PLANNER INTELLIGENTE</span><h1>Observation Planner</h1><p>Vista read-only di forecast reale del sito, geometria astronomica corrente della notte e suitability esplicita dei setup governati. Nessuna projection costituisce readiness, go/no-go, scheduling, comando o Safety Authority.</p></div>
  <div class="dsg-op-hero__mark" aria-hidden="true">◎</div>
</section>

<section class="dsg-op-notice"><strong>Stato: F1–F7 Accepted/Post-Merge Verified; F8 current astronomy + setup suitability è REVIEW CANDIDATE.</strong><p>F8 combina il forecast reale F7, acquisito sulle coordinate governate dell'osservatorio, con geometria astronomica della notte e suitability OTA/camera/filtro. Le coordinate protette restano nel boundary server-side e non sono pubblicate.</p><p>Seleziona un setup per vedere ranking motivato e migliori finestre advisory. I risultati non sono readiness, go/no-go, scheduling, comando o Safety Authority. BKL-032 e gli interlock fisici locali mantengono le rispettive autorità.</p><p>BKL-031 resta In Progress: dopo F8 rimane il gate finale di refresh ricorrente/current-night e chiusura funzionale.</p></section>

<div data-observation-planner-f8>
  <section class="dsg-op-panel"><h2>Caricamento Planner scientifico F8…</h2><p>Il consumer verifica privacy e authority boundary e fallisce chiuso.</p></section>
</div>

<div data-observation-planner-site-forecast>
  <section class="dsg-op-panel"><h2>Caricamento forecast reale del sito…</h2><p>Il consumer verifica lineage, freschezza e privacy e fallisce chiuso se la projection non è corrente.</p></section>
</div>

<div data-observation-planner-f6><section class="dsg-op-panel"><h2>Caricamento projection E2E F6…</h2><p>Evidence storica di integrazione, read-only.</p></section></div>
<div data-observation-planner-ranking><section class="dsg-op-panel"><h2>Caricamento ranking dimostrativo F5…</h2><p>Evidence storica di metodo, read-only.</p></section></div>
<div data-observation-planner-forecast><section class="dsg-op-panel"><h2>Caricamento projection forecast storica F4-D…</h2><p>Lineage predecessor, non forecast corrente.</p></section></div>
<div data-observation-planner><section class="dsg-op-panel"><h2>Caricamento projection astronomica F3-C…</h2><p>Evidence sintetica predecessor, separata e read-only.</p></section></div>
</div>
