# Executive Observatory Dashboard

La dashboard executive utilizza la vista Analytics v3.1 generata automaticamente dallo storico consolidato delle sessioni scientifiche. I KPI vengono rigenerati dal workflow governato dell'Analytics Center dopo l'importazione delle nuove sessioni.

<div class="dsg-analytics-links">
  <a class="dsg-analytics-link-card" href="../dashboard/">
    <strong>Executive Dashboard</strong>
    <span>KPI aggregati, andamento mensile, target e configurazioni sul dataset consolidato.</span>
  </a>
  <a class="dsg-analytics-link-card" href="../history-validation/">
    <strong>Validazione storico</strong>
    <span>Controlli di qualità, coerenza e completezza dei dataset consolidati.</span>
  </a>
  <a class="dsg-analytics-link-card" href="../configuration-summary/">
    <strong>Configurazioni</strong>
    <span>Prestazioni e utilizzo dei profili strumentali dell'osservatorio.</span>
  </a>
</div>

## Dashboard operativa

La vista operativa autorevole è la **Dashboard Analytics dinamica**. Questa pagina resta disponibile come alias di compatibilità per i collegamenti storici, ma non incorpora più il precedente `dashboard.html` statico.

[Apri Executive Dashboard](../dashboard/){ .md-button .md-button--primary }

!!! info "Aggiornamento automatico"
    La dashboard viene rigenerata a partire da `data/analytics/history/sessions.csv` insieme al riepilogo configurazioni e viene verificata dal gate di consistenza dell'Analytics Center. I dati mancanti o non risolti restano espliciti e non vengono inferiti.
