(() => {
  const host = document.querySelector('[data-equipment-performance]');
  if (!host) return;
  const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const refs=(title,values)=>`<details><summary>${esc(title)}</summary><code>${(values||[]).map(esc).join('<br>')}</code></details>`;
  const statisticLabel=value=>({MEAN:'Mean',MINIMUM:'Minimum',MAXIMUM:'Maximum',SAMPLE_STDDEV:'Sample stddev'}[value]||value);
  const fail=()=>{host.innerHTML='<section class="dsg-ep-panel dsg-ep-fail"><h2>Projection non disponibile</h2><p>Fail-closed: il browser non inferisce valori, stato dell’attrezzatura o raccomandazioni.</p></section>';};
  const valid=v=>v&&v.authority==='projection'&&v.action_authority==='NONE'&&v.unit==='NINA_FILENAME_FWHM_SOURCE_UNIT'&&v.unit_semantics==='SOURCE_NATIVE_UNCALIBRATED'&&v.angular_calibration_state==='NOT_PROVEN'&&Array.isArray(v.measurements)&&Array.isArray(v.statistics)&&v.measurements.length===v.measurement_count&&Array.isArray(v.limitations)&&v.limitations.includes('NO_EQUIPMENT_HEALTH_RANKING_THRESHOLD_OR_RECOMMENDATION')&&v.limitations.includes('HISTORICAL_READ_ONLY_PROJECTION_NOT_SAFETY_AUTHORITY');
  const render=v=>{
    if(!valid(v)) throw new Error('population drift');
    const stats=v.statistics.map(s=>`<article><span>${esc(statisticLabel(s.statistic_type))}</span><strong>${esc(s.value)}</strong><small>${esc(v.unit)}</small><code>${esc(s.method_id)}</code></article>`).join('');
    const rows=v.measurements.map(m=>`<tr><td>${esc(m.sequence_number)}</td><td>${esc(m.timestamp)}</td><td>${esc(m.value)}</td><td><code>${esc(m.source_record_ref)}</code></td></tr>`).join('');
    const limitations=v.limitations.map(x=>`<li><code>${esc(x)}</code></li>`).join('');
    const content=document.querySelector('[data-equipment-performance-view]');
    content.innerHTML=`<section class="dsg-ep-context"><article><span>CONFIGURATION</span><strong>${esc(v.configuration_id)}</strong></article><article><span>SESSION</span><strong>${esc(v.session_id)}</strong></article><article><span>TARGET / FILTER</span><strong>${esc(v.target_name)} · ${esc(v.filter_name)}</strong></article><article><span>POPULATION</span><strong>${esc(v.measurement_count)} ${esc(v.frame_type)}</strong><small>${esc(v.coverage)}</small></article></section><section class="dsg-ep-panel"><span>DESCRIPTIVE STATISTICS</span><h2>${esc(v.metric_name)} · source-native unit</h2><p>Unit semantics: <code>${esc(v.unit_semantics)}</code> · angular calibration: <code>${esc(v.angular_calibration_state)}</code></p><div class="dsg-ep-stats">${stats}</div></section><section class="dsg-ep-panel"><span>MEASUREMENTS</span><h2>Source-backed population</h2><div class="dsg-ep-table-wrap"><table><thead><tr><th>#</th><th>Timestamp</th><th>FWHM</th><th>Source record</th></tr></thead><tbody>${rows}</tbody></table></div></section><section class="dsg-ep-panel"><span>LINEAGE</span><h2>Citation &amp; Provenance</h2>${refs('Citation',v.citation_refs)}${refs('Provenance',v.provenance_refs)}${refs('All source records',v.source_record_refs)}</section><section class="dsg-ep-panel"><span>LIMITATIONS</span><h2>Interpretation boundary</h2><ul>${limitations}</ul></section>`;
  };
  fetch('../data/equipment-performance-registry-f5-collection.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw new Error('projection unavailable');return r.json();}).then(data=>{
    if(data.component!=='DSG.EquipmentPerformanceRegistry.F5.CollectionReadModel'||data.authority!=='projection'||data.action_authority!=='NONE'||!Array.isArray(data.views)||data.views.length!==data.population_count||!data.views.length) throw new Error('collection drift');
    if(!data.views.every(valid)) throw new Error('population drift');
    const options=data.views.map((v,i)=>`<option value="${i}">${esc(v.session_id)} · ${esc(v.target_name)} · ${esc(v.configuration_id)} · ${esc(v.filter_name)} · n=${esc(v.measurement_count)}</option>`).join('');
    host.innerHTML=`<section class="dsg-ep-panel"><span>POPULATION SELECTOR</span><h2>Dynamic multi-session registry</h2><p><label for="dsg-ep-population">Session / target / configuration / filter</label><br><select id="dsg-ep-population">${options}</select></p><small>${esc(data.population_count)} eligible population(s); excluded populations remain fail-closed.</small></section><div data-equipment-performance-view></div>`;
    const selector=document.getElementById('dsg-ep-population');
    selector.addEventListener('change',()=>render(data.views[Number(selector.value)]));
    render(data.views[0]);
  }).catch(fail);
})();
