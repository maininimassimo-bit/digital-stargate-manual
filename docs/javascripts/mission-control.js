(() => {
  const initialize = () => {
  const root = document.querySelector('[data-mission-control]');
  if (!root || root.dataset.missionReady === 'true') return;
  root.dataset.missionReady = 'true';

  const engine = window.DSGScientificDataEngine;
  const source = root.dataset.sessionCatalog;
  const kpis = root.querySelector('[data-mission-kpis]');
  const recent = root.querySelector('[data-mission-recent]');
  const knowledge=root.querySelector('[data-mission-knowledge]'), status=root.querySelector('[data-mission-lineage-status]'), button=root.querySelector('[data-mission-refresh]');

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
          const accepted = session.qualityState === 'VALIDATED_ANALYTICS';
          const incomplete = session.qualityState === 'METADATA_INCOMPLETE';
          const tone = accepted ? 'is-green' : 'is-amber';
          const detailUrl = `../scientific-session-detail/?sessionId=${encodeURIComponent(session.sessionId)}`;
          const qualityLabel = incomplete
            ? 'Metadata scientifici incompleti'
            : (session.qualityState || session.analyticsState || 'Stato non disponibile');
          return `
            <article class="dsg-mission-session ${tone}">
              <div>
                <span>${esc(session.sessionId)}</span>
                <strong>${esc(session.target)}</strong>
                <small>${esc(formatDate(session.observationDate))} · ${esc(qualityLabel)}</small>
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

  const pipeline=root.querySelector('[data-mission-pipeline]'),boundary=root.querySelector('[data-mission-boundary]'),pipelineStatus=root.querySelector('[data-mission-pipeline-status]'),boundaryStatus=root.querySelector('[data-mission-boundary-status]');
  const statusRows=rows=>rows.map(([label,value])=>`<div><span>${esc(label)}</span><strong>${esc(value)}</strong></div>`).join('');
  const renderOperational=value=>{
    if(!value){pipeline.innerHTML=statusRows([['Baseline','Non verificabile']]);boundary.innerHTML=statusRows([['Vincoli documentati','Non verificabili']]);pipelineStatus.textContent=boundaryStatus.textContent='Proiezione corrente non disponibile; nessuna attestazione runtime.';return;}
    const d=value.historicalDiscovery,t=value.transfer;
    pipeline.innerHTML=statusRows([
      ['Discovery storica',`${d.files} file · ${d.sessions} sessioni · ${formatDate(d.asOf)}`],
      ['Filename parsing storico',`${d.parsed}/${d.files} · ${d.ambiguous} ambigui · ${d.failed} falliti`],
      ['Transfer mode (baseline)',`${t.mode} · ${t.status}`],
      ['Limite batch accettato',`≤ ${t.maxFilesPerRun} file / run`],
      ['Overwrite (vincolo)',t.overwriteExisting?'Autorizzato':'Non autorizzato'],
      ['Source cleanup (vincolo)',t.sourceCleanupAuthorized?'Autorizzato':'Non autorizzato']
    ]);
    boundary.innerHTML=statusRows([
      ['Safety Authority','Interlock locali · vincolo architetturale'],
      ['Trigger documentato',`${value.scheduler.timeLocal} locali · evidenza storica`],
      ['Integrità richiesta',t.hashAlgorithm],
      ['Telemetria operativa','Non disponibile in questa proiezione']
    ]);
    pipelineStatus.textContent=`Proiezione aggiornata al ${formatDate(value.updatedAt)}. Evidence e acceptance documentali; non è l’inventario corrente dei file né l’esito dell’ultimo trasferimento.`;
    boundaryStatus.textContent='Vincoli di progetto e scheduler storico: non attestano lo stato presente di EAGLE, dei task o della safety.';
  };
  const renderCoverage=(sessions,gallery,transfer)=>{
    knowledge.innerHTML=window.DSGMissionLineage.describe(sessions,gallery,transfer).map(row=>`<article class="is-${esc(row.state)}"><strong>${esc(row.label)}</strong><span>${esc(row.detail)}</span></article>`).join('');
  };
  const refresh=async()=>{
    if(button.disabled)return;button.disabled=true;renderCoverage(null,null,null);renderOperational(null);
    [...kpis.querySelectorAll('strong')].forEach(node=>node.textContent='—');
    recent.textContent='Verifica del catalogo in corso…';status.textContent='Verifica delle fonti correnti in corso…';
    try{
      const [catalog,gallery,transfer,platform]=await Promise.allSettled([engine.getCurrentSessions(source),engine.getSessionPhotoCollection(),engine.getSessionTransferCollection(),engine.getMissionPlatformState()]);
      if(!root.isConnected)return;
      renderOperational(platform.status==='fulfilled'?platform.value:null);
      const sessions=catalog.status==='fulfilled'?catalog.value:null;
      if(sessions){
        renderKpis({sessionCount:sessions.length,targetCount:new Set(sessions.map(s=>s.target)).size,integrationHours:sessions.reduce((sum,s)=>sum+Number(s.integrationHours||0),0),validatedCount:sessions.filter(s=>s.qualityState==='VALIDATED_ANALYTICS').length});
        renderRecent(sessions);
      }else recent.textContent='Catalogo corrente non disponibile.';
      renderCoverage(sessions,gallery.status==='fulfilled'?gallery.value:null,transfer.status==='fulfilled'?transfer.value:null);
      const failures=[catalog.status!=='fulfilled'?'catalogo':null,gallery.status!=='fulfilled'?'gallery':null,transfer.status!=='fulfilled'?'pacchetti':null,platform.status!=='fulfilled'?'baseline AP-013':null].filter(Boolean);
      status.textContent=`Copertura aggregata dell’intero catalogo · riletta alle ${new Intl.DateTimeFormat('it-IT',{timeStyle:'medium'}).format(new Date())}. ${failures.length?`Fonti non verificabili: ${failures.join(', ')}.`:'Fonti correnti disponibili.'} Aggiornamento ogni minuto mentre la pagina è visibile.`;
    }finally{button.disabled=false;}
  };
  button.addEventListener('click',refresh);
  const visible=()=>{if(root.isConnected && document.visibilityState==='visible')refresh();};
  document.addEventListener('visibilitychange',visible);
  const timer=setInterval(()=>{if(!root.isConnected){clearInterval(timer);document.removeEventListener('visibilitychange',visible);return;}visible();},60000);
  refresh();
  };
  if(window.DSG?.components){window.DSG.components.register({name:'mission-control',order:67,initialize});return;}
  const fallback=()=>initialize();
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',fallback,{once:true});else fallback();
  if(window.document$?.subscribe)window.document$.subscribe(fallback);
})();
