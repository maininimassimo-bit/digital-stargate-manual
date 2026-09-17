<link rel="stylesheet" href="../styles/observation-planner.css">
<script type="module" src="../javascripts/observation-planner.js"></script>
<script type="module" src="../javascripts/observation-planner-e2e-f6.js"></script>
<script type="module" src="../javascripts/observation-planner-ranking-f5.js"></script>

<div class="dsg-op-center">
<section class="dsg-op-hero">
  <div><span>BKL-031 · OBSERVATION PLANNER INTELLIGENTE</span><h1>Observation Planner</h1><p>Vista read-only di evidence astronomica, forecast e compatibilità setup governati. Nessuna projection costituisce readiness, go/no-go, comando o Safety Authority.</p></div>
  <div class="dsg-op-hero__mark" aria-hidden="true">◎</div>
</section>

<section class="dsg-op-notice"><strong>Stato della funzionalità: F1–F5 Accepted/Post-Merge Verified; F6 real-evidence setup-aware E2E è REVIEW CANDIDATE.</strong><p>F6 lega una projection sanitizzata a valori meteorologici reali già acquisiti in F4-C e a evidence governata di compatibilità setup/target, senza nuove chiamate provider. Il forecast resta su localizzazione generalizzata e non è ancora un feed runtime fresco del sito; lo score F5 conserva geometria sintetica di validazione. Quindi questa vista prova il percorso end-to-end ma non costituisce ancora una raccomandazione reale per la notte.</p><p>Continuità governata dei predecessori: F4-B accettata; la fixture astronomica sintetica F3-C resta evidence di integrazione TEST/NONE e non viene reinterpretata come geometria osservativa reale.</p></section>

<div data-observation-planner-f6>
  <section class="dsg-op-panel"><h2>Caricamento projection E2E F6…</h2><p>Il consumer è fail-closed e pubblica soltanto evidence sanitizzata read-only.</p></section>
</div>

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
