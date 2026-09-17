<link rel="stylesheet" href="../styles/observation-planner.css">
<script type="module" src="../javascripts/observation-planner.js"></script>
<script type="module" src="../javascripts/observation-planner-forecast-f7-site.js"></script>
<script type="module" src="../javascripts/observation-planner-e2e-f6.js"></script>
<script type="module" src="../javascripts/observation-planner-ranking-f5.js"></script>
<script type="module" src="../javascripts/observation-planner-f8.js"></script>
<script type="module" src="../javascripts/observation-planner-f9.js"></script>

<div class="dsg-op-center">
<section class="dsg-op-hero">
  <div><span>BKL-031 · OBSERVATION PLANNER INTELLIGENTE</span><h1>Observation Planner</h1><p>Vista read-only di forecast reale del sito, geometria astronomica corrente della notte e suitability esplicita dei setup governati. Nessuna projection costituisce readiness, go/no-go, scheduling, comando o Safety Authority.</p></div>
  <div class="dsg-op-hero__mark" aria-hidden="true">◎</div>
</section>

<section class="dsg-op-notice"><strong>Stato: F1–F8 Accepted/Post-Merge Verified; F9 repeatable current-night è implementation candidate.</strong><p>F9 usa i run ufficiali ItaliaMeteo/ARPAE ICON-2I pubblicati da MeteoHub, con massimo due acquisizioni giornaliere, budget monetario €0 e nessuna conservazione dei GRIB.</p><p>Seleziona un setup per vedere ranking motivato e migliori finestre advisory. I risultati non sono readiness, go/no-go, scheduling, comando o Safety Authority. BKL-032 e gli interlock fisici locali mantengono le rispettive autorità.</p><p>Se il run è stale, incompleto o non disponibile, il consumer fallisce chiuso e non presenta F7/F8 come dato corrente.</p><p>Continuità dei predecessori: F4-B accettata; la fixture astronomica sintetica F3-C resta evidence TEST/NONE separata e non viene reinterpretata come geometria corrente.</p></section>

<div data-observation-planner-f9>
  <section class="dsg-op-panel"><h2>Caricamento Planner corrente F9…</h2><p>Il consumer verifica lineage, freschezza, privacy e authority boundary.</p></section>
</div>

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
