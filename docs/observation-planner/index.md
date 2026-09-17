<link rel="stylesheet" href="../styles/observation-planner.css">
<script type="module" src="../javascripts/observation-planner.js"></script>
<script type="module" src="../javascripts/observation-planner-forecast-f7-site.js"></script>
<script type="module" src="../javascripts/observation-planner-e2e-f6.js"></script>
<script type="module" src="../javascripts/observation-planner-ranking-f5.js"></script>

<div class="dsg-op-center">
<section class="dsg-op-hero">
  <div><span>BKL-031 · OBSERVATION PLANNER INTELLIGENTE</span><h1>Observation Planner</h1><p>Vista read-only di forecast reale del sito, evidence astronomica e compatibilità setup governati. Nessuna projection costituisce readiness, go/no-go, comando o Safety Authority.</p></div>
  <div class="dsg-op-hero__mark" aria-hidden="true">◎</div>
</section>

<section class="dsg-op-notice"><strong>Stato della funzionalità: F1–F6 Accepted/Post-Merge Verified; F7 fresh protected-site forecast è REVIEW CANDIDATE.</strong><p>F7 acquisisce forecast reale lato server sulle coordinate governate dell'osservatorio e pubblica soltanto una projection sanitizzata con il label generalizzato “Manciano (GR), Italia”, modello/run/freschezza e valori orari. Le coordinate protette, l'elevazione e la grid provider non sono esposte. Questa evidence è one-shot/evaluation: se il run supera la soglia di freschezza, il consumer fallisce chiuso invece di mostrare dati storici come correnti.</p><p>BKL-031 resta In Progress: ranking e finestre target reali richiedono ancora geometria astronomica corrente e suitability esplicita OTA/camera/filtro. BKL-032 e gli interlock fisici locali mantengono le rispettive autorità readiness/Safety.</p><p>Continuità governata dei predecessori: F4-B accettata; la fixture astronomica sintetica F3-C resta evidence di integrazione TEST/NONE e non viene reinterpretata come geometria osservativa reale.</p></section>

<div data-observation-planner-site-forecast>
  <section class="dsg-op-panel"><h2>Caricamento forecast reale del sito…</h2><p>Il consumer verifica lineage, freschezza e privacy e fallisce chiuso se la projection non è corrente.</p></section>
</div>

<div data-observation-planner-f6>
  <section class="dsg-op-panel"><h2>Caricamento projection E2E F6…</h2><p>Il consumer è fail-closed e pubblica soltanto evidence sanitizzata read-only.</p></section>
</div>

<div data-observation-planner-ranking>
  <section class="dsg-op-panel"><h2>Caricamento ranking dimostrativo F5…</h2><p>Il consumer è fail-closed e read-only; nessun risultato precedente o fallback viene sostituito.</p></section>
</div>

<div data-observation-planner-forecast>
  <section class="dsg-op-panel"><h2>Caricamento projection forecast storica governata F4-D…</h2><p>Resta visibile come lineage di predecessor evidence; non viene usata come forecast corrente del sito.</p></section>
</div>

<div data-observation-planner>
  <section class="dsg-op-panel"><h2>Caricamento projection astronomica governata…</h2><p>La projection F3-C resta separata e read-only.</p></section>
</div>
</div>
