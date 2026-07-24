# Executive Observatory Dashboard

La dashboard raccoglie i principali indicatori delle sessioni osservative, dei target acquisiti, delle configurazioni strumentali e dell’affidabilità dei processi automatici.

<div class="dsg-dashboard-shell">
  <div class="dsg-dashboard-toolbar">
    <span class="dsg-dashboard-status">Dashboard Analytics v3.0</span>
    <a class="md-button" href="dashboard.html" target="_blank" rel="noopener">Apri a schermo intero</a>
  </div>
  <div id="dsg-dashboard-loading" class="admonition info">
    <p class="admonition-title">Caricamento dashboard</p>
    <p>Attendere il caricamento dei dati Analytics.</p>
  </div>
  <iframe
    id="dsg-analytics-frame"
    class="dsg-analytics-frame"
    src="dashboard.html"
    title="Digital StarGate Analytics Dashboard"
    loading="eager">
  </iframe>
</div>

<style>
.dsg-dashboard-shell {
  margin-top: 1rem;
}
.dsg-dashboard-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: .75rem;
}
.dsg-dashboard-status {
  color: var(--md-default-fg-color--light);
  font-size: .85rem;
}
.dsg-analytics-frame {
  display: block;
  width: 100%;
  min-height: 2400px;
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: .6rem;
  background: var(--md-default-bg-color);
}
@media (max-width: 760px) {
  .dsg-dashboard-toolbar {
    align-items: flex-start;
    flex-direction: column;
  }
  .dsg-analytics-frame {
    min-height: 3200px;
  }
}
</style>
