(() => {
  const root = document.querySelector('[data-mission-control]');
  if (!root) return;

  const engine = window.DSGScientificDataEngine;
  const source = root.dataset.sessionCatalog;
  const kpis = root.querySelector('[data-mission-kpis]');
  const recent = root.querySelector('[data-mission-recent]');

  const esc = (value) => String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');

  const dec = (value, digits = 2) => Number(value || 0).toFixed(digits).replace('.', ',');
  const formatDate = (value) => {
    const date = new Date(`${value}T00:00:00`);
    return Number.isNaN(date.getTime()) ? value : new Intl.DateTimeFormat('it-IT', { dateStyle: 'medium' }).format(date);
  };

  const renderKpis = (values) => {
    const display = [
      String(values.sessionCount),
      String(values.targetCount),
      `${dec(values.integrationHours)} h`,
      `${values.validatedCount}/${values.sessionCount}`
    ];
    [...kpis.querySelectorAll('strong')].forEach((node, index) => {
      node.textContent = display[index] || '—';
    });
  };

  const renderRecent = (sessions) => {
    const items = sessions.slice(0, 3);
    recent.innerHTML = items.length
      ? items.map((session) => {
          const tone = session.qualityState === 'VALIDATED_ANALYTICS' ? 'is-green' : 'is-amber';
          const detailUrl = `../scientific-session-detail/?sessionId=${encodeURIComponent(session.sessionId)}`;
          return `
            <article class="dsg-mission-session ${tone}">
              <div>
                <span>${esc(session.sessionId)}</span>
                <strong>${esc(session.target)}</strong>
                <small>${esc(formatDate(session.observationDate))}</small>
              </div>
              <div>
                <span>Integrazione</span>
                <strong>${dec(session.integrationHours)} h</strong>
                <small>RMS ${dec(session.rmsTotalArcsec, 3)}″</small>
              </div>
              <a href="${detailUrl}">Apri →</a>
            </article>`;
        }).join('')
      : '<p>Nessuna sessione disponibile nel catalogo versionato.</p>';
  };

  if (!engine) {
    recent.innerHTML = '<p>Scientific Data Engine non disponibile.</p>';
    return;
  }

  Promise.all([
    engine.getKPIs(source),
    engine.getSessions(source)
  ])
    .then(([values, sessions]) => {
      renderKpis(values);
      renderRecent(sessions);
    })
    .catch((error) => {
      console.error(error);
      recent.innerHTML = '<p>Impossibile caricare i dati del Mission Control.</p>';
    });
})();
