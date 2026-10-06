/* Public projection of reviewed photos. Original binaries never have public URLs. */
(() => {
  'use strict';
  const initialize=()=>{
    const link=document.querySelector('[data-session-photo-upload]');
    if(link){const update=()=>{const url=new URL(link.href);const id=new URLSearchParams(location.search).get('sessionId');if(id)url.searchParams.set('sessionId',id);link.href=url.href;};update();if(!link.dataset.photoLinked){link.dataset.photoLinked='true';link.addEventListener('click',update);}}
    const host=document.querySelector('[data-session-photo-gallery]');if(!host || host.dataset.initialized)return;host.dataset.initialized='true';
    const grid=host.querySelector('[data-gallery-grid]'),status=host.querySelector('[data-gallery-count]'),search=host.querySelector('[data-gallery-search]');
    let records=[],sequence=0;search.value=new URLSearchParams(location.search).get('sessionId') || '';
    const el=(tag,text,parent)=>{const node=document.createElement(tag);if(text!==undefined)node.textContent=text;parent?.append(node);return node;};
    const render=()=>{
      const query=search.value.toLocaleLowerCase();const filtered=records.filter(r=>`${r.title} ${r.target} ${r.sessionIds.join(' ')}`.toLocaleLowerCase().includes(query));
      grid.replaceChildren();status.textContent=`${filtered.length} immagini pubblicate`;
      if(!filtered.length)el('p',records.length?'Nessun risultato.':'Nessuna immagine ancora pubblicata.',grid);
      for(const record of filtered){
        const card=el('article',undefined,grid);card.className='dsg-image-card';const image=el('img',undefined,card);image.src=record.previewUrl;image.alt=record.title;image.loading='lazy';image.style.maxWidth='100%';
        el('h2',record.title,card);el('p',`${record.target} · elaborazione ${record.processingDate}`,card);
        for(const id of record.sessionIds){const link=el('a',id,card);const url=new URL('scientific-session-detail/',window.DSGPhotoApi.base);url.searchParams.set('sessionId',id);link.href=url.href;el('br',undefined,card);}
        el('p',`Versione ${record.imageVersionId}`,card);el('p',`${record.associationEvidence==='HISTORICAL_OWNER_DECLARATION'?'Riprese storiche dichiarate dall’autore; sessioni non importate.':'Sessioni dichiarate dall’autore.'} Workflow ${record.captureCompleteness==='PARTIAL'?'parziale':'non disponibile'}. Esecuzione non verificata.`,card);
        const details=el('details',undefined,card);el('summary','Leggi workflow',details);
        for(const step of record.steps){el('h3',`${step.sourceOrdinal}. ${step.processId}`,details);for(const p of step.parameters)el('pre',`${p.name}: ${p.lexicalJson}`,details);}
        if(!record.steps.length)el('p','Nessun passaggio disponibile per questa versione.',details);
        el('p','Visibile fino al ritiro esplicito.',details);
      }
    };
    const load=async()=>{
      const current=++sequence;
      records=[];grid.replaceChildren();status.textContent='Verifica delle immagini pubblicate…';
      try{
        if(!window.DSGScientificDataEngine)await new Promise((resolve,reject)=>{const script=el('script');script.src=new URL('javascripts/scientific-data-engine.js',window.DSGPhotoApi.base);script.onload=resolve;script.onerror=reject;document.head.append(script);});
        const collection=await window.DSGScientificDataEngine.getSessionPhotoCollection();if(!host.isConnected || current!==sequence)return;records=collection.records;render();
      }catch{if(!host.isConnected || current!==sequence)return;status.textContent='Archivio delle sessioni non ancora disponibile. Le immagini già pubblicate con workflow sono consultabili qui sotto.';}
    };
    search.addEventListener('input',render);host.querySelector('[data-gallery-reset]').addEventListener('click',()=>{search.value='';load();});
    load();
  };
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',initialize);else initialize();window.document$?.subscribe(initialize);
})();
