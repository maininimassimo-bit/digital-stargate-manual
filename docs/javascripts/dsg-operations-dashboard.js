(() => {
  'use strict';

  const escapeHtml = (value) => String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');

  const formatNumber = (value) => Number(value || 0).toLocaleString('it-IT');

  const initialize = ({ events } = {}) => {
    const root = document.querySelector('[data-dsg-operations-dashboard]');
    if (!root || root.dataset.dsgOperationsDashboardReady === 'true') return;

    const service = window.DSGOperationsService;
    if (!service) {
      root.innerHTML = '<div class="dsg-operations-dashboard__error">Operations Service non disponibile.</div>';
      events?.emit('operations-dashboard-error', { reason: 'service-unavailable' });
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

    const renderKPIs = (kpis) => {
      const items = [
        ['Componenti registrati', kpis.registeredComponents],
        ['Componenti ready', kpis.readyComponents],
        ['Errori componenti', kpis.componentErrors],
        ['Sessioni indicizzate', kpis.scientificSessionsIndexed],
        ['Documenti ricerca', kpis.searchDocuments],
        ['Eventi osservati', kpis.observedRuntimeEvents]
      ];

      kpiNode.innerHTML = items.map(([label, value]) => `
        <article>
          <span>${escapeHtml(label)}</span>
          <strong>${formatNumber(value)}</strong>
        </article>`).join('');
    };

    const renderComponents = (snapshot) => {
      componentNode.innerHTML = snapshot.components.components.length
        ? snapshot.components.components.map((component) => `
          <article class="is-${escapeHtml(component.state)}">
            <strong>${escapeHtml(component.name)}</strong>
            <span>${escapeHtml(component.state)}</span>
            <small>Lifecycle cycle ${formatNumber(component.lastCycle)}</small>
          </article>`).join('')
        : '<div class="dsg-operations-dashboard__empty">Nessun componente registrato.</div>';
    };

    const renderServices = (snapshot) => {
      const services = [
        ['Enterprise Core', snapshot.enterpriseCore.available, snapshot.enterpriseCore.version],
        ['Scientific Data Engine', snapshot.scientific.available, snapshot.scientific.version],
        ['Search Service', snapshot.search.available, snapshot.search.version],
        ['Theme Service', snapshot.theme.available, snapshot.theme.version]
      ];

      serviceNode.innerHTML = services.map(([name, available, version]) => `
        <article class="${available ? 'is-available' : 'is-unavailable'}">
          <strong>${escapeHtml(name)}</strong>
          <span>${available ? 'Available' : 'Unavailable'}</span>
          <small>${escapeHtml(version || 'versione non disponibile')}</small>
        </article>`).join('');
    };

    const renderEvents = (snapshot) => {
      eventNode.innerHTML = snapshot.telemetry.recent.length
        ? snapshot.telemetry.recent.slice(0, 12).map((event) => `
          <article>
            <strong>${escapeHtml(event.type)}</strong>
            <time>${escapeHtml(new Date(event.observedAt).toLocaleString('it-IT'))}</time>
          </article>`).join('')
        : '<div class="dsg-operations-dashboard__empty">Nessun evento runtime osservato in questa sessione.</div>';
    };

    const renderAP013 = (snapshot) => {
      const ap013 = snapshot.ap013;
      ap013Node.innerHTML = `
        <article class="dsg-operations-ap013 is-${escapeHtml(ap013.validationState.toLowerCase())}">
          <div>
            <span>${escapeHtml(ap013.package)} · ${escapeHtml(ap013.capability)}</span>
            <strong>${escapeHtml(ap013.validationState)}</strong>
          </div>
          <dl>
            <div><dt>Operatore</dt><dd>${ap013.operatorReportedCompletion ? 'Completato' : 'Non completato'}</dd></div>
            <div><dt>Evidenze repository</dt><dd>${ap013.repositoryEvidenceAvailable ? 'Disponibili' : 'Pending'}</dd></div>
            <div><dt>Modalità</dt><dd>${escapeHtml(ap013.constraints.mode)}</dd></div>
            <div><dt>Limite</dt><dd>${formatNumber(ap013.constraints.maxFilesPerRun)} file/run</dd></div>
            <div><dt>Integrità</dt><dd>${escapeHtml(ap013.constraints.hashAlgorithm)}</dd></div>
          </dl>
        </article>`;
    };

    const render = () => {
      root.classList.add('is-refreshing');
      const snapshot = service.refresh();
      const kpis = service.getKPIs();

      renderKPIs(kpis);
      renderComponents(snapshot);
      renderServices(snapshot);
      renderEvents(snapshot);
      renderAP013(snapshot);
      generatedNode.textContent = `Snapshot ${new Date(snapshot.generatedAt).toLocaleString('it-IT')}`;

      root.classList.remove('is-refreshing');
      root.classList.add('is-ready');
      events?.emit('operations-dashboard-ready', {
        generatedAt: snapshot.generatedAt,
        registeredComponents: kpis.registeredComponents,
        componentErrors: kpis.componentErrors
      });
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
