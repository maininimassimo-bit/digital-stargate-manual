(() => {
  'use strict';

  const STATUS_LABELS = {
    active: 'Attivo',
    completed: 'Completato',
    planned: 'Pianificato',
    blocked: 'Bloccato'
  };

  const text = (value, fallback = '—') => {
    const normalized = String(value ?? '').trim();
    return normalized || fallback;
  };

  const statusLabel = (status) => STATUS_LABELS[String(status || '').toLowerCase()] || text(status, 'Stato non disponibile');

  const setKpi = (node, value, detail) => {
    if (!node) return;
    const strong = node.querySelector('strong');
    const small = node.querySelector('small');
    if (strong) strong.textContent = value;
    if (small) small.textContent = detail;
  };

  const parseRoadmap = (payload) => {
    if (!payload || typeof payload !== 'object') throw new Error('Roadmap non valida');
    if (!payload.summary || !Array.isArray(payload.waves)) throw new Error('Contratto roadmap incompleto');
    return payload;
  };

  const render = (root, roadmap) => {
    const kpis = root.querySelectorAll('[data-architecture-kpis] .dsg-architecture-kpi');
    const summary = roadmap.summary;

    setKpi(kpis[0], text(roadmap.currentPackage, 'UNKNOWN'), text(roadmap.nextMilestone, 'Milestone non disponibile'));
    setKpi(
      kpis[1],
      `${Number.isFinite(Number(summary.percentCompleted)) ? Number(summary.percentCompleted) : 0}%`,
      `${Number(summary.active) || 0} attivi · ${Number(summary.planned) || 0} pianificati`
    );
    setKpi(kpis[2], `${Number(summary.completed) || 0}/${Number(summary.total) || 0}`, 'Elementi completati nella roadmap');
    setKpi(kpis[3], text(roadmap.updatedAt), text(roadmap.generatedFrom, 'Fonte governata'));

    const items = new Map(
      roadmap.waves.flatMap((wave) => Array.isArray(wave.items) ? wave.items : [])
        .filter((item) => item && item.id)
        .map((item) => [item.id, item])
    );

    root.querySelectorAll('[data-ap-id]').forEach((card) => {
      const item = items.get(card.dataset.apId);
      const small = card.querySelector('small');
      card.classList.remove('is-active', 'is-completed', 'is-planned');
      if (!item) {
        if (small) small.textContent = 'Non presente nella projection';
        return;
      }
      const status = String(item.status || '').toLowerCase();
      if (['active', 'completed', 'planned'].includes(status)) card.classList.add(`is-${status}`);
      if (small) small.textContent = statusLabel(status);
    });

    root.dataset.architectureState = 'ready';
  };

  const renderFailure = (root) => {
    const kpis = root.querySelectorAll('[data-architecture-kpis] .dsg-architecture-kpi');
    setKpi(kpis[0], 'UNKNOWN', 'Projection non disponibile');
    setKpi(kpis[1], '—', 'Avanzamento non disponibile');
    setKpi(kpis[2], '—', 'Conteggi non disponibili');
    setKpi(kpis[3], '—', 'Verificare la roadmap governata');
    root.dataset.architectureState = 'unavailable';
  };

  const initialize = async () => {
    const root = document.querySelector('[data-architecture-roadmap]');
    if (!root || root.dataset.architectureLoading === 'true') return;
    root.dataset.architectureLoading = 'true';
    try {
      const source = root.dataset.architectureRoadmap;
      const response = await fetch(new URL(source, document.baseURI), { cache: 'no-store' });
      if (!response.ok) throw new Error(`Roadmap HTTP ${response.status}`);
      render(root, parseRoadmap(await response.json()));
    } catch (error) {
      renderFailure(root);
      console.warn('Digital StarGate Architecture Center:', error);
    } finally {
      root.dataset.architectureLoading = 'false';
    }
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialize, { once: true });
  else initialize();

  if (typeof document$ !== 'undefined') document$.subscribe(initialize);
})();
