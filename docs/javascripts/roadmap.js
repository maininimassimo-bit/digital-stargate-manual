(() => {
  const root = document.querySelector('.dsg-roadmap-app');
  if (!root) return;

  const source = root.dataset.roadmapSource;
  const wavesEl = root.querySelector('[data-roadmap-waves]');
  const summaryEl = root.querySelector('[data-roadmap-summary]');
  const overviewEl = root.querySelector('[data-roadmap-overview]');
  const galleryEl = root.querySelector('[data-roadmap-gallery]');
  const progressEl = root.querySelector('[data-roadmap-progress]');

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

  function renderOverview({ completed, active, planned, total, percent }) {
    const remaining = active + planned;
    const activeStart = percent;
    const activeEnd = Math.round(((completed + active) / total) * 100);

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

  function render(data) {
    const items = data.waves.flatMap(w => w.items);
    const completed = items.filter(i => i.status === 'completed').length;
    const active = items.filter(i => i.status === 'active').length;
    const planned = items.filter(i => i.status === 'planned').length;
    const percent = items.length ? Math.round((completed / items.length) * 100) : 0;

    summaryEl.innerHTML = `
      <div><span>Stato progetto</span><strong>${escapeHtml(data.projectStatus)}</strong></div>
      <div><span>Package corrente</span><strong>${escapeHtml(data.currentPackage)}</strong></div>
      <div><span>Prossima milestone</span><strong>${escapeHtml(data.nextMilestone)}</strong></div>
      <div><span>Target</span><strong>${escapeHtml(data.target)}</strong></div>`;

    renderOverview({ completed, active, planned, total: items.length, percent });

    progressEl.style.width = `${percent}%`;
    progressEl.setAttribute('aria-valuenow', String(percent));
    progressEl.title = `${completed} completati, ${active} in corso, ${planned} pianificati`;

    wavesEl.innerHTML = data.waves.map(wave => `
      <section class="dsg-roadmap-wave is-${escapeHtml(wave.status)}">
        <header><span>${escapeHtml(wave.id.toUpperCase())}</span><h2>${escapeHtml(wave.title)}</h2></header>
        <div class="dsg-roadmap-grid">${wave.items.map(itemMarkup).join('')}</div>
      </section>`).join('');

    galleryEl.innerHTML = data.milestones.map(m => `
      <article class="dsg-roadmap-milestone is-${escapeHtml(m.status)}">
        ${m.image ? `<a href="${escapeHtml(m.image)}"><img src="${escapeHtml(m.image)}" alt="Roadmap della milestone ${escapeHtml(m.title)}" loading="lazy"></a>` : `<div class="dsg-roadmap-milestone__placeholder" aria-hidden="true">${escapeHtml(m.id)}</div>`}
        <div><span>${m.date ? escapeHtml(m.date) : labels[m.status]}</span><h3>${escapeHtml(m.title)}</h3><p>${escapeHtml(m.description)}</p></div>
      </article>`).join('');
  }

  fetch(source, { cache: 'no-store' })
    .then(response => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    })
    .then(render)
    .catch(error => {
      wavesEl.innerHTML = `<div class="admonition warning"><p class="admonition-title">Roadmap non disponibile</p><p>Impossibile caricare il registro dinamico: ${escapeHtml(error.message)}</p></div>`;
      if (overviewEl) overviewEl.innerHTML = '<p>Riepilogo grafico non disponibile.</p>';
    });
})();