(() => {
  'use strict';

  const initialize = async ({ events } = {}) => {
    const root = document.querySelector('[data-session-catalog]');
    if (!root || root.dataset.dsgSessionExplorerReady === 'true') return;

    const engine = window.DSGScientificDataEngine;
    if (!engine) {
      console.error('Scientific Data Engine is not available.');
      events?.emit('scientific-session-explorer-error', { reason: 'engine-unavailable' });
      return;
    }

    root.dataset.dsgSessionExplorerReady = 'true';
    root.classList.add('is-loading');

    const source = root.dataset.sessionCatalog;
    const grid = root.querySelector('[data-session-grid]');
    const kpis = root.querySelector('[data-session-kpis]');
    const count = root.querySelector('[data-session-count]');
    const search = root.querySelector('[data-session-search]');
    const year = root.querySelector('[data-session-year]');
    const target = root.querySelector('[data-session-target]');
    const quality = root.querySelector('[data-session-quality]');
    const reset = root.querySelector('[data-session-reset]');

    const state = { sessions: [], filtered: [], transfers: new Map(), available:false };

    const esc = (value) => String(value ?? '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');

    const dec = (value, digits = 2) => typeof value==='number' && Number.isFinite(value) ? value.toFixed(digits).replace('.', ',') : 'Non disponibile';
    const unit=(value,suffix,digits=2)=>typeof value==='number'&&Number.isFinite(value)?`${dec(value,digits)}${suffix}`:'Non disponibile';
    const coordinate = (value) => {
      const number = Number(value);
      return Number.isFinite(number) ? `${number.toFixed(4).replace('.', ',')}°` : 'Non disponibile';
    };
    const formatDate = (value) => {
      const date = new Date(`${value}T00:00:00`);
      return Number.isNaN(date.getTime()) ? value : new Intl.DateTimeFormat('it-IT', { dateStyle: 'medium' }).format(date);
    };

    const statusLabel = (session) => {
      if(session.lightStarted===0 && session.lightCompleted===0)return 'Pacchetto senza LIGHT';
      if (session.qualityState === 'VALIDATED_ANALYTICS') return 'Validated analytics';
      if (session.qualityState === 'METADATA_INCOMPLETE') return 'Metadata incomplete';
      return 'Attention required';
    };

    const governedCoordinates = (session) => {
      const ra = session.raDeg ?? session.ra_deg;
      const decValue = session.decDeg ?? session.dec_deg;
      if (typeof ra!=='number'||typeof decValue!=='number'||!Number.isFinite(ra)||!Number.isFinite(decValue)||ra<0||ra>=360||decValue< -90||decValue>90) return null;
      return { ra, dec: decValue, source: session.coordinateSource || 'governed-registry' };
    };

    const renderKpis = async () => {
      const values = await engine.getKPIs(source);
      const display = [String(values.sessionCount),String(values.targetCount),`${dec(values.integrationHours)} h`,`${values.validatedCount}/${values.sessionCount}`];
      [...kpis.querySelectorAll('strong')].forEach((node, index) => { node.textContent = display[index] || '—'; });
      const label=root.querySelector('[data-session-acquisition-count]');
      if(label)label.textContent=`${values.acquisitionCount} con LIGHT · ${values.noLightCount} senza LIGHT`;
    };

    const populateFilters = async () => {
      const [years, targets] = await Promise.all([engine.getYears(source),engine.getTargets(source)]);
      const selectedYear=year.value, selectedTarget=target.value;
      year.innerHTML='<option value="">Tutti</option>';target.innerHTML='<option value="">Tutti</option>';
      years.forEach((value) => year.insertAdjacentHTML('beforeend', `<option value="${esc(value)}">${esc(value)}</option>`));
      targets.forEach((value) => target.insertAdjacentHTML('beforeend', `<option value="${esc(value)}">${esc(value)}</option>`));
      if(years.includes(selectedYear))year.value=selectedYear;
      if(targets.includes(selectedTarget))target.value=selectedTarget;
    };

    const card = (session) => {
      const tone = session.qualityState === 'VALIDATED_ANALYTICS' ? 'is-green' : 'is-red';
      const detailUrl = `../scientific-session-detail/?sessionId=${encodeURIComponent(session.sessionId)}`;
      const coords = governedCoordinates(session);
      const sqmMedian = session.sqm?.medianMagArcsec2;
      const sqmMetric = typeof sqmMedian==='number'&&Number.isFinite(sqmMedian) ? `
            <div><span>SQM mediano</span><strong>${esc(dec(sqmMedian, 2))} mag/arcsec²</strong></div>` : '';
      const coordinateMetrics = coords ? `
            <div><span>RA (J2000)</span><strong>${esc(coordinate(coords.ra))}</strong></div>
            <div><span>DEC (J2000)</span><strong>${esc(coordinate(coords.dec))}</strong></div>` : '';
      const coordinateState = coords ? `<span>Coordinate: ${esc(coords.source)}</span>` : '';
      const analyticsState = session.severity ? `<span>Analytics: ${esc(session.severity)}</span>` : '';
      const sqmState = session.sqm?.state ? `<span>SQM: ${esc(session.sqm.state)}</span>` : '';
      const receipt=state.transfers.get(session.sessionId);
      const transfer=receipt ? `${receipt.state} · ${receipt.verifiedFileCount}/${receipt.fileCount} file` : 'Non disponibile';
      return `
        <article class="dsg-session-card ${tone}">
          <div class="dsg-session-card__topline"><span>${esc(session.sessionId)}</span><span class="dsg-session-badge">${esc(statusLabel(session))}</span></div>
          <h2>${esc(session.target)}</h2>
          <p class="dsg-session-card__date">${esc(formatDate(session.observationDate))}</p>
          <div class="dsg-session-card__metrics">
            <div><span>Telescopio</span><strong>${esc(session.telescope)}</strong></div>
            <div><span>Camera</span><strong>${esc(session.camera)}</strong></div>
            <div><span>Filtro</span><strong>${esc(session.filter)}</strong></div>
            <div><span>Esposizione</span><strong>${session.exposureSeconds==null?'Non disponibile':`${esc(session.exposureSeconds)} s`}</strong></div>
            <div><span>Integrazione</span><strong>${unit(session.integrationHours,' h')}</strong></div>
            <div><span>Completamento</span><strong>${unit(session.completionPct,'%')}</strong></div>
            <div><span>RMS</span><strong>${unit(session.rmsTotalArcsec,'″',3)}</strong></div>
            <div><span>Light</span><strong>${esc(session.lightCompleted)} / ${esc(session.lightStarted)}</strong></div>${sqmMetric}${coordinateMetrics}
          </div>
          <div class="dsg-session-card__states">
            <span>Evidence: ${esc(session.evidenceState)}</span><span>Manifest: ${esc(session.manifestState)}</span><span>Transfer pacchetto: ${esc(transfer)}</span>${analyticsState}${sqmState}${coordinateState}
          </div>
          <a href="${detailUrl}">Apri sessione →</a>
        </article>`;
    };

    const render = () => {
      if(!state.available)return;
      state.filtered = engine.filterSessions(state.sessions, {query: search.value,year: year.value,target: target.value,quality: quality.value});
      count.textContent = `${state.filtered.length} registrazioni visualizzate su ${state.sessions.length}`;
      grid.innerHTML = state.filtered.length ? state.filtered.map(card).join('') : '<article class="dsg-session-empty">Nessuna sessione corrisponde ai filtri selezionati.</article>';
      events?.emit('scientific-session-explorer-filtered', {source,visible: state.filtered.length,total: state.sessions.length});
    };

    [search, year, target, quality].forEach((control) => control.addEventListener('input', render));
    reset.addEventListener('click', () => {search.value='';year.value='';target.value='';quality.value='';render();});

    let loading=false;
    const refreshButton=root.querySelector('[data-session-refresh]');
    const refresh=async()=>{
    if(loading||!root.isConnected)return;
    loading=true;if(refreshButton)refreshButton.disabled=true;
    const controller=new AbortController(),timeout=setTimeout(()=>controller.abort(),12000);
    try {
      const [sessions,collection] = await Promise.all([engine.getSessions(source,{force:true,signal:controller.signal}),engine.getSessionTransferCollection().catch(()=>null)]);
      if(!root.isConnected)return;
      state.sessions = sessions;
      state.available=true;
      state.transfers=new Map((collection?.records||[]).map(receipt=>[receipt.sessionId,receipt]));
      await Promise.all([renderKpis(),populateFilters()]);
      if(!root.isConnected)return;
      render();
      root.classList.remove('is-loading', 'is-error');
      root.classList.add('is-ready');
      events?.emit('scientific-session-explorer-ready', {source,sessions:sessions.length,metrics:engine.getMetrics?.() || null});
    } catch (error) {
      if(!root.isConnected)return;
      state.available=false;state.sessions=[];state.transfers.clear();
      console.error(error);
      root.classList.remove('is-loading', 'is-ready');
      root.classList.add('is-error');
      count.textContent = 'Catalogo non disponibile';
      grid.innerHTML = '<article class="dsg-session-empty is-error">Impossibile caricare il catalogo delle sessioni. Verificare il dataset versionato.</article>';
      kpis.querySelectorAll('strong').forEach(node=>{node.textContent='—';});
      const label=root.querySelector('[data-session-acquisition-count]');if(label)label.textContent='Acquisizioni non disponibili';
      events?.emit('scientific-session-explorer-error', {source,message:error.message});
    } finally {clearTimeout(timeout);loading=false;if(refreshButton)refreshButton.disabled=false;}
    };
    refreshButton?.addEventListener('click',refresh);
    const visible=()=>{if(!document.hidden)refresh();};
    document.addEventListener('visibilitychange',visible);
    const timer=setInterval(()=>{if(!root.isConnected){clearInterval(timer);document.removeEventListener('visibilitychange',visible);return;}visible();},60000);
    await refresh();
  };

  if (window.DSG?.components) {window.DSG.components.register({name:'scientific-session-explorer',order:65,initialize});return;}
  const fallback = () => initialize();
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fallback, { once: true }); else fallback();
  if (window.document$?.subscribe) window.document$.subscribe(fallback);
})();
