(() => {
  const root = document.querySelector('[data-scientific-platform-status]');
  if (!root) return;

  const escapeHtml = (value) => String(value ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');

  const statusLabel = (status) => ({ completed: 'COMPLETED', active: 'CURRENT', planned: 'PLANNED' }[status] || String(status || 'UNKNOWN').toUpperCase());
  const itemCard = (item) => `<article><span>${escapeHtml(item.id)}</span><strong>${escapeHtml(item.title)}</strong><small>${escapeHtml(statusLabel(item.status))}</small></article>`;

  const render = (data) => {
    const d = data.historicalDiscovery;
    const t = data.transfer;
    const current = data.current.package;

    root.innerHTML = `
      <section class="dsg-scientific-section">
        <span>GOVERNED CURRENT STATE</span>
        <h2>Stato corrente della Scientific Platform</h2>
        <div class="dsg-scientific-status-grid">
          <article><span>CURRENT PACKAGE</span><strong>${escapeHtml(current.id)}</strong><small>${escapeHtml(current.title)} · ${escapeHtml(statusLabel(current.status))}</small></article>
          <article><span>AP-013</span><strong>${escapeHtml(statusLabel(data.architecture.ap013.status))}</strong><small>Scientific Image Repository</small></article>
          <article><span>AP-014</span><strong>${escapeHtml(statusLabel(data.architecture.ap014.status))}</strong><small>Scientific Observation Catalog &amp; Search</small></article>
          <article><span>AP-015</span><strong>${escapeHtml(statusLabel(data.architecture.ap015.status))}</strong><small>Scientific Knowledge Platform</small></article>
        </div>
        <p><strong>Next milestone:</strong> ${escapeHtml(data.current.nextMilestone)}</p>
      </section>

      <section class="dsg-scientific-section">
        <span>HISTORICAL DISCOVERY EVIDENCE</span>
        <h2>Baseline AP-013 verificata, non telemetria live</h2>
        <div class="dsg-scientific-kpis">
          <div class="dsg-scientific-kpi"><span>DISCOVERY</span><strong>${escapeHtml(d.files)} file</strong><small>${escapeHtml(d.sessions)} sessioni · evidence ${escapeHtml(d.evidenceId)}</small></div>
          <div class="dsg-scientific-kpi"><span>PARSE QUALITY</span><strong>${d.files ? Math.round((d.parsed / d.files) * 100) : 0}%</strong><small>${escapeHtml(d.parsed)} parsed · ${escapeHtml(d.ambiguous)} ambiguous · ${escapeHtml(d.failed)} failed</small></div>
          <div class="dsg-scientific-kpi"><span>EVIDENCE DATE</span><strong>${escapeHtml(d.asOf)}</strong><small>Snapshot storico governato</small></div>
          <div class="dsg-scientific-kpi"><span>PROJECTION</span><strong>READ ONLY</strong><small>Non rappresenta stato runtime corrente</small></div>
        </div>
      </section>

      <section class="dsg-scientific-section">
        <span>SAFE TRANSFER</span>
        <h2>Boundary operativo governato</h2>
        <div class="dsg-scientific-status-grid">
          <article><span>TRANSFER MODE</span><strong>${escapeHtml(t.mode)}</strong><small>${escapeHtml(t.status)}</small></article>
          <article><span>BATCH LIMIT</span><strong>&le; ${escapeHtml(t.maxFilesPerRun)} file/run</strong><small>Limite massimo accettato</small></article>
          <article><span>INTEGRITÀ</span><strong>${escapeHtml(t.hashAlgorithm)}</strong><small>No overwrite · no source cleanup</small></article>
          <article><span>SCHEDULER</span><strong>${escapeHtml(data.scheduler.timeLocal)}</strong><small>${escapeHtml(data.scheduler.state)} · evidenza governata</small></article>
        </div>
        <div class="dsg-scientific-warning"><strong>Safety boundary:</strong> questa pagina non possiede command authority, remediation authority o Safety Authority. Gli interlock fisici locali restano indipendenti.</div>
      </section>

      <section class="dsg-scientific-section">
        <span>ACCEPTED INTELLIGENCE FOUNDATIONS</span>
        <h2>Fondazioni scientifiche e di intelligence</h2>
        <div class="dsg-scientific-status-grid">
          ${itemCard(data.intelligence.knowledgeAiEvidenceContract)}
          ${itemCard(data.intelligence.targetKnowledgeBase)}
          ${itemCard(data.intelligence.nightTimelineReplay)}
          ${itemCard(data.intelligence.anomalyTrendCenter)}
        </div>
      </section>`;
  };

  const showError = () => {
    root.innerHTML = '<section class="dsg-scientific-section"><div class="dsg-scientific-warning"><strong>Governed status unavailable.</strong> La projection della Scientific Platform non è disponibile; nessuno stato viene inferito dal browser.</div></section>';
  };

  fetch('../data/scientific-platform-status.json', { cache: 'no-store' })
    .then((response) => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    })
    .then(render)
    .catch(showError);
})();
