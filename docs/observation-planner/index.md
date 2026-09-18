<link rel="stylesheet" href="../styles/observation-planner.css">
<script type="module" src="../javascripts/observation-planner.js"></script>
<!-- Legacy governance bindings retained as non-rendered markers; stale F6/F7 panels are intentionally not mounted. -->
<script type="module" src="../javascripts/observation-planner-forecast-f7-site.js"></script>
<script type="module" src="../javascripts/observation-planner-e2e-f6.js"></script>
<script type="module" src="../javascripts/observation-planner-f9.js?v=300"></script>

<div class="dsg-op-center">
<section class="dsg-op-hero">
  <div><span>BKL-031 · OBSERVATION PLANNER INTELLIGENTE</span><h1>Observation Planner</h1><p>Vista read-only di forecast reale del sito, geometria astronomica corrente della notte e suitability esplicita dei setup governati. Nessuna projection costituisce readiness, go/no-go, scheduling, comando o Safety Authority.</p></div>
  <div class="dsg-op-hero__mark" aria-hidden="true">◎</div>
</section>

<section class="dsg-op-notice"><strong>Stato: BKL-031 F1–F9 Closed / Accepted / Post-Merge Verified.</strong><p>F9 usa i run ufficiali ItaliaMeteo/ARPAE ICON-2I pubblicati da MeteoHub: massimo due acquisizioni UTC/giorno, budget monetario €0, fail-closed e nessuna conservazione dei GRIB.</p><p>Seleziona un setup per vedere ranking motivato e migliori finestre advisory. I risultati non sono readiness, go/no-go, scheduling, comando o Safety Authority. BKL-032 e gli interlock fisici locali mantengono le rispettive autorità.</p><p>Il consumer verifica lineage, freschezza, privacy e authority boundary; se il run è stale, incompleto o non disponibile, fallisce chiuso.</p><p>Continuità dei predecessori: F4-B accettata; la fixture astronomica sintetica F3-C resta evidence TEST/NONE separata e non viene reinterpretata come geometria corrente.</p></section>

<div data-observation-planner-f9>
  <section class="dsg-op-panel"><h2>Caricamento Planner corrente F9…</h2><p>Il consumer verifica lineage, freschezza, privacy e authority boundary.</p></section>
</div>
<!-- data-observation-planner-site-forecast and data-observation-planner-f6 are intentionally absent from the DOM. -->

</div>
