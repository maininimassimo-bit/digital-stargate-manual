# Executive Observatory Dashboard

La dashboard raccoglie i principali indicatori delle sessioni osservative, dei target acquisiti, delle configurazioni strumentali e dell’affidabilità dei processi automatici.

<div class="dsg-analytics-links">
  <a class="dsg-analytics-link-card" href="#dashboard-operativa">
    <strong>Executive overview</strong>
    <span>KPI aggregati, andamento mensile e stato operativo delle sessioni.</span>
  </a>
  <a class="dsg-analytics-link-card" href="history-validation/">
    <strong>Validazione storico</strong>
    <span>Controlli di qualità, coerenza e completezza dei dataset consolidati.</span>
  </a>
  <a class="dsg-analytics-link-card" href="configuration-summary/">
    <strong>Configurazioni</strong>
    <span>Prestazioni e utilizzo dei profili strumentali dell’osservatorio.</span>
  </a>
</div>

## Dashboard operativa

<div class="dsg-dashboard-shell">
  <div class="dsg-dashboard-toolbar">
    <span class="dsg-dashboard-status">Digital StarGate Analytics v3.1 — integrazione Material</span>
    <a class="md-button" href="../dashboard.html" target="_blank" rel="noopener">Apri a schermo intero</a>
  </div>
  <iframe
    id="dsg-analytics-frame"
    class="dsg-analytics-frame"
    src="../dashboard.html"
    title="Digital StarGate Analytics Dashboard"
    loading="eager">
  </iframe>
</div>

!!! info "Fase di transizione Analytics 3.1"
    La dashboard mantiene temporaneamente il motore HTML v3.0 all’interno del layout MkDocs Material. Il passaggio successivo estrarrà il contenuto generato in componenti nativi, senza modificare i calcoli dei KPI.
