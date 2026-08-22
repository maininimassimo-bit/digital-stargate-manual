(() => {
  'use strict';

  const initialize = ({ events } = {}) => {
    const root = document.querySelector('[data-dsg-operations-dashboard]');
    if (!root || root.dataset.dsgOperationsDashboardReady === 'true') return;

    const service = window.DSGOperationsService;
    const widgets = window.DSGOperationsWidgets;

    if (!service || !widgets) {
      root.innerHTML = '<div class="dsg-operations-dashboard__error">Operations Service o widget layer non disponibile.</div>';
      events?.emit('operations-dashboard-error', {
        reason: !service ? 'service-unavailable' : 'widgets-unavailable'
      });
      return;
    }

    root.dataset.dsgOperationsDashboardReady = 'true';

    const kpiNode = root.querySelector('[data-operations-kpis]');
    const componentNode = root.querySelector('[data-operations-components]');
    const serviceNode = root.querySelector('[data-operations-services]');
    const eventNode = root.querySelector('[data-operations-events]');
    const ap013Node = root.querySelector('[data-operations-ap013]');
    const generatedNode = root.querySelector('[data-operations-generated]');
    const refreshButton = root.querySelector('[data-operations-refresh]');

    const render = () => {
      root.classList.add('is-refreshing');

      try {
        const snapshot = service.refresh();
        const kpis = service.getKPIs();

        kpiNode.innerHTML = widgets.kpiCards([
          { label: 'Componenti registrati', value: kpis.registeredComponents },
          { label: 'Componenti ready', value: kpis.readyComponents },
          { label: 'Errori componenti', value: kpis.componentErrors },
          { label: 'Sessioni indicizzate', value: kpis.scientificSessionsIndexed },
          { label: 'Documenti ricerca', value: kpis.searchDocuments },
          { label: 'Eventi osservati', value: kpis.observedRuntimeEvents }
        ]);

        componentNode.innerHTML = widgets.healthList(
          snapshot.components.components.map((component) => ({
            name: component.name,
            state: component.state,
            detail: `Lifecycle cycle ${component.lastCycle}`
          }))
        );

        serviceNode.innerHTML = widgets.serviceList([
          {
            name: 'Enterprise Core',
            available: snapshot.enterpriseCore.available,
            version: snapshot.enterpriseCore.version
          },
          {
            name: 'Scientific Data Engine',
            available: snapshot.scientific.available,
            version: snapshot.scientific.version
          },
          {
            name: 'Search Service',
            available: snapshot.search.available,
            version: snapshot.search.version
          },
          {
            name: 'Theme Service',
            available: snapshot.theme.available,
            version: snapshot.theme.version
          }
        ]);

        eventNode.innerHTML = widgets.eventTimeline(snapshot.telemetry.recent, 12);
        ap013Node.innerHTML = widgets.ap013Card(snapshot.ap013);
        generatedNode.textContent = `Snapshot ${new Date(snapshot.generatedAt).toLocaleString('it-IT')}`;

        root.classList.remove('is-refreshing');
        root.classList.add('is-ready');

        events?.emit('operations-dashboard-ready', {
          generatedAt: snapshot.generatedAt,
          registeredComponents: kpis.registeredComponents,
          componentErrors: kpis.componentErrors
        });
      } catch (error) {
        root.classList.remove('is-refreshing', 'is-ready');
        root.classList.add('is-error');
        root.insertAdjacentHTML(
          'beforeend',
          '<div class="dsg-operations-dashboard__error">Impossibile generare lo snapshot operativo.</div>'
        );
        events?.emit('operations-dashboard-error', { message: error.message });
      }
    };

    refreshButton?.addEventListener('click', render);
    render();
  };

  if (window.DSG?.components) {
    window.DSG.components.register({
      name: 'operations-dashboard',
      order: 80,
      initialize
    });
  } else if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => initialize(), { once: true });
  } else {
    initialize();
  }
})();
