(() => {
  'use strict';

  const labels = { completed: 'Completato', active: 'In corso', planned: 'Pianificato' };
  const escapeHtml = value => String(value ?? '').replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));

  function itemMarkup(item) {
    return `<article class="dsg-roadmap-card is-${escapeHtml(item.status)}">
      <div class="dsg-roadmap-card__status">${labels[item.status] || escapeHtml(item.status)}</div>
      <div class="dsg-roadmap-card__body">
        <span class="dsg-roadmap-card__id">${escapeHtml(item.id)}</span>
        <h3>${escapeHtml(item.title)}</h3>
        ${item.note ? `<p>${escapeHtml(item.note)}</p>` : ''}
        ${item.review ? `<span class="dsg-roadmap-card__review">Review ${escapeHtml(item.review)}</span>` : ''}
      </div>
    </article>`;
  }

  function renderOverview(overviewEl, { completed, active, planned, total, percent }) {
    const remaining = active + planned;
    const activeStart = percent;
    const activeEnd = total ? Math.round(((completed + active) / total) * 100) : 0;

    overviewEl.innerHTML = `
      <div class="dsg-roadmap-donut" style="--completed:${percent};--active-start:${activeStart};--active-end:${activeEnd}" role="img" aria-label="${completed} package completati, ${active} in corso e ${planned} pianificati su ${total}">
        <div class="dsg-roadmap-donut__center">
          <strong>${percent}%</strong>
          <span>completato</span>
        </div>
      </div>
      <div class="dsg-roadmap-overview__stats">
        <article class="is-completed"><span>Completati</span><strong>${completed}</strong><small>Architecture Package conclusi</small></article>
        <article class="is-active"><span>In corso</span><strong>${active}</strong><small>Package attualmente attivi</small></article>
        <article class="is-planned"><span>Pianificati</span><strong>${planned}</strong><small>Package ancora da avviare</small></article>
        <article class="is-remaining"><span>Da completare</span><strong>${remaining}</strong><small>In corso più pianificati</small></article>
      </div>`;
  }

  function renderCurrent(currentEl, data, items) {
    if (!currentEl) return;
    const current = items.find(item => item.id === data.currentPackage) || items.find(item => item.status === 'active');
    if (!current) {
      currentEl.innerHTML = '<p>Nessun package corrente identificato nel registro.</p>';
      return;
    }
    currentEl.innerHTML = `
      <div><span>PACKAGE CORRENTE</span><strong>${escapeHtml(current.id)}</strong></div>
      <div><h2>${escapeHtml(current.title)}</h2><p>${escapeHtml(current.note || 'Stato derivato dal registro versionato.')}</p></div>
      <div class="dsg-roadmap-current__status is-${escapeHtml(current.status)}">${labels[current.status] || escapeHtml(current.status)}</div>`;
  }

  function renderNext(nextEl, data, items) {
    if (!nextEl) return;
    const candidates = items.filter(item => item.status !== 'completed').slice(0, 4);
    const cards = candidates.map(item => `
      <article class="is-${escapeHtml(item.status)}">
        <span>${escapeHtml(item.id)}</span>
        <strong>${escapeHtml(item.title)}</strong>
        <small>${escapeHtml(item.note || labels[item.status])}</small>
      </article>`).join('');
    nextEl.innerHTML = `${cards}
      <article class="is-governance">
        <span>PROSSIMA MILESTONE</span>
        <strong>${escapeHtml(data.nextMilestone)}</strong>
        <small>Fonte: ${escapeHtml(data.authority)}</small>
      </article>`;
  }

  const initialize = async ({ events } = {}) => {
    const root = document.querySelector('.dsg-roadmap-app');
    if (!root || root.dataset.dsgRoadmapReady === 'true') return;
    root.dataset.dsgRoadmapReady = 'true';

    const source = root.dataset.roadmapSource;
    const wavesEl = root.querySelector('[data-roadmap-waves]');
    const summaryEl = root.querySelector('[data-roadmap-summary]');
    const overviewEl = root.querySelector('[data-roadmap-overview]');
    const galleryEl = root.querySelector('[data-roadmap-gallery]');
    const progressEl = root.querySelector('[data-roadmap-progress]');
    const currentEl = root.querySelector('[data-roadmap-current]');
    const nextEl = root.querySelector('[data-roadmap-next]');

    const render = data => {
      const items = data.waves.flatMap(wave => wave.items);
      const architectureWave = data.waves.find(wave => wave.id === 'architecture-program');
      const progressItems = architectureWave?.items || items.filter(item => /^AP-\d{3}$/.test(item.id));
      const completed = progressItems.filter(item => item.status === 'completed').length;
      const active = progressItems.filter(item => item.status === 'active').length;
      const planned = progressItems.filter(item => item.status === 'planned').length;
      const percent = progressItems.length ? Math.round((completed / progressItems.length) * 100) : 0;

      summaryEl.innerHTML = `
        <div><span>Stato progetto</span><strong>${escapeHtml(data.projectStatus)}</strong></div>
        <div><span>Package corrente</span><strong>${escapeHtml(data.currentPackage)}</strong></div>
        <div><span>Prossima milestone</span><strong>${escapeHtml(data.nextMilestone)}</strong></div>
        <div><span>Target</span><strong>${escapeHtml(data.target)}</strong></div>`;

      renderCurrent(currentEl, data, items);
      renderOverview(overviewEl, { completed, active, planned, total: progressItems.length, percent });
      renderNext(nextEl, data, items);

      progressEl.style.width = `${percent}%`;
      progressEl.setAttribute('aria-valuenow', String(percent));
      progressEl.title = `${completed} Architecture Package completati, ${active} in corso, ${planned} pianificati`;

      wavesEl.innerHTML = data.waves.map(wave => `
        <section class="dsg-roadmap-wave is-${escapeHtml(wave.status)}">
          <header><span>${escapeHtml(wave.id.toUpperCase())}</span><h2>${escapeHtml(wave.title)}</h2></header>
          <div class="dsg-roadmap-grid">${wave.items.map(itemMarkup).join('')}</div>
        </section>`).join('');

      galleryEl.innerHTML = data.milestones.map(milestone => `
        <article class="dsg-roadmap-milestone is-${escapeHtml(milestone.status)}">
          ${milestone.image ? `<a href="${escapeHtml(milestone.image)}"><img src="${escapeHtml(milestone.image)}" alt="Roadmap della milestone ${escapeHtml(milestone.title)}" loading="lazy"></a>` : `<div class="dsg-roadmap-milestone__placeholder" aria-hidden="true">${escapeHtml(milestone.id)}</div>`}
          <div><span>${milestone.date ? escapeHtml(milestone.date) : labels[milestone.status]}</span><h3>${escapeHtml(milestone.title)}</h3><p>${escapeHtml(milestone.description)}</p></div>
        </article>`).join('');
    };

    try {
      const response = await fetch(source, { cache: 'no-store' });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      render(await response.json());
      events?.emit('roadmap-ready', { source });
    } catch (error) {
      root.dataset.dsgRoadmapReady = 'error';
      wavesEl.innerHTML = `<div class="admonition warning"><p class="admonition-title">Roadmap non disponibile</p><p>Impossibile caricare il registro dinamico: ${escapeHtml(error.message)}</p></div>`;
      if (overviewEl) overviewEl.innerHTML = '<p>Riepilogo grafico non disponibile.</p>';
      if (currentEl) currentEl.innerHTML = '<p>Package corrente non disponibile.</p>';
      if (nextEl) nextEl.innerHTML = '<p>Prossime attività non disponibili.</p>';
      events?.emit('roadmap-error', { source, error });
    }
  };

  if (window.DSG?.components) {
    window.DSG.components.register({
      name: 'roadmap-center',
      order: 70,
      initialize
    });
    return;
  }

  const fallback = () => initialize();
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', fallback, { once: true });
  } else {
    fallback();
  }
  if (window.document$?.subscribe) window.document$.subscribe(fallback);
})();