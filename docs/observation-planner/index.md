<link rel="stylesheet" href="../styles/observation-planner.css">
<link rel="stylesheet" href="../styles/planner-weather-sky.css">
<script type="module" src="../javascripts/observation-planner.js"></script>
<!-- Legacy governance bindings retained as non-rendered markers; stale F6/F7 panels are intentionally not mounted. -->
<script type="module" src="../javascripts/observation-planner-forecast-f7-site.js"></script>
<script type="module" src="../javascripts/observation-planner-e2e-f6.js"></script>
<script type="module" src="../javascripts/observation-planner-f9.js?v=refresh-2"></script>

<div class="dsg-op-center">
<section class="dsg-op-hero">
<!-- DSG:IMMERSIVE-SCENE -->
  <div><span>BKL-031 · OBSERVATION PLANNER INTELLIGENTE</span><h1>Observation Planner</h1><p>Vista read-only di forecast reale del sito, geometria astronomica corrente della notte e suitability esplicita dei setup governati. Nessuna projection costituisce readiness, go/no-go, scheduling, comando o Safety Authority.</p></div>
  <figure class="dsg-weather-sky" data-weather-sky data-sky-state="unknown">
    <div class="dsg-weather-sky__view"><img width="768" height="768" decoding="async" alt="" hidden></div>
    <figcaption><span>CIELO DELLA NOTTE · MANCIANO</span><strong data-sky-title>Verifica della previsione…</strong><p data-sky-details>In attesa dei dati del Planner.</p><small data-sky-period></small><small>Illustrazione atmosferica · non fotografia né mappa astronomica</small><details><summary>Come viene scelta l’immagine</summary><p>Stessi campioni della previsione completa della notte, fonte MeteoHub · ItaliaMeteo/ARPAE ICON-2I. Media aritmetica delle nuvole: fino al 20% immagine serena, oltre il 20% nuvolosa. Qualsiasi precipitazione prevista nella notte seleziona la pioggia, anche se limitata a poche ore. Convenzione solo visiva: non modifica semafori, ranking o autorità operativa. La Via Lattea è illustrativa: posizione e visibilità reale non sono calcolate.</p></details></figcaption>
  </figure>
</section>

<section class="dsg-op-notice"><strong>Stato: BKL-031 F1–F9 Closed / Accepted / Post-Merge Verified.</strong><p>F9 usa i run ufficiali ItaliaMeteo/ARPAE ICON-2I pubblicati da MeteoHub: nessun limite giornaliero imposto dal workflow, budget monetario €0, fail-closed e nessuna conservazione dei GRIB.</p><p>Seleziona un setup per vedere ranking motivato e finestre advisory. Ogni finestra deve superare i limiti meteo comuni e i filtri astronomici: Sole almeno 18° sotto l’orizzonte e target ad almeno 20° di altezza nei campioni orari. I limiti meteo sono nuvolosità ≤20% (vincolo di pianificazione della cupola richiesto dal proprietario, più restrittivo del limite BKL-032 del 50%), pioggia assente, vento ≤15 km/h, raffiche ≤20 km/h e UR ≤90%. Per ogni ora il margine dewpoint è temperatura (°C) − dewpoint (°C): margine ≤3 °C è NO-GO; solo un margine >3 °C supera questo controllo. La Luna contribuisce al punteggio advisory in base ad altezza, illuminazione e distanza angolare dal target. Il semaforo è solo advisory meteo: non è readiness, autorizzazione ad aprire la cupola, scheduling, comando o Safety Authority. Questa soglia F9 di pianificazione non modifica il criterio readiness BKL-032 né gli interlock fisici locali.</p><p>Il ranking ordina i target per score della migliore finestra; a parità considera il numero di finestre idonee e poi la suitability target/setup. La suitability F9 è una stima euristica, non un modello ottico calibrato. Il consumer verifica lineage, freschezza, privacy e authority boundary; se il run è stale, incompleto o non disponibile, fallisce chiuso.</p><p>Continuità dei predecessori: F4-B accettata; la fixture astronomica sintetica F3-C resta evidence TEST/NONE separata e non viene reinterpretata come geometria corrente.</p></section>

<div data-observation-planner-f9>
  <section class="dsg-op-panel"><h2>Caricamento Planner corrente F9…</h2><p>Il consumer verifica lineage, freschezza, privacy e authority boundary.</p></section>
</div>
<!-- data-observation-planner-site-forecast and data-observation-planner-f6 are intentionally absent from the DOM. -->

</div>
