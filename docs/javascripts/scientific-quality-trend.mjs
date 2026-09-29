// Presentation only: values come from the already validated quality projection.
export function buildQualityTrend(projection, catalog) {
  const sessions = new Map(catalog.sessions.map(s => [s.sessionId, s]));
  const groups = new Map();
  let unknownSetup = 0;
  for (const item of projection.assessments) {
    const s = sessions.get(item.sessionId);
    if (!s?.configurationId || s.configurationId === 'UNKNOWN') { unknownSetup++; continue; }
    if (!groups.has(s.configurationId)) groups.set(s.configurationId, {
      id: s.configurationId, label: `${s.telescope} · ${s.camera}`, points: [], excluded: 0
    });
    const group = groups.get(s.configurationId);
    const day = s.observationDate;
    let time = /^\d{4}-\d{2}-\d{2}$/.test(day || '') ? Date.parse(`${day}T00:00:00Z`) : NaN;
    if (Number.isFinite(time) && new Date(time).toISOString().slice(0,10) !== day) time = NaN;
    const value = item.assessment?.score?.value;
    const valid = item.projectionRecordState === 'AVAILABLE' && Number.isFinite(value) && value >= 0 && value <= 100 && Number.isFinite(time);
    if (!valid) group.excluded++;
    group.points.push({ sessionId: item.sessionId, target: item.target, day, time, value: valid ? value : null, state: item.projectionRecordState });
  }
  const series = [...groups.values()].sort((a,b) => a.id.localeCompare(b.id));
  series.forEach(g => g.points.sort((a,b) => (a.time - b.time) || a.sessionId.localeCompare(b.sessionId)));
  return { series, unknownSetup };
}

const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const num = v => v.toLocaleString('it-IT', { maximumFractionDigits: 2 });
const dayLabel = d => new Date(d).toLocaleDateString('it-IT', {day:'2-digit',month:'short',timeZone:'UTC'});

export function renderQualityTrend(host, projection, catalog) {
  const {series, unknownSetup} = buildQualityTrend(projection, catalog);
  const dated = series.flatMap(g => g.points).filter(p => Number.isFinite(p.time));
  const valid = dated.filter(p => p.value !== null);
  const times = dated.map(p => p.time);
  const min = Math.min(...times), max = Math.max(...times);
  const x = t => min === max ? 328 : 52 + (t-min)/(max-min)*552;
  const y = v => 240-v*2;
  const colors = ['#65e4ee','#f6bb70','#bfadff'];
  const description = p => `${dayLabel(p.time)} · ${p.target} · score ${num(p.value)} / 100`;
  const paths = series.map((g,i) => {
    let d = '', connected = false;
    for (const p of g.points) {
      if (p.value === null || !Number.isFinite(p.time)) { connected = false; continue; }
      d += `${connected?'L':'M'}${x(p.time).toFixed(2)},${y(p.value).toFixed(2)} `; connected = true;
    }
    return `<g data-series="${i}" style="color:${colors[i%colors.length]}"><path d="${d}" fill="none" stroke="currentColor" stroke-width="2.5"/>${g.points.filter(p => p.value !== null).map(p => `<a href="../scientific-session-detail/?sessionId=${encodeURIComponent(p.sessionId)}" aria-label="${esc(g.label+' · '+description(p))}" data-readout="${esc(description(p))}"><title>${esc(g.label+' · '+description(p))}</title><circle cx="${x(p.time)}" cy="${y(p.value)}" r="12" fill="transparent"/><circle cx="${x(p.time)}" cy="${y(p.value)}" r="4.5" fill="${colors[i%colors.length]}" stroke="#081625" stroke-width="2"/></a>`).join('')}</g>`;
  }).join('');
  host.innerHTML = `<header><span class="dsg-trend-eyebrow">SESSION QUALITY / HISTORY</span><h2>Score nel tempo</h2><p>Sessioni separate per setup · scala 0–100</p></header>
    <div class="dsg-trend-legend">${series.map((g,i) => `<button type="button" data-toggle="${i}" aria-pressed="true" style="--series-color:${colors[i%colors.length]}"><i></i><span>${esc(g.label)}<small>${g.points.length-g.excluded} score · ${g.excluded} non disponibili</small></span></button>`).join('')}</div>
    ${valid.length ? `<svg viewBox="0 0 640 280" role="group" aria-label="Andamento dello score sperimentale per setup. Ogni punto apre la sessione.">${[0,25,50,75,100].map(v=>`<line x1="52" x2="604" y1="${y(v)}" y2="${y(v)}" stroke="#aecbd5" stroke-opacity=".14"/><text x="38" y="${y(v)+4}" text-anchor="end">${v}</text>`).join('')}${paths}<text x="52" y="268">${dayLabel(min)}</text><text x="604" y="268" text-anchor="end">${dayLabel(max)}</text></svg>` : '<p class="dsg-trend-empty">Nessuno score disponibile per i setup identificati.</p>'}
    <p class="dsg-trend-readout" aria-live="polite">Seleziona un punto per aprire la sessione.</p>
    <footer><p>${valid.length} score disponibili · ${unknownSetup} sessioni con setup non identificato. I valori mancanti interrompono le linee.</p><p>Score sperimentale · nessun ranking o giudizio sull’immagine.</p><details><summary>Valori e sessioni</summary><div class="dsg-trend-table"><table><thead><tr><th>Setup / sessione</th><th>Data</th><th>Score</th></tr></thead><tbody>${series.flatMap(g=>g.points.map(p=>`<tr><td>${esc(g.label)}<br><a href="../scientific-session-detail/?sessionId=${encodeURIComponent(p.sessionId)}">${esc(p.sessionId)}</a></td><td>${esc(p.day || 'Non disponibile')}</td><td>${p.value === null ? esc(p.state === 'AVAILABLE' ? 'Non rappresentabile' : p.state) : num(p.value)}</td></tr>`)).join('')}</tbody></table></div></details></footer>`;
  host.querySelectorAll('[data-toggle]').forEach(button => button.addEventListener('click', () => {
    const active = button.getAttribute('aria-pressed') !== 'true';
    button.setAttribute('aria-pressed', String(active));
    const group = host.querySelector(`[data-series="${button.dataset.toggle}"]`);
    if (group) group.style.display = active ? '' : 'none';
  }));
  host.querySelectorAll('[data-readout]').forEach(point => {
    const show = () => { host.querySelector('.dsg-trend-readout').textContent = point.dataset.readout; };
    point.addEventListener('pointerenter', show); point.addEventListener('focus', show);
  });
}
