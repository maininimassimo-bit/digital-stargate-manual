(() => {
  const host = document.querySelector('[data-bkl034-gallery]');
  if (!host) return;
  const source = host.dataset.source;
  const esc = value => String(value ?? '').replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const grid = host.querySelector('[data-gallery-grid]');
  const count = host.querySelector('[data-gallery-count]');
  const search = host.querySelector('[data-gallery-search]');
  const state = host.querySelector('[data-gallery-state]');
  const reset = host.querySelector('[data-gallery-reset]');
  let items = [];

  const failClosed = () => {
    count.textContent = 'Projection non disponibile';
    grid.innerHTML = '<article class="dsg-image-gallery__empty dsg-image-gallery__empty--fail"><strong>Gallery non disponibile</strong><span>Fail-closed: nessun dato viene inferito o sostituito.</span></article>';
  };

  const valid = payload => payload && payload.schemaVersion === '1.0' && payload.authority === 'projection' && payload.commandAuthority === 'NONE' && payload.safetyAuthority === 'NONE' && Array.isArray(payload.items) && payload.items.length > 0 && payload.items.length <= 12 && payload.items.every(item => item && item.assetType === 'scientific_image' && ['observed','stale','unknown','unavailable'].includes(item.state) && ['current','stale','unknown','not_applicable'].includes(item.freshness) && String(item.sessionRef).startsWith('session:') && String(item.targetRef).startsWith('target:') && Array.isArray(item.provenanceRefs) && item.provenanceRefs.length > 0 && Array.isArray(item.sourceRefs) && item.sourceRefs.every(ref => String(ref).startsWith('src:')));
  const matches = item => {
    const needle = search.value.trim().toLowerCase();
    const haystack = [item.id, item.sessionRef, item.targetRef, ...(item.provenanceRefs || []), ...(item.sourceRefs || [])].join(' ').toLowerCase();
    return (!needle || haystack.includes(needle)) && (!state.value || item.state === state.value);
  };
  const refs = values => values.map(value => `<code>${esc(value)}</code>`).join(' ');
  const render = () => {
    const visible = items.filter(matches);
    count.textContent = `${visible.length} di ${items.length} projection`;
    if (!visible.length) { grid.innerHTML = '<article class="dsg-image-gallery__empty">Nessun item corrisponde ai filtri.</article>'; return; }
    grid.innerHTML = visible.map(item => `<article class="dsg-image-card"><div class="dsg-image-card__preview" aria-label="Preview non materializzata per ${esc(item.id)}"><span>IMAGE<br>PROJECTION</span></div><div class="dsg-image-card__body"><div class="dsg-image-card__topline"><code>${esc(item.id)}</code><span class="dsg-image-card__state dsg-image-card__state--${esc(item.state)}">${esc(item.state)}</span></div><h2>${esc(item.targetRef.replace('target:', ''))}</h2><dl><div><dt>Sessione</dt><dd>${esc(item.sessionRef)}</dd></div><div><dt>Freshness</dt><dd>${esc(item.freshness)}</dd></div><div><dt>Provenance</dt><dd>${refs(item.provenanceRefs)}</dd></div><div><dt>Source</dt><dd>${refs(item.sourceRefs)}</dd></div></dl><p class="dsg-image-card__caption">${esc(item.caption || 'Projection read-only')}</p></div></article>`).join('');
  };
  search.addEventListener('input', render); state.addEventListener('change', render); reset.addEventListener('click', () => { search.value = ''; state.value = ''; render(); });
  fetch(source, { cache: 'no-store' }).then(response => { if (!response.ok) throw new Error(`HTTP ${response.status}`); return response.json(); }).then(payload => { if (!valid(payload)) throw new Error('BKL-034 projection boundary mismatch'); items = payload.items; render(); }).catch(failClosed);
})();
