const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmt=v=>v.toLocaleString('it-IT',{maximumFractionDigits:3});
const date=t=>new Date(t).toLocaleDateString('it-IT',{day:'2-digit',month:'short',year:'numeric',timeZone:'UTC'});
export function skyPoints(data){
 if(data.dimension!=='SQM_MEDIAN'||data.unit!=='mag/arcsec2') throw Error('Dimensione SQM non compatibile');
 return data.includedSessions.map(s=>{
  const day=s.sessionId?.slice(0,10),time=Date.parse(`${day}T00:00:00Z`);
  if(!/^\d{4}-\d{2}-\d{2}$/.test(day)||!Number.isFinite(time)||new Date(time).toISOString().slice(0,10)!==day||!Number.isFinite(s.value)||s.unit!==data.unit||s.quality!=='AVAILABLE'||s.completeness!=='COMPLETE'||!s.provenanceRef) throw Error('Misura SQM non rappresentabile');
  return {...s,time};
 }).sort((a,b)=>a.time-b.time||a.sessionId.localeCompare(b.sessionId));
}
export function skyChart(data){
 const points=skyPoints(data);
 if(!points.length) return '<section class="dsg-sc-panel"><h2>Luminosità del cielo</h2><p>Nessuna misura SQM disponibile.</p></section>';
 const values=points.map(p=>p.value),lo=Math.floor((Math.min(...values)-.15)*2)/2,hi=Math.ceil((Math.max(...values)+.15)*2)/2;
 const first=points[0],last=points.at(-1);
 const x=t=>first.time===last.time?440:70+(t-first.time)/(last.time-first.time)*740;
 const y=v=>260-(v-lo)/(hi-lo)*210;
 let path='';points.forEach((p,i)=>{path+=`${i&&p.time-points[i-1].time<=86400000?'L':'M'}${x(p.time)},${y(p.value)} `;});
 return `<section class="dsg-sky-chart" aria-label="Andamento della luminosità del cielo"><header><div><span class="dsg-sky-eyebrow">MANCIANO / SKY HISTORY</span><h2>Luminosità del cielo nel tempo</h2><p>Mediana SQM per notte · mag/arcsec²</p></div><div class="dsg-sky-latest"><small>ULTIMA NOTTE MISURATA</small><strong>${fmt(last.value)}</strong><span>${date(last.time)}</span></div></header><p>Valori più alti indicano un cielo più buio. La misura non descrive da sola seeing, nuvole o idoneità della sessione.</p><div class="dsg-sky-plot"><svg viewBox="0 0 880 310" role="group" aria-label="Mediane SQM: ogni punto apre il dettaglio della sessione"><defs><linearGradient id="sky-line"><stop stop-color="#75e9f2"/><stop offset="1" stop-color="#b8a0ff"/></linearGradient></defs>${[0,1,2,3,4].map(i=>{const v=lo+(hi-lo)*i/4;return `<line x1="70" x2="810" y1="${y(v)}" y2="${y(v)}"/><text x="55" y="${y(v)+5}" text-anchor="end">${fmt(v)}</text>`;}).join('')}<path d="${path}" fill="none" stroke="url(#sky-line)" stroke-width="3"/>${points.map(p=>`<a href="../scientific-session-detail/?sessionId=${encodeURIComponent(p.sessionId)}" data-sky-point aria-label="${esc(p.sessionId)}: ${fmt(p.value)} mag/arcsec²"><title>${esc(p.sessionId)} · ${fmt(p.value)} mag/arcsec²</title><circle cx="${x(p.time)}" cy="${y(p.value)}" r="13" fill="transparent"/><circle cx="${x(p.time)}" cy="${y(p.value)}" r="5" fill="#83e8ec" stroke="#081625" stroke-width="2"/></a>`).join('')}<text x="70" y="295">${date(first.time)}</text><text x="810" y="295" text-anchor="end">${date(last.time)}</text></svg></div><footer><span>${points.length} notti misurate · ${data.exclusions.length} sessioni escluse</span><span>Scala verticale adattata ai valori · intervalli senza misure non collegati</span></footer><details><summary>Valori e provenienza</summary><div class="dsg-sky-table"><table><thead><tr><th>Notte</th><th>Mediana SQM</th><th>Provenienza</th></tr></thead><tbody>${points.map(p=>`<tr><td>${esc(p.sessionId)}</td><td>${fmt(p.value)} mag/arcsec²</td><td>${esc(p.provenanceRef)}</td></tr>`).join('')}</tbody></table></div></details></section>`;
}
